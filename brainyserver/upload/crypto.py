#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Cryptographic tools for signing and verifying."""


from hashlib import sha512

from M2Crypto import EC, BIO
import bsontools


class ECVerifier(object):
    
    def __init__(self, mai):
        self.mai = mai
        self._ecs = []
        bio = BIO.MemoryBuffer(str(self.mai.pubkey_ec))
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
