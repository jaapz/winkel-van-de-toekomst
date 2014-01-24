import subprocess
import sys
import os

from pynt import task

_curpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_curpath)

from app import db
from app.users.models import User
from app.shoppinglist.models import Product, ShoppingList


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


@task(setup_db)
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

    b = Product(
        name='Blik Bier',
        barcode='1902901902901902',
        price=15.0
    )

    h = Product(
        name='Hagelslag',
        barcode='9090191919348524',
        price=10.0
    )

    s = ShoppingList(user=u, name='Mijn Lijstje')
    s.products.append(b)
    s.products.append(h)

    db.session.add(s)
    db.session.add(b)
    db.session.add(h)
    db.session.commit()


@task(setup_db)
def tests():
    """ Run ALL the tests! """
    subprocess.call(['py.test', 'tests/', '-v'])


@task()
def server():
    """ Run the development server, don't use this in production! """
    subprocess.call(['./server.py'])
