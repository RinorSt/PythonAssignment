from .models import Course, Enrollment, Student

students = []
courses = []
enrollments = []


def _generate_student_id():
    """Generate the next available student ID."""
    if not students:
        return 1
    return max(student.id for student in students) + 1


def add_student(name) -> int:
    """Create a new student and return the assigned ID."""
    new_id = _generate_student_id()
    student = Student(new_id, name)
    students.append(student)
    return new_id


def add_course(code, title):
    """Add a new course if the course code does not already exist."""
    for course in courses:
        if course.code == code:
            raise ValueError("Course already exists")

    course = Course(code, title)
    courses.append(course)


def enroll(student_id, course_code):
    """Enroll a student in a course."""
    student_exists = any(student.id == student_id for student in students)
    if not student_exists:
        raise ValueError("Student ID not found")

    course_exists = any(course.code == course_code for course in courses)
    if not course_exists:
        raise ValueError("Course code not found")

    already_enrolled = any(
        enrollment.student_id == student_id
        and enrollment.course_code == course_code
        for enrollment in enrollments
    )
    if already_enrolled:
        raise ValueError("Student is already enrolled in this course")

    enrollment = Enrollment(student_id, course_code, [])
    enrollments.append(enrollment)


def add_grade(student_id, course_code, grade):
    """Add a grade to an existing enrollment."""
    if not isinstance(grade, (int, float)):
        raise ValueError("Grade must be a number")

    if grade < 0 or grade > 100:
        raise ValueError("Grade must be between 0 and 100")

    for enrollment in enrollments:
        if (
            enrollment.student_id == student_id
            and enrollment.course_code == course_code
        ):
            enrollment.grades.append(grade)
            return

    raise ValueError("Enrollment not found")


def list_students():
    """Return all students sorted by name."""
    return sorted(
        [student.to_dict() for student in students],
        key=lambda student: student["name"]
    )


def list_courses():
    """Return all courses sorted by code."""
    return sorted(
        [course.to_dict() for course in courses],
        key=lambda course: course["code"]
    )


def list_enrollments():
    """Return all enrollments sorted by student ID and course code."""
    return sorted(
        [enrollment.to_dict() for enrollment in enrollments],
        key=lambda enrollment: (
            enrollment["student_id"],
            enrollment["course_code"]
        )
    )


def compute_average(student_id, course_code):
    """Return the average grade for a student's course enrollment."""
    for enrollment in enrollments:
        if (
            enrollment.student_id == student_id
            and enrollment.course_code == course_code
        ):
            if not enrollment.grades:
                return 0
            return sum(enrollment.grades) / len(enrollment.grades)

    raise ValueError("Enrollment not found")


def compute_gpa(student_id):
    """Return the GPA as the average of course averages for a student."""
    student_exists = any(student.id == student_id for student in students)
    if not student_exists:
        raise ValueError("Student ID not found")

    averages = [
        sum(enrollment.grades) / len(enrollment.grades)
        for enrollment in enrollments
        if enrollment.student_id == student_id and enrollment.grades
    ]

    return sum(averages) / len(averages) if averages else 0