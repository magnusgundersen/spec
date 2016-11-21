"""
Project specific functionality

"""
__author__ = 'magnus'
from rc_ca_project import rc_ca_system as rcca
from gui import ca_basic_visualizer as bviz
import random
import pprint
import itertools # for permutations
import csv
import os
import pickle as pickle

from multiprocessing import Pool

def run_exec(n_bit_data, rule, rcca_problem, rcca_config):
    """
    Parallelizable
    :param n_bit_data:
    :param rule:
    :param R:
    :param I:
    :return:
    """

    rcca_system = rcca.RCCASystem()
    rcca_system.set_problem(rcca_problem)
    rcca_system.set_config(rcca_config)
    rcca_system.initialize_rc()

    _,_ = rcca_system.fit_to_problem()
    rcca_output = rcca_system.test_on_problem()


    return rcca_output

class Project:
    """
    Contains all tasks and functionality specifically to the specialization project.

    Will communicate with the main, and give the user feedback if neccecery.


    """
    def __init__(self):
        pass

    def run_bye_experiements(self):
        rules = [n for n in range(256)]
        rules = [60,90,102,105,150,153,165,180,195]  # Bye rules
        #rules = [182, 90]  # wuixcc
        Is_and_Rs = [(2,4),(2,8),(4,4),(4,8)]

        n_bit_data = self.open_temporal_data("temp_n_bit/5_bit_200_dist_32")
        random.shuffle(n_bit_data)

        ## Save:
        headline = "Rule\tI=2,R=4\t\tI=2,R=8\t\tI=4,R=4\t\tI=4,R=8\n"


        results = ""
        for rule in rules:
            rule_results = []
            for I, R in Is_and_Rs:
                rcca_problem = rcca.RCCAProblem(n_bit_data)
                rcca_config = rcca.RCCAConfig()
                rcca_config.set_single_reservoir_config(ca_rule=rule, R=R, C=10, I=I, classifier="linear-svm",
                                                        encoding="random_mapping",
                                                        time_transition="random_permutation")

                successful_runs = 0
                total_runs = 7

                with Pool(7) as p:
                    results_from_runs = p.starmap(run_exec, [(n_bit_data,rule, rcca_problem, rcca_config) for _ in range(total_runs)])

                csv_name = "rule_" + str(rule) + "_I" + str(I) + "R" + str(R)
                path = os.getcwd()
                path = path + r"\..\data\experiments_data\rule_" + str(rule) + "\\"  # raw string


                # Rule directory
                try:
                    os.makedirs(path)
                except OSError as exception:
                    pass

                # Pickles dir
                try:
                    os.makedirs(path + r"pickles\\")
                except OSError as exception:
                    pass


                # Dump pickles

                i = 0
                save_pickle = False
                for run in results_from_runs:
                    # save pickle
                    if save_pickle:
                        with open(path + "pickles\\run_" + str(i) + ".pkl", 'wb') as output:
                            pickle.dump(run.all_predictions, output, pickle.HIGHEST_PROTOCOL)
                    if run.was_successful():
                        successful_runs += 1
                    i += 1

                # csv
                with open(path + csv_name+".csv", 'w+', newline='') as f:
                    writer = csv.writer(f, dialect='excel')
                    #writer.writerow(["rule","correct"])
                    for run in results_from_runs:
                        writer.writerow([rule, run.total_correct])

                #print("successful: " + str(successful_runs) + " of " + str(len(results_from_runs)))
                percentage_success = (successful_runs/total_runs)*100
                percentage_success = round(percentage_success, 1)  # 43.6
                rule_results.append(percentage_success)
            rule_result = (str(rule)+"\t"+str(rule_results[0])+"\t\t"+str(rule_results[1])
                           + "\t\t"+str(rule_results[2])+"\t\t"+str(rule_results[3]))
            results += rule_result+"\n"


            with open(path +"rule_" + str(rule) + "_summary" + ".txt", 'w+') as f:
                temp_results = headline + rule_result
                f.write(temp_results)

        output = headline + results
        print(output)

        with open("bye_results.txt", 'w+') as f:
            f.write(output)
    def n_bit_task(self, n=5):


        n_bit_data = self.open_temporal_data("temp_n_bit/5_bit_5_dist_32")
        random.shuffle(n_bit_data)
        rcca_problem = rcca.RCCAProblem(n_bit_data)
        rcca_config = rcca.RCCAConfig()
        rcca_config.set_single_reservoir_config(ca_rule=110, R=4, C=1, I=32, classifier="linear-svm",
                                                encoding="random_mapping", time_transition="normalized_addition")
        #rcca_config.set_parallel_reservoir_config(ca_rules=[90,182], parallel_size_policy="bounded", R=64, C=1, I=16,
        #                              classifier="linear-svm", encoding="random_mapping",
        #                              time_transition="normalized_addition")

        rcca_system = rcca.RCCASystem()




        rcca_system.set_problem(rcca_problem)
        rcca_system.set_config(rcca_config)
        rcca_system.initialize_rc()
        rcca_system.fit_to_problem(validation_set_size=0.1)
        rcca_out = rcca_system.test_on_problem()
        print(str(rcca_out.total_correct) + " of " + str(len(rcca_out.all_test_examples)))
        print("--example--")
        example_run = rcca_out.all_predictions[0]
        example_test = rcca_out.all_test_examples[0]
        for i in range(len(example_run)):
            time_step = example_run[i]
            prediction = time_step[0]
            correct = example_test[i][1]
            _input = "".join([str(x) for x in example_test[i][0]])
            print("Input: " + _input +"  Correct: " + str(correct) +"  Predicted:" + str(prediction))

        # Visualize:
        """
        outputs = rcca_out.all_RCOutputs
        whole_output = []
        lists_of_states = [output.list_of_states for output in outputs]
        for output in lists_of_states:
            width = len(output[0])
            whole_output.extend(output)
            whole_output.extend([[-1 for _ in range(width)]])
        self.visualise_example(whole_output)
        """

        # Visualize:
        outputs = rcca_system.get_example_run()
        whole_output = []
        lists_of_states = [output.list_of_states for output in outputs]
        for output in lists_of_states:
            width = len(output[0])
            whole_output.extend(output)
            whole_output.extend([[-1 for _ in range(width)]])
        self.visualise_example(whole_output)


    def majority_task(self):

        majority_data = self.open_temporal_data("majority/8_bit_mix_1000")


        rcca_problem = rcca.RCCAProblem(majority_data)
        rcca_config = rcca.RCCAConfig()
        rcca_config.set_single_reservoir_config(ca_rule=90, R=16, C=3, I=9, classifier="linear-svm",
                                                encoding="random_mapping", time_transition="random_permutation")

        rcca_config.set_parallel_reservoir_config()

        rcca_system = rcca.RCCASystem()

        rcca_system.set_problem(rcca_problem)
        rcca_system.set_config(rcca_config)
        rcca_system.initialize_rc()

        rcca_system.fit_to_problem(validation_set_size=0.1)

    def run_mg_experiments(self):
        """

        :return:
        """

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






