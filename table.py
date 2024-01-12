import copy
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
        name = Employees
        columns = [ID, Name, Age]
        rows = [[1, John, 32], [2, Alice, 28], [3, Bob, 29]]
        """

        self.name = ''
        self.columns = []
        self.rows = []

        # Create an empty table
        if not string:
            return

        # Strip off all whitespace and leading newline characters
        string = string.replace(' ', '')
        string = string.lstrip()

        # Sanity check on the string
        pattern = re.compile(r'[^a-zA-Z0-9{}(),.=\-\n]')
        if pattern.search(string):
            raise TableError('Bad Characters: {}'.format(pattern.findall(string)))

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

    @staticmethod
    def selection(table, column, comparator, value):

        index = table.columns.index(column)

        result = Table('')
        result.columns = copy.deepcopy(table.columns)

        # Copy the matching rows
        for row in table.rows:
            if comparator(row[index], value):
                result.rows.append(copy.deepcopy(row))

        return result

    @staticmethod
    def projection(table, columns):

        indices = []

        result = Table('')
        result.columns = copy.deepcopy(table.columns)
        result.rows = copy.deepcopy(table.rows)

        # Gather columns to remove
        for column in columns:
            indices.append(result.columns.index(column))

        # Remove columns
        for index in reversed(indices):
            result.columns.pop(index)
            for row in result.rows:
                row.pop(index)

        # Clear the rows if there are no more columns
        if not result.columns:
            result.rows = []

        return result
