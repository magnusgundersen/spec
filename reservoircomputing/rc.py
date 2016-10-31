"""
Module for reservoir computing. Modular implemented.

The classifier and reservoir must implement the interfaces as described by the rc_interface.py-module
"""
import numpy as np
import random

import sklearn.svm as svm  # REMOVE! SEE HACK below

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

    def encode_and_execute(self, _input, iterations):
        # CONSIDER IF NEED TO BE MOVED

        # NOTE: CURRENTLY DOES NOT SUPPORT R >1 !


        encoded_inputs = self.encoder.encode_input(_input)
        reservoir_outputs = []
        print("Encoded inputs: " + str(encoded_inputs))
        for encoded_input in encoded_inputs:
            reservoir_outputs.append(self.reservoir.run_simulation(encoded_input, iterations))



        return reservoir_outputs


    def fit_to_training_data(self):
        """
        Function to be used for fitting the whole rc-system to some data set.
        May be both temporal and non-temporal
        :return:
        """
        pass

    def fit_to_training_set(self, training_set, iterations):
        """
        must split the training set in what to feed the reservoir and what to fit the classifier to
        :return:
        """

        reservoir_outputs = []
        classifier_outputs = []


        for _input, _output in training_set:
            encoded_input = self.encoder.encode_input(_input)
            #print("Encoded input:" + str(encoded_input))
            unencoded_output = []

            for _input in encoded_input:  # If multiple reservoirs
                reservoir_output = self.reservoir.run_simulation(_input, iterations)
                reservoir_output = [ca_val for sublist in reservoir_output for ca_val in sublist]  # flatten
                unencoded_output.append(reservoir_output)

            encoded_output = self.encoder.encode_output(unencoded_output)
            #print("Encoded output: " + str(encoded_output))
            reservoir_outputs.append(encoded_output)
            classifier_outputs.append(_output)

        print("Finished propagating")
        self.classifier.fit(reservoir_outputs,classifier_outputs)
        print("Finished fitting the classifier")

    def normalized_adding(self, transmission_input, _input):
        # TODO: REMOVE FROM this class
        transmitted_output = []
        for i in range(len(transmission_input)):
            a = transmission_input[i]
            b = _input[i]
            print("A and B: " + str(a) + " " + str(b))
            if a == 1 and b ==1:
                transmitted_output.append(1)
            elif a ==1 and b ==0:
                transmitted_output.append(random.choice([0, 1]))
            elif a == 0 and b == 1:
                transmitted_output.append(random.choice([0, 1]))
            elif a == 0 and b ==0:
                transmitted_output.append(0)
        return transmitted_output



    def fit_to_temporal_training_set(self, training_set, iterations, transmission_scheme="adding"):
        """
        Fits the trainer to the temporal data

        transmission scheme

        :param training_set:
        :param iterations:
        :param transmission_scheme:
        :return:
        """
        transmission_input = [[train_tuple[0] for _ in range(self.encoder.R)] for train_tuple in training_set[0]]  # Initializes the transmission inputs
        print("Transmission_input: " + str(transmission_input))
        classifier_outputs = []
        timestep_reservoir_outputs = []
        for i in range(len(training_set)):
            for _input, _output in training_set[i]:
                if i > 0:
                    _input = self.normalized_adding(transmission_input[i-1], _input)
                    # MAJOR PROBLEM: This style of encoding encodes R times each timstep
                    # The same encoding must following in time

                reservoir_output = self.encode_and_execute(_input, iterations)  # This is a list of lists

                transmission_input.append([reservoir_output[j][-1] for j in range(len(reservoir_output))])  # append the last state to norm. add the next gen
                timestep_reservoir_outputs.append(self.encoder.encode_output(reservoir_output))  # Flatten

                classifier_outputs.append(_output)



        flattened_outputs = []
        for output in timestep_reservoir_outputs:
            # Flatten
            new_output = [ca_val for sublist in output for ca_val in sublist]
            flattened_outputs.append(new_output)
        print("-----")
        print("Flattened output to train the calssifier:")
        print(len(flattened_outputs))
        print(flattened_outputs[0])
        print("-")


        self.classifier.fit(flattened_outputs, classifier_outputs)


    def predict(self, _input, iterations):

        encoded_input = self.encoder.encode_input(_input)
        unencoded_output = []
        for _input in encoded_input:
            reservoir_output = self.reservoir.run_simulation(_input, iterations)
            reservoir_output = [ca_val for sublist in reservoir_output for ca_val in sublist]  # flatten
            unencoded_output.append(reservoir_output)

        encoded_output = self.encoder.encode_output(unencoded_output)
        return self.classifier.predict(np.array(encoded_output).reshape(-1, len(encoded_output)))

    def predict_temporal_system(self, temporal_input, iterations):
        predictions = []
        transmission_input = [train_input for train_input in temporal_input[0]]

        for i in range(len(temporal_input)):
            predictions_at_this_timestep = []
            encoded_input = temporal_input[i]
            unencoded_output = []
            all_output = []
            for _input in encoded_input:
                if i > 0:
                    _input = self.normalized_adding(transmission_input[i-1], _input)

                reservoir_output = self.encode_and_execute([_input], iterations)
                transmission_input.append(reservoir_output[-1])
                reservoir_output = [ca_val for sublist in reservoir_output for ca_val in sublist]  # flatten
                prediction = self.classifier.predict(np.array(reservoir_output).reshape(-1, len(reservoir_output)))
                predictions_at_this_timestep.append(prediction)

            predictions.append(predictions_at_this_timestep)

        return predictions


    def run_example_simulation(self, _input, iterations):

        encoded_input = self.encoder.encode_input(_input)
        unencoded_output = []
        for _input in encoded_input:
            reservoir_output = self.reservoir.run_simulation(_input, iterations)
            #reservoir_output = [ca_val for sublist in reservoir_output for ca_val in sublist]  # flatten
            unencoded_output.append(reservoir_output)

        #encoded_output = self.encoder.encode_output(unencoded_output)
        return unencoded_output

    # Expermiental is below!

    def fit_to_data(self, training_data, transmission_scheme="addition"):
        """

        The input consists of data:

        temporal_data =
        [
        (input, output),
        (input, output)
        ]

        or:

        non_temporal_data =
        [
        (input, output)
        ]

        :param training_data:
        :return:
        """

        transmission_data = []
        current_time_step = 0
        for _input, _output in training_data: # input and output at each timestep
            if current_time_step > 0:
                _input = self.time_transistor.translate()

            current_time_step += 1
            # TODO: Here it must come something to do with the transmission between the time steps!


