import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QGridLayout, QDialog
)
from PyQt5.QtGui import QFont
from Classes.Person import Instructor


class InstructorTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout(self)

        # THIS PART IS FOR CREATING NEW INSTRUCTORS IN DATABASE
        bold_font = QFont()
        bold_font.setPointSize(14)
        bold_font.setBold(True)

        instructor_label = QLabel("Add New Instructor")
        instructor_label.setFont(bold_font)
        layout.addWidget(instructor_label, 0, 0, 1, 2)

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
        submit_button_instructor = QPushButton("Create")
        submit_button_instructor.clicked.connect(self.submit_form_instructor)
        layout.addWidget(submit_button_instructor, 6, 1)

        # --------------------------------------------------------------------------------------------------------

        # THIS PART IS TO VIEW/EDIT/DELETE INFORMATION OF INSTRUCTOR IN DATABASE
        instructor_label = QLabel("View Instructor Information")
        instructor_label.setFont(bold_font)
        layout.addWidget(instructor_label, 0, 4)

        viewemail_label = QLabel("Select instructor email")
        layout.addWidget(viewemail_label, 1, 4)

        self.selected_email = QComboBox()
        layout.addWidget(self.selected_email, 2, 4)

        edit_button = QPushButton("View Information")
        edit_button.clicked.connect(self.edit_instructor)
        layout.addWidget(edit_button, 3, 4)

        self.dropdown_refresh()

    # THIS FUNCTION CREATES NEW INSTRUCTOR IN DATABASE
    def submit_form_instructor(self):
        name = self.name_entry.text()
        age = int(self.age_entry.text())
        email = self.email_entry.text()
        instructorID = int(self.ID_entry.text())

        Instructor.create_instructor(name, age, email, instructorID).save_to_db()

        # Clear fields after submission
        self.name_entry.clear()
        self.age_entry.clear()
        self.email_entry.clear()
        self.ID_entry.clear()

        self.dropdown_refresh()

        print(f"Instructor Submitted: {name}, {age}, {email}, {instructorID}")

    # THIS FUNCTION REFRESHES THE DROPDOWN MENU WITH INSTRUCTOR EMAIL
    def dropdown_refresh(self):
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('SELECT email FROM instructors')
        instructors = cursor.fetchall()
        conn.close()

        self.selected_email.clear()
        instructors_email = [instructor[0] for instructor in instructors]
        if instructors_email:
            self.selected_email.addItems(instructors_email)
        else:
            self.selected_email.addItem("No instructors in database")

    # THIS CLASS ALLOWS INSTRUCTORS TO MODIFY/DELETE THEIR INFORMATION
    class EditDialog(QDialog):
        def __init__(self, instructor_ID, parent=None):
            super().__init__(parent)
            self.instructorID = instructor_ID

            self.setWindowTitle("Edit Instructor")
            self.setFixedSize(300, 200)

            conn = sqlite3.connect('school_management.db')
            cursor = conn.cursor()

            layout = QGridLayout(self)

            cursor.execute('SELECT name, age, email FROM instructors WHERE instructorID = ?', (instructor_ID,))
            instructor_data = cursor.fetchone()

            self.name_entry = QLineEdit(instructor_data[0])
            layout.addWidget(QLabel("Name:"), 0, 0)
            layout.addWidget(self.name_entry, 0, 1)

            self.age_entry = QLineEdit(str(instructor_data[1]))
            layout.addWidget(QLabel("Age:"), 1, 0)
            layout.addWidget(self.age_entry, 1, 1)

            self.email_entry = QLineEdit(instructor_data[2])
            layout.addWidget(QLabel("Email:"), 2, 0)
            layout.addWidget(self.email_entry, 2, 1)

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

            cursor.execute('UPDATE instructors SET name = ?, age = ?, email = ? WHERE instructorID = ?',
                           (name, age, email, self.instructorID))
            conn.commit()
            conn.close()

            self.parent().dropdown_refresh()
            self.accept()

        def delete(self):
            conn = sqlite3.connect('school_management.db')
            cursor = conn.cursor()

            cursor.execute('DELETE FROM instructors WHERE instructorID = ?', (self.instructorID,))
            conn.commit()
            conn.close()

            self.parent().dropdown_refresh()
            self.accept()

    # THIS FUNCTION OPENS THE EDIT WINDOW WHERE INSTRUCTOR CAN EDIT THEIR INFORMATION
    def edit_instructor(self):
        email = self.selected_email.currentText()
        if email == "No instructors in database":
            return

        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('SELECT instructorID FROM instructors WHERE email = ?', (email,))
        instructor_ID = cursor.fetchone()
        conn.close()

        if instructor_ID:
            dialog = self.EditDialog(instructor_ID[0], self)
            dialog.exec_()
