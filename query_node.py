from query_error import QueryError
from relational_operator import RelationalOperator
from table import Table
from table_operator import TableOperator

class QueryNode:
    '''
    A tree representation of a query.
    Consists of:
        - child nodes (QueryNode)
        - operator to apply to the child nodes (TableOperator)
        - condition for the operator (RelationalOperator)
        - parameters for the condition
        - computed table (Table)
    Every pair of parentheses is converted into a child node, creating a binary
    tree-like structure.
    Each child node will have a smaller query until we eventually find a table
    allowing us to create a leaf node.
    '''

    def __init__(self, string):
        ''''''
        # For parsing
        self.start = 0
        self.end = 0
        self.string = string
        # For computing
        self.table = None
        self.table_operator = TableOperator.NONE
        self.relational_operator = RelationalOperator.NONE
        self.parameters = []
        self.nodes = []

    def parse(self, tables):
        ''' Create child nodes, tables, and operators from the string and table. '''
        self.string = self.string.strip()

        # Check if node is a known table
        for table in tables:
            if self.string != table.name:
                continue
            self.table = table
            return

        # Create child nodes
        string = self.string
        for i in range(2):
            node = self.extract(string)
            if not node:
                break
            node.parse(tables)
            string = string[:node.start] + string[node.end:]
            self.nodes.append(node)

        # Separate the operator and parameters
        strings = string.split(maxsplit=1)

        # Find the table operator
        for table_operator in TableOperator:
            if table_operator != strings[0]:
                continue
            self.table_operator = table_operator
            break
        if not self.table_operator:
            raise QueryError()
        if self.table_operator.nodes != len(self.nodes):
            raise QueryError()

        # Strip out right and maybe left node
        if self.table_operator.nodes == 1:
            self.string = self.string[:self.nodes[0].start]
        if self.table_operator.nodes == 2:
            self.string = self.string[self.nodes[0].end:self.nodes[0].end + self.nodes[1].start]

        # Separate the operator and parameters, again...
        strings = self.string.split(maxsplit=1)

        # Check for parameters
        if len(strings) > 1:
            # Check for relational operator
            for relational_operator in RelationalOperator:
                if not relational_operator.within(strings[1]):
                    continue
                self.relational_operator = relational_operator
                break

            # Parse parameters
            strings[1] = strings[1].replace(',', ' ')
            if self.relational_operator:
                strings[1] = strings[1].replace(str(self.relational_operator), ' {} '.format(self.relational_operator))
            self.parameters = strings[1].split()
            if self.relational_operator:
                # Ensure operator is not at the start or end
                index = self.parameters.index(str(self.relational_operator))
                if not index or index == len(self.parameters) - 1:
                    raise QueryError()
                self.parameters.pop(index)

        # Ensure valid number of parameters
        if not self.table_operator.parametrize(len(self.parameters)):
            raise QueryError()

    def compute(self):
        ''' Compute the result of the query. '''
        # Check if node is a leaf node
        if self.table:
            return self.table

        # Get table arguments
        tables = []
        for node in self.nodes:
            tables.append(node.compute())
        comparator = self.relational_operator
        parameters = ['', '']
        if self.parameters:
            parameters = self.parameters

        # Forward arguments to table functions
        if self.table_operator == TableOperator.SELECTION:
            return Table.selection(tables[0], parameters[0], comparator, parameters[1])
        if self.table_operator == TableOperator.PROJECTION:
            return Table.projection(tables[0], parameters)
        if self.table_operator == TableOperator.CROSS_JOIN:
            return Table.cross_join(tables[0], tables[1])
        if self.table_operator == TableOperator.NATURAL_JOIN:
            return Table.natural_join(tables[0], tables[1], parameters[0], comparator, parameters[1])
        if self.table_operator == TableOperator.LEFT_OUTER_JOIN:
            return Table.left_outer_join(tables[0], tables[1], parameters[0], comparator, parameters[1])
        if self.table_operator == TableOperator.RIGHT_OUTER_JOIN:
            return Table.right_outer_join(tables[0], tables[1], parameters[0], comparator, parameters[1])
        if self.table_operator == TableOperator.FULL_OUTER_JOIN:
            return Table.full_outer_join(tables[0], tables[1], parameters[0], comparator, parameters[1])
        if self.table_operator == TableOperator.UNION:
            return Table.union(tables[0], tables[1])
        if self.table_operator == TableOperator.INTERSECTION:
            return Table.intersection(tables[0], tables[1])
        if self.table_operator == TableOperator.MINUS:
            return Table.minus(tables[0], tables[1])
        if self.table_operator == TableOperator.DIVISION:
            return Table.division(tables[0], tables[1])
        raise AssertionError()

    @staticmethod
    def pair(string):
        ''' Find the index of the closing parenthesis matching the first one. '''
        count = 0
        for i, char in enumerate(string):
            # Keep track of the parenthesis stack
            if char == '(':
                count += 1
                continue
            if char != ')':
                continue
            count -= 1
            if not count:
                return i
            # If there is a closing parenthesis before an opening one
            if count < 0:
                break
        raise QueryError()

    @staticmethod
    def extract(string):
        ''' Extract a node from a string. '''
        node = QueryNode('')
        node.start = string.find('(')
        if node.start == -1:
            return None
        node.end = QueryNode.pair(string) + 1
        # Create a substring and strip off the parentheses
        node.string = string[node.start + 1:node.end - 1]
        node.string = node.string.strip()
        return node
