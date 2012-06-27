#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""MongoDB documents."""


import datetime

from brainyserver import mongo


class Researcher(mongo.Document):
    username = mongo.StringField(required=True, unique=True, min_length=3,
                                 max_length=50)
    email = mongo.EmailField(required=True, unique=True, min_length=3,
                             max_length=50)
    expapps = mongo.ListField(mongo.ReferenceField('ExpApp'))
    pwsalt = mongo.StringField(required=True)
    pwhash = mongo.StringField(required=True)


class Result(mongo.DynamicEmbeddedDocument):
    created_at = mongo.DateTimeField(default=datetime.datetime.now,
                                     required=True)
    metaappinstance = mongo.ReferenceField('MetaAppInstance', required=True)


class ExpApp(mongo.Document):
    ea_id = mongo.StringField(regex='^[a-zA-Z0-9_-]+$', required=True,
                              unique=True, min_length=3, max_length=50)
    description = mongo.StringField(max_length=100)
    owners = mongo.ListField(mongo.ReferenceField(Researcher), required=True)
    results = mongo.ListField(mongo.EmbeddedDocumentField(Result))


class MetaAppInstance(mongo.Document):
    mai_id = mongo.StringField(regex='^[a-zA-Z0-9_-]+$', required=True,
                               unique=True, min_length=3, max_length=50)
    pubkey_ec = mongo.StringField(max_length=5000, required=True)


def drop_all_collections():
    Researcher.drop_collection()
    ExpApp.drop_collection()
    MetaAppInstance.drop_collection()
