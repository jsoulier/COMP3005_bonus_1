import tkinter

from gui_editor import GUIEditor
from gui_lexer import GUILexer
from gui_options import GUIOptions

class GUI(tkinter.Tk):
    ''''''

    def __init__(self):
        ''''''
        super().__init__()
        self.title('Relational Algebra Query Processor')
        self.geometry('640x480')

        # Add widgets
        self.editor = GUIEditor(self)
        self.menu = GUIOptions(self, self.editor)
        self.lexer = GUILexer()

        # Configure menu
        self.menu.on_compute = self.on_compute
        self.configure(menu=self.menu)

    def on_compute(self):
        ''''''
        self.lexer.compute(self.editor.get())
