#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Forms for the user blueprint."""


from flask.ext.wtf import Form, TextAreaField


class EditPrevizForm(Form):
    
    source = TextAreaField('Source code of the previz')
