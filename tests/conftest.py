"""Раздельные тестовые базы ПР7 и Django ORM; рабочие данные не меняются."""

import os

import django
import pytest
from django.db import transaction
from django.test import Client
from django.test.utils import (
    setup_databases, setup_test_environment,
    teardown_databases, teardown_test_environment,
)

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


@pytest.fixture(scope="session")
def orm_database():
    setup_test_environment()
    config = setup_databases(verbosity=0, interactive=False)
    yield
    teardown_databases(config, verbosity=0)
    teardown_test_environment()


@pytest.fixture
def orm_db(orm_database):
    with transaction.atomic():
        yield
        transaction.set_rollback(True)


@pytest.fixture
def client(database_path, orm_db):
    from db.import_sqlite_to_orm import import_data as import_to_orm
    import_to_orm(database_path)
    return Client(SERVER_NAME="localhost")
