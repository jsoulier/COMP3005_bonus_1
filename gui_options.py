import tkinter
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

from table_operator import TableOperator

class GUIOptions(tkinter.Menu):
    ''''''

    def __init__(self, master, editor):
        ''''''
        super().__init__(master)

        self.editor = editor

        # Add main commands
        self.add_command(label='Open', command=self.open)
        self.add_command(label='Save', command=self.save)
        self.add_command(label='Compute', command=self.compute)

        # Add table operator commands
        self.add_command(label='Operators:', columnbreak=tkinter.TRUE)
        self.add_command(label=TableOperator.SELECTION, command=lambda: self.insert(TableOperator.SELECTION))
        self.add_command(label=TableOperator.PROJECTION, command=lambda: self.insert(TableOperator.PROJECTION))
        self.add_command(label=TableOperator.CROSS_JOIN, command=lambda: self.insert(TableOperator.CROSS_JOIN))
        self.add_command(label=TableOperator.NATURAL_JOIN, command=lambda: self.insert(TableOperator.NATURAL_JOIN))
        self.add_command(label=TableOperator.LEFT_OUTER_JOIN, command=lambda: self.insert(TableOperator.LEFT_OUTER_JOIN))
        self.add_command(label=TableOperator.RIGHT_OUTER_JOIN, command=lambda: self.insert(TableOperator.RIGHT_OUTER_JOIN))
        self.add_command(label=TableOperator.FULL_OUTER_JOIN, command=lambda: self.insert(TableOperator.FULL_OUTER_JOIN))
        self.add_command(label=TableOperator.UNION, command=lambda: self.insert(TableOperator.UNION))
        self.add_command(label=TableOperator.INTERSECTION, command=lambda: self.insert(TableOperator.INTERSECTION))
        self.add_command(label=TableOperator.MINUS, command=lambda: self.insert(TableOperator.MINUS))
        self.add_command(label=TableOperator.DIVISION, command=lambda: self.insert(TableOperator.DIVISION))

    def open(self):
        ''''''
        # Ask for path
        path = filedialog.askopenfilename()
        if not path:
            return

        # Read file into string
        string = ''
        with open(path, 'r', encoding='utf-8') as file:
            string = file.read()

        # Ensure user wants to override
        if self.editor.get():
            result = messagebox.askyesno('Yes/No', 'Do you want to overwrite the contents?')
            if not result:
                return
            
        self.editor.set(string)

    def save(self):
        ''''''
        # Ask for path
        path = filedialog.asksaveasfilename(filetypes=[('', '.txt')])
        if not path:
            return
        
        # Write string into file
        with open(path, 'w', encoding='utf-8') as file:
            file.write(self.editor.get())

    def insert(self, string):
        ''''''
        self.editor.insert(string)

    def on_compute(self):
        ''''''
        raise NotImplementedError
    
    def compute(self):
        ''''''
        self.on_compute()
