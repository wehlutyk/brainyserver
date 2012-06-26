#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Admin blueprint views."""


from brainyserver.admin.showmongo import mongo_all_tostring
from brainyserver.admin import admin
from brainyserver import mongodb


@admin.route('/show_db')
def show_db():
    """Return the MongoDB data."""
    return mongo_all_tostring('html')


@admin.route('/flush_db')
def flush_db():
    """Flush the MongoDB and GPG data."""
    mongodb.drop_all_collections()
    return 'Database flushed.\n'
