#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Discover and run all tests."""


import unittest


if __name__ == '__main__':
    suite_all_tests =  unittest.defaultTestLoader.discover('.', '*_test.py')
    unittest.TextTestRunner(verbosity=2).run(suite_all_tests)
