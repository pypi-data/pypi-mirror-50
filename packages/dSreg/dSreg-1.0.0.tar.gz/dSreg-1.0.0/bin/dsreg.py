#!/usr/bin/env python
import argparse

import numpy as np
import pandas as pd
from dSreg.dsreg_fit import dSregCounts
from dSreg.utils.settings import AVAILABLE_MODELS, DSREG_PW, VERSION


def main():
    description = 'dSreg performs simultaneous analysis of differential'
    description += 'inclusion and underlying regulatory mechanisms '
    description += 'using a bayesian model to integrate both layers '
    description += 'in a unique inferential step'

    # Create arguments
    parser = argparse.ArgumentParser(description=description)
    input_group = parser.add_argument_group('Input')
    input_group.add_argument('-I', '--inclusion', required=True,
                             help='Inclusion counts matrix')
    input_group.add_argument('-T', '--total', required=True,
                             help='Total counts matrix')
    input_group.add_argument('-S', '--sites_matrix', required=True,
                             help='Event binding sites matrix')
    input_group.add_argument('-d', '--design', required=True,
                             help='Matrix containing experimental design')
    
    bias_group = parser.add_argument_group('Reads bias corrections')
    help_msg = 'Correct inclusion reads bias. By default assume double chance'
    help_msg += ' to sample SJ reads supporting inclusion than skipping. '
    help_msg += 'Event specific correction can be done with -L'
    bias_group.add_argument('-b', '--inclusion_bias', default=False,
                            action='store_true', help=help_msg)
    help_msg = 'Matrix containing mappable lengths of inclusion and skipping '
    help_msg += 'forms to take into account differences in mappabilities'
    bias_group.add_argument('-L', '--lengths', default=None, help=help_msg)

    events_group = parser.add_argument_group('Event selection')
    help_msg = 'File containing events to keep in the analysis'
    events_group.add_argument('-k', '--keep_events', default=None,
                              help=help_msg)
    help_msg = 'Number of events to sample to reduce computational cost'
    events_group.add_argument('-K', '--event_number', default=None, type=int,
                              help=help_msg + ' (No sampling)')
    events_group.add_argument('--seed', default=None, type=int,
                              help='Seed for sampling (None)')

    filter_group = parser.add_argument_group('Filter events and regulators')
    help_msg = 'Minimum number of counts to consider an event (1)'
    filter_group.add_argument('-m', '--min_counts', default=1, type=int,
                              help=help_msg)
    help_msg = 'Min number of samples for counts filtering (1)'
    filter_group.add_argument('-s', '--min_samples', default=1, type=int,
                              help=help_msg)
    help_msg = 'Minimum number of inclusion counts in at least 1 sample (1)'
    filter_group.add_argument('-mi', '--min_inc_counts', default=1, type=int,
                              help=help_msg)
    help_msg = 'Minimum number of skipping counts in at least 1 sample (1)'
    filter_group.add_argument('-ms', '--min_skp_counts', default=1, type=int,
                              help=help_msg)
    filter_group.add_argument('-r', '--sel_regions', default=None,
                              help='File containing regions to filter')
    help_msg = 'Events bound by a regulator to be considered'
    filter_group.add_argument('-me', '--min_events', default=5, type=int,
                              help=help_msg)

    options_group = parser.add_argument_group('MCMC Options')
    options_group.add_argument('-t', '--nthreads', default=4, type=int,
                               help='Number of threads to fit the model (4)')
    options_group.add_argument('-c', '--nchains', default=4, type=int,
                               help='Number MCMC chains to fit the model (4)')
    options_group.add_argument('-n', '--n_samples', default=2000,  type=int,
                               help='Number of MCMC samples (2000)')

    model_group = parser.add_argument_group('Models options')
    model_group.add_argument('--recompile', default=False, action='store_true',
                             help='Recompile stan model before fitting')
    help_msg = 'Model to fit. Models available: {} ({})'
    model_group.add_argument('-M', '--model', default=DSREG_PW,
                             help=help_msg.format(AVAILABLE_MODELS, DSREG_PW))
    help_msg = 'Expected proportion of non-zero effect regulators (None)'
    model_group.add_argument('-e', '--exp_reg', default=None, help=help_msg)
    
