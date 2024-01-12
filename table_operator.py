import enum

class TableOperator(enum.Enum):
    ''' The table operators and their textual representations. '''

    NONE               = (0,  [])
    SELECTION          = (1,  ['\u03C3', 'select'])
    PROJECTION         = (2,  ['\u03C0', 'pi'])
    CROSS_JOIN         = (3,  ['\u00D7'])
    NATURAL_JOIN       = (4,  ['\u2A1D'])
    LEFT_OUTER_JOIN    = (5,  ['\u27D5'])
    RIGHT_OUTER_JOIN   = (6,  ['\u27D6'])
    FULL_OUTER_JOIN    = (7,  ['\u27D7'])
    UNION              = (8,  ['\u222A'])
    INTERSECTION       = (9,  ['\u2229'])
    MINUS              = (10, ['\u2212'])
    DIVISION           = (11, ['\u00F7'])

    def __init__(self, id, strings):
        ''' Create a new TableOperator. '''
        self.id = id
        self.strings = strings

    def __eq__(self, other):
        ''' Compare by identifier. '''
        return self.id == other.id
