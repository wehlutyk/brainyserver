#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""MongoDB documents.

Classes:
  * ``Researcher``: represent a researcher
  * ``Result``: represent a result set from a subject
  * ``ExpApp``: represent an experiment app, (to be) published to devices
  * ``MetaAppInstance``: represent an installation (i.e. an instance) of
    brainydroid on a device

"""


import datetime

import mongoengine as mongo

from brainyserver.crypto import encrypt_password


class Researcher(mongo.Document):
    
    """Represent a researcher.
    
    Class attributes:
      * ``username``
      * ``email``
      * ``expapps``: a list of references to the ``ExpApp``s owned by the
        researcher
      * ``pwsalt``: the salt for encryption of the password
      * ``pwhash``: the salted sha512 hash of the password
    
    Methods:
      * ``set_passord``: set the researcher's password
      * ``check_password``: check if the researcher's password is the one
        given
    
    """
    
    username = mongo.StringField(regex='^[a-zA-Z0-9_-]+$', required=True,
                                 unique=True, min_length=3, max_length=50)
    email = mongo.EmailField(required=True, unique=True, min_length=3,
                             max_length=50)
    expapps = mongo.ListField(mongo.ReferenceField('ExpApp'))
    pwsalt = mongo.StringField(required=True)
    pwhash = mongo.StringField(required=True)
    
    def set_password(self, pw):
        """Set the researcher's password."""
        pwsalt, pwhash = encrypt_password(pw)
        self.pwsalt = pwsalt
        self.pwhash = pwhash
    
    def check_password(self, pw):
        """Check if the researcher's password is the one given."""
        pwhash = encrypt_password(pw, str(self.pwsalt))[1]
        return pwhash == str(self.pwhash)


class Result(mongo.DynamicEmbeddedDocument):
    
    """Represent a result set from a subject.
    
    Class attributes:
      * ``created_at``: the date of creation
      * ``metaappinstance``: a reference to the owning ``MetaAppInstance``
      * ``data``: a string meant to contain a json string representing the
         data
    
    """
    
    created_at = mongo.DateTimeField(default=datetime.datetime.now,
                                     required=True)
    metaappinstance = mongo.ReferenceField('MetaAppInstance', required=True)
    data = mongo.StringField(required=True)


class ExpApp(mongo.Document):
    
    """Represent an experiment app, (to be) published to devices.
    
    Class attributes:
      * ``name``: a name for the experiment app
      * ``description``: short description of the experiment 
      * ``owners``: a list of references to ``Researcher`` documents which are
        the experiment's owners
      * ``results``: a list of references to ``Result`` documents
      * ``previzpjs``: a string containing the code for the previz
    
    """
    
    ea_name = mongo.StringField(regex='^[a-zA-Z0-9_-]+$', required=True,
                                unique=True, min_length=3, max_length=50)
    description = mongo.StringField(max_length=300)
    owners = mongo.ListField(mongo.ReferenceField(Researcher), required=True)
    results = mongo.ListField(mongo.EmbeddedDocumentField(Result))
    previzpjs = mongo.StringField()


class MetaAppInstance(mongo.Document):
    
    """Represent an installation (i.e. an instance) of brainydroid on a
    device.
    
    Class attributes:
      * ``mai_id``: a Meta App Instance ID
      * ``pubkey_ec``: an elliptic curve public key
    
    """
    
    mai_id = mongo.StringField(regex='^[a-zA-Z0-9_-]+$', required=True,
                               unique=True, min_length=3, max_length=150)
    pubkey_ec = mongo.StringField(max_length=5000, required=True)
