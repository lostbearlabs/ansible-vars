
class VariableDefault(object):

    def __init__(self, variable_name, default_value, path):
        self.variable_name = variable_name
        self.default_value = default_value
        self.path = path

    def get_variable_name(self):
        return self.variable_name

    def get_default_value(self):
        return self.default_value

    def get_path(self):
        return self.path

    def __hash__(self):
        return hash((self.variable_name, self.default_value, self.path))

    def __eq__(self, other):
        return (self.variable_name, self.default_value, self.path) == (other.variable_name, self.default_value, other.path)

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return "%s => %s [%s]" % (self.variable_name, self.default_value, self.path)