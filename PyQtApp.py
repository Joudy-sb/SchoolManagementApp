import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQtTabs.StudentTab import StudentTab
from PyQtTabs.InstructorTab import InstructorTab
from PyQtTabs.CourseTab import CourseTab
from PyQtTabs.RegisterTab import RegisterTab
from PyQtTabs.ViewAllTab import ViewAllTab

# Initialize the SQLite database
def initialize_database():
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Create students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT UNIQUE,
            studentID INTEGER UNIQUE
        )
    ''')

    # Create instructors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS instructors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT UNIQUE,
            instructorID INTEGER UNIQUE
        )
    ''')

    # Create courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            courseID INTEGER UNIQUE,
            courseName TEXT NOT NULL,
            instructor TEXT
        )
    ''')

    # Create registrations table
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

class SchoolManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 600)

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.init_tabs()

    def init_tabs(self):
        self.tab_widget.addTab(StudentTab(), "Students")
        self.tab_widget.addTab(InstructorTab(), "Instructors")
        self.tab_widget.addTab(CourseTab(), "Courses")
        self.tab_widget.addTab(RegisterTab(), "Register")
        self.tab_widget.addTab(ViewAllTab(), "View All")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchoolManagementSystem()
    window.show()
    sys.exit(app.exec_())
