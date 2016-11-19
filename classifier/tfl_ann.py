import tflearn


class ANN:
    def __init__(self):
        input_ = tflearn.input_data(shape=[None])
        linear = tflearn.single_unit(input_)
        regression = tflearn.regression(linear)
        self.m = tflearn.DNN(regression)

    def fit(self, training, correct):
        return self.m.fit(training, correct)

    def predict(self, reservoir_outputs):
        return self.m.predict(reservoir_outputs)


