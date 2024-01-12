import enum

class QueryNodeType(enum.Enum):
    NONE           = 0
    TABLE          = 1
    TABLE_OPERATOR = 2
    GROUP          = 3
