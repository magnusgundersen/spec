"""
Module that shows how the classifiers and reservoirs must be implemented

As this is not Java, they are strictly not needed, but they work as architectural help.
"""
__author__ = 'magnus'


class RCClassifier:
    """
    Functioning as an interface of a classifier that may be used for the rc-system
    """
    def __init__(self):
        pass

    def fit(self, reservoir_outputs, correct_classifications):
        raise NotImplementedError("fit must be implemented to fit the classifier to the output of the reservoir")

    def predict(self, reservoir_outputs):
        raise NotImplementedError('')

class RCReservoir:
    """

    """
    def __init__(self):
        pass