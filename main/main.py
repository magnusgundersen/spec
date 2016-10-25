"""
Main-file for executing the CA-RC framework written by Magnus Gundersen

System consists of:
reservoir-package: Contains a cellular automata simulator.
classifier-package: Contains various implementations of a classifier. Is used for the readout-layer of the RC-system
reservoircomputing-package: Contains the reservoir computation framework in which the CA may be used as a reservoir

gui-package: Tentative GUI-package which is proposed used to visualize the computations
tests-package: Tentative package for testing the various parts of the system. e.g. the rules of the CA.

"""
#import sys
#import reservoir.ca as ca
#import classifier.skl_svm as svmclf
import random
from rc_ca_project import project as project

import reservoircomputing.rc as rc
__author__ = 'magnus'

def main():
    p = project.Project()
    #p.execute_test1()


    print(p.execute_majority_task())


if __name__ == "__main__":
    main()


