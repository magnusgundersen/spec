"""
Module for reservoir computing. Modular implemented.

The classifier and reservoir must implement the interfaces as described by the rc_interface.py-module
"""
import numpy as np
import random
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)



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

        self.classifier_input_set = []
        self.classifier_output_set = []

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

    def set_helper(self, rc_helper):
        self.rc_helper = rc_helper
        self.classifier = rc_helper.config.classifier

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






    def predict_old(self, _input, iterations):

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

    def fit_to_data(self, training_data):
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

        self.rc_helper.reset()
        rc_outputs = []
        for _input, _output in training_data: # input and output at each timestep
            rc_output = self.rc_helper.run_input(_input)
            rc_outputs.append(rc_output)
            # make training-set for the classifier:
            self.classifier_input_set.append(rc_output.flattened_states)
            self.classifier_output_set.append(_output)

        return rc_outputs




    def train_classifier(self):
        print("Fitting classifier")
        for _ in range(0):
            self.classifier_input_set += self.classifier_input_set
            self.classifier_output_set += self.classifier_output_set
        self.classifier.fit(self.classifier_input_set, self.classifier_output_set)

    def predict(self, test_data):
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

        _outputs = []
        classifier_input_set = []
        self.rc_helper.reset()
        number_of_correct = 0
        for _input, _output in test_data:  # input and output at each timestep
            rc_output = self.rc_helper.run_input(_input)
            classifier_input = rc_output.flattened_states
            classifier_prediction = self.classifier.predict(classifier_input)
            _outputs.append(classifier_prediction)


            # HACK
            #print("Correct class: " + str(_output))
            #print("predicted cls: " + str(classifier_prediction))
            #print("Correct: "+ str(_output) +"     Prediction"+ str(classifier_prediction))
            if _output == classifier_prediction[0]:
                number_of_correct += 1
        #print("number: " + str(number_of_correct) + " of "+str(len(test_data)))
        return _outputs





class RCHelper:
    def __init__(self, external_config):
        self.config = external_config
        self.encoder = self.config.encoder
        self.time_transition = self.config.time_transition
        self.reservoir = self.config.reservoir
        self.I = self.config.I
        self.parallelizer = self.config.parallelizer


    def reset(self):
        self.time_step = 0
        self.previous_data = []
        self.last_step_data = [] #ONLY FOR CONCAT RESERVOIRS!

    def run_input(self, _input):
        # Run input that is deptandant on previous inputs
        # 1. step is to consider if the reservoir landscape is parallelized
        # TODO: currently not implemented

        # 2. Step is to encode the input
        encoded_inputs = self.encoder.encode_input(_input)  # List of lists
        # 3. Step is to concat or keep the inputs by themselves
        # TODO: Remove this if you want to be able to have separate reservoirs!
        encoded_input = [val for sublist in encoded_inputs for val in sublist]

        encoded_input, rule_dict = self.parallelizer.encode(encoded_input)

        # 4. step is to use transition to take previous steps into account
        if self.time_step > 0:  # No transition at first time step
            transitioned_data = self.time_transition.join(encoded_input, self.last_step_data, self.encoder)
        else:
            transitioned_data = encoded_input

          # ajour

        # 5. step is to propagate in CA reservoir
        all_propagated_data = self.reservoir.run_simulation(transitioned_data, self.I,  rule_dict)
        self.last_step_data = all_propagated_data[-1]

        # 6. step is to create an output-object
        output = RCOutput()
        output.set_states(all_propagated_data, self.last_step_data)

        self.time_step += 1

        return output















class RCOutput:

    def __init__(self):
        self.list_of_states = []
        self.transitioned_state = []
        self.flattened_states = []

    def set_states(self, all_states, transitioned_state):
        self.list_of_states = all_states
        self.transitioned_state = transitioned_state
        self.flattened_states = [state_val for sublist in all_states for state_val in sublist]











