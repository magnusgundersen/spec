from reservoircomputing import rc_interface as rcif
import random


class RandomMappingEncoder(rcif.RCEncoder):
    def __init__(self):
        super().__init__()
        self.R = 1
        self.encoding_scheme = "separate"

    def create_mappings(self, input_length):
        list_of_mappings = []
        self.input_length = input_length
        num_list = [x for x in range(input_length)]
        num_list2 = num_list[:]

        for _ in range(self.R):
            random.shuffle(num_list2)
            list_of_mappings.append(num_list2)
        self.mappings = list_of_mappings


    def encode_input(self, _input):
        """

        :param _input:
        :return:
        """

        encoded_input = []
        if len(_input) != self.input_length:
            raise ValueError("Wrong input-length to encoder!")

        for i in range(self.R):
            temp_enc_list = ([0]*len(_input))[:] # Copy!
            for j in range(len(_input)):
                temp_enc_list[j] = _input[self.mappings[i][j]]

            encoded_input.append(temp_enc_list)

        return encoded_input






    def encode_input_old(self, _input):
        """
        Encodes the input with randomization of the input R times

        The encoding scheme tells the encoder if the input and permutations is to be

        Returns:

        [
        [0,1,1,1],
        [0,0,0,0],
        ...
        ]

        :param _input:
        :return:
        """
        #new_input = _input[:]
        input_vectors = []
        new_input = []

        for i in range(self.R):
            r_list = _input[:]
            random.shuffle(r_list)
            if self.encoding_scheme == "separate":
                input_vectors.append(r_list)
            elif self.encoding_scheme =="concat":
                new_input.extend(r_list)  # Flatten

        if self.encoding_scheme =="concat":
            input_vectors = [[new_input]]



        return input_vectors

    def encode_input_with_translator(self, _input, translator):
        # new_input = _input[:]
        input_vectors = []
        new_input = []

        # NB_ only separate reservoirs now possible!

        for i in range(self.R):
            _input = None
            r_list = _input[:]
            random.shuffle(r_list)
            if self.encoding_scheme == "separate":
                input_vectors.append(r_list)
            elif self.encoding_scheme == "concat":
                new_input.extend(r_list)  # Flatten

        if self.encoding_scheme == "concat":
            input_vectors = [[new_input]]

        return input_vectors


    def encode_output(self, _output):
        # Flatten
        _output = [ca_val for sublist in _output for ca_val in sublist]
        return _output
