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

        self.menubar = Menu(self.master)

        self.report_menu = Menu(self.menubar)
        self.report_menu.add_command(label="Export Program Report", command=backend.generate_program_report)

        self.menubar.add_cascade(label="Reports", menu=self.report_menu)
        self.master.config(menu=self.menubar)

        self.listbox = Listbox(self.master)
        self.listbox.pack()
        self.listbox.insert(END, "a list entry")
        self.refresh_students_listbox()

        self.load_button = Button(self.master,text="Load", command=self.load_student)
        self.load_button.pack()

    def refresh_students_listbox(self, sort_parameter=None,criteria=None):
        students = backend.return_student_list(sort_parameter, criteria)
        if students is None:
            student_names = ["No data found."]
        else:
            student_names = []
            for student in students:
                student_names.append(student["name"])
        self.listbox.delete(0, END)
        for name in student_names:
            self.listbox.insert(END, name)
    def load_student(self):
        print(self.listbox.get(0))

# TODO: Add filter, keep working on listbox function, then add info area on right side
root.state("zoomed")

app = Window(root)
root.mainloop()

