
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


is_seats_available = current_students < max_students
is_registration_open = True  


if is_seats_available and is_registration_open:
    registration_status = "Вы можете записаться на данный факультатив."
elif not is_seats_available:
    registration_status = "Извините, на курс уже закончились места."
else:
    registration_status = "Регистрация на курс закрыта."


print(f"Система управления факультативами")
print(f"Студент: {student_name} ({student_group})")
print(f"Курс: {course_name}")
print(f"Преподаватель: {course_teacher}")
print(f"Дата начала: {course_start_date}")
print(f"Свободных мест: {max_students - current_students}")
print(f"Статус: {registration_status}")


print("\nПроверка условий записи")
can_apply = True


if student_group != "ЭФБО-02-24":
    print("Предупреждение: Данный курс ориентирован на группу ЭФБО-02-24")
    can_apply = False


if not is_seats_available:
    print("Мест нет")
    can_apply = False


if can_apply:
    print("Итог: Вы можете подать заявку на этот факультатив.")
else:
    print("Итог: Заявка на этот факультатив недоступна.")