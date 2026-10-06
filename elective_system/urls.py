
from django.contrib import admin
from django.urls import include, path
from homepage import views as homepage_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("courses/", include("courses.urls")),
    path("students/", include("students.urls")),
    path("enrollments/", include("enrollments.urls")),
]

handler404 = "homepage.views.page_not_found"