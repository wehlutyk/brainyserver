#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Main file for the brainyserver server."


import os
import stat

from flask import Flask, request, abort
from flask.ext.pymongo import PyMongo
from flask.ext.uploads import (UploadSet, configure_uploads,
                               patch_request_class)

import uploadtools as ut
import gpgtools
import settings as st
from showmongo import mongo_all_tostring


# Create the Flask app, its MongDB connection, and the GnuPG home.

app = Flask(__name__)

app.config['MONGO_DBNAME'] = st.MONGO_DBNAME
mongo = PyMongo(app)

if not os.path.exists(st.GPG_HOME):
    os.makedirs(st.GPG_HOME)
os.chmod(st.GPG_HOME, stat.S_IRWXU)


# Configure upload sets

dest=lambda app: os.path.join(app.root_path, 'uploads')
us_aadata = UploadSet('aadata', 'json_signed', default_dest=dest)
us_aafps = UploadSet('aafps', 'pub', default_dest=dest)
configure_uploads(app, (us_aadata, us_aafps))
patch_request_class(app, st.MAX_CONTENT_LENGTH)


@app.route('/')
def hello():
    """Say hello."""
    return 'Hello World!\n'


@app.route('/showdata')
def showdata():
    """Return the MongoDB data."""
    return mongo_all_tostring('html')


@app.route('/uploadpubkey/<androidapp_id>', methods=['POST'])
def uploadpubkey(androidapp_id):
    """Process a public key uploaded for an androidapp."""
    pubkeyfile = request.files['pubkeyfile']
    
    if not pubkeyfile:
        abort(400)
    
    if not ut.file_allowed(us_aafps, pubkeyfile):
        abort(401)
    
    if not gpgtools.save_pubkey(mongo, androidapp_id, pubkeyfile):
        abort(500)
    
    return 'Key saved.\n'


@app.route('/uploaddata/<androidapp_id>', methods=['POST'])
def uploaddata(androidapp_id):
    """Process data uploaded by an androidapp."""
    jsonfile_signed = request.files['jsonfile_signed']

    if not jsonfile_signed:
        abort(400)

    if not ut.validate_file(us_aadata, mongo, jsonfile_signed, androidapp_id):
        abort(401)

    data = ut.json_signed_tofulldict(jsonfile_signed, androidapp_id)
    mongo.db[st.MONGO_CL_AADATA].insert(data)

    return 'File uploaded.\n'


if __name__ == '__main__':
    app.debug = True
    app.run()
