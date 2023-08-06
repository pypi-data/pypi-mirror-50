data {
    int<lower=1> N; // number of events
    int<lower=1> K; // number of samples
    
    row_vector[N] mappability;
    
    vector <lower=0, upper=1> [K] design;
    
    int <lower=0> inclusion[K, N]; 
    int <lower=0> total[K, N];
}
transformed data{
    vector[K] K_indentity;
    
    K_indentity = rep_vector(1, K); 
    
}

parameters {
    row_vector[N] alpha;
    
    real <lower=0> sigma;
    matrix[K, N] X_raw;
    
    real beta_mean;
    real <lower=0> beta_sigma;
    row_vector[N] beta_raw;
}

transformed parameters {
    matrix[K, N] X;
    row_vector[N] beta;
    
    beta = beta_mean + beta_sigma * beta_raw;
    X = K_indentity * alpha + design * beta + sigma * X_raw; 
}

model {
    alpha ~ normal(3, 3);
    
    sigma ~ cauchy(0, 3);
    to_row_vector(X_raw) ~ normal(0, 1);
    
    beta_mean ~ normal(0, 1);
    beta_sigma ~ cauchy(0, 1);
    beta_raw ~ normal(0, 1);
    
    for (i in 1:K)
        inclusion[i] ~ binomial_logit(total[i], X[i] + mappability);
}
