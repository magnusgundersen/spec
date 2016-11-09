class RandomPermutationTransition:
    def __init__(self):
        pass

    def join(self, _input, _transition_input, encoder):

        size = len(_transition_input)


        mappings = encoder.mappings
        R = encoder.R

        adjusted_mappings = []
        for i in range(len(mappings)):
            new_mapping = []
            for integer in mappings[i]:
                new_mapping.append(integer+(i*8)) # 8 ni
            adjusted_mappings.extend(new_mapping)

        new_input = ["x" for _ in range(size)]
        for index in adjusted_mappings:
            new_input[index] = _input[index]
        for i in range(len(new_input)):
            if new_input[i] == "x":
                new_input[i] = _transition_input[i]

        return new_input












