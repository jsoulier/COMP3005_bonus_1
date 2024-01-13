
class QueryError(Exception):
    ''' Signifies an error when parsing a query. '''

    def __init__(self, *args, **kwargs):
        ''''''
        super().__init__(*args, **kwargs)
