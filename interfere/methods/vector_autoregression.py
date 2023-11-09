import numpy as np
from statsmodels.tools.validation import array_like, int_like


def simulate_perfect_intervention_var(
    intervention_idx: int,
    intervention_value: float,
    coefs: np.ndarray,
    intercept: np.ndarray,
    sig_u: np.ndarray,
    steps: int =100,
    initial_values=None,
    seed=None,
    nsimulations=None

):
    """Simulate a perfect intervention applied to a VAR model.

    Args:
        var_result: The return value of VAR().fit(lags)
        intervention_idx: The index of the variable where the intervention
            will be applied.
        intervention_value: The value that the variable at inter_idx will be
            pinned to.
        coefs : ndarray
            Coefficients for the VAR lags of endog.
        intercept : None or ndarray 1-D (neqs,) or (steps, neqs)
            This can be either the intercept for each equation or an offset.
            If None, then the VAR process has a zero intercept.
            If intercept is 1-D, then the same (endog specific) intercept is
            added to all observations. If intercept is 2-D, then it is treated
            as an offset and is added as an observation specific intercept that
            may include trend, seasonality, etc., to the autoregression. In
            this case, the intercept/offset should have same number of rows as
            steps, and the same number of columns as endogenous variables 
            (neqs).
        sig_u : ndarray
            Covariance matrix of the residuals or innovations.
            If sig_u is None, then an identity matrix is used.
        steps : {None, int}
            number of observations to simulate, this includes the initial
            observations to start the autoregressive process.
            If offset is not None, then exog of the model are used if they were
            provided in the model
        initial_values : array_like, optional
            Initial values for use in the simulation. Shape should be
            (nlags, neqs) or (neqs,). Values should be ordered from less to
            most recent. Note that this values will be returned by the
            simulation as the first values of `endog_simulated` and they
            will count for the total number of steps.
        seed : {None, int}
            If seed is not None, then it will be used with for the random
            variables generated by numpy.random.
        nsimulations : {None, int}
            Number of simulations to perform. If `nsimulations` is None it will
            perform one simulation and return value will have shape (steps, neqs).
    """
    p, k, k = coefs.shape
    # Validate nsimulations
    nsimulations= int_like(nsimulations, "nsimulations", optional=True)
    if isinstance(nsimulations, int) and nsimulations <= 0:
        raise ValueError("nsimulations must be a positive integer if provided")
    if nsimulations is None:
        result_shape = (steps, k)
        nsimulations = 1
    else:
        result_shape = (nsimulations, steps, k)

    # Default for covariance
    if sig_u is None:
        sig_u = np.eye(k)

    # Default values and validation for intercept
    if intercept is not None:
        # intercept can be 2-D like an offset variable
        if np.ndim(intercept) > 1:
            if not len(intercept) == ugen.shape[1]:
                raise ValueError('2-D intercept needs to have length `steps`')
    
    # Validate initial values
    initial_values = array_like(
        initial_values,
        "initial_values",
        optional=True,
        maxdim=2
    )
    if initial_values is not None:
        if not (initial_values.shape == (p, k) or initial_values.shape == (k,)):
            raise ValueError("initial_values should have shape (p, k) or (k,) where p is the number of lags and k is the number of equations.")
            
    # Initialize the random seed
    rs = np.random.RandomState(seed=seed)

    # Draw noise from multivariate normal (mean zero and cov = sig_u)
    rmvnorm = rs.multivariate_normal
    ugen = rmvnorm(np.zeros(len(sig_u)), sig_u, steps*nsimulations)
    ugen = ugen.reshape(nsimulations, steps, k)

    # Initialize empty result array
    result = np.zeros((nsimulations, steps, k))

    if intercept is not None:
        # add intercept/offset also to intial values. When initial_values
        # is none, this makes the initial value equal to the offset

        # When the 
        result += intercept

    # Prep result array by adding noise before calculating recurrence 
    result[:,p:] += ugen[:,p:]

    # Set beginning of results equal to initial values
    if initial_values is not None:
        result[:,:p] = initial_values

    # Apply the intervention to the initial values
    result[:, :p, intervention_idx] = intervention_value

    # add in AR terms
    for t in range(p, steps):
        ygen = result[:,t]
        for j in range(p):
            ygen += np.dot(coefs[j], result[:,t-j-1].T).T
            # Overwrite ygen with the intervention
            ygen[:, intervention_idx] = intervention_value

    return result.reshape(result_shape)
    
