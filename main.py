import os

from courses import (
    find_course,
    search_courses,
    filter_available,
    sort_by_name,
    sort_by_seats,
    print_courses,
)
from enrollments import add_enrollment, cancel_enrollment
from storage import load_data, save_data
from utils import input_int


DATA_DIR = "data"
COURSES_FILE = os.path.join(DATA_DIR, "courses.json")
STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
ENROLLMENTS_FILE = os.path.join(DATA_DIR, "enrollments.json")


def show_stats(courses: list[dict],
               students: list[dict],
               enrollments: list[dict]) -> None:

    active = [e for e in enrollments if e["status"] == "active"]
    counts = {}
    for enrollment in active:
        cid = enrollment["course_id"]
        counts[cid] = counts.get(cid, 0) + 1

    top = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:3]

    print("СТАТИСТИКА")
    print(f"Курсов: {len(courses)} | "
          f"Студентов: {len(students)} | "
          f"Активных записей: {len(active)}")
    print("Топ-3 популярных курса:")
    for cid, count in top:
        course = find_course(courses, cid)
        if course:
            print(f"  {course['name']} — {count} записей")


def show_menu() -> None:
    print(" СИСТЕМА УПРАВЛЕНИЯ ФАКУЛЬТАТИВАМИ")
    print(" " * 55)
    print("1. Показать все курсы")
    print("2. Показать доступные курсы")
    print("3. Найти курс")
    print("4. Сортировать курсы по названию")
    print("5. Сортировать курсы по местам")
    print("6. Записаться на курс")
    print("7. Отменить запись")
    print("8. Показать статистику")
    print("0. Выход")


def main() -> None:
    courses = load_data(COURSES_FILE)
    students = load_data(STUDENTS_FILE)
    enrollments = load_data(ENROLLMENTS_FILE)

    while True:
        show_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            print_courses(courses, "Все курсы")
        elif choice == "2":
            print_courses(filter_available(courses), "Доступные курсы")
        elif choice == "3":
            keyword = input("Ключевое слово: ")
            results = search_courses(courses, keyword)
            print_courses(results, "Результаты поиска")
        elif choice == "4":
            print_courses(sort_by_name(courses), "Сортировка по названию")
        elif choice == "5":
            print_courses(sort_by_seats(courses), "Сортировка по местам")
        elif choice == "6":
            student_id = input_int("ID студента: ")
            course_id = input_int("ID курса: ")
            result = add_enrollment(
                enrollments, courses, student_id, course_id
            )
            print(result)
            save_data(ENROLLMENTS_FILE, enrollments)
            save_data(COURSES_FILE, courses)
        elif choice == "7":
            student_id = input_int("ID студента: ")
            course_id = input_int("ID курса: ")
            result = cancel_enrollment(
                enrollments, courses, student_id, course_id
            )
            print(result)
            save_data(ENROLLMENTS_FILE, enrollments)
            save_data(COURSES_FILE, courses)
        elif choice == "8":
            show_stats(courses, students, enrollments)
        elif choice == "0":
            print("До свидания")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
