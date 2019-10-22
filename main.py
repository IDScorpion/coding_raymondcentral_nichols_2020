#TODO: write code
import sqlite3 as lite
from os import path, mkdir
import dataset

class Student:
    def __init__(self,student_id,name,grade,csa_level):
        self.student_id = student_id
        self.name = name
        self.grade = grade
        self.csa_level = csa_level

def create_file(name):
    with open(name, "w+"):
        print('File', name, 'created.')

def setup():
    if path.exists(r"data") is False:
        mkdir(r"data")
    if path.exists(r"data\Students.db") is False:
        db_location = r"data\Students.db"
        create_file(db_location)
        db = dataset.connect('sqlite:///' + db_location)
        table = db['Students']
        db.commit()

def return_table():
    db_location = r"data\Students.db"
    db = dataset.connect('sqlite:///' + db_location)
    table = db['Students']
    return table

def get_query_type(query):
    try:
        int(str(query))
        if len(str(query)) == 8:
            query_type = 'id'
        else:
            query_type = 'grade'
    except ValueError:
        if query.lower() in ('community','service','achievement'):
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
        return student_list

    elif query_type == 'grade':
        table = return_table()
        student = table.find(grade=query)
        student_list = []
        for row in student:
            student_list.append(dict(row))
        return student_list

    elif query_type == 'csa_level':
        table = return_table()
        student = table.find(csa_level=query)
        student_list = []
        for row in student:
            student_list.append(dict(row))
        return student_list

    elif query_type == 'name':
        table = return_table()
        student = table.find(name=query)
        student_list = []
        for row in student:
            student_list.append(dict(row))
        return student_list






def add_student(student): # assumes student object
    student_dict = vars(student)
    table = return_table()
    table.insert(student_dict)

def edit_student(student): # assumes student object from search
    pass

newStudent = Student(12345678,'JimmyJon',10,'Community')

# add_student(newStudent)

search_table(10) # grade
search_table('Community') # csa
search_table('JimmyJon') # name
search_table(12345678) # id


print(newStudent.grade)