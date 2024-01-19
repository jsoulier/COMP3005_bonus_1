import tkinter

from gui_editor import GUIEditor
from lexer import Lexer

class GUILexer(tkinter.Toplevel):
    ''''''

    def __init__(self):
        ''''''
        super().__init__()
        self.title('')
        self.geometry('640x480')

        # Hide window until compute
        self.protocol('WM_DELETE_WINDOW', self.quit)
        self.quit()

        self.editor = GUIEditor(self)

    def quit(self):
        ''''''
        # Disable destroying window
        self.iconify()

    def compute(self, string):
        ''''''
        self.deiconify()
        self.editor.unlock()
        self.editor.set('')

        try:
            self.editor.set(Lexer.format(string))

        # If bad formatting or computing, print error
        except Exception as e:
            self.editor.insert(str(e))
            print(e)

        self.editor.lock()
