import re

from table_element import TableElement

class TableError(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Table:
    """ A structural representation of a table """

    def __init__(self, string):
        """ Construct a table from a textual representation.
        e.g.
        Employees (ID, Name, Age) = {
            1, John, 32
            2, Alice, 28
            3, Bob, 29
        }
        """

        # Strip off all whitespace and leading newline characters
        string = string.replace(' ', '')
        string = string.lstrip()

        # Sanity check on the string
        pattern = re.compile(r'[^a-zA-Z0-9{}(),.=\-\n]')
        if pattern.search(string):
            raise TableError("Found Bad Characters: {}".format(pattern.findall(string)))

        lines = string.splitlines()
        columns = lines[0]
        rows = lines[1:-1]

        # Strip the header until there is only the table and column titles
        columns = columns.replace('(', ' ')
        columns = columns.replace(')', ' ')
        columns = columns.replace('{', ' ')
        columns = columns.replace('}', ' ')
        columns = columns.replace('=', ' ')
        columns = columns.replace(',', ' ')
        columns = columns.split()

        self.name = columns[0]
        self.columns = columns[1:]
        self.rows = []

        # Convert the rows of strings to rows of table elements
        for row in rows:
            columns = row.split(',')
            self.rows.append([TableElement(i) for i in columns])
