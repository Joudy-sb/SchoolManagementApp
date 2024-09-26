import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import font
from Classes.Course import Course
from Classes.Person import Student, Instructor

def create_viewall_tab(notebook):
    """
    Creates the 'View All' tab in the notebook UI.

    This function adds a tab where users can view all students, instructors, and courses.
    It provides buttons to view each category and initializes with viewing students.

    Parameters:
    ----------
        notebook (tk.Notebook): The Tkinter notebook widget to which the 'View All' tab will be added.
    """
    viewall_tab = tk.Frame(notebook)
    notebook.add(viewall_tab, text="View All")
    view_students(viewall_tab)

    bold_font = font.Font(size=14, weight="bold")
    course_label = tk.Label(viewall_tab, text="Database", font=bold_font)
    course_label.grid(row=0, column=0,padx=20, pady=5, sticky="W")
    # view all students button
    view_student_button = tk.Button(viewall_tab, text="View Students", command=lambda: view_students(viewall_tab))
    view_student_button.grid(row=3, column=0, padx=5, pady=5)
    # view all instructor button  
    view_instructor_button = tk.Button(viewall_tab, text="View Instructors", command=lambda: view_instructors(viewall_tab))
    view_instructor_button.grid(row=3, column=1, padx=5, pady=5)
    # view all courses button  
    view_courses_button = tk.Button(viewall_tab, text="View Courses", command=lambda: view_courses(viewall_tab))
    view_courses_button.grid(row=3, column=2, padx=5, pady=5)
    viewall_tab.grid_rowconfigure(1, weight=1)  
    viewall_tab.grid_columnconfigure(0, weight=1) 
    viewall_tab.grid_columnconfigure(1, weight=1)  
    viewall_tab.grid_columnconfigure(2, weight=1)  

# THIS FUNCTION ALLOWS USER TO VIEW ALL INSTRUCTORS
def view_instructors(viewall_tab):
    """
    Displays all instructors in the database in a treeview widget.

    This function fetches instructor data from the database and displays it in a treeview.
    Users can also search for instructors by name, email, or assigned courses.

    Parameters:
    ----------
        viewall_tab (tk.Frame): The Tkinter frame widget where the treeview will be displayed.
    """
    for widget in viewall_tab.winfo_children():
        if isinstance(widget, ttk.Treeview):
            widget.destroy()
    search_label = tk.Label(viewall_tab, text="Search:")
    search_label.grid(row=1, column=0, padx=10, pady=5)
    search_var = tk.StringVar()
    search_entry = tk.Entry(viewall_tab, textvariable=search_var)
    search_entry.grid(row=1, column=1, padx=10, pady=5, sticky="W")
    tree = ttk.Treeview(viewall_tab, columns=("name", "age", "email", "instructorID", "assigned_courses"), show='headings')
    tree.heading("name", text="Name")
    tree.heading("age", text="Age")
    tree.heading("email", text="Email")
    tree.heading("instructorID", text="Instructor ID")
    tree.heading("assigned_courses", text="Assigned Courses")
    tree.column("name", width=100)
    tree.column("age", width=50)
    tree.column("email", width=150)
    tree.column("instructorID", width=100)
    tree.column("assigned_courses", width=150)
    tree.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky='nsew')
    def update_treeview(search_query):
        tree.delete(*tree.get_children()) 
        instructors = Instructor.load_from_db() 
        courses = Course.load_from_db() 
        for instructor in instructors:
            course_instructor = []
            for course in courses:
                if course.instructor == instructor.email:
                    course_instructor.append(course.courseName)  
            courseInstructor = ", ".join(course_instructor) if course_instructor else "None"
            if (search_query.lower() in instructor.name.lower() or
                search_query.lower() in instructor.email.lower() or
                search_query.lower() in courseInstructor.lower()):
                tree.insert("", "end", values=(instructor.name, instructor.age, instructor.email, instructor.instructorID, courseInstructor))
    search_var.trace("w", lambda name, index, mode: update_treeview(search_var.get()))
    update_treeview("")

