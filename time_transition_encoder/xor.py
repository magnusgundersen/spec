import random

class XORTimeTransition:
    def __init__(self):
        self.previous_inputs = {} # dict to contains the previous inputs to .....

    def join(self, _input, transition_input, encoder):
        return self.xor(transition_input, _input)

    def xor(self, transmission_input, _input):

        transmitted_output = []
        for i in range(len(transmission_input)):
            a = transmission_input[i]
            b = _input[i]

            if a == 1 and b == 1:
                transmitted_output.append(0)
            elif a ==1 and b == 0:  # Returning 1 gives good results
                transmitted_output.append(1) #random.choice([0, 1])
            elif a == 0 and b == 1:
                transmitted_output.append(1)
            elif a == 0 and b == 0:
                transmitted_output.append(0)
        return transmitted_output
