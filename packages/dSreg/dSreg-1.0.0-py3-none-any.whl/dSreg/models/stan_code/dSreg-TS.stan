functions {
  // Function to interpolate GP outside of obsered values
  vector gp_pred_rng(real[] x2,
                     vector y1, real[] x1,
                     real alpha, real rho, real sigma, real delta) {
    int N1 = rows(y1);
    int N2 = size(x2);
    vector[N2] f2;
    {
      matrix[N1, N1] K =   cov_exp_quad(x1, alpha, rho)
                         + diag_matrix(rep_vector(square(sigma), N1));
      matrix[N1, N1] L_K = cholesky_decompose(K);

      vector[N1] L_K_div_y1 = mdivide_left_tri_low(L_K, y1);
      vector[N1] K_div_y1 = mdivide_right_tri_low(L_K_div_y1', L_K)';
      matrix[N1, N2] k_x1_x2 = cov_exp_quad(x1, x2, alpha, rho);
      vector[N2] f2_mu = (k_x1_x2' * K_div_y1);
      matrix[N1, N2] v_pred = mdivide_left_tri_low(L_K, k_x1_x2);
      matrix[N2, N2] cov_f2 =   cov_exp_quad(x2, alpha, rho) - v_pred' * v_pred
                              + diag_matrix(rep_vector(delta, N2));
      f2 = multi_normal_rng(f2_mu, cov_f2);
    }
    return f2;
  }
}

data {
    int<lower=1> N; // number of events
    int<lower=1> K; // number of samples
    
    int<lower=1> W; // number of regulators
    int<lower=1> Z; // number of tpred
    
    real <lower=0> a;
    real <lower=0> b;
    
    row_vector[N] mappability;
    matrix<lower=0, upper=1>[N, W] binding_sites;
    real times[K];
    real times_pred[Z];
    
    int <lower=0> inclusion[K, N]; 
    int <lower=0> total[K, N];
}


parameters {
    // GPs parameters for RBP activity
    vector <lower=0>[W] rho;
    vector <lower=0>[W] alpha;
    
    real <lower=0> theta_sigma;
    matrix[K, W] theta_raw;
    
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
    matrix [W, K] theta;
    matrix [K, K] L_theta;
    matrix [K, K] L_sigma;
    matrix [K, N] X;
    vector[N] pi;
    
    // baseline psi
    pi = pi_mu + exp(pi_sigma_raw) * pi_raw;
    
    // RBP activity theta
    for(w in 1:W){
        L_theta = cholesky_decompose(cov_exp_quad(times, alpha[w], rho[w]) + 
                                        diag_matrix(rep_vector(square(theta_sigma), K)));
        theta[w] = to_row_vector(L_theta * theta_raw[,w]);
    }
    
    // Splicing transformations
    L_sigma = cholesky_decompose(cov_exp_quad(times, X_alpha, X_rho) + 
                                 diag_matrix(rep_vector(square(X_sigma), K)));
    X = rep_matrix(pi, K)' + (binding_sites * theta)' +  L_sigma * X_raw; 
}

model {
    // GP priors
    rho ~ inv_gamma(a, b);
    alpha ~ gamma(0.5, 1);
    X_rho ~ inv_gamma(a, b);
    X_alpha ~ gamma(0.5, 1);
    theta_sigma  ~ cauchy(0, 5);
    to_row_vector(theta_raw) ~ normal(0, 1);
    
    // Splicing priors
    pi_mu ~ normal(0, 5);
    pi_sigma_raw ~ normal(log(3), 0.58);
    pi_raw ~ normal(0, 1);
    
    X_sigma  ~ cauchy(0, 5);
    to_row_vector(X_raw) ~ normal(0, 1);

    // Likelihood
    for(k in 1:K)
        inclusion[k] ~ binomial_logit(total[k], X[k] + mappability);
}

generated quantities {
    matrix[W, Z] theta_pred;
    
    for(w in 1:W)
        theta_pred[w] = to_row_vector(gp_pred_rng(times_pred, to_vector(theta[w]), times,
                                                  alpha[w], rho[w], theta_sigma, 1e-10));
}
