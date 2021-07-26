class ListParameter:

    def __init__(self, name, values):
        self.name    = name
        if not isinstance(values, list):
            raise Exception('Values received in ListParameter for %s are not a list.' % name)
        self.values  = values
        self.current = 0

    def get_name(self):
        return self.name

    def get_initial_value(self):
        return self.values[0]

    def get_end_value(self):
        return self.values[-1]

    def has_value(self):
        return self.current + 1 < len(self.values)

    def get_next_value(self):
        self.current += 1
        value = self.values[self.current]
        return value

    def reset(self):
        self.current = 0

    def number_of_values(self):
        return len(self.values)

    def __str__(self):
        return str(self.values) + '\n'