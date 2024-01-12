
class TableError(Exception):
    """ Signifies an error in parsing a table. """

    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
