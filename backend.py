# TODO: write code
# TODO: Add backup and restore, comments

from os import path, mkdir
import dataset


class Student:  # defines what makes a student
    def __init__(self, student_id, name, grade, csa_level, csa_hours = 0):
        self.student_id = student_id
        self.name = name
        self.grade = grade
        self.csa_level = csa_level
        self.csa_hours = csa_hours

    def __call__(self):
        pass


def create_file(name):  # acts as simple way to create files
    with open(name, "w+"):
        print('File', name, 'created.')


def setup():  # first time setup
    if path.exists(r"data") is False:
        mkdir(r"data")  # makes data directory
    if path.exists(r"data\Students.db") is False:
        db_location = r"data\Students.db"
        create_file(db_location)


def return_table():  # Returns the Students table
    db_location = r"data\Students.db"
    db = dataset.connect('sqlite:///' + db_location)
    table = db['Students']
    return table


def get_query_type(query): # Interprets the query type (ID, Grade, CSA Level, Name, or Student obj.) TODO: Add CSA HOURS
    try:
        int(str(query))
        if len(str(query)) == 8:
            query_type = 'id'
        else:
            query_type = 'grade'
    except ValueError:
        if callable(query):
            query_type = 'student object'
        elif query.lower() in ('community','service','achievement'):
            query_type = 'csa_level'
        else:
            query_type = 'name'

    return query_type


def search_table(query):
    query_type = get_query_type(query)
    print(query_type)
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
            print(row)
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

    elif query_type == 'student object':
        print(query)
        table = return_table()
        student = table.find(student_id=query.student_id)
        student_list = []
        for row in student:
            student_list.append(dict(row))
        print(student_list)

    if len(student_list) >= 2:
        name_list = []
        for item in student_list:
            name_list.append(item['name'])
        student = input("Which student are you looking for? {} Type a number based on list position,"
                        " left to right, starting at 1: ".format(name_list))
        list_index = int(student) - 1
        print(student_list)
        print(list_index)
        student_list[list_index].pop('id')
        print(student_list[list_index])
        student = build_student(student_list[list_index])
        return student
    student_list[0].pop('id')
    student = build_student(student_list[0])
    return student


def build_student(student_data):  # builds a student from data list or dict
    if isinstance(student_data, dict):
        student = Student(student_data['student_id'], student_data['name'], student_data['grade'],
                          student_data['csa_level'], student_data['csa_hours'])
        print(student)
        return student
    elif isinstance(student_data,list):
        print(student_data)
        student = Student(student_data[0]['student_id'], student_data[0]['name'], student_data[0]['grade'],
                          student_data[0]['csa_level'], student_data[0]['csa_hours'])
        return student


def add_student(student):  # assumes student object
    if isinstance(student, Student):
        student_dict = vars(student)
        table = return_table()
        table.insert(student_dict)

    elif isinstance(student, dict):
        student_dict = student
        table = return_table()
        table.insert(student_dict)


def edit_student(student, key, new_value):  # assumes student object from search
    if isinstance(student, Student):
        student_dict = vars(student)
        student_dict[key] = new_value
        table = return_table()
        table.update(student_dict, ['student_id'])

    elif isinstance(student, dict):
        student_dict = student
        student_dict[key] = new_value
        table = return_table()
        table.update(student_dict, [key])


def math_csa_hours(student, hours):  # assumes student object
    table = return_table()
    student = search_table(student)
    print(student)
    student.csa_hours += hours
    student_dict = vars(student)
    table.update(student_dict, ['student_id'])


def edit_csa_hours(student, edit_value):  # assumes student object
    table = return_table()
    student = search_table(student)
    print(student)
    student.csa_hours = edit_value
    student_dict = vars(student)
    table.update(student_dict, ['student_id'])


def graduate_csa_levels():
    table = return_table()
    student_list = []
    for row in table:
        student_list.append(dict(row))
    for item in student_list:
        if 0 <= item['csa_hours'] < 50:
            edit_student(item, 'csa_level', 'Community')
        if 50 <= item['csa_hours'] < 200:
            edit_student(item, 'csa_level', 'Service')
        if 0 <= item['csa_hours'] < 500:
            edit_student(item, 'csa_level', 'Ach')


newStudent = Student(12345678, 'JimmyJon', 10, 'Community', 10)

student2 = Student(12345679, 'JimmyJoe', 10, 'Service', 0)


graduate_csa_levels()
# TODO: CSA HOURS IMPLEMENT
