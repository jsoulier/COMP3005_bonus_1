import tkinter
import tkinter.ttk as ttk

class GUIEditor(ttk.Frame):
    ''''''

    def __init__(self, master):
        ''''''
        super().__init__(master)

        # Create text widget
        self.text = tkinter.Text(self, wrap=tkinter.NONE)
        self.text.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.text.configure(undo=tkinter.TRUE)
        self.text.configure(maxundo=-1)
        self.text.bind('<Key>', self.key)

        # Allow fill
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Create scrollbars
        self.scrollbar1 = ttk.Scrollbar(self, orient=tkinter.VERTICAL, command=self.text.yview)
        self.scrollbar2 = ttk.Scrollbar(self, orient=tkinter.HORIZONTAL, command=self.text.xview)
        self.scrollbar1.grid(row=0, column=1, sticky=tkinter.NS)
        self.scrollbar2.grid(row=1, column=0, sticky=tkinter.EW)
        self.text.configure(yscrollcommand=self.scrollbar1.set)
        self.text.configure(xscrollcommand=self.scrollbar2.set)

        self.pack(fill=tkinter.BOTH, expand=tkinter.TRUE)

    def key(self, event):
        ''''''
        # Needed because autoseparator is broken
        keys = ['space', 'comma']
        if event.keysym not in keys:
            return
        self.text.edit_separator()
    
    def undo(self):
        ''''''
        try:
            self.text.edit_undo()
        except Exception:
            pass
    
    def redo(self):
        ''''''
        try:
            self.text.edit_redo()
        except Exception:
            pass

    def insert(self, string):
        ''''''
        self.text.insert(tkinter.INSERT, string)

    def get(self):
        ''''''
        return self.text.get(1.0, tkinter.END)[:-1]
    
    def set(self, string):
        ''''''
        self.text.delete(1.0, tkinter.END)
        self.text.insert(tkinter.END, string)
