def find_course(courses: list[dict], course_id: int) -> dict | None:

    for course in courses:
        if course["id"] == course_id:
            return course
    return None


def search_courses(courses: list[dict], keyword: str) -> list[dict]:

    keyword_lower = keyword.lower()
    return [
        course for course in courses
        if keyword_lower in course["name"].lower()
        or keyword_lower in course["description"].lower()
    ]


def filter_available(courses: list[dict]) -> list[dict]:

    return [
        course for course in courses
        if course["current_students"] < course["max_students"]
    ]


def sort_by_name(courses: list[dict]) -> list[dict]:

    return sorted(courses, key=lambda c: c["name"])


def sort_by_seats(courses: list[dict]) -> list[dict]:

    return sorted(
        courses,
        key=lambda c: c["max_students"] - c["current_students"],
        reverse=True,
    )


def print_courses(courses: list[dict], title: str) -> None:

    print(f"{title}")
    if not courses:
        print("  Курсы не найдены.")
        return
    for course in courses:
        free = course["max_students"] - course["current_students"]
        status = "доступен" if free > 0 else "мест нет"
        print(f"  [{course['id']}] {course['name']} | "
              f"{course['teacher']} | мест: {free} | {status}")
