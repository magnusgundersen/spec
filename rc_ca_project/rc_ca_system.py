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


    def predict(self, _input):
        return self.rc_framework.predict(_input, self.iterations)

    def run_example_simulation(self, _input, iterations):
        return self.rc_framework.run_example_simulation(_input, iterations)


