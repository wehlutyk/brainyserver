#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Settings for the application in default mode, i.e. production mode.

Divides into:
  * General Flask app settings
  * Data upload settings
  * MongoDB settings

"""


# Flask app settings

SECRET_KEY = 'development key'
DEBUG = False
TESTING = False
HOST = '0.0.0.0'


# Data uploading settings

MAX_CONTENT_LENGTH = 16 * 1024 * 1024


# MongDB settings

MONGODB_DB = 'brainyserver'
