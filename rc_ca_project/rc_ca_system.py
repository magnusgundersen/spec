"""
Project specific implementation of the CA-RC-system that is implemented.
More specifically this means that the RC-framework is initialized with project-specific reservoirs, and use
classifiers as chosen.

"""
__author__ = 'magnus'
import classifier.skl_svm as svm
from reservoir import ca as ca


class RCCASystem:
    """
    Sets up the CA
    Set the CA as a reservoir

    etc...
    """
    def __init__(self):
        self.classification_alternatives = ['sklearn_svm']
        self.reservoir_alternatives = ['elem_ca']
        self.rc_framework = None

        self.reservoir = None
        self.classifier = None

    def use_elem_ca(self, rule_number):
        """
        """
        self.reservoir = ca.ElemCAReservoir()
        self.reservoir.set_rule(110)


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
        pairs of training and correct classifiers

        """
        classifier_training_set = []
        for training_input, training_correct in training_set:
            # Propagates through the reservoir
            reservoir_output = self.rc_framework.propagate_in_reservoir(training_input)
            classifier_training_set.append((reservoir_output, training_correct))



        pass


    def predict(self):
        pass


