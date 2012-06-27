#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Upload blueprint views."""


import os
import json

from flask import request

from brainyserver.upload import (upload, us_maipubkeys, us_eadata,
                                 us_maisignatures, crypto)
from brainyserver.mongodb import MetaAppInstance, ExpApp, Result


def file_allowed(uploadset, f):
    return uploadset.file_allowed(f, os.path.basename(f.filename))


@upload.route('/mai_pubkey/<mai_id>', methods=['POST'])
def mai_pubkey(mai_id):
    """Process a public key uploaded for a MetaAppInstance."""
    pubkeyfile = request.files['pubkeyfile']
    
    if not pubkeyfile:
        return 'No pubkeyfile uploaded -> key not uploaded.\n'
    
    if not file_allowed(us_maipubkeys, pubkeyfile):
        return 'Filetype not allowed -> key not uploaded.\n'
    
    if MetaAppInstance.objects(mai_id=mai_id).count() >= 1:
        return ('This Meta App Instance (id={}) already exists and has a key '
                '-> key not uploaded.\n').format(mai_id)
    
    mai = MetaAppInstance(mai_id=mai_id, pubkey_ec=pubkeyfile.read())
    mai.save()
    
    return 'Key saved.\n'


@upload.route('/ea_data/<mai_id>/<ea_id>', methods=['POST'])
def ea_data(mai_id, ea_id):
    """Process data uploaded by a MetaAppInstance for an ExpApp."""
    datafile = request.files['datafile']
    sigfile = request.files['sigfile']
    
    if not datafile:
        return 'No datafile uploaded -> no data uploaded.\n'
    
    if not file_allowed(us_eadata, datafile):
        return 'Filetype not allowed -> no data uploaded.\n'
    
    if not sigfile:
        return 'No sigfile uploaded -> no data uploaded.\n'
    
    if not file_allowed(us_maisignatures, sigfile):
        return 'Filetype not allowed -> no data uploaded.\n'
    
    mais = MetaAppInstance.objects(mai_id=mai_id)
    if len(mais) == 0:
        return ('Unknown MetaAppInstance (id={}) -> no data '
                'uploaded.\n').format(mai_id)
    
    mai = mais[0]
    ecv = crypto.ECVerifier(mai)
    datastring = datafile.read()
    
    if not ecv.verify(datastring, sigfile):
        return 'Signature invalid -> no data uploaded.\n'
    
    eas = ExpApp.objects(ea_id=ea_id)
    if len(eas) == 0:
        return ('Unknown ExpApp (id={}) -> no data '
                'uploaded.\n').format(ea_id)
                
    ea = eas[0]
    r = Result(**json.loads(datastring))
    r.metaappinstance = mai
    ea.results.append(r)
    ea.save()

    return 'Data uploaded.\n'
