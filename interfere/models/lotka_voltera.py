from typing import Optional

from .base import OrdinaryDifferentialEquation

import numpy as np

class LotkaVoltera(OrdinaryDifferentialEquation):
    """Class for simulating Lotka Voltera dynamics.

    Can be simulated using the parent class `simulate` method.
    """

    def __init__(self, growth_rates: np.ndarray, capacities: np.ndarray,
                 interaction_mat: np.ndarray):
        """Initializes class for simulating Lotka Voltera dynamics.

        Args:
            growth_rates (ndarray): A length n vector of growth rates.
            capacities (ndarray): A length n vector of carrying capacities.
            interaction_mat: A weighted (n, n) matrix of interspecies interactions.
        """
        # Input validation
        if any([
            growth_rates.shape != capacities.shape,
            interaction_mat.shape[0] != interaction_mat.shape[1],
            interaction_mat.shape[1] != capacities.shape[0],
        ]):
            raise ValueError("Parameters for Lotka Voltera must have the same "
                             "dimensions. Argument shapes: "
                             f"\n\tgrowth_rates.shape = {growth_rates.shape}"
                             f"\n\tcapacities.shape = {capacities.shape}"
                             f"\n\tinteraction_mat.shape = {interaction_mat.shape}"
                            )
        
        # Assign parameters.
        self.growth_rates = growth_rates
        self.capacities = capacities
        self.interaction_mat = interaction_mat
        # Set dimension of the system.
        super().__init__(len(growth_rates))

    def dXdt(self, x: np.ndarray, t: Optional[float] = None):
        """Coputes derivative of a generalized Lotka Voltera model.

        dx_i/dt = r_i * x_i * (1 - x_i / k_i +  [A x]_i / k_i)

        Args:
            x (ndarray): The current state of the system.
            t (float): The current time. Optional because the system is 
                autonomous.

        Returns:
            The derivative of the system at x and t with respect to time.
        """
        return self.growth_rates * x * (
            1 - x / self.capacities + self.interaction_mat @ (
                x / self.capacities
            )
        )