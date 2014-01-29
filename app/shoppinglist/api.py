from flask import Blueprint, abort, jsonify, g, Response, json, request
from sqlalchemy import and_
from functools import wraps

from app import db
from app.shoppinglist.models import (ShoppingList, Product,
                                     ShoppingListToProduct)
from app.users.auth import needs_auth
from app.users.models import CheckoutUser

shoppinglist_api = Blueprint('shoppinglist_api', __name__,
                             url_prefix='/api/shoppinglists')

product_api = Blueprint('product_api', __name__, url_prefix='/api/products')


def get_shoppinglist(func):
    """ Decorator to inject the requested shopping list object if found. """
    @wraps(func)
    def wrapper(*args, **kwargs):
        shoppinglist = ShoppingList.query.get(kwargs['id'])
        if shoppinglist is None:
            abort(404)

        if g.current_user.id != CheckoutUser.id and\
           shoppinglist.user.id != g.current_user.id:
            abort(404)

        kwargs['shoppinglist'] = shoppinglist
        return func(*args, **kwargs)
    return wrapper


@shoppinglist_api.route('/<int:id>')
@needs_auth
@get_shoppinglist
def get_shoppinglist_by_id(id, shoppinglist):
    """ Fetch a shoppinglist by id, return json if found, else 404. """
    return jsonify(shoppinglist.to_dict())


@shoppinglist_api.route('/<int:id>', methods=['PUT'])
@needs_auth
@get_shoppinglist
def update_shoppinglist(id, shoppinglist):
    """ Update a shoppinglist, return the updated json if found, else 404. """
    try:
        data = json.loads(request.data)
    except:
        abort(422)

    name = data.get('name') or None
    status = data.get('status') or None

    shoppinglist.name = name if name is not None else shoppinglist.name
    shoppinglist.status = status if status is not None else shoppinglist.status

    db.session.commit()

    return jsonify(shoppinglist.to_dict())


@shoppinglist_api.route('')
@needs_auth
def get_shoppinglists():
    """ Fetch all shopping lists the current user can see. """
    results = [l.to_dict() for l in g.current_user.shopping_lists]
    return Response(json.dumps(results), mimetype='application/json')


@shoppinglist_api.route('/<int:id>/products', methods=['GET'])
@needs_auth
@get_shoppinglist
def get_shoppinglists_products(id, shoppinglist):
    """ Fetch all products for a shopping list. """
    results = [p.product.to_dict(shoppinglist) for p in shoppinglist.products]
    return Response(json.dumps(results), mimetype='application/json')


@shoppinglist_api.route('/<int:id>/products', methods=['POST', 'PUT'])
@needs_auth
@get_shoppinglist
def post_shoppinglists_product(id, shoppinglist):
    """ Fetch all products for a shopping list. """
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

    assoc = product.get_shopping_list_assocation(shoppinglist)

    # If we are POSTing we expect to not have a association yet, so we create
    # a new one.
    if request.method == 'POST':
        if assoc is None:
            assoc = ShoppingListToProduct(
                product=product,
                shopping_list=shoppinglist,
                amount=amount if amount is not None else 0,
                amount_scanned=amount_scanned if amount_scanned is not None else 1
            )

            shoppinglist.products.append(assoc)
        else:
            # Heighten the amount_scanned automatically if we already have the
            # product in our list.
            assoc.amount_scanned += 1

    # If we are PUTting, we do already have an association so we update it.
    elif request.method == 'PUT':
        if assoc is not None:
            # Update the amounts only when we have a non-None value for each.
            assoc.amount = amount if amount is not None else assoc.amount
            assoc.amount_scanned = amount_scanned if amount_scanned is not None else assoc.amount_scanned

    db.session.commit()

    results = [p.product.to_dict(shoppinglist) for p in shoppinglist.products]
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
