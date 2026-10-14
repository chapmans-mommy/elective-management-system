"""Проверка параметров поиска курсов."""

from django import forms


class CourseSearchForm(forms.Form):
    q = forms.CharField(label="Название или описание", required=False)
    min_seats = forms.IntegerField(
        label="Минимум свободных мест", min_value=0,
        required=False, initial=0,
    )


class AvailableCoursesForm(forms.Form):
    date = forms.DateField(
        label="Дата начала не раньше", input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    min_seats = forms.IntegerField(
        label="Минимум свободных мест", min_value=1,
        required=False, initial=1,
    )
