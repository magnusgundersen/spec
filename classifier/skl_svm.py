__author__ = 'magnus'
from sklearn import svm as svm
from sklearn.linear_model import ridge as ridge
from sklearn import neighbors as neig

from reservoircomputing import rc_interface as interfaces


class SVM(interfaces.RCClassifier):
    def __init__(self):
        super(SVM, self).__init__()
        self.svm = svm.LinearSVC()
        #self.svm = ridge.Ridge()
        #self.svm = neig.KNeighborsClassifier()

    def fit(self, training_input, correct_predictions):
        #print("[SVM] " + str(training_input[:100]))
        #print("[SVM] " + str(correct_predictions[:100]))
        #print(training_input)
        return self.svm.fit(training_input, correct_predictions)

    def predict(self, reservoir_outputs):
        return self.svm.predict(reservoir_outputs)
