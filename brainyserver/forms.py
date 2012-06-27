#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Forms for the root of the app."""


from flask.ext.wtf import Form, PasswordField, TextField, validators


class RegisterForm(Form):
    username = TextField('Username', [validators.Length(min=3, max=50)])
    email = TextField('Email Address', [validators.Length(min=3, max=50),
                                        validators.Email()])
    password = PasswordField('Password')
