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
from pylibad4.libad4 import ad_open, ad_close, ad_get_range_count, \
    ad_get_range_info, ad_discrete_in, ad_discrete_inv, ad_sample_to_float, \
    ad_discrete_in64, ad_discrete_out, ad_discrete_out64, \
    ad_discrete_outv, LibAD4Error
from pylibad4.types import AD_CHA_TYPE_ANALOG_IN, AD_RETURN_CODE_6, \
    AD_CHA_TYPE_ANALOG_OUT


TEST_DEVICE_NAME = 'memadfpusb'
INVALID_HANDLE = -1


class LibAD4TestCase(TestCase):

    def setUp(self):
        self.handle = ad_open(TEST_DEVICE_NAME)

    def tearDown(self):
        ad_close(self.handle)

    def test_connection_error(self):
        with self.assertRaises(IOError):
            ad_open('')

        with self.assertRaises(IOError):
            ad_close(INVALID_HANDLE)

    def test_range_info(self):
        # Check for range count
        range_count = ad_get_range_count(self.handle, AD_CHA_TYPE_ANALOG_IN)
        self.assertEqual(range_count, 1)

        # Get range info
        range_info = ad_get_range_info(
            self.handle, AD_CHA_TYPE_ANALOG_IN | 0x0001, 0)
        self.assertEqual(range_info.min, -5.12)
        self.assertEqual(range_info.max, 5.12)
        # self.assertEqual(range_info.unit, 'V')

    def test_range_info_error(self):

        # check range count error
        with self.assertRaises(LibAD4Error):
            ad_get_range_count(INVALID_HANDLE, AD_CHA_TYPE_ANALOG_IN)

        # check range info error
        with self.assertRaises(LibAD4Error):
            ad_get_range_info(INVALID_HANDLE, AD_CHA_TYPE_ANALOG_IN | 0x0001, 0)

    def test_discrete_in(self):

        # check for error code with invalid handle
        with self.assertRaises(LibAD4Error) as cm:
            ad_discrete_in(INVALID_HANDLE, 0, 0)
        self.assertEqual(cm.exception.error_code, AD_RETURN_CODE_6)

        # check if returned value is integer
        channel = AD_CHA_TYPE_ANALOG_IN | 0x0001
        data = ad_discrete_in(self.handle, channel, 0)
        self.assertIsInstance(data, int)

        # check sample to float
        value = ad_sample_to_float(self.handle, channel, 0, data)
        self.assertIsInstance(value, float)

        # check sample to float error
        with self.assertRaises(LibAD4Error):
            ad_sample_to_float(INVALID_HANDLE, channel, 0, data)

    def test_discrete_in64(self):
        # check if returned value is integer
        channel = AD_CHA_TYPE_ANALOG_IN | 0x0001
        data = ad_discrete_in64(self.handle, channel, 0)
        self.assertIsInstance(data, int)

        # check for error
        with self.assertRaises(LibAD4Error):
            ad_discrete_in64(INVALID_HANDLE, channel, 0)

    def test_discrete_inv(self):
        channels = [
            AD_CHA_TYPE_ANALOG_IN | 0x0001,
            AD_CHA_TYPE_ANALOG_IN | 0x0002,
        ]
        ranges = [0, 0]

        # check for error code with invalid handle
        with self.assertRaises(LibAD4Error) as cm:
            ad_discrete_inv(INVALID_HANDLE, channels, ranges)
        self.assertEqual(cm.exception.error_code, AD_RETURN_CODE_6)

        # check if returned value is integer
        data = ad_discrete_inv(self.handle, channels, ranges)
        self.assertEqual(len(data), 2)
        for x in data:
            self.assertIsInstance(x, int)

        # check for error if different array sizes
        ranges.append(0)
        with self.assertRaises(ValueError):
            data = ad_discrete_inv(self.handle, channels, ranges)

    def test_discrete_out(self):
        channel = AD_CHA_TYPE_ANALOG_OUT | 0x0001
        range_ = 0
        data = 0xffffffff

        ad_discrete_out(self.handle, channel, range_, data)

        # check for error
        with self.assertRaises(LibAD4Error):
            ad_discrete_out(INVALID_HANDLE, channel, range_, data)

    def test_discrete_out64(self):
        channel = AD_CHA_TYPE_ANALOG_OUT | 0x0001
        range_ = 0
        data = 0xffffffffffffffff

        ad_discrete_out64(self.handle, channel, range_, data)

        # check for error
        with self.assertRaises(LibAD4Error):
            ad_discrete_out64(INVALID_HANDLE, channel, range_, data)

    def test_discrete_outv(self):
        channels = [
            AD_CHA_TYPE_ANALOG_OUT | 0x0001,
            AD_CHA_TYPE_ANALOG_OUT | 0x0002,
        ]
        ranges = [0, 0]
        data = [0xffffffffffffffff, 0xffffffffffffffff]

        # check for error code with invalid handle
        with self.assertRaises(LibAD4Error) as cm:
            ad_discrete_outv(INVALID_HANDLE, channels, ranges, data)
        self.assertEqual(cm.exception.error_code, AD_RETURN_CODE_6)

        # check if returned value is integer
        data = ad_discrete_outv(self.handle, channels, ranges, data)

        # check for error if different array sizes
        ranges.append(0)
        with self.assertRaises(ValueError):
            data = ad_discrete_outv(self.handle, channels, ranges, data)


if __name__ == '__main__':
    unittest.main()
