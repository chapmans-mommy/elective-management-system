"""Студенты предметной области, отдельно от пользователей Django."""

from django.db import models


class Student(models.Model):
    name = models.CharField("ФИО", max_length=256)
    group_name = models.CharField("Учебная группа", max_length=64)
    email = models.EmailField("Электронная почта")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name", "pk"]
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
