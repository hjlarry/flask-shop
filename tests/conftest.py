# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""
from pathlib import Path

import pytest

from flaskshop.app import create_app
from flaskshop.database import db as _db
from flaskshop.random_data import create_menus, create_products_by_schema
from flaskshop.utils import jinja_global_varibles


@pytest.fixture
def app():
    """An application for the tests."""
    _app = create_app("tests.settings")
    jinja_global_varibles(_app)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

        create_menus()
        create_products_by_schema(
            placeholder_dir=Path("placeholders"), how_many=1, create_images=False
        )

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()
