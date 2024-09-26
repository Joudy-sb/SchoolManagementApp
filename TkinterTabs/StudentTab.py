import sqlite3
import tkinter as tk
from tkinter import font
from Classes.Person import Student

def create_student_tab(notebook):
    """
    Creates the 'Student' tab in the notebook UI.
    This function adds a tab to the provided notebook UI component. It includes 
    a form for adding a new student to the database, and a section to view/edit/delete 
    existing students' information.

    Parameters:
    ----------
        notebook (tk.Notebook): The Tkinter notebook widget to which the student tab will be added.
    """
    student_tab = tk.Frame(notebook)
    notebook.add(student_tab, text="Student")

    # THIS PART IS FOR CREATING NEW STUDENTS IN DATABASE
    bold_font = font.Font(size=14, weight="bold")
    student_label = tk.Label(student_tab, text="Add New Student", font=bold_font)
    student_label.grid(row=0, column=0, columnspan=2, padx=20, pady=5)
    
    # input information about students to be saved
    name_label = tk.Label(student_tab, text="Enter Name")
    name_label.grid(row=1, column=0, padx=20, pady=5, sticky="W" ) 
    name_entry = tk.Entry(student_tab)
    name_entry.grid(row=1, column=1, padx=20, pady=5)
    age_label = tk.Label(student_tab, text="Enter Age")
    age_label.grid(row=2, column=0, padx=20, pady=5, sticky="W")
    age_entry = tk.Entry(student_tab)
    age_entry.grid(row=2, column=1, padx=20, pady=5)
    email_label = tk.Label(student_tab, text="Enter Email")
    email_label.grid(row=3, column=0, padx=20, pady=5, sticky="W")
    email_entry = tk.Entry(student_tab)
    email_entry.grid(row=3, column=1, padx=20, pady=5)
    ID_label = tk.Label(student_tab, text="Enter ID")
    ID_label.grid(row=4, column=0, padx=20, pady=5, sticky="W")
    ID_entry = tk.Entry(student_tab)
    ID_entry.grid(row=4, column=1, padx=20, pady=5)
    
    # THIS FUNCTION CREATES NEW STUDENT IN DATABASE
    def submit_form_student():
        """
        Submits the form to create a new student and saves the data to the database.

        This function retrieves the data entered in the student creation form (name, age, 
        email, and studentID), validates it, and creates a new student record in the 
        database. After successful submission, the form is cleared and the dropdown is 
        refreshed to reflect the changes.
        """
        name = name_entry.get()
        age = int(age_entry.get())
        email = email_entry.get()
        studentID = int(ID_entry.get())
        #Student.create_student(name, age, email, studentID).save_to_file()  
        Student.create_student(name, age, email, studentID).save_to_db()  
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        ID_entry.delete(0, tk.END)
        dropdown_refresh()      
        print(f"Student Submitted: {name}, {age}, {email}, {studentID}")
    
    submit_button_student = tk.Button(student_tab, text="Create", command=submit_form_student)
    submit_button_student.grid(row=6, column=1, columnspan=2, pady=10)

