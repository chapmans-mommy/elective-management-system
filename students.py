def find_student(students: list[dict], student_id: int) -> dict | None:

    for student in students:
        if student["id"] == student_id:
            return student
    return None
