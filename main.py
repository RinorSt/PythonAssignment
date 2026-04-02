import argparse
import sys
import logging
import os

import gradebook.service as service
from gradebook.models import Student, Course, Enrollment
from gradebook.storage import load_data, save_data

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_into_service():
    """Load saved JSON data into the service layer."""
    data = load_data()

    service.students.clear()
    service.courses.clear()
    service.enrollments.clear()

    for student_data in data.get("students", []):
        service.students.append(
            Student(student_data["id"], student_data["name"])
        )

    for course_data in data.get("courses", []):
        service.courses.append(
            Course(course_data["code"], course_data["title"])
        )

    for enrollment_data in data.get("enrollments", []):
        service.enrollments.append(
            Enrollment(
                enrollment_data["student_id"],
                enrollment_data["course_code"],
                enrollment_data["grades"]
            )
        )


def save_from_service():
    """Save current service-layer data to JSON."""
    data = {
        "students": [student.to_dict() for student in service.students],
        "courses": [course.to_dict() for course in service.courses],
        "enrollments": [
            enrollment.to_dict() for enrollment in service.enrollments
        ],
    }
    save_data(data)


def handle_add_student(args):
    student_id = service.add_student(args.name)
    save_from_service()
    logging.info("Added student: %s (ID: %s)", args.name, student_id)
    print(f"Student added successfully. ID: {student_id}")


def handle_add_course(args):
    service.add_course(args.code, args.title)
    save_from_service()
    logging.info("Added course: %s", args.code)
    print(f"Course added successfully: {args.code} - {args.title}")


def handle_enroll(args):
    service.enroll(args.student_id, args.course)
    save_from_service()
    logging.info(
        "Enrolled student %s in course %s",
        args.student_id,
        args.course
    )
    print(f"Student {args.student_id} enrolled in course {args.course}.")


def handle_add_grade(args):
    service.add_grade(args.student_id, args.course, args.grade)
    save_from_service()
    logging.info(
        "Added grade %s for student %s in %s",
        args.grade,
        args.student_id,
        args.course
    )
    print(
        f"Grade {args.grade} added for student "
        f"{args.student_id} in {args.course}."
    )


def handle_list(args):
    if args.entity == "students":
        items = service.list_students()
        if args.sort == "name":
            items = sorted(items, key=lambda x: x["name"])
        for student in items:
            print(f'ID: {student["id"]} | Name: {student["name"]}')

    elif args.entity == "courses":
        items = service.list_courses()
        if args.sort == "code":
            items = sorted(items, key=lambda x: x["code"])
        for course in items:
            print(f'Code: {course["code"]} | Title: {course["title"]}')

    elif args.entity == "enrollments":
        items = service.list_enrollments()
        for enrollment in items:
            print(
                f'Student ID: {enrollment["student_id"]} | '
                f'Course: {enrollment["course_code"]} | '
                f'Grades: {enrollment["grades"]}'
            )


def handle_avg(args):
    average = service.compute_average(args.student_id, args.course)
    print(f"Average for student {args.student_id} in {args.course}: {average:.2f}")


def handle_gpa(args):
    gpa = service.compute_gpa(args.student_id)
    print(f"GPA for student {args.student_id}: {gpa:.2f}")


def parse_grade(value):
    """Parse and validate a grade value."""
    try:
        grade = float(value)
    except ValueError:
        raise ValueError("Grade must be a number.")

    if grade < 0 or grade > 100:
        raise ValueError("Grade must be between 0 and 100.")

    return grade


def parse_student_id(value):
    """Parse and validate a student ID."""
    try:
        student_id = int(value)
    except ValueError:
        raise ValueError("Student ID must be an integer.")

    if student_id <= 0:
        raise ValueError("Student ID must be positive.")

    return student_id


def build_parser():
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Gradebook CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_student_parser = subparsers.add_parser("add-student", help="Add a new student")
    add_student_parser.add_argument("--name", required=True, help="Student name")
    add_student_parser.set_defaults(func=handle_add_student)

    add_course_parser = subparsers.add_parser("add-course", help="Add a new course")
    add_course_parser.add_argument("--code", required=True, help="Course code")
    add_course_parser.add_argument("--title", required=True, help="Course title")
    add_course_parser.set_defaults(func=handle_add_course)

    enroll_parser = subparsers.add_parser("enroll", help="Enroll a student in a course")
    enroll_parser.add_argument("--student-id", type=parse_student_id, required=True)
    enroll_parser.add_argument("--course", required=True, help="Course code")
    enroll_parser.set_defaults(func=handle_enroll)

    add_grade_parser = subparsers.add_parser("add-grade", help="Add a grade")
    add_grade_parser.add_argument("--student-id", type=parse_student_id, required=True)
    add_grade_parser.add_argument("--course", required=True, help="Course code")
    add_grade_parser.add_argument("--grade", type=parse_grade, required=True)
    add_grade_parser.set_defaults(func=handle_add_grade)

    list_parser = subparsers.add_parser("list", help="List data")
    list_parser.add_argument(
        "entity",
        choices=["students", "courses", "enrollments"],
        help="What to list"
    )
    list_parser.add_argument("--sort", choices=["name", "code"])
    list_parser.set_defaults(func=handle_list)

    avg_parser = subparsers.add_parser("avg", help="Compute average")
    avg_parser.add_argument("--student-id", type=parse_student_id, required=True)
    avg_parser.add_argument("--course", required=True, help="Course code")
    avg_parser.set_defaults(func=handle_avg)

    gpa_parser = subparsers.add_parser("gpa", help="Compute GPA")
    gpa_parser.add_argument("--student-id", type=parse_student_id, required=True)
    gpa_parser.set_defaults(func=handle_gpa)

    return parser


def main():
    """Run the CLI application."""
    load_into_service()

    parser = build_parser()
    args = parser.parse_args()

    try:
        args.func(args)
    except ValueError as e:
        logging.error("Validation error: %s", e)
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logging.exception("Unexpected error")
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()