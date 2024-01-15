import tkinter

from gui_editor import GUIEditor
from gui_menu import GUIMenu

class GUI(tkinter.Tk):
    ''''''

    def __init__(self):
        ''''''
        super().__init__()
        self.title('Relational Algebra Query Processor')
        self.geometry('640x480')

        # Add widgets
        self.editor = GUIEditor(self)
        self.menu = GUIMenu(self, self.editor)

        # Configure menu
        self.menu.on_execute = self.execute
        self.configure(menu=self.menu)

    def execute(self):
        ''''''
