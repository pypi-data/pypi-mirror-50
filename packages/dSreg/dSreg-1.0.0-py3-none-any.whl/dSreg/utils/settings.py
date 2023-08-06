from os.path import join, abspath, dirname
from pkg_resources import resource_filename

# Version
VERSION = '1.0.0'

# Directories
BASE_DIR = abspath(join(dirname(__file__), '..'))
MODELS_DIR = join(BASE_DIR, 'models')
COMPILED_DIR = join(MODELS_DIR, 'compiled')
COMPILED_DIR = resource_filename('dSreg', 'models/compiled')
STAN_CODE_DIR = join(MODELS_DIR, 'stan_code')
STAN_CODE_DIR = resource_filename('dSreg', 'models/stan_code')

# Model labels
DS_PW = 'dS-PW'
DSREG_PW = 'dSreg-PW'
DSREG_TS = 'dSreg-TS'
DSREG_SIGMOID = 'dsreg-Sigmoid'
# AVAILABLE_MODELS = [DS_PW, DSREG_PW, DSREG_TS, DSREG_SIGMOID]
AVAILABLE_MODELS = [DS_PW, DSREG_PW]

# Models parameters
MODELS_PARAMS = {(DSREG_PW, True): ['theta', 'sigma', 'alpha', 'beta'],
                 (DSREG_PW, False): ['theta', 'sigma'],
                 DS_PW: ['sigma', 'alpha', 'beta'],
                 DSREG_TS: ['theta_pred', 'X_sigma', 'rho', 'alpha',
                            'theta_sigma', 'X_alpha', 'X_rho',
                            'pi_mu', 'pi_sigma_raw'],
                 DSREG_SIGMOID: ['X_sigma', 'sigmoid_a', 'sigmoid_b',
                                 'theta_sigma', 'X_alpha', 'X_rho',
                                 'pi_mu', 'pi_sigma_raw',
                                 'delta_theta', 'delta_theta_mu',
                                 'delta_theta_sigma', 'theta0']}
