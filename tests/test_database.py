"""Проверка сохранности данных, ограничений и SQL-статистики."""

import json
import sqlite3
from contextlib import closing

import pytest

from db.database import BASE_DIR, get_connection
from db.import_json import import_data, load_json
from db.queries import get_query, load_queries


def test_import_preserves_json_data(database_path):
    data = BASE_DIR / "data"
    with closing(get_connection()) as conn:
        courses = [dict(row) for row in conn.execute(
            "SELECT * FROM courses ORDER BY id",
        )]
        assert courses == load_json(data / "courses.json")
        students = [dict(row) for row in conn.execute(
            'SELECT id, name, group_name AS "group", email '
            'FROM students ORDER BY id',
        )]
        assert students == load_json(data / "students.json")
        expected = [
            {"id": item["id"], "student_id": item["student_id"],
             "course_id": item["course_id"],
             "enrollment_date": item["enrollment_date"],
             "is_cancelled": int(item["status"] == "cancelled")}
            for item in load_json(data / "enrollments.json")
        ]
        assert [dict(row) for row in conn.execute(
            "SELECT * FROM enrollments ORDER BY id",
        )] == expected
        assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
        assert conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"


def test_repeated_import_does_not_duplicate(database_path):
    assert import_data() == (3, 3, 5)
    assert import_data() == (3, 3, 5)
    with closing(get_connection()) as conn:
        assert conn.execute(
            "SELECT COUNT(*) FROM enrollments",
        ).fetchone()[0] == 5


def test_foreign_keys_are_enforced(database_path):
    with closing(get_connection()) as conn:
        assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO enrollments "
                "(id, student_id, course_id, enrollment_date) "
                "VALUES (?, ?, ?, ?)", (99, 999, 1, "2026-10-01"),
            )
        conn.rollback()


def test_import_error_rolls_back_entire_transaction(database_path, tmp_path):
    data = BASE_DIR / "data"
    sources = {
        name: load_json(data / (name + ".json"))
        for name in ("courses", "students", "enrollments")
    }
    sources["courses"][0]["name"] = "Не должно сохраниться"
    sources["enrollments"][0]["student_id"] = 999
    for name, content in sources.items():
        (tmp_path / (name + ".json")).write_text(
            json.dumps(content, ensure_ascii=False), encoding="utf-8",
        )
    with pytest.raises(sqlite3.IntegrityError):
        import_data(data_dir=tmp_path)
    with closing(get_connection()) as conn:
        assert conn.execute(
            "SELECT name FROM courses WHERE id = ?", (1,),
        ).fetchone()["name"] == load_json(data / "courses.json")[0]["name"]
        assert conn.execute("PRAGMA foreign_key_check").fetchall() == []


def test_statistics_keep_zero_enrollment_objects(database_path):
    with closing(get_connection()) as conn:
        totals = conn.execute(get_query("enrollment_totals")).fetchone()
        assert dict(totals) == {"total": 5, "active": 2, "cancelled": 3}
        seats = conn.execute(get_query("course_totals")).fetchone()
        assert seats["total_seats"] == 75
        assert seats["occupied_seats"] == 65
        assert seats["free_seats"] == 10
        courses = {row["id"]: row for row in conn.execute(
            get_query("course_statistics"),
        )}
        assert courses[2]["total_enrollments"] == 0
        assert courses[2]["active"] == 0
        assert courses[3]["cancelled"] == 3
        students = {row["id"]: row for row in conn.execute(
            get_query("student_statistics"),
        )}
        assert students[3]["total_enrollments"] == 0
        popular = conn.execute(get_query("popular_courses"), (1,)).fetchall()
        assert popular == []


def test_all_saved_queries_execute(database_path):
    parameters = {
        "courses_search": ("%SQL%", "%SQL%", 0),
        "available_courses": ("2026-10-01", 1),
        "enrollment_detail": (1,), "course_detail": (1,),
        "popular_courses": (0,), "students_by_group": ("ЭФБО-02-24",),
    }
    queries = load_queries()
    assert len(queries) >= 10
    with closing(get_connection()) as conn:
        for name, query in queries.items():
            conn.execute(query, parameters.get(name, ())).fetchall()
