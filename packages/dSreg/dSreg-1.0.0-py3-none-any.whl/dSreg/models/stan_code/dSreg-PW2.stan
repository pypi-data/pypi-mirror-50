data {
    int<lower=1> N; // number of events
    int<lower=1> K; // number of samples
    int<lower=1> W; // number of regulators
    
    row_vector[N] mappability;
    real rho_prior;
    
    vector <lower=0, upper=1> [K] design;
    
    matrix<lower=0>[N, W] binding_sites_distances;
    real <lower=0> max_distance;
    
    int <lower=0> inclusion[K, N]; 
    int <lower=0> total[K, N];
}

parameters {
    real alpha_mu;
    vector[N] alpha_raw;
    real<lower=0> alpha_sigma;
    
    vector[W] theta_raw;
    vector<lower=0>[W] tau;
    real <lower=0> rho;
    row_vector[W]<lower=0> opt_distance;
    real <lower=0> dist_scale;
    
    real <lower=0> sigma;
    matrix[K, N] X_raw;
    
    real <lower=0> beta_sigma;
    row_vector[N] beta_raw;
}

transformed parameters {
    matrix[K, N] X;
    vector[W] theta;
    row_vector[N] beta;
    vector[N] alpha;
    matrix[N, W] binding_sites_strength;

    theta = rho * theta_raw .* tau;
    
    // Adding dependence on the distance to an optimal position
    binding_sites_strength = exp(- (binding_sites_distance - rep_matrix(opt_distance, N)) ** 2 / dist_scale);
    
    // Hierarchical model for alpha
    alpha = alpha_mu + alpha_sigma * alpha_raw;
    
    beta = to_row_vector(binding_sites_strength * theta) + beta_sigma * beta_raw;
    X = rep_matrix(alpha, K)' + design * beta + sigma * X_raw; 
}

model {
    // Hierarchican model for alpha now
    alpha_mu ~ normal(3, 3);
    alpha_sigma ~ gamma(2, 1);
    alpha_raw ~ normal(0, 1);
    
    theta_raw ~ normal(0, 1);
    tau ~ cauchy(0, 1);
    rho ~ cauchy(0, rho_prior);
    
    // Revise priors for distance related and potential identifibility issues
    // when theta is 0 as the opt_distance will not matter
    // Options:
    //     hierarchical model for opt_distances. Based on distance required for a regulator to modify splicing activity
    //                 makes sense if what matters is mostly 1D instead of 3D distance
    //     Force dependency of opt_distance on theta somehow: variance? mean?
    // There is not much information in either case to estimate from the data
    opt_distance ~ gamma(2, 1);
    scale_dist ~ gamma(2, 1);
    
    
    sigma ~ cauchy(0, 3);
    to_row_vector(X_raw) ~ normal(0, 1);

    // Long tail distribution for changes unexplained by the linear
    // combination of activities    
    beta_sigma ~ cauchy(0, 1);
    beta_raw ~ cauchy(0, 1);
    
    for (i in 1:K)
        inclusion[i] ~ binomial_logit(total[i], X[i] + mappability);
}
