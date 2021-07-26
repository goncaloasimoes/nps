class ValuesBag:

    def __init__(self, values = {}):
        self.values       = values
        self.last_printed = {}

    def is_empty(self):
        return len(self.values) == 0

    def update_values(self, new_values):
        self.values = new_values

    def update_value_of(self, name, value):
        self.values[name] = value

    def get_values(self):
        return self.values
    
    def get_value(self, name):
        return self.values[name]

    def print(self):
        print(str(self))
    
    def __str__(self):
        output = ''
        diff = {k: self.values[k] for k in self.values if k not in self.last_printed or self.values[k] != self.last_printed[k]}
        for name in self.values:
            if name in diff:
                output += "\033[4m\033[93m%s\033[0m: %.2f, " % (name, self.values[name])
                continue
            output += "\033[92m%s\033[0m: %.2f, " % (name, self.values[name])
        self.last_printed = self.values.copy()
        return output