# --------------------------------------------------------------------------------------------------------

    # THIS PART IS TO VIEW/EDIT/DELETE INFORMATION OF STUDENT IN DATABASE
    student_label = tk.Label(student_tab, text="View Student Information", font=bold_font)
    student_label.grid(row=0, column=4, padx=20, pady=5, sticky="W")
    viewemail_label = tk.Label(student_tab, text="Select student email")
    viewemail_label.grid(row=1, column=4, padx=20, pady=5, sticky="W" ) 
    selected_email = tk.StringVar(value="")
    
    students_dropdown = tk.OptionMenu(student_tab, selected_email, "No students in database")

    # THIS FUNCTION REFRESHES THE DROPDOWN MENY WITH STUDENT EMAIL
    def dropdown_refresh():
        """
        Refreshes the dropdown menu with the latest list of students' emails.

        This function retrieves the email addresses of all students from the database and 
        updates the dropdown menu with the latest data. If no students are found, a placeholder 
        message is displayed.
        """
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('SELECT email FROM students')
        students = cursor.fetchall()
        conn.close()
        students_email = [student[0] for student in students]
        if students_email:
            students_dropdown = tk.OptionMenu(student_tab, selected_email, *students_email)
        else:
            students_dropdown = tk.OptionMenu(student_tab, selected_email, "No students in database")
        students_dropdown.config(width=21)
        students_dropdown.grid(row=2, column=4, padx=20, pady=5, sticky="W")
    dropdown_refresh()
    
    # THIS CLASS ALLOWS STUDENTS TO MODIFY/DELETE THEIR INFORMATIONS
    class EditDialog(tk.Toplevel):
        """
        A dialog window that allows students to edit or delete their information.

        This class creates a modal dialog window where the selected student's information 
        (name, age, and email) is displayed for editing. It also provides a delete option 
        to remove the student from the database.

        Parameters:
        ----------
            parent (tk.Widget): The parent widget that opens the dialog.
            student_ID (int): The unique ID of the student whose information is being edited.
            selected_email_var (tk.StringVar): A Tkinter StringVar used to hold the selected student's email from the dropdown.
            students_dropdown (tk.OptionMenu): The dropdown menu displaying the list of student emails.
        """
        def __init__(self, parent, student_ID, selected_email_var, students_dropdown):
            super().__init__(parent)
            self.dropdown_menu = students_dropdown
            self.selected_email_var = selected_email_var
            self.studentID = student_ID
            
            conn = sqlite3.connect('school_management.db')
            cursor = conn.cursor()
            self.title("Edit Student")
            tk.Label(self, text="Name:").grid(row=0, column=0, padx=10, pady=10)
            self.name_entry = tk.Entry(self)
            self.name_entry.grid(row=0, column=1, padx=10, pady=10)
            cursor.execute('SELECT name FROM students WHERE studentID = ?', (student_ID))
            existing_name = cursor.fetchone()
            self.name_entry.insert(0, existing_name)
            tk.Label(self, text="Age:").grid(row=1, column=0, padx=10, pady=10)
            self.age_entry = tk.Entry(self)
            self.age_entry.grid(row=1, column=1, padx=10, pady=10)
            cursor.execute('SELECT age FROM students WHERE studentID = ?', (student_ID))
            existing_age = cursor.fetchone()
            self.age_entry.insert(0, existing_age)
            tk.Label(self, text="Email:").grid(row=2, column=0, padx=10, pady=10)
            self.email_entry = tk.Entry(self)
            self.email_entry.grid(row=2, column=1, padx=10, pady=10)
            cursor.execute('SELECT email FROM students WHERE studentID = ?', (student_ID))
            existing_email = cursor.fetchone()
            self.email_entry.insert(0, existing_email)

            modify_button = tk.Button(self, text="Save", command=self.modify)
            modify_button.grid(row=3, column=1, padx=10, pady=10)
            delete_button = tk.Button(self, text="Delete", command=self.delete)
            delete_button.grid(row=3, column=0, padx=10, pady=10)
        
        # THIS METHOD EDITS/KEEPS THE INFORMATION OF THE STUDENT
        def modify(self):
            """
            Modifies the selected student's information in the database.

            This method allows the user to edit the name, age, and email of the selected 
            student. It validates that the new email is not already taken by another student 
            before saving the changes to the database. After modification, the dropdown menu is 
            updated, and the dialog is closed.
            """
            studentID = self.studentID 
            conn = sqlite3.connect('school_management.db')
            cursor = conn.cursor()
            if isinstance(studentID, tuple):
                studentID = studentID[0]
            if self.name_entry.get():
                cursor.execute('''
                UPDATE students
                SET name = ?
                WHERE studentID = ?
                ''', (self.name_entry.get(), studentID))
            if self.age_entry.get():
                cursor.execute('''
                UPDATE students
                SET age = ?
                WHERE studentID = ?
                ''', (self.age_entry.get(), studentID))
            if self.email_entry.get():
                # check that the new email isn't already taken by another student
                cursor.execute('SELECT email FROM students WHERE email = ? AND studentID != ?', (self.email_entry.get(), studentID))
                existing_email = cursor.fetchone()
                if existing_email:
                    conn.close()
                    raise ValueError("Student email already taken")
                cursor.execute('''
                UPDATE students
                SET email = ?
                WHERE studentID = ?
                ''', (self.email_entry.get(), studentID))
            conn.commit()
            conn.close()
            self.update_dropdown()
            self.destroy()

        # THIS METHOD DELETES EXISTING STUDENT FROM THE FILE
        def delete(self):
            """
            Deletes the selected student's record from the database.

            This method removes the student's data from the database and refreshes the dropdown 
            menu to reflect the deletion. After deletion, the dialog window is closed.
            """
            studentID = self.studentID
            #self.student.delete_from_file()
            Student.delete_from_db(studentID)  
            self.update_dropdown() 
            self.destroy()

        # THIS METHOD UPDATES DROPDOWN MENU AFTER CHANGES OCCUR
        def update_dropdown(self):
            """
            Updates the student email dropdown menu.

            This method clears the current selection in the dropdown menu and refreshes it 
            with the updated list of student emails after modifying or deleting a student.
            """
            self.selected_email_var.set("")
            menu = self.dropdown_menu["menu"]
            menu.delete(0, "end")
            dropdown_refresh()

    # THIS FUNCTIONS OPENS THE EDIT WINDOW WHERE STUDENT CAN EDIT HIS INFORMATION
    def edit_student():
        """
        Opens a dialog window to edit the selected student's information.

        This function retrieves the studentID associated with the selected email from the 
        dropdown menu and opens the `EditDialog` to allow the user to view and edit the 
        student's information.
        """
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        email = selected_email.get()
        cursor.execute('SELECT studentID FROM students WHERE email = ?', (email,))
        student_ID = cursor.fetchone()
        EditDialog(None, student_ID, selected_email, students_dropdown)

    edit_button = tk.Button(student_tab, text="View Information", command=edit_student)
    edit_button.grid(row=3, column=4, pady=10)

    
    '''# THIS FUNCTION REFRESHES THE DROPDOWN MENY WITH STUDENT EMAIL
    def dropdown_refresh():
        students = Student.load_from_file()
        students_email = [student.email for student in students]
        if students_email:
            students_dropdown = tk.OptionMenu(student_tab, selected_email, *students_email)
        else:
            students_dropdown = tk.OptionMenu(student_tab, selected_email, "No students in database")
        students_dropdown.config(width=21)
        students_dropdown.grid(row=2, column=4, padx=20, pady=5, sticky="W")
    dropdown_refresh()'''

    '''# THIS METHOD EDITS/KEEP THE INFORMATION OF THE STUDENT
        def modify(self):
            students = Student.load_from_file()
            if self.name_entry.get():
                self.student.name = self.name_entry.get()
            if self.age_entry.get():
                self.student.age = int(self.age_entry.get())
            if self.email_entry.get() and self.email_entry.get() != self.student.email:
                # email must not be taken
                for student in students:
                    if self.email_entry.get() == student.email:
                        raise ValueError("Student email already taken")
                self.student.email = self.email_entry.get()
            self.student.save_to_file()
            self.update_dropdown()  
            self.destroy()'''
    '''# THIS FUNCTIONS OPENS THE EDIT WINDOW WHERE STUDENT CAN EDIT HIS INFORMATION
    def edit_student():
        students = Student.load_from_file()
        email = selected_email.get()
        for student in students:
            if student.email == email:
                EditDialog(None, student, selected_email, students_dropdown)
                break'''