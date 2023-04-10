"""Methods for determining a the network underlying a time series. 
"""

import numpy as np
import qspems
from idtxl.multivariate_te import MultivariateTE
from idtxl.data import Data
from statsmodels.tsa.api import VAR

from .statsmodels_var_helpers import coef_matrix


def lagged_correlation_corrected_for_reverse_causation(
    timeseries: np.ndarray,
    num_edges: int,
    max_lag: int = 1,
):
    """Infer a network with `num_eges` edges from time series data `timeseries`
    using lagged correlation with a correction for reverse causation.

    Args:
        timeseries: An (m x n) numpy array where m is the number of features and
            n is the number of observations.
        num_edges: The number of edges that this algorithm will predict.
        max_lag: The maximum number of timesteps prior to the current timestep
            that could potentially be correlated with the current timestep.

    Returns:
        An (m x m) adjacency matrix of zeros and ones that is the predicted
        network underlying the timeseries.
    """
    return qspems.inf_via_LCRC(timeseries, num_edges, max_lag=max_lag)

def multivariate_transfer_entropy(
    timeseries: np.ndarray,
    max_lag: int = 1,
    **kwargs
):
    """Predicts the computational network using multivariate transfer entropy.

    Args:
        timeseries: An (m x n) numpy array where m is the number of features and
            n is the number of observations.
        max_lag: The maximum number of timesteps prior to the current timestep
            that could potentially be correlated with the current timestep.
        kwargs: Settings for `idtxl.MultivariateTE.analyse_network`

    Returns:
        An (m x m) adjacency matrix of zeros and ones that is the predicted
        network underlying the timeseries.
    """
    reshaped_timeseries = np.reshape(timeseries, (*timeseries.shape, 1))
    data = Data(reshaped_timeseries)


    # Initialize multivariate transfer entropy
    network_analysis = MultivariateTE()
    settings = {
        'cmi_estimator': 'JidtGaussianCMI',
        'max_lag_sources': max_lag,
        'min_lag_sources': 1,
        'verbose': False,
        **kwargs
    }

    # Infer network
    results = network_analysis.analyse_network(settings=settings, data=data)
    mte_pred_adj = results.get_adjacency_matrix('binary').weight_matrix
    return mte_pred_adj

def vector_autoregression(
        timeseries: np.ndarray,
        max_lag=1,
        significance=0.05,
):
    """Predicts the computational network using vector autogregression.

    This technique models the adjacency matrix underlying the data as
    the significant entries in the lag one coefficient matrix.

    That is, if
        `y_k = mu + A_1 y_k-1 + A_2 y_k-2 + ... + A_n y_k-n`
    Then this model returns statistically significant entries in `A_1`

    Args:
        timeseries: An (m x n) numpy array where m is the number of features and
            n is the number of observations.
        max_lag: The maximum number of timesteps prior to the current timestep
            that could potentially be correlated with the current timestep.
        significance: the maximum allowable p-value for a correlation to be
            counted as significant.

    Returns:
        An (m x m) adjacency matrix of zeros and ones that is the predicted
        network underlying the timeseries.
    """
    var_model = VAR(timeseries.T)
    result = var_model.fit(maxlags=max_lag, verbose=False)
    _, pvals = coef_matrix(result, timestep_lag=1, return_pvals=True)
    return (pvals < significance).astype(float)
    

def var_union_matrix(timeseries, num_edges, max_lag, significance):

    """Unfinished and untested.
    """
    var_model = VAR(timeseries.T)
    result = var_model.fit(maxlags=max_lag, verbose=False)
    # Collect coefficients and p-values from the model
    lag_adjs_coef_and_pvals = [
        coef_matrix(result, timestep_lag=i, return_pvals=True) for i in range(max_lag)
    ]

    # Remove all coefficients that are not significant
    for coef, pvals in lag_adjs_coef_and_pvals:
        coef[pvals > significance] = 0.0
    lag_coefs = [c for c, p in lag_adjs_coef_and_pvals]
    stacked_coefs = np.stack(lag_coefs, axis=-1)

    # Find the largest correlation between time series across
    # all possible lags.
    max_coefs = np.max(np.abs(stacked_coefs), axis=2)
    # Only keep `num_edges` of the biggest correlations
    num_edges = int(num_edges)
    max_coefs[ max_coefs < np.sort(np.ravel(max_coefs))[-1*num_edges]] = 0.0
    # Turn matrix to a binary adj
    max_coefs[max_coefs != 0] = 1.0
    # 
    raise NotImplementedError()


