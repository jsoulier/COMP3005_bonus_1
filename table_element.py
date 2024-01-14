import operator

class TableElement:
    '''
    A wrapper for all the supported types in a table.
    The possible types include:
        - strings
        - integers
        - floats
    The wrapper allows for the automatic comparison of string, integral, and floating
    types, even when the other operand is a string.
    '''

    def __init__(self, string):
        ''''''
        self.value = self.convert(string)

    @staticmethod
    def convert(string):
        ''' Try to convert the string to any of the supported types. '''
        if not isinstance(string, float):
            try:
                return int(string)
            except:
                pass
        try:
            return float(string)
        except:
            pass
        return string
    
    def __bool__(self):
        ''''''
        return bool(self.value)

    def __str__(self):
        ''''''
        return str(self.value)
    
    def __repr__(self):
        ''''''
        return str(self.value)

    def compare(self, comparator, other):
        ''' Compare with any of the supported types using the selected operator. '''
        return comparator(self.value, self.convert(other))

    def __lt__(self, other):
        ''''''
        return self.compare(operator.lt, other)
    
    def __le__(self, other):
        ''''''
        return self.compare(operator.le, other)
    
    def __eq__(self, other):
        ''''''
        return self.compare(operator.eq, other)
    
    def __ne__(self, other):
        ''''''
        return self.compare(operator.ne, other)
    
    def __ge__(self, other):
        ''''''
        return self.compare(operator.ge, other)
    
    def __gt__(self, other):
        ''''''
        return self.compare(operator.gt, other)
