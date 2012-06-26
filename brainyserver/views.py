#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Views for the root of the app."""


from brainyserver import app


@app.route('/')
def index():
    return 'Hello, it works! Follow the tutorial for more interesting stuff.'
