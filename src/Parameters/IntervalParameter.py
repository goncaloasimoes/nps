class IntervalParameter:

    def __init__(self, name, initial_value, end_value, step):
        self.name          = name
        self.initial_value = initial_value
        self.current_value = initial_value
        self.end_value     = end_value
        self.step          = step

    def get_name(self):
        return self.name

    def get_initial_value(self):
        return self.initial_value

    def get_end_value(self):
        return self.end_value

    def has_value(self):
        return round( self.current_value + self.step, 4) <= self.end_value

    def get_next_value(self):
        self.current_value = round( self.current_value + self.step, 4)
        return self.current_value

    def reset(self):
        self.current_value = self.initial_value
    
    def number_of_values(self):
        return int(abs(self.end_value - self.current_value)/self.step) + 1

    def __str__(self):
        if self.initial_value == self.end_value:
            return '%.2f\n' % self.initial_value
        return '%.2f to %.2f, step %.2f\n' % ( self.initial_value, self.end_value, self.step )
