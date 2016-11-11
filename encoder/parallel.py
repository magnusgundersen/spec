class ParallelNonUniformEncoder:  # Consider renaming/rebranding to a "rule-governer"
    def __init__(self, ca_rules, parallel_size_policy="unbounded"):
        self.P = len(ca_rules)
        self.ca_rules = ca_rules
        self.parallel_size_policy = parallel_size_policy
        self.rule_dict = {}



    def encode(self, _input):
        new_input = []
        rule_dict = {}

        if self.parallel_size_policy == "unbounded":
            size = len(_input)/self.P
            new_input = _input
            for i in range(self.P):
                rule_dict[i*size, (i+1)*(size-1)] = self.ca_rules[i]


        elif self.parallel_size_policy == "bounded":
            new_input = _input
            size = len(_input)
            pieces = size // self.P  # devide in even parts
            for i in range(self.P):
                rule_dict[(i*pieces, ((i+1)*pieces)-1)] = self.ca_rules[i]
                # TODO: MAJOR PROBLEM if its an odd number of cells


        return new_input, rule_dict



