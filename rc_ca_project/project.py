"""
Project specific functionality

"""
__author__ = 'magnus'
from rc_ca_project import rc_ca_system as rcca

class Project:
    """
    Contains all tasks and functionality specifically to the specialization project.

    Will communicate with the main, and give the user feedback if neccecery.


    """
    def __init__(self):
        pass

    def execute_majority_task(self):
        raise NotImplementedError()

    def execute_test1(self):
        rcca_system = rcca.RCCASystem() # Init a system that has elementary CA as reservoir and SVM as clf
        rcca_system.use_elem_ca(110)
        test_data =

        rcca_system.


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
    rc_system.initialize_system('reservoir','sklearn_svm')
    rc_system.train_system()


runRC()
        pass



