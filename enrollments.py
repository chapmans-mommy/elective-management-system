from datetime import date
from courses import find_course


def is_student_enrolled(enrollments: list[dict],
                        student_id: int,
                        course_id: int) -> bool:
    for enrollment in enrollments:
        if (enrollment["student_id"] == student_id
                and enrollment["course_id"] == course_id
                and enrollment["status"] == "active"):
            return True
    return False


def add_enrollment(enrollments: list[dict],
                   courses: list[dict],
                   student_id: int,
                   course_id: int) -> str:

    if is_student_enrolled(enrollments, student_id, course_id):
        return "Студент уже записан на этот курс."
    course = find_course(courses, course_id)
    if course is None:
        return "Курс не найден."

    if course["current_students"] >= course["max_students"]:
        return "На курсе нет свободных мест."

    new_id = max([e["id"] for e in enrollments], default=0) + 1
    enrollments.append({
        "id": new_id,
        "student_id": student_id,
        "course_id": course_id,
        "enrollment_date": str(date.today()),
        "status": "active",
    })
    course["current_students"] += 1
    return "Запись успешно добавлена."


def cancel_enrollment(enrollments: list[dict],
                      courses: list[dict],
                      student_id: int,
                      course_id: int) -> str:

    for enrollment in enrollments:
        if (enrollment["student_id"] == student_id
                and enrollment["course_id"] == course_id
                and enrollment["status"] == "active"):
            enrollment["status"] = "cancelled"
            course = find_course(courses, course_id)
            if course is not None:
                course["current_students"] -= 1
            return "Запись отменена."
    return "Активная запись не найдена."
