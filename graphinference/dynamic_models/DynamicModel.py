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
    num_endogenous = attr.ib()
    num_exogenous = attr.ib()

    asdict = attr.asdict

class DynamicModel:
    """Abstract class outlining necessary dynamic modle methods.
    """
    def __init__(self, params: DynamicModelParams):
        self.params = params

    def random_initial_condition(self):
        """Draws an appropriate random initial condition for simulation.
        """
        raise NotImplementedError()
    
    def random_exogenous_input(self):
        """Creates appropriate external input
        """
        raise NotImplementedError()
    
    def simulate(
            self, 
            initial_state=None,
            exogeneous_input=None,
            variance_of_noise=0
        ):
        """Run a simulation of the system.
        
        Args:
            initial_state: """
        raise NotImplementedError()
    
    def jacobian(self, endogenous_state, exogeneous_state=None):
        """Produces a jacobian of the system given the state of the endogenous
        and exogenous variables."""
        raise NotImplementedError()
