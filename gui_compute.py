import tkinter

from gui_error import GUIError
from gui_lexer import GUILexer

class GUICompute(tkinter.Toplevel):
    ''''''

    def __init__(self):
        ''''''
        super().__init__()
        self.title('Compute')
        self.geometry('320x240')
        self.resizable(tkinter.FALSE, tkinter.TRUE)

        # Hide window until compute
        self.protocol('WM_DELETE_WINDOW', self.quit)
        self.quit()

        # Queries or error
        self.widget = None

    def quit(self):
        ''''''
        # Disable destroying window
        self.iconify()

    def compute(self, string):
        ''''''
        self.deiconify()
        self.reset()

        self.widget = GUILexer(self, string)

        # Compute and display queries. Show error if fails
        try:
            self.widget = GUILexer(self, string)
        except Exception as e:
            self.reset()
            self.widget = GUIError(self, str(e))
            print(e)

    def reset(self):
        ''' Delete widget if exists. '''
        if not self.widget:
            return
        self.widget.destroy()
        self.widget = None
