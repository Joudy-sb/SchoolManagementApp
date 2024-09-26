import sqlite3
import tkinter as tk
from tkinter import font
from Classes.Person import Instructor

def create_instructor_tab(notebook):
    """
    This function creates the 'Instructor' tab in the notebook UI.
    It adds a form for adding new instructors to the database, and includes
    a section to view, edit, or delete existing instructor information.

    Parameters:
    ----------
        notebook (tk.Notebook): The Tkinter notebook widget to which the instructor tab will be added.
    """
    instructor_tab = tk.Frame(notebook)
    notebook.add(instructor_tab, text="Instructor")

    # THIS PART IS FOR CREATING NEW INSTRUCTORS IN DATABASE
    bold_font = font.Font(size=14, weight="bold")
    instructor_label = tk.Label(instructor_tab, text="Add New Instructor", font=bold_font)
    instructor_label.grid(row=0, column=0,columnspan=2, padx=20, pady=5)

    # input information about instructors to be saved
    name_label = tk.Label(instructor_tab, text="Enter Name")
    name_label.grid(row=1, column=0, padx=20, pady=5, sticky="W" )
    name_entry = tk.Entry(instructor_tab)
    name_entry.grid(row=1, column=1, padx=20, pady=5)
    age_label = tk.Label(instructor_tab, text="Enter Age")
    age_label.grid(row=2, column=0, padx=20, pady=5, sticky="W" )
    age_entry = tk.Entry(instructor_tab)
    age_entry.grid(row=2, column=1, padx=20, pady=5)
    email_label = tk.Label(instructor_tab, text="Enter Email")
    email_label.grid(row=3, column=0, padx=20, pady=5, sticky="W" )
    email_entry = tk.Entry(instructor_tab)
    email_entry.grid(row=3, column=1, padx=20, pady=5)
    ID_label = tk.Label(instructor_tab, text="Enter ID")
    ID_label.grid(row=4, column=0, padx=20, pady=5, sticky="W" )
    ID_entry = tk.Entry(instructor_tab)
    ID_entry.grid(row=4, column=1, padx=20, pady=5)

    # THIS FUNCTION CREATES NEW INSTRUCTOR IN DATABASE
    def submit_form_instructor():
        """
        Submits the form to create a new instructor and saves the data to the database.

        This function retrieves the data entered in the instructor creation form (name, age, 
        email, and instructorID), validates it, and creates a new instructor record in the 
        database. After successful submission, the form is cleared and the dropdown is refreshed.
        """
        name = name_entry.get()
        age = int(age_entry.get())
        email = email_entry.get()
        instructorID = int(ID_entry.get())
        #Instructor.create_instructor(name, age, email, studentID).save_to_file()  
        Instructor.create_instructor(name, age, email, instructorID).save_to_db()
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        ID_entry.delete(0, tk.END)
        dropdown_refresh() 
        print(f"Instructor Submitted: {name}, {age}, {email}, {instructorID}")
    
    submit_button_instructor = tk.Button(instructor_tab, text="Create", command=submit_form_instructor)
    submit_button_instructor.grid(row=6, column=1, columnspan=2, pady=10)

