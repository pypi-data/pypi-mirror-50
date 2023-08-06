data {
    int<lower=1> N; // number of events
    int<lower=1> K; // number of samples
    
    int<lower=1> W; // number of regulators
    
    row_vector[N] mappability;
    matrix<lower=0, upper=1>[N, W] binding_sites;
    real times[K];
    
    real <lower=0> a;
    real <lower=0> b;
    
    int <lower=0> inclusion[K, N]; 
    int <lower=0> total[K, N];
}
transformed data{
    real sigmoid_a_mean;
    real sigmoid_a_sd;
    real time_interval;
    
    time_interval = max(times) - min(times); 
    sigmoid_a_mean = (max(times) + min(times))/2;
    sigmoid_a_sd = time_interval / 4;
}


parameters {
    // Sigmoid parameters for RBP activity
    vector [W] sigmoid_a;
    vector [W] sigmoid_b;
    vector [W] theta0;
        
    real delta_theta_mu;
    real <lower=0> delta_theta_sigma;
    vector [W] delta_theta_raw;
    
    real <lower=0> theta_sigma;
    matrix[W, K] theta_raw;
    
    // Splicing parameters
    vector[N] pi_raw;
    real pi_mu;
    real pi_sigma_raw;
    
    real <lower=0> X_rho;
    real <lower=0> X_sigma;
    real <lower=0> X_alpha;
    matrix [K, N] X_raw;
}

transformed parameters {
    vector [W] delta_theta;
    matrix [W, K] theta;
    matrix [K, K] L_sigma;
    matrix [K, N] X;
    vector[N] pi;
    
    // Sigmoidal RBP activity theta
    delta_theta = delta_theta_mu + delta_theta_sigma * delta_theta_raw;
    for(w in 1:W)
        theta[w] = to_row_vector(theta0[w] + rep_vector(delta_theta[w], K) ./ (1.0 + exp(sigmoid_a[w] + sigmoid_b[w] * to_vector(times)))) + theta_sigma * theta_raw[w];
    
    // baseline psi
    pi = pi_mu + exp(pi_sigma_raw) * pi_raw;
    
    // Splicing transformations
    L_sigma = cholesky_decompose(cov_exp_quad(times, X_alpha, X_rho) + 
                                 diag_matrix(rep_vector(square(X_sigma), K)));
    X = rep_matrix(pi, K)' + (binding_sites * theta)' +  L_sigma * X_raw; 
}

model {
    // Sigmoid parameters for RBP activity
    sigmoid_a ~ normal(0, 5);
    sigmoid_b ~ normal(0, 5);

    theta0 ~ normal(0, 1);
    delta_theta_mu ~ normal(0, 1);
    delta_theta_sigma ~ normal(0, 2);
    delta_theta_raw ~ normal(0, 1);
    
    theta_sigma  ~ cauchy(0, 5);
    to_row_vector(theta_raw) ~ normal(0, 1);
    
    // Splicing priors
    pi_mu ~ normal(0, 5);
    pi_sigma_raw ~ normal(log(3), 0.58);
    pi_raw ~ normal(0, 1);
    
    X_sigma  ~ cauchy(0, 5);
    to_row_vector(X_raw) ~ normal(0, 1);
    
    // GP priors
    X_rho ~ inv_gamma(a, b);
    X_alpha ~ gamma(0.5, 1);

    // Likelihood
    for(k in 1:K)
        inclusion[k] ~ binomial_logit(total[k], X[k] + mappability);
}
