#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Forms for the user blueprint."""


from flask.ext.wtf import Form, TextField, validators

from brainyserver.mongodb import ExpApp


class ExpAppIDValidator(object):
    
    def __call__(self, form, field):
        if ExpApp.objects(ea_id=field.data).count() != 0:
            raise validators.ValidationError(('This ID is already '
                                               'in use'))


class AddExpAppForm(Form):
    
    ea_id = TextField('App ID', [validators.Length(min=3, max=50),
                                 ExpAppIDValidator()])
    description = TextField('Short description',
                            [validators.Length(max=100)])
