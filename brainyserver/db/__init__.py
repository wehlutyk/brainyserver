#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tools for manipulating the databases."""


import gnupg

from brainyserver import app


gpg = gnupg.GPG(gnupghome=app.config['GPG_HOME'])
