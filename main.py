"""Точка запуска: система управления факультативами."""

import os
from typing import List

from models import Course, Student, Enrollment
from models.courses import (
    find_course, search_courses, filter_available,
    sort_by_name, sort_by_seats, print_courses,
)
from models.students import find_student, print_students
from models.enrollments import (
    add_enrollment, cancel_enrollment, print_enrollments,
)
from storage import (
    load_courses, save_courses,
    load_students,
    load_enrollments, save_enrollments,
)
from utils import input_int


DATA_DIR = "data"
COURSES_FILE = os.path.join(DATA_DIR, "courses.json")
STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
ENROLLMENTS_FILE = os.path.join(DATA_DIR, "enrollments.json")


def create_new_enrollment(
    enrollments: List[Enrollment],
    courses: List[Course],
    students: List[Student],
) -> None:
    """Сценарий создания записи на курс."""
    student_id = input_int("ID студента: ")
    student = find_student(students, student_id)
    if student is None:
        print("Студент не найден.")
        return

    course_id = input_int("ID курса: ")
    course = find_course(courses, course_id)
    if course is None:
        print("Курс не найден.")
        return

    result = add_enrollment(enrollments, student, course)
    print(result)


def cancel_existing_enrollment(
    enrollments: List[Enrollment],
) -> None:
    """Сценарий отмены записи."""
    student_id = input_int("ID студента: ")
    course_id = input_int("ID курса: ")
    result = cancel_enrollment(enrollments, student_id, course_id)
    print(result)


def show_stats(
    courses: List[Course],
    students: List[Student],
    enrollments: List[Enrollment],
) -> None:
    """Вывести статистику."""
    active = [e for e in enrollments if e.is_active()]
    print("\n=== СТАТИСТИКА ===")
    print(f"Курсов: {len(courses)} | "
          f"Студентов: {len(students)} | "
          f"Активных записей: {len(active)}")


def show_menu() -> None:
    """Вывести меню."""
    print("\n" + "=" * 55)
    print("   СИСТЕМА УПРАВЛЕНИЯ ФАКУЛЬТАТИВАМИ")
    print("=" * 55)
    print("1. Показать все курсы")
    print("2. Показать доступные курсы")
    print("3. Найти курс")
    print("4. Сортировать по названию")
    print("5. Сортировать по местам")
    print("6. Показать студентов")
    print("7. Записаться на курс")
    print("8. Отменить запись")
    print("9. Показать записи")
    print("10. Показать статистику")
    print("0. Выход")


def main() -> None:
    """Точка запуска приложения."""
    courses = load_courses(COURSES_FILE)
    students = load_students(STUDENTS_FILE)
    enrollments = load_enrollments(ENROLLMENTS_FILE, students, courses)

    while True:
        show_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            print_courses(courses, "Все курсы")
        elif choice == "2":
            print_courses(filter_available(courses), "Доступные курсы")
        elif choice == "3":
            keyword = input("Ключевое слово: ")
            print_courses(
                search_courses(courses, keyword),
                "Результаты поиска",
            )
        elif choice == "4":
            print_courses(sort_by_name(courses), "Сортировка по названию")
        elif choice == "5":
            print_courses(sort_by_seats(courses), "Сортировка по местам")
        elif choice == "6":
            print_students(students, "Студенты")
        elif choice == "7":
            create_new_enrollment(enrollments, courses, students)
            save_enrollments(ENROLLMENTS_FILE, enrollments)
            save_courses(COURSES_FILE, courses)
        elif choice == "8":
            cancel_existing_enrollment(enrollments)
            save_enrollments(ENROLLMENTS_FILE, enrollments)
            save_courses(COURSES_FILE, courses)
        elif choice == "9":
            print_enrollments(enrollments, "Записи")
        elif choice == "10":
            show_stats(courses, students, enrollments)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Некорректный выбор.")


if __name__ == "__main__":
    main()
