-- Система управления факультативами: схема ПР7.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    teacher TEXT NOT NULL,
    max_students INTEGER NOT NULL CHECK (max_students > 0),
    current_students INTEGER NOT NULL DEFAULT 0
        CHECK (current_students BETWEEN 0 AND max_students),
    start_date TEXT
);

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    group_name TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrollment_date TEXT NOT NULL,
    is_cancelled INTEGER NOT NULL DEFAULT 0 CHECK (is_cancelled IN (0, 1)),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE INDEX IF NOT EXISTS idx_enrollments_student
    ON enrollments(student_id);
CREATE INDEX IF NOT EXISTS idx_enrollments_course
    ON enrollments(course_id);
CREATE INDEX IF NOT EXISTS idx_courses_start_date
    ON courses(start_date);
