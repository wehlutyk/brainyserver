#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Admin blueprint views."""


from brainyserver import app, mongo
from brainyserver.admin.showmongo import mongo_all_tostring
import brainyserver.gpgtools as gpgtools
from brainyserver.admin import admin


@admin.route('/show_db')
def show_db():
    """Return the MongoDB data."""
    return mongo_all_tostring('html')


@admin.route('/flush_db')
def flush_db():
    """Flush the MongoDB and GPG data."""
    mongo.db.drop_collection(app.config['MONGO_CL_AADATA'])
    mongo.db.drop_collection(app.config['MONGO_CL_AAFPS'])
    gpgtools.flush_db()
    return 'Database flushed.\n'
