"""Факультативные курсы в базе Django."""

from django.core.validators import MinValueValidator
from django.db import models


class Course(models.Model):
    name = models.CharField("Название", max_length=256)
    description = models.TextField("Описание", blank=True, null=True)
    teacher = models.CharField("Преподаватель", max_length=256)
    max_students = models.PositiveIntegerField(
        "Количество мест", validators=[MinValueValidator(1)],
    )
    current_students = models.PositiveIntegerField("Занято мест", default=0)
    start_date = models.DateField(
        "Дата начала", blank=True, null=True, db_index=True,
    )

    @property
    def free_seats(self):
        return self.max_students - self.current_students

    def has_free_seats(self):
        return self.current_students < self.max_students

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name", "pk"]
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(max_students__gt=0),
                name="course_capacity_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(current_students__lte=models.F(
                    "max_students",
                )),
                name="course_occupancy_within_capacity",
            ),
        ]
