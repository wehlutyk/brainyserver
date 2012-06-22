#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tools to handle uploaded files."""


import re
import os
import json

from brainyserver.db import gpg
from brainyserver import app


def file_allowed(uploadset, f):
    return uploadset.file_allowed(f, os.path.basename(f.filename))


def validate_file(uploadset, mongo, f, androidapp_id):
    """Check uploaded file's extension and validate the data signature."""
    return (file_allowed(uploadset, f) and
            verify_signature(mongo, f, androidapp_id))


def json_signed_tostring(jsonfile_signed):
    seek_to_content(jsonfile_signed)
    return read_til_signature(jsonfile_signed)


def json_signed_tofulldict(jsonfile_signed, androidapp_id):
    jsonstring = json_signed_tostring(jsonfile_signed)
    data = json.loads(jsonstring)
    data.update({'androidapp_id': androidapp_id})
    return data


def verify_signature(mongo, file_signed, androidapp_id):
    """Check a file's androidapp signature."""
    v = gpg.verify_file(file_signed)
    ref = mongo.db[app.config['MONGO_CL_AAFPS']].find_one(
                                            {'androidapp_id': androidapp_id})
    
    if v.status == 'no public key' or not ref:
        raise Exception('Public key not found')
    
    ref_fingerprint = ref['fingerprint']
    return v.valid and v.fingerprint == ref_fingerprint


def seek_to_content(file_signed):
    file_signed.seek(0)
    
    prev_line1 = ''
    prev_line2 = ''
    gpgfound = False
    for l in file_signed:
        
        if re.search('-----BEGIN PGP SIGNED MESSAGE-----.*', prev_line2):
            gpgfound = True
            break
        
        prev_line2 = prev_line1
        prev_line1 = l
    
    if not gpgfound:
        raise Exception('GPG Signature Not Found')


def read_til_signature(file_signed):
    output = u''
    
    for l in file_signed:
        if re.search('-----BEGIN PGP SIGNATURE-----.*', l):
            break
        output += l
    
    return output
