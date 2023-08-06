# -*- coding: utf-8 -*-
"""This module defines functions for querying the PolyPhen-2 online tool,
parsing its output and deriving features that will be used by the Rhapsody
classifiers.
"""

from prody import LOGGER
import numpy as np
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from math import log

__all__ = ['PP2_FEATS', 'queryPolyPhen2', 'parsePolyPhen2output',
           'getSAVcoords', 'calcPolyPhen2features']

PP2_FEATS = ['wt_PSIC', 'Delta_PSIC']
"""List of features derived from PolyPhen-2's output."""

pph2_columns = ['o_acc', 'o_pos', 'o_aa1', 'o_aa2', 'rsid',
                'acc', 'pos', 'aa1', 'aa2', 'nt1', 'nt2',
                'prediction', 'based_on', 'effect', 'pph2_class',
                'pph2_prob', 'pph2_FPR', 'pph2_TPR', 'pph2_FDR',
                'site', 'region', 'PHAT', 'dScore', 'Score1',
                'Score2', 'MSAv', 'Nobs', 'Nstruct', 'Nfilt',
                'PDB_id', 'PDB_pos', 'PDB_ch', 'ident', 'length',
                'NormASA', 'SecStr', 'MapReg', 'dVol', 'dProp',
                'B-fact', 'H-bonds', 'AveNHet', 'MinDHet', 'AveNInt',
                'MinDInt', 'AveNSit', 'MinDSit', 'Transv', 'CodPos',
                'CpG', 'MinDJxn', 'PfamHit', 'IdPmax', 'IdPSNP',
                'IdQmin', 'other']


