from flask.ext.wtf import Form
from wtforms import PasswordField, TextField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(Form):
    """ Form used for the login page. """
    username = TextField('E-mailadres', validators=[DataRequired(), Email()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])


class RegisterForm(Form):
    """ Form used for registering a new user. """
    username = TextField('E-mailadres', validators=[DataRequired(), Email()])

    password = PasswordField('Wachtwoord', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])

    confirm = PasswordField('Controle Wachtwoord')
