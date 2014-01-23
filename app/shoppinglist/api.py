from flask import Blueprint, abort, jsonify, g, Response, json

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

    if shop_list.user is not g.current_user:
        return abort(404)

    return jsonify(shop_list.to_dict())


@shoppinglist_api.route('')
@needs_auth
def get_shoppinglists():
    """ Fetch all shopping lists the current user can see. """
    results = [l.to_dict() for l in g.current_user.shopping_lists]
    return Response(json.dumps(results),  mimetype='application/json')
