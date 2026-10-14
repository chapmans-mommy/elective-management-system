# Система управления факультативами

Веб-приложение на Django для учёта факультативных курсов
и управления записью студентов. Консольная версия из ПР3 сохранена.

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

    python -m db.import_json
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
| `/courses/available/` | Свободные места по дате начала | `courses.views.available_courses` |
| `/enrollments/active/` | Активные записи | `enrollments.views.active_enrollments` |
| `/enrollments/statistics/` | Статистика | `enrollments.views.statistics` |


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
- SQLite и стандартная библиотека sqlite3 (ПР7)
- JSON-хранилище консольной версии из ПР3

## Формат данных

Исходные данные для импорта и консольной версии хранятся в JSON-файлах
в каталоге `data/`. Веб-приложение ПР7 читает `data/electives.sqlite`:

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

## Текущий этап разработки: ПР7

Веб-приложение получает данные из отдельной базы `data/electives.sqlite`
через стандартную библиотеку `sqlite3`. Таблицы создаются SQL-командами,
без Django ORM и миграций предметной области. Служебная Django-база
`db.sqlite3` остаётся отдельной.

### Структура базы данных

| Таблица | Поля и типы |
|---------|-------------|
| `courses` | `id INTEGER`, `name TEXT`, `description TEXT`, `teacher TEXT`, `max_students INTEGER`, `current_students INTEGER`, `start_date TEXT` |
| `students` | `id INTEGER`, `name TEXT`, `group_name TEXT`, `email TEXT` |
| `enrollments` | `id INTEGER`, `student_id INTEGER`, `course_id INTEGER`, `enrollment_date TEXT`, `is_cancelled INTEGER` |

- Первичный ключ каждой таблицы: `id INTEGER PRIMARY KEY`.
- Внешние ключи: `enrollments.student_id → students.id` и
  `enrollments.course_id → courses.id`.
- `description` и `start_date` могут иметь значение `NULL`,
  остальные поля обязательны.
- Даты хранятся как `TEXT` в формате `YYYY-MM-DD`.
- `is_cancelled`: 0 — активная запись, 1 — отменённая; значение по умолчанию 0.
- `max_students > 0`; `current_students` от 0 до `max_students`.
- Для связей записей и даты начала курсов созданы индексы.

Число занятых мест `current_students` переносится из JSON без пересчёта:
исходный журнал содержит только 5 записей и не описывает всю занятость
курсов. Свободные места равны `max_students - current_students`.
Статистика записей отдельно считает фактические строки журнала,
включая отменённые записи. Курсы и студенты без записей также отображаются.

### Файлы и импорт

- `sql/schema.sql` — таблицы, ограничения и индексы.
- `sql/queries.sql` — 16 запросов с комментариями и примерами параметров.
- `db/database.py` — абсолютный путь к базе, `sqlite3.connect()`,
  `sqlite3.Row` и `PRAGMA foreign_keys = ON` для каждого подключения.
- `db/import_json.py` — создание схемы и перенос JSON через
  `executemany()`, параметры `?`, `commit()` и `rollback()`.
- `db/queries.py` — загрузка именованных запросов из SQL-файла:
  представления используют тот же SQL, который проверяется в CLI.

Для запуска из PowerShell в корне проекта:

```powershell
.\venv\Scripts\Activate.ps1
python -m db.import_json
python manage.py runserver
```

Импортировано 3 курса, 3 студента, 5 записей; исходные JSON сохранены.
Повторный запуск импорта обновляет записи по идентификатору, не создавая
дубликатов. Записи, добавленные только в SQLite, не удаляются. Ошибка
импорта отменяет изменения всей транзакции. Статусы `active`/`cancelled`
преобразуются в `is_cancelled`. Поле JSON `group` хранится как `group_name`.

