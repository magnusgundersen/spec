from encoder import rnd_mapping
from time_transition_encoder import random_permutation

def test():
    enc = rnd_mapping.RandomMappingEncoder()
    enc.R = 1
    enc.C = 2
    enc.create_mappings(4)

    _input = [0,0,0,0]
    encoded_input = enc.encode_input(_input)
    decoded_input = enc.encode_output(encoded_input)
    print(decoded_input)

    translated_input = [1, 1, 1, 1, 1, 1, 1, 1]# 1, 1, 1, 1, 1, 1, 1, 1]

    trans = random_permutation.RandomPermutationTransition()

    new_input = trans.join(decoded_input,translated_input, enc)
    print(new_input)

test()
