"""View-функции приложения students."""

from django.http import HttpResponse

from homepage.views import page
from storage import load_students


def students_list(request) -> HttpResponse:
    """Страница со списком студентов."""
    students = load_students("data/students.json")

    items = ""
    for student in students:
        items += (
            f'<li class="list-group-item">'
            f'{student.name} — {student.group} '
            f'({student.email})'
            f'</li>'
        )

    content = f"""
    <h1>Студенты</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Студенты", content))