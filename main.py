from datetime import date

student_name = "Иванова Валерия Денисовна"
student_group = "ЭФБО-02-24"
student_email = "ivanova.v.d@edu.mirea.ru"

course_name = "Введение в искусственный интеллект"
course_description = "Базовые понятия ИИ и машинного обучения"
course_teacher = "старший преподаватель Макиевский С.Е."
max_students = 30
current_students = 28
course_start_date = date(2026, 10, 1)


def check_seats_available(current, max_capacity):
    return current < max_capacity


def check_group_match(student_group, target_group="ЭФБО-02-24"):
    return student_group == target_group


def get_registration_status(seats_available, registration_open):
    if seats_available and registration_open:
        return "Вы можете записаться на данный факультатив."
    elif not seats_available:
        return "Извините, на курс уже закончились места."
    else:
        return "Регистрация на курс закрыта."


def check_application_eligibility(student_group, seats_available, target_group="ЭФБО-02-24"):
    can_apply = True
    warnings = []
    
    if student_group != target_group:
        warnings.append("Данный курс ориентирован на группу ЭФБО-02-24")
        can_apply = False
    
    if not seats_available:
        warnings.append("Мест нет")
        can_apply = False
    
    return can_apply, warnings


is_seats_available = check_seats_available(current_students, max_students)
is_registration_open = True

registration_status = get_registration_status(is_seats_available, is_registration_open)

print(f"Система управления факультативами")
print(f"Студент: {student_name} ({student_group})")
print(f"Курс: {course_name}")
print(f"Преподаватель: {course_teacher}")
print(f"Дата начала: {course_start_date}")
print(f"Свободных мест: {max_students - current_students}")
print(f"Статус: {registration_status}")

print("\nПроверка условий записи")
can_apply, warnings = check_application_eligibility(student_group, is_seats_available)

for warning in warnings:
    print(warning)

if can_apply:
    print("Итог: Вы можете подать заявку на этот факультатив.")
else:
    print("Итог: Заявка на этот факультатив недоступна.")