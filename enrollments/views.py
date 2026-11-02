"""Журнал, карточка и статистика записей через Django ORM."""

from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Q, Sum
from django.db.models.functions import Round
from django.shortcuts import get_object_or_404, render

from courses.models import Course
from students.models import Student
from .forms import EnrollmentFilterForm, SORT_FIELDS, StatisticsForm
from .models import Enrollment


def _enrollments_page(request, active_only):
    data = request.GET.copy()
    if data.get("sort", "date") not in SORT_FIELDS:
        data["sort"] = "date"
    form = EnrollmentFilterForm(data or None)
    enrollments = Enrollment.objects.all()
    if active_only:
        enrollments = enrollments.exclude(is_cancelled=True)
    sort = "date"
    if form.is_bound:
        if form.is_valid():
            selected = form.cleaned_data
            if selected["date"]:
                enrollments = enrollments.filter(
                    enrollment_date=selected["date"],
                )
            if selected["course"]:
                enrollments = enrollments.filter(course=selected["course"])
            if selected["student"]:
                enrollments = enrollments.filter(student=selected["student"])
            if selected["q"]:
                enrollments = enrollments.filter(
                    Q(course__name__icontains=selected["q"])
                    | Q(student__name__icontains=selected["q"]),
                )
            sort = selected["sort"] or "date"
        else:
            enrollments = enrollments.none()
    enrollments = enrollments.annotate(
        student_name=F("student__name"),
        course_name=F("course__name"),
        group_name=F("student__group_name"),
    ).values(
        "id", "enrollment_date", "is_cancelled", "student_id", "course_id",
        "student_name", "course_name", "group_name",
    ).order_by(*SORT_FIELDS[sort])
    page_obj = Paginator(enrollments, 5).get_page(request.GET.get("page"))
    return render(request, "enrollments/enrollment_list.html", {
        "enrollments": page_obj, "page_obj": page_obj,
        "active_only": active_only, "form": form,
    })


def enrollments_list(request):
    """Все записи, включая отменённые: сценарий ПР7 сохранён."""
    return _enrollments_page(request, active_only=False)


def active_enrollments(request):
    return _enrollments_page(request, active_only=True)


def enrollment_detail(request, enrollment_id: int):
    enrollment = get_object_or_404(
        Enrollment.objects.select_related("student", "course"),
        pk=enrollment_id,
    )
    return render(request, "enrollments/enrollment_detail.html", {
        "enrollment": enrollment,
    })


def statistics(request):
    """Показатели ПР7, включая курсы и студентов без записей."""
    form = StatisticsForm(request.GET or None)
    valid = not form.is_bound or form.is_valid()
    threshold = 0
    if form.is_bound and valid:
        threshold = form.cleaned_data["threshold"] or 0
    course_totals = Course.objects.aggregate(
        course_count=Count("pk"), total_seats=Sum("max_students", default=0),
        occupied_seats=Sum("current_students", default=0),
        free_seats=Sum(F("max_students") - F("current_students"), default=0),
        average_capacity=Round(Avg("max_students", default=0), 1),
    )
    enrollment_totals = Enrollment.objects.aggregate(
        total=Count("pk"), active=Count("pk", filter=Q(is_cancelled=False)),
        cancelled=Count("pk", filter=Q(is_cancelled=True)),
    )
    course_statistics = Course.objects.annotate(
        free_seats=F("max_students") - F("current_students"),
        total_enrollments=Count("enrollments"),
        active=Count(
            "enrollments", filter=Q(enrollments__is_cancelled=False),
        ),
        cancelled=Count(
            "enrollments", filter=Q(enrollments__is_cancelled=True),
        ),
    ).values(
        "id", "name", "max_students", "current_students", "free_seats",
        "total_enrollments", "active", "cancelled",
    ).order_by("-active", "name", "id")
    student_statistics = Student.objects.annotate(
        total_enrollments=Count("enrollments"),
        active=Count(
            "enrollments", filter=Q(enrollments__is_cancelled=False),
        ),
        cancelled=Count(
            "enrollments", filter=Q(enrollments__is_cancelled=True),
        ),
    ).values(
        "id", "name", "group_name", "total_enrollments", "active", "cancelled",
    ).order_by("-active", "name", "id")
    group_statistics = Student.objects.values("group_name").annotate(
        student_count=Count("pk"),
    ).order_by("group_name")
    popular_courses = Course.objects.annotate(
        active=Count("enrollments", filter=Q(enrollments__is_cancelled=False)),
    ).filter(active__gt=threshold).values(
        "id", "name", "active",
    ).order_by("-active", "name", "id") if valid else []
    return render(request, "enrollments/statistics.html", {
        "course_totals": course_totals,
        "enrollment_totals": enrollment_totals,
        "course_statistics": course_statistics,
        "student_statistics": student_statistics,
        "group_statistics": group_statistics,
        "popular_courses": popular_courses,
        "form": form, "threshold": threshold,
    })
