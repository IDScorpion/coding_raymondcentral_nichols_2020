import os  # Manages os level interactions
from tkinter import *  # Tkinter imports for GUI
from tkinter import messagebox, filedialog

import backend  # Imports the backend functionality

if os.path.exists(r"data") is False:
    backend.setup()  # Checks to see if the data folder exists, if it doesn't we need to run setup

root = Tk()


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master = master  # Sets the master
        self.master.title("FBLA Community Service Awards Tracking")
        self.pack(fill=BOTH, expand=1)

        self.left_frame = Frame(self.master)  # Creates frames to separate the left objects from right.
        self.left_frame.pack(side=LEFT)
        self.right_frame = Frame(self.master)
        self.right_frame.pack(side=RIGHT)

        # Creates a Student object to use if none is selected
        self.current_student = None
        if self.current_student is None:
            self.current_student = backend.Student("None Selected", 12)
            self.current_student.student_id = None
            self.current_student.grade = None

        # Sets the variables to be used later in dialog boxes.
        self.add_name_text = StringVar()
        self.add_grade_int = IntVar()
        self.add_csa_hours_flt = DoubleVar()

        self.edit_name_text = StringVar()
        self.edit_grade_int = IntVar()
        self.edit_csa_hours_flt = DoubleVar()
        self.add_hours_text = DoubleVar()

        self.student_name_label_text = StringVar()
        self.student_id_label_text = IntVar()
        self.student_grade_label_text = IntVar()
        self.student_csa_level_label_text = StringVar()
        self.student_csa_hours_label_text = DoubleVar()

        # Sets the default values for variables
        self.student_name_label_text.set(f"Student Name: {self.current_student.name}")
        self.student_id_label_text.set(f"Student ID: {self.current_student.student_id}")
        self.student_grade_label_text.set(f"Student Grade: {self.current_student.grade}")
        self.student_csa_level_label_text.set(f"Student CSA Level: {self.current_student.csa_level}")
        self.student_csa_hours_label_text.set(f"Student CSA Hours: {self.current_student.csa_hours}")

        # Creates the menubar.
        self.menubar = Menu(self.master)

        # Creates the left frame objects
        self.load_button = Button(self.left_frame, text="Load", command=self.load_student)
        self.delete_button = Button(self.left_frame, text="Delete", command=self.delete_student_dialog)
        self.edit_button = Button(self.left_frame, text="Edit", command=self.edit_student_dialog)
        self.add_button = Button(self.left_frame, text="Add", command=self.add_student_dialog)

        self.listbox = Listbox(self.left_frame, selectmode=SINGLE)
        self.refresh_students_listbox()

        # Grids the left frame objects
        self.add_button.grid(column=0, row=1)
        self.edit_button.grid(column=1, row=1)
        self.load_button.grid(column=2, row=1)
        self.delete_button.grid(column=3, row=1)
        self.listbox.grid(column=0, row=0, columnspan=4)

        # Creates the right frame objects
        self.student_name_label = Label(self.right_frame, textvariable=self.student_name_label_text)
        self.student_id_label = Label(self.right_frame, textvariable=self.student_id_label_text)
        self.student_grade_label = Label(self.right_frame, textvariable=self.student_grade_label_text)
        self.student_csa_level_label = Label(self.right_frame, textvariable=self.student_csa_level_label_text)
        self.student_csa_hours_label = Label(self.right_frame, textvariable=self.student_csa_hours_label_text)
        self.add_hours_button = Button(self.right_frame, text="Add Hours", command=self.add_hours_dialog)

        # Grids the right frame objects
        self.student_name_label.grid(column=0, row=0)
        self.student_id_label.grid(column=0, row=1)
        self.student_grade_label.grid(column=0, row=2)
        self.student_csa_level_label.grid(column=0, row=3)
        self.student_csa_hours_label.grid(column=0, row=4)

        self.add_hours_button.grid(column=0, row=5)

        # Adds commands to the menubar.
        self.report_menu = Menu(self.menubar)
        self.report_menu.add_command(label="Export Program Report", command=self.program_report_wrapper)
        self.report_menu.add_command(label="Export Student Report", command=self.student_report_wrapper)
        self.report_menu.add_command(label="Export Student Report (All)",
                                     command=lambda: self.student_report_wrapper(
                                         student_list=backend.return_student_list()
                                        )
                                     )
        self.menubar.add_cascade(label="Reports", menu=self.report_menu)

        self.menubar.add_command(label="Refresh", command=self.reload_ui)

        self.menubar.add_command(label="Restore Backup", command=self.restore_backup)

        self.master.config(menu=self.menubar)

        # Creates a backup of the database
        backend.backup()

        # Sets the Add Hours button to disable, since no one is selected.
        self.add_hours_button["state"] = DISABLED

    def refresh_students_listbox(self, sort_parameter=None, criteria=None):  # Refreshes the listbox
        try:
            prev_sel = self.listbox.curselection()  # Trys to restore past selection, defaulting to top item
        except IndexError:
            prev_sel = 0
        students = backend.return_student_list(sort_parameter, criteria)  # Gets the list of all students
        if students is None:
            student_names = ["No data found."]  # Displays if no students are found.
        else:
            student_names = []
            for student in students:
                student_names.append(student["name"])
        self.listbox.delete(0, END)  # Gets rid of the placeholder item
        for name in student_names:
            self.listbox.insert(END, name)
        try:
            self.listbox.selection_set(prev_sel)
        except TclError:
            self.listbox.selection_set(0)

    def load_student(self):
        self.refresh_students_listbox()  # Refreshes the listbox for tidiness
        backend.graduate_csa_levels()  # Makes sure the CSA level is accurate
        try:
            temp_student = self.listbox.get(self.listbox.curselection()[0])  # Gets what student is currently selected
            if temp_student:
                self.current_student = backend.search_table(temp_student)  # Searches for student
                # Updates all labels accordingly
                self.student_name_label_text.set(f"Student Name: {self.current_student.name}")
                self.student_id_label_text.set(f"Student ID: {self.current_student.student_id}")
                self.student_grade_label_text.set(f"Student Grade: {self.current_student.grade}")
                self.student_csa_level_label_text.set(f"Student CSA Level: {self.current_student.csa_level}")
                self.student_csa_hours_label_text.set(f"Student CSA Hours: {self.current_student.csa_hours}")
                # Sets the add hours button to normal, since a student is loaded.
                self.add_hours_button["state"] = NORMAL
            else:
                self.student_name_label_text.set(f"Student Name: None Selected")
        except IndexError:
            return None

    def disable_buttons(self):  # Disables all left frame buttons. Inverse of enable_buttons()
        self.add_button["state"] = DISABLED
        self.edit_button["state"] = DISABLED
        self.load_button["state"] = DISABLED
        self.delete_button["state"] = DISABLED

    def enable_buttons(self):  # Enables all left frame buttons. Inverse of disable_buttons()
        self.add_button["state"] = NORMAL
        self.edit_button["state"] = NORMAL
        self.load_button["state"] = NORMAL
        self.delete_button["state"] = NORMAL

    def purge_menus(self):  # Purges all of the menu boxes
        try:
            self.add_window.destroy()
            try:
                self.edit_window.destroy()
            except AttributeError:
                return None
        except AttributeError:
            try:
                self.edit_window.destroy()
            except AttributeError:
                return None

    def reload_ui(self):  # Runs every UI refresh
        backend.graduate_csa_levels()
        try:
            self.load_student()
        except AttributeError:
            self.listbox.selection_set(0)
        self.refresh_students_listbox()
        self.enable_buttons()
        self.purge_menus()

    def add_student_dialog(self):  # Creates the dialog for adding students
        self.add_window = Toplevel()
        self.add_window.protocol("WM_DELETE_WINDOW", self.reload_ui)  # Sets exit behavior
        self.disable_buttons()  # Disables the left frame buttons so multiple boxes aren't able to display

        name_label = Label(self.add_window, text="Name")
        name_label.grid(column=0, row=0)
        name_input = Entry(self.add_window, textvariable=self.add_name_text)
        name_input.grid(column=1, row=0)

        grades = {9, 10, 11, 12}

        grade_label = Label(self.add_window, text="Grade")
        grade_label.grid(column=0, row=1)
        grade_input = OptionMenu(self.add_window, self.add_grade_int, *grades)
        self.add_grade_int.set(9)
        grade_input.grid(column=1, row=1)

        csa_hours_label = Label(self.add_window, text="CSA Hours")
        csa_hours_label.grid(column=0, row=2)
        self.add_csa_hours_flt.set(0)
        csa_hours_input = Entry(self.add_window, textvariable=self.add_csa_hours_flt)
        csa_hours_input.grid(column=1, row=2)

        add_button = Button(self.add_window, text="Add Student", command=self.add_student_wrapper)
        add_button.grid(column=0, row=5)

    def add_student_wrapper(self):  # Acts as the bridge between the UI and the backend.
        try:
            if self.add_name_text.get() == "":
                messagebox.showerror(title="Error", message="Name is required.")  # Names are required
                self.add_window.destroy()
                self.reload_ui()

            elif backend.duplicate_check(self.add_name_text.get()) is True:  # Names must be unique
                messagebox.showerror(title="Error", message="Name is already in database. Please use last names.")
                self.add_window.destroy()
                self.reload_ui()

            else: # Builds a Student object and sends it to the backend
                student = backend.Student(name=self.add_name_text.get(),
                                          grade=self.add_grade_int.get(),
                                          csa_hours=self.add_csa_hours_flt.get())
                backend.add_student(student)
                self.add_window.destroy()
                self.reload_ui()
        except TclError:  # Produced when non number is entered for CSA hours
            messagebox.showerror(title="Error", message=f"Invalid input for CSA Hours, input must be number")
            self.add_window.destroy()
            self.reload_ui()

    def edit_student_dialog(self): # Similar to add_student. except it pulls data to populate the box
        current_student = self.listbox.get(self.listbox.curselection())

        self.current_student = backend.search_table(current_student)

        self.edit_window = Toplevel()
        self.disable_buttons()
        self.edit_window.protocol("WM_DELETE_WINDOW", self.reload_ui)

        name_label = Label(self.edit_window, text="Name")
        name_label.grid(column=0, row=0)
        name_input = Entry(self.edit_window, textvariable=self.edit_name_text)
        self.edit_name_text.set(self.current_student.name)
        name_input.grid(column=1, row=0)

        grades = {9, 10, 11, 12}

        grade_label = Label(self.edit_window, text="Grade")
        grade_label.grid(column=0, row=1)
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

    def edit_student_wrapper(self): # Similar to add_student, but makes sure the IDs match when editing
        try:
            if backend.duplicate_check(self.edit_name_text.get()) is True and \
                    backend.search_table(self.edit_name_text.get()).student_id != self.current_student.student_id:
                messagebox.showerror(title="Error", message="Name is already in database.")
                self.edit_window.destroy()
                self.reload_ui()
            else:
                student = backend.Student(name=self.edit_name_text.get(),
                                          student_id=self.current_student.student_id,
                                          grade=self.edit_grade_int.get(),
                                          csa_hours=self.edit_csa_hours_flt.get())
                backend.edit_student(self.current_student, data_write=student)
                self.edit_window.destroy()
                self.refresh_students_listbox()
                self.reload_ui()
        except TclError:
            messagebox.showerror(title="Error", message=f"Invalid input for CSA Hours, input must be number")
            self.edit_window.destroy()
            self.reload_ui()

    def delete_student_dialog(self):  # Provides confirmation for deletion
        current_student = self.listbox.get(self.listbox.curselection())

        self.current_student = backend.search_table(current_student)
        self.disable_buttons()
        delete_student_window = messagebox.askyesno(title="Delete", message="Are you sure you want to delete?")
        if delete_student_window is True:
            backend.delete_student(self.current_student)
        self.reload_ui()

    def student_report_wrapper(self, student_list=None):  # Generates student reports
        if student_list is None:
            current_student = self.listbox.get(self.listbox.curselection())

            self.current_student = backend.search_table(current_student)

            backend.generate_student_report(self.current_student)

            messagebox.showinfo(title="Report Generated", message="Your report has been generated.")
        elif isinstance(student_list, list):
            for student in student_list:
                self.current_student = backend.search_table(student["name"])
                backend.generate_student_report(self.current_student)
            messagebox.showinfo(title="Reports Generated", message="Your reports have been generated.")


    def program_report_wrapper(self):  # Generates program reports
        backend.generate_program_report()

        messagebox.showinfo(title="Report Generated", message="Your report has been generated.")

    def add_hours_dialog(self): # Builds the add hours dialog
        current_student = self.listbox.get(self.listbox.curselection())

        self.current_student = backend.search_table(current_student)

        self.add_hours_window = Toplevel()
        add_hours_label = Label(self.add_hours_window, text="Hours to Add:")
        add_hours_label.grid(column=0, row=0)

        add_hours_entry = Entry(self.add_hours_window, textvariable=self.add_hours_text)
        add_hours_entry.grid(column=1, row=0)

        add_hours_button = Button(self.add_hours_window, text="Add", command=self.add_hours_wrapper)
        add_hours_button.grid(column=0, row=1)

    def add_hours_wrapper(self): # Provides connections to backend
        try:
            backend.math_csa_hours(self.current_student, self.add_hours_text.get())
            self.add_hours_window.destroy()
            self.reload_ui()
        except TclError:
            messagebox.showerror(title="Error", message=f"Invalid input for CSA Hours, input must be number")
            self.add_hours_window.destroy()
            self.reload_ui()

    def restore_backup(self):  # Provides ability to restore from backups by selecting file
        file = filedialog.askopenfile(initialdir=os.getcwd(), title="Select file",
                                      filetypes=[("database files", "*.db")])
        try:
            file_path = file.name
            backend.restore(file_path)
            self.reload_ui()
        except AttributeError:
            return None


root.resizable(0, 0)  # Makes the window a static size
app = Window(root)

root.mainloop()
