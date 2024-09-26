import sqlite3
import tkinter as tk
from tkinter import font
from Classes.Course import Course
from Classes.Person import Student, Instructor

def create_register_tab(notebook):
    """
    Creates the 'Register/Assign' tab in the notebook UI.

    This function adds a tab to the provided notebook where users can register or assign courses 
    to students or instructors. It also includes a section to unregister/unassign courses.

    Parameters:
    ----------
        notebook (tk.Notebook): The Tkinter notebook widget to which the 'Register/Assign' tab will be added.
    """
    register_tab = tk.Frame(notebook)
    notebook.add(register_tab, text="Register/Assign")

    # THIS PART IS FOR REGISTERING/ASSIGNING COURSES TO STUDENTS/INSTRUCTORS
    bold_font = font.Font(size=14, weight="bold")
    course_level_label = tk.Label(register_tab, text="Register/Assign Course", font=bold_font)
    course_level_label.grid(row=0, column=0, padx=20, pady=5)

    # THIS FUNCTION UPDATE THE DROPDOWN BUTTON BASED ON ROLE TYPE
    def update_dropdown():
        """
        Updates the dropdown menu with the emails of students or instructors based on the selected role.

        This function populates the dropdown menu with either student or instructor email addresses 
        depending on the role (student or instructor) selected by the user.
        """
        selected_name.set("") 
        selected_course.set("") 
        selected_role = role_var.get()
        menu = student_dropdown["menu"]
        menu.delete(0, "end")
        # if it's a student, register course
        if selected_role == "Student":
            students = Student.load_from_db()
            students_email = [student.email for student in students]
            for email in students_email:
                menu.add_command(label=email, command=lambda value=email: selected_name.set(value))
        # if it's an instructor, assign course
        elif selected_role == "Instructor":
            instructors = Instructor.load_from_db()
            instructors_email = [instructor.email for instructor in instructors]
            for email in instructors_email:
                menu.add_command(label=email, command=lambda value=email: selected_name.set(value))

    role_var = tk.StringVar(value="Student")  
    course_level_label = tk.Label(register_tab, text="Select your role")
    course_level_label.grid(row=1, column=0, padx=20, pady=5)
    student_radio = tk.Radiobutton(register_tab, text="Student", variable=role_var, value="Student", command=update_dropdown)
    student_radio.grid(row=2, column=0, padx=20, pady=5)
    instructor_radio = tk.Radiobutton(register_tab, text="Instructor", variable=role_var, value="Instructor", command=update_dropdown)
    instructor_radio.grid(row=2, column=1, padx=20, pady=5)

    student_label = tk.Label(register_tab, text="Select your email")
    student_label.grid(row=3, column=0, padx=20, pady=5)
    selected_name = tk.StringVar(value="")

    # default values in dropdown
    students = Student.load_from_db()
    students_email = [student.email for student in students]
    if students_email:
        student_dropdown = tk.OptionMenu(register_tab, selected_name, *students_email)
    else:
        student_dropdown = tk.OptionMenu(register_tab, selected_name, "No students available")
    student_dropdown.config(width=21)
    student_dropdown.grid(row=4, column=0, columnspan = 2, padx=20, pady=5)

    # THIS FUNCTIONS RETURNS THE COURSEID OF THE COURSES THAT THE STUDENT IS TAKING
    def get_student_courses(email):
        """
        Retrieves the course IDs of courses that a student is currently registered for.

        This function queries the database to get all course IDs associated with a specific student.

        Parameters:
        ----------
            email (str): The email address of the student.

        Returns:
        -------
            list of int: A list of course IDs that the student is registered for.
        """
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT courseID FROM registrations WHERE studentEmail = ?
        ''', (email,))
        course_ids = cursor.fetchall()  
        course_ids = [course_id[0] for course_id in course_ids]  
        conn.close()
        return course_ids
    
    # THIS FUNCTIONS RETURNS THE COURSEID OF THE COURSES THAT THE INSTRUCTOR IS TAKING
    def get_instructor_courses(email):
        """
        Retrieves the course IDs of courses assigned to a specific instructor.

        This function queries the database to get all course IDs associated with a specific instructor.

        Parameters:
        ----------
            email (str): The email address of the instructor.

        Returns:
        -------
            list of int: A list of course IDs that the instructor is assigned to.
        """
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT courseID FROM courses WHERE instructor = ?
        ''', (email,))
        course_ids = cursor.fetchall()  
        course_ids = [course_id[0] for course_id in course_ids]  
        conn.close()
        return course_ids      
        
    # THIS FUNCTIONS RETURNS COURSES THE STUDENT/INSTRUCTOR CAN REGISTER/ASSIGN
    def submit_email():
        """
        Updates the course dropdown menu with unregistered/unassigned courses based on the selected role.

        This function updates the dropdown menu to display only the courses that a student or instructor 
        has not yet registered for (if student) or been assigned to (if instructor).

        It fetches all course IDs from the database and filters out the courses that the selected student 
        or instructor has already registered for or been assigned to.

        Returns:
        -------
            None
        """
        selected_course.set("") 
        roleVar = role_var.get()
        unregistered_courses = []
        email = selected_name.get()
        courses = Course.load_from_db()  
        course_ID = [course.courseID for course in courses]  
        
        if roleVar == "Student":
            registered_courses = get_student_courses(email)
            for course in course_ID:
                if course not in registered_courses:
                    unregistered_courses.append(course)
            if unregistered_courses:
                # show only courses unregistered to the student
                course_dropdown = tk.OptionMenu(register_tab, selected_course, *unregistered_courses)
            else:
                course_dropdown = tk.OptionMenu(register_tab, selected_course, "No courses available")
            course_dropdown.config(width=21)
            course_dropdown.grid(row=6, column=0, columnspan=2, padx=20, pady=5)
        
        elif roleVar == "Instructor":
            registered_courses = get_instructor_courses(email)
            for course in course_ID:
                if course not in registered_courses:
                    unregistered_courses.append(course)
            if unregistered_courses:
                # show only courses unassigned to the instructor
                course_dropdown = tk.OptionMenu(register_tab, selected_course, *unregistered_courses)
            else:
                course_dropdown = tk.OptionMenu(register_tab, selected_course, "No courses available")
            course_dropdown.config(width=21)
            course_dropdown.grid(row=6, column=0, columnspan=2, padx=20, pady=5)

        return

    submit__email = tk.Button(register_tab, text="Choose", command=submit_email)
    submit__email.grid(row=4, column=1, pady=10)

    course_label = tk.Label(register_tab, text="Select a Course")
    course_label.grid(row=5, column=0, padx=20, pady=5)
    selected_course = tk.StringVar(value="")
    course_dropdown = tk.OptionMenu(register_tab, selected_course, "No courses available")
    course_dropdown.config(width=21)
    course_dropdown.grid(row=6, column=0, columnspan = 2,padx=20, pady=5)   

    # THIS FUNCTIONS REGISTERS A COURSE 
    def submit_course_registration():
        """
        Registers or assigns a selected course to a student or instructor based on the selected role.

        This function either registers a course to a student or assigns a course to an instructor, 
        depending on the selected role (student or instructor).

        Returns:
        -------
            None
        """
        roleVar = role_var.get()
        email = selected_name.get()
        course_ID = selected_course.get()

        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        if roleVar == "Student":
            cursor.execute('''
                INSERT INTO registrations (studentEmail, courseID)
                VALUES (?,?)
            ''', (email, course_ID))
        elif roleVar == "Instructor":
            cursor.execute('''
                UPDATE courses
                SET instructor = ?
                WHERE courseID = ?  
            ''', (email, course_ID))

        conn.commit()
        conn.close()
        selected_name.set("") 
        selected_course.set("") 
        return

    submit_registration_course = tk.Button(register_tab, text="Register", command=submit_course_registration)
    submit_registration_course.grid(row=6, column=1, columnspan=2, pady=10)

