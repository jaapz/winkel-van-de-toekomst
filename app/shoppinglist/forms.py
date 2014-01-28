from flask.ext.wtf import Form
from wtforms import TextField, DecimalField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app.shoppinglist.models import Product


class ShoppingListForm(Form):
    """ Creates and edits a shopping list. """
    name = TextField('Naam', validators=[DataRequired()])


def products_query_factory():
    """ Return all products for use in a form. """
    return Product.query.all()


class ProductForm(Form):
    """ Adds a produt to a shopping list. """
    amount = DecimalField('Hoeveelheid', validators=[DataRequired()])
    product = QuerySelectField('Product', query_factory=products_query_factory,
                               get_label='name', allow_blank=False)
