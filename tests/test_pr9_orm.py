"""Проверки ПР9: перенос, модели, связи, ORM и журнал с пагинацией."""

import hashlib
import sqlite3
from contextlib import closing
from datetime import date
from html import unescape
from urllib.parse import parse_qs, urlsplit

import pytest
from django.db import IntegrityError, connection, transaction
from django.db.models.deletion import ProtectedError
from django.test.utils import CaptureQueriesContext

from courses.models import Course
from db.import_sqlite_to_orm import import_data
from enrollments.models import Enrollment
from students.models import Student


def test_transfer_preserves_every_field_and_is_repeatable(
        client, database_path):
    before = hashlib.sha256(database_path.read_bytes()).hexdigest()
    with closing(sqlite3.connect(database_path)) as source:
        source.row_factory = sqlite3.Row
        for table, model in [("courses", Course), ("students", Student),
                             ("enrollments", Enrollment)]:
            expected = [dict(row) for row in source.execute(
                f"SELECT * FROM {table} ORDER BY id",
            )]
            actual = list(model.objects.order_by("pk").values())
            for row in actual:
                for field, value in row.items():
                    if isinstance(value, date):
                        row[field] = value.isoformat()
            assert actual == expected
    assert import_data(database_path) == (3, 3, 5)
    assert import_data(database_path) == (3, 3, 5)
    extra = Student.objects.create(
        name="Новая", group_name="Т", email="n@e.ru")
    assert import_data(database_path) == (3, 4, 5)
    assert Student.objects.filter(pk=extra.pk).exists()
    assert hashlib.sha256(database_path.read_bytes()).hexdigest() == before


@pytest.mark.parametrize("field,value", [
    ("enrollment_date", "2026-02-30"), ("is_cancelled", 2),
    ("student_id", 999),
])
def test_bad_source_does_not_partially_import(
        client, database_path, field, value):
    original = Course.objects.get(pk=1).name
    with closing(sqlite3.connect(database_path)) as source:
        source.execute("PRAGMA ignore_check_constraints = ON")
        source.execute("UPDATE courses SET name = 'Не сохранять' WHERE id = 1")
        source.execute(
            f"UPDATE enrollments SET {field} = ? WHERE id = 5", (value,))
        source.commit()
    with pytest.raises(ValueError):
        import_data(database_path)
    assert Course.objects.get(pk=1).name == original
    assert Enrollment.objects.count() == 5


def test_missing_source_is_not_created(orm_db, tmp_path):
    missing = tmp_path / "missing.sqlite"
    with pytest.raises(FileNotFoundError):
        import_data(missing)
    assert not missing.exists()


def test_model_crud_defaults_links_and_protected_deletion(orm_db):
    student = Student.objects.create(
        name="Тест", group_name="Т", email="t@e.ru")
    student.name = "Изменено"
    student.full_clean()
    student.save()
    assert Student.objects.get(pk=student.pk).name == "Изменено"
    course = Course.objects.create(name="Курс", teacher="Т", max_students=1)
    assert course.current_students == 0 and course.free_seats == 1
    assert course.start_date is None and course.has_free_seats()
    enrollment = Enrollment.objects.create(
        student=student, course=course, enrollment_date=date(2026, 11, 3),
    )
    assert not enrollment.is_cancelled and enrollment.is_active()
    assert list(course.enrollments.all()) == [enrollment]
    assert list(student.enrollments.all()) == [enrollment]
    assert enrollment.course == course and enrollment.student == student
    assert isinstance(enrollment.enrollment_date, date)
    for obj in (course, student):
        with pytest.raises(ProtectedError):
            obj.delete()
    enrollment.cancel()
    enrollment.refresh_from_db()
    assert enrollment.is_cancelled and not enrollment.is_active()
    enrollment.delete()
    student_id = student.pk
    student.delete()
    assert not Student.objects.filter(pk=student_id).exists()
    Course.objects.filter(pk=course.pk).delete()
    assert not Course.objects.exists()


@pytest.mark.parametrize("capacity,occupied", [(0, 0), (1, 2), (1, -1)])
def test_capacity_constraints(orm_db, capacity, occupied):
    with pytest.raises(IntegrityError), transaction.atomic():
        Course.objects.create(
            name="Тест", teacher="Т", max_students=capacity,
            current_students=occupied,
        )


