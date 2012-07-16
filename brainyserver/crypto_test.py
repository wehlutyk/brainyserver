#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the crypto module."""


import unittest
from hashlib import sha512

import brainyserver.crypto as crypto


class PasswordTestCase(unittest.TestCase):
    
    def setUp(self):
        self.pw1 = 'testpassword'
        self.pw2 = 'anotherpassword'
        self.salt = 'somesalt'
        
        self.string1 = 'test string'
        self.string2 = 'another string'
        
        self.sha = sha512()
    
    def test_sha512_hash(self):
        self.sha.update(self.string1)
        h1 = self.sha.digest()
        
        assert crypto.sha512_hash(self.string2) != h1
        assert crypto.sha512_hash(self.string1) == h1
    
    def test_sha512_hash_hex(self):
        self.sha.update(self.string1)
        h1hex = self.sha.hexdigest()
        
        assert crypto.sha512_hash_hex(self.string2) != h1hex
        assert crypto.sha512_hash_hex(self.string1) == h1hex
    
    def test_gen_salt(self):
        assert len(crypto.gen_salt()) == 128
    
    def test_encrypt_password_with_salt(self):
        self.sha.update(self.salt + self.pw1)
        enc1 = self.sha.hexdigest()
        
        assert crypto.encrypt_password(self.pw2, self.salt)[1] != enc1
        assert (crypto.encrypt_password(self.pw1, self.salt)
                == (self.salt, enc1))
    
    def test_encrypt_password_no_salt1(self):
        salt, enc1_test = crypto.encrypt_password(self.pw1)
        assert crypto.encrypt_password(self.pw1, salt) == (salt, enc1_test)
        
        self.sha.update(salt + self.pw1)
        enc1 = self.sha.hexdigest()
        assert enc1_test == enc1
    
    def test_encrypt_password_no_salt2(self):
        salt, enc1_test = crypto.encrypt_password(self.pw1)
        self.sha.update(salt + self.pw2)
        enc2 = self.sha.hexdigest()
        
        assert enc1_test != enc2


suite = unittest.defaultTestLoader.loadTestsFromTestCase(PasswordTestCase)


if __name__ == '__main__':
    unittest.main()
