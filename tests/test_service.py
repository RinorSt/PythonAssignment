import unittest

import gradebook.service as service


class TestService(unittest.TestCase):
    """Unit tests for the gradebook service layer."""

    def setUp(self):
        """Reset in-memory data before each test."""
        service.students.clear()
        service.courses.clear()
        service.enrollments.clear()

    def test_add_student(self):
        """Test that adding a student works correctly."""
        student_id = service.add_student("Alice")

        self.assertEqual(student_id, 1)
        self.assertEqual(len(service.students), 1)
        self.assertEqual(service.students[0].name, "Alice")

    def test_add_grade_happy_path(self):
        """Test that a grade can be added to an existing enrollment."""
        student_id = service.add_student("Alice")
        service.add_course("CS101", "Intro to CS")
        service.enroll(student_id, "CS101")

        service.add_grade(student_id, "CS101", 95)

        self.assertEqual(service.enrollments[0].grades, [95])

    def test_compute_average_happy_path(self):
        """Test average calculation for a student in a course."""
        student_id = service.add_student("Alice")
        service.add_course("CS101", "Intro to CS")
        service.enroll(student_id, "CS101")
        service.add_grade(student_id, "CS101", 90)
        service.add_grade(student_id, "CS101", 80)

        average = service.compute_average(student_id, "CS101")

        self.assertEqual(average, 85.0)

    def test_add_grade_failing_case(self):
        """Test that adding a grade fails if enrollment does not exist."""
        student_id = service.add_student("Alice")
        service.add_course("CS101", "Intro to CS")

        with self.assertRaises(ValueError):
            service.add_grade(student_id, "CS101", 95)


if __name__ == "__main__":
    unittest.main()