import random

class RandomAdditionTimeTransition:
    def __init__(self):
        self.previous_inputs = {} # dict to contains the previous inputs to .....




    def normalized_adding(self, transmission_input, _input):

        transmitted_output = []
        for i in range(len(transmission_input)):
            a = transmission_input[i]
            b = _input[i]
            print("A and B: " + str(a) + " " + str(b))
            if a == 1 and b ==1:
                transmitted_output.append(1)
            elif a ==1 and b ==0:
                transmitted_output.append(random.choice([0, 1]))
            elif a == 0 and b == 1:
                transmitted_output.append(random.choice([0, 1]))
            elif a == 0 and b ==0:
                transmitted_output.append(0)
        return transmitted_output

    def translate(self, _input, R):
        """
        R might be neeed if the mapping must be the same each time step
        :param _input:
        :param R:
        :return:
        """
        if self.previous_inputs.get(R, default=None) is None:
            self.previous_inputs[R] = _input
            return _input
        _input = self.normalized_adding(self.previous_inputs[R], _input)
        self.previous_inputs[R] = _input
        return _input



