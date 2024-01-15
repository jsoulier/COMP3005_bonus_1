import copy

from query_node import QueryNode

class Query:
    ''' A wrapper for a root QueryNode. '''

    def __init__(self, string, tables):
        ''''''
        self.string = string.strip()
        self.tables = copy.deepcopy(tables)

    def compute(self):
        ''''''
        # Add parentheses to table names
        string = self.string
        for table in self.tables:
            string = self.parenthesize(string, table.name)

        # Start the root parse and compute
        root = QueryNode(string)
        root.parse(self.tables)
        return root.compute()
    
    def __str__(self):
        ''''''
        return self.string

    @staticmethod
    def parenthesize(string1, string2):
        ''' Ensure string2 occurrences in string1 are surrounded with parentheses. '''
        indices = Query.occurrences(string1, string2)
        count = 0

        # Walk through the indices and check if they need parentheses
        for index in indices:
            start = index + count
            end = start + len(string2)
            result1 = 0
            result2 = 0

            # Search backwards for characters
            for i in range(start - 1, -1, -1):
                if string1[i] == '(':
                    result1 = 1
                    break
                if string1[i] != ' ':
                    break

            # Search forward for characters
            for i in range(end, len(string1)):
                if string1[i] == ')':
                    result2 = 1
                    break
                if string1[i] != ' ':
                    break

            # Skip if there are already parentheses
            if result1 and result2:
                continue

            # Finally, add the parentheses
            string1 = '{}({}){}'.format(string1[:start], string2, string1[end:])
            count += 2

        return string1

    @staticmethod
    def occurrences(string1, string2):
        ''' Get string2 occurrences in string1. '''
        indices = []
        start = 0
        index = 0
        valid = '() '

        if not string2:
            return indices
        
        # Scan for occurrences
        while start < len(string1):
            index = string1.find(string2, start)
            if index == -1:
                break
            start = index + len(string2)

            # Check if the string is compound
            if index and string1[index - 1] not in valid:
                continue
            if start < len(string1) and string1[start] not in valid:
                continue
            indices.append(index)

        return indices
