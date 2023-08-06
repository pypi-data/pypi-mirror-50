#!/usr/bin/env python
import argparse

import pandas as pd
from dSreg.utils.plots import plot_dsreg_pw_results #, plot_dsreg_ts_results
from dSreg.utils.settings import (AVAILABLE_MODELS, DSREG_PW,
                                  #DSREG_TS, DSREG_SIGMOID
                                  )
# from dSreg.utils.utils import load_dsreg_ts_results, load_dsreg_sigmoid_results


def main():
    description = 'Plots posterior distributions from fitting dSreg models. '

    # Create arguments
    parser = argparse.ArgumentParser(description=description)
    input_group = parser.add_argument_group('Input')
    help_msg = 'CSV files with dSreg posterior distribution'
    input_group.add_argument('posterior', nargs=1, help=help_msg)
    input_group.add_argument('-r', '--rbp_names', required=True,
                             help='File containing regulators names')

    options_group = parser.add_argument_group('Options')
    options_group.add_argument('-n', '--top_n', default=5,
                               help='Plot top N regulators separately (5)')
    options_group.add_argument('-a', '--add_traces', default=False,
                               action='store_true',
                               help='Add MCMC traces for theta differences')

#     help_msg = 'Number of predicted dSreg-TS time points (100)'
#     options_group.add_argument('-t', '--n_time_points', default=100,
#                                help=help_msg)
#     options_group.add_argument('-et', '--end_time', default=10,
#                                help='Experiment end time (10)')

    model_group = parser.add_argument_group('Models options')
    help_msg = 'Model ({}). Available: {}'
    model_group.add_argument('-M', '--model', default=DSREG_PW,
                             help=help_msg.format(DSREG_PW, [DSREG_PW]))

    output_group = parser.add_argument_group('Output')
    output_group.add_argument('-o', '--output', required=True,
                              help='Output file name')

    # Parse arguments
    parsed_args = parser.parse_args()
    posterior_fpath = parsed_args.posterior[0]
    rbps_fpath = parsed_args.rbp_names
    plot_top_n = int(parsed_args.top_n)
    add_traces = parsed_args.add_traces
    model_label = parsed_args.model
#     n_time_points = int(parsed_args.n_time_points)
#     end_time = float(parsed_args.end_time)
    out_fpath = parsed_args.output

    # Check arguments
    rbps_names = [line.strip() for line in open(rbps_fpath)]

    if model_label == DSREG_PW:
        posterior = pd.read_csv(posterior_fpath, usecols=rbps_names)
        data = pd.melt(posterior)
        data['variable'] = data['variable'].astype(str)
        means = posterior.mean(0)
        plot_dsreg_pw_results(posterior, data, means, out_fpath,
                              plot_top_n=plot_top_n, add_traces=add_traces)
#     elif model_label == DSREG_TS:
#         max_diffs, theta = load_dsreg_ts_results(posterior_fpath,
#                                                  rbp_names=rbps_names,
#                                                  n_time_points=n_time_points)
#         plot_dsreg_ts_results(max_diffs, theta, rbps_names, out_fpath,
#                               add_traces=add_traces)
#     elif model_label == DSREG_SIGMOID:
#         max_diffs, theta = load_dsreg_sigmoid_results(posterior_fpath,
#                                                       rbps_names, end_time)
#         plot_dsreg_ts_results(max_diffs, theta, rbps_names, out_fpath,
#                               add_traces=add_traces)

    else:
        raise ValueError('Invalid model {}. Try {}'.format(model_label,
                                                           AVAILABLE_MODELS))


if __name__ == '__main__':
    main()
