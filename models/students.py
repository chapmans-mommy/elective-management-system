"""Класс Student и функции работы со студентами."""

from typing import List, Optional


class Student:
    """Студент, записывающийся на факультативы."""

    def __init__(
        self,
        student_id: int,
        name: str,
        group: str,
        email: str,
    ) -> None:
        """Создать объект студента."""
        self.id = student_id
        self.name = name
        self.group = group
        self.email = email

    @classmethod
    def from_data(cls, data: dict) -> "Student":
        """Создать студента из словаря."""
        return cls(
            student_id=data["id"],
            name=data["name"],
            group=data["group"],
            email=data["email"],
        )

    def to_data(self) -> dict:
        """Преобразовать в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "group": self.group,
            "email": self.email,
        }

    def __str__(self) -> str:
        """Строковое представление студента."""
        return f"[{self.id}] {self.name} ({self.group}) — {self.email}"


def find_student(students: List[Student],
                 student_id: int) -> Optional[Student]:
    """Найти студента по идентификатору."""
    for student in students:
        if student.id == student_id:
            return student
    return None


def print_students(students: List[Student], title: str) -> None:
    """Вывести список студентов."""
    print(f"\n=== {title} ===")
    for student in students:
        print(f"  {student}")
