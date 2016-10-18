"""
Module for reservoir computing. Modular implemented.

The classifier and reservoir must implement the interfaces as described by the rc_interface.py-module
"""
import reservoir.ca as ca


class ReservoirComputingFramework:
    """
    Class used to execute reservoir computing
    It is responsible for

    The reservoir must implement the reservoir-interface
    The classifier must implement the classifier-interface


    """
    def __init__(self):
        self._reservoir = None
        self._classifier = None

    @property
    def reservoir(self):
        return self._reservoir

    @reservoir.setter
    def reservoir(self, reservoir):
        """
        The reservoir must be able to take an input, propagate it, and give an output.
        Input of reservoir must be a python-array of 0 and 1.
        Output must be a hierarchical list of the input that propagates
        :return:
        """
        self._reservoir = reservoir

    @property
    def classifier(self):
        return self._classifier

    @classifier.setter
    def classifier(self, classifier):
        self._classifier = classifier

    def propagate_in_reservoir(self, input_array):
        self.reservoir.run_simulation(input_array)
