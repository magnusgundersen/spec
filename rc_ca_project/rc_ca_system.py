"""
Project specific implementation of the CA-RC-system that is implemented.
More specifically this means that the RC-framework is initialized with project-specific reservoirs, and use
classifiers as chosen.

"""
__author__ = 'magnus'
from classifier import skl_svm as svm
from reservoir import ca as ca
from reservoircomputing import rc as rc
from encoder import rnd_mapping as rnd_map


class RCCASystem:
    """
    Sets up the CA
    Set the CA as a reservoir
    etc...
    """
    def __init__(self):
        self.classification_alternatives = ['sklearn_svm']
        self.reservoir_alternatives = ['elem_ca']
        self.reservoir = None  # ca.ElemCAReservoir()
        #self.reservoir.set_rule(ca_rule)
        self.classifier = None  # svm.SVM()
        self.encoder = None
        self.rc_framework = rc.ReservoirComputingFramework()
        #self.rc_framework.reservoir = self.reservoir
        #self.rc_framework.classifier = self.classifier

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




    def train_system(self, training_set):
        """
        pairs of training-vector and correct classifiers

        """
        classifier_training_set = []
        self.rc_framework.fit_to_training_set(training_set, self.iterations)

    def train_temporal_system(self, training_set, timestep_transfer_policy=None):
        self.rc_framework.fit_to_temporal_training_set(training_set, self.iterations)


    def predict(self, _input):
        return self.rc_framework.predict(_input, self.iterations)

    def predict_temporal(self, _input):

        return self.rc_framework.predict_temporal_system(_input, self.iterations)

    def run_example_simulation(self, _input, iterations):
        return self.rc_framework.run_example_simulation(_input, iterations)

    # Below is experimental code
    def set_problem(self, rcca_problem):
        self.rcca_problem = rcca_problem

    def fit_to_problem(self):
        """

        :return:
        """
        if self.rcca_problem is None:
            raise ValueError("No RCCAProblem set!")

        # Run each training-example through the rc-framework
        for training_example in self.rcca_problem.training_data:
            #  We now have a timeseries of data, on which the rc-framework must be fitted
            for time_series_data in training_example:
                # The time_step now contains a list of tuples of inputs and outputs

                self.rc_framework.fit_to_data(time_series_data)






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


    def initialize_training_data(self, example_data):
        self.check_data_validity(example_data)

        self.number_of_time_steps = len(example_data[0])

        self.training_data = example_data

        if self.number_of_time_steps > 1:
            self.is_temporal = True


    def get_timeseries_data(self):
        """
        Returns a list of the timeseries data
        :return:
        """
        if self.is_temporal:
            return self.training_data




