#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Settings for the application."


# Data uploading settings

MAX_CONTENT_LENGTH = 16 * 1024 * 1024


# MongDB settings

MONGO_DBNAME = 'brainyserver'
MONGO_CL_AADATA = 'androidapps_data'
MONGO_CL_AAFPS = 'androidapps_keyfingerprints'


# GnuPG settigns

GPG_HOME = './gpg'
