"""Класс Enrollment и функции работы с записями на курсы."""

from datetime import date
from typing import List, Optional

from .courses import Course, find_course
from .students import Student


class Enrollment:
    """Запись студента на факультативный курс."""

    def __init__(
        self,
        enrollment_id: int,
        student: Student,
        course: Course,
        enrollment_date: str,
        is_cancelled: bool = False,
    ) -> None:
        """Создать объект записи."""
        self.id = enrollment_id
        self.student = student
        self.course = course
        self.enrollment_date = enrollment_date
        self.is_cancelled = is_cancelled

    def cancel(self) -> None:
        """Отменить запись."""
        self.is_cancelled = True

    def is_active(self) -> bool:
        """Проверить, активна ли запись."""
        return not self.is_cancelled

    @classmethod
    def from_data(
        cls,
        data: dict,
        students: List[Student],
        courses: List[Course],
    ) -> Optional["Enrollment"]:
        """Создать запись из данных JSON, восстановив связи."""
        student = next(
            (s for s in students if s.id == data["student_id"]), None
        )
        course = find_course(courses, data["course_id"])
        if student is None or course is None:
            return None
        return cls(
            enrollment_id=data["id"],
            student=student,
            course=course,
            enrollment_date=data["enrollment_date"],
            is_cancelled=data.get("is_cancelled", False),
        )

    def to_data(self) -> dict:
        """Преобразовать в словарь для JSON (используем id связей)."""
        return {
            "id": self.id,
            "student_id": self.student.id,
            "course_id": self.course.id,
            "enrollment_date": self.enrollment_date,
            "is_cancelled": self.is_cancelled,
        }

    def __str__(self) -> str:
        """Строковое представление записи."""
        status = "отменена" if self.is_cancelled else "активна"
        return (
            f"[{self.id}] {self.student.name} → {self.course.name} "
            f"({self.enrollment_date}) — {status}"
        )


# ============ Функции работы с коллекцией Enrollment ============

def is_student_enrolled(
    enrollments: List[Enrollment],
    student_id: int,
    course_id: int,
) -> bool:
    """Проверить, записан ли студент на курс (активная запись)."""
    for e in enrollments:
        if (e.student.id == student_id
                and e.course.id == course_id
                and e.is_active()):
            return True
    return False


def add_enrollment(
    enrollments: List[Enrollment],
    student: Student,
    course: Course,
) -> str:
    """Добавить запись студента на курс."""
    if is_student_enrolled(enrollments, student.id, course.id):
        return "Студент уже записан на этот курс."
    if not course.has_free_seats():
        return "На курсе нет свободных мест."

    new_id = max((e.id for e in enrollments), default=0) + 1
    enrollment = Enrollment(
        enrollment_id=new_id,
        student=student,
        course=course,
        enrollment_date=str(date.today()),
    )
    enrollments.append(enrollment)
    course.current_students += 1
    return "Запись успешно добавлена."


def cancel_enrollment(
    enrollments: List[Enrollment],
    student_id: int,
    course_id: int,
) -> str:
    """Отменить запись студента на курс."""
    for e in enrollments:
        if (e.student.id == student_id
                and e.course.id == course_id
                and e.is_active()):
            e.cancel()
            e.course.current_students -= 1
            return "Запись отменена."
    return "Активная запись не найдена."


def print_enrollments(
    enrollments: List[Enrollment], title: str
) -> None:
    """Вывести список записей."""
    print(f"\n=== {title} ===")
    if not enrollments:
        print("  Записей нет.")
        return
    for e in enrollments:
        print(f"  {e}")

def find_enrollment_by_id(
    enrollments: List[Enrollment], enrollment_id: int
) -> Optional[Enrollment]:
    """Найти запись по идентификатору.

    Args:
        enrollments: список записей.
        enrollment_id: идентификатор записи.

    Returns:
        Объект Enrollment или None.
    """
    for e in enrollments:
        if e.id == enrollment_id:
            return e
    return None