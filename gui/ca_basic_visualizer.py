__author__ = 'magnus'
from reservoir import ca as ca
import matplotlib.pyplot as plt
import random

class CAVisualizer:
    def __init__(self):
        pass

    def visualize(self, list_of_states):
        width = len(list_of_states[0])
        gens = len(list_of_states)

        fig, ax = plt.subplots(figsize=(10, 10))
        ax.pcolormesh(list_of_states, cmap="Greys")
        ax.set_xlim(0, width)
        ax.set_ylim(0, gens + 1)
        ax.set_title("CA")
        ax.set_axis_off()
        ax.set_aspect("equal")
        plt.show()

    def rule_vizualize(self, ca_rule, R, I, _input):

        width = 100
        gens = I

        elem_ca = ca.ElemCAReservoir()
        elem_ca.set_rule(ca_rule)
        short_input = _input[:]
        for _ in range(R):
            _input.extend(short_input)
        print(_input)
        output = elem_ca.run_simulation([_input], gens)
        output = output[::-1]
        self.visualize(output)


def CATests():
    width = 100
    gens = 120
    input_one = [0 for x in range(width)]
    input_one[width//2] = 1
    list_of_nums = [0,1]
    input_one = [random.choice(list_of_nums) for x in range(width)]
    input_one = [input_one]
    elem_ca = ca.ElemCAReservoir()
    elem_ca.set_rule(59)


    output = elem_ca.run_simulation(input_one,gens)
    output = output[::-1]

    viz = CAVisualizer()

    viz.visualize(output)




#CATests()
