# -*- coding: utf-8 -*-
"""This module defines functions for training Random Forest classifiers
implementing Rhapsody's classification schemes."""

import pickle
import numpy as np
import numpy.lib.recfunctions as rfn
from prody import LOGGER
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, roc_auc_score, auc
from sklearn.metrics import precision_recall_curve, average_precision_score
from ..utils.settings import DEFAULT_FEATSETS, getDefaultTrainingDataset
from .figures import print_pred_distrib_figure, print_path_prob_figure
from .figures import print_ROC_figure, print_feat_imp_figure


__all__ = ['calcMetrics', 'calcPathogenicityProbs', 'RandomForestCV',
           'trainRFclassifier', 'extendDefaultTrainingDataset']


def calcMetrics(y_test, y_pred):
    # compute ROC and AUROC
    fpr, tpr, roc_thr = roc_curve(y_test, y_pred)
    auroc = roc_auc_score(y_test, y_pred)
    # compute optimal cutoff J (argmax of Youden's index)
    diff = np.array([y-x for x, y in zip(fpr, tpr)])
    Jopt = roc_thr[(-diff).argsort()][0]
    # compute Precision-Recall curve and AUPRC
    pre, rec, prc_thr = precision_recall_curve(y_test, y_pred)
    auprc = average_precision_score(y_test, y_pred)
    return {'FPR': fpr, 'TPR': tpr, 'ROC_thresholds': roc_thr,
            'AUROC': auroc, 'optimal cutoff': Jopt,
            'precision': pre, 'recall': rec, 'PRC_thresholds': prc_thr,
            'AUPRC': auprc}


def calcPathogenicityProbs(CV_info, num_bins=15,
                           ppred_reliability_cutoff=200,
                           pred_distrib_fig='predictions_distribution.png',
                           path_prob_fig='pathogenicity_prob.png', **kwargs):
    '''Compute pathogenicity probabilities,
    from predictions on CV test sets
    '''

    avg_Jopt = np.mean(CV_info['Youden_cutoff'])
    preds = [np.array(CV_info['predictions_0']),
             np.array(CV_info['predictions_1'])]

    # compute (normalized) histograms
    dx = 1./num_bins
    bins = np.arange(0, 1+dx, dx)
    histo = np.empty((2, len(bins)-1))
    norm_histo = np.empty_like(histo)
    for i in [0, 1]:
        h, _ = np.histogram(preds[i], bins, range=(0, 1))
        histo[i] = h
        norm_histo[i] = h/len(preds[i])

    # print predictions distribution figure
    if pred_distrib_fig is not None:
        print_pred_distrib_figure(pred_distrib_fig, bins, norm_histo,
                                  dx, avg_Jopt)

    # compute pathogenicity probability
    s = np.sum(norm_histo, axis=0)
    path_prob = np.divide(norm_histo[1], s, out=np.zeros_like(s),
                          where=(s != 0))

    # smooth path. probability profile and extend it to [0, 1] interval
    _smooth = _running_average(path_prob)
    # _smooth = _calcSmoothCurve(path_prob, 5)
    y_ext = np.concatenate([[0], _smooth, [1]])
    x_ext = np.concatenate([[0], bins[:-1]+dx/2, [1]])
    smooth_path_prob = np.array([x_ext, y_ext])

    # print pathogenicity probability figure
    if path_prob_fig is not None:
        print_path_prob_figure(path_prob_fig, bins, histo, dx, path_prob,
                               smooth_plot=smooth_path_prob,
                               cutoff=ppred_reliability_cutoff)

    return np.array(smooth_path_prob)


def _running_average(curve):
    ext_pprob = np.concatenate([[0], curve, [1]])
    return np.convolve(ext_pprob, np.ones((3,))/3, mode='valid')


def _calcSmoothCurve(curve, smooth_window):
    # smooth pathogenicity probability profile
    n = len(curve)
    smooth_curve = np.zeros_like(curve)
    for i in range(n):
        p = curve[i]
        sw = 0
        for k in range(1, smooth_window + 1):
            if (i-k < 0) or (i+k >= n):
                break
            else:
                sw = k
                p += curve[i-k] + curve[i+k]
        smooth_curve[i] = p / (1 + sw*2)
    return smooth_curve


