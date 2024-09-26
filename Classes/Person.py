import json
import sqlite3

# THIS IS THE SUPER CLASS PERSON
class Person:
    # CONSTRUCTOR OF THE CLASS STUDENT
    def __init__(self, name, age, email):
        """
        This function creates a person object.

        Parameters:
        ----------
            name (str): The name of the person. It must be a non-empty string.
            age (int): The age of the person. It must be a non-negative integer.
            email (str): The email address of the person. It must be a valid AUB email ending with '@mail.aub.edu'.

        Raises:
        ------
            ValueError: If the provided name is not a string or is empty.
            ValueError: If the provided age is not an integer, is negative, or invalid.
            ValueError: If the provided email is not a valid string or does not contain '@mail.aub.edu'.
        """
        if not isinstance(name, str) or not name:
            raise ValueError("Invalid name provided")
        if not isinstance(age, int) or age < 0 or not age:
            raise ValueError("Invalid age provided")
        if '@mail.aub.edu' not in email or not isinstance(email, str) or not email:
            raise ValueError("Invalid email provided")
        self.name = name
        self.age = age
        self.email = email

# --------------------------------------------------------------------------------------------------------

# THIS IS THE SUBCLASS STUDENT 
class Student(Person):
    # CONSTRUCTOR
    def __init__(self, name, age, email, studentID, registered_courses=[]):
        """
        This function creates a Student object and initializes the student's details, including their ID and registered courses.

        Parameters:
        ----------
            name (str): The name of the student. It must be a non-empty string.
            age (int): The age of the student. It must be a non-negative integer.
            email (str): The email address of the student. It must be a valid AUB email ending with '@mail.aub.edu'.
            studentID (int): The unique identifier for the student. It must be a non-empty integer.
            registered_courses (list): A list of courses the student is registered for (default is an empty list).

        Raises:
        ------
            ValueError: If the provided name is not a string or is empty.
            ValueError: If the provided age is not an integer, is negative, or invalid.
            ValueError: If the provided email is not a valid string or does not contain '@mail.aub.edu'.
            ValueError: If the provided studentID is not an integer or is invalid (e.g., empty or None).
        """        
        super().__init__(name, age, email)
        if not isinstance(studentID, int) or not studentID:
            raise ValueError("Invalid student ID provided")
        self.studentID = studentID
        self.registered_courses = registered_courses
    
    # THIS METHOD VALIDATES DATA INPUTED AND ADDS STUDENT TO THE DATABASE
    @classmethod
    def create_student(cls, name, age, email, studentID):
        """
        This method validates the input data and adds a new student to the database.
        It checks whether the provided student ID and email are unique before creating a new
        `Student` object and saving the details in the `students` table of the SQLite database.

        Parameters:
        ----------
            name (str): The name of the student. It must be a non-empty string.
            age (int): The age of the student. It must be a non-negative integer.
            email (str): The email address of the student. It must be a valid AUB email ending with '@mail.aub.edu'.
            studentID (int): The unique identifier for the student. It must be a non-empty integer.

        Returns:
        -------
            Student: An instance of the `Student` class with the provided details.

        Raises:
        ------
            ValueError: If the student ID is already taken.
            ValueError: If the email is already taken.
            ValueError: If the provided name, age, email, or studentID are invalid.
        """
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        # check that id is unique and not already taken
        cursor.execute('''
            SELECT * FROM students WHERE studentID = ?
        ''', (studentID,))
        existing_student_id = cursor.fetchone()
        if existing_student_id:
            conn.close()
            raise ValueError("Student ID already taken")
        # check that email is unique and not already taken
        cursor.execute('''
            SELECT * FROM students WHERE email = ?
        ''', (email,))
        existing_student_email = cursor.fetchone()
        if existing_student_email:
            conn.close()
            raise ValueError("Student email already taken")
        student = cls(name, age, email, studentID)
        # create student instance in database
        cursor.execute('''
            INSERT INTO students (name, age, email, studentID)
            VALUES (?, ?, ?, ?)
        ''', (name, age, email, studentID))
        conn.commit()
        conn.close()
        return student
    
    # THIS METHOD INTRODUCES THE STUDENT
    def introduce(self):
        super().introduce()
        print("ID: " + str(self.studentID))
        print("Registered Courses: " + ", ".join(self.registered_courses))       
    
    # THIS METHOD SAVES DATA OF A STUDENT TO THE DATABSE
    def save_to_db(self):
        """
        Saves the student data to the database.
        This method inserts or replaces the current `Student` instance's data (name, age, email, and studentID)
        in the `students` table of the SQLite database.

        Raises:
        ------
            sqlite3.Error: If there is an issue with the database operation.
        """
        conn = sqlite3.connect('school_management.db') 
        cursor = conn.cursor()
        # SQL query to insert or replace student data based on the studentID
        cursor.execute('''
            INSERT OR REPLACE INTO students (name, age, email, studentID)
            VALUES (?, ?, ?, ?)
        ''', (self.name, self.age, self.email, self.studentID))
        conn.commit() 
        conn.close()  
        print(f"Student {self.name} saved to the database.")
    
    # THIS METHOD LOADS DATA OF A STUDENT FROM THE STUDENT DATABASE
    @classmethod
    def load_from_db(cls):
        """
        Loads all student data from the database and creates a list of `Student` objects.
        This method fetches all rows from the `students` table in the SQLite database, 
        converts each row into a `Student` instance, and returns a list of `Student` objects.

        Returns:
        -------
            list of Student: A list containing instances of `Student` for all students in the database.

        Raises:
        ------
            sqlite3.Error: If there is an issue with the database operation.
        """
        students = []
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, age, email, studentID FROM students')
        rows = cursor.fetchall()
        for row in rows:
            name, age, email, studentID = row
            students.append(cls(name, age, email, studentID))
        conn.close()
        return students
    
    # THIS METHOD DELETES STUDENT OBJECT FROM DATABASE
    @classmethod
    def delete_from_db(cls,id):
        """
        Deletes a student from the database by studentID.
        This method deletes a row from the `students` table in the SQLite 
        database based on the provided studentID.

        Parameters:
        ----------
            id (int): The ID of the student to delete.

        Raises:
        ------
            sqlite3.Error: If there is an issue with the database operation.
        """
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM students WHERE studentID = ?
        ''', (id))
        conn.commit() 
        conn.close() 
        print(f"Student with ID {id} deleted from the database.")

# --------------------------------------------------------------------------------------------------------

# THIS IS THE SUBCLASS INSTRUCTOR
class Instructor(Person):
    # CONSTRUCTOR 
    def __init__(self, name, age, email, instructorID, assigned_courses=[]):
        """
        Initializes an Instructor object with the provided details.

        Parameters:
        ----------
            name (str): The name of the instructor. It must be a non-empty string.
            age (int): The age of the instructor. It must be a non-negative integer.
            email (str): The email address of the instructor. It must be a valid AUB email ending with '@mail.aub.edu'.
            instructorID (int): The unique identifier for the instructor. It must be a non-empty integer.
            assigned_courses (list): A list of courses assigned to the instructor (default is an empty list).

        Raises:
        ------
            ValueError: If the provided name, age, email, or instructorID are invalid.
        """        
        super().__init__(name, age, email)
        if not isinstance(instructorID, int) or not instructorID:
            raise ValueError("Invalid instructor ID provided")
        self.instructorID = instructorID
        self.assigned_courses = assigned_courses

    # THIS METHOD VALIDATES DATA INPUTED AND ADDS INSTRUCTOR TO THE DATABASE
    @classmethod
    def create_instructor(cls, name, age, email, instructorID):
        """
        Validates the input data and adds a new instructor to the database.
        This method checks whether the provided instructor ID and email are unique before 
        creating a new `Instructor` object and saving the details in the `instructors` table 
        of the SQLite database.

        Parameters:
        ----------
            name (str): The name of the instructor. It must be a non-empty string.
            age (int): The age of the instructor. It must be a non-negative integer.
            email (str): The email address of the instructor. It must be a valid AUB email ending with '@mail.aub.edu'.
            instructorID (int): The unique identifier for the instructor. It must be a non-empty integer.

        Returns:
        -------
            Instructor: An instance of the `Instructor` class with the provided details.

        Raises:
        ------
            ValueError: If the instructor ID or email is already taken.
            ValueError: If the provided name, age, email, or instructorID are invalid.
        """
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        # check that id is unique and not already taken
        cursor.execute('''
            SELECT * FROM instructors WHERE instructorID = ?
        ''', (instructorID,))
        existing_instructor_id = cursor.fetchone()
        if existing_instructor_id:
            conn.close()
            raise ValueError("Instructor ID already taken")
        # check that email is unique and not already taken
        cursor.execute('''
            SELECT * FROM instructors WHERE email = ?
        ''', (email,))
        existing_instructor_email = cursor.fetchone()
        if existing_instructor_email:
            conn.close()
            raise ValueError("Instructor email already taken")
        instructor = cls(name, age, email, instructorID)
        # create student instance in database
        cursor.execute('''
            INSERT INTO instructors (name, age, email, instructorID)
            VALUES (?, ?, ?, ?)
        ''', (name, age, email, instructorID))
        conn.commit()
        conn.close()
        return instructor
    
    # THIS METHOD ADDS COURSE TO ASSIGNED COURSES
    def assign_course(self, course):
        self.assigned_courses.append(course)
    
    # THIS METHOD INTRODUCES THE INSTRUCTOR
    def introduce(self):
        super().introduce()
        print("ID: " + str(self.instructorID))
        print("Assigned Courses: " + ", ".join(self.assigned_courses))

    # THIS METHOD SAVES DATA OF A INSTRUCTOR TO THE DATABSE
    def save_to_db(self):
        """
        Saves the instructor's data to the database.
        This method inserts or replaces the current `Instructor` instance's data 
        (name, age, email, and instructorID) in the `instructors` table of the SQLite database.

        Raises:
        ------
            sqlite3.Error: If there is an issue with the database operation.
        """
        conn = sqlite3.connect('school_management.db') 
        cursor = conn.cursor()
        # SQL query to insert or replace instructor data based on the instructorID
        cursor.execute('''
            INSERT OR REPLACE INTO instructors (name, age, email, instructorID)
            VALUES (?, ?, ?, ?)
        ''', (self.name, self.age, self.email, self.instructorID))
        conn.commit() 
        conn.close()  
        print(f"Instructor {self.name} saved to the database.")
    
    # THIS METHOD LOADS DATA OF A INSTRUCTOR FROM THE INSTRUCTOR DATABASE
    @classmethod
    def load_from_db(cls):
        """
        Loads all instructor data from the database and creates a list of `Instructor` objects.
        This method fetches all rows from the `instructors` table in the SQLite database, 
        converts each row into an `Instructor` instance, and returns a list of `Instructor` objects.

        Returns:
        -------
            list of Instructor: A list containing instances of `Instructor` for all instructors in the database.

        Raises:
        ------
            sqlite3.Error: If there is an issue with the database operation.
        """
        instructors = []
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, age, email, instructorID FROM instructors')
        rows = cursor.fetchall()
        for row in rows:
            name, age, email, instructorID = row
            instructors.append(cls(name, age, email, instructorID))
        conn.close()
        return instructors    
    
    # THIS METHOD DELETES AN INSTRUCTOR OBJECT FROM DATABASE
    @classmethod
    def delete_from_db(cls,id):
        """
        Deletes an instructor from the database by instructorID.
        This method deletes a row from the `instructors` table in the SQLite database 
        based on the provided instructorID.

        Parameters:
        ----------
            id (int): The ID of the instructor to delete.

        Raises:
        ------
            sqlite3.Error: If there is an issue with the database operation.
        """    
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM instructors WHERE instructorID = ?
        ''', (id))
        conn.commit() 
        conn.close() 
        print(f"Instructor with ID {id} deleted from the database.")   


    '''
    ------------------------------------------------------------------------------------------------------------
    # THIS METHOD INTRODUCES THE PERSON
    def introduce(self):
        print("Name: " + self.name)
        print("Age: " + str(self.age))
        print("Email: " + self.email)'''

    '''# THIS METHOD VALIDATES DATA INPUTED AND RETURNS THE STUDENT OBJECT CREATED
    @classmethod
    def create_student(cls, name, age, email, studentID, registered_courses=[]):
        students = Student.load_from_file()
        for student in students:
            if studentID == student.studentID:
                raise ValueError("Student ID already taken")
            if email == student.email:
                raise ValueError("Student email already taken")
        return Student(name, age, email, studentID, registered_courses)'''
    
    '''# THIS METHOD SAVES DATA OF A STUDENT TO THE STUDENT DATA FILE
    def save_to_file(self, filename="C:/Users/joudy/Desktop/University-Joods/435L/Lab2/JSON_Data/Students.json"):
        data = {
            'name': self.name,
            'age': self.age,
            'email': self.email,
            'studentID': self.studentID,
            'registered_courses': self.registered_courses
        }
        with open(filename, 'r+') as f:
            try:
                persons = json.load(f)
                if isinstance(persons, dict):
                    persons = [persons]
            except json.JSONDecodeError:
                persons = []
            # remove old version/ duplicates
            persons = [person for person in persons if person['studentID'] != self.studentID]
            persons.append(data)
            f.seek(0)
            json.dump(persons, f, indent=4)
            f.truncate()     '''
    
    '''# THIS METHOD LOADS DATA OF A STUDENT FROM THE STUDENT DATA FILE (this is a class method because there is no need to create an instance of the class)
    @classmethod
    def load_from_file(cls, filename="C:/Users/joudy/Desktop/University-Joods/435L/Lab2/JSON_Data/Students.json"):
        persons = []
        try:
            with open(filename, 'r') as f:
                data_list = json.load(f)
                for data in data_list:
                    persons.append(cls(data['name'], data['age'], data['email'], data['studentID'], data['registered_courses']))
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        return persons'''
    
    '''# THIS METHOD DELETES STUDENT OBJECT FROM FILE
    def delete_from_file(self, filename="C:/Users/joudy/Desktop/University-Joods/435L/Lab2/JSON_Data/Students.json"):
        with open(filename, 'r+') as f:
            try:
                persons = json.load(f)
                if isinstance(persons, dict):
                    persons = [persons]
            except json.JSONDecodeError:
                persons = []
            updated_persons = [person for person in persons if person['studentID'] != self.studentID]
            f.seek(0)
            json.dump(updated_persons, f, indent=4)
            f.truncate() ''' 

    '''# THIS METHOD VALIDATES DATA INPUTED AND RETURNS THE INSTRUCTOR OBJECT CREATED
    @classmethod
    def create_instructor(cls, name, age, email, instructorID, assigned_courses=[]):
        instructors = Instructor.load_from_file()
        for instructor in instructors:
            if instructorID == instructor.instructorID:
                raise ValueError("Instructor ID already taken")
            if email == instructor.email:
                raise ValueError("Instructor email already taken")
        return Instructor(name, age, email, instructorID, assigned_courses)'''
            
    '''# THIS METHOD SAVES DATA OF A INSTRUCTOR TO THE INSTRUCTOR DATA FILE
    def save_to_file(self, filename="C:/Users/joudy/Desktop/University-Joods/435L/Lab2/JSON_Data/Instructors.json"):
        data = {
            'name': self.name,
            'age': self.age,
            'email': self.email,
            'instructorID': self.instructorID,
            'assigned_courses': self.assigned_courses
        }
        with open(filename, 'r+') as f:
            try:
                persons = json.load(f)
                if isinstance(persons, dict):
                    persons = [persons]
            except json.JSONDecodeError:
                persons = []
            # remove duplicates
            persons = [person for person in persons if person['instructorID'] != self.instructorID]
            persons.append(data)
            f.seek(0)
            json.dump(persons, f, indent=4)
            f.truncate() '''           

    '''# THIS METHOD LOADS DATA OF A STUDENT FROM THE STUDENT DATA FILE (this is a class method because there is no need to create an instance of the class)
    @classmethod
    def load_from_file(cls, filename="C:/Users/joudy/Desktop/University-Joods/435L/Lab2/JSON_Data/Instructors.json"):
        persons = []
        try:
            with open(filename, 'r') as f:
                data_list = json.load(f)
                for data in data_list:
                    persons.append(cls(data['name'], data['age'], data['email'], data['instructorID'], data['assigned_courses']))
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        return persons'''
    
    '''# THIS METHOD DELETES INSTRUCTOR OBJECT FROM FILE
    def delete_from_file(self, filename="C:/Users/joudy/Desktop/University-Joods/435L/Lab2/JSON_Data/Instructors.json"):
        with open(filename, 'r+') as f:
            try:
                persons = json.load(f)
                if isinstance(persons, dict):
                    persons = [persons]
            except json.JSONDecodeError:
                persons = []
            updated_persons = [person for person in persons if person['instructorID'] != self.instructorID]
            f.seek(0)
            json.dump(updated_persons, f, indent=4)
            f.truncate() '''