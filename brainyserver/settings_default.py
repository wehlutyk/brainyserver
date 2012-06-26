#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Settings for the application."


# Flask app settings

DEBUG = False
SECRET_KEY = 'YMWBpGgufZgC2Vy7pMu+fRBAAG0Gx1dHlrEBtZWhoby5uZXQ+iQE+BBMBAgNAhs'
DEBUG_TB_INTERCEPT_REDIRECTS = False


# Data uploading settings

MAX_CONTENT_LENGTH = 16 * 1024 * 1024


# MongDB settings

MONGODB_DB = 'brainyserver'
MONGO_CL_AADATA = 'androidapps_data'
MONGO_CL_AAFPS = 'androidapps_keyfingerprints'


# GnuPG settigns

GPG_HOME = './gpg'
