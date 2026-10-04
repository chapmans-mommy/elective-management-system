"""Маршруты приложения enrollments."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.enrollments_list, name="enrollments_list"),
    path("<int:enrollment_id>/", views.enrollment_detail,
         name="enrollment_detail"),
]