from enrollments import add_enrollment, cancel_enrollment


def test_add_enrollment_success():
    """добавление записи."""
    courses = [{"id": 1, "name": "Python",
                "max_students": 30, "current_students": 28}]
    enrollments = []
    result = add_enrollment(enrollments, courses, 1, 1)
    assert result == "Запись успешно добавлена."
    assert len(enrollments) == 1
    assert courses[0]["current_students"] == 29


def test_add_enrollment_no_seats():
    """запрет записи при отсутствии мест."""
    courses = [{"id": 1, "name": "Python",
                "max_students": 20, "current_students": 20}]
    enrollments = []
    result = add_enrollment(enrollments, courses, 1, 1)
    assert result == "На курсе нет свободных мест."
    assert len(enrollments) == 0


def test_add_enrollment_duplicate():
    """запрет повторной записи."""
    courses = [{"id": 1, "name": "Python",
                "max_students": 30, "current_students": 28}]
    enrollments = []
    add_enrollment(enrollments, courses, 1, 1)
    result = add_enrollment(enrollments, courses, 1, 1)
    assert result == "Студент уже записан на этот курс."


def test_cancel_enrollment():
    """отмену записи."""
    courses = [{"id": 1, "name": "Python",
                "max_students": 30, "current_students": 29}]
    enrollments = [{"id": 1, "student_id": 1, "course_id": 1,
                    "enrollment_date": "2026-09-15", "status": "active"}]
    result = cancel_enrollment(enrollments, courses, 1, 1)
    assert result == "Запись отменена."
    assert enrollments[0]["status"] == "cancelled"
    assert courses[0]["current_students"] == 28
