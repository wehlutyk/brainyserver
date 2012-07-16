#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main file for the brainyserver server."""


from flask import Flask, request, abort, session, g
from flask.ext.mongoengine import MongoEngine
from flask.ext.uploads import (UploadSet, configure_uploads,
                               patch_request_class)
from flask_debugtoolbar import DebugToolbarExtension

import brainyserver.settings as settings


# Create the Flask app, its MongDB connection, and the debugging toolbar.

app = Flask(__name__)

app.config.from_object(settings)
mongo = MongoEngine(app)
toolbar = DebugToolbarExtension(app)


# Import the database classes.

import brainyserver.mongodb as mongodb


# Continue with imports that may need the app or mongo objects.

from brainyserver import views
from brainyserver.upload import upload
from brainyserver.user import user

app.register_blueprint(upload, url_prefix='/upload')
app.register_blueprint(user, url_prefix='/<username>')


# Run if we're the main script.

if __name__ == '__main__':
    app.run()
