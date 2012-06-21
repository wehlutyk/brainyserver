#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tools to handle uploaded files."""


import gpgtools
import settings as st


def file_allowed(f):
    """Check that a file's extension is allowed for upload."""
    fn = f.filename
    return '.' in fn and fn.rsplit('.', 1)[1] in st.ALLOWED_EXTENSIONS


def validate_file(mongo, jsonfile_signed, androidapp_id):
    """Check uploaded file's extension and validate the data signature."""
    return (file_allowed(jsonfile_signed) and
            gpgtools.verify_signature(mongo, jsonfile_signed, androidapp_id))


def json_signed_tostring(jsonfile_signed):
    gpgtools.seek_to_content(jsonfile_signed)
    return gpgtools.read_til_signature(jsonfile_signed)
