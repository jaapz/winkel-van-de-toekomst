from flask.ext.wtf import Form
from wtforms import PasswordField, TextField
from wtforms.validators import DataRequired

class LoginForm(Form):
    """ Form used for the login page. """
    username = TextField('Gebruikersnaam', validators=[DataRequired()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
