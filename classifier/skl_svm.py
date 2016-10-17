__author__ = 'magnus'
from sklearn import svm as svm


class SVM:
    def __init__(self):
        self.svm = svm.SVC()

    def fit(self, training_input, correct_predictions):
        self.svm.fit(training_input, correct_predictions)

    def predict(self, _input):
        print(self.svm.predict(_input))
