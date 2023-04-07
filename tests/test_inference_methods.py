import unittest

import numpy as np
from graphinference import inference_methods as im
from graphinference.libs import qspems_sim_core

class TestInferenceMethods(unittest.TestCase):
    np.random.seed(110)
    adj = np.array([
        [0., 1., 0., 0., 1.],
        [1., 0., 1., 0., 0.],
        [0., 1., 0., 1., 1.],
        [0., 0., 1., 0., 0.],
        [1., 0., 1., 0., 0.],
    ])
    timeseries = qspems_sim_core.sim(adj, dt=1.0, sigma=0.01, T=2000)
    
    def test_lccrc(self):
        np.random.seed(11)
        pred_adj = im.lagged_correlation_corrected_for_reverse_causation(
            self.timeseries, np.sum(self.adj))
        np.testing.assert_array_equal(pred_adj, self.adj)
        self.assertTrue(np.all(pred_adj == self.adj))

    def test_mte(self):
        np.random.seed(111)
        pred_adj = im.multivariate_transfer_entropy(self.timeseries)
        np.testing.assert_array_equal(pred_adj, self.adj)
        self.assertTrue(np.all(pred_adj == self.adj))

    def test_var(self):
        np.random.seed(100)
        pred_adj = im.vector_autoregression(
            self.timeseries, np.sum(self.adj))
        np.testing.assert_array_equal(pred_adj, self.adj)
        self.assertTrue(np.all(pred_adj == self.adj))



if __name__ == '__main__':
    unittest.main()