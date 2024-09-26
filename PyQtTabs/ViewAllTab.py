import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem
)
from PyQt5.QtGui import QFont
from Classes.Course import Course
from Classes.Person import Student, Instructor


class ViewAllTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # Header label
        bold_font = QFont()
        bold_font.setPointSize(14)
        bold_font.setBold(True)

        course_label = QLabel("Database")
        course_label.setFont(bold_font)
        layout.addWidget(course_label)

        # Buttons for viewing students, instructors, and courses
        button_layout = QHBoxLayout()

        view_student_button = QPushButton("View Students")
        view_student_button.clicked.connect(lambda: self.view_students())
        button_layout.addWidget(view_student_button)

        view_instructor_button = QPushButton("View Instructors")
        view_instructor_button.clicked.connect(lambda: self.view_instructors())
        button_layout.addWidget(view_instructor_button)

        view_courses_button = QPushButton("View Courses")
        view_courses_button.clicked.connect(lambda: self.view_courses())
        button_layout.addWidget(view_courses_button)

        layout.addLayout(button_layout)

        # Initialize by showing students by default
        self.view_students()

    # Function to clear the layout before adding new content
    def clear_view(self):
        while self.layout().count():
            child = self.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # Function to view all instructors
    def view_instructors(self):
        self.clear_view()

        # Search layout
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_layout.addWidget(search_label)
        search_var = QLineEdit()
        search_layout.addWidget(search_var)
        self.layout().addLayout(search_layout)

        # Tree to display instructors
        tree = QTreeWidget()
        tree.setHeaderLabels(["Name", "Age", "Email", "Instructor ID", "Assigned Courses"])
        self.layout().addWidget(tree)

        def update_treeview(search_query):
            tree.clear()
            instructors = Instructor.load_from_db()
            courses = Course.load_from_db()
            for instructor in instructors:
                course_instructor = [course.courseName for course in courses if course.instructor == instructor.email]
                courseInstructor = ", ".join(course_instructor) if course_instructor else "None"
                if (search_query.lower() in instructor.name.lower() or
                    search_query.lower() in instructor.email.lower() or
                    search_query.lower() in courseInstructor.lower()):
                    item = QTreeWidgetItem([instructor.name, str(instructor.age), instructor.email, str(instructor.instructorID), courseInstructor])
                    tree.addTopLevelItem(item)

        search_var.textChanged.connect(lambda: update_treeview(search_var.text()))
        update_treeview("")

    # Function to view all students
    def view_students(self):
        self.clear_view()

        # Search layout
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_layout.addWidget(search_label)
        search_var = QLineEdit()
        search_layout.addWidget(search_var)
        self.layout().addLayout(search_layout)

        # Tree to display students
        tree = QTreeWidget()
        tree.setHeaderLabels(["Name", "Age", "Email", "Student ID", "Registered Courses"])
        self.layout().addWidget(tree)

        def update_treeview(search_query):
            tree.clear()
            students = Student.load_from_db()
            for student in students:
                registered_courses = self.get_student_courses(student.email)
                registered_courses_str = ", ".join(registered_courses) if registered_courses else "None"
                if (search_query.lower() in student.name.lower() or
                    search_query.lower() in student.email.lower() or
                    search_query.lower() in registered_courses_str.lower()):
                    item = QTreeWidgetItem([student.name, str(student.age), student.email, str(student.studentID), registered_courses_str])
                    tree.addTopLevelItem(item)

        search_var.textChanged.connect(lambda: update_treeview(search_var.text()))
        update_treeview("")

    # Function to view all courses
    def view_courses(self):
        self.clear_view()

        # Search layout
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_layout.addWidget(search_label)
        search_var = QLineEdit()
        search_layout.addWidget(search_var)
        self.layout().addLayout(search_layout)

        # Tree to display courses
        tree = QTreeWidget()
        tree.setHeaderLabels(["Course Name", "Course ID", "Instructor", "Enrolled Students"])
        self.layout().addWidget(tree)

        def update_treeview(search_query):
            tree.clear()
            courses = Course.load_from_db()
            for course in courses:
                enrolled_students = course.get_students_for_course(course.courseID)
                enrolled_students_str = ", ".join(enrolled_students) if enrolled_students else "None"
                if (search_query.lower() in course.courseName.lower() or
                    search_query.lower() in course.instructor.lower() or
                    search_query.lower() in enrolled_students_str.lower()):
                    item = QTreeWidgetItem([course.courseName, str(course.courseID), course.instructor, enrolled_students_str])
                    tree.addTopLevelItem(item)

        search_var.textChanged.connect(lambda: update_treeview(search_var.text()))
        update_treeview("")

    # Function to get courses registered by a student
    def get_student_courses(self, email):
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('SELECT courseID FROM registrations WHERE studentEmail = ?', (email,))
        course_ids = cursor.fetchall()
        course_ids = [course_id[0] for course_id in course_ids]
        if course_ids:
            query = 'SELECT courseName FROM courses WHERE courseID IN ({})'.format(
                ','.join('?' * len(course_ids))
            )
            cursor.execute(query, course_ids)
            courses = cursor.fetchall()
            course_names = [course[0] for course in courses]
        else:
            course_names = []
        conn.close()
        return course_names
