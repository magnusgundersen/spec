"""
Project specific implementation of the CA-RC-system that is implemented.
More specifically this means that the RC-framework is initialized with project-specific reservoirs, and use
classifiers as chosen.

"""
__author__ = 'magnus'
from classifier import skl_svm as svm
from classifier import tfl_ann as tflann
from reservoir import ca as ca
from reservoircomputing import rc as rc
from reservoircomputing import rc_interface as rc_if
from encoder import rnd_mapping as rnd_map
from encoder import parallel as prl
from time_transition_encoder import normalized_addition as norm_add
from time_transition_encoder import random_permutation as rnd_perm
from time_transition_encoder import xor as xor
import random

global t
t=16 # FOR TRAINING SET SPLITTING! REMOVE

class RCCASystem:
    """
    Sets up the CA
    Set the CA as a reservoir
    etc...
    """
    def __init__(self):


        self.reservoir = None
        self.classifier = None
        self.encoder = None
        self.rc_framework = None

        self.rcca_config = None

    def use_svm(self):
        self.classifier = svm.SVM()
        self.rc_framework.classifier = self.classifier

    def use_elem_ca(self, rule_number):
        """
        """
        self.reservoir = ca.ElemCAReservoir()
        self.reservoir.set_rule(rule_number)
        self.rc_framework.reservoir = self.reservoir

    def use_random_mapping(self, r):
        self.encoder = rnd_map.RandomMappingEncoder()
        self.encoder.R = r
        self.rc_framework.encoder = self.encoder

    def use_uniform_iterations(self, I):
        self.iterations = I

    # Below is experimental code
    def set_problem(self, rcca_problem):
        self.rcca_problem = rcca_problem

    def set_config(self, rcca_config):
        self.rcca_config = rcca_config

    def initialize_rc(self):
        self.rcca_config.encoder.create_mappings(self.rcca_problem.get_input_size())
        rc_helper = rc.RCHelper(self.rcca_config)
        self.rc_framework = rc.ReservoirComputingFramework()
        self.rc_framework.set_helper(rc_helper)




    def fit_to_problem(self, validation_set_size=0.5):
        """

        :return:
        """
        if self.rcca_problem is None:
            raise ValueError("No RCCAProblem set!")

        # divide training_data:
        #training_data = self.rcca_problem.training_data[:int(len(self.rcca_problem.training_data)*(1-validation_set_size))]
        #test_data = self.rcca_problem.training_data[int(len(self.rcca_problem.training_data)*(1-validation_set_size)):]

        training_data = self.rcca_problem.training_data[:int(len(self.rcca_problem.training_data)*validation_set_size)]
        #print(str(len(self.rcca_problem.training_data)*validation_set_size))
        #print("size training set: " + str(len(training_data)))

        self.example_data = None
        # Run each training-example through the rc-framework
        for training_example in training_data:
            #  We now have a timeseries of data, on which the rc-framework must be fitted
            output = self.rc_framework.fit_to_data(training_example)
            if self.example_data is None:
                self.example_data = output

        self.rc_framework.train_classifier()
        #print("done with training")
        number_of_correct = 0
        """
        for test_ex in test_data:
            #  We now have a timeseries of data, on which the rc-framework must be fitted
            outputs = self.rc_framework.predict(test_ex)
            pointer = 0
            all_correct = True
            for _, output in test_ex:
                if output != outputs[pointer]:
                    #print("WRONG: " + str(output) + str( "  ") + str(outputs[pointer]))
                    all_correct = False
                pointer += 1
            if all_correct:
                number_of_correct += 1

        #print("Number of correct: " + str(number_of_correct) +" of " + str(len(test_data)))
        """
        return 0, 0

    def test_on_problem(self, test_set_size=0.5):
        """

                :return:
                """
        if self.rcca_problem is None:
            raise ValueError("No RCCAProblem set!")
        rcca_output = RCCAOutput()
        rcca_output.rcca_config = self.rcca_config


        # divide training_data:
        test_data = self.rcca_problem.training_data[int(len(self.rcca_problem.training_data)*test_set_size):]
        rcca_output.all_test_examples=test_data

        number_of_correct = 0

        for test_ex in test_data:
            #  We now have a timeseries of data, on which the rc-framework must be fitted
            outputs = self.rc_framework.predict(test_ex)
            rcca_output.all_RCOutputs.append(outputs)
            pointer = 0
            all_correct = True
            predictions = []
            for _, output in test_ex:
                predictions.append(outputs[pointer])
                if output != outputs[pointer]:
                    # print("WRONG: " + str(output) + str( "  ") + str(outputs[pointer]))
                    all_correct = False
                pointer += 1
            rcca_output.all_predictions.append(predictions)

            if all_correct:
                number_of_correct += 1

        # print("Number of correct: " + str(number_of_correct) +" of " + str(len(test_data)))

        rcca_output.total_correct = number_of_correct
        return rcca_output

    def get_example_run(self):
        return self.example_data

