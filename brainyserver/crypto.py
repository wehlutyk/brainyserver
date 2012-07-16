#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tools for cryptographic signing, verifying, and encrypting of passwords.

Methods:
  * ``sha512_hash``: hash a string with the sha512 function
  * ``sha512_hash_hex``: hash a string with the sha512 function and return the
    hex representation
  * ``gen_salt``: create a salt to use with password encryption
  * ``encrypt_password``: encrypt a password with salted sha512

Classes:
  * ``ECVerifier``: verify elliptic curve signatures

"""


import string
import random
from hashlib import sha512

from M2Crypto import EC, BIO


def sha512_hash(string):
    """Hash a string with the sha512 function."""
    sha = sha512()
    sha.update(string)
    return sha.digest()


def sha512_hash_hex(string):
    """Hash a string with the sha512 function and return the hex
    representation."""
    sha = sha512()
    sha.update(string)
    return sha.hexdigest()


def gen_salt():
    """Create a salt to use with password encryption."""
    presalt = ''.join(random.choice(string.printable) for i in range(20))
    return sha512_hash_hex(presalt)


def encrypt_password(pw, pwsalt=None):
    """Encrypt a password with salted sha512.
    
    Arguments:
      * ``pw``: the password to encrypt
    
    Keyword arguments:
      * ``pwsalt``: the salt to use in password encryption; if not provided,
        a salt is automatically generated (a random string of 20 printable
        characters)
    
    Returns: a tuple consisting of:
      * the salt used in password encryption
      * the encrypted password, in hex representation
    
    """
    
    if pwsalt == None:
        pwsalt = gen_salt()
    return pwsalt, sha512_hash_hex(pwsalt + pw)


class ECVerifier(object):
    
    """Verify elliptic curve signatures.
    
    Methods:
      * ``__init__``: initialize the structure with a MetaAppInstance
      * ``verify``: verify a signature allegedly performed by our
        MetaAppInstance
    
    
    """
    
    def __init__(self, mai):
        """Initialize the structure with a MetaAppInstance.
        
        Arguments:
          * ``mai``: the MetaAppInstance whose public key is used to verify
            signatures
        
        """
        
        self.mai = mai
        self._ecs = []
        bio = BIO.MemoryBuffer(str(self.mai.pubkey_ec))
        self._ecs.append(EC.load_pub_key_bio(bio))
    
    def verify(self, datastring, sigfile):
        """Verify a signature allegedly performed by our MetaAppInstance."""
        digest = sha512_hash(datastring)
        sig = sigfile.read()
        return sum([bool(ec.verify_dsa_asn1(digest, sig))
                    for ec in self._ecs])
