from flask import Blueprint, abort, jsonify, g, Response, json, request
from sqlalchemy import and_

from app import db
from app.shoppinglist.models import ShoppingList, Product, ShoppingListToProduct
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

    results = [p.product.to_dict(shopping_list) for p in shopping_list.products]
    return Response(json.dumps(results), mimetype='application/json')


@shoppinglist_api.route('/<int:id>/products', methods=['POST', 'PUT'])
@needs_auth
def post_shoppinglists_product(id):
    """ Fetch all products for a shopping list. """
    shopping_list = ShoppingList.query.get(id)
    if shopping_list is None:
        abort(404)

    # If no ID is given, we cannot do anything.
    data = json.loads(request.data)
    try:
        barcode = data['id']
    except KeyError:
        abort(422)

    # Get the extra values we could post.
    amount = data.get('amount', None)
    amount_scanned = data.get('amount_scanned', None)

    product = Product.query.get(barcode)
    if product is None:
        abort(404)

    assoc = product.get_shopping_list_assocation(shopping_list)

    # If we are POSTing we expect to not have a association yet, so we create
    # a new one.
    if request.method == 'POST':
        if assoc is None:
            assoc = ShoppingListToProduct(
                product=product,
                shopping_list=shopping_list,
                amount=amount,
                amount_scanned=amount_scanned
            )

            shopping_list.products.append(assoc)

    # If we are PUTting, we do already have an association so we update it.
    elif request.method == 'PUT':
        if assoc is not None:
            # Update the amounts only when we have a non-None value for each.
            assoc.amount = amount if amount is not None else assoc.amount
            assoc.amount_scanned = amount_scanned if amount_scanned is not None else assoc.amount_scanned

    db.session.commit()

    results = [p.product.to_dict(shopping_list) for p in shopping_list.products]
    return Response(json.dumps(results), mimetype='application/json')


@shoppinglist_api.route('/<int:id>/products/<int:product_id>', methods=['DELETE'])
@needs_auth
def delete_product_from_shopping_list(id, product_id):
    """ Removes a product from the shopping list. """
    assoc = ShoppingListToProduct.query.filter(and_(
        ShoppingListToProduct.product_id == product_id,
        ShoppingListToProduct.shopping_list_id == id
    )).first()

    if assoc is None:
        abort(404)

    db.session.delete(assoc)
    db.session.commit()

    return Response(), 204


@product_api.route('/<int:id>', methods=['GET'])
@needs_auth
def get_product(id):
    """ Get a product by id/barcode. """
    product = Product.query.get(id)
    if product is None:
        abort(404)

    return jsonify(product.to_dict())
