"""View-функции приложения enrollments."""

from django.http import HttpResponse

from homepage.views import page
from models.enrollments import find_enrollment_by_id
from storage import (
    load_courses, load_students, load_enrollments,
)


def enrollments_list(request) -> HttpResponse:
    """Страница со списком всех записей."""
    courses = load_courses("data/courses.json")
    students = load_students("data/students.json")
    enrollments = load_enrollments(
        "data/enrollments.json", students, courses
    )

    items = ""
    for e in enrollments:
        status = "отменена" if e.is_cancelled else "активна"
        badge = "bg-secondary" if e.is_cancelled else "bg-success"
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between">'
            f'<a href="/enrollments/{e.id}/">'
            f'{e.student.name} → {e.course.name}</a>'
            f'<span class="badge {badge}">{status}</span>'
            f'</li>'
        )

    content = f"""
    <h1>Записи на курсы</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Записи", content))


def enrollment_detail(request, enrollment_id: int) -> HttpResponse:
    """Страница отдельной записи."""
    courses = load_courses("data/courses.json")
    students = load_students("data/students.json")
    enrollments = load_enrollments(
        "data/enrollments.json", students, courses
    )
    enrollment = find_enrollment_by_id(enrollments, enrollment_id)

    if enrollment is None:
        content = """
        <h1 class="text-danger">Запись не найдена</h1>
        <a href="/enrollments/" class="btn btn-outline-secondary">
            ← к списку записей
        </a>
        """
        return HttpResponse(
            page("Запись не найдена", content), status=404
        )

    status = "отменена" if enrollment.is_cancelled else "активна"
    badge = "bg-secondary" if enrollment.is_cancelled else "bg-success"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">
                Запись №{enrollment.id}
            </h5>
            <p class="card-text">
                <strong>Студент:</strong>
                {enrollment.student.name}
            </p>
            <p class="card-text">
                <strong>Курс:</strong> {enrollment.course.name}
            </p>
            <p class="card-text">
                <strong>Дата записи:</strong>
                {enrollment.enrollment_date}
            </p>
            <p class="card-text">
                <strong>Статус:</strong>
                <span class="badge {badge}">{status}</span>
            </p>
            <a href="/enrollments/"
               class="btn btn-outline-secondary">
                ← к списку записей
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Запись №{enrollment.id}", content)
    )