#!/usr/bin/env python

import argparse

import pandas as pd
import numpy as np
from statsmodels.stats.multitest import multipletests
from scipy.stats.stats import fisher_exact

from dSreg.utils.utils import LogTrack


def padjust(p_values, method='fdr_bh'):
    if p_values.shape[0] == 0:
        return([])
    return(multipletests(p_values, method=method)[1])


def calc_contingency_table(v1, v2):
    table = [[np.logical_and(v1, v2).sum(),
              np.logical_and(v1, v2 == False).sum()],
             [np.logical_and(v1 == False, v2).sum(),
             np.logical_and(v1 == False, v2 == False).sum()]]
    return(table)


def perform_ORA(events_labels, binding_sites, background_group,
                test_labels=['Included', 'Skipped']):
    
    if test_labels is None:
        test_labels = [x for x in np.unique(events_labels)
                       if x != background_group]
    
    for regulator in binding_sites.columns:
        v1 = binding_sites[regulator]
        
        for label in test_labels:
            v2 = events_labels == label
            if v2.sum(0) == 0:
                odds_ratio, pvalue = np.nan, np.nan
            else:
                table = calc_contingency_table(v1, v2)
                odds_ratio, pvalue = fisher_exact(table)
        
            record = {'regulator': regulator, 'OR': odds_ratio,
                      'pvalue': pvalue, 'group': label}
            yield(record)
            

def calc_enrichment_scores(sorted_idxs, scores):
    s = np.cumsum(scores.loc[sorted_idxs, :], axis=0)
    return(s.min(0), s.max(0))


def calc_null_enrichment_scores(scores, n=10000):
    rownames = np.arange(scores.shape[0])
    es_nulls = [[], []]
    for _ in range(n):
        np.random.shuffle(rownames)
        es_min, es_max = calc_enrichment_scores(rownames, scores)
        es_nulls[0].append(es_min)
        es_nulls[1].append(es_max)
    return(np.array(es_nulls[0]), np.array(es_nulls[1]))


def perform_GSEA(data, binding_sites, log, npermutations=10000,
                 key_field='dpsi'):
    data['id'] = data.index
    scores = binding_sites.astype(int)
    scores = scores - scores.mean(0)
    sorted_exon_ids = data.sort_values(key_field)['id']
    es_min, es_max = calc_enrichment_scores(sorted_exon_ids, scores)
    log.write('Generating null distribution: {}...'.format(npermutations))
    null_es_min, null_es_max = calc_null_enrichment_scores(scores,
                                                           n=npermutations)
    log.write('\tDone')
    p_skp = np.mean(np.vstack([es_min] * npermutations) < null_es_min, 0)
    p_inc = np.mean(np.vstack([es_max] * npermutations) > null_es_max, 0)

    for i, regulator in enumerate(binding_sites.columns):
        record = {'regulator': regulator, 'ES': es_max[i],
                  'pvalue': min(p_inc[i], 1), 'group': 'Included'}
        yield(record)
        record = {'regulator': regulator, 'ES': es_min[i],
                  'pvalue': min(p_skp[i], 1), 'group': 'Skipped'}
        yield(record)


def main():
    description = 'Run a simple over-representation analysis with a one-sided'
    description += 'Fisher test to find over-represented binding sites in '
    description += 'groups of events. Alternatively, GSEA can be performed if '
    description += 'estimations of dPSI are provided instead'

    # Create arguments
    parser = argparse.ArgumentParser(description=description)
    input_group = parser.add_argument_group('Input')
    help_msg = 'Input file:\nfor ORA a table with the groups\n'
    help_msg += 'for GSEA a table with the estimated dPSI'
    input_group.add_argument('input', help=help_msg)
    input_group.add_argument('-S', '--sites_matrix', required=True,
                             help='Event binding sites matrix')
    help_msg = 'Character separating columns for input file (,)'
    input_group.add_argument('-s', '--sep_character', default=',',
                             help=help_msg)

    filter_group = parser.add_argument_group('Filtering')
    filter_group.add_argument('-r', '--sel_regions', default=None,
                              help='File containing regions to filter')
    help_msg = 'Events bound by a regulator to be considered (5)'
    filter_group.add_argument('-me', '--min_events', default=5, type=int,
                              help=help_msg)

    options_group = parser.add_argument_group('Options')
    options_group.add_argument('-b', '--background_group', default='No-change',
                               help='Name of the background grouop (No-change)')
    options_group.add_argument('--gsea', default=False, action='store_true',
                               help='Run GSEA analysis on regulators')
    options_group.add_argument('-n', '--n_permutations',
                               default=10000, type=int,
                               help='Number of permutations for GSEA (10000)')
    options_group.add_argument('-k', '--key_field', default='dpsi',
                               help='Key field to sort for GSEA (dpsi)')

    output_group = parser.add_argument_group('Output')
    output_group.add_argument('-o', '--output', required=True,
                              help='Output file')

    # Parse arguments
    parsed_args = parser.parse_args()
    
    input_fpath = parsed_args.input
    binding_sites_fpath = parsed_args.sites_matrix
    sel_regions_fpath = parsed_args.sel_regions
    background_group = parsed_args.background_group
    min_events = parsed_args.min_events
    run_gsea = parsed_args.gsea
    key_field = parsed_args.key_field
    n_permutations = parsed_args.n_permutations
    sep = parsed_args.sep_character
    output_fpath = parsed_args.output

    # Init log
    log = LogTrack()
    log.write('Start data analysis...')

    # Load count data
    data = pd.read_csv(input_fpath, index_col=0, sep=sep) 
    log.write('Loaded {} events'.format(data.shape[0]))

    # Load and filter binding sites
    binding_sites = pd.read_csv(binding_sites_fpath).set_index('event_id')
    binding_sites = binding_sites.loc[data.index, :].fillna(0) > 0
    log.write('Loaded binding sites for {} RBPs'.format(binding_sites.shape[1]))

    if sel_regions_fpath is not None:
        sel_regions = set([line.strip() for line in open(sel_regions_fpath)])
        sel_cols = [x for x in binding_sites.columns
                    if x.split('.', 1)[-1] in sel_regions]
        binding_sites = binding_sites.loc[:, sel_cols]
        log.write('Filtered {} RBPs'.format(binding_sites.shape[1]))

    binding_sites = binding_sites.loc[:, binding_sites.sum(0) > min_events]
    log.write('Filtered {} RBPs >= {} events'.format(binding_sites.shape[1],
                                                     min_events))

    # Analysis
    if run_gsea:
        records = perform_GSEA(data, binding_sites, log, n_permutations,
                               key_field=key_field)
    else:
        records = perform_ORA(data['Group'], binding_sites, background_group)
    
    results = pd.DataFrame(records)
    results['fdr'] = padjust(results['pvalue'])
    results.sort_values('fdr', inplace=True)
    results.to_csv(output_fpath)
    log.finish()
    

if __name__ == '__main__':
    main()
