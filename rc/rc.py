import ca.ca as ca
import classifier.skl_svm as svm

class ReservoirSystem:
    def __init__(self):
        self.classification_alternatives = ['sklearn_ann', 'sklearn_svm', 'tflearn_ann']
        self.reservoir_alternatives = ['ca']
        self.rc_framework = None

    def initialize_system(self, reservoir_chosen, classification_chosen):
        if reservoir_chosen not in self.reservoir_alternatives \
                or classification_chosen not in self.classification_alternatives:
            raise ValueError("Illegal reservoir or classification")

        self.rc_framework = ReservoirComputingFramework()

        if reservoir_chosen == "ca":
            reservoir = ca.CA()
            self.rc_framework.reservoir = reservoir

        if classification_chosen == "sklearn_svm":
            classification = svm.SVM()
            self.rc_framework.classifier = classification



    def train_system(self, training_set):
        """
        pairs of training and correct classifiers

        """
        for training_input, training_correct in training_set:
            # Propagates through the reservoir
            self.rc_framework.propagate_in_reservoir()

        pass


    def predict(self):
        pass




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
