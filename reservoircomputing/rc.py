"""
Module for reservoir computing. Modular implemented.

The classifier and reservoir must implement the interfaces as described by the rc_interface.py-module
"""
import numpy as np

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
        self._encoder = None

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

    @property
    def encoder(self):
        return self._encoder

    @encoder.setter
    def encoder(self, encoder):
        self._encoder = encoder


    def fit_to_training_set(self, training_set):
        """
        must split the training set in what to feed the reservoir and what to fit the classifier to
        :return:
        """
        number_of_generations = 4

        reservoir_outputs = []
        classifier_outputs = []

        for _input, _output in training_set:
            # TODO: Consider how to feed temporal sequences to the reservoir, ie. [_input1, _input2, ...]

            _input = self.encoder.encode(_input)

            reservoir_output = self.reservoir.run_simulation([_input], number_of_generations)
            reservoir_output = [ca_val for sublist in reservoir_output for ca_val in sublist]  # flatten
            reservoir_outputs.append(reservoir_output)
            classifier_outputs.append(_output)

        print("Finished propagating")
        self.classifier.fit(reservoir_outputs,classifier_outputs)
        print("finished fitting the classifier")

    def predict(self, _input):
        _input = self.encoder.encode(_input)
        reservoir_output = self.reservoir.run_simulation([_input], 4)

        reservoir_output = [ca_val for sublist in reservoir_output for ca_val in sublist]
        return self.classifier.predict(np.array(reservoir_output).reshape(-1, len(reservoir_output)))

    def propagate_in_reservoir(self, input_array):
        return self.reservoir.run_simulation(input_array)

