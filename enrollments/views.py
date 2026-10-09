"""View-функции приложения enrollments."""

from django.shortcuts import render

from models.enrollments import find_enrollment_by_id
from storage import load_courses, load_students, load_enrollments


def enrollments_list(request):
    """Страница со списком всех записей."""
    courses = load_courses("data/courses.json")
    students = load_students("data/students.json")
    enrollments = load_enrollments(
        "data/enrollments.json", students, courses
    )
    context = {"enrollments": enrollments}
    return render(request, "enrollments/enrollment_list.html", context)


def enrollment_detail(request, enrollment_id: int):
    """Страница отдельной записи."""
    courses = load_courses("data/courses.json")
    students = load_students("data/students.json")
    enrollments = load_enrollments(
        "data/enrollments.json", students, courses
    )
    enrollment = find_enrollment_by_id(enrollments, enrollment_id)
    context = {"enrollment": enrollment}
    return render(
        request,
        "enrollments/enrollment_detail.html",
        context,
        status=404 if enrollment is None else 200,
    )