# --------------------------------------------------------------------------------------------------------

    # THIS PART IS TO VIEW/EDIT/DELETE INFORMATION OF INSTRUCTOR IN DATABASE
    instructor_label = tk.Label(instructor_tab, text="View Instructor Information", font=bold_font)
    instructor_label.grid(row=0, column=4, padx=20, pady=5)
    viewemail_label = tk.Label(instructor_tab, text="Select instructor email")
    viewemail_label.grid(row=1, column=4, padx=20, pady=5, sticky="W" ) 
    selected_email = tk.StringVar(value="")

    instructors_dropdown = tk.OptionMenu(instructor_tab, selected_email, "No instructor in database")

    # THIS FUNCTION REFRESHES THE DROPDOWN MENY WITH INSTRUCTOR EMAIL
    def dropdown_refresh():
        """
        Refreshes the dropdown menu with the latest list of instructor emails.

        This function retrieves the email addresses of all instructors from the database and 
        updates the dropdown menu with the latest data. If no instructors are found, a placeholder 
        message is displayed.
        """
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('SELECT email FROM instructors')
        instructors = cursor.fetchall()
        conn.close()
        instructors_email = [instructor[0] for instructor in instructors]
        if instructors_email:
            instructors_dropdown = tk.OptionMenu(instructor_tab, selected_email, *instructors_email)
        else:
            instructors_dropdown = tk.OptionMenu(instructor_tab, selected_email, "No instructors in database")
        instructors_dropdown.config(width=21)
        instructors_dropdown.grid(row=2, column=4, padx=20, pady=5, sticky="W")
    dropdown_refresh()

    # THIS CLASS ALLOWS STUDENTS TO MODIFY/DELETE THEIR INFORMATIONS
    class EditDialog(tk.Toplevel):
        """
        A dialog window that allows instructors to edit or delete their information.

        This class creates a modal dialog window where the selected instructor's information 
        (name, age, and email) is displayed for editing. It also provides a delete option to 
        remove the instructor from the database.

        Parameters:
        ----------
            parent (tk.Widget): The parent widget that opens the dialog.
            instructor_ID (int): The unique ID of the instructor whose information is being edited.
            selected_email_var (tk.StringVar): A Tkinter StringVar used to hold the selected instructor's email from the dropdown.
            instructors_dropdown (tk.OptionMenu): The dropdown menu displaying the list of instructor emails.
        """
        def __init__(self, parent, instructor_ID, selected_email_var, instructors_dropdown):
            super().__init__(parent)
            self.dropdown_menu = instructors_dropdown
            self.selected_email_var = selected_email_var
            self.instructorID = instructor_ID
            
            conn = sqlite3.connect('school_management.db')
            cursor = conn.cursor()
            self.title("Edit Instructor")
            tk.Label(self, text="Name:").grid(row=0, column=0, padx=10, pady=10)
            self.name_entry = tk.Entry(self)
            self.name_entry.grid(row=0, column=1, padx=10, pady=10)
            cursor.execute('SELECT name FROM instructors WHERE instructorID = ?', (instructor_ID))
            existing_name = cursor.fetchone()
            self.name_entry.insert(0, existing_name)
            tk.Label(self, text="Age:").grid(row=1, column=0, padx=10, pady=10)
            self.age_entry = tk.Entry(self)
            self.age_entry.grid(row=1, column=1, padx=10, pady=10)
            cursor.execute('SELECT age FROM instructors WHERE instructorID = ?', (instructor_ID))
            existing_age = cursor.fetchone()
            self.age_entry.insert(0, existing_age)
            tk.Label(self, text="Email:").grid(row=2, column=0, padx=10, pady=10)
            self.email_entry = tk.Entry(self)
            self.email_entry.grid(row=2, column=1, padx=10, pady=10)
            cursor.execute('SELECT email FROM instructors WHERE instructorID = ?', (instructor_ID))
            existing_email = cursor.fetchone()
            self.email_entry.insert(0, existing_email)

            modify_button = tk.Button(self, text="Save", command=self.modify)
            modify_button.grid(row=3, column=1, padx=10, pady=10)
            delete_button = tk.Button(self, text="Delete", command=self.delete)
            delete_button.grid(row=3, column=0, padx=10, pady=10)

        # THIS METHOD EDITS/KEEPS THE INFORMATION OF THE INSTRUCTOR
        def modify(self):
            """
            Modifies the selected instructor's information in the database.

            This method allows the user to edit the name, age, and email of the selected instructor.
            It validates that the new email is not already taken by another instructor before saving
            the changes to the database. After modification, the dropdown menu is updated, and the 
            dialog is closed.
            """
            instructorID = self.instructorID  
            conn = sqlite3.connect('school_management.db')
            cursor = conn.cursor()

            if isinstance(instructorID, tuple):
                instructorID = instructorID[0]
            if self.name_entry.get():
                cursor.execute('''
                UPDATE instructors
                SET name = ?
                WHERE instructorID = ?
                ''', (self.name_entry.get(), instructorID))
            if self.age_entry.get():
                cursor.execute('''
                UPDATE instructors
                SET age = ?
                WHERE instructorID = ?
                ''', (self.age_entry.get(), instructorID))
            if self.email_entry.get():
                # check that the new email isn't already taken by another student
                cursor.execute('SELECT email FROM instructors WHERE email = ? AND instructorID != ?', (self.email_entry.get(), instructorID))
                existing_email = cursor.fetchone()
                if existing_email:
                    conn.close()
                    raise ValueError("Instructor email already taken")
                cursor.execute('''
                UPDATE instructors
                SET email = ?
                WHERE instructorID = ?
                ''', (self.email_entry.get(), instructorID))
            conn.commit()
            conn.close()
            self.update_dropdown()
            self.destroy()

        # THIS METHOD DELETES EXISTING INSTRUCTOR FROM THE DATABASE
        def delete(self):
            """
            Deletes the selected instructor's record from the database.

            This method removes the instructor's data from the database and refreshes the dropdown 
            menu to reflect the deletion. After deletion, the dialog window is closed.
            """
            #self.instructor.delete_from_file()
            instructorID = self.instructorID
            Instructor.delete_from_db(instructorID)  
            self.update_dropdown() 
            self.destroy()

        # THIS METHOD UPDATES DROPDOWN MENU AFTER CHANGES OCCUR
        def update_dropdown(self):
            """
            Updates the instructor email dropdown menu.

            This method clears the current selection in the dropdown menu and refreshes it 
            with the updated list of instructor emails after modifying or deleting an instructor.
            """
            self.selected_email_var.set("")
            menu = self.dropdown_menu["menu"]
            menu.delete(0, "end")
            dropdown_refresh()

    # THIS FUNCTIONS OPENS THE EDIT WINDOW WHERE STUDENT CAN EDIT HIS INFORMATION
    def edit_instructor():
        """
        Opens a dialog window to edit the selected instructor's information.

        This function retrieves the instructorID associated with the selected email from the 
        dropdown menu and opens the `EditDialog` to allow the user to view and edit the 
        instructor's information.
        """
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        email = selected_email.get()
        cursor.execute('SELECT instructorID FROM instructors WHERE email = ?', (email,))
        instructor_ID = cursor.fetchone()
        EditDialog(None, instructor_ID, selected_email, instructors_dropdown)

    edit_button = tk.Button(instructor_tab, text="View Information", command=edit_instructor)
    edit_button.grid(row=3, column=4, pady=10)


    '''# THIS FUNCTION REFRESHES THE DROPDOWN MENY WITH INSTRUCTOR EMAIL
    def dropdown_refresh():
        instructors = Instructor.load_from_file()
        instructors_email = [instructor.email for instructor in instructors]
        if instructors_email:
            instructors_dropdown = tk.OptionMenu(instructor_tab, selected_email, *instructors_email)
        else:
            instructors_dropdown = tk.OptionMenu(instructor_tab, selected_email, "No instructor in database")
        instructors_dropdown.config(width=21)
        instructors_dropdown.grid(row=2, column=4, padx=20, pady=5, sticky="W")
    dropdown_refresh()'''

    '''# THIS METHOD EDITS/KEEP THE INFORMATION OF THE INSTRUCTOR
        def modify(self):
            instructors = Instructor.load_from_file()
            if self.name_entry.get():
                self.instructor.name = self.name_entry.get()
            if self.age_entry.get():
                self.instructor.age = int(self.age_entry.get())
            # email must not be taken
            if self.email_entry.get() and self.email_entry.get() != self.instructor.email:
                for instructor in instructors:
                    if self.email_entry.get() == instructor.email:
                        raise ValueError("Instructor email already taken")
                    self.instructor.email = self.email_entry.get()
            self.instructor.save_to_file()
            self.update_dropdown()  
            self.destroy()       '''


    '''# THIS FUNCTIONS OPENS THE EDIT WINDOW WHERE INSTRUCTOR CAN EDIT HIS INFORMATION
    def edit_instructor():
        instructors = Instructor.load_from_file()
        email = selected_email.get()
        for instructor in instructors:
            if instructor.email == email:
                EditDialog(None, instructor, selected_email, instructors_dropdown)
                break'''