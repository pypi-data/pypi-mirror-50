#!/usr/bin/env python
from dSreg.models.stan_models import BayesianModel
from dSreg.utils.settings import AVAILABLE_MODELS
from dSreg.utils.utils import LogTrack


def main():
    log = LogTrack()
    log.write('Compiling dSreg models...')
    for model_label in AVAILABLE_MODELS:
        log.write('\tCompile {}'.format(model_label))
        model = BayesianModel()
        model.init(model_label=model_label)
        model.recompile()
    log.finish()


if __name__ == '__main__':
    main()
