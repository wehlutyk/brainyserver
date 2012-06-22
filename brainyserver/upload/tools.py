#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tools to handle uploaded files."""


import os
import json

import brainyserver.gpgtools as gpgtools


def file_allowed(uploadset, f):
    return uploadset.file_allowed(f, os.path.basename(f.filename))

def validate_file(uploadset, mongo, f, androidapp_id):
    """Check uploaded file's extension and validate the data signature."""
    return (file_allowed(uploadset, f) and
            gpgtools.verify_signature(mongo, f, androidapp_id))


def json_signed_tostring(jsonfile_signed):
    gpgtools.seek_to_content(jsonfile_signed)
    return gpgtools.read_til_signature(jsonfile_signed)


def json_signed_tofulldict(jsonfile_signed, androidapp_id):
    jsonstring = json_signed_tostring(jsonfile_signed)
    data = json.loads(jsonstring)
    data.update({'androidapp_id': androidapp_id})
    return data
