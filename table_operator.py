import enum

class TableOperator(enum.Enum):
    ''' The table operators and their textual representations. '''

    NONE             = ([])
    SELECTION        = (['\u03C3', 'select'])
    PROJECTION       = (['\u03C0', 'pi'])
    CROSS_JOIN       = (['\u00D7'])
    NATURAL_JOIN     = (['\u2A1D'])
    LEFT_OUTER_JOIN  = (['\u27D5'])
    RIGHT_OUTER_JOIN = (['\u27D6'])
    FULL_OUTER_JOIN  = (['\u27D7'])
    UNION            = (['\u222A'])
    INTERSECTION     = (['\u2229'])
    MINUS            = (['\u2212'])
    DIVISION         = (['\u00F7'])

    def __init__(self, strings):
        ''' Create a new TableOperator. '''
        self.strings = strings

    def __eq__(self, other):
        ''' Compare by identifier or strings. '''
        if isinstance(other, TableOperator):
            return self.value == other.value
        if isinstance(other, str):
            return other in self.strings
        raise AssertionError()
    
    def __bool__(self):
        ''' Check if valid. '''
        return self != TableOperator.NONE
