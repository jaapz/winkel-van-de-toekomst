from flask import Response
from uuid import uuid4
from hashlib import sha512


def json_response(data, status=200, mimetype='application/json'):
    """ Returns a Response object with a json mimetype. """
    return Response(
        data,
        mimetype=mimetype,
        status=status
    )


def semirandom_string(len=10):
    """ Return a semirandom string, using uuid. """
    return str(uuid4().int)[:len]


def sha512_string(text):
    """ Return the string representation of a sha512 hash for a text. """
    return sha512(text).hexdigest()
