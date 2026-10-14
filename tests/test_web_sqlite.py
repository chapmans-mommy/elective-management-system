"""Пользовательские сценарии на данных SQLite и проверка ввода."""

from contextlib import closing

import pytest

from db.database import create_schema, get_connection


@pytest.mark.parametrize("url", [
    "/", "/courses/", "/courses/1/", "/students/", "/enrollments/",
    "/enrollments/1/", "/enrollments/active/", "/courses/available/",
    "/enrollments/statistics/",
])
def test_pages_open(client, url):
    response = client.get(url)
    assert response.status_code == 200
    assert "Факультативы" in response.content.decode()


def test_join_data_and_cancelled_status(client):
    response = client.get("/enrollments/3/")
    content = response.content.decode()
    assert "Иванова Валерия Денисовна" in content
    assert "Базы данных и SQL" in content
    assert "Отменена" in content
    active = client.get("/enrollments/active/").content.decode()
    assert "Всего записей: 2" in active
    assert "Отменена" not in active


def test_available_courses_date_and_capacity(client):
    response = client.get("/courses/available/", {"date": "2026-10-01"})
    content = response.content.decode()
    assert "Введение в искусственный интеллект" in content
    assert "Базы данных и SQL" in content
    assert "Веб-разработка на Django" not in content
    response = client.get("/courses/available/", {
        "date": "2026-10-10", "min_seats": 8,
    })
    assert "Найдено курсов: 1" in response.content.decode()
    assert "Базы данных и SQL" in response.content.decode()
    response = client.get("/courses/available/", {"date": "2026-10-11"})
    assert "Найдено курсов: 0" in response.content.decode()


@pytest.mark.parametrize("parameters", [
    {"date": "2026-02-30"}, {"date": "bad"},
    {"date": "2026-10-01", "min_seats": -1},
    {"date": "2026-10-01", "min_seats": "bad"},
])
def test_invalid_search_is_shown_as_form_error(client, parameters):
    response = client.get("/courses/available/", parameters)
    assert response.status_code == 200
    assert 'class="errorlist"' in response.content.decode()


def test_search_and_sql_injection(client):
    response = client.get("/courses/", {"q": "SQL", "min_seats": 5})
    assert "Найдено курсов: 1" in response.content.decode()
    assert "Базы данных и SQL" in response.content.decode()
    response = client.get("/courses/", {"q": "%' OR 1=1 --"})
    assert "Найдено курсов: 0" in response.content.decode()
    response = client.get("/students/", {"group": "' OR 1=1 --"})
    assert "Всего студентов: 0" in response.content.decode()
    response = client.get("/students/", {"group": "ЭФБО-02-24"})
    assert "Всего студентов: 2" in response.content.decode()


def test_statistics_filters_and_validation(client):
    content = client.get("/enrollments/statistics/").content.decode()
    assert "Всего записей: 5" in content
    assert "Активных: 2" in content
    content = client.get("/enrollments/statistics/", {
        "threshold": 1,
    }).content.decode()
    assert "Курсы с таким количеством записей не найдены." in content
    response = client.get("/enrollments/statistics/", {"threshold": -1})
    assert response.status_code == 200
    assert 'class="errorlist"' in response.content.decode()


def test_page_reads_database_changes(client):
    with closing(get_connection()) as conn:
        conn.execute("UPDATE courses SET name = ? WHERE id = ?", (
            "Изменено непосредственно в SQLite", 1,
        ))
        conn.commit()
    assert "Изменено непосредственно в SQLite" in client.get(
        "/courses/",
    ).content.decode()


@pytest.mark.parametrize("url", [
    "/courses/999/", "/enrollments/999/", "/does-not-exist/",
])
def test_missing_objects_return_404(client, url):
    assert client.get(url).status_code == 404


def test_empty_database_pages(client, tmp_path, monkeypatch):
    monkeypatch.setattr("db.database.DB_PATH", tmp_path / "empty.sqlite")
    with closing(get_connection()) as conn:
        create_schema(conn)
    for url in ["/courses/", "/students/", "/enrollments/active/",
                "/enrollments/statistics/"]:
        assert client.get(url).status_code == 200
    assert "Курсы не найдены." in client.get("/courses/").content.decode()
    content = client.get("/enrollments/statistics/").content.decode()
    assert "Всего записей: 0" in content
