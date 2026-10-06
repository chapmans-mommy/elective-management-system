"""View-функции приложения homepage."""

from django.http import HttpResponse


BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
    "/dist/css/bootstrap.min.css"
)


def page(title: str, content: str) -> str:
    """Сформировать HTML-каркас страницы.

    Args:
        title: заголовок вкладки.
        content: HTML-содержимое страницы.

    Returns:
        Полный HTML-документ.
    """
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,
          initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">Факультативы</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/courses/">Курсы</a>
                <a class="nav-link" href="/students/">Студенты</a>
                <a class="nav-link" href="/enrollments/">Записи</a>
            </div>
        </div>
    </nav>
    <main class="container">
        {content}
    </main>
</body>
</html>"""


def index(request) -> HttpResponse:
    """Главная страница."""
    content = """
    <h1 class="display-4">Система управления факультативами</h1>
    <p class="lead">Приложение для учёта факультативных курсов
    и записи студентов.</p>
    <p>Основные разделы:</p>
    <a href="/courses/" class="btn btn-primary me-2">Курсы</a>
    <a href="/students/" class="btn btn-secondary me-2">Студенты</a>
    <a href="/enrollments/" class="btn btn-success">Записи</a>
    """
    return HttpResponse(page("Главная", content))

def page_not_found(request, exception=None) -> HttpResponse:
    """Страница 404: объект или адрес не найдены.

    Args:
        request: HTTP-запрос.
        exception: исключение, вызвавшее 404 (обычно не используется).

    Returns:
        HTTP-ответ со статусом 404 и HTML-страницей.
    """
    content = """
    <div class="text-center mt-5">
        <h1 class="display-1 text-danger">404</h1>
        <h2 class="mb-3">Страница не найдена</h2>
        <p class="lead">
            Возможно, объект был удалён, либо адрес введён неверно.
        </p>
        <a href="/" class="btn btn-primary">
            ← Вернуться на главную
        </a>
        <a href="/courses/" class="btn btn-outline-secondary ms-2">
            К списку курсов
        </a>
    </div>
    """
    return HttpResponse(
        page("Страница не найдена", content),
        status=404,
    )