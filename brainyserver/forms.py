#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Forms for urls at the root of the app.

Classes:
  * ``UsernameMongoValidator``: check that a username isn't already used
  * ``EmailMongoValidator``: check that an email isn't already used
  * ``RegisterForm``: provide a registration form
  * ``LoginForm``: provide a login form
  * ``ExpAppNameMongoValidator``: check that an ExpAppName isn't already used
  * ``AddExpAppForm``: provide a form to create a new ExpApp

"""


from flask.ext.wtf import Form, PasswordField, TextField, validators

from brainyserver.mongodb import Researcher, ExpApp


class UsernameMongoValidator(object):
    
    """Check that a username isn't already used."""
    
    def __call__(self, form, field):
        if Researcher.objects(username=field.data).count() != 0:
            raise validators.ValidationError(('That username is already '
                                              'in use'))


class EmailMongoValidator(object):
    
    """Check that an email isn't already used."""
    
    def __call__(self, form, field):
        if Researcher.objects(email=field.data).count() != 0:
            raise validators.ValidationError(('That email address is already '
                                              'in use'))


class RegisterForm(Form):
    
    """Provide a registration form.
    
    Class attributes:
      * ``username``: gets checked for format, length, and checked that it's
        not already used
      * ``email``: gets checked for format, length, and checked that it's not
        already used
      * ``password``: is checked for length
      * ``confirmpassword``: confirmation for the password, is checked that it
        matches the ``password`` field
    
    """
    
    username = TextField('Username',
        [validators.Length(min=3, max=50),
         UsernameMongoValidator(),
         validators.Regexp('^[a-zA-Z0-9_-]+$',
                           message=('Only alphanumerical characters (with '
                                    "'-' and '_') please!"))])
    email = TextField('Email Address', [validators.Length(min=3, max=50),
                                        validators.Email(),
                                        EmailMongoValidator()])
    password = PasswordField('Password', [validators.Length(min=8,
                    message='Password must be at least 8 characters long')])
    confirmpassword = PasswordField('Confirm password',
                                    [validators.EqualTo('password',
                                                    "Passwords don't match")])


class LoginForm(Form):
    
    """Provide a login form.
    
    Class attributes:
      * ``username_email``: the username or email of the user to log in; gets
        checked for length
      * ``password``
    
    """
    
    username_email = TextField('Username or Email',
                               [validators.Length(min=3, max=50)])
    password = PasswordField('Password',
                [validators.Required(message='Please type in your password')])


class ExpAppNameMongoValidator(object):
    
    """Check that an ExpAppName isn't already used."""
    
    def __call__(self, form, field):
        if ExpApp.objects(name=field.data).count() != 0:
            raise validators.ValidationError(('You are already using this '
                                              'name'))


class AddExpAppForm(Form):
    
    """Provide a form to create a new ExpApp.
    
    Class attributes:
      * ``name``: the name of the experiment app; gets checked for length,
        format, and checked that the name isn't already used
      * ``description``: a short description for the experiment; gets checked
        for maximum length
    
    """
    
    ea_name = TextField('App name',
        [validators.Length(min=3, max=50),
         ExpAppNameMongoValidator(),
         validators.Regexp('^[a-zA-Z0-9_-]+$',
                           message=('Only alphanumerical characters (with '
                                    "'-' and '_') please!"))])
    description = TextField('A short description',
                            [validators.Length(max=300)])
