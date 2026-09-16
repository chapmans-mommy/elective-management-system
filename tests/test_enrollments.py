"""Тесты для класса Enrollment."""

from models import Course, Student, Enrollment
from models.enrollments import (
    add_enrollment, cancel_enrollment, is_student_enrolled,
)


def make_student():
    return Student(1, "Иванова", "ЭФБО-02-24", "i@edu.ru")


def make_course():
    return Course(1, "Python", "d", "И", 30, 28, "2026-10-01")


def test_enrollment_creation():
    """Проверяет создание Enrollment."""
    student = make_student()
    course = make_course()
    enrollment = Enrollment(1, student, course, "2026-09-15")
    assert enrollment.id == 1
    assert enrollment.student is student
    assert enrollment.course is course


def test_enrollment_cancel():
    """Проверяет отмену."""
    student = make_student()
    course = make_course()
    enrollment = Enrollment(1, student, course, "2026-09-15")
    assert enrollment.is_active()
    enrollment.cancel()
    assert not enrollment.is_active()


def test_add_enrollment_success():
    """Проверяет добавление записи."""
    student = make_student()
    course = make_course()
    enrollments = []
    result = add_enrollment(enrollments, student, course)
    assert result == "Запись успешно добавлена."
    assert len(enrollments) == 1
    assert course.current_students == 29


def test_add_enrollment_no_seats():
    """Проверяет запрет при отсутствии мест."""
    student = make_student()
    course = Course(1, "Python", "d", "И", 20, 20, "")
    enrollments = []
    result = add_enrollment(enrollments, student, course)
    assert result == "На курсе нет свободных мест."


def test_add_enrollment_duplicate():
    """Проверяет запрет дублирования."""
    student = make_student()
    course = make_course()
    enrollments = []
    add_enrollment(enrollments, student, course)
    result = add_enrollment(enrollments, student, course)
    assert result == "Студент уже записан на этот курс."


def test_cancel_enrollment():
    """Проверяет отмену записи."""
    student = make_student()
    course = make_course()
    enrollments = []
    add_enrollment(enrollments, student, course)
    result = cancel_enrollment(enrollments, student.id, course.id)
    assert result == "Запись отменена."
    assert enrollments[0].is_cancelled
    assert course.current_students == 28


def test_is_student_enrolled():
    """Проверяет проверку активной записи."""
    student = make_student()
    course = make_course()
    enrollments = []
    add_enrollment(enrollments, student, course)
    assert is_student_enrolled(enrollments, student.id, course.id)
