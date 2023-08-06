import numpy as np
import pandas as pd
from dSreg.utils.settings import (AVAILABLE_MODELS, DSREG_PW, DSREG_TS, DS_PW,
                                  MODELS_PARAMS, DSREG_SIGMOID)
from dSreg.utils.utils import invlogit
from dSreg.utils.event_counts import EventsCounts
from dSreg.models.stan_models import BayesianModel


class dSregCounts(EventsCounts):
    @property
    def n_binding_sites(self):
        if hasattr(self, 'binding_sites'):
            return(self.binding_sites.shape[1])
        else:
            return(0)

    @property
    def regulators_names(self):
        if not hasattr(self, '_regulators_names'):
            self._regulators_names = self.binding_sites.columns
        return(self._regulators_names)

    def load_binding_sites(self, fpath, use_event_id=True):
        if use_event_id:
            binding_sites = pd.read_csv(fpath).set_index('event_id')
        else:
            binding_sites = pd.read_csv(fpath, index_col=0)

        binding_sites = binding_sites.loc[self.counts['total'].index, :]
        binding_sites = (binding_sites > 0).astype(int)
        self.binding_sites = binding_sites
        if self.log is not None:
            msg = 'Loaded binding sites for {} RBPs'
            self.log.write(msg.format(self.n_binding_sites))

    def filter_binding_sites(self, min_events=5):
        sel_cols = self.binding_sites.sum(0) >= min_events
        self.binding_sites = self.binding_sites.loc[:, sel_cols]
        if self.log is not None:
            msg = 'Filtered {} RBPs >= {} events'
            self.log.write(msg.format(self.n_binding_sites, min_events))

    def select_regions(self, regions, remove=False):
        sel_cols = [x for x in self.binding_sites.columns
                    if x.split('.', 1)[-1] in regions != remove]
        self.binding_sites = self.binding_sites.loc[:, sel_cols]
        if self.log is not None:
            self.log.write('Filtered {} RBPs'.format(self.n_binding_sites))

    def get_stan_data(self, design, n_ts_pred=100, mappability=0,
                      hs_prior=1, gp_prior_a=6.4, gp_prior_b=24.4):

        data = {'inclusion': self.counts['inclusion'].transpose().astype(int),
                'total': self.counts['total'].transpose().astype(int)}
        data['binding_sites'] = self.binding_sites
        data['W'] = self.n_binding_sites
        data['K'] = self.n_samples
        data['N'] = self.n_events
        
        if mappability is None:
            mappability = np.full(self.n_events, 0)
        data['mappability'] = mappability

        # Model specific data
        if self.model_label in [DSREG_PW, DS_PW]:
            data['design'] = design
            data['rho_prior'] = hs_prior
        elif self.model_label in [DSREG_TS, DSREG_SIGMOID]:
            data['times'] = design
            data['a'] = gp_prior_a
            data['b'] = gp_prior_b
            if self.model_label == DSREG_TS:
                data['times_pred'] = np.linspace(design.min(), design.max(),
                                                 n_ts_pred)
                data['Z'] = n_ts_pred

        else:
            msg = '{} model not allowed. Try {}'.format(self.model_label, 
                                                        AVAILABLE_MODELS)
            raise ValueError(msg)
        return(data)

    def fit_dsreg(self, design, model_label, params=None, n_ts_pred=100,
                  mappability=None, n_iter=2000, n_chains=4,
                  exp_prop_nonzero=None, gp_prior_a=6.4, gp_prior_b=24.4,
                  n_jobs=None, save_all_params=False, recompile=False):
        self.model_label = model_label
        if params is None:
            params = MODELS_PARAMS.get((self.model_label, save_all_params),
                                       MODELS_PARAMS.get(self.model_label, None))

        # Assume variance in betas (sigma) is around 1
        # hs_prior = p / (1 - p) * sigma / sqrt(n_exons)
        if exp_prop_nonzero is None:
            hs_prior = 1
        else:
            exp_prop_nonzero = float(exp_prop_nonzero)
            hs_prior = exp_prop_nonzero / (1 - exp_prop_nonzero)
            hs_prior = hs_prior * 1 / np.sqrt(self.n_events)
        X = self.get_stan_data(design, n_ts_pred, mappability,
                               hs_prior=hs_prior,
                               gp_prior_a=gp_prior_a, gp_prior_b=gp_prior_b)
        
        if self.log is not None:
            msg = 'Fitting {} model with {} exons, {} samples and {} RBPs'
            self.log.write(msg.format(self.model_label, self.n_events,
                                      self.n_samples, self.n_binding_sites))
        
        # Init and fit model through MCMC
        self.model = BayesianModel()
        self.model.init(model_label=model_label)
        if recompile:
            self.model.recompile()
        self.model.fit(X, pars=params, n_iter=n_iter, n_chains=n_chains,
                       n_jobs=n_jobs)
        self.update_labels()
    
    def get_events_summary(self):
        # TODO: Create a separate class for results to allow independent 
        # work from the counts class
        if self.model_label not in [DS_PW, DSREG_PW]:
            summ = None
            msg = 'Event summary not implemented for this model {}'
            self.log.write(msg.format(self.model_label))
        elif 'alpha' in self.model.traces and 'beta' in self.model.traces:
            alpha = self.model.traces['alpha']
            beta = self.model.traces['beta']
            
            psi1 = invlogit(alpha)
            psi2 = invlogit(alpha + beta)
            dpsi = psi2 - psi1
            p = np.max([(dpsi > 0.05).mean(0),
                        (dpsi < -0.05).mean(0)], axis=0)
            
            summ = pd.DataFrame({'E[PSI_1]': psi1.mean(0),
                                 'E[PSI_2]': psi2.mean(0),
                                 'E[dPSI]': dpsi.mean(0),
                                 'dPSI_p2.5': np.percentile(dpsi, 2.5, axis=0),
                                 'dPSI_p97.5': np.percentile(dpsi, 97.5, axis=0),
                                 'P(|dPSI|>0.05)': p},
                                 index=self.event_ids)
            summ.sort_values('E[dPSI]', ascending=False, inplace=True)
        else: 
            summ = None
        return(summ)
    
    def get_regulators_summary(self):
        if self.model_label != DSREG_PW:
            if self.log is not None:
                msg = 'Warning: Regulators not available for this model {}'
                self.log.write(msg)
            return(None)
        
        theta = self.model.traces['theta']
        p = np.max([(theta > 0.).mean(0),
                    (theta < -0.).mean(0)], axis=0)
        summ = pd.DataFrame({'E[dTheta]': theta.mean(0),
                             'dTheta_p2.5': np.percentile(theta, 2.5, axis=0),
                             'dTheta_p97.5': np.percentile(theta, 97.5, axis=0),
                             'P(|dTheta|>0)': p},
                             index=self.regulators_names) 
        summ.sort_values('E[dTheta]', ascending=False, inplace=True)
        return(summ)
    
    @property
    def events_summary(self):
        if not hasattr(self, '_events_summary'):
            self._events_summary = self.get_events_summary()
        return(self._events_summary)
    
    @property
    def regulators_summary(self):
        if not hasattr(self, '_regulators_summary'):
            self._regulators_summary = self.get_regulators_summary()
        return(self._regulators_summary)

    def update_regulator_label(self, label, prefix='theta', suffix=''):
        # TODO: Prepare better output for sigmoid
        if label.startswith('theta') and '.' in label:
            label = label.rstrip(']').replace('[', '.').replace(',', '.')
            items = label.split('.')
            idx = int(items[1]) - 1
            return('.'.join([self.regulators_names[idx]] + items[2:]))
        else:
            return(label)

    def update_labels(self):
        self.model.posterior.columns = [self.update_regulator_label(x)
                                        for x in self.model.posterior.columns]
        self.model._summary.index = [self.update_regulator_label(x)
                                     for x in self.model._summary.index]

    def write_regulators(self, prefix):
        with open('{}.binding_sites.csv'.format(prefix), 'w') as fhand:
            for regulator in self.regulators_names:
                fhand.write('{}\n'.format(regulator))

    def write_output(self, prefix):
        self.model.write_fit(prefix)
    
    def write_summary(self, prefix):
        if self.events_summary is not None:
            fpath = '{}.events.csv'.format(prefix)
            self.events_summary.to_csv(fpath)
        if self.regulators_summary is not None:
            fpath = '{}.regulators.csv'.format(prefix)
            self.regulators_summary.to_csv(fpath)
