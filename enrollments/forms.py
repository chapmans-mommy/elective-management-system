"""Параметры статистики записей."""

from django import forms


class StatisticsForm(forms.Form):
    threshold = forms.IntegerField(
        label="Число активных записей больше", min_value=0,
        required=False, initial=0,
    )
