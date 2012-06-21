#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tools to verify signatures and extract content from signed files."""


import re

import gnupg

import settings as st


gpg = gnupg.GPG(gnupghome=st.GPG_HOME)


def save_pubkey(mongo, androidapp_id, pubkeyfile):
    """Save a public key from file to GnuPG and MongoDB."""
    keystr = pubkeyfile.read()
    r = gpg.import_keys(keystr)
    
    if r.count != 1:
        raise Exception('Error while importing public key')
    
    mongo.db[st.MONGO_CL_AAFPS].insert({'androidapp_id': androidapp_id,
                                        'fingerprint': r.fingerprints[0]})
    return True


def flush_db():
    """Flush the GPG database."""
    fp_list = [key['fingerprint'] for key in gpg.list_keys()]
    gpg.delete_keys(fp_list, True)
    gpg.delete_keys(fp_list)


def verify_signature(mongo, file_signed, androidapp_id):
    """Check a file's androidapp signature."""
    v = gpg.verify_file(file_signed)
    ref = mongo.db[st.MONGO_CL_AAFPS].find_one(
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
