functions {
  // Function for selecting prior parameters for lenght scale rho
  vector tail_delta(vector y, vector theta, real[] x_r, int[] x_i) {
    vector[2] deltas;
    deltas[1] = inv_gamma_cdf(theta[1], exp(y[1]), exp(y[2])) - 0.025;
    deltas[2] = 1 - inv_gamma_cdf(theta[2], exp(y[1]), exp(y[2])) - 0.025;
    return deltas;
  }
}

transformed data{
    // Data to create prior for length scale
    vector[2] y_guess = [log(10), log(20)]';        // starting guess at a,b
    vector[2] bounds = [2, 10]';                                // bounds for 95% prob
    vector[2] rho_hyperparams;
    real x_r[0];
    int x_i[0];

//     // Find max and minimal distance between time points
//     vector[K*K] delta_t;
//     for(k1 in 1:K){
//         for(k2 in 1:K){
//             delta_t[(k1 - 1) * K + k2] = fabs(times[k1] - times[k2]);
//         }
//     }
//     bounds[1] = min(delta_t);
//     bounds[2] = max(delta_t);

    // solve a, b of InvGamma such that 90% mass is between bounds[1] and bounds[2]
    // from https://betanalpha.github.io/assets/case_studies/gp_part3/part3.html
    rho_hyperparams = exp(algebra_solver(tail_delta, y_guess, bounds, x_r, x_i));
}


generated quantities {
    real a;
    real b;
    
    a = rho_hyperparams[1];
    b = rho_hyperparams[2];
}
