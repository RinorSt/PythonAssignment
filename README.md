Gradebook CLI

This is a command-line application for managing students, courses, enrollments, and grades.

Creating a virtual enviorment:

python -m venv venv

Activate it (Windows):
venv\Scripts\activate

How to run seed.py:
python -m scripts.seed
Output:
Sample data saved to data/gradebook.json
Check gradebook.json with all the added data

Here are the commands we can use and the expected outputs:

Add a student:
python main.py add-student --name "Someone"
Output:
Student added successfully. ID: 1

Add a course:
python main.py add-course --code CS101 --title "Intro to CS
Output:
Course added successfully: CS101 - Intro to CS

Enroll a student:
python main.py enroll --student-id 1 --course CS101
Output:
Student 1 enrolled in course CS101.


Add a grade:
python main.py add-grade --student-id 1 --course CS101 --grade 95
Output:
Grade 95.0 added for student 1 in CS101.

Check Average:
python main.py avg --student-id 1 --course CS101
Output:
Average for student 1 in CS101: 95.00

Check GPA:
python main.py gpa --student-id 1
Output:
GPA for student 1: 95.00

Get a list of all enrollments:
python main.py list enrollments
Output:
Student ID: 1 | Course: CS101 | Grades: [95.0]


Design Decisions and limitations:

Design decisions

- I separated the project into modules (models, service, storage, CLI) to keep things organized and easier to manage.
- I used a service layer so the CLI only handles input, while the logic is in one place.
- Data is stored in a JSON file instead of a database to keep the project simple.
- Student IDs are generated automatically as integers for easier use.
- I added input validation to prevent invalid data (like wrong grades).
- Logging is included to track actions and errors.


Limitations

- The app is meant for small use and not large datasets.
- JSON storage is simple but not as powerful as a real database.
- Running the seed script overwrites existing data.
- No support for multiple users at the same time.