def _performCV(X, y, n_estimators=1000, max_features='auto', n_splits=10,
               ROC_fig='ROC.png', feature_names=None, **kwargs):

    # set classifier
    classifier = RandomForestClassifier(
        n_estimators=n_estimators, max_features=max_features,
        oob_score=True, n_jobs=-1, class_weight='balanced')

    # set cross-validation procedure
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=666)

    # cross-validation loop
    CV_info = {
        'AUROC': [],
        'AUPRC': [],
        'feat_importance': [],
        'OOB_score': [],
        'Youden_cutoff': [],
        'predictions_0': [],
        'predictions_1': []
    }
    mean_tpr = 0.0
    mean_fpr = np.linspace(0, 1, 100)
    i = 0
    for train, test in cv.split(X, y):
        # create training and test datasets
        X_train = X[train]
        X_test = X[test]
        y_train = y[train]
        y_test = y[test]
        # train Random Forest classifier
        classifier.fit(X_train, y_train)
        # calculate probabilities over decision trees
        y_pred = classifier.predict_proba(X_test)
        # compute ROC, AUROC, optimal cutoff (argmax of Youden's index), etc...
        d = calcMetrics(y_test, y_pred[:, 1])
        auroc = d['AUROC']
        auprc = d['AUPRC']
        Jopt = d['optimal cutoff']
        # store other info and metrics for each iteration
        mean_tpr += np.interp(mean_fpr, d['FPR'], d['TPR'])
        oob_score = classifier.oob_score_
        CV_info['AUROC'].append(auroc)
        CV_info['AUPRC'].append(auprc)
        CV_info['feat_importance'].append(classifier.feature_importances_)
        CV_info['OOB_score'].append(oob_score)
        CV_info['Youden_cutoff'].append(Jopt)
        CV_info['predictions_0'].extend(y_pred[np.where(y_test == 0), 1][0])
        CV_info['predictions_1'].extend(y_pred[np.where(y_test == 1), 1][0])
        # print log
        i += 1
        LOGGER.info(f'CV iteration #{i:2d}:   AUROC = {auroc:.3f}   '
                    f'AUPRC = {auprc:.3f}   OOB score = {oob_score:.3f}')

    # compute average ROC, optimal cutoff and other stats
    mean_tpr /= cv.get_n_splits(X, y)
    mean_tpr[0] = 0.0
    mean_tpr[-1] = 1.0
    mean_auroc = auc(mean_fpr, mean_tpr)
    mean_auprc = np.mean(CV_info['AUPRC'])
    mean_oob = np.mean(CV_info['OOB_score'])
    avg_Jopt = np.mean(CV_info['Youden_cutoff'])
    std_Jopt = np.std(CV_info['Youden_cutoff'])
    avg_feat_imp = np.mean(np.array(CV_info['feat_importance']), axis=0)
    LOGGER.info('-'*60)
    LOGGER.info('Cross-validation summary:')
    LOGGER.info(f'training dataset size:   {len(y):<d}')
    LOGGER.info(f'fraction of positives:   {sum(y)/len(y):.3f}')
    LOGGER.info(f'mean AUROC:              {mean_auroc:.3f}')
    LOGGER.info(f'mean AUPRC:              {mean_auprc:.3f}')
    LOGGER.info(f'mean OOB score:          {mean_oob:.3f}')
    LOGGER.info(f'optimal cutoff*:         {avg_Jopt:.3f} +/- {std_Jopt:.3f}')
    LOGGER.info("(* argmax of Youden's index)")
    LOGGER.info('feature importances:')
    if feature_names is None:
        feature_names = [f'feature {i}' for i in range(len(avg_feat_imp))]
    for feat_name, importance in zip(feature_names, avg_feat_imp):
        LOGGER.info(f'{feat_name:>23s}: {importance:.3f}')
    LOGGER.info('-'*60)
    path_prob = calcPathogenicityProbs(CV_info, **kwargs)
    CV_summary = {
        'dataset size': len(y),
        'dataset bias': sum(y)/len(y),
        'mean AUROC': mean_auroc,
        'mean AUPRC': mean_auprc,
        'mean OOB score': mean_oob,
        'mean ROC': list(zip(mean_fpr, mean_tpr)),
        'optimal cutoff': (avg_Jopt, std_Jopt),
        'feat. importance': avg_feat_imp,
        'path. probability': path_prob
    }

    # plot average ROC
    if ROC_fig is not None:
        print_ROC_figure(ROC_fig, mean_fpr, mean_tpr, mean_auroc)

    return CV_summary


