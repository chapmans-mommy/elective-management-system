"""Записи студентов на факультативы."""

from django.db import models


class Enrollment(models.Model):
    student = models.ForeignKey(
        "students.Student", on_delete=models.PROTECT,
        related_name="enrollments", verbose_name="Студент",
    )
    course = models.ForeignKey(
        "courses.Course", on_delete=models.PROTECT,
        related_name="enrollments", verbose_name="Курс",
    )
    enrollment_date = models.DateField("Дата записи")
    is_cancelled = models.BooleanField("Запись отменена", default=False)

    def cancel(self):
        self.is_cancelled = True
        self.save(update_fields=["is_cancelled"])

    def is_active(self):
        return not self.is_cancelled

    def __str__(self):
        return f"{self.student} → {self.course} ({self.enrollment_date})"

    class Meta:
        ordering = ["-enrollment_date", "-pk"]
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
