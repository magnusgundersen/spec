__author__ = 'magnus'
from reservoir import ca as ca
import matplotlib.pyplot as plt
import random

def CATests():
    width = 1000
    gens = 1000
    input_one = [0 for x in range(width)]
    input_one[width//2] = 1
    list_of_nums = [0,1,0,0,0,0]
    input_one = [random.choice(list_of_nums) for x in range(width)]
    input_one = [input_one]
    elem_ca = ca.ElemCAReservoir()
    elem_ca.set_rule(104)

    output = elem_ca.run_simulation(input_one,gens)
    output = output[::-1]

    fig, ax = plt.subplots(figsize=(10,10))
    ax.pcolormesh(output, cmap="Greys")
    ax.set_xlim(0, width)
    ax.set_ylim(0, gens+1)
    ax.set_title("CA")
    ax.set_axis_off()
    ax.set_aspect("equal")
    plt.show()


CATests()
