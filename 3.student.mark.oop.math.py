import math
import numpy as np
import curses

class Student:
    def __init__(self, sid="", name="", dob=""):
        self.__student_id = sid
        self.__name = name
        self.__dob = dob

    def get_id(self):
        return self.__student_id

    def get_name(self):
        return self.__name

    def get_dob(self):
        return self.__dob

    def set_id(self, sid):
        self.__student_id = sid

    def set_name(self, name):
        self.__name = name

    def set_dob(self, dob):
        self.__dob = dob

    def student_input(self):
        self.__student_id = input("Student ID: ")
        self.__name = input("Student name: ")
        self.__dob = input("Date of birth (mm/dd/yyyy): ")

    def student_display(self):
        print(f"ID: {self.__student_id}, Name: {self.__name}, DoB: {self.__dob}")


class Course:
    def __init__(self, cid="", cname="", credits = 0):
        self.__course_id = cid
        self.__course_name = cname
        self.__credits = credits

    def get_cid(self):
        return self.__course_id

    def get_cname(self):
        return self.__course_name
    
    def get_credits(self):
        return self.__credits

    def set_cid(self, cid):
        self.__course_id = cid

    def set_cname(self, cname):
        self.__course_name = cname
    
    def set_credits(self, credits):
        self.__credits = credits

    def course_input(self):
        self.__course_id = input("Course ID: ")
        self.__course_name = input("Course name: ")
        self.__credits = int(input("Number of credits: "))

    def course_display(self):
        print(f"Course ID: {self.__course_id}, Course name: {self.__course_name}, Number of credits: {self.__credits}")


class StudentList:
    def __init__(self):
        self.__students = []

    def number_of_students(self):
        n = int(input("Enter the number of students: "))
        for i in range(n):
            print(f"\nEntering student {i+1}:")
            s = Student()
            s.student_input()
            self.__students.append(s)

    def slist(self):
        print("\nStudent info:")
        for s in self.__students:
            s.student_display()

    def get_all(self):
        return self.__students

    def sort_numpy(self):
        arr = np.array(self.__students, dtype=object)

        ids = np.array([int(s.get_id()) for s in arr])

        sorted_indices = np.argsort(ids)[::-1]

        self.__students = arr[sorted_indices].tolist()

class CourseList:
    def __init__(self):
        self.__courses = []

    def number_of_courses(self):
        n = int(input("Enter the number of courses: "))
        for i in range(n):
            print(f"\nEntering course {i+1}:")
            c = Course()
            c.course_input()
            self.__courses.append(c)

    def clist(self):
        print("\nCourse info:")
        for c in self.__courses:
            c.course_display()

    def get_all(self):
        return self.__courses


class Mark:
    def __init__(self, students, courses):
        self.__students = students
        self.__courses = courses
        self.__marks = {}

    def calculate_gpa(self, student_id):
        marks = []
        credits = []

        for course in self.__courses:
            cid = course.get_cid()
            credit = course.get_credits()
            if cid in self.__marks and student_id in self.__marks[cid]:
                marks.append(self.__marks[cid][student_id])
                credits.append(credit)

        if not marks:
                print("Cannot find marks for this student.")
                return 
            
        marks_array = np.array(marks)
        credits_array = np.array(credits)

        gpa = np.sum(marks_array * credits_array) / np.sum(credits_array)
        print(f"\nAverage GPA for this student (ID: {student_id}): {round(gpa,2)}" )

    def select_course_and_input_marks(self):
        print("\nList of courses:")
        for c in self.__courses:
            print(f"- {c.get_cid()} : {c.get_cname()}")

        cid = input("Enter course ID to input marks: ")

        if cid not in [c.get_cid() for c in self.__courses]:
            print("Course not found!")
            return

        self.__marks.setdefault(cid, {})

        print("\nEnter marks for each student:")
        for s in self.__students:
            sid = s.get_id()
            mark = math.floor(float(input(f"Mark for {s.get_name()} ({sid}): ")))
            self.__marks[cid][sid] = mark

        print("Changes have been saved!")

    def show_marks(self):
        cid = input("\nEnter course ID to show marks: ")

        if cid not in self.__marks:
            print("No marks are found for this course.")
            return

        print(f"\nMarks for course {cid}:")
        for s in self.__students:
            sid = s.get_id()
            mark = self.__marks[cid].get(sid, "Not marked")
            print(f"{s.get_name()}: {mark}")

class Test:
    def __init__(self):
        self.students = StudentList()
        self.courses = CourseList()

    def runTest(self):
            
        self.students.number_of_students()
        self.courses.number_of_courses()

        mark_manager = Mark(
            self.students.get_all(),
            self.courses.get_all()
        )

        
        mark_manager.select_course_and_input_marks()
        self.students.slist()
        self.courses.clist()
        mark_manager.show_marks()

        student_id = input("\nEnter student ID to calculate GPA: ")
        mark_manager.calculate_gpa(student_id)
        
        print("\nStudents sorted by ID (descending):")
        self.students.sort_numpy()
        self.students.slist()

def ui(stdscr):
    curses.curs_set(0)

    test = Test()
    mark_manager = None

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Student Mark Management")
        stdscr.addstr(2, 0, "1. Input students")
        stdscr.addstr(3, 0, "2. Input courses")
        stdscr.addstr(4, 0, "3. Input marks")
        stdscr.addstr(5, 0, "0. Exit")
        stdscr.addstr(7, 0, "Choice: ")
        stdscr.refresh()

        ch = stdscr.getkey()

        # leave curses safely
        curses.endwin()

        if ch == "1":
            test.students.number_of_students()
        elif ch == "2":
            test.courses.number_of_courses()
            mark_manager = Mark(
                test.students.get_all(),
                test.courses.get_all()
            )
        elif ch == "3" and mark_manager:
            mark_manager.select_course_and_input_marks()
        elif ch == "0":
            break

        input("\nPress Enter to return to menu...")

        # reinitialize curses (IMPORTANT)
        stdscr = curses.initscr()
        curses.curs_set(0)

curses.wrapper(ui)