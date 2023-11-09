from typing import Optional

import numpy as np

from .base import StochasticDifferentialEquation


class OrnsteinUhlenbeck(StochasticDifferentialEquation):

    def __init__(
        self,
        theta: Optional[np.ndarray] = None,
        mu: Optional[np.ndarray] = None,
        Sigma: Optional[np.ndarray] = None
    ):
        """Initializes n-dimensional Ornstein Uhlenbeck process.

        dX = theta(mu - X)dt + Sigma dW

        Args:
            theta (ndarray): A (n, n) matrix.
            mu (ndarray): A (n,) vector.
            Sigma (ndarray): A (n, n) matrix.
        """
        # Input validation
        if any([
            mu.shape[0] != theta.shape[0],
            theta.shape[0] != theta.shape[1],
            theta.shape[0] != Sigma.shape[0],
            Sigma.shape[1] != mu.shape[0]
        ]):
            raise ValueError(
                "Parameters for Lotka Voltera must have matching dimensions. "
                "Argument shapes: "
                f"\n\ttheta.shape = {theta.shape}"
                f"\n\tmu.shape = {mu.shape}"
                f"\n\tSigma.shape = {Sigma.shape}"
            )
        # Set dimension
        super().__init__(len(mu))
        # Assign class attributes
        self.theta = theta
        self.mu = mu
        self.Sigma = Sigma

    def drift(self, x: np.ndarray, t: float):
        return self.theta @ (self.mu - x)
    
    def noise(self, x: np.ndarray, t: float):
        return self.Sigma