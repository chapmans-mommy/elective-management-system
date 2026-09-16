"""Тесты для модуля students."""

from students import find_student


def test_find_student_success():
    """Проверяет, что студент находится по ID."""
    students = [
        {"id": 1, "name": "Иванова Валерия Денисовна",
         "group": "ЭФБО-02-24", "email": "ivanova.v.d@edu.mirea.ru"},
        {"id": 2, "name": "Петров Алексей Сергеевич",
         "group": "ЭФБО-02-24", "email": "petrov.a.s@edu.mirea.ru"},
    ]
    result = find_student(students, 1)
    assert result is not None
    assert result["name"] == "Иванова Валерия Денисовна"
    assert result["group"] == "ЭФБО-02-24"


def test_find_student_not_found():
    """Проверяет, что при отсутствии студента возвращается None."""
    students = [
        {"id": 1, "name": "Иванова Валерия Денисовна",
         "group": "ЭФБО-02-24", "email": "ivanova.v.d@edu.mirea.ru"},
    ]
    result = find_student(students, 99)
    assert result is None


def test_find_student_empty_list():
    """Проверяет поведение при пустом списке студентов."""
    students = []
    result = find_student(students, 1)
    assert result is None


def test_find_student_correct_id():
    """Проверяет, что возвращается именно нужный студент."""
    students = [
        {"id": 1, "name": "Иванова Валерия Денисовна",
         "group": "ЭФБО-02-24", "email": "ivanova.v.d@edu.mirea.ru"},
        {"id": 2, "name": "Петров Алексей Сергеевич",
         "group": "ЭФБО-02-24", "email": "petrov.a.s@edu.mirea.ru"},
        {"id": 3, "name": "Смирнова Анна Викторовна",
         "group": "ЭФБО-01-24", "email": "smirnova.a.v@edu.mirea.ru"},
    ]
    result = find_student(students, 2)
    assert result["name"] == "Петров Алексей Сергеевич"
    assert result["id"] == 2
