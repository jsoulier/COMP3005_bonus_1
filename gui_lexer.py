import tkinter

from gui_editor import GUIEditor
from lexer import Lexer

class GUILexer(tkinter.Toplevel):
    ''''''

    def __init__(self):
        ''''''
        super().__init__()
        self.title('')
        self.geometry('240x320')

        # Hide window until compute
        self.protocol('WM_DELETE_WINDOW', self.quit)
        self.quit()

        self.editor = GUIEditor(self)
        self.lexer = Lexer()

    def quit(self):
        ''''''
        # Disable destroying window
        self.iconify()

    def compute(self, string):
        ''''''
        self.deiconify()

        # Enable editing and clear
        self.editor.text.config(state=tkinter.NORMAL)
        self.editor.set('')

        try:
            # Try to print tables and queries
            tables = self.lexer.compute(string)
            queries = self.lexer.queries
            for i, [table, query] in enumerate(zip(tables, queries)):
                table.name = 'Table' + str(i)
                self.editor.insert(query)
                self.editor.insert(' =\n')
                self.editor.insert(table)
                self.editor.insert('\n\n')

        # If bad formatting or computing, print error
        except Exception as e:
            self.editor.insert(str(e))
            print(e)

        # Disable editing
        self.editor.text.config(state=tkinter.DISABLED)
