"""View-функции приложения courses."""

from django.http import HttpResponse

from homepage.views import page
from models.courses import find_course
from storage import load_courses


def courses_list(request) -> HttpResponse:
    """Страница со списком всех курсов."""
    courses = load_courses("data/courses.json")

    items = ""
    for course in courses:
        free = course.free_seats()
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between align-items-center">'
            f'<a href="/courses/{course.id}/">{course.name}</a>'
            f'<span class="badge bg-info">{free} мест</span>'
            f'</li>'
        )

    content = f"""
    <h1>Курсы</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Курсы", content))


def course_detail(request, course_id: int) -> HttpResponse:
    """Страница отдельного курса."""
    courses = load_courses("data/courses.json")
    course = find_course(courses, course_id)

    if course is None:
        content = """
        <h1 class="text-danger">Курс не найден</h1>
        <a href="/courses/" class="btn btn-outline-secondary">
            ← к списку курсов
        </a>
        """
        return HttpResponse(
            page("Курс не найден", content), status=404
        )

    free = course.free_seats()
    badge = "bg-success" if free > 0 else "bg-danger"
    status = "есть места" if free > 0 else "мест нет"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{course.name}</h5>
            <p class="card-text">{course.description}</p>
            <p class="card-text">
                <strong>Преподаватель:</strong> {course.teacher}
            </p>
            <p class="card-text">
                <strong>Дата начала:</strong> {course.start_date}
            </p>
            <p class="card-text">
                <strong>Мест:</strong> {course.current_students}
                / {course.max_students}
                <span class="badge {badge}">{status}</span>
            </p>
            <a href="/courses/" class="btn btn-outline-secondary">
                ← к списку курсов
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(course.name, content))