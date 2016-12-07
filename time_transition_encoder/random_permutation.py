class RandomPermutationTransition:
    def __init__(self):
        pass


    def sep_join(self, _input, _transition_input, encoder):
        # ONLY DIFF FROM BELOW IS THAT THIS VERSION TAKES IN A LIST OF LISTS
        joined = []
        for i in range(len(_input)):
            joined.append(self.join(_input[i], _transition_input[i], encoder))
        return joined

    def join(self, _input, _transition_input, encoder, selected_interval =(0,0)):

        size = len(_transition_input)

        if selected_interval == ():
            mappings = encoder.mappings
        else:
            mappings = encoder.mappings[0:1]
        print(mappings)
        R = encoder.R
        P = encoder.P

        adjusted_mappings = []
        for i in range(len(mappings)):
            new_mapping = []
            for integer in mappings[i]:
                new_mapping.append(integer+(i*(size//R))) # 8 ni
            adjusted_mappings.extend(new_mapping)

        new_input = ["x" for _ in range(size)]

        for index in adjusted_mappings:
            new_input[index] = _input[index]
        for i in range(len(new_input)):
            if new_input[i] == "x":
                new_input[i] = _transition_input[i]

        return new_input












