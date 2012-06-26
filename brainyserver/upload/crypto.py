#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Cryptographic tools for signing and verifying."""


from hashlib import sha512

from M2Crypto import EC, BIO
import bsontools

from brainyserver.mongodb import AndroidApp


class ECVerifier(object):
    
    def __init__(self, aa_id):
        
        # TODO: We could check for revoked keys here
        
        aas = AndroidApp.objects(aa_id=aa_id)
        
        if len(aas) == 0:
            return None
        
        aa = aas[0]
        self._ecs = []
        #for aa in aas:
        bio = BIO.MemoryBuffer(str(aa.pubkey))
        self._ecs.append(EC.load_pub_key_bio(bio))
    
    def digest(self, datastring):
        sha = sha512()
        sha.update(datastring)
        return sha.digest()
    
    def bson_to_sigtuple(self, sigfile):
        return bsontools.loads(sigfile.read())
    
    def verify(self, datastring, sigfile):
        digest = self.digest(datastring)
        sig = self.bson_to_sigtuple(sigfile)
        return sum([bool(ec.verify_dsa(digest, sig['r'], sig['s']))
                    for ec in self._ecs])
