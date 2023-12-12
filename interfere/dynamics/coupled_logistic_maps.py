from typing import Optional, Callable

import numpy as np

from ..base import DynamicModel, DEFAULT_RANGE


class CoupledLogisticMaps(DynamicModel):

    def __init__(
        self,
        adjacency_matrix: np.array,
        logistic_param=3.72,
        eps=0.5
    ):
        """N-dimensional coupled logistic map.
        
        A coupled map lattice where coupling is determined by the passed
        adjacency matrix and the map applied is the logistic map.

        x[n+1]_i = (1 - eps) * f(x[n]_i) + (eps / degree(i)) sum_j Aij f(x[n]_j)

        where f(x) = logistic_param * x * (1 - x).

        Note: This is not a continuous time system.


        Args:
            adjacency_matrix (2D array): The adjacency matrix that defines the
                way the variables are coupled. The entry A[i, j] should contain
                the weight of the link from x_j to x_i.
            logistic_param (float): The logistic map weight parameter   
                r, where the map is f(x) = rx(1-x).
            eps (float): A parameter that controls the relative strenth of    
                coupling. High epsilon means greater connection to neighbors.
        """
        self.adjacency_matrix = adjacency_matrix
        self.logistic_param = logistic_param
        self.eps = eps
        super().__init__(self.adjacency_matrix.shape[0])
    
    def logistic_map(self, x):
        return self.logistic_param * x * (1 - x)
    
    def simulate(
        self,
        initial_condition: np.ndarray,
        time_points: np.ndarray,
        intervention: Optional[Callable[[np.ndarray, float], np.ndarray]]= None,
        measurement_noise_std: Optional[np.ndarray] = None,
        rng: np.random.mtrand.RandomState = DEFAULT_RANGE,
    ) -> np.ndarray:
        """Runs a simulation of the dynamic model.

        Args:
            initial_condition (ndarray): A (m,) array of the initial
                condition of the dynamic model.
            time_points (ndarray): A (n,) array of the time points where the   
                dynamic model will be simulated. Must be integers
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

            measurement_noise_std (ndarray): None, or a vector with shape (n,)
                where each entry corresponds to the standard deviation of the
                measurement noise for that particular dimension of the dynamic
                model. For example, if the dynamic model had two variables x1
                and x2 and `measurement_noise_std = [1, 10]`, then
                independent gaussian noise with standard deviation 1 and 10
                will be added to x1 and x2 respectively at each point in time.
            rng: A numpy random state for reproducibility. (Uses numpy's mtrand 
                random number generator by default.)

        Returns:
            X: An (n, m) array containing a realization of the trajectory of 
                the m dimensional system corresponding to the n times in 
                `time_points`. The first p rows contain the initial condition/
                history of the system and count towards n.
        """
        nsteps = len(time_points)

        # Make sure that the simulation is not passed continuous time values
        if np.any(np.round(time_points) != time_points):
            raise ValueError("CoupledLogisticMap requires integer time points")
        
        # Initialize array of realizations of the trajectory.
        X_do = np.zeros((nsteps, self.dim))
        X_do[0] = initial_condition
            
        # Precompute row sums of adjacency matrix
        row_sums = np.sum(self.adjacency_matrix, axis=1)

        for i in range(nsteps - 1):

            # Apply intervention
            if intervention is not None:
                X_do[i] = intervention(X_do[i], time_points[i])

            # Compute next state
            X_do[i+1] = (
                (1 - self.eps) * self.logistic_map(X_do[i]) + 
                self.eps * self.adjacency_matrix @ self.logistic_map(X_do[i]) / row_sums
            )

        # Apply interention
        if intervention is not None:
            X_do[nsteps - 1] = intervention(
                X_do[nsteps - 1], time_points[nsteps - 1])
        
        if measurement_noise_std is not None:
            X_do = self.add_measurement_noise(X_do, measurement_noise_std, rng)

        return X_do