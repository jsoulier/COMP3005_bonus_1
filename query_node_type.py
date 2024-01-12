import enum

class QueryNodeType(enum.Enum):
    NONE           = 0
    ROOT           = 1
    TABLE          = 2
    TABLE_OPERATOR = 3
    GROUP          = 4
