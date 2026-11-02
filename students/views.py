"""Список студентов, поиск по имени и фильтрация по группе через ORM."""

from django.shortcuts import render

from .models import Student


def students_list(request):
    group = request.GET.get("group", "").strip()
    keyword = request.GET.get("q", "").strip()
    groups = Student.objects.order_by("group_name").values(
        "group_name",
    ).distinct()
    students = Student.objects.all()
    if group:
        students = students.filter(group_name=group)
    if keyword:
        students = students.filter(name__icontains=keyword)
    return render(request, "students/student_list.html", {
        "students": students, "groups": groups, "selected_group": group,
        "q": keyword,
    })
