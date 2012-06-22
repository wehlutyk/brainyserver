#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tools for accessing the gpg database."""


from brainyserver import app
from brainyserver.db import gpg


def save_pubkey(mongo, androidapp_id, pubkeyfile):
    """Save a public key from file to GnuPG and MongoDB."""
    keystr = pubkeyfile.read()
    r = gpg.import_keys(keystr)
    
    if r.count != 1:
        raise Exception('Error while importing public key')
    
    mongo.db[app.config['MONGO_CL_AAFPS']].insert(
                                        {'androidapp_id': androidapp_id,
                                         'fingerprint': r.fingerprints[0]})
    return True


def flush_db():
    """Flush the GPG database."""
    fp_list = [key['fingerprint'] for key in gpg.list_keys()]
    gpg.delete_keys(fp_list, True)
    gpg.delete_keys(fp_list)
