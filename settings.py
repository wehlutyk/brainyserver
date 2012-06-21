#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Settings for the application."


# Data uploading settings

ALLOWED_EXTENSIONS = set(['json_signed'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024


# MongDB settings

MONGO_DBNAME = 'brainyserver'
MONGO_COLL_AADATA = 'androidapps_data'
MONGO_COLL_AAFINGERPRINTS = 'androidapps_keyfingerprints'


# GnuPG settigns

GPG_HOME = './gpg'
