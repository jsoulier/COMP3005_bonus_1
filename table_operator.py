import enum

class TableOperator(enum.Enum):
    ''' The table operators and their textual representations. '''

    NONE             = (0,  0, '')
    SELECTION1       = (1,  1, '\u03C3')
    SELECTION2       = (1,  1, 'select')
    PROJECTION1      = (2,  1, '\u03C0')
    PROJECTION2      = (2,  1, 'pi')
    CROSS_JOIN       = (3,  2, '\u00D7')
    NATURAL_JOIN     = (4,  2, '\u2A1D')
    LEFT_OUTER_JOIN  = (5,  2, '\u27D5')
    RIGHT_OUTER_JOIN = (6,  2, '\u27D6')
    FULL_OUTER_JOIN  = (7,  2, '\u27D7')
    UNION            = (8,  2, '\u222A')
    INTERSECTION     = (9,  2, '\u2229')
    MINUS            = (10, 2, '\u2212')
    DIVISION1        = (11, 2, '\u00F7')
    DIVISION2        = (11, 2, '/')

    SELECTION        = SELECTION1
    PROJECTION       = PROJECTION1
    DIVISION         = DIVISION1

    def __init__(self, id, operands, string):
        ''''''
        self.id = id
        self.operands = operands
        self.string = string

    def __eq__(self, other):
        ''' Compare with other or check if strings contain other. '''
        if isinstance(other, TableOperator):
            return self.id == other.id
        if isinstance(other, str):
            return other in self.string
        raise AssertionError()

    def __bool__(self):
        ''''''
        return self != TableOperator.NONE

    def __str__(self):
        ''''''
        return self.string
    
    def __len__(self):
        ''''''
        return len(self.string)

    def left_outer_join(self):
        ''''''
        array = [TableOperator.LEFT_OUTER_JOIN, TableOperator.FULL_OUTER_JOIN]
        return self in array

    def right_outer_join(self):
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
