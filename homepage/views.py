"""View-функции приложения homepage."""

from django.shortcuts import render


def index(request):
    """Главная страница."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception=None):
    """Страница 404: объект или адрес не найдены."""
    return render(request, "404.html", status=404)