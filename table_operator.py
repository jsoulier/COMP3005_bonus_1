import enum

class TableOperator(enum.Enum):
    ''' The table operators and their textual representations. '''

    NONE             = (0, [])
    SELECTION        = (1, ['\u03C3', 'select'])
    PROJECTION       = (1, ['\u03C0', 'pi'])
    CROSS_JOIN       = (2, ['\u00D7'])
    NATURAL_JOIN     = (2, ['\u2A1D'])
    LEFT_OUTER_JOIN  = (2, ['\u27D5'])
    RIGHT_OUTER_JOIN = (2, ['\u27D6'])
    FULL_OUTER_JOIN  = (2, ['\u27D7'])
    UNION            = (2, ['\u222A'])
    INTERSECTION     = (2, ['\u2229'])
    MINUS            = (2, ['\u2212'])
    DIVISION         = (2, ['\u00F7', '/'])

    def __init__(self, nodes, strings):
        ''''''
        self.nodes = nodes
        self.strings = strings

    def __eq__(self, other):
        ''' Compare with other or check if strings contain other. '''
        if isinstance(other, TableOperator):
            return self.value == other.value
        if isinstance(other, str):
            return other in self.strings
        raise AssertionError()

    def __bool__(self):
        ''''''
        return self != TableOperator.NONE

    def __str__(self):
        ''''''
        if not self.strings:
            return ''
        return self.strings[0]

    def left(self):
        ''''''
        array = [TableOperator.LEFT_OUTER_JOIN, TableOperator.FULL_OUTER_JOIN]
        return self in array

    def right(self):
        ''''''
        array = [TableOperator.RIGHT_OUTER_JOIN, TableOperator.FULL_OUTER_JOIN]
        return self in array

    def parametrize(self, count):
        ''' Check if count is a valid number of parameters. '''
        if self == TableOperator.NONE:
            return count == 0
        if self == TableOperator.SELECTION:
            return count == 2
        if self == TableOperator.PROJECTION:
            return count >= 1
        if self == TableOperator.CROSS_JOIN:
            return count == 0
        if self == TableOperator.NATURAL_JOIN:
            return count == 0 or count == 2
        if self == TableOperator.LEFT_OUTER_JOIN:
            return count == 0 or count == 2
        if self == TableOperator.RIGHT_OUTER_JOIN:
            return count == 0 or count == 2
        if self == TableOperator.FULL_OUTER_JOIN:
            return count == 0 or count == 2
        if self == TableOperator.UNION:
            return count == 0
        if self == TableOperator.INTERSECTION:
            return count == 0
        if self == TableOperator.MINUS:
            return count == 0
        if self == TableOperator.DIVISION:
            return count == 0
        raise AssertionError()
