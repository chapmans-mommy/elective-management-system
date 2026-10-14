"""Маршруты приложения enrollments."""

from django.urls import path

from . import views

app_name = "enrollments"

urlpatterns = [
    path("", views.enrollments_list, name="list"),
    path("active/", views.active_enrollments, name="active"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:enrollment_id>/", views.enrollment_detail, name="detail"),
]
