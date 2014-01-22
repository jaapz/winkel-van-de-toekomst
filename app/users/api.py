from flask import Blueprint, abort, jsonify

from app.users.models import User
from app.users.auth import needs_auth

users_api = Blueprint('users_api', __name__, url_prefix='/api/users')


@users_api.route('/<string:name>')
@needs_auth
def get_user_by_name(name):
    """ Fetch a user by name. Return json if found, 404 if not. """
    user = User.query.filter(User.username == name).first()
    if not user:
        return abort(404)

    return jsonify(user.to_dict())
