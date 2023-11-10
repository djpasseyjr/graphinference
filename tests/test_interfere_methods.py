import numpy as np
from statsmodels.tsa.vector_ar.util import varsim

from interfere.methods import simulate_perfect_intervention_var


def test_simulate_perfect_intervention_var():

    seed = 1
    rs = np.random.RandomState(seed)

    # Initialize a random VAR model
    A1 = rs.rand(3, 3) - 0.5
    A2 = rs.rand(3, 3) - 0.5
    coefs = np.stack([A1, A2])
    mu = rs.rand(3)
    Z = rs.rand(3, 3)
    Sigma = Z * Z.T
    steps = 101
    initial_vals = np.ones((2, 3))
    nsims = 10000

    # Simulate it
    true_var_sim = varsim(
        coefs,
        mu,
        Sigma,
        steps=steps,
        initial_values=initial_vals,
        seed=seed,
        nsimulations=nsims,
    )

    # Copy the VAR but add another dimension where the intervention will be
    # applied. 
    intervention_idx = 3
    intervention_value = 10
    intervention_coefs = 0.5 * np.stack([np.eye(4), np.eye(4)])
    intervention_coefs[:, :3, :3] = coefs
    intervention_mu = rs.rand(4)
    intervention_mu[:3] = mu
    intervention_sigma = np.eye(4)
    intervention_sigma[:3, :3] = Sigma
    intervention_initial_vals = np.ones((2, 4))


    perf_inter_sim = simulate_perfect_intervention_var(
        intervention_idx,
        intervention_value,
        intervention_coefs,
        intervention_mu,
        intervention_sigma,
        steps=steps,
        initial_values=intervention_initial_vals,
        seed=seed,
        nsimulations=nsims,
    )

    # Check that the shape is correct
    assert true_var_sim.shape == perf_inter_sim[:, :, :3].shape

    # Check that the intervention was applied correctly
    assert np.all(perf_inter_sim[:, :, intervention_idx] == intervention_value)

    # Average over the 10000 simulations to compute the expected trajectory.
    # Make sure it is equal for both models.
    assert np.all(
        np.mean(true_var_sim - perf_inter_sim[:, :, :3], axis=0) < 0.1
    )

    # Do a third simulation to  double check that the above average doesn't hold
    # in general
    A1 = rs.rand(3, 3) - 0.5
    A2 = rs.rand(3, 3) - 0.5
    coefs = np.stack([A1, A2])
    mu = rs.rand(3)
    Z = rs.rand(3, 3)
    Sigma = Z * Z.T
    steps = 101
    initial_vals = np.ones((2, 3))
    nsims = 10000

    true_var_sim2 = varsim(
        coefs,
        mu,
        Sigma,
        steps=steps,
        initial_values=initial_vals,
        seed=seed,
        nsimulations=nsims,
    )

    assert not np.all(
        np.mean(true_var_sim - true_var_sim2, axis=0) < 0.1
    )