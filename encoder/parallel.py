class ParallelNonUniformEncoder:
    def __init__(self, ca_rules, parallel_size_policy="unbounded"):
        self.P = len(ca_rules)
        self.ca_rules = ca_rules
        self.parallel_size_policy = parallel_size_policy


    def encode(self, _input):
        new_input = []
        if self.parallel_size_policy == "unbounded":
            size = len(_input)
            for i in range(self.P):
                new_input += _input

        elif self.parallel_size_policy == "bounded":
            size = len(_input)
            pieces = size // self.P

        rule_dict = {

        }
        return new_input, rule_dict



