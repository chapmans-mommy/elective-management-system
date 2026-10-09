"""Маршруты приложения students."""

from django.urls import path

from . import views

app_name = "students"

urlpatterns = [
    path("", views.students_list, name="list"),
]