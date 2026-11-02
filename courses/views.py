"""Список, карточка и поиск доступных курсов через Django ORM."""

from django.db.models import F, Q
from django.shortcuts import get_object_or_404, render

from .forms import AvailableCoursesForm, CourseSearchForm
from .models import Course


def courses_list(request):
    """Поиск по названию/описанию и количеству свободных мест."""
    form = CourseSearchForm(request.GET or None)
    courses = Course.objects.order_by("name", "pk")
    if form.is_bound:
        if form.is_valid():
            keyword = form.cleaned_data["q"]
            minimum = form.cleaned_data["min_seats"] or 0
            courses = courses.annotate(
                remaining_seats=F("max_students") - F("current_students"),
            ).filter(
                Q(name__icontains=keyword) | Q(description__icontains=keyword),
                remaining_seats__gte=minimum,
            )
        else:
            courses = courses.none()
    return render(request, "courses/course_list.html", {
        "courses": courses, "form": form,
    })


def course_detail(request, course_id: int):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "courses/course_detail.html", {"course": course})


def available_courses(request):
    """Свободные места на курсах, начинающихся не раньше выбранной даты."""
    form = AvailableCoursesForm(request.GET or None)
    courses = Course.objects.none()
    searched = False
    if form.is_bound and form.is_valid():
        searched = True
        courses = Course.objects.annotate(
            remaining_seats=F("max_students") - F("current_students"),
        ).filter(
            start_date__gte=form.cleaned_data["date"],
            remaining_seats__gte=form.cleaned_data["min_seats"] or 1,
        ).exclude(
            current_students__gte=F("max_students"),
        ).order_by("start_date", "name", "pk")
    return render(request, "courses/available_courses.html", {
        "courses": courses, "form": form, "searched": searched,
    })
