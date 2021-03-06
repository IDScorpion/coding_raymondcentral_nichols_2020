import datetime  # Used in various file names
import os  # Used in creation and deletion of files and directories
import random  # Used in the creation of random ids
import shutil  # Used in backup and restore

import dataset  # Provides database
import jinja2  # Used to interpret HTML template and fill data
import pdfkit  # Creates PDF reports from HTML output by jinja2. Packaged within the project.


class Student:  # defines what makes a student
    def __init__(self, name, grade, student_id=None, csa_level=None, csa_hours=0):
        if student_id is None:
            self.student_id = create_ids(name)
        else:
            self.student_id = student_id
        self.name = name
        self.grade = grade
        if csa_level is None:
            self.csa_level = 'None'
        else:
            self.csa_level = csa_level
        self.csa_hours = csa_hours

    def __call__(self):  # makes the function callable
        pass


csa_levels_names = ['None', 'Community', 'Service', 'Achievement']

csa_levels_hours = {
    'None': 0,
    'Community': 50,
    'Service': 200,
    'Achievement': 500
}


def create_ids(name):  # creates randomized 8 digit ids
    table = return_table()
    possible_id = random.randint(10000000, 99999999)  # 8 digit number gen
    name_check = table.find(name=name)  # Checks if name is in database
    student_list = []  # Creates student list
    for row in name_check:
        student_list.append(dict(row))  # Appends each row from name_check
    if student_list:  # If student_list is truthy(has a value), gets the ID from it and returns it
        final_id = student_list[0]['student_id']
        return final_id
    elif not student_list:  # Continues with id generation if student_list is falsy
        id_check = table.find(student_id=possible_id)  # Checks to make sure ID is unique
        student_list = []
        for row in id_check:
            student_list.append(dict(row))
        if student_list:
            create_ids(name)  # Tries again if ID isn't unique
        elif not student_list:  # If the ID is unique, returns ID
            return possible_id


def create_file(name):  # acts as simple way to create files
    with open(name, "w+"):
        return True


def get_date():  # Date is used commonly throughout the program
    d = datetime.datetime.now()
    date_now = d.strftime("%d-%B-%Y")

    return date_now

def backup(save_location=None):  # Copies current database in data to the backups folder
    if save_location is None:
        shutil.copyfile(r'data\Students.db', r'backups\Students({}).db'.format(get_date()))
    else:
        shutil.copyfile(r'data\Students.db', save_location)


def restore(restore_file):  # Restores the chosen backup
    shutil.copyfile(restore_file, r'data\Students.db')


def setup():  # first time setup
    if os.path.exists(r'data') is False:
        os.mkdir(r'data')
    if os.path.exists(r'reports') is False:
        os.mkdir(r'reports')
    if os.path.exists(r'backups') is False:
        os.mkdir(r'backups')
    if os.path.exists(r"data\Students.db") is False:
        db_location = r"data\Students.db"
        create_file(db_location)  # creates file
    graduate_csa_levels()  # Used so on every run the CSA levels are updated
    backup()


config = pdfkit.configuration(wkhtmltopdf=r'wkhtmltox\bin\wkhtmltopdf.exe')  # WKHTMLtoPDF is a dependency of PDFkit


def return_table():  # Returns the Students table
    db_location = r"data\Students.db"
    db = dataset.connect('sqlite:///' + db_location)
    table = db['Students']
    return table


def get_query_type(query):  # Interprets query type (ID, Grade, CSA Level, Name, or Student obj.)
    try:
        int(str(query))
        if len(str(query)) == 8:
            query_type = 'id'
        else:
            query_type = 'grade'
    except ValueError:
        if callable(query):  # Checks to see if query is a Student object; these need special treatment
            query_type = 'student object'
        elif query.lower() in ('none', 'community', 'service', 'achievement'):
            query_type = 'csa_level'
        else:
            query_type = 'name'

    return query_type


