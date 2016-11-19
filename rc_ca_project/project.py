"""
Project specific functionality

"""
__author__ = 'magnus'
from rc_ca_project import rc_ca_system as rcca
from gui import ca_basic_visualizer as bviz
import random
import pprint
import itertools # for permutations

from multiprocessing import Pool

def run_exec(n_bit_data, rule, R, I):
    rcca_problem = rcca.RCCAProblem(n_bit_data)
    rcca_config = rcca.RCCAConfig()
    rcca_config.set_single_reservoir_config(ca_rule=rule, R=R, C=10, I=I, classifier="linear-svm",
                                            encoding="random_mapping",
                                            time_transition="random_permutation")
    rcca_system = rcca.RCCASystem()

    rcca_system.set_problem(rcca_problem)
    rcca_system.set_config(rcca_config)
    rcca_system.initialize_rc()

    correct, total = rcca_system.fit_to_problem(validation_set_size=0.1)
    if correct == total:
        return 1
    return 0

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
        rules = [22, 88]  # wuixcc
        Is_and_Rs = [(2,4),(2,8),(4,4),(4,8)]

        n_bit_data = self.open_temporal_data("temp_n_bit/5_bit_200_dist_32")
        random.shuffle(n_bit_data)

        ## Save:
        headline = "Rule\t\tI=2,R=4\t\tI=2,R=8\t\tI=4,R=4\t\tI=4,R=8\n"


        results = ""
        for rule in rules:
            rule_results = []
            for I, R in Is_and_Rs:
                successful_runs = 0
                total_runs = 100
                results_from_runs = []

                """
                def run():
                    rcca_problem = rcca.RCCAProblem(n_bit_data)
                    rcca_config = rcca.RCCAConfig()
                    rcca_config.set_single_reservoir_config(ca_rule=rule, R=R, C=10, I=I, classifier="linear-svm",
                                                            encoding="random_mapping",
                                                            time_transition="random_permutation")
                    rcca_system = rcca.RCCASystem()

                    rcca_system.set_problem(rcca_problem)
                    rcca_system.set_config(rcca_config)
                    rcca_system.initialize_rc()

                    correct, total = rcca_system.fit_to_problem(validation_set_size=0.1)

                    if correct == total:
                        return 1
                    return 0
                #for i in range(total_runs):
                #    results_from_runs.append(run())

                """
                with Pool(3) as p:
                    results_from_runs= p.starmap(run_exec, [(n_bit_data,rule, I, R) for _ in range(total_runs)])


                print(results_from_runs)
                successful_runs = results_from_runs.count(1)

                print("successful: " + str(successful_runs) + " of " + str(len(results_from_runs)))
                percentage_success = (successful_runs/total_runs)*100
                round(percentage_success,1)  # 43.6
                rule_results.append(percentage_success)
            rule_result = (str(rule)+"\t\t"+str(rule_results[0])+"\t\t"+str(rule_results[1])
                           + "\t\t"+str(rule_results[2])+"\t\t"+str(rule_results[3]))
            results += rule_result+"\n"

            with open("bye_results_rule_" + str(rule) + ".txt", 'w+') as f:
                temp_results = headline + rule_result
                f.write(temp_results)

        output = headline + results
        print(output)

        with open("bye_results.txt", 'w+') as f:
            f.write(output)
    def n_bit_task(self, n=5):


        n_bit_data = self.open_temporal_data("temp_n_bit/5_bit_200_dist_32")
        random.shuffle(n_bit_data)
        rcca_problem = rcca.RCCAProblem(n_bit_data)
        rcca_config = rcca.RCCAConfig()
        rcca_config.set_single_reservoir_config(ca_rule=90, R=4, C=10, I=4, classifier="linear-svm",
                                                encoding="random_mapping", time_transition="random_permutation")
        #rcca_config.set_parallel_reservoir_config(ca_rules=[180,180], parallel_size_policy="bounded", R=4, C=10, I=4,
        #                              classifier="linear-svm", encoding="random_mapping",
        #                              time_transition="random_permutation")

        rcca_system = rcca.RCCASystem()




        rcca_system.set_problem(rcca_problem)
        rcca_system.set_config(rcca_config)
        rcca_system.initialize_rc()

        print(rcca_system.fit_to_problem(validation_set_size=0.1))

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






