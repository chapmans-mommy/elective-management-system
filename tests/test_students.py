"""Тесты для класса Student."""

from models import Student
from models.students import find_student


def test_student_creation():
    """Проверяет создание Student."""
    student = Student(1, "Иванова В.Д.", "ЭФБО-02-24", "i@edu.ru")
    assert student.id == 1
    assert student.name == "Иванова В.Д."
    assert student.group == "ЭФБО-02-24"


def test_student_str():
    """Проверяет строковое представление."""
    student = Student(1, "Иванова В.Д.", "ЭФБО-02-24", "i@edu.ru")
    assert "Иванова" in str(student)
    assert "ЭФБО-02-24" in str(student)


def test_find_student():
    """Проверяет поиск студента по ID."""
    students = [Student(1, "Иванова", "ЭФБО-02-24", "i@edu.ru")]
    assert find_student(students, 1).name == "Иванова"
    assert find_student(students, 99) is None
