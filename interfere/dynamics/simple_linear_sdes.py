import numpy as np

from .base import StochasticDifferentialEquation


# A Real matrix with all imaginary eigenvalues.
MATRIX_ALL_IMAG_EIGS = np.array([
    [ 0.54748989, -3.28156307,  1.5146247 , -1.29057552],
    [ 1.17925623,  0.19553371, -0.39465974, -1.60525885],
    [ 0.14984667,  1.40491579, -0.4096218 , -3.29551032],
    [ 0.50900001, -0.24048083,  1.16530899, -0.3334018 ]
])


class LinearSDE(StochasticDifferentialEquation):

    def __init__(self, A: np.ndarray, sigma: np.ndarray):
        """Initializes stochastic differential equation with the following form:

            dX = A X dt + sigma dW

        Args:
            A (ndarray): (n, n) matrix.
            sigma (ndarray): (n, n) matrix. Used to rescale the independent
                Weiner increments.
        """

        # Input vaidation
        if any((
            A.shape[0] != A.shape[1],
            A.shape[0] != sigma.shape[0],
            sigma.shape[0] != sigma.shape[1]
        )):
            raise ValueError("Parameters for LinearSDE must have matching dimensions. "
                "Argument shapes: "
                f"\n\tA.shape = {A.shape}"
                f"\n\tsigma.shape = {sigma.shape}"
            )
        dim = A.shape[0]
        super().__init__(dim)
        self.A = A
        self.sigma = sigma

    def drift(self, x, t):
        return self.A @ x
    
    def noise(self, x, t):
        return self.sigma


class DampedOscillator(StochasticDifferentialEquation):

    def __init__(self, m: float, c: float, k: float, sigma: float):
        """Initializes a stochastic damped linear oscilator.

        The deterministic dynamics can be described by the second order
        equation: 

           m x'' + c x' + k x = 0

        Letting y = x' transforms the system to a first order
        system. Adding brownian noise produces:

            dx = y dt + sigma dW1 

            dy = - (k/m x + c/m y) dt + sigma dW2

        See http://hyperphysics.phy-astr.gsu.edu/hbase/oscda.html
        for more details.

        Args:
            m (float): The mass. Must be positive.
            c (float): The damping coefficient. Must be positive.
            k (float): The spring constant. Must be positive.
            sigma (float): The noise coefficient.
        """
        # Validate input
        if any((
            m < 0,
            c < 0,
            k < 0,
            sigma < 0
        )):
            raise ValueError("Damped oscilator parameters must be positive.")
        
        dims = 2
        super().__init__(dims)
        self.m = m
        self.c = c
        self.k = k
        self.sigma = sigma

        self.A = np.array([
            [0.0, 1.0],
            [- k / m, - c / m]
        ])
        self.Sigma = sigma * np.eye(dims)

    def drift(self, x, t):
        return self.A @ x
    
    def noise(self, x, t):
        return self.Sigma
    

def DegenerateRoot2DLinearSDE(sigma: float = 0.0):
    """Initializes a linear SDE with pure imaginary eigenvalues.

    The system has the form:

        dX = AX dt + sigma dW

    Where dW is a 2D vector of independent brownian increments and

    A = [[0 -4]
         [1  0]].

    See Perko, Differential equations and dynamical systems. pg. 24 
    https://www-users.cse.umn.edu/~scheel/teaching/8501-fall18/perko.pdf
    for more details.


    Args:
        sigma (float): controls the magnitude of the system noise.        
    """
    Sigma = sigma * np.eye(2)
    A = np.array([
        [0, -4],
        [1, 0]
    ])
    return LinearSDE(A, Sigma)


def DegenerateRoot4DLinearSDE(sigma: float = 0.0):
    """Initializes a linear SDE with pure imaginary eigenvalues.

    The system has the form:

        dX = AX dt + Sigma dW

    Where dW is a 2D vector of independent brownian increments and

    A = np.array([
        [ 0.54748989, -3.28156307,  1.5146247 , -1.29057552],
        [ 1.17925623,  0.19553371, -0.39465974, -1.60525885],
        [ 0.14984667,  1.40491579, -0.4096218 , -3.29551032],
        [ 0.50900001, -0.24048083,  1.16530899, -0.3334018 ]
    ])

    Sigma = sigma * I

    Args:
        sigma (float): controls the magnitude of the system noise.        
    """
    Sigma = sigma * np.eye(MATRIX_ALL_IMAG_EIGS.shape[0])
    A = MATRIX_ALL_IMAG_EIGS
    return LinearSDE(A, Sigma)


    