__author__ = 'magnus'
from sklearn import svm as svm
from reservoircomputing import rc_interface as interfaces


class SVM(interfaces.RCClassifier()):
    def __init__(self):
        super(SVM, self).__init__()
        self.svm = svm.SVC()

    def fit(self, training_input, correct_predictions):
        return self.svm.fit(training_input, correct_predictions)

    def predict(self, reservoir_outputs):
        return self.svm.predict(reservoir_outputs)
