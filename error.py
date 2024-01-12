
class TableError(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class QueryError:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
