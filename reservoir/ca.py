__author__ = 'magnus'
import pprint

class ElemCAReservoir:
    def __init__(self):
        self.current_rule = None

    def set_rule(self, rule_number):
        self.current_rule = Rule(rule_number)

    def run_simulation_step(self, prev_generation, rule):
        length = len(prev_generation)
        next_generation = []

        #Wrap around
        for i in range(length):
            left_index = (i-1) % length
            mid_index = i
            right_index = (i+1) % length
            next_generation.append(rule.getOutput([prev_generation[left_index],
                                                  prev_generation[mid_index], prev_generation[right_index]]))
        return next_generation



    def run_simulation(self, initial_inputs, number_of_generations):
        all_generations = []
        number_of_input_vectors = len(initial_inputs)
        all_generations.append(initial_inputs.pop(0))
        current_generation = all_generations[0]
        for i in range(number_of_generations):
            current_generation = self.run_simulation_step(current_generation, self.current_rule)
            all_generations.append(current_generation)
        return all_generations[1:]


    def show_console_printout(self, all_generations):
        for gen in all_generations:
            genstring = ""
            for ind in gen:
                if ind == 1:
                    genstring += "X"
                else:
                    genstring += " "
            print(genstring)




class CAGeneration:
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
        binrule = bin(rule_number)
        binrule = format(rule_number,"08b")

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
        output = 0
        if len(input_array) != 3:
            raise ValueError

        scheme = self.getRuleScheme(self.number)
        output = scheme[(input_array[0], input_array[1], input_array[2])]

        return output


