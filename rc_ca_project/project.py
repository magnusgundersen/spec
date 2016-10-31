"""
Project specific functionality

"""
__author__ = 'magnus'
from rc_ca_project import rc_ca_system as rcca
from gui import ca_basic_visualizer as bviz
import random
import pprint
import itertools # for permutations

class Project:
    """
    Contains all tasks and functionality specifically to the specialization project.

    Will communicate with the main, and give the user feedback if neccecery.


    """
    def __init__(self):
        pass

    def execute_majority_task(self, ca_rule=1, R=16, I=128, data_set_name="8_bit_mix_1000"):
        # Parameters
        fraction_use_for_test = 0.1

        rcca_system = rcca.RCCASystem()
        rcca_system.use_elem_ca(ca_rule)
        rcca_system.use_svm()
        rcca_system.use_random_mapping(R)
        rcca_system.use_uniform_iterations(I)

        majority_data = self.open_data("majority/"+data_set_name)
        majority_data = self.convert_to_array(majority_data)

        # use ten percent as test data
        size_of_data = len(majority_data)
        test_set_pointer = int(size_of_data*fraction_use_for_test)
        test_set = majority_data[:test_set_pointer]
        majority_data = majority_data[test_set_pointer:]

        rcca_system.train_system(majority_data)

        test_score = self.test_majority_task(test_set, rcca_system)

        visualize_rule = True
        if visualize_rule:
            vis = bviz.CAVisualizer()
            ex_run = rcca_system.run_example_simulation(majority_data[random.randint(0,100)][0], I)
            vis.visualize_multiple_reservoirs(ex_run)
            #pprint.pprint(ex_run)
            #print(ex_run)
            #vis.rule_vizualize(ca_rule, R, I, majority_data[random.randint(0,100)][0])
        return {"dataset": data_set_name,
                "ca_rule": ca_rule,
                "R": R,
                "I": I,
                "correct": test_score}

    def test_majority_task(self, test_set, rcca_system):
        number_of_correct = 0
        for _input, _output in test_set:
            predicted = rcca_system.predict(_input)

            #print("Predicted: " + str(predicted))
            #print("Correct: " + str(_output))
            if predicted>=0.5 and _output == 1:
                number_of_correct += 1
            elif predicted<0.5 and _output == 0:
                number_of_correct += 1
        print("correct:" + str(number_of_correct) + " of " + str(len(test_set)))

        run_vis = False  # DOES NOT WORK
        if run_vis:
            visable = rcca_system.run_example_simulation(test_set[-1])
            self.visualise_example(visable)

        return (number_of_correct / len(test_set)) * 100

    def five_bit_task(self, R=4, I=10, ca_rule=90):


        n_bit_data = self.open_temporal_data("temp_n_bit/8_bit_1_dist_256")

        rcca_problem = rcca.RCCAProblem(n_bit_data)

        # Parameters
        fraction_use_for_test = 0.1

        rcca_system = rcca.RCCASystem()
        rcca_system.use_elem_ca(ca_rule)
        rcca_system.use_svm()
        rcca_system.use_random_mapping(R)
        rcca_system.use_uniform_iterations(I)

        rcca_system.set_problem(rcca_problem)



        #rcca_system.train_temporal_system(n_bit_data)



    def test_n_bit_task(self, test_set, rcca_system, n=5):
        number_of_correct = 0
        print("test set: " + str(test_set))

        test_set_inputs = [[temporal_list2[0] for temporal_list2 in temporal_list] for temporal_list in test_set]
        test_set_outputs = [[temporal_list2[1] for temporal_list2 in temporal_list] for temporal_list in test_set]
        print("inputs: " + str(test_set_inputs))
        predictions = rcca_system.predict_temporal(test_set_inputs)

        for i in range(len(predictions)):
            if predictions[i] == test_set_outputs[i]:
                print("Correct!")
            print("Prediction: " + str(predictions[i]))
            print("Correct:    " + str(test_set_outputs[i]))



        """
        for timestep in test_set:

            for _input, _output in timestep:
                predicted = rcca_system.predict_temporal(_input)
                print("Predicted: " + str(predicted))
                print("Correct:   " + str(_output))
        #print("correct:" + str(number_of_correct) + " of " + str(len(test_set)))
        """

        run_vis = False  # DOES NOT WORK
        if run_vis:
            visable = rcca_system.run_example_simulation(test_set[-1])
            self.visualise_example(visable)

        return (number_of_correct / len(test_set)) * 100


    def visualise_example(self, training_array):
        visualizer = bviz.CAVisualizer()
        visualizer.visualize(training_array)

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

    def open_temporal_data(self, filename):
        dataset = []
        with open("../data/"+filename, "r") as f:
            content = f.readlines()
            training_set = []
            for line in content:
                if line == "\n":
                    dataset.append(training_set)
                    training_set = []
                else:
                    _input, _output = line.split(" ")
                    training_set.append(([int(number) for number in _input],_output[0:-1]))
        return dataset






