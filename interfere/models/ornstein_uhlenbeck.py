from typing import Optional

import numpy as np

from .base import StochasticDifferentialEquation


class OrnsteinUhlenbeck(StochasticDifferentialEquation):

    def __init__(
        self,
        theta: Optional[np.ndarray] = None,
        mu: Optional[np.ndarray] = None,
        sigma: Optional[np.ndarray] = None
    ):
        """Initializes n-dimensional Ornstein Uhlenbeck process.

        dX = theta(mu - X)dt + sigma dW

        Args:
            theta (ndarray): A (n, n) matrix.
            mu (ndarray): A (n,) vector.
            sigma (ndarray): A (n,) vector.
        """
        # Input validation
        if any([
            mu.shape[0] != theta.shape[0],
            theta.shape[0] != theta.shape[1],
            theta.shape[0] != sigma.shape[0],
            sigma.shape[1] != mu.shape[0]
        ]):
            raise ValueError(
                "Parameters for Lotka Voltera must have matching dimensions. "
                "Argument shapes: "
                f"\n\ttheta.shape = {theta.shape}"
                f"\n\tmu.shape = {mu.shape}"
                f"\n\tsigma.shape = {sigma.shape}"
            )
        # Set dimension
        super().__init__(len(mu))
        # Assign class attributes
        self.theta = theta
        self.mu = mu
        self.sigma = sigma

    def drift(self, x: np.ndarray, t: float):
        return self.theta @ (self.mu - x)
    
    def noise(self, x: np.ndarray, t: float):
        return self.sigma