"""Тесты для класса Course и функций курсов."""

from models import Course
from models.courses import (
    find_course, search_courses, filter_available,
)


def test_course_creation():
    """Проверяет создание объекта Course."""
    course = Course(1, "Python", "Курс Python",
                    "Иванов", 30, 28, "2026-10-01")
    assert course.id == 1
    assert course.name == "Python"
    assert course.max_students == 30


def test_course_has_free_seats():
    """Проверяет метод has_free_seats."""
    course = Course(1, "Python", "desc", "Иванов", 30, 28, "2026-10-01")
    assert course.has_free_seats() is True

    full = Course(2, "SQL", "desc", "Петров", 20, 20, "2026-10-05")
    assert full.has_free_seats() is False


def test_course_str():
    """Проверяет строковое представление."""
    course = Course(1, "Python", "desc", "Иванов", 30, 28, "2026-10-01")
    assert "Python" in str(course)
    assert "2" in str(course)  # свободных мест


def test_find_course():
    """Проверяет поиск курса по ID."""
    courses = [Course(1, "Python", "d", "И", 30, 0, "")]
    assert find_course(courses, 1).name == "Python"
    assert find_course(courses, 99) is None


def test_filter_available():
    """Проверяет фильтрацию по наличию мест."""
    courses = [
        Course(1, "A", "d", "И", 30, 28, ""),
        Course(2, "B", "d", "И", 20, 20, ""),
    ]
    result = filter_available(courses)
    assert len(result) == 1
    assert result[0].id == 1


def test_search_courses():
    """Проверяет поиск курсов по ключевому слову."""
    courses = [
        Course(1, "Python", "Курс Python", "Иванов", 30, 28, ""),
        Course(2, "Django", "Веб-разработка", "Петров", 25, 25, ""),
        Course(3, "SQL", "Базы данных", "Сидоров", 20, 10, ""),
    ]
    result = search_courses(courses, "python")
    assert len(result) == 1
    assert result[0].id == 1

    result2 = search_courses(courses, "разработка")
    assert len(result2) == 1
    assert result2[0].id == 2


def test_search_courses_empty():
    """Проверяет поиск, который ничего не находит."""
    courses = [Course(1, "Python", "Курс Python", "Иванов", 30, 0, "")]
    result = search_courses(courses, "Java")
    assert result == []
