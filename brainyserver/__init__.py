#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Main file for the brainyserver server."


import os
import stat

from flask import Flask, request, abort
from flask.ext.mongoengine import MongoEngine
from flask.ext.uploads import (UploadSet, configure_uploads,
                               patch_request_class)
from flask_debugtoolbar import DebugToolbarExtension

import brainyserver.settings_default as settings_default


# Create the Flask app, its MongDB connection, and the GnuPG home.

app = Flask(__name__)

app.config.from_object(settings_default)
app.config.from_envvar('BRAINYSERVER_SETTINGS', silent=True)
mongo = MongoEngine(app)
toolbar = DebugToolbarExtension(app)

if not os.path.exists(app.config['GPG_HOME']):
    os.makedirs(app.config['GPG_HOME'])
os.chmod(app.config['GPG_HOME'], stat.S_IRWXU)


# Continue with imports that may need the app or mongo objects

from brainyserver import views
from brainyserver.admin import admin
from brainyserver.upload import upload

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(upload, url_prefix='/upload')