Если виртуального окружения ещё нет:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m db.import_json
```

### Запросы и пользовательские сценарии

| № | Запрос | Назначение и страница |
|---|--------|----------------------|
| 1 | `courses_list` | Список курсов: `/courses/` |
| 2 | `students_list` | Список студентов: `/students/` |
| 3 | `courses_search` | Название/описание и минимум мест: `/courses/?q=SQL&min_seats=5` |
| 4 | `available_courses` | Места и дата начала: `/courses/available/?date=2026-10-01&min_seats=1` |
| 5 | `enrollments_list` | Журнал с данными курса и студента: `/enrollments/` |
| 6 | `enrollment_detail` | Подробности записи: `/enrollments/1/` |
| 7 | `course_totals` | COUNT, SUM, AVG мест: `/enrollments/statistics/` |
| 8 | `enrollment_totals` | COUNT, SUM записей и статусов: статистика |
| 9 | `course_statistics` | GROUP BY, LEFT JOIN записей по курсам: статистика |
| 10 | `student_statistics` | GROUP BY, LEFT JOIN записей по студентам: статистика |
| 11 | `popular_courses` | GROUP BY, HAVING активных записей больше порога: статистика |
| 12 | `course_detail` | Карточка курса: `/courses/1/` |
| 13 | `active_enrollments` | Активные записи: `/enrollments/active/` |
| 14 | `students_by_group` | WHERE по группе: `/students/?group=ЭФБО-02-24` |
| 15 | `student_groups` | DISTINCT групп для формы на странице студентов |
| 16 | `group_statistics` | GROUP BY, COUNT студентов по группам: статистика |

Реализованы больше пяти сценариев: просмотр и поиск курсов, карточка курса,
поиск свободных мест по дате начала, просмотр студентов и фильтр по группе,
журнал всех/активных записей, подробности записи, статистика и фильтр
популярных курсов по числу активных записей.

Поиск по дате означает: курс начинается в выбранный день или позже
и имеет необходимое количество свободных мест. Это адаптация примера
поиска помещений к факультативам; расписание отдельных занятий в исходных
данных отсутствует. Например, на 2026-10-01 доступны курсы 1 и 3,
на 2026-10-10 — курс 3. Полный курс 2 не попадает в результаты.

Представления `courses/views.py`, `students/views.py`, `enrollments/views.py`
получают именованные строки SQLite и передают их через контекст шаблонам.
Введённые значения передаются параметрами `?`, даты и числа проверяются
Django-формами. Переходы и действия форм используют именованные URL;
раздел «Статистика» добавлен в общее меню.

### Проверка SQL в SQLite CLI

SQLite CLI установлен в текущем `venv/Scripts/sqlite3.exe`.
После активации окружения:

```powershell
sqlite3 data/electives.sqlite
```

В консоли SQLite можно проверить таблицы и связи:

```sql
.tables
.schema
PRAGMA foreign_keys = ON;
PRAGMA foreign_key_check;
SELECT COUNT(*) FROM courses;
SELECT COUNT(*) FROM students;
SELECT COUNT(*) FROM enrollments;
```

Все 16 запросов проверены в SQLite CLI с параметрами из комментариев
к `sql/queries.sql`. Для параметризованного поиска по дате:

```sql
.parameter init
.parameter set ?1 "'2026-10-01'"
.parameter set ?2 1
SELECT id, name, start_date, max_students - current_students AS free_seats
FROM courses
WHERE start_date >= ?1
  AND max_students - current_students >= ?2
  AND current_students < max_students
ORDER BY start_date, name, id;
.exit
```

### Проверки проекта

```powershell
python manage.py check
python -m pytest -v
python -m flake8 . --extend-exclude=venv
```

Тесты проверяют прежние классы, сохранность импортированных данных,
внешние ключи, откат неуспешного импорта, повторный импорт без дубликатов,
статистику, страницы и поиск, неверный ввод, SQL-инъекции, пустую базу
и отображение изменения записи непосредственно из SQLite.
