__author__ = 'magnus'
import pprint

class ElemCAReservoir:
    def __init__(self):
        self.rules = []


    def set_rule(self, rule_number):
        self.rules = Rule(rule_number)

    def set_rules(self, rule_list):
        self.parallel_reservoirs=True
        for rule in rule_list:
            self.rules.append(Rule(rule))

    def set_rule_dict(self, rule_dict):
        """

        :param intervals:
        :return:
        """


        self.rule_dict = rule_dict



    def run_simulation_step(self, prev_generation, rules):
        length = len(prev_generation)
        next_generation = []
        #Wrap around
        for i in range(length):
            left_index = (i-1) % length
            mid_index = i
            right_index = (i+1) % length
            for start_index, end_index in rules.keys():
                if start_index <= i <= end_index:  # Get the rule at the current interval
                    rule = rules[(start_index, end_index)]
                    next_generation.append(rule.getOutput([prev_generation[left_index],
                                                  prev_generation[mid_index], prev_generation[right_index]]))
        return next_generation


    def run_simulation(self, initial_inputs, iterations, rule_dict):
        """
        Runs a simulation of the initial input, for a given iterations

        Returns the whole list of generations
        :param initial_inputs:
        :param iterations:
        :return:
        """
        all_generations = [initial_inputs]
        current_generation = all_generations[0]
        #rule_dict = {(0, len(initial_inputs)//2-1):self.current_rule,
        #             (len(initial_inputs)//2, len(initial_inputs)): Rule(90)}

        for i in range(iterations):
            # TODO: Parlallizaation scheme

            current_generation = self.run_simulation_step(current_generation, rule_dict)
            all_generations.append(current_generation)
        return all_generations

class CAGeneration:
    # TODO:
    def __init__(self):
        pass

class CACell:
    def __init__(self):
        pass

class Rule:
    def __init__(self, number=0):
        """

        :param number: Corresponds to Wolfram number of elem. CA rules
        :return:
        """
        self.number = number

    def getRuleScheme(self, rule_number):
        """
        :param rule_number:
        :return:
        """
        binrule = format(rule_number, "08b")  # convert to binary, with fill of zeros until the string is of length 8

        rule = {
            (1,1,1): int(binrule[0]),
            (1,1,0): int(binrule[1]),
            (1,0,1): int(binrule[2]),
            (1,0,0): int(binrule[3]),
            (0,1,1): int(binrule[4]),
            (0,1,0): int(binrule[5]),
            (0,0,1): int(binrule[6]),
            (0,0,0): int(binrule[7])
        }

        return rule

    def getOutput(self, input_array):
        if len(input_array) != 3:
            raise ValueError

        scheme = self.getRuleScheme(self.number)
        output = scheme[(input_array[0], input_array[1], input_array[2])]

        return output


