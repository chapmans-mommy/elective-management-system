"""Однократный перенос исходных JSON-данных: python -m db.import_json."""

import json
from contextlib import closing
from pathlib import Path

from db.database import BASE_DIR, create_schema, get_connection


DATA_DIR = BASE_DIR / "data"


def load_json(filename):
    """Прочитать список записей, не изменяя исходный файл."""
    with Path(filename).open(encoding="utf-8") as file:
        return json.load(file)


def cancelled_value(enrollment):
    """Поддержать status из ПР6 и логическое поле is_cancelled."""
    if "status" in enrollment:
        status = enrollment["status"]
        if status not in ("active", "cancelled"):
            raise ValueError("Неизвестный статус записи: " + str(status))
        return int(status == "cancelled")
    value = enrollment.get("is_cancelled", False)
    if value not in (False, True, 0, 1):
        raise ValueError("is_cancelled должен быть логическим значением")
    return int(value)


def import_courses(conn, courses):
    conn.executemany(
        """
        INSERT INTO courses
            (id, name, description, teacher, max_students,
             current_students, start_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name = excluded.name,
            description = excluded.description,
            teacher = excluded.teacher,
            max_students = excluded.max_students,
            current_students = excluded.current_students,
            start_date = excluded.start_date
        """,
        [
            (course["id"], course["name"], course.get("description"),
             course["teacher"], course["max_students"],
             course.get("current_students", 0),
             course.get("start_date") or None)
            for course in courses
        ],
    )


def import_students(conn, students):
    conn.executemany(
        """
        INSERT INTO students (id, name, group_name, email)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name = excluded.name,
            group_name = excluded.group_name,
            email = excluded.email
        """,
        [(student["id"], student["name"], student["group"], student["email"])
         for student in students],
    )


def import_enrollments(conn, enrollments):
    conn.executemany(
        """
        INSERT INTO enrollments
            (id, student_id, course_id, enrollment_date, is_cancelled)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            student_id = excluded.student_id,
            course_id = excluded.course_id,
            enrollment_date = excluded.enrollment_date,
            is_cancelled = excluded.is_cancelled
        """,
        [(item["id"], item["student_id"], item["course_id"],
          item["enrollment_date"], cancelled_value(item))
         for item in enrollments],
    )


def import_data(db_path=None, data_dir=DATA_DIR):
    """Импортировать атомарно; повторный запуск не дублирует записи."""
    data_dir = Path(data_dir)
    courses = load_json(data_dir / "courses.json")
    students = load_json(data_dir / "students.json")
    enrollments = load_json(data_dir / "enrollments.json")
    with closing(get_connection(db_path)) as conn:
        create_schema(conn)
        try:
            import_courses(conn, courses)
            import_students(conn, students)
            import_enrollments(conn, enrollments)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
    return len(courses), len(students), len(enrollments)


def main():
    courses, students, enrollments = import_data()
    print("Импорт завершён: курсов {}, студентов {}, записей {}.".format(
        courses, students, enrollments,
    ))


if __name__ == "__main__":
    main()
