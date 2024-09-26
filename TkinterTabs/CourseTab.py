import sqlite3
import tkinter as tk
from tkinter import font
from Classes.Course import Course
from Classes.Person import Student, Instructor

def create_course_tab(notebook):
    """
    This function creates the 'Course' tab in the notebook UI.

    It adds a form for adding new courses to the database, and includes
    a section to view, edit, or delete existing course information.

    Parameters:
    ----------
        notebook (tk.Notebook): The Tkinter notebook widget to which the course tab will be added.
    """
    course_tab = tk.Frame(notebook)
    notebook.add(course_tab, text="Course")

    # THIS PART IS FOR CREATING NEW COURSES IN DATABASE
    bold_font = font.Font(size=14, weight="bold")
    course_label = tk.Label(course_tab, text="Add New Course", font=bold_font)
    course_label.grid(row=0, column=0,columnspan=2, padx=20, pady=5)

    # input information about courses to be saved
    course_label = tk.Label(course_tab, text="Enter Name")
    course_label.grid(row=1, column=0, padx=20, pady=5, sticky="W" )
    course_entry = tk.Entry(course_tab)
    course_entry.grid(row=1, column=1, padx=20, pady=5)
    ID_label = tk.Label(course_tab, text="Enter ID")
    ID_label.grid(row=2, column=0, padx=20, pady=5, sticky="W" )
    ID_entry = tk.Entry(course_tab)
    ID_entry.grid(row=2, column=1, padx=20, pady=5)

    # THIS FUNCTION CREATES NEW COURSE IN DATABASE
    def submit_form_course():
        """
        Submits the form to create a new course and saves the data to the database.

        This function retrieves the data entered in the course creation form (courseName, courseID),
        validates it, and creates a new course record in the database. After successful submission, 
        the form is cleared and the dropdown is refreshed.
        """
        courseName = course_entry.get()
        courseID = int(ID_entry.get())
        #Course.create_course(courseID, courseName).save_to_file()
        Course.create_course(courseID,courseName).save_to_db()
        course_entry.delete(0, tk.END)
        ID_entry.delete(0, tk.END)
        dropdown_refresh()
        print(f"Course Submitted: {courseName}, {courseID}")
    
    submit_button_course = tk.Button(course_tab, text="Create", command=submit_form_course)
    submit_button_course.grid(row=3, column=1, columnspan=2, pady=10)

