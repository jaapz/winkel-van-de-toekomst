import pytest
import os

from random import randint
from base64 import b64encode
from datetime import datetime

from app import app as testable_app
from app import db as testable_db

from app.users.models import User


@pytest.fixture
def app():
    """ The flask app. """
    return testable_app


@pytest.fixture
def db():
    """ The database object. """
    return testable_db


@pytest.fixture
def client(app):
    """ A test client.

    Example usage:

        def test_some_endpoint(client):
            with client as c:
                rv = c.get('/api/test', follow_redirects=True)
                assert rv.status_code == 200

    """
    return app.test_client()


@pytest.fixture
def user(db):
    """ User object. """
    u = User(
        username=u'%d@broekhuizen.nu' % User.query.count(),
        password='testpass'
    )

    u2 = User(
        username=u'anders%d@broekhuizen.nu' % User.query.count(),
        password='testpass'
    )

    db.session.add(u)
    db.session.add(u2)
    db.session.commit()

    return u


@pytest.fixture
def user_auth_headers(user):
    """ Authentication headers for the normal user. """
    auth_string = b64encode('%s:%s' % (user.username, user.password))
    return [('Authorization', 'Basic %s' % auth_string)]
