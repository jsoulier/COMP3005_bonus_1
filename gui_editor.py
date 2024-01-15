import tkinter
import tkinter.ttk as ttk

class GUIEditor(tkinter.Frame):
    ''''''

    def __init__(self, owner):
        ''''''
        super().__init__(owner)

        # Packing for text widget
        self.pack(fill=tkinter.BOTH, expand=tkinter.TRUE)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Create text widget
        text = tkinter.Text(self, wrap=tkinter.NONE)
        text.grid(row=0, column=0, sticky=tkinter.NSEW)

        # Create scrollbars
        scrollbar1 = ttk.Scrollbar(self, orient=tkinter.VERTICAL, command=text.yview)
        scrollbar2 = ttk.Scrollbar(self, orient=tkinter.HORIZONTAL, command=text.xview)
        scrollbar1.grid(row=0, column=1, sticky=tkinter.NS)
        scrollbar2.grid(row=1, column=0, sticky=tkinter.EW)
        text.configure(yscrollcommand=scrollbar1.set)
        text.configure(xscrollcommand=scrollbar2.set)
