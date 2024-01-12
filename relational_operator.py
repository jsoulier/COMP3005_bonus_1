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

    def __init__(self, string, comparator):
        ''' Create a new RelationalOperator. '''
        self.string = string
        self.comparator = comparator

    def within(self, other):
        ''' Check if string is contained in other. '''
        return self.string and self.string in other
    
    def __bool__(self):
        ''' Check if valid. '''
        return self != RelationalOperator.NONE
