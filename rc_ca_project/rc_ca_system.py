"""
Project specific implementation of the CA-RC-system that is implemented.
More specifically this means that the RC-framework is initialized with project-specific reservoirs, and use
classifiers as chosen.

"""
__author__ = 'magnus'
from classifier import skl_svm as svm
from reservoir import ca as ca
from reservoircomputing import rc as rc


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
        self.reservoir.set_rule(110)
        self.rc_framework.reservoir = self.reservoir


    def initialize_system(self, reservoir_chosen, classification_chosen):
        if reservoir_chosen not in self.reservoir_alternatives \
                or classification_chosen not in self.classification_alternatives:
            raise ValueError("Illegal reservoir or classification")

        #self.rc_framework = ReservoirComputingFramework()

        if reservoir_chosen == "reservoir":
            reservoir = ca.CA()
            self.rc_framework.reservoir = reservoir

        if classification_chosen == "sklearn_svm":
            classification = svm.SVM()
            self.rc_framework.classifier = classification



    def train_system(self, training_set):
        """
        pairs of training-vector and correct classifiers

        """
        classifier_training_set = []
        self.rc_framework.fit_to_training_set(training_set)


        """
        for training_input, training_correct in training_set:
            # Propagates through the reservoir
            reservoir_output = self.rc_framework.propagate_in_reservoir(training_input)
            classifier_training_set.append((reservoir_output, training_correct))


        """
        pass


    def predict(self, _input):
        return self.rc_framework.predict(_input)



