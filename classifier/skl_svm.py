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
        #print(str(len(training_input)))
        for i in range(len(training_input)):
            #print("FITTING: ")
            #print(str(len(training_input[i])))
            #print(training_input[i])
            #print(correct_predictions[i])
            #print("")
            pass
        return self.svm.fit(training_input, correct_predictions)

    def predict(self, reservoir_outputs):
        #print("PREdicting:")
        #print(reservoir_outputs)
        predictions = self.svm.predict(reservoir_outputs)
        #print(predictions)
        #print("")
        return predictions
