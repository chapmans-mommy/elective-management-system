"""View-функции приложения students."""

from django.shortcuts import render

from storage import load_students


def students_list(request):
    """Страница со списком студентов."""
    students = load_students("data/students.json")
    context = {"students": students}
    return render(request, "students/student_list.html", context)