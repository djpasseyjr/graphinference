from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Type

import numpy as np
from numpy.random import Generator
from sktime.forecasting.base import BaseForecaster

# Default range for random number generation.
DEFAULT_RANGE = generator = np.random.default_rng()


class DynamicModel(ABC):
    """Abstract base class for dynamic models.
    
    Any dynamic model that implements an appropriate `simulate` method
    can be used for dynamic counterfactual analysis. 
    """
    def __init__(
        self,
        dim: int, 
        measurement_noise_std: Optional[np.ndarray] = None,
    ):
        """Initializes a DynamicModel instance.

        Args:
            dim: The number of dimensions in the multivariate time series
                generated by the dynamic model.
            measurement_noise_std (ndarray): None, or a vector with shape (n,)
                where each entry corresponds to the standard deviation of the
                measurement noise for that particular dimension of the dynamic
                model. For example, if the dynamic model had two variables x1
                and x2 and `measurement_noise_std = [1, 10]`, then
                independent gaussian noise with standard deviation 1 and 10
                will be added to x1 and x2 respectively at each point in time.
        """
        self.dim = dim
        self.measurement_noise_std = measurement_noise_std

    @abstractmethod
    def simulate(
        self,
        initial_condition: np.ndarray,
        time_points: np.ndarray,
        intervention: Optional[Callable[[np.ndarray, float], np.ndarray]]= None,
        rng: np.random.mtrand.RandomState = DEFAULT_RANGE,
    ) -> np.ndarray:
        """Runs a simulation of the dynamic model.

        Args:
            initial_condition (ndarray): A (m,) or (p, m) array of the initial
                condition or the historical conditions of the dynamic model.
            time_points (ndarray): A (n,) array of the time points where the   
                dynamic model will be simulated.
            intervention (callable): A function that accepts (1) a vector of the
                current state of the dynamic model and (2) the current time. It should return a modified state. The function will be used in the
                following way: 
                    
                If the dynamic model without the intervention can be described 
                as
                    x(t+dt) = F(x(t))

                where dt is the timestep size, x(t) is the trajectory, and F is
                the function that uses the current state to compute the state at
                the next timestep. Then the intervention function will be used
                to simulate the system

                    z(t+dt) = F(g(z(t), t), t)
                    x_do(t) = g(z(t), t)

                where x_do is the trajectory of the intervened system and g is 
                the intervention function.
                TODO: Make notation inclusive of time delays.
            rng: A numpy random state for reproducibility. (Uses numpy's mtrand 
                random number generator by default.)

        Returns:
            X: An (n, m) array containing a realization of the trajectory of 
                the m dimensional system corresponding to the n times in 
                `time_points`. The first p rows contain the initial condition/
                history of the system and count towards n.
        """
        raise NotImplementedError
    
    def add_measurement_noise(
        self,
        X: np.ndarray,
        rng: np.random.mtrand.RandomState = DEFAULT_RANGE,
    ):
        """Adds independent gaussian noise to the array X.

        Only adds noise if self.measurement_noise_std is not None.

        Adds gaussian noise to each column. Equivalent to
            X[i, j] += normal() * stdevs[j]
        For all i and j.

        Args:
            X (ndarray): An (m, n) matrix that is interpreted to be a  
                realization of an n dimensional stochastic multivariate timeseries.
            measurement_noise_std (ndarray): An (n,) array that contains the
                standard deviations of the gaussian noise that will be added to
                each of the columns.
            rng: A numpy random state for reproducibility. (Uses numpy's mtrand 
                random number generator by default.)

        Returns:
            Xhat (ndarray): An (m, n) matrix that is equivalent to X + normally
                normally distributed noise.
        """
        if self.measurement_noise_std is None:
            return X
        
        return X + rng.standard_normal(X.shape) * self.measurement_noise_std


class Intervention(ABC):
    """Abstract intervention class"""
    
    @abstractmethod
    def __call__():
        raise NotImplementedError
    

def generate_counterfactual_dynamics(
    model_type: Optional[Type[DynamicModel]] = None,
    model_params: Optional[Dict[str, Any]] = None,
    intervention_type: Optional[
        Callable[[np.ndarray, float], np.ndarray]] = None,
    intervention_params: Optional[Dict[str, Any]] = None,
    initial_condition_iter: Optional[Iterable[np.ndarray]] = None,
    time_points_iter: Optional[Iterable[np.ndarray]] = None,
    rng: np.random.mtrand.RandomState = DEFAULT_RANGE,
):
    """Generates trajectories and corresponding counterfactual trajectories.

    Args:
        model (Type[DynamicModel]): The type of the dynamic model to simulate
            with and without interventions.
        model_params (Dict[str, Any]): The initialization parameters of the    
            dynamic model.
        intervention_type (Type[Intervention]): The type of the intervention to
            apply.
        intervention_params (Dict[str, Any]): The initialization parameters of
            the intervention.
        initial_condition_iter (Iterable[np.ndarray]): An iterable containing
            initial conditions that conform to the conditions on the 
            `initial_condition` argument in the
            `model(**model_parameters).simulate` function.
        time_points_iter (Iterable[np.ndarray]): An iterable containing arrays
            of time points that conform to the conditions on the `time_points` 
            argument in the `model(**model_parameters).simulate` function.
        rng: A numpy random state for reproducibility. (Uses numpy's mtrand 
            random number generator by default.)
            
    Returns:
        observations: An list of arrays where the ith array represents a
            realization of a trajectory of the dynamic model when the initial
            condition is initial_condition_iter[i]. The ith array has dimensions
            (n_i, m) where  `n_i = len(time_points_iter[i])` and m is the
            dimensionality of the system.
        counterfactuals: A list of arrays corresponding exactly to observations
            except that the supplied intervention was applied.    
    """
    model = model_type(**model_params)
    intervention = intervention_type(**intervention_params)
    observations = [
        model.simulate(
            initial_condition=ic,
            time_points=t,
            intervention=None,

            rng=rng,
        )
        for ic, t in zip(initial_condition_iter, time_points_iter)
    ]

    counterfactuals = [
        model.simulate(
            initial_condition=ic,
            time_points=t,
            intervention=intervention,
            rng=rng,
        )
        for ic, t in zip(initial_condition_iter, time_points_iter)
    ]
    return observations, counterfactuals


