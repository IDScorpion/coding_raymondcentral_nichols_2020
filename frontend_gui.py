import os
from tkinter import *
from tkinter import messagebox, filedialog
from sqlite3 import IntegrityError
import backend

# TODO: Fix ability to make multiple boxes


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


# noinspection PyAttributeOutsideInit
class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.left_frame = Frame(self.master)
        self.left_frame.pack(side=LEFT)
        self.right_frame = Frame(self.master)
        self.right_frame.pack(side=RIGHT)
        # TODO: ORGANIZE THIS
        self.menubar = Menu(self.master)
        self.load_button = Button(self.left_frame, text="Load", command=self.load_student)
        self.delete_button = Button(self.left_frame, text="Delete", command=self.delete_student_dialog)
        self.add_hours_button = Button(self.right_frame, text="Add Hours", command=self.add_hours_dialog)

        self.edit_button = Button(self.left_frame, text="Edit", command=self.edit_student_dialog)
        self.add_button = Button(self.left_frame, text="Add", command=self.add_student_dialog)
        self.listbox = Listbox(self.left_frame, selectmode=SINGLE)
        self.report_menu = Menu(self.menubar)

        backend.backup()

        self.current_student = None
        if self.current_student is None:
            self.current_student = backend.Student("None Selected", 12)
            self.current_student.student_id = None
            self.current_student.grade = None

        self.add_name_text = StringVar()
        self.add_grade_int = IntVar()
        self.add_csa_hours_flt = DoubleVar()

        self.edit_name_text = StringVar()
        self.edit_grade_int = IntVar()
        self.edit_csa_hours_flt = DoubleVar()
        self.add_hours_text = DoubleVar()

        self.student_name_label_text = StringVar()
        self.student_id_label_text = StringVar()
        self.student_grade_label_text = StringVar()
        self.student_csa_level_label_text = StringVar()
        self.student_csa_hours_label_text = StringVar()

        self.student_name_label_text.set(f"Student Name: {self.current_student.name}")
        self.student_name_label = Label(self.right_frame, textvariable=self.student_name_label_text)

        self.student_id_label_text.set(f"Student ID: {self.current_student.student_id}")
        self.student_id_label = Label(self.right_frame,
                                      textvariable=self.student_id_label_text)

        self.student_grade_label_text.set(f"Student Grade: {self.current_student.grade}")
        self.student_grade_label = Label(self.right_frame,
                                         textvariable=self.student_grade_label_text)

        self.student_csa_level_label_text.set(f"Student CSA Level: {self.current_student.csa_level}")
        self.student_csa_level_label = Label(self.right_frame,
                                             textvariable=self.student_csa_level_label_text)

        self.student_csa_hours_label_text.set(f"Student CSA Hours: {self.current_student.csa_hours}")
        self.student_csa_hours_label = Label(self.right_frame,
                                             textvariable=self.student_csa_hours_label_text)
        # TODO: Add fonts
        self.init_window()

    def init_window(self):
        self.master.title("FBLA Community Service Awards Tracking")
        self.pack(fill=BOTH, expand=1)

        self.report_menu.add_command(label="Export Program Report", command=self.program_report_wrapper)
        self.report_menu.add_command(label="Export Student Report", command=self.student_report_wrapper)
        self.menubar.add_cascade(label="Reports", menu=self.report_menu)

        self.menubar.add_command(label="Refresh", command=self.reload_ui)
        self.menubar.add_command(label="Restore Backup", command=self.restore_backup)
        self.master.config(menu=self.menubar)

        # self.listbox = Listbox(self.left_frame, height=50, width=100, selectmode=SINGLE)\
        self.listbox.grid(column=0, row=0, columnspan=4)
        self.listbox.insert(END, "a list entry")
        self.refresh_students_listbox()

        self.add_button.grid(column=0, row=1)

        self.edit_button.grid(column=1, row=1)

        self.load_button.grid(column=2, row=1)

        self.delete_button.grid(column=3, row=1)

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

        self.add_hours_button.grid(column=0, row=5)
        self.add_hours_button["state"] = DISABLED

    def refresh_students_listbox(self, sort_parameter=None, criteria=None):
        try:
            prev_sel = self.listbox.curselection()
        except IndexError:
            prev_sel = 0
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
        try:
            self.listbox.selection_set(prev_sel)
        except TclError:
            self.listbox.selection_set(0)

    def load_student(self):
        self.refresh_students_listbox()
        backend.graduate_csa_levels()
        try:
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
                self.add_hours_button["state"] = NORMAL
            else:
                print("Nope")
                self.student_name_label_text.set(f"Student Name: None Selected")
        except IndexError:
            return None

    def reload_ui(self):
        backend.graduate_csa_levels()
        self.load_student()
        self.refresh_students_listbox()

    # noinspection DuplicatedCode,DuplicatedCode
    def add_student_dialog(self):
        self.add_window = Toplevel()

        name_label = Label(self.add_window, text="Name")
        name_label.grid(column=0, row=0)
        self.add_name_text = StringVar()
        name_input = Entry(self.add_window, textvariable=self.add_name_text)
        name_input.grid(column=1, row=0)

        grade_label = Label(self.add_window, text="Grade")
        grade_label.grid(column=0, row=1)
        self.add_grade_int = IntVar()
        grades = {9, 10, 11, 12}
        grade_input = OptionMenu(self.add_window, self.add_grade_int, *grades)
        self.add_grade_int.set(9)
        grade_input.grid(column=1, row=1)

        csa_hours_label = Label(self.add_window, text="CSA Hours")
        csa_hours_label.grid(column=0, row=2)
        self.add_csa_hours_flt = DoubleVar()
        self.add_csa_hours_flt.set(0)
        csa_hours_input = Entry(self.add_window, textvariable=self.add_csa_hours_flt)
        csa_hours_input.grid(column=1, row=2)

        add_button = Button(self.add_window, text="Add Student", command=self.add_student_wrapper)
        add_button.grid(column=0, row=5)

    def add_student_wrapper(self):
        try:
            print(self.add_name_text.get())
            print(backend.duplicate_check(self.add_name_text.get()))
            if self.add_name_text.get() == "":
                messagebox.showerror(title="Error", message="Name is required.")
                self.add_window.destroy()

            elif backend.duplicate_check(self.add_name_text.get()) is True:
                messagebox.showerror(title="Error", message="Name is already in database. Please use last names.")
                self.add_window.destroy()

            else:
                student = backend.Student(name=self.add_name_text.get(),
                                          grade=self.add_grade_int.get(),
                                          csa_hours=self.add_csa_hours_flt.get())
                backend.add_student(student)
                self.add_window.destroy()
                self.reload_ui()
        except TclError:
            messagebox.showerror(title="Error", message=f"Invalid input for CSA Hours, input must be number")
            self.add_window.destroy()
            encountered_error = True
            self.reload_ui()

    # noinspection DuplicatedCode,DuplicatedCode
    def edit_student_dialog(self):
        current_student = self.listbox.get(self.listbox.curselection())

        self.current_student = backend.search_table(current_student)

        self.edit_window = Toplevel()
        name_label = Label(self.edit_window, text="Name")
        name_label.grid(column=0, row=0)
        name_input = Entry(self.edit_window, textvariable=self.edit_name_text)
        self.edit_name_text.set(self.current_student.name)
        name_input.grid(column=1, row=0)

        grade_label = Label(self.edit_window, text="Grade")
        grade_label.grid(column=0, row=1)
        grades = {9, 10, 11, 12}
        grade_input = OptionMenu(self.edit_window, self.edit_grade_int, *grades)
        self.edit_grade_int.set(self.current_student.grade)
        grade_input.grid(column=1, row=1)

        csa_hours_label = Label(self.edit_window, text="CSA Hours")
        csa_hours_label.grid(column=0, row=2)
        self.edit_csa_hours_flt.set(self.current_student.csa_hours)
        csa_hours_input = Entry(self.edit_window, textvariable=self.edit_csa_hours_flt)
        csa_hours_input.grid(column=1, row=2)

        edit_button = Button(self.edit_window, text="Edit Student", command=self.edit_student_wrapper)
        edit_button.grid(column=0, row=5)

    def edit_student_wrapper(self):
        # TODO: Add duplicate checking to this
        try:
            print(self.edit_name_text.get())
            student = backend.Student(name=self.edit_name_text.get(),
                                      grade=self.edit_grade_int.get(),
                                      csa_hours=self.edit_csa_hours_flt.get())
            print(student.name)
            backend.edit_student(self.current_student, data_write=student)
            self.edit_window.destroy()
            self.refresh_students_listbox()
            self.reload_ui()
        except TclError:
            messagebox.showerror(title="Error", message=f"Invalid input for CSA Hours, input must be number")
            self.edit_window.destroy()
            self.reload_ui()

    def delete_student_dialog(self):
        current_student = self.listbox.get(self.listbox.curselection())

        self.current_student = backend.search_table(current_student)

        delete_student_window = messagebox.askyesno(title="Delete", message="Are you sure you want to delete?")
        print(delete_student_window)
        if delete_student_window is True:
            backend.delete_student(self.current_student)
            self.reload_ui()

    def student_report_wrapper(self):
        current_student = self.listbox.get(self.listbox.curselection())

        self.current_student = backend.search_table(current_student)

        backend.generate_student_report(self.current_student)

        messagebox.showinfo(title="Report Generated", message="Your report has been generated.")

    @staticmethod
    def program_report_wrapper():
        backend.generate_program_report()

        messagebox.showinfo(title="Report Generated", message="Your report has been generated.")

    def add_hours_dialog(self):
        current_student = self.listbox.get(self.listbox.curselection())

        self.current_student = backend.search_table(current_student)

        self.add_hours_window = Toplevel()
        add_hours_label = Label(self.add_hours_window, text="Hours to Add:")
        add_hours_label.grid(column=0, row=0)

        add_hours_entry = Entry(self.add_hours_window, textvariable=self.add_hours_text)
        add_hours_entry.grid(column=1, row=0)

        add_hours_button = Button(self.add_hours_window, text="Add", command=self.add_hours_wrapper)
        add_hours_button.grid(column=0, row=1)

    def add_hours_wrapper(self):
        # current_student = self.listbox.get(self.listbox.curselection())

        # self.current_student = backend.search_table(current_student) # TODO: look into making this a function
        try:
            backend.math_csa_hours(self.current_student, self.add_hours_text.get())
            self.add_hours_window.destroy()
            self.reload_ui()
        except TclError:
            messagebox.showerror(title="Error", message=f"Invalid input for CSA Hours, input must be number")
            self.add_hours_window.destroy()
            self.reload_ui()

    def restore_backup(self):
        file = filedialog.askopenfile(initialdir=os.getcwd(), title="Select file",
                                      filetypes=[("database files", "*.db")])
        try:
            file_path = file.name
            backend.restore(file_path)
            self.reload_ui()
        except AttributeError:
            return None


# TODO: Add filter, keep working on listbox function, then add info area on right side

# root.state("zoomed")


root.resizable(0, 0)
app = Window(root)
root.mainloop()
