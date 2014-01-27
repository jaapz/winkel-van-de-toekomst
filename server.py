#!/usr/bin/env python
from app import app
from werkzeug.debug import DebuggedApplication

if app.config['DEBUG'] == True:
    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

if __name__ == '__main__':
    app.run(debug=True)
