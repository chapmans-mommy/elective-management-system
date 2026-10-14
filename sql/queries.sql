-- Проверенные запросы ПР7. Маркеры name используются db/queries.py.
-- Значения передаются через ?; примеры параметров указаны в комментариях.

-- name: courses_list
-- 1. Список курсов с сортировкой по названию (SELECT, ORDER BY).
SELECT id, name, description, teacher, max_students, current_students,
       start_date, max_students - current_students AS free_seats
FROM courses
ORDER BY name, id;

-- name: students_list
-- 2. Список студентов (SELECT, ORDER BY).
SELECT id, name, group_name AS "group", email
FROM students
ORDER BY name, id;

-- name: courses_search
-- 3. Поиск по названию/описанию и минимуму свободных мест (WHERE).
-- Параметры: '%SQL%', '%SQL%', 0.
SELECT id, name, description, teacher, max_students, current_students,
       start_date, max_students - current_students AS free_seats
FROM courses
WHERE (name LIKE ? OR COALESCE(description, '') LIKE ?)
  AND max_students - current_students >= ?
ORDER BY name, id;

-- name: available_courses
-- 4. Курсы со свободными местами, начинающиеся не раньше даты (WHERE).
-- Параметры: '2026-10-01', 1. Полные курсы всегда исключаются.
SELECT id, name, description, teacher, max_students, current_students,
       start_date, max_students - current_students AS free_seats
FROM courses
WHERE start_date >= ?
  AND max_students - current_students >= ?
  AND current_students < max_students
ORDER BY start_date, name, id;

-- name: enrollments_list
-- 5. Журнал записей с именами студентов и названиями курсов (JOIN).
SELECT e.id, e.enrollment_date, e.is_cancelled,
       s.id AS student_id, s.name AS student_name,
       s.group_name, s.email, c.id AS course_id, c.name AS course_name
FROM enrollments AS e
JOIN students AS s ON s.id = e.student_id
JOIN courses AS c ON c.id = e.course_id
ORDER BY e.enrollment_date DESC, e.id DESC;

-- name: enrollment_detail
-- 6. Подробности одной записи из трёх связанных таблиц (JOIN, WHERE).
-- Параметр: 1.
SELECT e.id, e.enrollment_date, e.is_cancelled,
       s.id AS student_id, s.name AS student_name,
       s.group_name, s.email, c.id AS course_id, c.name AS course_name,
       c.teacher, c.start_date
FROM enrollments AS e
JOIN students AS s ON s.id = e.student_id
JOIN courses AS c ON c.id = e.course_id
WHERE e.id = ?;

-- name: course_totals
-- 7. Общая вместимость, занятость и свободные места (COUNT, SUM, AVG).
SELECT COUNT(*) AS course_count,
       COALESCE(SUM(max_students), 0) AS total_seats,
       COALESCE(SUM(current_students), 0) AS occupied_seats,
       COALESCE(SUM(max_students - current_students), 0) AS free_seats,
       COALESCE(ROUND(AVG(max_students), 1), 0) AS average_capacity
FROM courses;

-- name: enrollment_totals
-- 8. Количество всех, активных и отменённых записей (COUNT, SUM).
SELECT COUNT(*) AS total,
       COALESCE(SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END), 0)
           AS active,
       COALESCE(SUM(CASE WHEN is_cancelled = 1 THEN 1 ELSE 0 END), 0)
           AS cancelled
FROM enrollments;

-- name: course_statistics
-- 9. Число записей по каждому курсу, включая курсы без записей (GROUP BY).
SELECT c.id, c.name, c.max_students, c.current_students,
       c.max_students - c.current_students AS free_seats,
       COUNT(e.id) AS total_enrollments,
       SUM(CASE WHEN e.is_cancelled = 0 THEN 1 ELSE 0 END) AS active,
       SUM(CASE WHEN e.is_cancelled = 1 THEN 1 ELSE 0 END) AS cancelled
FROM courses AS c
LEFT JOIN enrollments AS e ON e.course_id = c.id
GROUP BY c.id, c.name, c.max_students, c.current_students
ORDER BY active DESC, c.name, c.id;

-- name: student_statistics
-- 10. Количество записей по студентам, включая студентов без записей.
-- GROUP BY и LEFT JOIN.
SELECT s.id, s.name, s.group_name, COUNT(e.id) AS total_enrollments,
       SUM(CASE WHEN e.is_cancelled = 0 THEN 1 ELSE 0 END) AS active,
       SUM(CASE WHEN e.is_cancelled = 1 THEN 1 ELSE 0 END) AS cancelled
FROM students AS s
LEFT JOIN enrollments AS e ON e.student_id = s.id
GROUP BY s.id, s.name, s.group_name
ORDER BY active DESC, s.name, s.id;

-- name: popular_courses
-- 11. Курсы, число активных записей на которые больше порога (HAVING).
-- Параметр: 0.
SELECT c.id, c.name, COUNT(e.id) AS active
FROM courses AS c
LEFT JOIN enrollments AS e ON e.course_id = c.id AND e.is_cancelled = 0
GROUP BY c.id, c.name
HAVING COUNT(e.id) > ?
ORDER BY active DESC, c.name, c.id;

-- name: course_detail
-- 12. Подробности курса (WHERE). Параметр: 1.
SELECT id, name, description, teacher, max_students, current_students,
       start_date, max_students - current_students AS free_seats
FROM courses
WHERE id = ?;

-- name: active_enrollments
-- 13. Только активные записи с данными студента и курса (WHERE, JOIN).
SELECT e.id, e.enrollment_date, e.is_cancelled,
       s.id AS student_id, s.name AS student_name,
       s.group_name, s.email, c.id AS course_id, c.name AS course_name
FROM enrollments AS e
JOIN students AS s ON s.id = e.student_id
JOIN courses AS c ON c.id = e.course_id
WHERE e.is_cancelled = 0
ORDER BY e.enrollment_date DESC, e.id DESC;

-- name: students_by_group
-- 14. Студенты выбранной учебной группы (WHERE).
-- Параметр: 'ЭФБО-02-24'.
SELECT id, name, group_name AS "group", email
FROM students
WHERE group_name = ?
ORDER BY name, id;

-- name: student_groups
-- 15. Существующие учебные группы для формы поиска (SELECT, DISTINCT).
SELECT DISTINCT group_name
FROM students
ORDER BY group_name;

-- name: group_statistics
-- 16. Количество студентов в каждой учебной группе (GROUP BY, COUNT).
SELECT group_name, COUNT(*) AS student_count
FROM students
GROUP BY group_name
ORDER BY group_name;
