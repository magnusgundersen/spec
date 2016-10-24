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
        # Parameters
        ca_rule = 105
        fraction_use_for_test = 0.1
        data_set_number = "mix"

        rcca_system = rcca.RCCASystem()
        rcca_system.use_elem_ca(ca_rule)
        rcca_system.use_svm()

        majority_data = self.open_data("majority/"+data_set_number)
        majority_data = self.convert_to_array(majority_data)

        # use ten percent as test data
        size_of_data = len(majority_data)
        test_set_pointer = int(size_of_data*fraction_use_for_test)
        test_set = majority_data[:test_set_pointer]
        majority_data = majority_data[test_set_pointer:]

        rcca_system.train_system(majority_data)

        self.test_majority_task(test_set, rcca_system)

    def test_majority_task(self, test_set, rcca_system):
        number_of_correct = 0
        for _input, _output in test_set:
            predicted = rcca_system.predict(_input)

            #print("Predicted: " + str(predicted))
            #print("Correct: " + str(_output))
            if predicted>0.55 and _output == 1:
                number_of_correct += 1
            elif predicted<0.55 and _output == 0:
                number_of_correct += 1
        print("correct:" + str(number_of_correct) + " of " + str(len(test_set)))

    def convert_to_array(self, training_set):
        new_training_set = []
        for _input,_output in training_set:
            new_training_set.append(([int(number) for number in _input],int(_output)))

        return new_training_set

    def open_data(self, filename):
        """
        Reads data from file

        data must be on the form of

        1010010101...100101 0

        Where the first vector is binary, and the last integer is the class. Must also be binary.
        :param filename:
        :return:
        """
        dataset = []
        with open("../data/"+filename, "r") as f:
            content = f.readlines()
            for line in content:
                _input, _output = line.split(" ")
                dataset.append((_input,_output[0]))
        return dataset