#     help_msg = 'Shape parameter of the InvGamma prior for GP scale rho (6.4)'
#     model_group.add_argument('-gp_a', '--gp_scale_a', default=6.4, type=float,
#                              help=help_msg)
#     help_msg = 'Scale parameter of the InvGamma prior for GP scale rho (24.4)'
#     model_group.add_argument('-gp_b', '--gp_scale_b', default=24.4, type=float,
#                              help=help_msg)

    output_group = parser.add_argument_group('Output')
    output_group.add_argument('-a', '--all_params', default=False,
                              action='store_true',
                              help='Save also single exon PSI estimations')
    output_group.add_argument('-o', '--output_prefix', required=True,
                              help='Prefix for output files')
    output_group.add_argument('--log', default=None,
                              help='Log file (stderr)')
    
    other_group = parser.add_argument_group('Other options')
    other_group.add_argument('--event_ids', default=False, action='store_true',
                             help='Use event_id column as index of -S')
    other_group.add_argument('--version', action='version',
                             version='dSreg-{}'.format(VERSION))

    # Parse arguments
    parsed_args = parser.parse_args()
    inc_fpath = parsed_args.inclusion
    total_fpath = parsed_args.total
    binding_sites_fpath = parsed_args.sites_matrix
    design_fpath = parsed_args.design
    sel_regions_fpath = parsed_args.sel_regions
    
    keep_events_fpath = parsed_args.keep_events
    sample_size = parsed_args.event_number
    seed = parsed_args.seed
    
    inclusion_bias = parsed_args.inclusion_bias
    lengths_fpath = parsed_args.lengths

    min_counts = parsed_args.min_counts
    min_samples = parsed_args.min_samples
    min_inc_counts = parsed_args.min_inc_counts
    min_skp_counts = parsed_args.min_skp_counts
    min_events = parsed_args.min_events
    model_label = parsed_args.model
    use_event_id = parsed_args.event_ids
    
    n_threads = parsed_args.nthreads
    n_chains = parsed_args.nchains
    n_samples = parsed_args.n_samples
#     gp_prior_a = parsed_args.gp_scale_a
#     gp_prior_b = parsed_args.gp_scale_b
    exp_prop_nonzero = parsed_args.exp_reg
    recompile = parsed_args.recompile
    
    save_all_params = parsed_args.all_params 
    output_prefix = '{}.{}'.format(parsed_args.output_prefix, model_label)
    log_fpath = parsed_args.log

    # Check arguments
    if model_label not in AVAILABLE_MODELS:
        raise ValueError('{} model is not available'.format(model_label))
    design = pd.read_csv(design_fpath, index_col=0).iloc[:, 0]
    
    # Init counts object
    data = dSregCounts()
    if log_fpath is None:
        log_fhand = None
    else:
        log_fhand = open(log_fpath, 'w') 
    data.init_log(log_fhand)

    # Load count data
    inclusion = pd.read_csv(inc_fpath, index_col=0).fillna(0).astype(int)
    total = pd.read_csv(total_fpath, index_col=0).fillna(0).astype(int)
    total.columns = inclusion.columns
    data.load_count_matrices(inclusion, total)
    
    if keep_events_fpath is not None:
        keep_events = set([line.strip() for line in open(keep_events_fpath)])
        data.keep_events(keep_events)
    
    # Filter events
    data.filter_counts(min_counts=min_counts, n_samples=min_samples)
    data.filter_counts(min_counts=min_skp_counts, n_samples=min_samples,
                       label='inclusion')
    data.filter_counts(min_counts=min_inc_counts, n_samples=min_samples,
                       label='skipping')
    if sample_size is not None:
        data.sample_events(sample_size, seed=seed)

    # Load and filter binding sites
    data.load_binding_sites(binding_sites_fpath, use_event_id=use_event_id)
    if sel_regions_fpath is not None:
        sel_regions = [line.strip() for line in open(sel_regions_fpath)]
        data.select_regions(sel_regions, remove=False)
    data.filter_binding_sites(min_events=min_events)
    
    # Store RBP names for later analysis
    rbps_fpath = '{}.rbp_names'.format(output_prefix)
    with open(rbps_fpath, 'w') as fhand:
        for rbp in data.regulators_names:
            fhand.write('{}\n'.format(rbp))
    data.log.write('{} selected RBPs written to {}'.format(data.n_binding_sites,
                                                           rbps_fpath))
    
    # Load mappability info if required
    if inclusion_bias:
        if lengths_fpath is not None:
            lengths = pd.read_csv(lengths_fpath, index_col=0)
            lengths = lengths.loc[data.event_ids, :]
            mappability = np.log(lengths['inc_len'] / lengths['skp_len'])
        else:
            mappability = np.full(data.n_events, np.log(2))
    else:
        mappability = None
        
    # Analysis
    data.log.write('Output prefix files: {}'.format(output_prefix))
    data.fit_dsreg(design, model_label, mappability=mappability,
                   n_iter=n_samples, n_chains=n_chains, n_jobs=n_threads,
                   exp_prop_nonzero=exp_prop_nonzero,
#                    gp_prior_a=gp_prior_a, gp_prior_b=gp_prior_b,
                   save_all_params=save_all_params,
                   recompile=recompile)
    data.write_regulators(output_prefix)
    data.write_output(output_prefix)
    data.write_summary(output_prefix)
    data.log.finish()


if __name__ == '__main__':
    main()
