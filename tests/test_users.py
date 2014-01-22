import pytest
import hashlib

from app.users.models import User


class TestUserModel:
    @pytest.mark.parametrize('field', [
        'id',
        'username',
        'password'
    ])
    def test_fields(self, field):
        """ The User model should have these fields. """
        assert hasattr(User, field)

    def test_get_id(self, user):
        """ Should have a get_id method that returns a unicode. """
        id = user.get_id()

        assert type(id) == unicode
        assert int(id) == user.id

    def test_is_authenticated(self, user):
        """ User should have an is_authenticated method. """
        assert user.is_authenticated() is True

    def test_is_active(self, user):
        """ User should have an is_active method. """
        assert user.is_active() is True

    def test_is_anonymous(self, user):
        """ User should have an is_anonymous method. """
        assert user.is_anonymous() is False

    def test_set_password(self, user):
        """ Setting the user password should transform the password to a sha512
        hash. """
        user.password = 'test'
        assert user.password == hashlib.sha512('test').hexdigest()

    def test_to_dict(self, user):
        """ Should return a dict representation of the user model. """
        data = user.to_dict()

        assert data['id'] == user.id
        assert data['username'] == user.username
