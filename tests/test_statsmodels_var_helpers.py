import unittest
import numpy as np
import graphinference.statsmodels_var_helpers as var_helper
from statsmodels.tsa.api import VAR

class TestStatsModelVARHelpers(unittest.TestCase):
    
    def test_var_coeffs_and_pvals(self):
        # Make a deterministic sinusoidal time series     
        t = np.linspace(0, 1000, 10000)
        ts = np.vstack((np.sin(t), np.cos(t)))
        # Add noise
        ts = ts + 0.001 * np.random.randn(*ts.shape)

        # Fit VAR to sin and cos
        sincos_var2_fit = VAR(ts.T).fit(maxlags=2)
        # Simulate the model
        sim_data = sincos_var2_fit.simulate_var(steps=20_000)
        # Fit a new VAR to the simulation
        refit_to_sim_var = VAR(sim_data).fit(maxlags=2)
        
        # Check that the coefficients are the same
        orig_lag1_coefs = var_helper.coef_matrix(sincos_var2_fit)
        orig_lag2_coefs = var_helper.coef_matrix(sincos_var2_fit, timestep_lag=2)
        
        lag1_coefs, lag1_pvals = var_helper.coef_matrix(refit_to_sim_var, return_pvals=True)
        lag2_coefs, lag2_pvals = var_helper.coef_matrix(refit_to_sim_var, timestep_lag=2, return_pvals=True)

        # Check that all lag-1 p-values are low
        self.assertTrue(np.all(lag1_pvals < 0.05))
        self.assertTrue(np.all(lag2_pvals < 0.05))

        # Check that coefficients are roughly the same

        self.assertTrue(np.all(np.abs(orig_lag1_coefs - lag1_coefs) < .1))
        self.assertTrue(np.all(np.abs(orig_lag2_coefs - lag2_coefs) < .1))



if __name__ == '__main__':
    unittest.main()