#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the crypto module."""


import tempfile
import unittest
from hashlib import sha512

from pymongo import Connection
from M2Crypto import EC, BIO

from brainyserver import create_app
from brainyserver.mongodb import MetaAppInstance
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


class ECVerifyerTestCase(unittest.TestCase):
    
    testdata1 = 'test data to sign'
    testdata2 = 'other data'
    test_mai_id = 'testmai'
    ec_name = EC.NID_secp112r1
    
    def setUp(self):
        self.app = create_app('testing')
        
        self.ec1 = EC.gen_params(self.ec_name)
        self.ec1.gen_key()
        bio1 = BIO.MemoryBuffer()
        self.ec1.save_pub_key_bio(bio1)
        
        self.mai = MetaAppInstance(mai_id=self.test_mai_id,
                                   pubkey_ec=bio1.getvalue())
        self.mai.save()
        
        self.ec2 = EC.gen_params(self.ec_name)
        self.ec2.gen_key()
        
        self.verifyer = crypto.ECVerifier(self.mai)
        
        self.sha = sha512()
        self.temp = tempfile.TemporaryFile()
    
    def tearDown(self):
        mongoco = Connection()
        mongoco.drop_database(self.app.config['MONGODB_DB'])
        self.temp.close()
    
    def test_signature(self):
        self.sha.update(self.testdata1)
        sig1 = self.ec1.sign_dsa_asn1(self.sha.digest())
        self.temp.write(sig1)
        
        assert self.verifyer.verify(self.testdata1, self.temp) == True
        assert self.verifyer.verify(self.testdata2, self.temp) == False
    
    def test_other_signature(self):
        self.sha.update(self.testdata1)
        sig2 = self.ec2.sign_dsa_asn1(self.sha.digest())
        self.temp.write(sig2)
        
        assert self.verifyer.verify(self.testdata1, self.temp) == False


if __name__ == '__main__':
    unittest.main()
