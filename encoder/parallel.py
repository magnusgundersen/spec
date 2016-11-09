class ParallelNonUniformEncoder:
    def __init__(self, ca_rules, parallel_size_policy="unbounded"):
        self.P = len(ca_rules)
        self.ca_rules = ca_rules
        self.parallel_size_policy = parallel_size_policy

    def encode(self, _input):
        if self.parallel_size_policy == "unbounded":

