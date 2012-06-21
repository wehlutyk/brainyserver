#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Main file for the brainyserver server."


import json
import os

from flask import Flask, request, abort
from flask.ext.pymongo import PyMongo
from flask.ext.uploads import UploadSet, configure_uploads

import uploadtools as ut
import settings as st
from showmongo import mongo_all_tostring


# Create the Flask app, its MongDB connection, and the GnuPG home.

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = st.MAX_CONTENT_LENGTH
app.config['MONGO_DBNAME'] = st.MONGO_DBNAME
mongo = PyMongo(app)
os.makedirs('gpg', 700)


@app.route('/')
def hello():
    """Say hello."""
    return 'Hello World!\n'

@app.route('/showdata')
def showdata():
    """Return the MongDB data."""
    return mongo_all_tostring('html')


@app.route('/uploadpublickey/<androidapp_id>', methods=['POST'])
def uploadpublickey(androidapp_id):
    """Process a public key uploaded for an androidapp."""
    ret = ''


@app.route('/uploaddata/<androidapp_id>', methods=['POST'])
def uploaddata(androidapp_id):
    """Process data uploaded by an androidapp."""
    ret = ''

    if request.method == 'POST':

        jsonfile_signed = request.files['jsonfile_signed']

        if not jsonfile_signed:
            abort(400)

        if not ut.validate_file(jsonfile_signed, androidapp_id):
            abort(401)

        jsonstring = ut.json_signed_tostring(jsonfile_signed)
        mongo.db[st.MONGO_COLL_AADATA].insert(json.loads(jsonstring))
        ret = 'File uploaded.\n'

    return ret


if __name__ == '__main__':
    app.debug = True
    app.run()
