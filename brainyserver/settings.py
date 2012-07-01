#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Settings for the application."


from M2Crypto import EC


# Flask app settings

SECRET_KEY = 'development key'
DEBUG_TB_INTERCEPT_REDIRECTS = False


# Data uploading settings

MAX_CONTENT_LENGTH = 16 * 1024 * 1024


# MongDB settings

MONGODB_DB = 'brainyserver'


# Elliptic Curve cryptography settings
# THIS SHOULD NOT BE CHANGED OR ELSE NO APP SIGNATURES WILL BE VALID

EC_NID = EC.NID_sect571k1
