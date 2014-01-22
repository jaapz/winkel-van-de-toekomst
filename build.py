import subprocess
import sys
import os

from pynt import task

_curpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_curpath)

from app import db
from app.users.models import User


@task()
def clean_db():
    """ Remove test database. """
    db_path = '/tmp/winkelvandetoekomst.db'
    if os.path.exists(db_path):
        print 'Removing database...'
        os.remove(db_path)


@task(clean_db)
def setup_db():
    """ Initiate the database. """
    db.create_all()


@task()
def fixtures():
    """ Create some database fixtures. """
    u = User.query.filter(User.username == 'admin').first()

    if not u:
        u = User(
            username='admin',
            password='test',
            email='yolo@swag.com',
        )

        db.session.add(u)


@task(setup_db)
def tests():
    """ Run ALL the tests! """
    subprocess.call(['py.test', 'tests/', '-v'])


@task()
def server():
    """ Run the development server, don't use this in production! """
    subprocess.call(['./server.py'])
