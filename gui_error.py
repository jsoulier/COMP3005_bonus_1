import tkinter

class GUIError(tkinter.Text):
    ''''''

    def __init__(self, master, string):
        ''''''
        super().__init__(master)

        # Set immutable string
        self.insert(tkinter.END, string)
        self.configure(state=tkinter.DISABLED)
        self.configure(wrap=tkinter.NONE)
