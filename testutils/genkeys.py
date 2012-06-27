#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate ECDSA keys and export them."""


import os
from argparse import ArgumentParser

from M2Crypto import EC


class Genkeys(object):

    def __init__(self):
        self._ec = EC.gen_params(EC.NID_X9_62_c2tnb431r1)
        self._ec.gen_key()
        parser = ArgumentParser(description=('Generate ECDSA keys and '
                                             'export them'))
        parser.add_argument('--pub', nargs=1, default='testkey.pub',
                            help=('Destination public key file. Defaults to '
                                  "'testkey.pub'."))
        parser.add_argument('--priv', nargs=1, default='testkey.key',
                            help=('Destination private key file. Defaults to '
                                  "'testkey.key'."))
        self.args = parser.parse_args()
    
    def save_keys(self):
        
        if os.path.exists(self.args.pub):
            print "Public key file '{}' already exists!".format(self.args.pub)
            print "Aborting."
            return
        
        if os.path.exists(self.args.priv):
            print "Private key file '{}' already exists!".format(self.args.priv)
            print "Aborting."
            return
        
        print "Saving public key file to '{}'.".format(self.args.pub)
        self._ec.save_pub_key(self.args.pub)
        
        print "Saving private key file to '{}'.".format(self.args.priv)
        self._ec.save_key(self.args.priv, cipher=None)


if __name__ == '__main__':
    gk = Genkeys()
    gk.save_keys()
