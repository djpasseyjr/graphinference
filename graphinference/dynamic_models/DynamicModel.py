"""Abstract dynamic model class.

A parent class that defines methods and data members for a 
`graphinference.DynamicModel`. Each concrete model in this
package inherets from this class and implements some or all
of the methods.
"""

import attr

@attr.s
class DynamicModelParams:
    """Simple storage class for model parameters"""
    asdict = attr.asdict

class DynamicModel:
    """Abstract class outlining necessary dynamic modle methods.
    """
    def __init__(self, params):
        self.params = params

    def random_initial_condition(self):
        """Draws an appropriate random initial condition for simulation.
        """
        raise NotImplementedError()
    
    def simulate(self, variance_of_noise=0):
        raise NotImplementedError()
    
    def jacobian(self, endogenous_state, exogeneous_state):
        raise NotImplementedError()
