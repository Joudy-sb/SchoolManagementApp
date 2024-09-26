import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QGridLayout, QRadioButton
)
from PyQt5.QtGui import QFont
from Classes.Course import Course
from Classes.Person import Student, Instructor


class RegisterTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout(self)

        # THIS PART IS FOR REGISTERING/ASSIGNING COURSES TO STUDENTS/INSTRUCTORS
        bold_font = QFont()
        bold_font.setPointSize(14)
        bold_font.setBold(True)

        course_level_label = QLabel("Register/Assign Course")
        course_level_label.setFont(bold_font)
        layout.addWidget(course_level_label, 0, 0)

        # Role selection (Student or Instructor)
        self.role_var = "Student"

        role_label = QLabel("Select your role")
        layout.addWidget(role_label, 1, 0)

        self.student_radio = QRadioButton("Student")
        self.student_radio.setChecked(True)
        self.student_radio.toggled.connect(self.update_dropdown)
        layout.addWidget(self.student_radio, 2, 0)

        self.instructor_radio = QRadioButton("Instructor")
        self.instructor_radio.toggled.connect(self.update_dropdown)
        layout.addWidget(self.instructor_radio, 2, 1)

        student_label = QLabel("Select your email")
        layout.addWidget(student_label, 3, 0)

        self.selected_name = QComboBox()
        layout.addWidget(self.selected_name, 4, 0, 1, 2)

        self.selected_course = QComboBox()
        layout.addWidget(self.selected_course, 6, 0, 1, 2)

        choose_button = QPushButton("Choose")
        choose_button.clicked.connect(self.submit_email)
        layout.addWidget(choose_button, 4, 1)

        submit_registration_button = QPushButton("Register")
        submit_registration_button.clicked.connect(self.submit_course_registration)
        layout.addWidget(submit_registration_button, 7, 1)

        self.update_dropdown()

        # --------------------------------------------------------------------------------------------------------

        # Unregistering courses
        unregister_label = QLabel("Unregister/Unassign Course")
        unregister_label.setFont(bold_font)
        layout.addWidget(unregister_label, 0, 4)

        self.student_radio_unregistered = QRadioButton("Student")
        self.student_radio_unregistered.setChecked(True)
        self.student_radio_unregistered.toggled.connect(self.update_dropdown_unregister)
        layout.addWidget(self.student_radio_unregistered, 2, 4)

        self.instructor_radio_unregistered = QRadioButton("Instructor")
        self.instructor_radio_unregistered.toggled.connect(self.update_dropdown_unregister)
        layout.addWidget(self.instructor_radio_unregistered, 2, 5)

        self.selected_name_unregistered = QComboBox()
        layout.addWidget(self.selected_name_unregistered, 4, 4, 1, 2)

        self.selected_course_unregistered = QComboBox()
        layout.addWidget(self.selected_course_unregistered, 6, 4, 1, 2)

        choose_unregistered_button = QPushButton("Choose")
        choose_unregistered_button.clicked.connect(self.submit_email_unregister)
        layout.addWidget(choose_unregistered_button, 4, 5)

        submit_unregistration_button = QPushButton("Unregister")
        submit_unregistration_button.clicked.connect(self.submit_course_unregistration)
        layout.addWidget(submit_unregistration_button, 7, 5)

        self.update_dropdown_unregister()

    def update_dropdown(self):
        """Updates the dropdown menu with emails of students or instructors based on the selected role."""
        self.selected_name.clear()
        self.selected_course.clear()

        role = "Student" if self.student_radio.isChecked() else "Instructor"

        if role == "Student":
            students = Student.load_from_db()
            students_email = [student.email for student in students]
            self.selected_name.addItems(students_email)
        elif role == "Instructor":
            instructors = Instructor.load_from_db()
            instructors_email = [instructor.email for instructor in instructors]
            self.selected_name.addItems(instructors_email)

    def submit_email(self):
        """Shows the available courses based on the selected user (student/instructor)."""
        self.selected_course.clear()
        role = "Student" if self.student_radio.isChecked() else "Instructor"
        email = self.selected_name.currentText()

        courses = Course.load_from_db()
        available_courses = [str(course.courseID) for course in courses]

        if role == "Student":
            registered_courses = self.get_student_courses(email)
        else:
            registered_courses = self.get_instructor_courses(email)

        unregistered_courses = [course for course in available_courses if course not in registered_courses]

        if unregistered_courses:
            self.selected_course.addItems(unregistered_courses)
        else:
            self.selected_course.addItem("No courses available")

    def submit_course_registration(self):
        """Registers a student or assigns a course to an instructor."""
        role = "Student" if self.student_radio.isChecked() else "Instructor"
        email = self.selected_name.currentText()
        course_ID = self.selected_course.currentText()

        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()

        if role == "Student":
            cursor.execute('''
                INSERT INTO registrations (studentEmail, courseID)
                VALUES (?, ?)
            ''', (email, course_ID))
        else:
            cursor.execute('''
                UPDATE courses
                SET instructor = ?
                WHERE courseID = ?
            ''', (email, course_ID))

        conn.commit()
        conn.close()

        self.selected_name.clear()
        self.selected_course.clear()
        self.update_dropdown()

    def update_dropdown_unregister(self):
        """Updates the dropdown for unregistering a course."""
        self.selected_name_unregistered.clear()
        self.selected_course_unregistered.clear()

        role = "Student" if self.student_radio_unregistered.isChecked() else "Instructor"

        if role == "Student":
            students = Student.load_from_db()
            students_email = [student.email for student in students]
            self.selected_name_unregistered.addItems(students_email)
        else:
            instructors = Instructor.load_from_db()
            instructors_email = [instructor.email for instructor in instructors]
            self.selected_name_unregistered.addItems(instructors_email)

    def submit_email_unregister(self):
        """Shows the courses registered by a student or assigned to an instructor."""
        self.selected_course_unregistered.clear()
        role = "Student" if self.student_radio_unregistered.isChecked() else "Instructor"
        email = self.selected_name_unregistered.currentText()

        courses = Course.load_from_db()
        available_courses = [str(course.courseID) for course in courses]

        if role == "Student":
            registered_courses = self.get_student_courses(email)
        else:
            registered_courses = self.get_instructor_courses(email)

        registered_courses_list = [course for course in available_courses if course in registered_courses]

        if registered_courses_list:
            self.selected_course_unregistered.addItems(registered_courses_list)
        else:
            self.selected_course_unregistered.addItem("No courses available")

    def submit_course_unregistration(self):
        """Unregisters a student from a course or unassigns an instructor from a course."""
        role = "Student" if self.student_radio_unregistered.isChecked() else "Instructor"
        email = self.selected_name_unregistered.currentText()
        course_ID = self.selected_course_unregistered.currentText()

        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()

        if role == "Student":
            cursor.execute('''
                DELETE FROM registrations
                WHERE studentEmail = ? AND courseID = ?
            ''', (email, course_ID))
        else:
            cursor.execute('''
                UPDATE courses
                SET instructor = NULL
                WHERE courseID = ?
            ''', (course_ID,))

        conn.commit()
        conn.close()

        self.selected_name_unregistered.clear()
        self.selected_course_unregistered.clear()
        self.update_dropdown_unregister()

    # Helper methods to get courses for a student or instructor
    def get_student_courses(self, email):
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('SELECT courseID FROM registrations WHERE studentEmail = ?', (email,))
        course_ids = cursor.fetchall()
        conn.close()
        return [str(course[0]) for course in course_ids]

    def get_instructor_courses(self, email):
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('SELECT courseID FROM courses WHERE instructor = ?', (email,))
        course_ids = cursor.fetchall()
        conn.close()
        return [str(course[0]) for course in course_ids]