# THIS FUNCTIONS RETURNS THE NAME OF THE COURSES THAT THE STUDENT IS TAKING
def get_student_courses(email):
    """
    Retrieves the names of the courses a student is registered for.

    This function queries the database to get all course IDs associated with a specific student,
    and then fetches the corresponding course names.

    Parameters:
    ----------
        email (str): The email address of the student.

    Returns:
    -------
        list of str: A list of course names the student is registered for.
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT courseID FROM registrations WHERE studentEmail = ?
    ''', (email,))
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

# THIS FUNCTION ALLOWS USER TO VIEW ALL STUDENTS
def view_students(viewall_tab):
    """
    Displays all students in the database in a treeview widget.

    This function fetches student data from the database and displays it in a treeview.
    Users can also search for students by name, email, or registered courses.

    Parameters:
    ----------
        viewall_tab (tk.Frame): The Tkinter frame widget where the treeview will be displayed.
    """
    for widget in viewall_tab.winfo_children():
        if isinstance(widget, ttk.Treeview):
            widget.destroy()
    search_label = tk.Label(viewall_tab, text="Search:")
    search_label.grid(row=1, column=0, padx=10, pady=5)
    search_var = tk.StringVar()
    search_entry = tk.Entry(viewall_tab, textvariable=search_var)
    search_entry.grid(row=1, column=1, padx=10, pady=5, sticky="W")
    tree = ttk.Treeview(viewall_tab, columns=("name", "age", "email", "studentID", "registered_courses"), show='headings')
    tree.heading("name", text="Name")
    tree.heading("age", text="Age")
    tree.heading("email", text="Email")
    tree.heading("studentID", text="Students ID")
    tree.heading("registered_courses", text="Registered Courses")
    tree.column("name", width=100)
    tree.column("age", width=50)
    tree.column("email", width=150)
    tree.column("studentID", width=100)
    tree.column("registered_courses", width=150)
    tree.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky='nsew')
    def update_treeview(search_query):
        tree.delete(*tree.get_children()) 
        students = Student.load_from_db()  
        for student in students:
            registered_courses = get_student_courses(student.email)  
            registered_courses_str = ", ".join(registered_courses) if registered_courses else "None"  
            if (search_query.lower() in student.name.lower() or
                search_query.lower() in student.email.lower() or
                search_query.lower() in registered_courses_str.lower()):
                tree.insert("", "end", values=(student.name, student.age, student.email, student.studentID, registered_courses_str))
    search_var.trace("w", lambda name, index, mode: update_treeview(search_var.get()))
    update_treeview("")

# THIS FUNCTION ALLOWS USER TO VIEW ALL COURSES
def view_courses(viewall_tab):
    """
    Displays all courses in the database in a treeview widget.

    This function fetches course data from the database and displays it in a treeview.
    Users can also search for courses by name, instructor, or enrolled students.

    Parameters:
    ----------
        viewall_tab (tk.Frame): The Tkinter frame widget where the treeview will be displayed.
    """
    for widget in viewall_tab.winfo_children():
        if isinstance(widget, ttk.Treeview):
            widget.destroy()
        search_label = tk.Label(viewall_tab, text="Search:")
    search_label.grid(row=1, column=0, padx=10, pady=5)
    search_var = tk.StringVar()
    search_entry = tk.Entry(viewall_tab, textvariable=search_var)
    search_entry.grid(row=1, column=1, padx=10, pady=5, sticky="W")
    tree = ttk.Treeview(viewall_tab, columns=("name", "courseID", "instructor", "enrolled_students"), show='headings')
    tree.heading("name", text="Course Name")
    tree.heading("courseID", text="Course ID")
    tree.heading("instructor", text="Instructor")
    tree.heading("enrolled_students", text="Enrolled Students")
    tree.column("name", width=100)
    tree.column("courseID", width=150)
    tree.column("instructor", width=150)
    tree.column("enrolled_students", width=150)
    tree.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky='nsew')
    def update_treeview(search_query):
        tree.delete(*tree.get_children())  
        courses = Course.load_from_db() 
        for course in courses:
            enrolled_students = course.get_students_for_course(course.courseID) 
            enrolled_students_str = ", ".join(enrolled_students) if enrolled_students else "None"  
            if (search_query.lower() in course.courseName.lower() or
                search_query.lower() in course.instructor.lower() or
                search_query.lower() in enrolled_students_str.lower()):
                tree.insert("", "end", values=(course.courseName, course.courseID, course.instructor, enrolled_students_str))
    search_var.trace("w", lambda name, index, mode: update_treeview(search_var.get()))
    update_treeview("")

