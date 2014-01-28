from flask import Blueprint, render_template, redirect, url_for, abort
from flask.ext.login import login_required, current_user

from app import db
from app.shoppinglist.models import ShoppingList
from app.shoppinglist.forms import ShoppingListForm

shoppinglists_views = Blueprint('shoppinglists_views', __name__,
                                url_prefix='/shoppinglists')


@shoppinglists_views.route('/', methods=['GET', 'POST'])
@login_required
def overview():
    """ Shows a list of all shoppinglists for the current user. """
    create_list_form = ShoppingListForm()
    if create_list_form.validate_on_submit():
        my_list = ShoppingList(
            name=create_list_form.name.data,
            user=current_user
        )

        db.session.add(my_list)
        db.session.commit()

    return render_template('shoppinglists/list.html',
                           create_list_form=ShoppingListForm())


@shoppinglists_views.route('/remove/<int:id>', methods=['GET'])
@login_required
def remove(id):
    """ Removes a shoppinglist. """
    my_list = ShoppingList.query.get(id)
    if my_list is None:
        abort(404)

    if my_list.user.id != current_user.id:
        abort(404)

    db.session.delete(my_list)
    db.session.commit()

    return redirect(url_for('shoppinglists_views.overview'))