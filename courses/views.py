"""Страницы курсов получают данные из SQLite средствами sqlite3."""

from contextlib import closing

from django.shortcuts import render

from db.database import get_connection
from db.queries import get_query
from .forms import AvailableCoursesForm, CourseSearchForm


def courses_list(request):
    """Список курсов и поиск по названию и свободным местам."""
    form = CourseSearchForm(request.GET or None)
    with closing(get_connection()) as conn:
        if not form.is_bound:
            courses = conn.execute(get_query("courses_list")).fetchall()
        elif form.is_valid():
            keyword = "%" + form.cleaned_data["q"] + "%"
            minimum = form.cleaned_data["min_seats"] or 0
            courses = conn.execute(
                get_query("courses_search"), (keyword, keyword, minimum),
            ).fetchall()
        else:
            courses = []
    return render(request, "courses/course_list.html", {
        "courses": courses, "form": form,
    })


def course_detail(request, course_id: int):
    """Страница отдельного курса."""
    with closing(get_connection()) as conn:
        course = conn.execute(
            get_query("course_detail"), (course_id,),
        ).fetchone()
    return render(
        request, "courses/course_detail.html", {"course": course},
        status=404 if course is None else 200,
    )


def available_courses(request):
    """Поиск курсов с местами, начинающихся не раньше выбранной даты."""
    form = AvailableCoursesForm(request.GET or None)
    courses = []
    searched = False
    if form.is_bound and form.is_valid():
        searched = True
        selected_date = form.cleaned_data["date"].isoformat()
        minimum = form.cleaned_data["min_seats"] or 1
        with closing(get_connection()) as conn:
            courses = conn.execute(
                get_query("available_courses"), (selected_date, minimum),
            ).fetchall()
    return render(request, "courses/available_courses.html", {
        "courses": courses, "form": form, "searched": searched,
    })
