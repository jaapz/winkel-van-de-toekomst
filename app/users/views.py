from flask import Blueprint, render_template, flash, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required

from app.utils import sha512_string
from app.users.forms import LoginForm
from app.users.models import User

users_views = Blueprint('user_views', __name__, url_prefix='/users')


@users_views.route('/login', methods=['GET', 'POST'])
def login():
    errors = False

    form = LoginForm()
    if form.validate_on_submit():
        # Check username first.
        user = User.query.filter(User.username == form.username.data).first()
        if user is None:
            errors = True

        # Check password.
        password = form.password.data or ''
        hashed_password = unicode(sha512_string(password))
        if hashed_password != getattr(user, 'password', ''):
            errors = True

        # If correct credentials, login and redirect to home.
        if not errors:
            if login_user(user):
                flash('U bent ingelogd.')
                return redirect(url_for('home'))
            else:
                errors = True

    return render_template('users/login.html', form=form, errors=errors)


@users_views.route('/logout')
@login_required
def logout():
    logout_user()
    flash('U bent uitgelogd.')
    return redirect(url_for('user_views.login'))
