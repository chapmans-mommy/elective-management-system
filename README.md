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

- `main.py` — точка запуска, меню
- `storage.py` — JSON с преобразованием в объекты
- `utils.py` — безопасный ввод
- `models/` — пакет с классами
  - `courses.py` — класс Course + функции
  - `students.py` — класс Student + функции
  - `enrollments.py` — класс Enrollment + функции
- `data/` — JSON-файлы
- `tests/` — тесты pytest

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