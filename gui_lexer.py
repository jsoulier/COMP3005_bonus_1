import tkinter
import tkinter.ttk as ttk

from gui_table import GUITable
from lexer import Lexer

class GUILexer(tkinter.Canvas):
    ''''''

    def __init__(self, master, string):
        ''''''

        string = '''
            Stud_Course (sid, cname, mark) = {
                1, Math, 3
                1, Physics, 2
                1, Network, 3
                2, Math, 3
                2, Physics, 2
                2, Network, 3
                3, Network, 3
            }
            Course (cname, Hours) = {
                Math, 3
                Physics, 2
                Network, 3
            }
            (pi sid, cname Stud_Course) / (pi cname Course)
            pi sid Stud_Course
            pi cname, Hours Course
        '''
        lexer = Lexer()
        tables = lexer.compute(string)
        queries = lexer.queries

        super().__init__(master)
        self.grid(row=0, column=0, sticky=tkinter.NSEW)

        self.scrollbar = ttk.Scrollbar(self, orient=tkinter.VERTICAL, command=self.yview)
        self.scrollbar.grid(row=0, column=1, sticky=tkinter.NS)

        self.configure(yscrollcommand=self.scrollbar.set)

        self.frame = ttk.Frame(self)
        self.create_window((0, 0), window=self.frame, anchor=tkinter.NW)

        for i, [query, table] in enumerate(zip(queries, tables)):

            frame = ttk.LabelFrame(self.frame, text=query.string)
            frame.grid(row=i, column=0, sticky=tkinter.NSEW)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(0, weight=1)
            frame = GUITable(frame, table)

        self.frame.update_idletasks()
        self.config(scrollregion=self.bbox("all"))

        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
