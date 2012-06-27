#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""User blueprint."""


from flask import Blueprint

from brainyserver import app


user = Blueprint('user', __name__, template_folder='templates')

from brainyserver.user import views
