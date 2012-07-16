#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Settings for the application.

Divides into:
  * General Flask app settings
  * Data upload settings
  * MongoDB settings

"""


# Flask app settings

SECRET_KEY = 'development key'
DEBUG_TB_INTERCEPT_REDIRECTS = False


# Data uploading settings

MAX_CONTENT_LENGTH = 16 * 1024 * 1024


# MongDB settings

MONGODB_DB = 'brainyserver'
