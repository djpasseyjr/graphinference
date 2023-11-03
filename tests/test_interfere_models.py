import interfere
import numpy as np
from scipy import integrate


def test_lotka_voltera():
    # Initialize interfere.LotkaVoltera model.
    n = 10
    r = np.random.rand(n)
    k = np.ones(n)
    A = np.random.rand(n, n) - 0.5

    interv_idx = n - 1
    interv_const = 1.0
    model = interfere.models.LotkaVoltera(r, k, A)

    # Make two kinds of interventions
    perf_interv = interfere.perfect_intervention(interv_idx, interv_const)
    sin_interv = interfere.signal_intervention(interv_idx, np.sin)

    # Create ground truth systems with the interventions built in
    def perf_int_true_deriv(x, t):
        x[interv_idx] = interv_const
        dx = r * x *( 1 - x / k + A @ (x / k))
        dx[interv_idx] = 0.0
        return dx

    def sin_int_true_deriv(x, t):
        x[interv_idx] = np.sin(t)
        dx = r * x *( 1 - x / k + A @ (x / k))
        dx[interv_idx] = np.cos(t)
        return dx

    # Set initial condition to match intervention
    x0 = np.random.rand(n)
    x0[interv_idx] = interv_const
    t = np.linspace(0, 2, 1000)

    # Test that for both interventions, the interfere API
    # correctly matches the ground truth system.
    true_perf_X = integrate.odeint(perf_int_true_deriv, x0, t)
    interfere_perf_X = model.simulate(x0, t, 1, perf_interv)
    assert np.allclose(true_perf_X, interfere_perf_X)

    x0[interv_idx] = np.sin(t[0])
    true_sin_X = integrate.odeint(sin_int_true_deriv, x0, t)
    interfere_sin_X = model.simulate(x0, t, 1, sin_interv)
    assert np.allclose(true_sin_X, interfere_sin_X)