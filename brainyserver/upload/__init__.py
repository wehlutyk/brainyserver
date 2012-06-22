#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Upload blueprint."""


import os

from flask import Blueprint
from flask.ext.uploads import (UploadSet, configure_uploads,
                               patch_request_class)

from brainyserver import app


upload = Blueprint('upload', __name__, template_folder='templates')


# Configure upload sets

dest=lambda app: os.path.join(app.root_path, 'uploads')
us_aadata = UploadSet('aadata', 'json_signed', default_dest=dest)
us_aafps = UploadSet('aafps', 'pub', default_dest=dest)
configure_uploads(app, (us_aadata, us_aafps))
patch_request_class(app, app.config['MAX_CONTENT_LENGTH'])


from brainyserver.upload import views
