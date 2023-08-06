data {
    int<lower=1> N; // number of events
    int<lower=1> K; // number of samples
    int<lower=1> W; // number of regulators
    
    row_vector[N] mappability;
    real rho_prior;
    
    vector <lower=0, upper=1> [K] design;
    
    matrix<lower=0, upper=1>[N, W] binding_sites;
    
    int <lower=0> inclusion[K, N]; 
    int <lower=0> total[K, N];
}

parameters {
    vector[N] alpha;
    
    vector[W] theta_raw;
    vector<lower=0>[W] tau;
    real <lower=0> rho;
    
    
    real <lower=0> sigma;
    matrix[K, N] X_raw;
    
    real <lower=0> beta_sigma;
    row_vector[N] beta_raw;
}

transformed parameters {
    matrix[K, N] X;
    vector[W] theta;
    row_vector[N] beta;
    
    theta = rho * theta_raw .* tau;
    beta = to_row_vector(binding_sites * theta) + beta_sigma * beta_raw;
    X = rep_matrix(alpha, K)' + design * beta + sigma * X_raw; 
}

model {
    alpha ~ normal(3, 3);
    
    theta_raw ~ normal(0, 1);
    tau ~ cauchy(0, 1);
    rho ~ cauchy(0, rho_prior);
    
    sigma ~ cauchy(0, 3);
    to_row_vector(X_raw) ~ normal(0, 1);
    
    beta_sigma ~ cauchy(0, 1);
    beta_raw ~ normal(0, 1);
    
    for (i in 1:K)
        inclusion[i] ~ binomial_logit(total[i], X[i] + mappability);
}
