from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_required

from app import config

app = Flask(__name__)
app.config.from_object(config)

# Set up database, you can now get the database in other files by importing it
# like this: from app import db
db = SQLAlchemy(app)

# Set up loginmanager, which will manage users that can login.
lm = LoginManager()
lm.init_app(app)
#lm.login_view = 'users_views.login'


@lm.user_loader
def _load_user(id):
    """ Gets the user for an id, only for use by the LoginManager. """
    from app.users.models import User
    return User.query.get(id)


# Register blueprints.
from app.users.api import users_api
app.register_blueprint(users_api)


@app.route('/')
@login_required
def home():
    return 'Welkom'
