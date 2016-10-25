from reservoircomputing import rc_interface as rcif
import random


class RandomMappingEncoder(rcif.RCEncoder):
    def __init__(self):
        super().__init__()
        self.R = 1

    def encode(self, _input):
        """
        Encodes the input with randomization of the input R times
        :param _input:
        :return:
        """
        new_input = _input[:]
        for _ in range(self.R):
            r_list = _input[:]
            random.shuffle(r_list)
            new_input.extend(r_list)  # Flatten

        return new_input