def search_table(query):  # Searches table and creates a Student object with result, or returns None if no results.
    query_type = get_query_type(query)  # Gets the type of query so we know what column to look in
    if query_type == 'id':
        table = return_table()
        student = table.find(student_id=query)
        student_list = []
        for row in student:
            student_list.append(dict(row))

    elif query_type == 'grade':
        table = return_table()
        student = table.find(grade=query)
        student_list = []
        for row in student:
            student_list.append(dict(row))

    elif query_type == 'csa_level':
        table = return_table()
        student = table.find(csa_level=query)
        student_list = []
        for row in student:
            student_list.append(dict(row))

    elif query_type == 'name':
        table = return_table()
        student = table.find(name=query)
        student_list = []
        for row in student:
            student_list.append(dict(row))

    elif query_type == 'student object':  # Similar to if ID
        table = return_table()
        student = table.find(student_id=query.student_id)
        student_list = []
        for row in student:
            student_list.append(dict(row))

    try:
        student_list[0].pop('id')  # Gets rid of database ID number, not needed in student object
        student = build_student(student_list[0])
        return student
    except IndexError:
        return None


def build_student(student_data):  # builds a student from data list or dict
    if isinstance(student_data, dict):
        student = Student(student_data['name'],
                          student_data['grade'],
                          student_data["student_id"],
                          student_data["csa_level"],
                          student_data['csa_hours']
                          )
        return student
    elif isinstance(student_data, list):
        student = Student(student_data[0]['name'],
                          student_data[0]['grade'],
                          student_data[0]["student_id"],
                          student_data[0]["csa_level"],
                          student_data[0]['csa_hours'])
        return student


def add_student(student):  # Adds student to table. Can accept Student object or dictionary.
    if isinstance(student, Student):
        student_dict = vars(student)
        table = return_table()
        table.insert(student_dict)

    elif isinstance(student, dict):
        student_dict = student
        table = return_table()
        table.insert(student_dict)


def edit_student(student, data_write=None, key=None, new_value=None):
    """Edits students within the database. Data can be presented as a dictionary or student, overwriting all using
    data_write, or can modify one key using key and new_value parameters"""
    if data_write is None:
        if isinstance(student, Student):
            student_dict = vars(student)
            student_dict[key] = new_value
            table = return_table()
            table.update(student_dict, ['student_id'])

        elif isinstance(student, dict):
            student_dict = student
            student_dict[key] = new_value
            table = return_table()
            table.update(student_dict, ['student_id'])
    else:
        if isinstance(data_write, Student):
            new_student = vars(data_write)
        table = return_table()
        table.update(new_student, ['student_id'])


def delete_student(student):  # Searches the database for a student and deletes them.
    search = search_table(student)
    table = return_table()
    table.delete(student_id=search.student_id)


def math_csa_hours(student, hours):  # Searches the database and performs arithmetic on csa hours.
    table = return_table()
    student = search_table(student)
    try:
        student.csa_hours += hours
        student_dict = vars(student)
        table.update(student_dict, ['student_id'])
    except AttributeError:  # Returns None if student  is not found
        return None


def edit_csa_hours(student, edit_value):  # Searches the database and directly edits CSA value to parameter edit_value.
    table = return_table()
    student = search_table(student)
    try:
        student.csa_hours = edit_value
        student_dict = vars(student)
        table.update(student_dict, ['student_id'])
    except AttributeError:  # Returns None if ID is not found
        return None


def graduate_csa_levels():  # Checks the database for anyone who has obtained a new level of the CSA.
    table = return_table()
    student_list = []
    for row in table:
        student_list.append(dict(row))
    for item in student_list:
        if 50 <= item['csa_hours'] < 200:
            edit_student(item, key='csa_level', new_value='Community')
        elif 200 <= item['csa_hours'] < 500:
            edit_student(item, key='csa_level', new_value='Service')
        elif 500 <= item['csa_hours']:
            edit_student(item, key='csa_level', new_value='Achievement')
        elif 0 <= item['csa_hours'] < 50:
            edit_student(item, key='csa_level', new_value='None')


