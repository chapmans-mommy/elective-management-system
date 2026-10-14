"""Подключение к отдельной базе предметной области, без Django ORM."""

import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "electives.sqlite"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection(db_path=None):
    """Открыть подключение с именованными полями и проверкой связей."""
    conn = sqlite3.connect(DB_PATH if db_path is None else db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_schema(conn):
    """Создать таблицы и индексы из SQL-файла."""
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    conn.commit()
