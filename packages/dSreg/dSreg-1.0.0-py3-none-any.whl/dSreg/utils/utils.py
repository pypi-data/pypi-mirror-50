#!/usr/bin/env python

from _pickle import dump, load
from os.path import join
import sys
from time import ctime
import time

import numpy as np
import pandas as pd


def logit(x):
    return(np.log(x / (1 - x)))


def invlogit(x):
    return(np.exp(x) / (1 + np.exp(x)))


def sigmoid(t, X0, deltaX, a, b):
    return(X0 + deltaX / (1 + np.exp(a + b * t)))


class LogTrack(object):
    '''Logger class'''
    def __init__(self, fhand=None):
        if fhand is None:
            fhand = sys.stderr
        self.fhand = fhand
        self.start_time = time.time()

    def init(self, dataset_dir, script_name):
        log_fpath = join(dataset_dir, '{}.log'.format(script_name))
        self.fhand = open(log_fpath, 'w')
        self.write('Start')

    def write(self, msg, add_time=True):
        if add_time:
            msg = '[ {} ] {}\n'.format(ctime(), msg)
        else:
            msg += '\n'
        self.fhand.write(msg)
        self.fhand.flush()

    def finish(self):
        t = time.time() - self.start_time
        msg = 'Finished succesfully. Total time elapsed: {:.2f}s'.format(t)
        self.write(msg)


def load_pickle(fpath):
    with open(fpath, 'rb') as fhand:
        data = load(fhand)
    return(data)


def write_pickle(data, fpath):
    with open(fpath, 'wb') as fhand:
        dump(data, fhand)
    return(data)


def classify_splicing_event(event_id, fmt='vast'):
    if fmt != 'vast':
        raise ValueError('Only vast format allowed so far')
    if 'EX' in event_id:
        return('Exon cassette')
    elif 'ALTD' in event_id:
        return('Alternative donor')
    elif 'ALTA' in event_id:
        return('Alternative acceptor')
    elif 'INT' in event_id:
        return('Intron retention')
    return(None)


def load_dsreg_ts_results(fpath, rbp_names, n_time_points=100):
    '''Processes results from fitting with dsreg-TS to return a matrix
       with posterior distribution of the differences between the points
       with min and maximal posterior mean activities'''

    # Load full posterior
    data = pd.read_csv(fpath, index_col=0)
    ts = np.arange(1, n_time_points + 1)

    stacked_thetas = []
    max_diffs = []

    for rbp in rbp_names:
        sel_cols = ['{}.{}'.format(rbp, t) for t in ts]
        theta = data[sel_cols]

        # Store maximal differences distributions
        means = theta.mean(axis=0)
        max_idx, min_idx = np.argmax(means), np.argmin(means)
        delta = pd.DataFrame({'delta': theta[max_idx] - theta[min_idx]})
        delta['rbp'] = rbp
        max_diffs.append(delta)

        # Decide whether to store distribution
        stacked_thetas.append(theta)

    stacked_thetas = np.stack(stacked_thetas, axis=2)
    max_diffs = pd.concat(max_diffs)
    return(max_diffs, stacked_thetas)


def load_dsreg_sigmoid_results(fpath, rbp_names, end_time, n_time_points=100):
    times = np.linspace(0, end_time, n_time_points)
    posterior = pd.read_csv(fpath, index_col=0)

    max_diffs = []
    stacked_thetas = []

    for i, rbp in enumerate(rbp_names):
        sigmoid_a = posterior['sigmoid_a.{}'.format(i + 1)]
        sigmoid_b = posterior['sigmoid_b.{}'.format(i + 1)]
        delta_theta = posterior['delta_theta.{}'.format(i + 1)]
        theta0 = posterior[rbp]

        # Store maximal differences distributions
        delta = pd.DataFrame({'delta': delta_theta})
        delta['rbp'] = rbp
        max_diffs.append(delta)

        # Decide whether to store distribution
        theta = np.array([sigmoid(times, X0=x0, deltaX=d, a=a, b=b)
                          for a, b, x0, d in zip(sigmoid_a, sigmoid_b,
                                                 theta0, delta_theta)])
        stacked_thetas.append(theta)

    stacked_thetas = np.stack(stacked_thetas, axis=2)
    max_diffs = pd.concat(max_diffs)
    return(max_diffs, stacked_thetas)
