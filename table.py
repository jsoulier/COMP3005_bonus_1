import copy
import re

from table_error import TableError
from table_element import TableElement

class Table:
    '''
    A structural representation of a table.
    Consists of:
        - name of the table
        - columns of the table
        - rows of the table
    The columns contain the names of the columns.
    The rows contain the elements as table elements in row-major order.
    '''

    def __init__(self, string):
        '''
        Construct a table from a textual representation.
        e.g.
        Employees (ID, Name, Age) = {
            1, John, 32
            2, Alice, 28
            3, Bob, 29
        }
        name = Employees
        columns = [ID, Name, Age]
        rows = [[1, John, 32], [2, Alice, 28], [3, Bob, 29]]
        '''
        self.name = ''
        self.columns = []
        self.rows = []

        # Create an empty table
        if not string:
            return

        string = string.replace(' ', '')

        # Sanity check
        pattern = re.compile(r'[^a-zA-Z0-9{}(),.=_\-\n]')
        if pattern.search(string):
            raise TableError('Bad Characters: {}'.format(pattern.findall(string)))

        # Remove empty lines
        lines = []
        for line in string.splitlines():
            if line:
                lines.append(line)

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
        ''''''
        # Get the column to compare
        if column not in table.columns:
            raise TableError('Bad Selection: {}'.format(column))
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
        ''''''
        result = Table('')
        result.columns = copy.deepcopy(table.columns)
        result.rows = copy.deepcopy(table.rows)

        # Gather columns to remove
        indices = []
        for column in columns:
            if column not in result.columns:
                raise TableError('Bad Projection: {}'.format(column))
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

    @staticmethod
    def cross_join(table1, table2):
        ''''''
        result = Table('')
        result.columns = table1.columns + table2.columns

        # Append rows together
        for row1 in table1.rows:
            for row2 in table2.rows:
                result.rows.append(row1 + row2)

        return result

    @staticmethod
    def natural_join(table1, table2, column1, comparator, column2):
        ''''''
        raise NotImplementedError

    @staticmethod
    def left_outer_join(table1, table2, column1, comparator, column2):
        ''''''
        raise NotImplementedError

    @staticmethod
    def right_outer_join(table1, table2, column1, comparator, column2):
        ''''''
        raise NotImplementedError

    @staticmethod
    def full_outer_join(table1, table2, column1, comparator, column2):
        ''''''
        raise NotImplementedError

    @staticmethod
    def union(table1, table2):
        ''''''
        raise NotImplementedError

    @staticmethod
    def intersection(table1, table2):
        ''''''
        raise NotImplementedError

    @staticmethod
    def minus(table1, table2):
        ''''''
        raise NotImplementedError

    @staticmethod
    def division(table1, table2):
        ''''''
        raise NotImplementedError
