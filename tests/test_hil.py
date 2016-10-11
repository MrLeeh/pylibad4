#!-*- coding: utf-8 -*-
"""
:author: Stefan Lehmann
:email: stefan.st.lehmann@gmail.com
:created: 2016-10-10

This is a hardware-in-the-loop test and should only be run with a connected
measurement device.

"""
import unittest
from unittest import TestCase
from pylibad4.libad4 import ad_open, ad_close


TEST_DEVICE_NAME = 'memadfpusb'


class LibAD4TestCase(TestCase):

    def setUp(self):
        self.handle = ad_open(TEST_DEVICE_NAME)

    def tearDown(self):
        ad_close(self.handle)

    def test_nothing(self):
        pass


if __name__ == '__main__':
    unittest.main()