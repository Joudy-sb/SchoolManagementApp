import json
import os
import sqlite3

from Classes.Person import Instructor, Student

# THIS IS THE CLASS COURSE
class Course:
    # CONSTRUCTOR
    def __init__(self, courseID, courseName, instructor="", enrolledStudents=[]):
        """
        This function create a course object

        Parameters:
        ----------
            courseID (int): The unique identifier for the course.
            courseName (str): The name of the course.
            instructor (str): The name of the instructor assigned to the course (default is an empty string).
            enrolledStudents (list): A list of students enrolled in the course (default is an empty list).

        Raises:
        ------
            ValueError: If the provided courseID is not an integer or is invalid (e.g., empty or None).
        """
        if not isinstance(courseID, int) or not courseID:
            raise ValueError("Invalid course ID provided")        
        self.courseID = courseID
        self.courseName = courseName
        self.instructor = instructor
        self.enrolledStudents = enrolledStudents
    
    # THIS METHOD VALIDATES DATA INPUTED AND ADDS COURSE TO THE DATABASE
    @classmethod
    def create_course(cls, courseID, courseName, instructor=""):
        """
        This method checks whether the provided courseID is unique and not already 
        present in the database. If the ID is valid and unique, a new course instance 
        is created and added to the database.

        Parameters:
        ----------
            courseID (int): The unique identifier for the course.
            courseName (str): The name of the course.
            instructor (str): The name of the instructor assigned to the course (default is an empty string).

        Returns:
        -------
            Course: An instance of the `Course` class.

        Raises:
        ------
            ValueError: If the courseID already exists in the database or if invalid data is provided.
        """
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        # check that id is unique and not already taken
        cursor.execute('''
            SELECT * FROM courses WHERE courseID = ?
        ''', (courseID,))
        existing_course_id = cursor.fetchone()
        if existing_course_id:
            conn.close()
            raise ValueError("Course ID already taken")
        
        course = cls(courseID, courseName, instructor)
        # create course instance in database
        cursor.execute('''
            INSERT INTO courses (courseID, courseName, instructor)
            VALUES (?, ?, ?)
        ''', (courseID, courseName, instructor))
        conn.commit()
        conn.close()
        return course

    # THIS METHOD SAVES DATA OF A COURSE TO THE DATABSE
    def save_to_db(self):
        """
        This method inserts or replaces the current `Course` instance data 
        (courseID, courseName, and instructor) into the `courses` table of the 
        SQLite database.

        Raises:
        ------
            sqlite3.Error: If there is an issue with the database operation.
        """
        conn = sqlite3.connect('school_management.db') 
        cursor = conn.cursor()
        # SQL query to insert or replace course data based on the courseID
        cursor.execute('''
            INSERT OR REPLACE INTO courses (courseID, courseName, instructor)
            VALUES (?, ?, ?)
        ''', (self.courseID, self.courseName, self.instructor))
        conn.commit() 
        conn.close()  
        print(f"Course {self.courseName} saved to the database.")
    
    # THIS METHOD LOADS DATA OF A COURSE FROM THE COURSE DATABASE
    @classmethod
    def load_from_db(cls):
        """
        This method fetches all rows from the `courses` table in the SQLite 
        database, converts each row into a `Course` instance, and returns 
        a list of `Course` objects.

        Returns:
        -------
            list of Course: A list containing instances of `Course` for all courses in the database.

        Raises:
        ------
            sqlite3.Error: If there is an issue with the database operation.
        """
        courses = []
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('SELECT courseID, courseName, instructor FROM courses')
        rows = cursor.fetchall()
        for row in rows:
            courseID, courseName, instructor = row
            courses.append(cls(courseID, courseName, instructor))
        conn.close()
        return courses
    
    # THIS METHOD DELETES COURSE OBJECT FROM DATABASE
    @classmethod
    def delete_from_db(cls,id):
        """
        This method deletes a row from the `courses` table in the SQLite 
        database based on the provided courseID.

        Parameters:
        ----------
            id (int) : The ID of the course to delete.

        Raises:
        ------
            sqlite3.Error: If there is an issue with the database operation.
        """
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM courses WHERE courseID = ?
        ''', (id,))
        conn.commit() 
        conn.close() 
        print(f"Course with ID {id} deleted from the database.")
    
    def get_students_for_course(self, course_id):
        """
        This method fetches the email addresses of all students registered 
        for a particular course using the courseID.

        Parameters:
        ----------
            course_id (int): The ID of the course for which to fetch the list of registered students.

        Returns:
        -------
            list of str: A list of email addresses of students enrolled in the specified course.

        Raises:
        ------
            sqlite3.Error: If there is an issue with the database operation.
        """
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT studentEmail FROM registrations WHERE courseID = ?
        ''', (course_id,))
        student_emails = cursor.fetchall()  
        student_emails = [email[0] for email in student_emails]  
        conn.close()
        return student_emails
    
    
    '''# THIS METHOD VALIDATES DATA INPUTED AND RETURNS THE COURSE OBJECT CREATED
    @classmethod
    def create_course(cls, courseID, courseName, instructor="", enrolledStudents=[]):
        courses = Course.load_from_file()
        for course in courses:
            if courseID == course.courseID:
                raise ValueError("Course ID already taken")
        if not isinstance(courseID, int) or not courseID:
            raise ValueError("Invalid course ID provided")
        return Course(courseID, courseName, instructor, enrolledStudents)'''
    
    '''# THIS METHOD ADDS STUDENT TO ENROLLED COURSE
    def add_student(self,student):
        self.enrolledStudents.append(student)'''
    
    '''# THIS METHOD SAVES DATA OF A COURSE TO THE COURSE DATA FILE
    def save_to_file(self, filename="C:/Users/joudy/Desktop/University-Joods/435L/Lab2/JSON_Data/Courses.json"):
        data = {
            'courseID': self.courseID,
            'courseName': self.courseName,
            'instructor': self.instructor,
            'enrolledStudents': self.enrolledStudents,
        }
        with open(filename, 'r+') as f:
            try:
                courses = json.load(f)
                if isinstance(courses, dict):
                    courses = [courses]
            except json.JSONDecodeError:
                courses = []
            # remove any existing course with the same courseID
            courses = [course for course in courses if course['courseID'] != self.courseID]
            courses.append(data)
            f.seek(0)
            json.dump(courses, f, indent=4)
            f.truncate()'''
    
    '''# THIS METHOD LOADS DATA OF A COURSE FROM THE COURSE DATA FILE (this is a class method because there is no need to create an instance of the class)
    @classmethod
    def load_from_file(cls, filename="C:/Users/joudy/Desktop/University-Joods/435L/Lab2/JSON_Data/Courses.json"):
        courses = []
        try:
            with open(filename, 'r') as f:
                data_list = json.load(f)
                for data in data_list:
                    # turn data into course object
                    courses.append(cls(data['courseID'], data['courseName'], data['instructor'], data['enrolledStudents']))
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        return courses '''
    
    '''# THIS METHOD DELETES A COURSE FROM FILE
    def delete_from_file(self, filename="C:/Users/joudy/Desktop/University-Joods/435L/Lab2/JSON_Data/Courses.json"):
        with open(filename, 'r+') as f:
            try:
                courses = json.load(f)
                if isinstance(courses, dict):
                    courses = [courses]
            except json.JSONDecodeError:
                courses = []
            updated_courses = [course for course in courses if course['courseID'] != self.courseID]
            f.seek(0)
            json.dump(updated_courses, f, indent=4)
            f.truncate()  '''
    
    '''# THIS METHOD ADDS A STUDENT TO IT'S REGISTERED CLASS
    def add_student(self, email):
        self.enrolledStudents.append(email)
        self.save_to_file()
        students = Student.load_from_file()
        for student in students:
            if student.email == email:
                student_obj = student
        student_obj.registered_courses.append(self.courseName)
        student_obj.save_to_file()
    
     # THIS METHOD ADDS AN INSTRUCTOR TO IT'S ASSIGNED CLASS
    def add_instructor(self, email):
        self.instructor = email
        self.save_to_file()
        instructors = Instructor.load_from_file()
        for instructor in instructors:
            if instructor.email == email:
                instructor_obj = instructor
        instructor_obj.assigned_courses.append(self.courseName)
        instructor_obj.save_to_file()

    # THIS METHOD REMOVES A STUDENT TO IT'S REGISTERED CLASS
    def remove_student(self, email):
        self.enrolledStudents.remove(email)
        self.save_to_file()
        students = Student.load_from_file()
        for student in students:
            if student.email == email:
                student_obj = student
        student_obj.registered_courses.remove(self.courseName)
        student_obj.save_to_file()
    
     # THIS METHOD REMOVES AN INSTRUCTOR TO IT'S ASSIGNED CLASS
    def remove_instructor(self, email):
        self.instructor = ""
        self.save_to_file()
        instructors = Instructor.load_from_file()
        for instructor in instructors:
            if instructor.email == email:
                instructor_obj = instructor
        instructor_obj.assigned_courses.remove(self.courseName)
        instructor_obj.save_to_file()'''