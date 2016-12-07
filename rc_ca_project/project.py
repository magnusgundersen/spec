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
import time

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
    portion_training_set = 0.5
    rcca_system = rcca.RCCASystem()
    rcca_system.set_problem(rcca_problem)
    rcca_system.set_config(rcca_config)
    rcca_system.initialize_rc()

    _,_ = rcca_system.fit_to_problem(1)
    rcca_output = rcca_system.test_on_problem(0)


    return rcca_output

class Project:
    """
    Contains all tasks and functionality specifically to the specialization project.

    Will communicate with the main, and give the user feedback if neccecery.


    """
    def __init__(self):
        pass

    def run_bye_experiements(self):
        print("Running bye-experiments")
        rules = [60,90,102,105,150,153,165,180,195]  # Bye rules
        #rules = [182, 90]  # wuixcc
        Is_and_Rs = [(2,4),(2,8),(4,4),(4,8)]
        total_runs_per_config = (4*7)

        n_bit_data = self.open_temporal_data("temp_n_bit/5_bit_200_dist_32")
        random.shuffle(n_bit_data)

        ## Save:
        headline = "Rule\t\tI=2,R=4\t\tI=2,R=8\t\tI=4,R=4\t\tI=4,R=8\n"


        results = ""
        before_time = time.time()
        for rule in rules:
            print("Executing rule: " + str(rule))
            rule_results = []

            for I, R in Is_and_Rs:
                rcca_problem = rcca.RCCAProblem(n_bit_data)
                rcca_config = rcca.RCCAConfig()
                rcca_config.set_single_reservoir_config(ca_rule=rule, R=R, C=10, I=I, classifier="linear-svm",
                                                        encoding="random_mapping",
                                                        time_transition="random_permutation")

                successful_runs = 0

                with Pool(7) as p:
                    results_from_runs = p.starmap(run_exec,
                                                  [(n_bit_data,rule,
                                                    rcca_problem, rcca_config) for _ in range(total_runs_per_config)])

                csv_name = "rule_" + str(rule) + "_I" + str(I) + "R" + str(R)
                path = os.getcwd()
                path = path + r"\..\data\experiments_data\rule_" + str(rule) + "\\"  # raw string


                # Rule directory
                try:
                    os.makedirs(path)
                except OSError as exception:
                    pass



                save_pickle = False
                # Pickles dir
                if save_pickle:
                    try:
                        os.makedirs(path + r"pickles\\")
                    except OSError as exception:
                        pass


                # Dump pickles ++
                i = 0
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
                    for run in results_from_runs:
                        writer.writerow([rule, run.total_correct, len(run.all_test_examples)])

                #print("successful: " + str(successful_runs) + " of " + str(len(results_from_runs)))
                percentage_success = (successful_runs/total_runs_per_config)*100
                percentage_success = round(percentage_success, 1)  # 43.6
                rule_results.append(percentage_success)

            if results=="":
                one_rule = (time.time()-before_time)
                no_of_rules = len(rules)
                total_time_estimated = no_of_rules*one_rule
                print("Total estimated_time: " + str(int(total_time_estimated)) + " seconds")
                print("In minutes: " + str(total_time_estimated//60))
                print("In hours: " + str(total_time_estimated // 3600))

            rule_result = (str(rule)+"\t\t"+str(rule_results[0])+"\t\t\t"+str(rule_results[1])
                           + "\t\t\t"+str(rule_results[2])+"\t\t\t"+str(rule_results[3]))
            results += rule_result+"\n"


            with open(path +"rule_" + str(rule) + "_summary" + ".txt", 'w+') as f:
                temp_results = headline + rule_result
                f.write(temp_results)

        output = headline + results
        print(output)
        print("total time used in seconds:" + str(time.time() - before_time))

        with open(path + "..\\bye_results_summary.txt", 'w+') as f:
            f.write(output)

    def run_yil_experiment_IR(self):
        print("Running Yilmaz-experiments")
        rules = [n for n in range(256)]
        rules = [22, 90, 150, 182]  # Yil rules

        Is_and_Rs = [(8, 8), (8, 16), (8, 32), (8, 64),
                     (16, 8), (16, 16), (16, 32), (16, 64),
                     (32, 8), (32, 16), (32, 32), (32, 64)
                     ]
        total_runs_per_config = 8

        n_bit_data = self.open_temporal_data("temp_n_bit/5_bit_200_dist_32")
        random.shuffle(n_bit_data)

        ## Save:
        headline = "Rule"
        for I, R in Is_and_Rs:
            headline += "\tI=" + str(I) + ",R=" + str(R)

        headline += "\n"

        results = ""
        before_time = time.time()
        for rule in rules:
            print("Executing rule: " + str(rule))
            rule_results = []

            for I, R in Is_and_Rs:
                rcca_problem = rcca.RCCAProblem(n_bit_data)
                rcca_config = rcca.RCCAConfig()
                rcca_config.set_single_reservoir_config(ca_rule=rule, R=R, C=1, I=I, classifier="linear-svm",
                                                        encoding="random_mapping",
                                                        time_transition="normalized_addition")

                successful_runs = 0

                with Pool(8) as p:
                    results_from_runs = p.starmap(run_exec,
                                                  [(n_bit_data, rule,
                                                    rcca_problem, rcca_config) for _ in range(total_runs_per_config)])

                csv_name = "rule_" + str(rule) + "_I" + str(I) + "R" + str(R)
                path = os.getcwd()
                path = path + r"\..\data\experiments_data\rule_" + str(rule) + "\\"  # raw string

                # Rule directory
                try:
                    os.makedirs(path)
                except OSError as exception:
                    pass

                save_pickle = False
                # Pickles dir
                if save_pickle:
                    try:
                        os.makedirs(path + r"pickles\\")
                    except OSError as exception:
                        pass

                # Dump pickles ++
                i = 0
                for run in results_from_runs:
                    # save pickle
                    if save_pickle:
                        with open(path + "pickles\\run_" + str(i) + ".pkl", 'wb') as output:
                            pickle.dump(run.all_predictions, output, pickle.HIGHEST_PROTOCOL)
                    if run.was_successful():
                        successful_runs += 1
                    i += 1

                # csv
                with open(path + csv_name + ".csv", 'w+', newline='') as f:
                    writer = csv.writer(f, dialect='excel')
                    for run in results_from_runs:
                        writer.writerow([rule, run.total_correct])

                # print("successful: " + str(successful_runs) + " of " + str(len(results_from_runs)))
                percentage_success = (successful_runs / total_runs_per_config) * 100
                percentage_success = round(percentage_success, 1)  # 43.6
                rule_results.append(percentage_success)

            if results == "":
                one_rule = (time.time() - before_time)
                no_of_rules = len(rules)
                total_time_estimated = no_of_rules * one_rule
                print("Total estimated_time: " + str(int(total_time_estimated)) + " seconds")
                print("In minutes: " + str(total_time_estimated // 60))
                print("In hours: " + str(total_time_estimated // 3600))


            rule_result = str(rule)
            for result in rule_results:
                rule_result += "\t\t" + str(result)

            results += rule_result + "\n"

            with open(path + "rule_" + str(rule) + "_summary" + ".txt", 'w+') as f:
                temp_results = headline + rule_result
                f.write(temp_results)

        output = headline + results
        print(output)
        print("total time used in seconds:" + str(time.time() - before_time))

        with open(path + "..\\yilmaz_results_summary.txt", 'w+') as f:
            f.write(output)
    def run_yil_experiment_RNN_distractor(self):
        print("Running Yilmaz-experiments with diff distractr")
        rules = [n for n in range(256)]
        rules = [90, 110, 150]  # Yil rules

        Is_and_Rs = [
                        (32, 8), (32, 10), (32, 12), (32, 14),
                        (32, 16), (32, 18), (32, 20), (32, 22),
                        (32, 24), (32, 26), (32, 28), (32, 30),
                        (32, 35), (32, 40), (32, 45)

                     ]
        Is_and_Rs = [
            (4, 2), (4, 3), (4, 4), (4, 5),
            (4, 6), (4, 7), (4, 8), (4, 9),
            (4, 10),
            (8, 2), (8, 3), (8, 4), (8, 5),
            (8, 6), (8, 7), (8, 8), (8, 9),
            (8, 10)
        ]
        total_runs_per_config = 32

        distractor_periods = [25,50,100,200]
        for distractor_period in distractor_periods:
            print("-------")
            print("Started distractor period: " + str(distractor_period) + " at " + str(time.localtime().tm_hour) + ":" + str(time.localtime().tm_min))
            n_bit_data = self.open_temporal_data("temp_n_bit/5_bit_"+str(distractor_period)+"_dist_32")
            random.shuffle(n_bit_data)

            ## Save:
            headline = "Rule"
            for I, R in Is_and_Rs:
                headline += "\tI=" + str(I) + ",R=" + str(R)

            headline += "\n"

            results = ""
            before_time = time.time()
            for rule in rules:
                print("Executing rule: " + str(rule))
                rule_results = []

                for I, R in Is_and_Rs:
                    rcca_problem = rcca.RCCAProblem(n_bit_data)
                    rcca_config = rcca.RCCAConfig()
                    rcca_config.set_single_reservoir_config(ca_rule=90, R=4, C=10, I=4, classifier="linear-svm",
                                                        encoding="random_mapping",
                                                        time_transition="random_permutation")

                    successful_runs = 0

                    with Pool(8) as p:
                        results_from_runs = p.starmap(run_exec,
                                                      [(n_bit_data, rule,
                                                        rcca_problem, rcca_config) for _ in range(total_runs_per_config)])

                    csv_name = "rule_" + str(rule) + "_I" + str(I) + "R" + str(R)
                    path = os.getcwd()
                    path = path + r"\..\data\experiments_data\d_"+str(distractor_period)+"_rule_" + str(rule) + "\\"  # raw string

                    # Rule directory
                    try:
                        os.makedirs(path)
                    except OSError as exception:
                        pass

                    save_pickle = False
                    # Pickles dir
                    if save_pickle:
                        try:
                            os.makedirs(path + r"pickles\\")
                        except OSError as exception:
                            pass

                    # Dump pickles ++
                    i = 0
                    for run in results_from_runs:
                        # save pickle
                        if save_pickle:
                            with open(path + "pickles\\run_" + str(i) + ".pkl", 'wb') as output:
                                pickle.dump(run.all_predictions, output, pickle.HIGHEST_PROTOCOL)
                        if run.was_successful():
                            successful_runs += 1
                        i += 1

                    # csv
                    with open(path + csv_name + ".csv", 'w+', newline='') as f:
                        writer = csv.writer(f, dialect='excel')
                        for run in results_from_runs:
                            writer.writerow([rule, run.total_correct])

                    # print("successful: " + str(successful_runs) + " of " + str(len(results_from_runs)))
                    percentage_success = (successful_runs / total_runs_per_config) * 100
                    percentage_success = round(percentage_success, 1)  # 43.6
                    rule_results.append(percentage_success)

                if results == "":
                    one_rule = (time.time() - before_time)
                    no_of_rules = len(rules)
                    total_time_estimated = no_of_rules * one_rule*len(distractor_periods)
                    print("Total estimated_time: " + str(int(total_time_estimated)) + " seconds")
                    print("In minutes: " + str(total_time_estimated // 60))
                    print("In hours: " + str(total_time_estimated // 3600))


                rule_result = str(rule)
                for result in rule_results:
                    rule_result += "\t\t" + str(result)

                results += rule_result + "\n"

                with open(path + "rule_" + str(rule) + "_summary" + ".txt", 'w+') as f:
                    temp_results = headline + rule_result
                    f.write(temp_results)

            output = headline + results
            print(output)
            print("total time used in seconds:" + str(time.time() - before_time))

            with open(path + "..\\yilmaz_distractor_results_summary.txt", 'w+') as f:
                f.write(output)
    def n_bit_task(self, n=5):


        n_bit_data = self.open_temporal_data("temp_n_bit/5_bit_100_dist_32")
        rcca_problem = rcca.RCCAProblem(n_bit_data)
        rcca_config = rcca.RCCAConfig()
        rcca_config.set_single_reservoir_config(ca_rule=60, R=2, C=2, I=4, classifier="linear-svm",
                                                        encoding="random_mapping",
                                                        time_transition="random_permutation")
        #rcca_config.set_parallel_reservoir_config(ca_rules=[90,182], parallel_size_policy="bounded", R=64, C=1, I=16,
        #                              classifier="linear-svm", encoding="random_mapping",
        #                              time_transition="normalized_addition")

        rcca_system = rcca.RCCASystem()




        rcca_system.set_problem(rcca_problem)
        rcca_system.set_config(rcca_config)
        rcca_system.initialize_rc()
        rcca_system.fit_to_problem(22/32)

        #rcca_config.encoder.create_mappings(4)

        rcca_out = rcca_system.test_on_problem(22/32)
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
        print("Running mg-experiments")
        rules = [60, 90, 102, 105, 150, 153, 165, 180, 195]  # Bye rules
        all_rules = [comb for comb in itertools.combinations(rules, 2)]

        # rules = [182, 90]  # wuixcc
        Is_and_Rs = [(2, 4), (2, 8), (4, 4), (4, 8)]
        total_runs_per_config = (8 * 4)

        n_bit_data = self.open_temporal_data("temp_n_bit/5_bit_200_dist_32")
        random.shuffle(n_bit_data)

        ## Save:
        headline = "Rule"
        for I, R in Is_and_Rs:
            headline += "\tI=" + str(I) + ",R=" + str(R)
        headline += "\n"
        results = ""
        before_time = time.time()
        for rule_1, rule_2 in all_rules:
            rule_string = str(rule_1) + "_" +str(rule_2)
            print("Executing rule: " + rule_string)

            rule_results = []

            for I, R in Is_and_Rs:
                rcca_problem = rcca.RCCAProblem(n_bit_data)
                rcca_config = rcca.RCCAConfig()
                rcca_config.set_parallel_reservoir_config(ca_rules=[rule_1,rule_2], parallel_size_policy="bounded", R=R, C=10, I=I,
                                      classifier="linear-svm", encoding="random_mapping",
                                      time_transition="random_permutation")


                successful_runs = 0

                with Pool(8) as p:
                    results_from_runs = p.starmap(run_exec,
                                                  [("", "",
                                                    rcca_problem, rcca_config) for _ in range(total_runs_per_config)])

                csv_name = "rule_" + rule_string + "_I" + str(I) + "R" + str(R)
                path = os.getcwd()
                path = path + r"\..\data\experiments_data\rule_" + rule_string+ "\\"  # raw string

                # Rule directory
                try:
                    os.makedirs(path)
                except OSError as exception:
                    pass

                save_pickle = False
                # Pickles dir
                if save_pickle:
                    try:
                        os.makedirs(path + r"pickles\\")
                    except OSError as exception:
                        pass

                # Dump pickles ++
                i = 0
                for run in results_from_runs:
                    # save pickle
                    if save_pickle:
                        with open(path + "pickles\\run_" + str(i) + ".pkl", 'wb') as output:
                            pickle.dump(run.all_predictions, output, pickle.HIGHEST_PROTOCOL)
                    if run.was_successful():
                        successful_runs += 1
                    i += 1

                # csv
                with open(path + csv_name + ".csv", 'w+', newline='') as f:
                    writer = csv.writer(f, dialect='excel')
                    for run in results_from_runs:
                        writer.writerow([rule_string, run.total_correct, len(run.all_test_examples)])

                # print("successful: " + str(successful_runs) + " of " + str(len(results_from_runs)))
                percentage_success = (successful_runs / total_runs_per_config) * 100
                percentage_success = round(percentage_success, 1)  # 43.6
                rule_results.append(percentage_success)

            if results == "":
                one_rule = (time.time() - before_time)
                no_of_rules = len(rules)
                total_time_estimated = no_of_rules * one_rule
                print("Total estimated_time: " + str(int(total_time_estimated)) + " seconds")
                print("In minutes: " + str(total_time_estimated // 60))
                print("In hours: " + str(total_time_estimated // 3600))

            rule_result = rule_string
            for result in rule_results:
                rule_result += "\t\t" + str(result)

            results += rule_result + "\n"

            with open(path + "rule_" + rule_string + "_summary" + ".txt", 'w+') as f:
                temp_results = headline + rule_result
                f.write(temp_results)

        output = headline + results
        print(output)
        print("total time used in seconds:" + str(time.time() - before_time))

        with open(path + "..\\mg_results_summary.txt", 'w+') as f:
            f.write(output)

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






