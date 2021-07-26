class ParameterBag:

    def __init__(self, parameters = {}):
        self.parameters = parameters

    def __contains__(self, name):
        return name in self.parameters
    
    def keys(self):
        return list(self.parameters.keys())
    
    def size(self):
        return len(self.parameters)
    
    def has_value(self, name):
        return self.parameters[name].has_value()
    
    def get_next_value(self, name):
        return self.parameters[name].get_next_value()

    def reset(self, name):
        return self.parameters[name].reset()
    
    def reset_all(self):
        for name in self.parameters.keys():
            self.parameters[name].reset()

    def get_initial_value_of(self, name):
        return self.parameters[name].get_initial_value()
    
    def get_end_value_of(self, name):
        return self.parameters[name].get_end_value()
    
    def get_first_values_dict(self):
        values = {}
        for name in self.parameters.keys():
            values[name] = self.parameters[name].get_initial_value()
        return values
    
    def number_of_values(self,name):
        return self.parameters[name].number_of_values()

    def __str__(self):
        output = ''
        for name, param in self.parameters.items():
            # TODO: make this better
            if len(name) > 6:
                output += "%s \t%s" % ( name, param.__str__() )
            else:
                output += "%s \t\t%s" % ( name, param.__str__() )
        return output