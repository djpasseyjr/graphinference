import numpy as np
import pysindy as ps

def sindy_perf_interv_extrapolate(
    X,
    t,
    intervention_idx,
    intervention_value,
    max_sim_val=1e6,
):
    """Predicts the effect of a perfect intervention on the observed system.
    """
    # Pass the intervention variable as a control signal
    u = X[:, intervention_idx]
    trainingX = np.delete(X, intervention_idx, axis=1)
    method = ps.SINDy()
    method.fit(trainingX, t=t, u=u)

    # Create a perfect intervention control signal
    sindy_interv = intervention_value * np.ones_like(u)

    # Initial condition (Remove control signal)
    x0 = np.delete(X[0, :], intervention_idx)

    # Sindy uses scipy.integrate.solve_ivp by default and solve_ivp
    # uses event functions with assigned attributes as callbacks.
    # The below code tells scipy to stop integrating when
    # too_big(t, y) == True.
    too_big = lambda t, y: np.all(np.abs(y) < max_sim_val)
    too_big.terminal = True

    # Simulate with intervention
    sindy_X_do = method.simulate(
        x0, t, u=sindy_interv, integrator_kws={"events": too_big})

    # Retrive number of successful steps
    n_steps = sindy_X_do.shape[0]
    # Reassemble the control and response signals into a single array
    sindy_all_sigs = np.insert(
        sindy_X_do, intervention_idx, sindy_interv[:n_steps], axis=1)
    
    return sindy_all_sigs