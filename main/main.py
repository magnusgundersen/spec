import ca.ca as ca

__author__ = 'magnus'

def runCA():
    testCA = ca.CA()

    ## IF initial
    init_gen_size = 333
    initial_generation = []
    for i in range(init_gen_size):
        initial_generation.append(0)
    initial_generation[50] = 1

    testCA.run_simulation(initial_generation,10,110)

runCA()

