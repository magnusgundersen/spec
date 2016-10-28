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


    def fit_to_training_set(self, training_set, iterations):
        """
        must split the training set in what to feed the reservoir and what to fit the classifier to
        :return:
        """
        number_of_generations = iterations

        reservoir_outputs = []
        classifier_outputs = []

        for _input, _output in training_set:
            # TODO: Consider how to feed temporal sequences to the reservoir, ie. [_input1, _input2, ...]
            #print("Running the training:")
            #print("INPUT: " + str(_input))
            encoded_input = self.encoder.encode_input(_input)
            #print("Encoded input:" + str(encoded_input))
            unencoded_output = []
            for _input in encoded_input:
                reservoir_output = self.reservoir.run_simulation(_input, number_of_generations)
                reservoir_output = [ca_val for sublist in reservoir_output for ca_val in sublist]  # flatten
                unencoded_output.append(reservoir_output)

            encoded_output = self.encoder.encode_output(unencoded_output)
            #print("Encoded output: " + str(encoded_output))
            reservoir_outputs.append(encoded_output)
            classifier_outputs.append(_output)

        print("Finished propagating")
        self.classifier.fit(reservoir_outputs,classifier_outputs)
        print("Finished fitting the classifier")

    def predict(self, _input, iterations):
        reservoir_output = self.reservoir.run_simulation([_input], iterations)

        encoded_input = self.encoder.encode_input(_input)
        unencoded_output = []
        for _input in encoded_input:
            reservoir_output = self.reservoir.run_simulation(_input, iterations)
            reservoir_output = [ca_val for sublist in reservoir_output for ca_val in sublist]  # flatten
            unencoded_output.append(reservoir_output)

        encoded_output = self.encoder.encode_output(unencoded_output)
        return self.classifier.predict(np.array(encoded_output).reshape(-1, len(encoded_output)))


    def run_example_simulation(self, _input, iterations):

        encoded_input = self.encoder.encode_input(_input)
        unencoded_output = []
        for _input in encoded_input:
            reservoir_output = self.reservoir.run_simulation(_input, iterations)
            #reservoir_output = [ca_val for sublist in reservoir_output for ca_val in sublist]  # flatten
            unencoded_output.append(reservoir_output)

        #encoded_output = self.encoder.encode_output(unencoded_output)
        return unencoded_output


