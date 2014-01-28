from flask import Blueprint, abort, jsonify, g, Response, json, request

from app import db
from app.shoppinglist.models import ShoppingList, Product
from app.users.auth import needs_auth

shoppinglist_api = Blueprint('shoppinglist_api', __name__, url_prefix='/api/shoppinglists')
product_api = Blueprint('product_api', __name__, url_prefix='/api/products')


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
    return Response(json.dumps(results), mimetype='application/json')


@shoppinglist_api.route('/<int:id>/products', methods=['GET'])
@needs_auth
def get_shoppinglists_products(id):
    """ Fetch all products for a shopping list. """
    shopping_list = ShoppingList.query.get(id)
    if shopping_list is None:
        abort(404)

    results = [p.to_dict() for p in shopping_list.products]
    return Response(json.dumps(results), mimetype='application/json')


@shoppinglist_api.route('/<int:id>/products', methods=['POST', 'DELETE'])
@needs_auth
def post_shoppinglists_products(id):
    """ Fetch all products for a shopping list. """
    shopping_list = ShoppingList.query.get(id)
    if shopping_list is None:
        abort(404)

    data = json.loads(request.data)
    try:
        barcode = data['id']
    except KeyError:
        abort(422)

    product = Product.query.get(barcode)
    if product is None:
        abort(404)

    if request.method == 'POST':
        shopping_list.products.append(product)
    elif request.method == 'DELETE':
        shopping_list.products.remove(product)

    db.session.commit()

    results = [p.to_dict() for p in shopping_list.products]
    return Response(json.dumps(results), mimetype='application/json')


@product_api.route('/<int:id>', methods=['GET'])
@needs_auth
def get_product(id):
    """ Get a product by id/barcode. """
    product = Product.query.get(id)
    if product is None:
        abort(404)

    return jsonify(product.to_dict())