def generate_student_report(student):  # Generates a student report using the templates in /templates
    graduate_csa_levels()
    student = search_table(student)
    try:
        next_level = csa_levels_names[csa_levels_names.index(student.csa_level) + 1]
    except IndexError:
        next_level = "Finished!"
    if next_level != "Finished!":
        rem_hours = csa_levels_hours[next_level] - student.csa_hours
    else:
        rem_hours = 0
    if rem_hours <= 0:
        rem_hours = 0
    template_loader = jinja2.FileSystemLoader(searchpath="templates\\")  # Loads the HTML template
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "student_template_v2.html"
    template = template_env.get_template(template_file)
    html_report = template.render(name=student.name,  # Renders the template as HTML
                                  grade=student.grade,
                                  student_id=student.student_id,
                                  csa_hours=student.csa_hours,
                                  csa_level=student.csa_level,
                                  rem_hours=rem_hours)
    with open(r'reports\temp_html_report.html', 'w+') as html:
        html.write(html_report)  # Writes HTML to a temp file
    date_now = get_date()
    css = [r'templates/css/idGeneratedStyles.css']  # Links to the default CSS
    options = {
        'quiet': ''  # Supresses PDFKit output.
    }
    pdfkit.from_file(r"reports\temp_html_report.html",
                     r'reports/{}_Student_Report_{}.pdf'.format(str(student.name).strip(), date_now),
                     configuration=config,  # Links to local wkhtmltox install.
                     css=css, options=options)
    os.remove(r'reports\temp_html_report.html')  # Gets rid of the temp html file.


def generate_program_report():  # Generates a general report of the program, similar to generate_student_report.
    graduate_csa_levels()
    table = return_table()
    students = []
    for row in table:
        students.append(dict(row))
    total_students_enrolled = len(students)
    total_overall_hours = 0

    total_students = {
        'None': 0,
        'Community': 0,
        'Service': 0,
        'Achievement': 0
    }
    total_hours = {
        'None': 0,
        'Community': 0,
        'Service': 0,
        'Achievement': 0
    }
    total_hours_above = {
        'None': 0,
        'Community': 0,
        'Service': 0,
        'Achievement': 0
    }

    for student in students:
        total_overall_hours += student['csa_hours']
        total_students[(student['csa_level'])] += 1
        total_hours[student['csa_level']] += student['csa_hours']
        total_hours_above[student['csa_level']] += student['csa_hours'] - csa_levels_hours[student['csa_level']]

    template_loader = jinja2.FileSystemLoader(searchpath="templates\\")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "program_template_v2.html"
    template = template_env.get_template(template_file)
    html_report = template.render(total_students_enrolled=total_students_enrolled,
                                  total_overall_hours=total_overall_hours,

                                  total_students_none=total_students['None'],
                                  total_students_community=total_students['Community'],
                                  total_students_service=total_students['Service'],
                                  total_students_achievement=total_students['Achievement'],

                                  total_hours_none=total_hours['None'],
                                  total_hours_community=total_hours['Community'],
                                  total_hours_service=total_hours['Service'],
                                  total_hours_achievement=total_hours['Achievement'],

                                  total_hours_above_none=total_hours_above['None'],
                                  total_hours_above_community=total_hours_above['Community'],
                                  total_hours_above_service=total_hours_above['Service'],
                                  total_hours_above_achievement=total_hours_above['Achievement']
                                  )
    with open(r'reports\temp_html_report.html', 'w+') as html:
        html.write(html_report)
    date_now = get_date()
    css = [r'templates/css/idGeneratedStyles.css']
    options = {
        'quiet': ''
    }
    pdfkit.from_file(r'reports\temp_html_report.html',
                     r'reports/Program_Report_{}.pdf'.format(date_now),
                     configuration=config,
                     css=css, options=options)
    os.remove(r'reports\temp_html_report.html')


def return_student_list(sort_parameter=None, criteria=None):  # Returns students as a list of dictionaries.
    table = return_table()
    students = []
    for row in table:
        if sort_parameter is None or criteria is None:
            students.append(dict(row))
        else:
            if dict(row)[sort_parameter] == criteria:
                students.append(dict(row))
    if students:
        return students
    else:
        return None


def duplicate_check(name):  # Checks the table for duplicate names.
    table = return_table()
    students = []
    for row in table:
        students.append(dict(row)["name"])
    students.append(name)
    if students.count(name) > 1:
        return True
    else:
        return False
