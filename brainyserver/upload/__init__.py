#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Upload blueprint."""


import os

from flask import Blueprint
from flask.ext.uploads import (UploadSet, configure_uploads,
                               patch_request_class)


upload = Blueprint('upload', __name__)


# Configure upload sets

dest=lambda app: os.path.join(app.root_path, 'uploads')

us_eadata = UploadSet('eadata', 'json', default_dest=dest)
us_maipubkeys = UploadSet('maipubkeys', 'pub', default_dest=dest)
us_maisignatures = UploadSet('maisignatures', 'sig', default_dest=dest)


def configure_upload_blueprint(app):
    configure_uploads(app, (us_eadata, us_maipubkeys, us_maisignatures))
    patch_request_class(app, app.config['MAX_CONTENT_LENGTH'])


from brainyserver.upload import views