class RCCAOutput:
    def __init__(self):
        self.all_RCOutputs = []  # Includes full iterations, transitioned and input
        self.all_predictions = []
        self.correct_predictions = []
        self.all_test_examples = []
        self.rcca_config = None
        self.total_correct = 0

    def was_successful(self):
        if self.total_correct == len(self.all_test_examples):  # Success criteria
            return True
        return False




class RCCAProblem:
    """
    This class is used to precisely describe problems that may be feeded to the rcca-system
    """
    def __init__(self, example_runs):
        """
        The example runs parameter is used to input some example data to the system. Must be on the form:

        data =
        [
        [ (input, output),
          (input, output)
        ],
        [ (input, output),
          (input, output)
        ]
        ]

        Each list in the list corresponds to a temporal run of the system. If the problem is non-temporal the following
        data set is used:

        data =
        [
        [(input, output)],
        [(input, output)]
        ]

        :param example_runs:
        """

        self.number_of_time_steps = 1
        self.is_temporal = False
        self.training_data = []
        self.initialize_training_data(example_runs)
    @staticmethod
    def check_data_validity(ex_data):

        try:
            training_set_size = len(ex_data)
        except Exception as e:
            raise ValueError("Data must be a list!" + str(e))


        try:
            number_of_time_steps = len(ex_data[0])
        except Exception as e:
            raise ValueError("Data in each training-example was bad " + str(e))


        for data in ex_data:
            if len(data) != number_of_time_steps:
                raise ValueError("Every training set data must have same size! ")

            number_of_input_values = len(data[0][0])
            for time_step in data:
                if len(time_step[0]) != number_of_input_values:
                    raise ValueError("Every training example must have same size! ")


    def initialize_training_data(self, example_data):
        self.check_data_validity(example_data)

        self.number_of_time_steps = len(example_data[0])

        self.training_data = example_data
        random.shuffle(self.training_data)

        if self.number_of_time_steps > 1:
            self.is_temporal = True


    def get_timeseries_data(self):
        """
        Returns a list of the timeseries data
        :return:
        """
        if self.is_temporal:
            return self.training_data

    def get_input_size(self):
        return len(self.training_data[0][0][0])

class RCCAConfig(rc_if.ExternalRCConfig):
    def __init__(self):
        self.reservoir = None
        self.I = 0
        self.classifier = None
        self.encoder = None
        self.time_transition = None
        self.parallelizer = None

    def set_single_reservoir_config(self, ca_rule=105, R=4, C=3, I=12, classifier="linear-svm",
                                    encoding="random_mapping", time_transition="normalized_addition"):
        # sets up elementary CA:
        self.reservoir = ca.ElemCAReservoir()
        ca_rule = [ca_rule]  # Parallel?
        self.reservoir.set_rules(ca_rule)

        self.parallelizer = prl.ParallelNonUniformEncoder(self.reservoir.rules, "unbounded")

        # clf
        if classifier=="linear-svm":
            self.classifier = svm.SVM()
        elif classifier =="tlf_ann":
            self.classifier = tflann.ANN()


        # Encoder
        if encoding == "random_mapping":
            self.encoder = rnd_map.RandomMappingEncoder(self.parallelizer)
            self.encoder.R = R
            self.encoder.C = C

        self.I = I
        if time_transition=="normalized_addition":
            self.time_transition = norm_add.RandomAdditionTimeTransition()
        elif time_transition == "random_permutation":
            self.time_transition = rnd_perm.RandomPermutationTransition()
        elif time_transition == "xor":
            self.time_transition = xor.XORTimeTransition()

    def set_parallel_reservoir_config(self, ca_rules=(105,110), parallel_size_policy="unbounded", R=4, C=3, I=12,
                                      classifier="linear-svm", encoding="random_mapping",
                                      time_transition="normalized_addition"):

        # sets up elementary CA:
        self.reservoir = ca.ElemCAReservoir()
        self.reservoir.set_rules(ca_rules)

        #if parallel_size_policy
        self.parallelizer = prl.ParallelNonUniformEncoder(self.reservoir.rules, parallel_size_policy)


        # clf
        if classifier=="linear-svm":
            self.classifier = svm.SVM()
        elif classifier =="tlf_ann":
            self.classifier = tflann.ANN()

        # Encoder
        if encoding == "random_mapping":
            self.encoder = rnd_map.RandomMappingEncoder(self.parallelizer)
            self.encoder.R = R
            self.encoder.C = C

        self.I = I
        if time_transition=="normalized_addition":
            self.time_transition = norm_add.RandomAdditionTimeTransition()
        elif time_transition == "random_permutation":
            self.time_transition = rnd_perm.RandomPermutationTransition()

















