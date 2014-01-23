from flask import Blueprint, abort, jsonify

from app.shoppinglist.models import ShoppingList
from app.users.auth import needs_auth

shoppinglist_api = Blueprint('shoppinglist_api', __name__, url_prefix='/api/shoppinglists')


@shoppinglist_api.route('/<int:id>')
@needs_auth
def get_shoppinglist_by_id(id):
    """ Fetch a shoppinglist by id, return json if found, else 404. """
    shop_list = ShoppingList.query.get(id)
    if not shop_list:
        return abort(404)

    return jsonify(shop_list.to_dict())
