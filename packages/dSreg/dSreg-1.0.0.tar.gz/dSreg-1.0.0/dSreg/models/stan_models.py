#!/usr/bin/env python
from itertools import groupby
from os.path import exists

import pystan

import numpy as np
import pandas as pd
from dSreg.utils.plots import plot_traces
from dSreg.utils.settings import COMPILED_DIR, STAN_CODE_DIR
from dSreg.utils.utils import write_pickle, load_pickle


def get_chunks(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def get_model(model_label, recompile=False):

    code_fpath = '{}/{}.stan'.format(STAN_CODE_DIR, model_label)
    compiled_fpath = '{}/{}.p'.format(COMPILED_DIR, model_label)

    if not exists(compiled_fpath) or recompile:
        # STAN model compilation
        model = pystan.StanModel(file=code_fpath)
        write_pickle(model, compiled_fpath)
    else:
        # Load stored model
        model = load_pickle(compiled_fpath)
    return(model)


def get_sampler_params(fit, n_iter, n_chains):
    dfs = []
    sampler_params = fit.get_sampler_params()
    for i in range(n_chains):
        df = pd.DataFrame({param: sample[int(n_iter / 2):]
                           for param, sample in sampler_params[i].items()})
        df['chain'] = i
        dfs.append(df)
    return(pd.concat(dfs, axis=0))


def get_traces_df(traces, params):
    traces_dict = {}
    for param in params:
        sample = traces[param]
        if len(sample.shape) == 2 and sample.shape[1] > 1:
            for i in range(sample.shape[1]):
                traces_dict['{}{}'.format(param, i + 1)] = sample[:, i]
        elif len(sample.shape) == 3:
            for i in range(sample.shape[1]):
                for j in range(sample.shape[2]):
                    value = sample[:, i, j]
                    traces_dict['{}{}{}'.format(param, i + 1, j + 1)] = value
        else:
            traces_dict[param] = sample
    return(pd.DataFrame(traces_dict))


def get_posterior_df(fit, params):
    traces = fit.extract()
    log_lik = traces.get('log_lik', None)
    traces = get_traces_df(fit, params)
    return(traces, log_lik)


def get_summary_df(fit):
    fit_summary = dict(fit.summary())
    df = pd.DataFrame(fit_summary['summary'],
                      index=fit_summary['summary_rownames'],
                      columns=fit_summary['summary_colnames'])
    return(df)


class BayesianModel(object):
    def init(self, model_label, prefix=None, n_chains=4, sim_label=None):
        self.model_label = model_label
        if sim_label is None:
            sim_label = model_label
        if prefix is None:
            prefix = model_label

        self.sim_label = sim_label
        self.model = None
        self.model_sim = None
        self.prefix = prefix
        self.n_chains = n_chains
        self.evaluation_results = {}

        self.sample_fpath = '{}.posterior'.format(prefix)
        self.summary_fpath = '{}.summary.csv'.format(prefix)
        self._summary = None
        self.summary_cols = ['2.5%', '50%', '97.5%', 'n_eff', 'Rhat']

    def recompile(self):
        self.model = get_model(self.model_label, recompile=True)

    def recompile_sim(self):
        self.model_sim = get_model('{}.sim'.format(self.sim_label),
                                   recompile=True)

    def _simulate(self, data, params, recompile=False, seed=None):
        model_label = '{}.sim'.format(self.sim_label)
        if self.model_sim is None:
            self.model_sim = get_model(model_label, recompile=recompile)
        fit = self.model_sim.sampling(data=data, chains=1, iter=1,
                                      n_jobs=1, pars=params, seed=seed)
        return(fit.extract())

    def load_posterior(self, pars, drop_warmup=False, n_warmups=1000):
        posterior = []
        for chain_id in range(self.n_chains):
            fpath = '{}_{}.csv'.format(self.sample_fpath, chain_id)
            if exists(fpath):
                chain_traces = pd.read_csv(fpath, usecols=pars,
                                           comment='#')
                chain_traces['chain_id'] = chain_id
                if drop_warmup:
                    chain_traces = chain_traces.iloc[n_warmups:, :]
                posterior.append(chain_traces)
        posterior = pd.concat(posterior, axis=0)
        self.posterior = posterior
        return(posterior)

    def traces_to_posterior(self, traces):
        data = {}
        for var_name, sample in traces.items():
            dim = sample.shape
            if len(dim) == 1:
                data[var_name] = sample
            elif len(dim) == 2:
                for i in range(sample.shape[1]):
                    data['{}.{}'.format(var_name, i + 1)] = sample[:, i]
            elif len(dim) == 3:
                for i in range(sample.shape[1]):
                    for j in range(sample.shape[2]):
                        xname = '{}.{}.{}'.format(var_name, i + 1, j + 1)
                        data[xname] = sample[:, i, j]
            else:
                msg = 'Transformation for more than 2D not implemented'
                raise ValueError(msg)
        return(pd.DataFrame(data))

    def posterior_to_traces(self, posterior):
        colnames = posterior.columns
        self.traces = {}
        for param, group in groupby(colnames, key=lambda x: x.split('.')[0]):
            group = list(group)
            size = len(group[0].split('.'))
            if size == 2:
                self.traces[param] = posterior[group]
            elif size == 3:
                zs = np.unique([int(x.split('.')[-1]) for x in group])
                ys = np.unique([int(x.split('.')[-2]) for x in group])
                xs = []
                for z in zs:
                    cols = ['{}.{}.{}'.format(param, y, z) for y in ys]
                    xs.append(posterior[cols])
                self.traces[param] = np.stack(xs, axis=2)
            elif size == 1:
                self.traces[param] = posterior[param]

    @property
    def summary(self):
        if self._summary is None:
            if exists(self.summary_fpath):
                self._summary = pd.read_csv(self.summary_fpath, index_col=0)
            else:
                msg = 'summary not available and not found in {}'
                raise ValueError(msg.format(self.summary_fpath))
        return(self._summary[self.summary_cols])

    def _get_sample_fpath(self, suffix=None):
        fpath = self.sample_fpath
        if suffix is not None:
            fpath = fpath + suffix
        return(fpath)

    def get_sampler_params(self, fit, n_iter, n_chains):
        dfs = []
        sampler_params = fit.get_sampler_params()
        for i in range(n_chains):
            df = pd.DataFrame({param: sample[int(n_iter / 2):]
                               for param, sample in sampler_params[i].items()})
            df['chain'] = i
            dfs.append(df)
        return(pd.concat(dfs, axis=0))

    def fit(self, data, pars, n_iter=2000, recompile=False, suffix=None,
            store_samples=False, n_chains=None, max_treedepth=12,
            n_jobs=None, adapt_delta=0.90, stepsize=None, integration_time=None,
            summarize=True, algorithm=None, traces_to_posterior=True,
            warmup=None):
        if n_jobs is None:
            n_jobs = n_chains
        if n_chains is None:
            n_chains = self.n_chains
        if self.model is None:
            self.model = get_model(self.model_label, recompile=recompile)
        sample_fpath = self._get_sample_fpath(suffix=suffix)
        if not store_samples:
            sample_fpath = None

        if algorithm is None:
            if stepsize is not None and integration_time is not None:
                algorithm = 'HMC'
                control = {'stepsize': stepsize, 'stepsize_jitter': 0.2,
                           'metric': 'diag_e', 'int_time': integration_time}
            else:
                algorithm = 'NUTS'
                control = {'adapt_delta': adapt_delta,
                           'max_treedepth': max_treedepth}
        else:
            control = {}

        fit = self.model.sampling(data=data, chains=n_chains, iter=n_iter,
                                  n_jobs=n_jobs, pars=pars,
                                  control=control, algorithm=algorithm,
                                  sample_file=sample_fpath, warmup=warmup)

        self.traces = fit.extract()
        self.sampler_params = self.get_sampler_params(fit, n_iter, n_chains)
        if summarize:
            summary = get_summary_df(fit)
#             summary.to_csv(self.summary_fpath)
            self._summary = summary[self.summary_cols]
        if traces_to_posterior:
            self.posterior = self.traces_to_posterior(self.traces)

        return(fit)

    def vb(self, data, pars, n_iter=2000, recompile=False):
        if self.model is None:
            self.model = get_model(self.model_label, recompile=recompile)
        self.fit = self.model.vb(data=data, pars=pars, output_samples=n_iter,
                                 algorithm='meanfield', adapt_iter=500,
                                 iter=20000)
        names = self.fit['sampler_param_names']
        sel_names = set(pars)
        sel_idx = dict((name, i) for i, name in enumerate(names)
                       if name.split('[')[0] in sel_names)
        self.traces = {name.replace('[', '.').replace(',', '.').replace(']', ''): np.array(self.fit['sampler_params'][i])
                       for name, i in sel_idx.items()}
        self.posterior = self.traces_to_posterior(self.traces)

        perc = {2.5: [], 50: [], 97.5: []}
        names = []
        for name, sample in self.traces.items():
            names.append(name)
            for p in perc:
                perc[p].append(np.percentile(sample, p))
        self.summary_cols = [2.5, 50, 97.5]
        self._summary = pd.DataFrame(perc, index=names)

    def tracesplot(self, fpath=None, sel_params=None, suffix=None,
                   split=False):
        if sel_params is None:
            sel_params = self.posterior.columns

        if fpath is None:
            fpath = '{}.tracesplot.png'.format(self._get_sample_fpath(suffix))
        if split:
            for colnames in get_chunks(sel_params, 5):
                fpath = '{}.{}.tracesplot.png'
                fpath = fpath.format(self._get_sample_fpath(suffix),
                                     colnames[0])
                plot_traces(self.posterior[colnames], colnames, fpath)
        else:
            plot_traces(self.posterior, sorted(sel_params), fpath)

    def write_fit(self, prefix, pickle=False):
        if pickle:
            fpath = '{}.p'.format(prefix)
            write_pickle(self.traces, fpath)
        else:
            fpath = '{}.csv'.format(prefix)
            self.posterior.to_csv(fpath)
        if hasattr(self, 'summary'):
            fpath = '{}.summary.csv'.format(prefix)
            self.summary.to_csv(fpath)
        if hasattr(self, 'sampler_params'):
            fpath = '{}.sampler_params.csv'.format(prefix)
            self.sampler_params.to_csv(fpath)
