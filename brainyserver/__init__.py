#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Main file for the brainyserver server."


from flask import Flask, request, abort
from flask.ext.mongoengine import MongoEngine
from flask.ext.uploads import (UploadSet, configure_uploads,
                               patch_request_class)
from flask_debugtoolbar import DebugToolbarExtension

import brainyserver.settings as settings


# Create the Flask app, its MongDB connection, and the GnuPG home.

app = Flask(__name__)

app.config.from_object(settings)
mongo = MongoEngine(app)
toolbar = DebugToolbarExtension(app)


# Continue with imports that may need the app or mongo objects

from brainyserver import views
from brainyserver.admin import admin
from brainyserver.upload import upload

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(upload, url_prefix='/upload')


if __name__ == '__main__':
    app.run()