def _requests_retry_session(retries=10, timeout=1, backoff_factor=0.3,
                            status_forcelist=(404,), session=None):
    # https://www.peterbe.com/plog/best-practice-with-retries-with-requests
    session = session or requests.Session()
    retry = Retry(total=retries, read=retries, connect=retries,
                  backoff_factor=backoff_factor,
                  status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def queryPolyPhen2(filename, dump=True, prefix='pph2', **kwargs):
    # original PolyPhen-2 curl command (see:
    # http://genetics.bwh.harvard.edu/pph2/dokuwiki/faq ):
    #
    # curl  -F _ggi_project=PPHWeb2  -F _ggi_origin=query         \
    # -F _ggi_target_pipeline=1  -F MODELNAME=HumDiv              \
    # -F UCSCDB=hg19  -F SNPFUNC=m  -F NOTIFYME=myemail@myisp.com \
    # -F _ggi_batch_file=@example_batch.txt                       \
    # -D - http://genetics.bwh.harvard.edu/cgi-bin/ggi/ggi2.cgi

    assert type(dump) is bool
    assert type(prefix) is str

    LOGGER.info('Submitting query to PolyPhen-2...')
    num_lines = sum(1 for line in open(filename, 'rb') if line[0] != '#')
    input_file = open(filename, 'rb')
    # submit query
    address = 'http://genetics.bwh.harvard.edu/cgi-bin/ggi/ggi2.cgi'
    files = {'_ggi_project': (None, 'PPHWeb2'),
             '_ggi_origin': (None, 'query'),
             '_ggi_target_pipeline': (None, '1'),
             '_ggi_batch_file': ('query.txt', input_file),
             'MODELNAME': (None, kwargs.get('MODELNAME', 'HumDiv')),
             'UCSCDB':    (None, kwargs.get('UCSCDB', 'hg19')),
             'SNPFUNC':   (None, kwargs.get('SNPFUNC', 'm'))}
    response = requests.post(address, files=files)
    # parse job ID from response page
    jobID = response.cookies['polyphenweb2']
    # results and semaphore files
    results_dir = f'http://genetics.bwh.harvard.edu/ggi/pph2/{jobID}/1/'
    files = {'started':   results_dir + 'started.txt',
             'completed': results_dir + 'completed.txt',
             'short':     results_dir + 'pph2-short.txt',
             'full':      results_dir + 'pph2-full.txt',
             'log':       results_dir + 'pph2-log.txt',
             'snps':      results_dir + 'pph2-snps.txt'}
    # keep checking if the job has started/completed and,
    # when done, fetch output files
    output = {}
    for k in ['started', 'completed', 'short', 'full', 'log', 'snps']:
        # delay = timeout + backoff_factor*[2^(total_retries - 1)]
        if k == 'started':
            LOGGER.timeit('_started')
            r = _requests_retry_session(retries=16, timeout=0,
                                        backoff_factor=0.1).get(files[k])
            LOGGER.report('Query to PolyPhen-2 started in %.1fs.', '_started')
            LOGGER.info('PolyPhen-2 is running...')
        elif k == 'completed':
            LOGGER.timeit('_queryPP2')
            r = _requests_retry_session(retries=12, timeout=log(num_lines)/2,
                                        backoff_factor=0.2).get(files[k])
            LOGGER.report('Query to PolyPhen-2 completed in %.1fs.',
                          '_queryPP2')
        else:
            r = _requests_retry_session(retries=12, timeout=0,
                                        backoff_factor=0.01).get(files[k])
        output[k] = r
        # print to file, if requested
        if dump:
            with open(prefix + '-' + k + '.txt', 'w', 1) as f:
                print(r.text, file=f)

    return output


def parsePolyPhen2output(pph2_output):
    '''Import PolyPhen-2 results directly from the output of
    'queryPolyPhen2' or from a file (in 'full' format).
    '''
    assert type(pph2_output) in [dict, str]
    if type(pph2_output) is dict:
        lines = pph2_output['full'].text.split('\n')
    else:
        with open(pph2_output, 'r') as file:
            lines = file.readlines()
    # discard invalid lines
    lines = [l for l in lines if l.strip() and l[0] != '#']
    if not lines:
        msg = ("PolyPhen-2's output is empty. Please make sure that: \n"
               "1) variants' format is correct "
               '(\"UniprotID pos wt_aa mut_aa\") \n'
               "2) query contains *human* variants \n")
        raise RuntimeError(msg)
    # define a structured array
    pl_dtype = np.dtype([(col, 'U25') for col in pph2_columns])
    parsed_lines = np.zeros(len(lines), dtype=pl_dtype)
    # fill structured array
    n_cols = len(pph2_columns)
    for i, line in enumerate(lines):
        # parse line
        words = [w.strip() for w in line.split('\t')]
        # check format
        n_words = len(words)
        if n_words == n_cols - 1:
            # manually insert null 'other' column
            words.append('?')
        elif n_words != n_cols:
            msg = 'Incorrect number of columns: {}'.format(n_words)
            raise ValueError(msg)
        # import to structured array
        parsed_lines[i] = tuple(words)
    LOGGER.info("PolyPhen-2's output parsed.")
    return parsed_lines


def getSAVcoords(parsed_lines):
    """Extracts SAV Uniprot coordinates as provided by the user. If not
    possible, the Uniprot coordinates computed by PolyPhen-2 will be returned.
    A string containing the original submitted SAV is returned as well.
    """
    SAV_dtype = np.dtype([('acc', 'U15'), ('pos', 'i'),
                          ('aa_wt', 'U1'), ('aa_mut', 'U1'),
                          ('text', 'U25')])
    SAV_coords = np.empty(len(parsed_lines), dtype=SAV_dtype)
    for i, line in enumerate(parsed_lines):
        o_acc = line['o_acc']
        if o_acc.startswith('rs') or o_acc.startswith('chr'):
            # recover Uniprot accession number from PolyPhen-2 output
            acc = line['acc']
            pos = int(line['pos'])
            aa1 = line['aa1']
            aa2 = line['aa2']
            SAV_str = o_acc
        else:
            acc = line['o_acc']
            pos = int(line['o_pos'])
            aa1 = line['o_aa1']
            aa2 = line['o_aa2']
            SAV_str = '{} {} {} {}'.format(acc, pos, aa1, aa2)
        SAV_coords[i] = (acc, pos, aa1, aa2, SAV_str)
    return SAV_coords


def calcPolyPhen2features(PolyPhen2output):
    # define a datatype for sequence-conservation features
    # extracted from the output of PolyPhen-2
    feat_dtype = np.dtype([('wt_PSIC', 'f'),
                           ('Delta_PSIC', 'f')])
    # import selected quantities from PolyPhen-2's output
    # into a structured array
    f_l = PolyPhen2output[['Score1', 'dScore']]
    f_t = [tuple(np.nan if x == '?' else x for x in l) for l in f_l]
    features = np.array(f_t, dtype=feat_dtype)
    LOGGER.info("Sequence-conservation features have been "
                "retrieved from PolyPhen-2's output.")
    return features