# --------------------------------------------------------------------------------------------------------

    # THIS PART IS FOR UNREGISTERING/UNASSIGNING COURSES TO STUDENTS/INSTRUCTORS
    course_unregister_label = tk.Label(register_tab, text="Unregister/Unassign Course", font=bold_font)
    course_unregister_label.grid(row=0, column=4, padx=20, pady=5)

    # THIS FUNCTION UPDATE THE DROPDOWN BUTTON BASED ON ROLE TYPE
    def update_dropdown_unregister():
        """
        Updates the dropdown menu with the emails of students or instructors for course unregistration/unassignment.

        This function populates the dropdown menu with either student or instructor email addresses 
        depending on the role selected by the user. The emails correspond to users who are already 
        registered for or assigned to courses.
        """
        selected_name_unregistered.set("")  
        selected_course_unregistered.set("")  
        selected_role = role_var_unregistered.get()
        menu = student_dropdown_unregistered["menu"]
        menu.delete(0, "end")
        # if it's a student, unregister course
        if selected_role == "Student":
            students = Student.load_from_db()
            students_email = [student.email for student in students]
            for email in students_email:
                menu.add_command(label=email, command=lambda value=email: selected_name_unregistered.set(value))
        # if it's an instructor, unassign course
        elif selected_role == "Instructor":
            instructors = Instructor.load_from_db()
            instructors_email = [instructor.email for instructor in instructors]
            for email in instructors_email:
                menu.add_command(label=email, command=lambda value=email: selected_name_unregistered.set(value))

    role_var_unregistered = tk.StringVar(value="Student")  
    course_unregisterRole_label = tk.Label(register_tab, text="Select your role")
    course_unregisterRole_label.grid(row=1, column=4, padx=20, pady=5)
    student_radio_unregistered = tk.Radiobutton(register_tab, text="Student", variable=role_var_unregistered, value="Student", command=update_dropdown_unregister)
    student_radio_unregistered.grid(row=2, column=4, padx=20, pady=5)
    instructor_radio_unregistered = tk.Radiobutton(register_tab, text="Instructor", variable=role_var_unregistered, value="Instructor", command=update_dropdown_unregister)
    instructor_radio_unregistered.grid(row=2, column=5, padx=20, pady=5)

    student_label_unregistered = tk.Label(register_tab, text="Select your email")
    student_label_unregistered.grid(row=3, column=4, padx=20, pady=5)
    selected_name_unregistered = tk.StringVar(value="")

    # default values in dropdown
    students = Student.load_from_db()
    students_email_unregistered = [student.email for student in students]
    if students_email_unregistered:
        student_dropdown_unregistered = tk.OptionMenu(register_tab, selected_name_unregistered, *students_email_unregistered)
    else:
        student_dropdown_unregistered = tk.OptionMenu(register_tab, selected_name_unregistered, "No students available")
    student_dropdown_unregistered.config(width=21)
    student_dropdown_unregistered.grid(row=4, column=4, columnspan = 2, padx=20, pady=5)

    # THIS FUNCTIONS RETURNS COURSES THE STUDENT/INSTRUCTOR CAN UNREGISTER/UNASSIGN
    def submit_email_unregister():
        """
        Updates the course dropdown menu with registered/assigned courses for unregistration/unassignment.

        This function updates the dropdown menu to display only the courses that the selected student 
        or instructor is currently registered for (if student) or assigned to (if instructor).

        Returns:
        -------
            None
        """
        selected_course_unregistered.set("")  
        roleVar = role_var_unregistered.get()
        unregisteredCourses = []
        email = selected_name_unregistered.get()
        courses = Course.load_from_db()  
        course_ID = [course.courseID for course in courses]  
        
        if roleVar == "Student":
            registered_courses = get_student_courses(email)
            for course in course_ID:
                if course in registered_courses:
                    unregisteredCourses.append(course)
            if unregisteredCourses:
                # show only courses registered by the student
                course_dropdown_unregistered = tk.OptionMenu(register_tab, selected_course_unregistered, *unregisteredCourses)
            else:
                course_dropdown_unregistered = tk.OptionMenu(register_tab, selected_course_unregistered, "No courses available")
            course_dropdown_unregistered.config(width=21)
            course_dropdown_unregistered.grid(row=6, column=4, columnspan = 2, padx=20, pady=5)
        
        elif roleVar == "Instructor":
            registered_courses = get_instructor_courses(email)
            for course in course_ID:
                if course in registered_courses:
                    unregisteredCourses.append(course)
            if unregisteredCourses:
                # show only courses assigned to the instructor
                course_dropdown_unregistered = tk.OptionMenu(register_tab, selected_course_unregistered, *unregisteredCourses)
            else:
                course_dropdown_unregistered = tk.OptionMenu(register_tab, selected_course_unregistered, "No courses available")
            course_dropdown_unregistered.config(width=21)
            course_dropdown_unregistered.grid(row=6, column=4, columnspan = 2, padx=20, pady=5)

        return

    submit__email = tk.Button(register_tab, text="Choose", command=submit_email_unregister)
    submit__email.grid(row=4, column=5, pady=10)
        
    course_label_unregistered = tk.Label(register_tab, text="Select a Course")
    course_label_unregistered.grid(row=5, column=4, padx=20, pady=5)
    selected_course_unregistered = tk.StringVar(value="")
    course_dropdown_unregistered = tk.OptionMenu(register_tab, selected_course_unregistered, "No courses available")
    course_dropdown_unregistered.config(width=21)
    course_dropdown_unregistered.grid(row=6, column=4, columnspan = 2, padx=20, pady=5)   

    # THIS FUNCTIONS UNREGISTERS A COURSE 
    def submit_course_unregistration():
        """
        Unregisters or unassigns a selected course from a student or instructor based on the selected role.

        This function either unregisters a course from a student or unassigns a course from an instructor, 
        depending on the selected role (student or instructor).

        Returns:
        -------
            None
        """
        roleVar = role_var_unregistered.get()
        email = selected_name_unregistered.get()
        course_ID = selected_course_unregistered.get()

        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        if roleVar == "Student":
            cursor.execute('''
                DELETE FROM registrations
                WHERE studentEmail = ? AND courseID = ?
            ''', (email, course_ID))
        elif roleVar == "Instructor":
            cursor.execute('''
                UPDATE courses
                SET instructor = ?
                WHERE courseID = ?  
            ''', ("", course_ID))

        conn.commit()
        conn.close()

        selected_name_unregistered.set("")  
        selected_course_unregistered.set("")  
        return 

    submit_unregistration_course = tk.Button(register_tab, text="Unregister", command=submit_course_unregistration)
    submit_unregistration_course.grid(row=6, column=5, columnspan=2, pady=10)

    '''# THIS FUNCTIONS REGISTERS A COURSE 
    def submit_course_registration():
        roleVar = role_var.get()
        email = selected_name.get()
        course_name = selected_course.get()
        courses = Course.load_from_file()
        for course in courses:
            if course.courseName == course_name:
                course_obj = course
        if roleVar == "Student":
            course_obj.add_student(email)
        elif roleVar == "Instructor":
            course_obj.add_instructor(email)
        selected_name.set("") 
        selected_course.set("")  
        return''' 
    