def test_enrollment_filters_search_and_sort(client):
    params = {"date": "2026-09-16", "course": 3, "student": 2, "q": "SQL"}
    response = client.get("/enrollments/active/", params)
    assert [row["id"] for row in response.context["enrollments"]] == [2]
    response = client.get("/enrollments/", {"student": 1, "sort": "date_asc"})
    assert [row["id"]
            for row in response.context["enrollments"]] == [3, 4, 5, 1]
    response = client.get("/enrollments/", {"sort": "course"})
    rows = list(response.context["enrollments"])
    assert [(r["course_name"], r["id"]) for r in rows] == sorted(
        (r["course_name"], r["id"]) for r in rows
    )
    response = client.get("/enrollments/", {"sort": "student"})
    rows = list(response.context["enrollments"])
    assert [(r["student_name"], r["id"]) for r in rows] == sorted(
        (r["student_name"], r["id"]) for r in rows
    )
    response = client.get(
        "/students/", {"q": "Валерия", "group": "ЭФБО-02-24"})
    assert [student.pk for student in response.context["students"]] == [1]


@pytest.mark.parametrize("params", [
    {"date": "2026-02-30"}, {"date": "bad"}, {"course": "bad"},
    {"course": -1}, {"student": 999}, {"student": "9" * 100},
])
def test_bad_enrollment_parameters_are_form_errors(client, params):
    response = client.get("/enrollments/", params)
    assert response.status_code == 200
    assert response.context["form"].errors
    assert response.context["page_obj"].paginator.count == 0


def test_unknown_sort_uses_safe_default(client):
    response = client.get("/enrollments/", {"sort": "student__password; DROP"})
    assert response.status_code == 200
    assert not response.context["form"].errors
    assert [row["id"]
            for row in response.context["enrollments"]] == [2, 1, 5, 4, 3]


def test_pagination_keeps_filters_sort_and_search(client):
    for _ in range(11):
        Enrollment.objects.create(
            course_id=3, student_id=2, enrollment_date=date(2026, 9, 16),
        )
    params = {"date": "2026-09-16", "course": "3", "student": "2",
              "q": "SQL", "sort": "date_asc", "page": "2"}
    response = client.get("/enrollments/active/", params)
    page = response.context["page_obj"]
    assert page.number == 2 and len(page) == 5 and page.paginator.count == 12
    assert page.has_previous() and page.has_next()
    from html.parser import HTMLParser

    class Links(HTMLParser):
        def __init__(self):
            super().__init__()
            self.urls = []

        def handle_starttag(self, tag, attrs):
            if tag == "a":
                self.urls.extend(v for k, v in attrs if k == "href")

    links = Links()
    links.feed(response.content.decode())
    paging = [url for url in links.urls if "page=" in url]
    assert len(paging) >= 2
    for url in paging:
        query = parse_qs(urlsplit(unescape(url)).query)
        for key, value in params.items():
            if key != "page":
                assert query[key] == [value]
        assert client.get("/enrollments/active/" + url).status_code == 200
    for value, expected in [("abc", 1), ("999", 3), ("-1", 3)]:
        params["page"] = value
        response = client.get("/enrollments/active/", params)
        assert response.context["page_obj"].number == expected


def test_statistics_keep_all_entities_and_original_seat_counts(client):
    response = client.get("/enrollments/statistics/")
    context = response.context
    assert context["course_totals"] == {
        "course_count": 3, "total_seats": 75, "occupied_seats": 65,
        "free_seats": 10, "average_capacity": 25.0,
    }
    assert context["enrollment_totals"] == {
        "total": 5, "active": 2, "cancelled": 3,
    }
    courses = {row["id"]: row for row in context["course_statistics"]}
    assert courses[2]["total_enrollments"] == courses[2]["active"] == 0
    assert courses[3]["cancelled"] == 3 and courses[3]["active"] == 1
    students = {row["id"]: row for row in context["student_statistics"]}
    assert students[3]["total_enrollments"] == 0
    assert sum(g["student_count"] for g in context["group_statistics"]) == 3
    assert [r["id"] for r in context["popular_courses"]] == [3, 1]


def test_detail_uses_one_join_query(client):
    with CaptureQueriesContext(connection) as queries:
        response = client.get("/enrollments/3/")
    assert response.status_code == 200
    assert len(queries) == 1
    assert queries[0]["sql"].count("INNER JOIN") == 2


def test_cancelled_enrollment_does_not_block_available_course(client):
    course = Course.objects.create(
        name="Свободный", teacher="Т", max_students=1,
        start_date=date(2026, 12, 1),
    )
    Enrollment.objects.create(
        course=course, student_id=1, enrollment_date=date(2026, 11, 3),
        is_cancelled=True,
    )
    response = client.get("/courses/available/", {"date": "2026-12-01"})
    assert [row.pk for row in response.context["courses"]] == [course.pk]
