from os.path import exists
import pandas as pd
import numpy as np
from dSreg.utils.utils import LogTrack


class EventsCounts(object):
    def __init__(self, prefix=None, samples_runs=None,
                 inclusion_suffix='inclusion', total_suffix='total',
                 skipping_suffix='skipping'):
        self.samples_runs = samples_runs
        self.prefix = prefix
        self.suffixes = {'inclusion': inclusion_suffix,
                         'skipping': skipping_suffix,
                         'total': total_suffix,
                         'events': 'events'}
        self.keep_rows = None
        self.log = None
        
    def init_log(self, fhand=None):
        self.log = LogTrack(fhand=fhand)
        self.log.write('Start data analysis...')

    @property
    def n_samples(self):
        return(self.counts['total'].shape[1])

    @property
    def samples(self):
        return(self.counts['total'].columns)

    @property
    def event_ids(self):
        return(self.counts['total'].index)

    @property
    def n_events(self):
        return(self.counts['total'].shape[0])

    def select_samples(self, sel_samples):
        for suffix in ['inclusion', 'total']:
            self.counts[suffix] = self.counts[suffix][sel_samples].fillna(0)

    def get_fpaths(self, prefix=None):

        fpaths = {}
        for label, suffix in self.suffixes.items():
            fpath = '{}.{}.csv'.format(prefix, suffix)
            if not exists(fpath):
                if label != 'events':
                    raise ValueError('{} file not found'.format(fpath))
                else:
                    continue
            fpaths[label] = fpath
        if not exists(fpaths['skipping']) and not exists(fpaths['total']):
            msg = 'Either skipping or total counts must be provided'
            raise ValueError(msg)
        return(fpaths)

    def load_counts(self, prefix=None):
        counts = {}
        fpaths = self.get_fpaths(prefix=prefix)
        for label, fpath in fpaths.items():
            df = pd.read_csv(fpath, index_col=0).fillna(0)
            if label != 'events' and self.samples_runs is not None:
                df = pd.DataFrame({sample: df[runs].sum(1)
                                   for sample, runs in self.samples_runs.items()})
            counts[label] = df

        if 'total' not in counts:
            counts['total'] = counts['inclusion'] + counts['total']
        if 'skipping' not in counts:
            counts['skipping'] = counts['total'] - counts['inclusion']
        if 'events' in counts:
            for suffix in ['inclusion', 'total']:
                counts['events'][suffix] = counts[suffix].mean(1)
        self.counts = counts
        self.keep_rows = np.full(self.n_events, False)
    
    def keep_events(self, event_ids):
        self.keep_rows = np.array([event_id in event_ids
                                   for event_id in self.event_ids])
        if self.log is not None:
            msg = 'Maintain always a set of {} events'
            self.log.write(msg.format(self.keep_rows.sum()))
    
    def _group_by_samples(self, df):
        if self.samples_runs is None:
            return(df)
        return(pd.DataFrame({sample: df[runs].sum(1)
                             for sample, runs in self.samples_runs.items()}))
    
    def load_count_matrices(self, inclusion, total):
        counts = {}
        counts['inclusion'] = self._group_by_samples(inclusion)
        counts['total'] = self._group_by_samples(total)
        counts['skipping'] = counts['total'] - counts['inclusion']
        if 'events' in counts:
            for suffix in ['inclusion', 'total']:
                counts['events'][suffix] = counts[suffix].mean(1)
        self.counts = counts
        self.keep_rows = np.full(self.n_events, False)
        
        if self.log is not None:
            msg = 'Loaded {} events wtih {} samples'
            self.log.write(msg.format(self.n_events, self.n_samples))

    def filter_rows(self, sel_rows):
        filtered = {}
        sel_rows = np.logical_or(self.keep_rows, sel_rows)
        for key, value in self.counts.items():
            filtered[key] = value.loc[sel_rows, :]
        self.keep_rows = self.keep_rows[sel_rows]
        self.counts = filtered
    
    def sample_events(self, sample_size, seed=None):
        random_size = int(sample_size - self.keep_rows.sum())
        sel_rows = self.keep_rows.copy()
        
        if random_size > 0:
            available_events = np.where(self.keep_rows == False)[0]
            if seed is not None:
                np.random.seed(int(seed))
            sel_events = np.random.choice(available_events, size=random_size,
                                          replace=False)
            sel_rows[sel_events] = True
            msg = 'Randomly sampled up to {} events'
        else:
            msg = 'Keep all {} events; sample size is smaller than kept events'

        self.filter_rows(sel_rows)
        
        if self.log is not None:
            msg = msg.format(self.n_events)
            self.log.write(msg)

    def filter_counts(self, min_counts, n_samples=1, label='total'):
        sel_rows = (self.counts[label] >= min_counts).sum(1) >= n_samples
        self.filter_rows(sel_rows)
        
        if self.log is not None:
            msg = 'Filtered {} events with at least '
            msg += '{} {} counts in at least {} samples'
            self.log.write(msg.format(self.n_events, label,
                                      min_counts, n_samples))

    def filter_event_type(self, event_type):
        sel_rows = self.counts['events']['type'] == event_type
        self.filter_rows(sel_rows)
