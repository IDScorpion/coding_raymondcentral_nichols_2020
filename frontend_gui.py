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
    "width": screen_width,
    "height": screen_height,
    "dimensions": f"{screen_width}x{screen_height}"
}


# root.geometry(screen_info["dimensions"])
# pythonprogramming.net/tkinter-menu-bar-tutorial/


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.left_frame = Frame(self.master)
        self.left_frame.pack(side=LEFT)
        self.right_frame = Frame(self.master)
        self.right_frame.pack(side=RIGHT)

        self.current_student = None
        if self.current_student is None:
            self.current_student = backend.Student("None Selected", 12)
            self.current_student.student_id = None
            self.current_student.grade = None

        self.init_info()
        self.init_window()

    def init_info(self):
        self.student_name_label_text = StringVar()
        self.student_name_label_text.set(f"Student Name: {self.current_student.name}")
        self.student_name_label = Label(self.right_frame, textvariable=self.student_name_label_text)

        self.student_id_label_text = StringVar()
        self.student_id_label_text.set(f"Student ID: {self.current_student.student_id}")
        self.student_id_label = Label(self.right_frame, textvariable=self.student_id_label_text)

        self.student_grade_label_text = StringVar()
        self.student_grade_label_text.set(f"Student Grade: {self.current_student.grade}")
        self.student_grade_label = Label(self.right_frame, textvariable=self.student_grade_label_text)

        self.student_csa_level_label_text = StringVar()
        self.student_csa_level_label_text.set(f"Student CSA Level: {self.current_student.csa_level}")
        self.student_csa_level_label = Label(self.right_frame, textvariable=self.student_csa_level_label_text)

        self.student_csa_hours_label_text = StringVar()
        self.student_csa_hours_label_text.set(f"Student CSA Hours: {self.current_student.csa_hours}")
        self.student_csa_hours_label = Label(self.right_frame, textvariable=self.student_csa_hours_label_text)

    def init_window(self):
        self.master.title("FBLA Community Service Awards Tracking")
        self.pack(fill=BOTH, expand=1)

        self.menubar = Menu(self.master)

        self.report_menu = Menu(self.menubar)
        self.report_menu.add_command(label="Export Program Report", command=backend.generate_program_report)
        self.menubar.add_cascade(label="Reports", menu=self.report_menu)

        self.menubar.add_command(label="Graduate Levels", command=backend.graduate_csa_levels) # TODO: Add wrapper to run load_students to refresh data

        self.master.config(menu=self.menubar)

        self.listbox = Listbox(self.left_frame, height=50, width=100, selectmode=SINGLE)
        self.listbox.grid(column=0, row=0)
        self.listbox.insert(END, "a list entry")
        self.refresh_students_listbox()

        self.load_button = Button(self.left_frame, text="Load", command=self.load_student)
        self.load_button.grid(column=1, row=0)

        self.student_name_label = Label(self.right_frame, textvariable=self.student_name_label_text)
        self.student_name_label.grid(column=0, row=0)

        self.student_id_label = Label(self.right_frame, textvariable=self.student_id_label_text)
        self.student_id_label.grid(column=0, row=1)

        self.student_grade_label = Label(self.right_frame, textvariable=self.student_grade_label_text)
        self.student_grade_label.grid(column=0, row=2)

        self.student_csa_level_label = Label(self.right_frame, textvariable=self.student_csa_level_label_text)
        self.student_csa_level_label.grid(column=0, row=3)

        self.student_csa_hours_label = Label(self.right_frame, textvariable=self.student_csa_hours_label_text)
        self.student_csa_hours_label.grid(column=0, row=4)

    def refresh_students_listbox(self, sort_parameter=None, criteria=None):
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
        temp_student = self.listbox.get(self.listbox.curselection()[0])
        print(temp_student)
        if temp_student:
            print(temp_student)
            self.current_student = backend.search_table(temp_student)
            print(self.current_student.csa_level)
            self.student_name_label_text.set(f"Student Name: {self.current_student.name}")
            self.student_id_label_text.set(f"Student ID: {self.current_student.student_id}")
            self.student_grade_label_text.set(f"Student Grade: {self.current_student.grade}")
            self.student_csa_level_label_text.set(f"Student CSA Level: {self.current_student.csa_level}")
            self.student_csa_hours_label_text.set(f"Student CSA Hours: {self.current_student.csa_hours}")
        else:
            print("Nope")
            self.student_name_label_text.set(f"Student Name: None Selected")


# TODO: Add filter, keep working on listbox function, then add info area on right side
# TODO: Check bug with CSA levels not updating
root.state("zoomed")

app = Window(root)
root.mainloop()
