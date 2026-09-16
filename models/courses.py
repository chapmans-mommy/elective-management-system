"""Класс Course и функции работы с курсами."""

from typing import List, Optional


class Course:
    """Факультативный курс."""

    def __init__(
        self,
        course_id: int,
        name: str,
        description: str,
        teacher: str,
        max_students: int,
        current_students: int = 0,
        start_date: str = "",
    ) -> None:
        """Создать объект курса."""
        self.id = course_id
        self.name = name
        self.description = description
        self.teacher = teacher
        self.max_students = max_students
        self.current_students = current_students
        self.start_date = start_date

    def has_free_seats(self) -> bool:
        """Проверить, есть ли свободные места на курсе."""
        return self.current_students < self.max_students

    def free_seats(self) -> int:
        """Вернуть количество свободных мест."""
        return self.max_students - self.current_students

    @classmethod
    def from_data(cls, data: dict) -> "Course":
        """Создать курс из словаря (данные JSON)."""
        return cls(
            course_id=data["id"],
            name=data["name"],
            description=data["description"],
            teacher=data["teacher"],
            max_students=data["max_students"],
            current_students=data["current_students"],
            start_date=data["start_date"],
        )

    def to_data(self) -> dict:
        """Преобразовать объект в словарь (для сохранения в JSON)."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "teacher": self.teacher,
            "max_students": self.max_students,
            "current_students": self.current_students,
            "start_date": self.start_date,
        }

    def __str__(self) -> str:
        """Строковое представление курса."""
        return (
            f"[{self.id}] {self.name} | {self.teacher} | "
            f"мест: {self.free_seats()}"
        )


# ============ Функции работы с коллекцией Course ============

def find_course(courses: List[Course], course_id: int) -> Optional[Course]:
    """Найти курс по идентификатору."""
    for course in courses:
        if course.id == course_id:
            return course
    return None


def search_courses(courses: List[Course], keyword: str) -> List[Course]:
    """Найти курсы по ключевому слову в названии или описании."""
    kw = keyword.lower()
    return [
        c for c in courses
        if kw in c.name.lower() or kw in c.description.lower()
    ]


def filter_available(courses: List[Course]) -> List[Course]:
    """Отобрать курсы со свободными местами."""
    return [c for c in courses if c.has_free_seats()]


def sort_by_name(courses: List[Course]) -> List[Course]:
    """Отсортировать курсы по названию."""
    return sorted(courses, key=lambda c: c.name)


def sort_by_seats(courses: List[Course]) -> List[Course]:
    """Отсортировать курсы по свободным местам (по убыванию)."""
    return sorted(courses, key=lambda c: c.free_seats(), reverse=True)


def print_courses(courses: List[Course], title: str) -> None:
    """Вывести список курсов."""
    print(f"\n=== {title} ===")
    if not courses:
        print("  Курсы не найдены.")
        return
    for course in courses:
        print(f"  {course}")
