Gradebook CLI
__________________________
This is a command-line application for managing students, courses, enrollments, and grades.

Creating a virtual enviorment:

python -m venv venv

Activate it (Windows):

venv\Scripts\activate
____________________________

How to run seed.py:
___________________
python -m scripts.seed

Output:

Sample data saved to data/gradebook.json

Check gradebook.json with all the added data
__________________________________________________________
How to run tests:
__________________________________________________________
python -m unittest tests.test_service

Output:


Ran 4 tests in 0.001s

OK

___________________________________________________________
Here are the commands we can use and the expected outputs:
__________________________________________________________
Add a student:
______________
python main.py add-student --name "Someone"

Output:

Student added successfully. ID: 1

_____________
Add a course:
_____________
python main.py add-course --code CS101 --title "Intro to CS

Output:

Course added successfully: CS101 - Intro to CS

_________________
Enroll a student:
_________________
python main.py enroll --student-id 1 --course CS101

Output:

Student 1 enrolled in course CS101.

____________
Add a grade:
____________
python main.py add-grade --student-id 1 --course CS101 --grade 95

Output:

Grade 95.0 added for student 1 in CS101.

______________
Check Average:
______________
python main.py avg --student-id 1 --course CS101

Output:

Average for student 1 in CS101: 95.00

___________
Check GPA:
___________
python main.py gpa --student-id 1

Output:

GPA for student 1: 95.00

_______________________________
Get a list of all enrollments:
_______________________________
python main.py list enrollments

Output:

Student ID: 1 | Course: CS101 | Grades: [95.0]

___________________________________
Design Decisions and limitations:
___________________________________
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
