"""Проверка параметров журнала записей и статистики."""

from django import forms

from courses.models import Course
from students.models import Student


SORT_FIELDS = {
    "date": ("-enrollment_date", "-id"),
    "date_asc": ("enrollment_date", "id"),
    "course": ("course__name", "id"),
    "student": ("student__name", "id"),
}


class EnrollmentFilterForm(forms.Form):
    date = forms.DateField(
        label="Дата записи", required=False, input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    course = forms.ModelChoiceField(
        label="Курс", queryset=Course.objects.order_by("name"), required=False,
        empty_label="Все курсы",
    )
    student = forms.ModelChoiceField(
        label="Студент", queryset=Student.objects.order_by("name"),
        required=False, empty_label="Все студенты",
    )
    q = forms.CharField(
        label="Название курса или имя студента",
        required=False)
    sort = forms.ChoiceField(
        label="Сортировать по", required=False, initial="date",
        choices=[("date", "Дате: сначала новые"),
                 ("date_asc", "Дате: сначала старые"),
                 ("course", "Курсу"), ("student", "Студенту")],
    )


class StatisticsForm(forms.Form):
    threshold = forms.IntegerField(
        label="Число активных записей больше", min_value=0,
        required=False, initial=0,
    )
