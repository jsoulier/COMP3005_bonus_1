import enum
import operator

class RelationalOperator(enum.Enum):
    ''' The relational operators and their comparators. '''

    NONE           = ('',   None)
    EQUAL1         = ('==', operator.eq)
    NOT_EQUAL      = ('!=', operator.ne)
    LESS_EQUAL1    = ('<=', operator.le)
    LESS_EQUAL2    = ('=<', operator.le)
    GREATER_EQUAL1 = ('>=', operator.ge)
    GREATER_EQUAL2 = ('=>', operator.ge)

    # Don't change the order. These need to be tried last
    EQUAL2         = ('=',  operator.eq)
    LESS           = ('<',  operator.lt)
    GREATER        = ('>',  operator.gt)

    # Aliases
    LESS_EQUAL     = LESS_EQUAL1
    GREATER_EQUAL  = GREATER_EQUAL1
    EQUAL          = EQUAL1

    def __init__(self, string, comparator):
        ''''''
        self.string = string
        self.comparator = comparator

    def within(self, other):
        ''''''
        return self.string and self.string in other

    def __str__(self):
        ''''''
        return self.string

    def __repr__(self):
        ''''''
        return self.string

    def __call__(self, a, b):
        ''''''
        return self.comparator(a, b)

    def __bool__(self):
        ''''''
        return self != RelationalOperator.NONE
