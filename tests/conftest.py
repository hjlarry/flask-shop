# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest
from webtest import TestApp

from flaskshop.app import create_app
from flaskshop.database import db as _db
from flaskshop.settings import TestConfig
from flaskshop.random_data import create_menus
from flaskshop.utils import jinja_global_varibles

from .factories import UserFactory


@pytest.fixture
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)
    jinja_global_varibles(_app)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


@pytest.fixture
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()
        for msg in create_menus():
            print(msg)

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def user(db):
    """A user for the tests."""
    user = UserFactory(password='myprecious')
    db.session.commit()
    return user
