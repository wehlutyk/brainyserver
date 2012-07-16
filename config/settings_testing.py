#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Settings for the application in testing mode.

Divides into:
  * General Flask app settings
  * Data upload settings
  * MongoDB settings

"""


# Flask app settings

SECRET_KEY = 'testing key'
DEBUG = True
TESTING = True
HOST = '127.0.0.1'


# Data uploading settings

MAX_CONTENT_LENGTH = 16 * 1024 * 1024


# MongDB settings

MONGODB_DB = 'brainyserver_testing'