def _importFeatMatrix(fm):
    assert fm.dtype.names is not None, \
        "feat. matrix must be a NumPy structured array."
    assert 'true_label' in fm.dtype.names, \
        "feat. matrix must have a 'true_label' field."
    assert 'SAV_coords' in fm.dtype.names, \
        "feat. matrix must have a 'SAV_coords' field."
    assert set(fm['true_label']) == {0, 1}, \
        'Invalid true labels in feat. matrix.'

    # check for ambiguous cases in training dataset
    del_SAVs = set(fm[fm['true_label'] == 1]['SAV_coords'])
    neu_SAVs = set(fm[fm['true_label'] == 0]['SAV_coords'])
    amb_SAVs = del_SAVs.intersection(neu_SAVs)
    if amb_SAVs:
        raise RuntimeError('Ambiguous cases found in training dataset: {}'
                           .format(amb_SAVs))

    # eliminate rows containing NaN values from feature matrix
    featset = [f for f in fm.dtype.names
               if f not in ['true_label', 'SAV_coords']]
    sel = [~np.isnan(np.sum([x for x in r])) for r in fm[featset]]
    fms = fm[sel]
    n_i = len(fm)
    n_f = len(fms)
    dn = n_i - n_f
    if dn:
        LOGGER.info(f'{dn} out of {n_i} cases ignored with missing features.')

    # split into feature array and true label array
    X = np.array([[np.float32(x) for x in v] for v in fms[featset]])
    y = fms['true_label']

    return X, y, featset


def RandomForestCV(feat_matrix, n_estimators=1500, max_features=2, **kwargs):

    X, y, featset = _importFeatMatrix(feat_matrix)
    CV_summary = _performCV(
        X, y, n_estimators=n_estimators, max_features=max_features,
        feature_names=featset, **kwargs)
    return CV_summary


def trainRFclassifier(feat_matrix, n_estimators=1500, max_features=2,
                      pickle_name='trained_classifier.pkl',
                      feat_imp_fig='feat_importances.png', **kwargs):

    X, y, featset = _importFeatMatrix(feat_matrix)

    # calculate optimal Youden cutoff through CV
    CV_summary = _performCV(
        X, y, n_estimators=n_estimators, max_features=max_features,
        feature_names=featset, **kwargs)

    # train a classifier on the whole dataset
    clsf = RandomForestClassifier(
        n_estimators=n_estimators, max_features=max_features,
        oob_score=True, class_weight='balanced', n_jobs=-1)
    clsf.fit(X, y)

    fimp = clsf.feature_importances_
    LOGGER.info('-'*60)
    LOGGER.info('Classifier training summary:')
    LOGGER.info(f'mean OOB score:          {clsf.oob_score_:.3f}')
    LOGGER.info('feature importances:')
    for feat_name, importance in zip(featset, fimp):
        LOGGER.info(f'{feat_name:>23s}: {importance:.3f}')
    LOGGER.info('-'*60)

    if feat_imp_fig is not None:
        print_feat_imp_figure(feat_imp_fig, fimp, featset)

    train_info = {
        'del. SAVs': feat_matrix[feat_matrix['true_label'] == 1]['SAV_coords'],
        'neu. SAVs': feat_matrix[feat_matrix['true_label'] == 0]['SAV_coords']
    }

    clsf_dict = {
        'trained RF': clsf,
        'features': featset,
        'CV summary': CV_summary,
        'training dataset': train_info
    }

    # save pickle with trained classifier and other info
    if pickle_name is not None:
        pickle.dump(clsf_dict, open(pickle_name, 'wb'))

    return clsf_dict


def extendDefaultTrainingDataset(names, arrays, base_default_featset='full'):
    """base : array
    Input array to extend.

    names : string, sequence
    String or sequence of strings corresponding to the names of the new fields.

    data : array or sequence of arrays
    Array or sequence of arrays storing the fields to add to the base.
    """

    training_dataset = getDefaultTrainingDataset()

    # select features from integrated dataset
    if base_default_featset is None:
        base_featset = []
    if base_default_featset in DEFAULT_FEATSETS:
        base_featset = DEFAULT_FEATSETS[base_default_featset]
    else:
        base_featset = list(base_default_featset)
    featset = ['SAV_coords', 'true_label'] + base_featset
    base_dataset = training_dataset[featset]

    # extend base training dataset
    fm = rfn.rec_append_fields(base_dataset, names, arrays, dtypes='float32')

    return fm
