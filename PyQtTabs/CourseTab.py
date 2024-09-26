import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QGridLayout, QDialog
)
from PyQt5.QtGui import QFont
from Classes.Course import Course


class CourseTab(QWidget):
    def __init__(self):
        super().__init__()

        # Layout for the course tab
        layout = QGridLayout(self)

        # THIS PART IS FOR CREATING NEW COURSES IN DATABASE
        bold_font = QFont()
        bold_font.setPointSize(14)
        bold_font.setBold(True)

        course_label = QLabel("Add New Course")
        course_label.setFont(bold_font)
        layout.addWidget(course_label, 0, 0, 1, 2)

        # Input fields for creating new course
        name_label = QLabel("Enter Name")
        layout.addWidget(name_label, 1, 0)
        self.course_entry = QLineEdit()
        layout.addWidget(self.course_entry, 1, 1)

        ID_label = QLabel("Enter ID")
        layout.addWidget(ID_label, 2, 0)
        self.ID_entry = QLineEdit()
        layout.addWidget(self.ID_entry, 2, 1)

        # Submit button for creating the course
        submit_button_course = QPushButton("Create")
        submit_button_course.clicked.connect(self.submit_form_course)
        layout.addWidget(submit_button_course, 3, 1)

        # --------------------------------------------------------------------------------------------------------

        # THIS PART IS TO VIEW/EDIT/DELETE INFORMATION OF COURSES IN DATABASE
        course_label = QLabel("View Course Information")
        course_label.setFont(bold_font)
        layout.addWidget(course_label, 0, 4)

        viewID_label = QLabel("Select course ID")
        layout.addWidget(viewID_label, 1, 4)

        self.selected_ID = QComboBox()
        layout.addWidget(self.selected_ID, 2, 4)

        edit_button = QPushButton("View Information")
        edit_button.clicked.connect(self.edit_course)
        layout.addWidget(edit_button, 3, 4)

        # Refresh dropdown menu to show existing courses
        self.dropdown_refresh()

    # THIS FUNCTION CREATES NEW COURSE IN DATABASE
    def submit_form_course(self):
        courseName = self.course_entry.text()
        courseID = int(self.ID_entry.text())

        # Create a new course and save it to the database
        Course.create_course(courseID, courseName).save_to_db()

        # Clear fields after submission
        self.course_entry.clear()
        self.ID_entry.clear()

        # Refresh the dropdown to include the new course
        self.dropdown_refresh()

        print(f"Course Submitted: {courseName}, {courseID}")

    # THIS FUNCTION REFRESHES THE DROPDOWN MENU WITH COURSE ID
    def dropdown_refresh(self):
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('SELECT courseID FROM courses')
        courses = cursor.fetchall()
        conn.close()

        self.selected_ID.clear()
        courses_ID = [str(course[0]) for course in courses]
        if courses_ID:
            self.selected_ID.addItems(courses_ID)
        else:
            self.selected_ID.addItem("No courses in database")

    # THIS CLASS ALLOWS COURSE INFORMATION MODIFICATION/DELETION 
    class EditDialog(QDialog):
        def __init__(self, course_ID, parent=None):
            super().__init__(parent)
            self.course_ID = course_ID

            self.setWindowTitle("Edit Course")
            self.setFixedSize(300, 200)

            conn = sqlite3.connect('school_management.db')
            cursor = conn.cursor()

            layout = QGridLayout(self)

            # Fetch existing course data
            cursor.execute('SELECT courseName FROM courses WHERE courseID = ?', (course_ID,))
            course_data = cursor.fetchone()

            # Fields for editing
            self.name_entry = QLineEdit(course_data[0])
            layout.addWidget(QLabel("Name:"), 0, 0)
            layout.addWidget(self.name_entry, 0, 1)

            # Buttons for saving or deleting the course
            modify_button = QPushButton("Save")
            modify_button.clicked.connect(self.modify)
            layout.addWidget(modify_button, 3, 1)

            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(self.delete)
            layout.addWidget(delete_button, 3, 0)

            conn.close()

        # THIS METHOD MODIFIES THE COURSE INFORMATION
        def modify(self):
            courseID = self.course_ID
            conn = sqlite3.connect('school_management.db')
            cursor = conn.cursor()

            if self.name_entry.text():
                cursor.execute('''
                    UPDATE courses
                    SET courseName = ?
                    WHERE courseID = ?
                ''', (self.name_entry.text(), courseID))

            conn.commit()
            conn.close()

            self.parent().dropdown_refresh()
            self.accept()

        # THIS METHOD DELETES THE COURSE
        def delete(self):
            courseID = self.course_ID
            Course.delete_from_db(courseID)

            self.parent().dropdown_refresh()
            self.accept()

    # THIS FUNCTION OPENS THE EDIT WINDOW WHERE COURSE INFORMATION CAN BE MODIFIED
    def edit_course(self):
        course_ID = self.selected_ID.currentText()
        if course_ID != "No courses in database":
            dialog = self.EditDialog(int(course_ID), self)
            dialog.exec_()
