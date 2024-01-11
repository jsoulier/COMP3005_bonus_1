import operator

class TableElement:
    """ An wrapper for all the supported types in a table.
    The possible types include:
        - strings
        - integers
        - floats
    The wrapper allows for the automatic comparison of string, integral, and floating types,
    even when the other operand is a string.
    """

    def __init__(self, string):
        self.value = self.convert(string)

    @staticmethod
    def convert(string):
        """ Try to convert the string to any of the supported types in a table. """
        try:
            return int(string)
        except:
            pass
        try:
            return float(string)
        except:
            pass
        return string
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)

    def compare(self, other, comparator):
        return comparator(self.value, self.convert(other))
    
    def __lt__(self, other):
        return self.compare(other, operator.lt)
    
    def __le__(self, other):
        return self.compare(other, operator.le)
    
    def __eq__(self, other):
        return self.compare(other, operator.eq)
    
    def __ne__(self, other):
        return self.compare(other, operator.ne)
    
    def __ge__(self, other):
        return self.compare(other, operator.ge)
    
    def __gt__(self, other):
        return self.compare(other, operator.gt)
