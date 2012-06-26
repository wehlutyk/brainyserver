#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Upload blueprint views."""


import os
import json

from flask import request

from brainyserver.upload import (upload, us_aapubkeys, us_aadata,
                                 us_aasignatures, crypto)
from brainyserver.mongodb import AndroidApp, Result


def file_allowed(uploadset, f):
    return uploadset.file_allowed(f, os.path.basename(f.filename))


@upload.route('/pubkey/<aa_id>', methods=['POST'])
def pubkey(aa_id):
    """Process a public key uploaded for an androidapp."""
    pubkeyfile = request.files['pubkeyfile']
    
    if not pubkeyfile:
        return 'No pubkeyfile uploaded -> key not uploaded.\n'
    
    if not file_allowed(us_aapubkeys, pubkeyfile):
        return 'Filetype not allowed -> key not uploaded.\n'
    
    if AndroidApp.objects(aa_id=aa_id).count() >= 1:
        return ('This Android App (id={}) already exists and has a key '
                '-> key not uploaded.\n').format(aa_id)
    
    aa = AndroidApp(aa_id=aa_id, pubkey=pubkeyfile.read())
    aa.save()
    
    return 'Key saved.\n'


@upload.route('/data/<aa_id>', methods=['POST'])
def data(aa_id):
    """Process data uploaded by an androidapp."""
    datafile = request.files['datafile']
    sigfile = request.files['sigfile']
    
    if not datafile:
        return 'No datafile uploaded -> no data uploaded.\n'
    
    if not file_allowed(us_aadata, datafile):
        return 'Filetype not allowed -> no data uploaded.\n'
    
    if not sigfile:
        return 'No sigfile uploaded -> no data uploaded.\n'
    
    if not file_allowed(us_aasignatures, sigfile):
        return 'Filetype not allowed -> no data uploaded.\n'
    
    datastring = datafile.read()
    ecv = crypto.ECVerifier(aa_id)
    
    if not ecv:
        return ('Unknown Android app ID (id={}) -> no data '
                'uploaded.\n').format(aa_id)
    
    if not ecv.verify(datastring, sigfile):
        return 'Signature invalid -> no data uploaded.\n'
    
    aa = AndroidApp.objects(aa_id=aa_id)[0]
    r = Result(**json.loads(datastring))
    aa.results.append(r)
    aa.save()

    return 'Data uploaded.\n'
