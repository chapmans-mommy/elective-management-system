"""Загрузка и сохранение данных проекта в JSON."""

import json
import os
from typing import List

from models import Course, Student, Enrollment


def load_courses(filename: str) -> List[Course]:
    """Загрузить курсы из JSON и преобразовать в объекты."""
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден.")
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Course.from_data(item) for item in data]
    except (json.JSONDecodeError, OSError) as error:
        print(f"Ошибка чтения {filename}: {error}")
        return []


def save_courses(filename: str, courses: List[Course]) -> None:
    """Сохранить курсы в JSON (преобразуя объекты в словари)."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                [c.to_data() for c in courses],
                f, ensure_ascii=False, indent=4,
            )
    except OSError as error:
        print(f"Не удалось сохранить {filename}: {error}")


def load_students(filename: str) -> List[Student]:
    """Загрузить студентов из JSON."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Student.from_data(item) for item in data]
    except (json.JSONDecodeError, OSError) as error:
        print(f"Ошибка чтения {filename}: {error}")
        return []


def save_students(filename: str, students: List[Student]) -> None:
    """Сохранить студентов в JSON."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                [s.to_data() for s in students],
                f, ensure_ascii=False, indent=4,
            )
    except OSError as error:
        print(f"Не удалось сохранить {filename}: {error}")


def load_enrollments(
    filename: str,
    students: List[Student],
    courses: List[Course],
) -> List[Enrollment]:
    """Загрузить записи из JSON и восстановить связи."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Ошибка чтения {filename}: {error}")
        return []

    result = []
    for item in data:
        enrollment = Enrollment.from_data(item, students, courses)
        if enrollment is not None:
            result.append(enrollment)
    return result


def save_enrollments(
    filename: str, enrollments: List[Enrollment]
) -> None:
    """Сохранить записи в JSON."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                [e.to_data() for e in enrollments],
                f, ensure_ascii=False, indent=4,
            )
    except OSError as error:
        print(f"Не удалось сохранить {filename}: {error}")
