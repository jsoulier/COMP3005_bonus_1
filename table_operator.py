import enum

class TableOperator(enum.Enum):
    """ The table operators and their textual representations. """

    NONE               = (0,  0, [])
    SELECTION          = (1,  1, ['\u03C3', 'select'])
    PROJECTION         = (2,  1, ['\u03C0', 'pi'])
    CROSS_JOIN         = (3,  2, ['\u00D7'])
    NATURAL_JOIN       = (4,  2, ['\u2A1D'])
    LEFT_OUTER_JOIN    = (5,  2, ['\u27D5'])
    RIGHT_OUTER_JOIN   = (6,  2, ['\u27D6'])
    FULL_OUTER_JOIN    = (7,  2, ['\u27D7'])
    UNION              = (8,  2, ['\u222A'])
    INTERSECTION       = (9,  2, ['\u2229'])
    MINUS              = (10, 2, ['\u2212'])
    DIVISION           = (11, 2, ['\u00F7'])

    def __init__(self, id, operands, strings):
        """ Create a new TableOperator. """
        self.id = id
        self.operands = operands
        self.strings = strings

    def __eq__(self, other):
        """ Compare by identifier. """
        return self.id == other.id
