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
        ''' Create child nodes, tables, and operators from string and table. '''
        self.string = self.string.strip()

        # Check if node is a known table
        for table in tables:
            if self.string != table.name:
                continue
            self.table = table
            return

        # Create child nodes
        string = self.string
        while 1:
            node = self.extract(string)
            if not node:
                break
            node.parse(tables)
            string = string[:node.start] + string[node.end:]
            self.nodes.append(node)

        # Get table operator, relational operator, and parameters
        self.table_operator = self.type(string)
        string = self.splice(self.string)
        string = string[len(self.table_operator):]
        self.parametrize(string)

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

    def splice(self, string):
        ''' Splice out child nodes. '''
        # Ensure table operator correct operands
        if self.table_operator.operands != len(self.nodes):
            raise QueryError()

        # Handle single operand table operators
        if self.table_operator.operands == 1:

            # Ensure node comes after the table operator
            index1 = string.find(self.nodes[0].string)
            index2 = string.find(str(self.table_operator))
            if index1 < index2:
                raise QueryError()

            # Splice out node
            string = string[:self.nodes[0].start]

        # Handle single operand table operators
        if self.table_operator.operands == 2:

            # Ensure nodes come before and after the table operator
            index1 = string.find(self.nodes[0].string)
            index2 = string.find(str(self.table_operator))
            index3 = string.find(self.nodes[1].string)
            if index1 > index2:
                raise QueryError()
            if index3 < index2:
                raise QueryError()

            # Splice out nodes
            string = string[self.nodes[0].end:self.nodes[0].end + self.nodes[1].start]

        string = string.strip()
        return string

    def parametrize(self, string):
        ''' Parse parameters and relational operator. '''
        string = string.strip()

        # Ensure table operator supports no parameters
        if not string:
            if not self.table_operator.parametrize(0):
                raise QueryError()
            return

        # Check for relational operator
        for relational_operator in RelationalOperator:
            if not relational_operator.within(string):
                continue
            self.relational_operator = relational_operator
            break

        # Split parameters
        string = string.replace(',', ' ')
        if self.relational_operator:
            string = string.replace(str(self.relational_operator), ' {} '.format(self.relational_operator))
        self.parameters = string.split()

        # Remove relational operator from parameters
        if self.relational_operator:
            if len(self.parameters) != 3:
                raise QueryError()

            # Ensure operator is at the center
            index = self.parameters.index(str(self.relational_operator))
            if index != 1:
                raise QueryError()

            # Remove operator from parameters
            self.parameters.pop(index)

        # Ensure valid number of parameters
        if not self.table_operator.parametrize(len(self.parameters)):
            raise QueryError()

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

            # Found a closing parenthesis
            count -= 1
            if not count:
                return i
            if count < 0:
                break

        raise QueryError()

    @staticmethod
    def extract(string):
        ''' Extract node from parentheses. '''
        node = QueryNode('')

        # Find the parentheses
        node.start = string.find('(')
        if node.start == -1:
            return None
        node.end = QueryNode.pair(string) + 1

        # Create a substring and strip off the parentheses
        node.string = string[node.start + 1:node.end - 1]
        node.string = node.string.strip()
        return node

    @staticmethod
    def type(string):
        ''' Get table operator type. '''
        # Separate the operator and parameters
        strings = string.split(maxsplit=1)
        if not strings:
            raise QueryError()
        string = strings[0]

        # Find the table operator
        for table_operator in TableOperator:
            if table_operator == string:
                return table_operator

        raise QueryError()
