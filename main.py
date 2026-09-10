import json
import os
from datetime import date

DATA_DIR = "data"
COURSES_FILE = os.path.join(DATA_DIR, "courses.json")
STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
ENROLLMENTS_FILE = os.path.join(DATA_DIR, "enrollments.json")


#файлы
def load(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


#поиск и фильтрация
def find_course(courses, course_id):
    for c in courses:
        if c["id"] == course_id:
            return c
    return None


def search_courses(courses, keyword):
    kw = keyword.lower()
    return [c for c in courses if kw in c["name"].lower() or kw in c["description"].lower()]


def filter_available(courses):
    return [c for c in courses if c["current_students"] < c["max_students"]]


#сортировка
def sort_by_name(courses):
    return sorted(courses, key=lambda c: c["name"])


def sort_by_seats(courses):
    return sorted(courses, key=lambda c: c["max_students"] - c["current_students"], reverse=True)


#бронирование
def add_enrollment(enrollments, courses, student_id, course_id):
    for e in enrollments:
        if e["student_id"] == student_id and e["course_id"] == course_id and e["status"] == "active":
            return "Студент уже записан на этот курс."

    course = find_course(courses, course_id)
    if not course:
        return "Курс не найден."
    if course["current_students"] >= course["max_students"]:
        return "На курсе нет свободных мест."

    new_id = max([e["id"] for e in enrollments], default=0) + 1
    enrollments.append({
        "id": new_id,
        "student_id": student_id,
        "course_id": course_id,
        "enrollment_date": str(date.today()),
        "status": "active"
    })
    course["current_students"] += 1
    return "Запись успешно добавлена."


def cancel_enrollment(enrollments, courses, student_id, course_id):
    for e in enrollments:
        if e["student_id"] == student_id and e["course_id"] == course_id and e["status"] == "active":
            e["status"] = "cancelled"
            course = find_course(courses, course_id)
            if course:
                course["current_students"] -= 1
            return "Запись отменена."
    return "Активная запись не найдена."


#статистика
def get_stats(courses, students, enrollments):
    active = [e for e in enrollments if e["status"] == "active"]
    counts = {}
    for e in active:
        counts[e["course_id"]] = counts.get(e["course_id"], 0) + 1
    top = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:3]

    print("СТАТИСТИКА")
    print(f"Курсов: {len(courses)} | Студентов: {len(students)} | Активных записей: {len(active)}")
    print("Топ курсов:")
    for cid, cnt in top:
        c = find_course(courses, cid)
        if c:
            print(f"  {c['name']} — {cnt}")


#вывод
def print_courses(courses, title):
    print(f"{title}")
    for c in courses:
        free = c["max_students"] - c["current_students"]
        status = "доступен" if free > 0 else "мест нет"
        print(f"  [{c['id']}] {c['name']} | {c['teacher']} | мест: {free} | {status}")



def main():
    courses = load(COURSES_FILE)
    students = load(STUDENTS_FILE)
    enrollments = load(ENROLLMENTS_FILE)

    print("СИСТЕМА УПРАВЛЕНИЯ ФАКУЛЬТАТИВАМИ")

    print_courses(courses, "Все курсы")
    print_courses(filter_available(courses), "Доступные курсы")
    print_courses(search_courses(courses, "Django"), "Поиск: Django")

    print("Сортировка по свободным местам")
    for c in sort_by_seats(courses):
        print(f"  {c['name']} — свободно: {c['max_students'] - c['current_students']}")

    print("Добавление брони")
    print(" ", add_enrollment(enrollments, courses, 1, 3))
    save(ENROLLMENTS_FILE, enrollments)
    save(COURSES_FILE, courses)

    print("Отмена брони")
    print(" ", cancel_enrollment(enrollments, courses, 1, 3))
    save(ENROLLMENTS_FILE, enrollments)
    save(COURSES_FILE, courses)

    get_stats(courses, students, enrollments)


if __name__ == "__main__":
    main()