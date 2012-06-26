#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""MongoDB documents."""


import datetime

from brainyserver import mongo


class User(mongo.Document):
    username = mongo.StringField(required=True, unique=True, min_length=3,
                                 max_length=50)
    email = mongo.EmailField(required=True, unique=True)
    androidapps = mongo.ListField(mongo.ReferenceField('AndroidApp'))


class Result(mongo.DynamicEmbeddedDocument):
    created_at = mongo.DateTimeField(default=datetime.datetime.now,
                                     required=True)


class AndroidApp(mongo.Document):
    aa_id = mongo.StringField(regex='^[a-zA-Z0-9_-]+$', required=True,
                              unique=True, min_length=3, max_length=50)
    pubkey = mongo.StringField(max_length=5000, required=True)
    description = mongo.StringField(max_length=100)
    owners = mongo.ListField(mongo.ReferenceField(User))
    results = mongo.ListField(mongo.EmbeddedDocumentField(Result))


def drop_all_collections():
    User.drop_collection()
    AndroidApp.drop_collection()
