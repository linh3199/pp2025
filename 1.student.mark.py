students = []      
courses = []       
marks = {}         

def number_of_students():
    n = int(input("Enter the number of students: "))
    for i in range(n):
        student_info()


def student_info():
    sid = input("Student ID: ")
    name = input("Student name: ")
    dob = input("Student DoB: ")

    students.append({
        "id": sid,
        "name": name,
        "dob": dob
    })

def number_of_courses():
    m = int(input("Enter the number of courses: "))
    for i in range(m):
        course_info()

def course_info():
    cid = input("Course ID: ")
    cname = input("Course name: ")

    courses.append({
        "id": cid,
        "name": cname
    })

def input_marks_for_course():
    print("\nList of courses:")
    list_courses()

    cid = input("Select course by ID: ")

    if not any(c["id"] == cid for c in courses):
        print("Course not found!\n")
        return

    if cid not in marks:
        marks[cid] = {}

    print(f"\nEntering marks for course ID {cid}:")
    for student in students:
        mark = float(input(f"Mark for {student['name']} ({student['id']}): "))
        marks[cid][student["id"]] = mark

    print("Marks updated.\n")


def list_students():
    if len(students) == 0:
        print("No students available.\n")
        return

    for s in students:
        print(f"- {s['id']}: {s['name']} (DoB: {s['dob']})")

def list_courses():
    if len(courses) == 0:
        print("No courses available.\n")
        return

    for c in courses:
        print(f"- {c['id']}: {c['name']}")

def show_student_marks():
    print("\nList of courses:")
    list_courses()

    cid = input("Enter course ID: ")

    if cid not in marks:
        print("No marks are found for this course.\n")
        return

    print(f"\nMarks for course ID {cid}:")
    for student in students:
        sid = student["id"]
        if sid in marks[cid]:
            mark = marks[cid][sid]
        else:
            mark = "Not marked"

        print(f"{student['name']}: {mark}")
    print()


def main():
    print("||Student Mark Management||")
    number_of_students()
    number_of_courses()
    input_marks_for_course()
    list_students()
    list_courses()
    show_student_marks()

main()
