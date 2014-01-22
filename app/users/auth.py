from flask import request, Response, g

from functools import wraps

from app import db
from app.users.models import User


def _auth_error(msg='Please log in with correct credentials'):
    """ Show authentication message to api. """
    return Response(
        msg,
        401,
        {'WWW-Authenticate': 'Basic realm="%s"' % msg}
    )


def needs_auth(func):
    """ Authenticate a user using HTTP Basic Auth. """
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        user = User.query.filter(
            User.username == getattr(auth, 'username', '')
        ).first()

        # If no user at all, 401.
        if not user:
            return _auth_error(msg='User does not exist')

        # If user wrong password, 401 and save tries.
        if user.password != getattr(auth, 'password', ''):
            return _auth_error(msg='Password incorrect')

        # Save the user to the thread global for later use.
        g.current_user = user

        db.session.commit()

        return func(*args, **kwargs)
    return wrapper
