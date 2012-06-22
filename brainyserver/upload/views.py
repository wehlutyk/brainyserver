#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Upload blueprint views."""


from flask import abort, request

from brainyserver import app, mongo
import brainyserver.db.gpgtools as gpgtools
from brainyserver.upload import upload, us_aafps, us_aadata, tools


@upload.route('/pubkey/<androidapp_id>', methods=['POST'])
def pubkey(androidapp_id):
    """Process a public key uploaded for an androidapp."""
    pubkeyfile = request.files['pubkeyfile']
    
    if not pubkeyfile:
        abort(400)
    
    if not tools.file_allowed(us_aafps, pubkeyfile):
        abort(401)
    
    if not gpgtools.save_pubkey(mongo, androidapp_id, pubkeyfile):
        abort(500)
    
    return 'Key saved.\n'


@upload.route('/data/<androidapp_id>', methods=['POST'])
def data(androidapp_id):
    """Process data uploaded by an androidapp."""
    jsonfile_signed = request.files['jsonfile_signed']

    if not jsonfile_signed:
        abort(400)

    if not tools.validate_file(us_aadata, mongo, jsonfile_signed,
                               androidapp_id):
        abort(401)

    data = tools.json_signed_tofulldict(jsonfile_signed, androidapp_id)
    mongo.db[app.config['MONGO_CL_AADATA']].insert(data)

    return 'File uploaded.\n'
