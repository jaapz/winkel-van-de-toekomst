import hashlib
from hashlib import sha512
from uuid import uuid4

from app import db, app


class CheckoutUser():
    """ The checkout user is only used when a checkout app is doing requests.
    It has a password made of a secret hash that is configured in the app. """

    id = uuid4()
    username = 'checkout'
    name = 'Checkout User'
    password = sha512(app.config['SECRET_KEY']).hexdigest()

    def get_id(self):
        """ Get the id as a unicode, for Flask-Login. """
        return unicode(self.id)

    def is_authenticated(self):
        """ Whether or not a user is authenticated. Needed for Flask-Login"""
        return True

    def is_active(self):
        """ Whether or not a user is active. Needed for Flask-Login. """
        return True

    def is_anonymous(self):
        """ If a user is anonymous. Needed for Flask-Login """
        return False


class User(db.Model):
    """ Basic user class for simple logging in. """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(50))
    shopping_lists = db.relationship('ShoppingList')

    def get_id(self):
        """ Get the id as a unicode, for Flask-Login. """
        return unicode(self.id)

    def is_authenticated(self):
        """ Whether or not a user is authenticated. Needed for Flask-Login"""
        return True

    def is_active(self):
        """ Whether or not a user is active. Needed for Flask-Login. """
        return True

    def is_anonymous(self):
        """ If a user is anonymous. Needed for Flask-Login """
        return False

    def __setattr__(self, key, value):
        """ Override setting of password so we are always secure. """
        if key == 'password':
            value = hashlib.sha512(value).hexdigest()

        super(User, self).__setattr__(key, value)

    def to_dict(self):
        """ Return a dict representation of this user. """
        return dict(
            id=self.id,
            username=self.username
        )
