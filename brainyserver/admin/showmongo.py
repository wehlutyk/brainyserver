#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Show the contents of all MondoDB databases."""


import pymongo as pm


def createline_raw(line=''):
    return line + '\n'


def createline_html(line=''):
    return '<p>' + line + '</p>'


def mongo_all_tostring(fmt='raw'):
    """Print out all documents from all collections from all databases
    (except indexes)."""
    
    createline = {'raw': createline_raw, 'html': createline_html}
    output = u''
    
    conn = pm.Connection()
    
    for dbn in conn.database_names():
        
        if dbn in [u'local', u'admin']:
            continue
        
        output += createline[fmt]()
        output += createline[fmt]('==============================')
        output += createline[fmt]('Database: "%s"' % dbn)
        output += createline[fmt]()
        db = conn[dbn]
        
        for colln in db.collection_names():
            
            if colln == 'system.indexes':
                continue
            
            output += createline[fmt]('-----')
            output += createline[fmt]('Collection: "%s"' % colln)
            output += createline[fmt]()
            coll = db[colln]
            
            for doc in coll.find():
                output += createline[fmt]('%s' % doc)
    
    return output
