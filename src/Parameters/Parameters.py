from .ParameterBag import ParameterBag
from .ValuesBag import ValuesBag

class Parameters:

    def __init__(self, parameters):
        # Current Parameter
        self.parameters = ParameterBag(parameters)
        self.values     = ValuesBag()
        self.names      = self.parameters.keys()
        self.current    = 0

    def number_of_combinations(self):
        num = 1
        for name in self.names:
            num *= self.parameters.number_of_values(name)
        return num

    def is_next_parameter_available(self):
        ''' Try to calculate next value to see if it is possible and respond accordingly. '''
        if self.current >= len(self.names):
            return False
        if self.values.is_empty():
            self.values.update_values(self.parameters.get_first_values_dict())
            return True
        return self._update_values() != None

    def get_next_values(self):
        return self.values

    def _update_values(self):
        idx = 0
        while idx <= self.current:
            name = self.names[idx]
            if self.parameters.has_value(name):
                next_value = self.parameters.get_next_value(name)
                self.values.update_value_of(name, next_value)
                break
            self.parameters.reset(name)
            self.values.update_value_of(name, self.parameters.get_initial_value_of(name))

            # if current param, then update it next cycle
            if idx == self.current:
                self.current += 1
                if not self.current < len(self.names):
                    return None

            idx += 1
            continue
        return True

    def reset_all(self):
        self.current = 0
        self.values = ValuesBag()
        self.parameters.reset_all()

    def __str__(self):
        return self.parameters.__str__()