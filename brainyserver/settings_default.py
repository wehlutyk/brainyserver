#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Settings for the application."


from M2Crypto import EC


# Flask app settings

DEBUG = False
SECRET_KEY = 'YMWBpGgufZgC2Vy7pMu+fRBAAG0Gx1dHlrEBtZWhoby5uZXQ+iQE+BBMBAgNAhs'
DEBUG_TB_INTERCEPT_REDIRECTS = False


# Data uploading settings

MAX_CONTENT_LENGTH = 16 * 1024 * 1024


# MongDB settings

MONGODB_DB = 'brainyserver'


# Elliptic cryptography settings
# THIS SHOULD NOT BE CHANGED OR ELSE NO APP SIGNATURES WILL BE VALID

EC_NID = EC.NID_X9_62_c2tnb431r1
