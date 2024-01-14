import tkinter

from table import Table
from gui_table import GUITable

class GUI(tkinter.Tk):
    ''''''

    def __init__(self):
        ''''''
        super().__init__()
        self.title('Relational Algebra Query Processor')
        self.geometry('640x480')

        string = '''
            Employees (ID, Name, Age) = {
                1, John, 32
                2, Alice, 28
                3, Bob, 29
            }
        '''
        table = Table(string)
        table = GUITable(self, table)
        table.pack()