# --------------------------------------------------------------------------------------------------------

    # THIS PART IS TO VIEW/EDIT/DELETE INFORMATION OF COURSE IN DATABASE
    course_label = tk.Label(course_tab, text="View Course Information", font=bold_font)
    course_label.grid(row=0, column=4, padx=20, pady=5)
    viewID_label = tk.Label(course_tab, text="Select course ID")
    viewID_label.grid(row=1, column=4, padx=20, pady=5, sticky="W" ) 
    selected_ID = tk.StringVar(value="")
    
    course_id_dropdown = tk.OptionMenu(course_tab, selected_ID, "No course in database")

    # THIS FUNCTION REFRESHES THE DROPDOWN MENY WITH COURSE ID
    def dropdown_refresh():
        """
        Refreshes the dropdown menu with the latest list of course IDs.

        This function retrieves the IDs of all courses from the database and updates the 
        dropdown menu with the latest data. If no courses are found, a placeholder message 
        is displayed.
        """
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('SELECT courseID FROM courses')
        courses = cursor.fetchall()
        conn.close()
        courses_ID = [course[0] for course in courses]
        if courses_ID:
            courses_dropdown = tk.OptionMenu(course_tab, selected_ID, *courses_ID)
        else:
            courses_dropdown = tk.OptionMenu(course_tab, selected_ID, "No courses in database")
        courses_dropdown.config(width=21)
        courses_dropdown.grid(row=2, column=4, padx=20, pady=5, sticky="W")
    dropdown_refresh()

    # THIS CLASS ALLOWS COURSE INFORMATION MODIFICATION/DELETION 
    class EditDialog(tk.Toplevel):
        """
        A dialog window that allows courses to be edited or deleted.

        This class creates a modal dialog window where the selected course's information 
        (name) is displayed for editing. It also provides a delete option to remove the 
        course from the database.

        Parameters:
        ----------
            parent (tk.Widget): The parent widget that opens the dialog.
            course_ID (int): The unique ID of the course whose information is being edited.
            selected_ID_var (tk.StringVar): A Tkinter StringVar used to hold the selected course's ID from the dropdown.
            dropdown_menu (tk.OptionMenu): The dropdown menu displaying the list of course IDs.
        """
        def __init__(self, parent, course_ID, selected_ID_var, dropdown_menu):
            super().__init__(parent)
            self.course_ID = course_ID
            self.selected_ID_var = selected_ID_var 
            self.dropdown_menu = dropdown_menu  
            
            conn = sqlite3.connect('school_management.db')
            cursor = conn.cursor()
            self.title("Edit Course")
            tk.Label(self, text="Name:").grid(row=0, column=0, padx=10, pady=10)
            self.name_entry = tk.Entry(self)
            self.name_entry.grid(row=0, column=1, padx=10, pady=10)
            cursor.execute('SELECT courseName FROM courses WHERE courseID = ?', (course_ID,))
            existing_name = cursor.fetchone()
            self.name_entry.insert(0, existing_name)            
            modify_button = tk.Button(self, text="Save", command=self.modify)
            modify_button.grid(row=3, column=1, padx=10, pady=10)
            delete_button = tk.Button(self, text="Delete", command=self.delete)
            delete_button.grid(row=3, column=0, padx=10, pady=10)
        
        def modify(self):
            """
            Modifies the selected course's information in the database.

            This method allows the user to edit the course name. After modification, the
            dropdown menu is updated, and the dialog is closed.
            """
            courseID = self.course_ID 
            conn = sqlite3.connect('school_management.db')
            cursor = conn.cursor()
            if isinstance(courseID, tuple):
                courseID = courseID[0]
            if self.name_entry.get():
                cursor.execute('''
                UPDATE courses
                SET courseName = ?
                WHERE courseID = ?
                ''', (self.name_entry.get(), courseID))
            conn.commit()
            conn.close()
            self.update_dropdown()
            self.destroy()
        
        # THIS METHOD DELETES EXISTING COURSE FROM THE FILE
        def delete(self):
            """
            Deletes the selected course's record from the database.

            This method removes the course's data from the database and refreshes the dropdown 
            menu to reflect the deletion. After deletion, the dialog window is closed.
            """
            courseID = self.course_ID
            #self.student.delete_from_file()
            Course.delete_from_db(courseID,)  
            self.update_dropdown() 
            self.destroy()

        # THIS METHOD UPDATES DROPDOWN MENU AFTER CHANGES OCCUR
        def update_dropdown(self):
            """
            Updates the course ID dropdown menu.

            This method clears the current selection in the dropdown menu and refreshes it 
            with the updated list of course IDs after modifying or deleting a course.
            """
            self.selected_ID_var.set("")
            menu = self.dropdown_menu["menu"]
            menu.delete(0, "end")
            dropdown_refresh()

    # THIS FUNCTIONS OPENS THE EDIT WINDOW WHERE STUDENT CAN EDIT HIS INFORMATION
    def edit_course():
        """
        Opens a dialog window to edit the selected course's information.

        This function retrieves the courseID associated with the selected course from the 
        dropdown menu and opens the `EditDialog` to allow the user to view and edit the 
        course's information.
        """
        course_ID = selected_ID.get()
        EditDialog(None, course_ID, selected_ID, course_id_dropdown)
    
    edit_button = tk.Button(course_tab, text="View Information", command=edit_course)
    edit_button.grid(row=3, column=4, pady=10)



    '''# THIS FUNCTION REFRESHES THE DROPDOWN MENY WITH COURSE ID
    def dropdown_refresh():
        courses = Course.load_from_file()
        course_id = [course.courseID for course in courses]
        if course_id:
            course_id_dropdown = tk.OptionMenu(course_tab, selected_ID, *course_id)
        else:
            course_id_dropdown = tk.OptionMenu(course_tab, selected_ID, "No course in database")
        course_id_dropdown.config(width=21)
        course_id_dropdown.grid(row=2, column=4, padx=20, pady=5, sticky="W")
    dropdown_refresh()'''

    '''# THIS METHOD EDITS/KEEP THE INFORMATION OF THE COURSE
        def modify(self):
            # rename name of course already registered/assigned
            students = Student.load_from_file()
            for student in students:
                if self.course.courseName in student.registered_courses:
                    student.registered_courses.remove(self.course.courseName)
                    student.registered_courses.append(self.name_entry.get())
                    student.save_to_file()  
            instructors = Instructor.load_from_file()
            for instructor in instructors:
                if self.course.courseName in instructor.assigned_courses:
                    instructor.assigned_courses.remove(self.course.courseName)
                    instructor.assigned_courses.append(self.name_entry.get())
                    instructor.save_to_file()  
            # replace course name in course database
            if self.name_entry.get():
                self.course.courseName = self.name_entry.get()
                self.course.save_to_file()
            self.update_dropdown()  
            self.destroy()    '''   
    
    '''# THIS METHOD DELETES EXISTING COURSE FROM FILE
        def delete(self):
            # delete course from registered/assigned courses
            students = Student.load_from_file()
            for student in students:
                if self.course.courseName in student.registered_courses:
                    student.registered_courses.remove(self.course.courseName)
                    student.save_to_file()  
            instructors = Instructor.load_from_file()
            for instructor in instructors:
                if self.course.courseName in instructor.assigned_courses:
                    instructor.assigned_courses.remove(self.course.courseName)
                    instructor.save_to_file()  
            self.course.delete_from_file()
            self.update_dropdown() 
            self.destroy()'''
    
    '''# THIS FUNCTIONS OPENS THE EDIT WINDOW WHERE COURSES' INFORMATION CAN BE EDITED
    def edit_course():
        courses = Course.load_from_file()
        ID = int(selected_ID.get())
        for course in courses:
            if course.courseID == ID:
                EditDialog(None, course, selected_ID, course_id_dropdown)
                break'''
