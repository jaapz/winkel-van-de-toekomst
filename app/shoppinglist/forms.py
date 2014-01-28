from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired


class ShoppingListForm(Form):
    """ Creates and edits a shopping list. """
    name = TextField('Naam', validators=[DataRequired()])
