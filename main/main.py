"""
Main-file for executing the CA-RC framework written by Magnus Gundersen

System consists of:
ca-package: Contains a cellular automata simulator.
classifier-package: Contains various implementations of a classifier. Is used for the readout-layer of the RC-system
rc-package: Contains the reservoir computation framework in which the CA may be used as a reservoir

gui-package: Tentative GUI-package which is proposed used to visualize the computations
tests-package: Tentative package for testing the various parts of the system. e.g. the rules of the CA.

"""
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

