import copy
import re

from relational_operator import RelationalOperator
from table_element import TableElement
from table_error import TableError
from table_operator import TableOperator

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

        # Sanity
        pattern = re.compile(r'[^a-zA-Z0-9{}(),.=_\-\n\s]')
        if pattern.search(string):
            raise TableError()

        # Remove empty lines
        lines = []
        for line in string.splitlines():
            if line and not line.isspace():
                lines.append(line)

        columns = lines[0]
        rows = lines[1:-1]

        # Strip the header until there is only the table and column titles
        columns = columns.replace('(', ' ')
        columns = columns.replace(')', ' ')
        columns = columns.replace('{', ' ')
        columns = columns.replace('=', ' ')
        columns = columns.replace(',', ' ')
        columns = columns.split()

        # Ensure column doesn't contain bad characters
        pattern = re.compile(r'[^a-zA-Z0-9_]')
        for i, column in enumerate(columns):
            column = column.strip()
            if pattern.search(column.strip()):
                raise TableError()
            columns[i] = column

        self.name = columns[0]
        self.columns = columns[1:]
        self.rows = []

        # Convert the rows of strings to rows of table elements
        for row in rows:
            columns = row.replace(',', ' ').split()
            self.rows.append([TableElement(i) for i in columns])

            # Ensure rows are the same length
            if len(columns) != len(self.columns):
                raise TableError()

    @staticmethod
    def selection(table, column, comparator, value):
        ''''''
        # Get the column to compare
        if column not in table.columns:
            raise TableError()
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
                raise TableError()
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
        count1 = len(table1.rows)
        count2 = len(table2.rows)
        if count1 != count2:
            raise TableError()

        result = Table('')
        result.columns = table1.columns + table2.columns

        # Append rows together
        for row1 in table1.rows:
            for row2 in table2.rows:
                result.rows.append(row1 + row2)

        return result

    @staticmethod
    def join(table1, table2, column1, comparator, column2, type):
        ''''''
        columns1 = []
        columns2 = []

        # Use provided columns
        if comparator:
            if column1 not in table1.columns:
                raise TableError()
            if column2 not in table2.columns:
                raise TableError()
            columns1 = [column1]
            columns2 = [column2]

        # Find columns
        else:
            comparator = RelationalOperator.EQUAL
            for column in table1.columns:
                if column not in table2.columns:
                    continue
                columns1.append(column)
                columns2.append(column)

        # Calculate indices
        indices1 = []
        indices2 = []
        for column in columns1:
            indices1.append(table1.columns.index(column))
        for column in columns2:
            indices2.append(table2.columns.index(column) + len(table1.columns))

        # Calculate and save rows to remove
        table = Table.cross_join(table1, table2)
        counts1 = len(table1.rows) * [0]
        counts2 = len(table2.rows) * [0]
        indices = []
        for column1, column2 in zip(indices1, indices2):
            for i, row in enumerate(table.rows):
                if comparator(row[column1], row[column2]):
                    continue
                counts1[i // len(table1.rows)] += 1
                counts2[i % len(table1.rows)] += 1
                indices.append(i)
        for i in reversed(indices):
            table.rows.pop(i)

        # Try adding back fully removed rows
        empty1 = len(table2.columns) * [TableElement('')]
        empty2 = len(table1.columns) * [TableElement('')]
        if type.left():
            for count in counts1:
                if count == len(table1.rows):
                    table.rows.append(table1.rows[count - 1] + empty1)
        if type.right():
            for count in counts2:
                if count == len(table2.rows):
                    table.rows.append(empty2 + table2.rows[count - 1])

        return table

    @staticmethod
    def natural_join(*args):
        ''''''
        return Table.join(*args, TableOperator.NATURAL_JOIN)

    @staticmethod
    def left_outer_join(*args):
        ''''''
        return Table.join(*args, TableOperator.LEFT_OUTER_JOIN)

    @staticmethod
    def right_outer_join(*args):
        ''''''
        return Table.join(*args, TableOperator.RIGHT_OUTER_JOIN)

    @staticmethod
    def full_outer_join(*args):
        ''''''
        return Table.join(*args, TableOperator.FULL_OUTER_JOIN)

    @staticmethod
    def union(table1, table2):
        ''''''
        raise NotImplementedError()

    @staticmethod
    def intersection(table1, table2):
        ''''''
        raise NotImplementedError()

    @staticmethod
    def minus(table1, table2):
        ''''''
        raise NotImplementedError()

    @staticmethod
    def division(table1, table2):
        ''''''
        raise NotImplementedError()
