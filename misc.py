
class Misc:
    """ Miscellaneous constants and conversions. """

    SELECTION          = ['\u03C3', 'select']
    PROJECTION         = ['\u03C0']
    CROSS_JOIN         = ['\u00D7']
    NATURAL_JOIN       = ['\u2A1D']
    LEFT_OUTER_JOIN    = ['\u27D5']
    RIGHT_OUTER_JOIN   = ['\u27D6']
    FULL_OUTER_JOIN    = ['\u27D7']
    UNION              = ['\u222A']
    INTERSECTION       = ['\u2229']
    MINUS              = ['\u2212']
    DIVISION           = ['\u00F7']
    LESS               = ['<']
    LESS_EQUAL         = ['<=']
    GREATER            = ['>']
    GREATER_EQUAL      = ['>=']
    EQUAL              = ['=']
    NOT_EQUAL          = ['!=']

    RELATION_OPERATORS = \
        SELECTION + \
        PROJECTION + \
        CROSS_JOIN + \
        NATURAL_JOIN + \
        LEFT_OUTER_JOIN + \
        RIGHT_OUTER_JOIN + \
        FULL_OUTER_JOIN + \
        UNION + \
        INTERSECTION + \
        MINUS + \
        DIVISION

    BASIC_OPERATORS = \
        LESS + \
        LESS_EQUAL + \
        GREATER + \
        GREATER_EQUAL + \
        EQUAL + \
        NOT_EQUAL

    OPERATORS = \
        RELATION_OPERATORS + \
        BASIC_OPERATORS
