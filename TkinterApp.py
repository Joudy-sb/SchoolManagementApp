from tkinter import Tk, ttk
from TkinterTabs import StudentTab  
from TkinterTabs import InstructorTab  
from TkinterTabs import CourseTab  
from TkinterTabs import ViewAllTab  
from TkinterTabs import RegisterTab  
import sqlite3

# THIS FUNCTIONS CREATE THE SQLite DATABASE USED IN OUR SCHOOL MANAGEMENT SYSTEM
def initialize_database():
    """
    Initializes the SQLite database for the School Management System.

    This function creates four tables in the database:
    - students: Stores information about students, including their name, age, email, and studentID.
    - instructors: Stores information about instructors, including their name, age, email, and instructorID.
    - courses: Stores information about courses, including courseID, courseName, and instructor.
    - registrations: Stores the registration details of students in various courses.

    The function also checks whether the tables exist before creating them.
    """
    
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # create ctudents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT UNIQUE,
            studentID INTEGER UNIQUE
        )
    ''')
    # create cnstructors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS instructors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT UNIQUE,
            instructorID INTEGER UNIQUE
        )
    ''')
    # create courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            courseID INTEGER UNIQUE,
            courseName TEXT NOT NULL,
            instructor TEXT
        )
    ''')
    # create registrations 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            studentEmail TEXT,
            courseID INTEGER NULL,
            FOREIGN KEY (studentEmail) REFERENCES students(email),
            FOREIGN KEY (courseID) REFERENCES courses(courseID)
        )
    ''')
    conn.commit()
    conn.close()
initialize_database()

# create the main window
root = Tk()
root.title("School Management System")
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, padx=20, pady=20)

# create the different tabs
StudentTab.create_student_tab(notebook)
InstructorTab.create_instructor_tab(notebook)
CourseTab.create_course_tab(notebook)
RegisterTab.create_register_tab(notebook)
ViewAllTab.create_viewall_tab(notebook)

# run the application
root.mainloop()