
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("courses/", include("courses.urls")),
    path("students/", include("students.urls")),
    path("enrollments/", include("enrollments.urls")),
]
