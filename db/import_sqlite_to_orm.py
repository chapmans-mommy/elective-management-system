"""Перенос исходной базы ПР7 в таблицы Django с сохранением ID и связей."""

import os
import sqlite3
import sys
from contextlib import closing
from datetime import date
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DB = BASE_DIR / "data" / "electives.sqlite"


def import_data(source_db=None):
    """Прочитать источник, затем атомарно создать/обновить ORM-объекты."""
    from django.db import connection, transaction
    from courses.models import Course
    from students.models import Student
    from enrollments.models import Enrollment

    source = Path(source_db or SOURCE_DB).resolve()
    if not source.is_file():
        raise FileNotFoundError(f"Исходная база не найдена: {source}")
    target = Path(connection.settings_dict["NAME"]).resolve()
    if source == target:
        raise ValueError("Исходная и целевая базы должны отличаться.")
    with closing(sqlite3.connect(
        source.as_uri() + "?mode=ro", uri=True,
    )) as src:
        src.row_factory = sqlite3.Row
        if src.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("В исходной базе нарушены внешние ключи.")
        courses = src.execute("SELECT * FROM courses ORDER BY id").fetchall()
        students = src.execute("SELECT * FROM students ORDER BY id").fetchall()
        enrollments = src.execute(
            "SELECT * FROM enrollments ORDER BY id",
        ).fetchall()

    with transaction.atomic():
        for row in courses:
            Course.objects.update_or_create(pk=row["id"], defaults={
                "name": row["name"], "description": row["description"],
                "teacher": row["teacher"], "max_students": row["max_students"],
                "current_students": row["current_students"],
                "start_date": (date.fromisoformat(row["start_date"])
                               if row["start_date"] else None),
            })
        for row in students:
            Student.objects.update_or_create(pk=row["id"], defaults={
                "name": row["name"], "group_name": row["group_name"],
                "email": row["email"],
            })
        for row in enrollments:
            if row["is_cancelled"] not in (0, 1):
                raise ValueError("is_cancelled должен быть равен 0 или 1.")
            Enrollment.objects.update_or_create(pk=row["id"], defaults={
                "course_id": row["course_id"], "student_id": row["student_id"],
                "enrollment_date": date.fromisoformat(row["enrollment_date"]),
                "is_cancelled": bool(row["is_cancelled"]),
            })
        connection.check_constraints()
    return (Course.objects.count(), Student.objects.count(),
            Enrollment.objects.count())


def main():
    sys.path.insert(0, str(BASE_DIR))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elective_system.settings")
    import django
    django.setup()
    counts = import_data()
    print("Перенос завершён. Курсов: {}, студентов: {}, записей: {}".format(
        *counts,
    ))


if __name__ == "__main__":
    main()
