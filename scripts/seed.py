from gradebook.models import Student, Course, Enrollment
from gradebook.storage import save_data


def main():
    students = [
        Student(1, "Ali"),
        Student(2, "Bella"),
        Student(3, "Filon"),
    ]

    courses = [
        Course("CS101", "Intro to CS"),
        Course("MATH101", "Mathematics"),
    ]

    enrollments = [
        Enrollment(1, "CS101", [90, 85]),
        Enrollment(1, "MATH101", [88]),
        Enrollment(2, "CS101", [70, 75]),
        Enrollment(3, "MATH101", [95, 100]),
    ]

    data = {
        "students": [s.to_dict() for s in students],
        "courses": [c.to_dict() for c in courses],
        "enrollments": [e.to_dict() for e in enrollments],
    }

    save_data(data)
    print("Sample data saved to data/gradebook.json")


if __name__ == "__main__":
    main()