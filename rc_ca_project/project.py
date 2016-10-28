"""
Project specific functionality

"""
__author__ = 'magnus'
from rc_ca_project import rc_ca_system as rcca
from gui import ca_basic_visualizer as bviz
import random
import pprint

class Project:
    """
    Contains all tasks and functionality specifically to the specialization project.

    Will communicate with the main, and give the user feedback if neccecery.


    """
    def __init__(self):
        pass

    def execute_majority_task(self, ca_rule=105, R=4, I=12, data_set_name="128_bit_mix_1000"):
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

    def five_bit_task(self, R=1, I=10, ca_rule=110, T=100):
        a1_values = [0,0,0,1,1] # 5-bit sequence


        # HACK: DUMMY VALUES
        temporal_training_set = []
        for _ in range(5):
            temporal_training_set.append(([1,0,0,0],'001'))
        for _ in range(T):
            temporal_training_set.append(([0,0,1,0], '001'))
        temporal_training_set.append(([0,0,0,1],'001'))
        for _ in range(5):
            temporal_training_set.append(([0,0,0,0],'100'))

        # Parameters
        fraction_use_for_test = 0.1

        rcca_system = rcca.RCCASystem()
        rcca_system.use_elem_ca(ca_rule)
        rcca_system.use_svm()
        rcca_system.use_random_mapping(R)
        rcca_system.use_uniform_iterations(I)

        #majority_data = self.open_data("majority/" + data_set_name)
        #majority_data = self.convert_to_array(majority_data)

        # use ten percent as test data
        #size_of_data = len(majority_data)
        #test_set_pointer = int(size_of_data * fraction_use_for_test)
        #test_set = majority_data[:test_set_pointer]
        #majority_data = majority_data[test_set_pointer:]

        rcca_system.train_temporal_system(temporal_training_set)

        #test_score = self.test_majority_task(test_set, rcca_system)


        pass


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





