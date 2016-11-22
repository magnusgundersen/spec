import random
import itertools

def generate_n_bit_file(n, distractor_period, number_of_training_sets):

    content = ""

    a1_values = []
    for prod in itertools.product((0,1), repeat=n):
        a1_values.append(prod)
    max_size = len(a1_values)

    if max_size<number_of_training_sets:
        print("Too many training-sets requested!" + str(max_size) + " is max")
        number_of_training_sets = max_size

    for i in range(number_of_training_sets):
        training_set = ""
        a1_value = a1_values[i]
        signal = []

        # n bit signal
        for j in range(n):
            _input, _corresponding_output = get_input_by_a1_value(a1_value[j])
            _output = "001"
            training_set += _input + " " + _output + "\n"
            signal.append(_corresponding_output)

        # Distractor period
        for j in range(distractor_period-1):
            _input = "0010"
            _output = "001"
            training_set += _input + " " + _output + "\n"

        # Cue signal
        _input = "0001"
        _output = "001"
        training_set += _input + " " + _output + "\n"

        # repeated n bit signal
        for signal_entry in signal:
            _input = "0010"
            _output = signal_entry
            training_set += _input + " " + _output + "\n"


        content += training_set + "\n"

    with open(str(n)+ "_bit_" + str(distractor_period) + "_dist_" + str(number_of_training_sets),'w+') as f:
        f.write(content)

def get_input_by_a1_value(a1_value):
    if a1_value == 1:
        return "1000", "100"
    else:
        return "0100", "010"
generate_n_bit_file(5, 200, 32)


