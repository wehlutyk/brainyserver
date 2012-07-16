#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main file for the brainyserver server."""


from flask import Flask, request, abort, session, g
from flask.ext.mongoengine import MongoEngine
from flask.ext.uploads import (UploadSet, configure_uploads,
                               patch_request_class)
from flask_debugtoolbar import DebugToolbarExtension


mode_to_config = {'testing': 'config/settings_testing.py',
                  'debug': 'config/settings_debug.py',
                  'prod': 'config/settings_prod.py'}


# Create the Flask app, its MongDB connection, and the debugging toolbar.

def create_app(mode=None, config_filename='config/settings_prod.py'):
    if mode:
        config_filename = mode_to_config[mode]
    
    app = Flask(__name__)
    
    app.config.from_pyfile(config_filename)
    DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['DEBUG_TB_PANELS'] = \
                                'flask.ext.mongoengine.panels.MongoDebugPanel'
    MongoEngine(app)
    
    
    # Import the database classes.
    
    import brainyserver.mongodb as mongodb
    
    
    # Continue with imports that may need the app object.
    
    from brainyserver import views
    from brainyserver.views import configure_frontend_app
    configure_frontend_app(app)
    
    from brainyserver.upload import upload, configure_upload_blueprint
    configure_upload_blueprint(app)
    app.register_blueprint(upload, url_prefix='/upload')
    
    from brainyserver.user import user
    app.register_blueprint(user, url_prefix='/<username>')
    
    return app


# Run if we're the main script.

if __name__ == '__main__':
    app = create_app()
    app.run()
