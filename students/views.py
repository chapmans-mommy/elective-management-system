"""Список студентов и фильтрация по учебной группе из SQLite."""

from contextlib import closing

from django.shortcuts import render

from db.database import get_connection
from db.queries import get_query


def students_list(request):
    group = request.GET.get("group", "").strip()
    with closing(get_connection()) as conn:
        groups = conn.execute(get_query("student_groups")).fetchall()
        if group:
            students = conn.execute(
                get_query("students_by_group"), (group,),
            ).fetchall()
        else:
            students = conn.execute(get_query("students_list")).fetchall()
    return render(request, "students/student_list.html", {
        "students": students, "groups": groups, "selected_group": group,
    })
