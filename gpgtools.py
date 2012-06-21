#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tools to verify signatures and extract content from signed files."""


import re

import gnupg

import settings as st


gpg = gnupg.GPG(st.GPG_HOME)


def verify_signature(mongo, jsonfile_signed, androidapp_id):
    """Check a file's androidapp signature."""
    v = gpg.verify_file(jsonfile_signed)
    
    if v.status == 'no public key':
        raise Exception('Public key not found')
    
    ref = mongo[st.MONGO_COLL_AAFINGERPRINTS].find_one(
                                            {'androidapp_id': androidapp_id})
    ref_fingerprint = ref['fingerprint']
    return v.valid and v.fingerprint == ref_fingerprint


def seek_to_content(jsonfile_signed):
    jsonfile_signed.seek(0)
    
    prev_line1 = ''
    prev_line2 = ''
    gpgfound = False
    for l in jsonfile_signed:
        
        if re.search('-----BEGIN PGP SIGNED MESSAGE-----.*', prev_line2):
            gpgfound = True
            break
        
        prev_line2 = prev_line1
        prev_line1 = l
    
    if not gpgfound:
        raise Exception('GPG Signature Not Found')


def read_til_signature(jsonfile_signed):
    output = u''
    
    for l in jsonfile_signed:
        if re.search('-----BEGIN PGP SIGNATURE-----.*', l):
            break
        output += l
    
    return output
