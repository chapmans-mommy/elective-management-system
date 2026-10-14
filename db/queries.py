"""Единый источник SQL-запросов для представлений и проверки в CLI."""

import re
from functools import lru_cache

from db.database import BASE_DIR


@lru_cache(maxsize=1)
def load_queries():
    text = (BASE_DIR / "sql" / "queries.sql").read_text(encoding="utf-8")
    parts = re.split(r"^-- name: (\w+)\s*$", text, flags=re.MULTILINE)
    return dict(zip(parts[1::2], parts[2::2]))


def get_query(name):
    return load_queries()[name]
