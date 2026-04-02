import argparse
import sys
import logging
import gradebook.service as service
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def handle_add_student(args):
    student_id = service.add_student(args.name)
    logging.info(f"Added student: {args.name} (ID: {student_id})")
    print(f"Student added successfully. ID: {student_id}")


def handle_add_course(args):
    service.add_course(args.code, args.title)
    logging.info(f"Added course: {args.code}")
    print(f"Course added successfully: {args.code} - {args.title}")


def handle_enroll(args):
    service.enroll(args.student_id, args.course)
    logging.info(f"Enrolled student {args.student_id} in {args.course}")
    print(f"Student {args.student_id} enrolled in course {args.course}.")


def handle_add_grade(args):
    service.add_grade(args.student_id, args.course, args.grade)
    logging.info(f"Added grade {args.grade} for student {args.student_id}")
    print(f"Grade {args.grade} added for student {args.student_id} in {args.course}.")


def handle_list(args):
    if args.entity == "students":
        items = service.list_students()
        if args.sort == "name":
            items = sorted(items, key=lambda x: x["name"])
        for s in items:
            print(f'ID: {s["id"]} | Name: {s["name"]}')

    elif args.entity == "courses":
        items = service.list_courses()
        if args.sort == "code":
            items = sorted(items, key=lambda x: x["code"])
        for c in items:
            print(f'Code: {c["code"]} | Title: {c["title"]}')

    elif args.entity == "enrollments":
        items = service.list_enrollments()
        for e in items:
            print(
                f'Student ID: {e["student_id"]} | '
                f'Course: {e["course_code"]} | '
                f'Grades: {e["grades"]}'
            )


def handle_avg(args):
    average = service.compute_average(args.student_id, args.course)
    print(f"Average for student {args.student_id} in {args.course}: {average:.2f}")


def handle_gpa(args):
    gpa = service.compute_gpa(args.student_id)
    print(f"GPA for student {args.student_id}: {gpa:.2f}")

def parse_grade(value):
    try:
        grade = float(value)
    except ValueError:
        raise ValueError("Grade must be a number.")

    if grade < 0 or grade > 100:
        raise ValueError("Grade must be between 0 and 100.")

    return grade


def parse_student_id(value):
    try:
        student_id = int(value)
    except ValueError:
        raise ValueError("Student ID must be an integer.")

    if student_id <= 0:
        raise ValueError("Student ID must be positive.")

    return student_id


def build_parser():
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

    add_grade_parser = subparsers.add_parser("add-grade", help="Add a grade to an enrollment")
    add_grade_parser.add_argument("--student-id", type=parse_student_id, required=True)
    add_grade_parser.add_argument("--course", required=True, help="Course code")
    add_grade_parser.add_argument("--grade", type=parse_grade, required=True)
    add_grade_parser.set_defaults(func=handle_add_grade)

    list_parser = subparsers.add_parser("list", help="List students, courses, or enrollments")
    list_parser.add_argument(
        "entity",
        choices=["students", "courses", "enrollments"],
        help="What to list"
    )
    list_parser.add_argument(
        "--sort",
        choices=["name", "code"],
        help="Optional sort field"
    )
    list_parser.set_defaults(func=handle_list)

    avg_parser = subparsers.add_parser("avg", help="Compute course average for a student")
    avg_parser.add_argument("--student-id", type=parse_student_id, required=True)
    avg_parser.add_argument("--course", required=True, help="Course code")
    avg_parser.set_defaults(func=handle_avg)

    gpa_parser = subparsers.add_parser("gpa", help="Compute GPA for a student")
    gpa_parser.add_argument("--student-id", type=parse_student_id, required=True)
    gpa_parser.set_defaults(func=handle_gpa)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        args.func(args)

    except ValueError as e:
        logging.error(f"Validation error: {e}")
        print(f"Error: {e}")
        sys.exit(1)

    except Exception as e:
        logging.exception("Unexpected error occurred")
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

