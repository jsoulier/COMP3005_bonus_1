import tkinter

# class PromptMenu(tkinter.Frame):

#     def __init__(self, master):
#         super().__init__(master)

#         self.run = tkinter.Button(self, text="run")
#         self.run.pack(side=tkinter.LEFT)

#         self.pack(fill=tkinter.X)

# class PromptText(tkinter.Frame):

#     def __init__(self, master):
#         super().__init__(master)

#         self.scrollbar = tkinter.Scrollbar(self)
#         self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

#         self.text = tkinter.Text(self, yscrollcommand=self.scrollbar.set)
#         self.text.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.TRUE)

#         self.scrollbar.configure(command=self.text.yview)

#         self.pack(fill=tkinter.BOTH, expand=tkinter.TRUE)

# class Prompt(tkinter.Frame):

#     def __init__(self, master):
#         super().__init__(master)

#         self.menu = PromptMenu(self)
#         self.text = PromptText(self)

#         self.pack(fill=tkinter.BOTH, expand=tkinter.TRUE)
