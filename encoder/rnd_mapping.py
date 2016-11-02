from reservoircomputing import rc_interface as rcif
import random


class RandomMappingEncoder(rcif.RCEncoder):
    def __init__(self):
        super().__init__()
        self.R = 1
        self.encoding_scheme = "separate"

    def create_mappings(self, input_length):
        """
        Facilitates having a fixed mapping
        :param input_length:
        :return:
        """
        print("Creating mappings!")
        list_of_mappings = []
        self.input_length = input_length
        num_list = [x for x in range(input_length)]
        num_list2 = num_list[:]

        for _ in range(self.R):
            random.shuffle(num_list2)
            list_of_mappings.append(num_list2[:])
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
            temp_enc_list = [0 for _ in range(len(_input))]
            for j in range(len(_input)):
                temp_enc_list[j] = _input[self.mappings[i][j]]

            encoded_input.append(temp_enc_list)

        return encoded_input


    def encode_output(self, _output):
        # Flatten
        _output = [ca_val for sublist in _output for ca_val in sublist]
        return _output

