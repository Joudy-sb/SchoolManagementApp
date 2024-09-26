import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QGridLayout, QDialog, QVBoxLayout
)
from PyQt5.QtGui import QFont
from Classes.Person import Student


class StudentTab(QWidget):
    def __init__(self):
        super().__init__()

        # Layout for the tab
        layout = QGridLayout(self)

        # THIS PART IS FOR CREATING NEW STUDENTS IN DATABASE
        bold_font = QFont()
        bold_font.setPointSize(14)
        bold_font.setBold(True)

        student_label = QLabel("Add New Student")
        student_label.setFont(bold_font)
        layout.addWidget(student_label, 0, 0, 1, 2)

        # Input fields for creating new student
        name_label = QLabel("Enter Name")
        layout.addWidget(name_label, 1, 0)
        self.name_entry = QLineEdit()
        layout.addWidget(self.name_entry, 1, 1)

        age_label = QLabel("Enter Age")
        layout.addWidget(age_label, 2, 0)
        self.age_entry = QLineEdit()
        layout.addWidget(self.age_entry, 2, 1)

        email_label = QLabel("Enter Email")
        layout.addWidget(email_label, 3, 0)
        self.email_entry = QLineEdit()
        layout.addWidget(self.email_entry, 3, 1)

        ID_label = QLabel("Enter ID")
        layout.addWidget(ID_label, 4, 0)
        self.ID_entry = QLineEdit()
        layout.addWidget(self.ID_entry, 4, 1)

        # Submit button
        submit_button_student = QPushButton("Create")
        submit_button_student.clicked.connect(self.submit_form_student)
        layout.addWidget(submit_button_student, 6, 1)

        # --------------------------------------------------------------------------------------------------------

        # THIS PART IS TO VIEW/EDIT/DELETE INFORMATION OF STUDENT IN DATABASE
        student_label = QLabel("View Student Information")
        student_label.setFont(bold_font)
        layout.addWidget(student_label, 0, 4)

        viewemail_label = QLabel("Select student email")
        layout.addWidget(viewemail_label, 1, 4)

        self.selected_email = QComboBox()
        layout.addWidget(self.selected_email, 2, 4)

        edit_button = QPushButton("View Information")
        edit_button.clicked.connect(self.edit_student)
        layout.addWidget(edit_button, 3, 4)

        self.dropdown_refresh()

    # THIS FUNCTION CREATES NEW STUDENT IN DATABASE
    def submit_form_student(self):
        name = self.name_entry.text()
        age = int(self.age_entry.text())
        email = self.email_entry.text()
        studentID = int(self.ID_entry.text())

        Student.create_student(name, age, email, studentID).save_to_db()

        # Clear fields after submission
        self.name_entry.clear()
        self.age_entry.clear()
        self.email_entry.clear()
        self.ID_entry.clear()
        self.dropdown_refresh()

        print(f"Student Submitted: {name}, {age}, {email}, {studentID}")

    # THIS FUNCTION REFRESHES THE DROPDOWN MENU WITH STUDENT EMAIL
    def dropdown_refresh(self):
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('SELECT email FROM students')
        students = cursor.fetchall()
        conn.close()

        self.selected_email.clear()
        students_email = [student[0] for student in students]
        if students_email:
            self.selected_email.addItems(students_email)
        else:
            self.selected_email.addItem("No students in database")

    # THIS CLASS ALLOWS STUDENTS TO MODIFY/DELETE THEIR INFORMATION
    class EditDialog(QDialog):
        def __init__(self, student_ID, parent=None):
            super().__init__(parent)
            self.studentID = student_ID

            self.setWindowTitle("Edit Student")
            self.setFixedSize(300, 200)

            conn = sqlite3.connect('school_management.db')
            cursor = conn.cursor()

            layout = QGridLayout(self)

            # Fetch existing student data
            cursor.execute('SELECT name, age, email FROM students WHERE studentID = ?', (student_ID,))
            student_data = cursor.fetchone()

            # Fields for editing
            self.name_entry = QLineEdit(student_data[0])
            layout.addWidget(QLabel("Name:"), 0, 0)
            layout.addWidget(self.name_entry, 0, 1)

            self.age_entry = QLineEdit(str(student_data[1]))
            layout.addWidget(QLabel("Age:"), 1, 0)
            layout.addWidget(self.age_entry, 1, 1)

            self.email_entry = QLineEdit(student_data[2])
            layout.addWidget(QLabel("Email:"), 2, 0)
            layout.addWidget(self.email_entry, 2, 1)

            # Buttons for saving or deleting the student
            modify_button = QPushButton("Save")
            modify_button.clicked.connect(self.modify)
            layout.addWidget(modify_button, 3, 1)

            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(self.delete)
            layout.addWidget(delete_button, 3, 0)

            conn.close()

        def modify(self):
            conn = sqlite3.connect('school_management.db')
            cursor = conn.cursor()

            name = self.name_entry.text()
            age = self.age_entry.text()
            email = self.email_entry.text()

            cursor.execute('UPDATE students SET name = ?, age = ?, email = ? WHERE studentID = ?',
                           (name, age, email, self.studentID))
            conn.commit()
            conn.close()

            self.parent().dropdown_refresh()
            self.accept()

        def delete(self):
            conn = sqlite3.connect('school_management.db')
            cursor = conn.cursor()

            cursor.execute('DELETE FROM students WHERE studentID = ?', (self.studentID,))
            conn.commit()
            conn.close()

            self.parent().dropdown_refresh()
            self.accept()

    # THIS FUNCTION OPENS THE EDIT WINDOW WHERE STUDENT CAN EDIT THEIR INFORMATION
    def edit_student(self):
        email = self.selected_email.currentText()
        if email == "No students in database":
            return

        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('SELECT studentID FROM students WHERE email = ?', (email,))
        student_ID = cursor.fetchone()
        conn.close()

        if student_ID:
            dialog = self.EditDialog(student_ID[0], self)
            dialog.exec_()
