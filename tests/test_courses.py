from courses import find_course, search_courses, filter_available


def test_find_course_success():
    """курс находится по ID."""
    courses = [{"id": 1, "name": "Python", "description": "Курс Python"}]
    assert find_course(courses, 1)["name"] == "Python"


def test_find_course_not_found():
    """при отсутствии курса возвращается None."""
    courses = [{"id": 1, "name": "Python", "description": "Курс Python"}]
    assert find_course(courses, 99) is None


def test_search_courses():
    """поиск по ключевому слову."""
    courses = [
        {"id": 1, "name": "Python", "description": "Курс Python"},
        {"id": 2, "name": "Django", "description": "Веб-разработка"},
    ]
    result = search_courses(courses, "python")
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_filter_available():
    """фильтрация курсов со свободными местами."""
    courses = [
        {"id": 1, "name": "A", "max_students": 30, "current_students": 28},
        {"id": 2, "name": "B", "max_students": 20, "current_students": 20},
    ]
    result = filter_available(courses)
    assert len(result) == 1
    assert result[0]["id"] == 1
