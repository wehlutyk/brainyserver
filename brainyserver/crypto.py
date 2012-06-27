#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Cryptographic tools for signing and verifying."""


import string
import random
from hashlib import sha512

from M2Crypto import EC, BIO
import bsontools


def sha512_hash(string):
    sha = sha512()
    sha.update(string)
    return sha.digest()


def sha512_hash_hex(string):
    sha = sha512()
    sha.update(string)
    return sha.hexdigest()


def gen_salt():
    presalt = ''.join(random.choice(string.printable) for i in range(20))
    return sha512_hash_hex(presalt)


def encrypt_password(pw, pwsalt=None):
    if pwsalt == None:
        pwsalt = gen_salt()
    return pwsalt, sha512_hash_hex(pwsalt + pw)


class ECVerifier(object):
    
    def __init__(self, mai):
        self.mai = mai
        self._ecs = []
        bio = BIO.MemoryBuffer(str(self.mai.pubkey_ec))
        self._ecs.append(EC.load_pub_key_bio(bio))
    
    def bson_to_sigtuple(self, sigfile):
        return bsontools.loads(sigfile.read())
    
    def verify(self, datastring, sigfile):
        digest = sha512_hash(datastring)
        sig = self.bson_to_sigtuple(sigfile)
        return sum([bool(ec.verify_dsa(digest, sig['r'], sig['s']))
                    for ec in self._ecs])
