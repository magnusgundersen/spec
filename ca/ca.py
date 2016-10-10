__author__ = 'magnus'
import pprint

class CA:
    def __init__(self):
        pass

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



    def run_simulation(self, number_of_generations, rule_number):
        rule = Rule(rule_number)
        all_generations = []
        initial_generation = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        all_generations.append(initial_generation)
        current_generation = initial_generation
        for i in range(number_of_generations):
            current_generation = self.run_simulation_step(current_generation, rule)
            all_generations.append(current_generation)
        for gen in all_generations:
            genstring = ""
            for ind in gen:
                if ind == 1:
                    genstring += "X"
                else:
                    genstring += " "
            print(genstring)

        #pprint.pprint(all_generations)





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
        rule_110 = {
            (1,1,1):0,
            (1,1,0):1,
            (1,0,1):1,
            (1,0,0):1,
            (0,1,1):1,
            (0,1,0):1,
            (0,0,1):0,
            (0,0,0):0
        }
        if rule_number == 110:
            return rule_110

    def getOutput(self, input_array):
        output = 0
        if len(input_array) != 3:
            raise ValueError
        if self.number == 110:
            print("Number:" + str(self.number))
            scheme = self.getRuleScheme(110)
            output = scheme[(input_array[0], input_array[1], input_array[2])]

        return output


