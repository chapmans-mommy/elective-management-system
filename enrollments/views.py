"""Журнал записей и статистика из SQLite, без Django ORM."""

from contextlib import closing

from django.shortcuts import render

from db.database import get_connection
from db.queries import get_query
from .forms import StatisticsForm


def enrollments_list(request):
    """Все записи, включая отменённые."""
    with closing(get_connection()) as conn:
        enrollments = conn.execute(
            get_query("enrollments_list"),
        ).fetchall()
    return render(request, "enrollments/enrollment_list.html", {
        "enrollments": enrollments, "active_only": False,
    })


def active_enrollments(request):
    """Активные записи с именами студентов и названиями курсов."""
    with closing(get_connection()) as conn:
        enrollments = conn.execute(
            get_query("active_enrollments"),
        ).fetchall()
    return render(request, "enrollments/enrollment_list.html", {
        "enrollments": enrollments, "active_only": True,
    })


def enrollment_detail(request, enrollment_id: int):
    """Подробности записи из трёх связанных таблиц."""
    with closing(get_connection()) as conn:
        enrollment = conn.execute(
            get_query("enrollment_detail"), (enrollment_id,),
        ).fetchone()
    return render(
        request, "enrollments/enrollment_detail.html",
        {"enrollment": enrollment},
        status=404 if enrollment is None else 200,
    )


def statistics(request):
    """Статистика курсов, студентов и групп; популярные курсы."""
    form = StatisticsForm(request.GET or None)
    valid = not form.is_bound or form.is_valid()
    threshold = 0
    if form.is_bound and valid:
        threshold = form.cleaned_data["threshold"] or 0
    with closing(get_connection()) as conn:
        context = {
            "course_totals": conn.execute(
                get_query("course_totals"),
            ).fetchone(),
            "enrollment_totals": conn.execute(
                get_query("enrollment_totals"),
            ).fetchone(),
            "course_statistics": conn.execute(
                get_query("course_statistics"),
            ).fetchall(),
            "student_statistics": conn.execute(
                get_query("student_statistics"),
            ).fetchall(),
            "group_statistics": conn.execute(
                get_query("group_statistics"),
            ).fetchall(),
            "popular_courses": conn.execute(
                get_query("popular_courses"), (threshold,),
            ).fetchall() if valid else [],
            "form": form, "threshold": threshold,
        }
    return render(request, "enrollments/statistics.html", context)
