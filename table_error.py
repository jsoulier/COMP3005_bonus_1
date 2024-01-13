
class TableError(Exception):
    ''' Signifies an error when parsing a table. '''

    def __init__(self, *args, **kwargs):
        ''''''
        super().__init__(*args, **kwargs)
