#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Main file for the brainyserver server."


from flask import Flask, request, abort, session, g
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


# Configure pre/post requests
import brainyserver.mongodb as mongodb
@app.before_request
def before_request():
    g.db = mongodb
    g.username = session.get('username')
    if g.username != None:
        g.logged_in = True
        g.user = mongodb.Researcher.objects(username=g.username).first()
    else:
        g.logged_in = False
        g.user = None
        g.username = ''


# Continue with imports that may need the app or mongo objects

from brainyserver import views
from brainyserver.admin import admin
from brainyserver.upload import upload
from brainyserver.user import user

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(upload, url_prefix='/upload')
app.register_blueprint(user, url_prefix='/<username>')


if __name__ == '__main__':
    app.run()
