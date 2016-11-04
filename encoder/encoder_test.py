from encoder import rnd_mapping
def test_random_mapping():
    enc = rnd_mapping.RandomMappingEncoder()
    enc.R=2
    enc.C=2
    enc.create_mappings(4)
    _input = [0,0,0,1]
    print("encoding: " + str(_input))

    print("Mpped input:" + str(enc.encode_input(_input)))
    print("Mpped input:" + str(enc.encode_input(_input)))
    print("Mpped input:" + str(enc.encode_input(_input)))


test_random_mapping()