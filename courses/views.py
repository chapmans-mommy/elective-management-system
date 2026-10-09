"""View-функции приложения courses."""

from django.shortcuts import render

from models.courses import find_course
from storage import load_courses


def courses_list(request):
    """Страница со списком всех курсов."""
    courses = load_courses("data/courses.json")
    context = {"courses": courses}
    return render(request, "courses/course_list.html", context)


def course_detail(request, course_id: int):
    """Страница отдельного курса."""
    courses = load_courses("data/courses.json")
    course = find_course(courses, course_id)
    context = {"course": course}
    return render(
        request,
        "courses/course_detail.html",
        context,
        status=404 if course is None else 200,
    )