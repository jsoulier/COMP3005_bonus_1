import tkinter

from gui_editor import GUIEditor

class GUI(tkinter.Tk):
    ''''''

    def __init__(self):
        ''''''
        super().__init__()
        self.title('Relational Algebra Query Processor')
        self.geometry('640x480')

        self.editor = GUIEditor(self)
