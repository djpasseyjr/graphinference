from abc import ABC, abstractmethod
from typing import Any, Dict,  Iterable, Optional, Type

import numpy as np
from scipy import integrate

class Intervention(ABC):
    """Abstract base class for interventions."""

    @abstractmethod
    def __call__(self, x: np.ndarray, t: float) -> np.ndarray:
        """Compute the state of the system after the intervention is applied.

        Args:
            x: The current state of the system.
            t: The current time.

        Returns:
            x_do: The state of the system at time t when the intervention is 
                applied.
        """
        raise NotImplementedError

class SingleVariableIntervention(Intervention):
    """Class for describing an intervention that only affects one variable.
    
    Important: The intervention variable must not use it's pre-intervention
        value to compute the post intervention value.

        e.g. if `intervention_vairable_idx = 0`, then 
            intervention(x) = x[0] * 2
        is NOT permitted but
            intervention(x) = x[1] * 2
        is fine.
    """

    def __init__(self, intervention_vairable_idx: int):
        """
        Args:
            intervention_vairable_idx (int): An index denoting which variable 
                will be overwritten by the intervention.
        """
        self.intervention_vairable_idx = intervention_vairable_idx


class DynamicModel(ABC):
    """Abstract base class for dynamic models.
    
    Any dynamic model that implements an appropriate `simulate` method
    can be used for dynamic counterfactual analysis. 
    """
    def __init__(self, dim: int):
        """

        Args:
            dim: The number of dimensions in the multivariate time series
                generated by the dynamic model.
        """
        self.dim = dim

    @abstractmethod
    def simulate(
        self,
        initial_condition: np.ndarray,
        time_points: np.ndarray,
        seed: int,
        intervention: Optional[Intervention] = None
    ) -> np.ndarray:
        """Runs a simulation of the dynamic model.

        Args:
            initial_condition: A (m,) or (p, m) array of the initial condition
                or the historical conditions of the dynamic model.
            time_points: A (n,) array of the time points where the dynamic 
            model will be simulated.
            seed: A seed for reproducibility.
            intervention: A function that accepts (1) a vector of the
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

        Returns:
            X: An (n, m) array containing a realization of the trajectory of 
                the m dimensional system corresponding to the n times in 
                `time_points`. The first p rows contain the initial condition/
                history of the system and count towards n.
        """
        raise NotImplementedError


class OrdinaryDifferentialEquation(DynamicModel):

    def simulate(
        self,
        initial_condition: np.ndarray,
        time_points: np.ndarray,
        seed: int,
        intervention: Optional[SingleVariableIntervention] = None
    ) -> np.ndarray:
        """
        Runs a simulation of the differential equaltion model.

        Args:
            initial_condition: A (m,) array of the initial condition
                or the historical conditions of the dynamic model.
            time_points: A (n,) array of the time points where the dynamic 
            model will be simulated.
            seed: A seed for reproducibility.
            intervention: A function that accepts (1) a vector of the
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

        Returns:
            X: An (n, m) array containing a realization of the trajectory of 
                the m dimensional system corresponding to the n times in 
                `time_points`. The first p rows contain the initial condition/
                history of the system and count towards n.
        """
        if intervention is None:
            return integrate.odeint(self.dXdt, initial_condition, time_points)
        
        # Define the derivative of the intervened system
        intervention_dXdt = lambda x, t: self.dXdt(intervention(x, t), t)

        # Integrate
        X = integrate.odeint(intervention_dXdt, initial_condition, time_points)

        # Appy the intervention to the states produced by the integrator.
        X_do = np.vstack([intervention(x, t) for x, t in zip(X, time_points)])
        return X_do

    @abstractmethod
    def dXdt(self, x: np.ndarray, t: float):
        """Produces the derivative of the system at the supplied state and time.

        Use __init__() to set the parameters of the ODE. 
        
        Args:
            x (ndarray): The current state of the system.
            t (float): The current time.

        Returns:
            The derivative of the system at x and t with respect to time.
        """
        raise NotImplementedError
    

    
def generate_counterfactual_dynamics(
    model_type: Optional[Type[DynamicModel]] = None,
    model_params: Optional[Dict[str, Any]] = None,
    intervention_type: Optional[Type[Intervention]] = None,
    intervention_params: Optional[Dict[str, Any]] = None,
    initial_condition_iter: Optional[Iterable[np.ndarray]] = None,
    time_points_iter: Optional[Iterable[np.ndarray]] = None,
    seed_iter: Optional[Iterable[int]] = None,
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
            argument in the
            `model(**model_parameters).simulate` function.
        seed_iter (Iterable[int]): An iterable containing seeds for reproducible
            random number generation. Each item in the iterable must
            conform to the conditions on the `seed` argument in the
            `model(**model_parameters).simulate` function.
            
    Returns:
        observations: An list of arrays where the ith array represents a
            realization of a trajectory of the dynamic model when the initial
            condition is initial_condition_iter[i] and the seed is seed_iter[i].
            The ith array has dimensions (n_i, m) where 
            `n_i = len(time_points_iter[i])` and m is the dimensionality of the 
            system.
        counterfactuals: A list of arrays corresponding exactly to observations
            except that the supplied intervention was applied.    
    """
    model = model_type(**model_params)
    intervention = intervention_type(**intervention_params)
    observations = [
        model.simulate(
            initial_condition=ic,
            time_points=t,
            seed=s,
            intervention_function=None
        )
        for ic, t, s in zip(
            initial_condition_iter, time_points_iter, seed_iter)
    ]

    counterfactuals = [
        model.simulate(
            initial_condition=ic,
            time_points=t,
            seed=s,
            intervention=intervention
        )
        for ic, t, s in zip(
            initial_condition_iter, time_points_iter, seed_iter)
    ]
    return observations, counterfactuals