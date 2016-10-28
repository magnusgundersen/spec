from reservoircomputing import rc_interface as rcif
import random


class RandomMappingEncoder(rcif.RCEncoder):
    def __init__(self):
        super().__init__()
        self.R = 1
        self.encoding_scheme = "separate"

    def encode_input(self, _input):
        """
        Encodes the input with randomization of the input R times

        The encoding scheme tells the encoder if the input and permutations is to be

        :param _input:
        :return:
        """
        #new_input = _input[:]
        input_vectors = []
        new_input = []

        for i in range(self.R):
            r_list = _input[:]
            #if i>0:#%2 == 1:
            #    r_list = [0,0,0,0,0,0,0,0]
            random.shuffle(r_list)
            if self.encoding_scheme == "separate":
                input_vectors.append([r_list])
            elif self.encoding_scheme =="concat":
                new_input.extend(r_list)  # Flatten

        if self.encoding_scheme =="concat":
            input_vectors = [[new_input]]



        return input_vectors

    def encode_output(self, _output):
        # Flatten
        _output = [ca_val for sublist in _output for ca_val in sublist]
        return _output
