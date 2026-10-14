"""Изолированная SQLite-база для проверки импорта и веб-страниц."""

import os

import django
import pytest
from django.test import Client

from db import database
from db.import_json import import_data

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elective_system.settings")
django.setup()


@pytest.fixture
def database_path(tmp_path, monkeypatch):
    path = tmp_path / "electives.sqlite"
    monkeypatch.setattr(database, "DB_PATH", path)
    import_data()
    return path


@pytest.fixture
def client(database_path):
    return Client(SERVER_NAME="localhost")
