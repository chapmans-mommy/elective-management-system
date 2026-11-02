"""Инспекция исходной базы ПР7: только чтение."""

import sqlite3
from contextlib import closing
from pathlib import Path


SOURCE_DB = Path(__file__).resolve().parent.parent / \
    "data" / "electives.sqlite"


def main():
    if not SOURCE_DB.is_file():
        raise FileNotFoundError(SOURCE_DB)
    with closing(sqlite3.connect(
        SOURCE_DB.as_uri() + "?mode=ro", uri=True,
    )) as connection:
        for table in ("courses", "students", "enrollments"):
            print(f"\nТаблица: {table}")
            for column in connection.execute(f'PRAGMA table_info("{table}")'):
                print(column)
            count = connection.execute(
                f'SELECT COUNT(*) FROM "{table}"',
            ).fetchone()[0]
            print(f"Количество записей: {count}")
        print("Проверка связей:", connection.execute(
            "PRAGMA foreign_key_check",
        ).fetchall())


if __name__ == "__main__":
    main()
