
class Table():

    def __init__(self, columns, rows):

        self.columns = columns
        self.rows = rows

    @staticmethod
    def selection(table, column, condition):
        pass

    @staticmethod
    def projection(table, columns):
        pass

    @staticmethod
    def cross_join(table1, table2):
        pass

    @staticmethod
    def natural_join(table1, table2, column1, column2, condition):
        pass
