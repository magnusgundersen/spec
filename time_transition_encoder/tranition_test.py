from encoder import rnd_mapping
from time_transition_encoder import random_permutation

def test():
    enc = rnd_mapping.RandomMappingEncoder()
    enc.R = 2
    enc.C = 2
    enc.create_mappings(4)

    _input = [0,0,0,1]
    encoded_input = enc.encode_input(_input)
    decoded_input = enc.encode_output(encoded_input)
    print(decoded_input)

    translated_input = [0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0]

    trans = random_permutation.RandomPermutationTransition()

    new_input = trans.join(decoded_input,translated_input, enc)

test()
