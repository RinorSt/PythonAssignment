class Student:
    """Represents a student in the gradebook."""

    def __init__(self, id, name):
        """Initialize a student with an ID and name."""
        if not name or name.strip() == "":
            raise ValueError("Name cannot be empty")

        self.id = id
        self.name = name

    def to_dict(self):
        """Return the student as a dictionary."""
        return {"id": self.id, "name": self.name}


class Course:
    """Represents a course in the gradebook."""

    def __init__(self, code, title):
        """Initialize a course with a code and title."""
        self.code = code
        self.title = title

    def to_dict(self):
        """Return the course as a dictionary."""
        return {"code": self.code, "title": self.title}


class Enrollment:
    """Represents a student's enrollment in a course and their grades."""

    def __init__(self, student_id, course_code, grades: list):
        """Initialize an enrollment with student ID, course code, and grades."""
        for grade in grades:
            if not isinstance(grade, (int, float)):
                raise ValueError("Grades must be numbers")
            if grade < 0 or grade > 100:
                raise ValueError("Grade must be between 0 and 100")

        self.student_id = student_id
        self.course_code = course_code
        self.grades = grades

    def to_dict(self):
        """Return the enrollment as a dictionary."""
        return {
            "student_id": self.student_id,
            "course_code": self.course_code,
            "grades": self.grades,
        }