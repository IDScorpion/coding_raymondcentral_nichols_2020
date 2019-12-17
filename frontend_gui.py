import os
from tkinter import *

import backend

"""
Will provide the GUI for the program.
I want to finish the backend before building a GUI
"""
if os.path.exists(r"data") is False:
    backend.setup()

root = Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
screen_info = {
    "width" : screen_width,
    "height": screen_height,
    "dimensions": f"{screen_width}x{screen_height}"
}

#root.geometry(screen_info["dimensions"])
# pythonprogramming.net/tkinter-menu-bar-tutorial/
class Window(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("FBLA Community Service Awards Tracking")
        self.pack(fill=BOTH, expand=1)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        export_menu = Menu(menu)
        export_menu.add_command(label="Export", command=backend.generate_program_report)
root.state("zoomed")

app = Window(root)
root.mainloop()

