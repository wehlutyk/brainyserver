#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Forms for the root of the app."""


from flask.ext.wtf import Form, PasswordField, TextField, validators

from brainyserver.mongodb import Researcher


class UsernameMongoValidator(object):
    
    def __call__(self, form, field):
        if Researcher.objects(username=field.data).count() != 0:
            raise validators.ValidationError(('That username is already '
                                              'in use'))


class EmailMongoValidator(object):
    
    def __call__(self, form, field):
        if Researcher.objects(email=field.data).count() != 0:
            raise validators.ValidationError(('That email address is already '
                                              'in use'))


class RegisterForm(Form):
    username = TextField('Username', [validators.Length(min=3, max=50),
                                      UsernameMongoValidator()])
    email = TextField('Email Address', [validators.Length(min=3, max=50),
                                        validators.Email(),
                                        EmailMongoValidator()])
    password = PasswordField('Password', [validators.Length(min=8,
                        message='Password must be at least 8 characters long')])
    confirmpassword = PasswordField('Confirm password',
                                    [validators.EqualTo('password',
                                                    "Passwords don't match")])
