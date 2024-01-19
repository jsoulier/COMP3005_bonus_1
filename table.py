import copy

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

    def __str__(self):
        ''''''
        string = self.name
        if self.name:
            string += ' '
        string += '('

        # Add columns
        for i, column in enumerate(self.columns):
            string += column
            if i < len(self.columns) - 1:
                string += ', '
        string += ') = {\n'

        # Add rows
        for row in self.rows:
            string += '    '
            for i, column in enumerate(row):
                string += str(column)
                if i < len(row) - 1:
                    string += ', '
            string += '\n'

        string += '}'
        return string

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

        # Gather columns to keep
        indices = []
        for column in columns:
            if column in table.columns:
                indices.append(table.columns.index(column))

        # Add columns
        for row in table.rows:
            result.rows.append([row[i] for i in indices])
        result.columns = [table.columns[i] for i in indices]

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
            indices2.append(table2.columns.index(column))

        result = Table('')
        result.columns = table1.columns + table2.columns

        # If any columns matched
        if columns1 and columns2:
            rows1 = copy.deepcopy(table1.rows)
            rows2 = copy.deepcopy(table2.rows)

            # For filling empty space on specific joins
            empty1 = len(table2.columns) * [TableElement('')]
            empty2 = len(table1.columns) * [TableElement('')]

            # Find matches for first table
            for row1 in rows1:
                matches = []

                # Compare columns and match rows
                columns1 = [row1[i] for i in indices1]
                for row2 in rows2:
                    columns2 = [row2[i] for i in indices2]
                    if columns1 != columns2:
                        continue
                    result.rows.append(row1 + row2)
                    matches.append(row2)

                # Delete matches
                for match in matches:
                    rows2.remove(match)

                # Fill unmatched rows
                if not matches and type.left():
                    result.rows.append(row1 + empty1)

            # Find matches for second table
            for row2 in rows2:
                matches = []

                # Compare columns and match rows
                columns2 = [row2[i] for i in indices2]
                for row1 in rows1:
                    columns1 = [row1[i] for i in indices1]
                    if columns2 != columns1:
                        continue
                    result.rows.append(row2 + row1)
                    matches.append(row1)

                # Delete matches
                for match in matches:
                    rows1.remove(match)

                # Fill unmatched rows
                if not matches and type.right():
                    result.rows.append(empty2 + row2)

        # Prepare for deleting duplicated columns
        for row in result.rows:
            for index1, index2 in zip(indices1, indices2):
                index2 += len(table1.columns)

                # Copy over valid columns
                if not row[index1]:
                    row[index1] = row[index2]
                if not row[index2]:
                    row[index2] = row[index1]

        # Sort to-be-deleted columns back to front
        columns = []
        for index in indices2:
            columns.append(index + len(table1.columns))
        columns.sort()
        columns.reverse()

        # Delete duplicated columns
        for column in columns:
            result.columns.pop(column)
            for row in result.rows:
                row.pop(column)

        return result

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
        # Ensure columns match
        for column in table1.columns:
            if column not in table2.columns:
                raise TableError()

        result = Table('')
        result.columns = copy.deepcopy(table1.columns)
        result.rows = copy.deepcopy(table1.rows)

        # Add row if not already in the first table
        for row in table2.rows:
            if row not in table1.rows:
                result.rows.append(row)

        return result

    @staticmethod
    def intersection(table1, table2):
        ''''''
        # Ensure columns match
        for column in table1.columns:
            if column not in table2.columns:
                raise TableError()
            
        result = Table('')
        result.columns = copy.deepcopy(table1.columns)
        
        # Add row if in both tables
        for row in table1.rows:
            if row in table2.rows:
                result.rows.append(row)

        return result

    @staticmethod
    def subtraction(table1, table2):
        ''''''
        # Ensure columns match
        for column in table1.columns:
            if column not in table2.columns:
                raise TableError()

        result = Table('')
        result.columns = copy.deepcopy(table1.columns)
        result.rows = copy.deepcopy(table1.rows)

        # Remove row if in first table
        for row in table2.rows:
            if row in result.rows:
                result.rows.remove(row)

        return result

    @staticmethod
    def division(table1, table2):
        ''''''
        # Division by zero
        if not table2.rows:
            raise TableError()

        result = Table('')
        result.columns = copy.deepcopy(table1.columns)

        # Remove columns from table
        flag = 0
        for column in table2.columns:
            if column not in table1.columns:
                flag = 1
                continue
            result.columns.remove(column)
        if flag:
            return result

        # Create hash for each left row to each right row
        rows = {}
        for row1 in table1.rows:
            row_l = tuple(row1[:-len(table2.columns)])
            row_r = tuple(row1[-len(table2.columns):])
            if row_l not in rows:
                rows[row_l] = {}
            if row_r not in rows[row_l]:
                rows[row_l][row_r] = 0
            rows[row_l][row_r] += 1

        # Check if left rows contain all the required right rows
        for row_l, rows_r in rows.items():
            i = -1
            for row2 in table2.rows:
                row2 = tuple(row2)

                # Count the number of valid rows
                if row2 in rows_r:
                    if i == -1:
                        i = rows_r[row2]
                    i = min(i, rows_r[row2])
                else:
                    i = -1
                    break

            # Add the valid rows
            i = max(i, 0)
            for j in range(i):
                result.rows.append(list(row_l))

        return result
