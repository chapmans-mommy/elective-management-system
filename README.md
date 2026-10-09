# Система управления факультативами

Консольное приложение для учёта факультативных курсов
и управления записью студентов.

## Возможности

- просмотр и поиск курсов;
- фильтрация по доступности;
- сортировка по названию и количеству мест;
- запись студента на курс;
- отмена записи;
- статистика (топ курсов, количество записей).

## Основные классы

### Course — факультативный курс
**Атрибуты:** id, name, description, teacher,
max_students, current_students, start_date
**Методы:** has_free_seats(), free_seats(),
from_data(), to_data(), __str__()

### Student — студент
**Атрибуты:** id, name, group, email
**Методы:** from_data(), to_data(), __str__()

### Enrollment — запись на курс
**Атрибуты:** id, student (объект Student),
course (объект Course), enrollment_date, is_cancelled
**Методы:** cancel(), is_active(), from_data(), to_data(), __str__()

## Структура проекта

- `main.py` — консольная версия приложения (сохранена из ПР3)
- `storage.py` — загрузка и сохранение данных в JSON
- `utils.py` — безопасный ввод для консольной версии
- `manage.py` — управление Django-проектом
- `models/` — пакет с классами предметной области (ПР3)
  - `courses.py` — класс `Course` + функции работы с курсами
  - `students.py` — класс `Student` + функции работы со студентами
  - `enrollments.py` — класс `Enrollment` + функции работы с записями
- `data/` — JSON-файлы данных
  - `courses.json`
  - `students.json`
  - `enrollments.json`
- `tests/` — тесты pytest для классов предметной области
- `elective_system/` — настройки Django-проекта
  - `settings.py`
  - `urls.py`
- `homepage/` — Django-приложение главной страницы
  - `views.py` — view-функции `index()` и `page_not_found()`
  - `urls.py` — маршруты приложения
  - `templates/homepage/index.html` — шаблон главной
  - `static/homepage/` — собственные статические файлы
    - `css/style.css`
    - `js/main.js`
    - `img/logo.png`
- `courses/` — Django-приложение курсов
  - `views.py` — `courses_list()`, `course_detail()`
  - `urls.py` — маршруты с `app_name = "courses"`
  - `templates/courses/`
    - `course_list.html`
    - `course_detail.html`
    - `includes/course_card.html`
- `students/` — Django-приложение студентов
  - `views.py` — `students_list()`
  - `urls.py` — маршруты с `app_name = "students"`
  - `templates/students/student_list.html`
- `enrollments/` — Django-приложение записей
  - `views.py` — `enrollments_list()`, `enrollment_detail()`
  - `urls.py` — маршруты с `app_name = "enrollments"`
  - `templates/enrollments/`
    - `enrollment_list.html`
    - `enrollment_detail.html`
    - `includes/enrollment_status.html`
- `templates/` — шаблоны уровня проекта
  - `base.html` — базовый шаблон с блоками `title` и `content`
  - `404.html` — кастомная страница 404
  - `includes/navigation.html` — навигация

## Веб-интерфейс на Django

### Запуск

    python manage.py runserver

Открыть http://127.0.0.1:8000/

### Страницы

| URL | Назначение | View-функция |
|-----|-----------|--------------|
| `/` | Главная | `homepage.views.index` |
| `/courses/` | Список курсов | `courses.views.courses_list` |
| `/courses/<int:course_id>/` | Страница курса | `courses.views.course_detail` |
| `/students/` | Список студентов | `students.views.students_list` |
| `/enrollments/` | Список записей | `enrollments.views.enrollments_list` |
| `/enrollments/<int:enrollment_id>/` | Страница записи | `enrollments.views.enrollment_detail` |


## Django Template Language

- `templates/base.html` — базовый шаблон с блоками `title` и `content`
- дочерние шаблоны используют `{% extends "base.html" %}`
- включаемые фрагменты через `{% include %}`:
  - `includes/navigation.html` — навигация
  - `courses/includes/course_card.html` — карточка курса
  - `enrollments/includes/enrollment_status.html` — статус записи
- циклы `{% for %}`, условия `{% if %}`, `{% empty %}`
- фильтры `|length`, `|default`
- именованные URL через `{% url %}` с пространствами имён
- статические файлы (`{% load static %}`): CSS, JS, логотип

## Статические файлы

- `homepage/static/homepage/css/style.css` — собственные стили
- `homepage/static/homepage/js/main.js` — вывод текущего года в подвал
- `homepage/static/homepage/img/logo.png` — логотип в навигации

### Используемые технологии

- Django 5.2
- Bootstrap 5.3 (CDN)
- JSON-хранилище из ПР3

## Формат данных

Данные хранятся в JSON-файлах в каталоге `data/`:

- `courses.json` — список курсов;
- `students.json` — список студентов;
- `enrollments.json` — список записей.

## Требования

- Python 3.10+;
- pytest;
- flake8.

Установка зависимостей:

pip install -r requirements.txt

## Запуск программы

python main.py

## Запуск тестов

python -m pytest

## Проверка качества кода

flake8 --exclude=venv,.venv,__pycache__,.pytest_cache