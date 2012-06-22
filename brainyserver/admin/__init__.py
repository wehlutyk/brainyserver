#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Admin blueprint."""


from flask import Blueprint

from brainyserver import app


admin = Blueprint('admin', __name__, template_folder='templates')

from brainyserver.admin import views
