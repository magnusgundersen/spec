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
        rcca_system = rcca.RCCASystem()
        rcca_system.use_elem_ca(110)
        rcca_system.use_svm()
        easy_majority_data = self.open_data("majority_hard.txt")
        easy_majority_data = self.convert_to_array(easy_majority_data)
        # use ten percent as test data
        size_of_data = len(easy_majority_data)
        test_set_pointer = int(size_of_data*0.1)
        test_set = easy_majority_data[:test_set_pointer]
        easy_majority_data = easy_majority_data[test_set_pointer:]
        rcca_system.train_system(easy_majority_data)

        self.test_majority_task(test_set, rcca_system)

    def test_majority_task(self, test_set, rcca_system):
        number_of_correct = 0
        for _input, _output in test_set:
            predicted = rcca_system.predict(_input)

            #print("Predicted: " + str(predicted))
            #print("Correct: " + str(_output))
            if predicted == _output:
                number_of_correct += 1
        print("correct:" + str(number_of_correct) + " of " + str(len(test_set)))



        #raise NotImplementedError()
    """

    def execute_test1(self):

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

"""
    def convert_to_array(self, training_set):
        new_training_set = []
        for _input,_output in training_set:
            new_training_set.append(([int(number) for number in _input],_output))

        return new_training_set

    def open_data(self, filename):
        dataset = []
        with open("../data/"+filename, "r") as f:
            content = f.readlines()
            for line in content:
                _input, _output = line.split(" ")
                dataset.append((_input,_output[0]))
        return dataset
"""

def runRC():
    rc_system = rc.ReservoirSystem()
    rc_system.initialize_system('reservoir','sklearn_svm')
    rc_system.train_system()


"""



