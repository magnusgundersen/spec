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

    def run_simulation(self, _input):
        raise NotImplementedError

class RCEncoder:
    """

    """
    def __init__(self):
        pass

    def encode_input(self, _input):
        """
        Encode the input in whatever way.

        _input is an array,
        :param _input:
        :return:
        """
        raise NotImplementedError

    def encode_output(self, _output):
        """

        :param _output:
        :return:
        """
        raise NotImplementedError


class ExternalRCConfig:
    def __init__(self):
        pass