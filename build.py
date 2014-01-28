import subprocess
import sys
import os

from pynt import task

_curpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_curpath)

from app import db
from app.users.models import User
from app.shoppinglist.models import Product, ShoppingList, ShoppingListToProduct


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
            username='admin@hanze.nl',
            password='test'
        )

        db.session.add(u)

    s = ShoppingList(user=u, name='Mijn Lijstje')

    b = Product(
        name='Blik Bier',
        id=1902901902901902,
        price=150
    )

    ba = ShoppingListToProduct(
        product=b,
        shopping_list=s,
        amount=3,
        amount_scanned=2
    )

    h = Product(
        name='Hagelslag',
        id=9090191919348524,
        price=100
    )

    ha = ShoppingListToProduct(
        product=h,
        shopping_list=s,
        amount=2,
        amount_scanned=2
    )

    p = Product(
        name='Sportlife',
        id=8711400406133,
        price=15
    )

    pa = ShoppingListToProduct(
        product=p,
        shopping_list=s,
        amount=1,
        amount_scanned=2
    )

    s.products.append(ba)
    s.products.append(ha)
    s.products.append(pa)

    db.session.add(s)
    db.session.commit()


@task(setup_db)
def tests():
    """ Run ALL the tests! """
    subprocess.call(['py.test', 'tests/', '-v'])


@task()
def server():
    """ Run the development server, don't use this in production! """
    subprocess.call(['./server.py'])
