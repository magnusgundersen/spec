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
import classifier.skl_svm as svmclf
import random

import rc.rc as rc
__author__ = 'magnus'


def runCA():
    testCA = ca.CA()

    ## IF initial
    init_gen_size = 10000
    initial_generation = []
    for i in range(init_gen_size):
        initial_generation.append(0)
    initial_generation[50] = 1

    number_of_generations = 100
    ca_rule = 110

    all_generations = testCA.run_simulation(initial_generation,number_of_generations,ca_rule)

    flat_ca_list = [ca_val for sublist in all_generations for ca_val in sublist]
    size_of_list = len(flat_ca_list)
    dummy_training = [flat_ca_list for _ in range(100)]
    dummy_correct = [random.randint(0,1) for _ in range(100)]
    print(len(dummy_training))
    svm = svmclf.SVM()
    svm.fit(dummy_training,dummy_correct)

    svm.predict([random.randint(0,1) for _ in range(size_of_list)])

#runCA()


def runRC():
    rc_system = rc.ReservoirSystem()
    rc_system.initialize_system('ca','sklearn_svm')
    rc_system.train_system()


runRC()
