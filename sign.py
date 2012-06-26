#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Sign a file with a given ECDSA key."""


from argparse import ArgumentParser
from hashlib import sha512

import bsontools
from M2Crypto.EC import load_key


class ECSigner(object):
    
    def __init__(self):
        parser = ArgumentParser(description=('Sign a file with a given ECDSA '
                                             'key'))
        parser.add_argument('--priv', nargs=1, default='testkey.key',
                            help=('Source private key file. Defaults to '
                                  "'testkey.key'."))
        parser.add_argument('files', nargs='+', help='Files to sign.')
        self.args = parser.parse_args()
        self._ec = load_key(self.args.priv)
    
    def digest(self, datastring):
        sha = sha512()
        sha.update(datastring)
        return sha.digest()
    
    def sigtuple_to_bson(self, (r, s)):
        return bsontools.dumps({'r': r, 's': s})
    
    def sign(self, datastring):
        digest = self.digest(datastring)
        return self._ec.sign_dsa(digest)
    
    def sign_all(self):
        for fname in self.args.files:
            with open(fname, 'rb') as f, open(fname + '.sig', 'wb') as sigf:
                b = self.sigtuple_to_bson(self.sign(f.read()))
                sigf.write(b)


if __name__ == '__main__':
    ecs = ECSigner()
    ecs.sign_all()
