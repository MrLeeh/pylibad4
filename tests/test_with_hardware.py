#!-*- coding: utf-8 -*-
"""
:author: Stefan Lehmann
:email: stefan.st.lehmann@gmail.com
:created: 2016-10-10

This is a hardware-in-the-loop test and should only be run with a connected
measurement device.

"""
import unittest
from unittest import TestCase, skipUnless
from pylibad4.libad4 import ad_open, ad_close, ad_get_range_count, \
    ad_get_range_info, ad_discrete_in, ad_discrete_inv, ad_sample_to_float, \
    ad_discrete_in64, ad_discrete_out, ad_discrete_out64, \
    ad_discrete_outv, ad_sample_to_float64, ad_float_to_sample, \
    ad_float_to_sample64, ad_analog_in, ad_analog_out, \
    ad_digital_in, ad_digital_out, ad_set_digital_line, ad_get_digital_line, \
    ad_get_line_direction, ad_set_line_direction, ad_get_version, \
    ad_get_drv_version, ad_get_product_info, LibAD4Error
from pylibad4.types import AD_CHA_TYPE_ANALOG_IN, AD_RETURN_CODE_6, \
    AD_CHA_TYPE_ANALOG_OUT, AD_CHA_TYPE_DIGITAL_IO, SADProductInfo


TEST_DEVICE_NAME = 'memadfpusb'
INVALID_HANDLE = -1


def device_connected():
    try:
        handle = ad_open(TEST_DEVICE_NAME)
        ad_close(handle)
        return True
    except:
        return False


@skipUnless(device_connected(),
            'Skipping hardware test. Device {} not connected.'
            .format(TEST_DEVICE_NAME))
class LibAD4TestCase(TestCase):

    def setUp(self):
        self.handle = ad_open(TEST_DEVICE_NAME)

    def tearDown(self):
        ad_close(self.handle)

    def test_connection_error(self):
        with self.assertRaises(LibAD4Error):
            ad_open('')

        with self.assertRaises(LibAD4Error):
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

        # check sample to float64
        value = ad_sample_to_float64(self.handle, channel, 0, data)
        self.assertIsInstance(value, float)

        # check for error
        with self.assertRaises(LibAD4Error):
            ad_discrete_in64(INVALID_HANDLE, channel, 0)

        # check sample to float64 error
        with self.assertRaises(LibAD4Error):
            ad_sample_to_float64(INVALID_HANDLE, channel, 0, data)

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
        value = 5.0

        # check ad_float_to_sample
        data = ad_float_to_sample(self.handle, channel, range_, value)
        self.assertIsInstance(data, int)

        # check ad_discrete_out
        ad_discrete_out(self.handle, channel, range_, data)

        # check for error
        with self.assertRaises(LibAD4Error):
            ad_discrete_out(INVALID_HANDLE, channel, range_, data)

        # check ad_float_to_sample for error
        with self.assertRaises(LibAD4Error):
            ad_float_to_sample(INVALID_HANDLE, channel, range_, value)

    def test_discrete_out64(self):
        channel = AD_CHA_TYPE_ANALOG_OUT | 0x0001
        range_ = 0
        value = 5.0

        # check ad_float_to_sample64
        data = ad_float_to_sample64(self.handle, channel, range_, value)
        self.assertIsInstance(data, int)

        # check ad_discrete_out64
        ad_discrete_out64(self.handle, channel, range_, data)

        # check for error
        with self.assertRaises(LibAD4Error):
            ad_discrete_out64(INVALID_HANDLE, channel, range_, data)

        # check ad_float_to_sample64 for error
        with self.assertRaises(LibAD4Error):
            ad_float_to_sample64(INVALID_HANDLE, channel, range_, value)

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

    def test_analog_in(self):
        channel = 1
        range_ = 0

        # check ad_analog_in
        value = ad_analog_in(self.handle, channel, range_)
        self.assertIsInstance(value, float)

        # check ad_analog_in for error
        with self.assertRaises(LibAD4Error):
            ad_analog_in(INVALID_HANDLE, channel, range_)

    def test_analog_out(self):
        channel = 1
        range_ = 0
        value = 5.0

        # check ad_analog_out
        ad_analog_out(self.handle, channel, range_, value)

        # check ad_analog_out error
        with self.assertRaises(LibAD4Error):
            ad_analog_out(INVALID_HANDLE, channel, range_, value)

    def test_digital_in(self):
        value = ad_digital_in(self.handle, 0)
        self.assertIsInstance(value, int)

        with self.assertRaises(LibAD4Error):
            ad_digital_in(INVALID_HANDLE, 0)

    def test_digital_out(self):
        ad_digital_out(self.handle, 0, 0xf)

        with self.assertRaises(LibAD4Error):
            ad_digital_out(INVALID_HANDLE, 0, 0xf)

    def test_set_digital_line(self):
        ad_set_digital_line(self.handle, 0, 0, True)

        with self.assertRaises(LibAD4Error):
            ad_set_digital_line(INVALID_HANDLE, 0, 0, True)

    def test_get_digital_line(self):
        flag = ad_get_digital_line(self.handle, 0, 0)
        self.assertIsInstance(flag, bool)

        with self.assertRaises(LibAD4Error):
            ad_get_digital_line(INVALID_HANDLE, 0, 0)

    def test_set_line_direction(self):
        mask = 0xFFFF
        channel = AD_CHA_TYPE_DIGITAL_IO | 0

        # set line direction: all in
        ad_set_line_direction(self.handle, channel, mask)

        # check error for invalid setter
        with self.assertRaises(LibAD4Error):
            ad_set_line_direction(INVALID_HANDLE, channel, mask)

    def test_get_line_direction(self):
        channel = AD_CHA_TYPE_DIGITAL_IO | 0

        # get line direction
        mask = ad_get_line_direction(self.handle, channel)

        # check if both masks are equal
        self.assertIsInstance(mask, int)

        # check error for invalid getter
        with self.assertRaises(LibAD4Error):
            ad_get_line_direction(INVALID_HANDLE, channel)

    def test_ad_get_version(self):
        self.assertIsInstance(ad_get_version(), int)

    def test_get_drv_version(self):
        drv_version = ad_get_drv_version(self.handle)
        self.assertIsInstance(drv_version, int)

        with self.assertRaises(LibAD4Error):
            ad_get_drv_version(INVALID_HANDLE)

    def test_get_product_info(self):
        product_info = ad_get_product_info(self.handle)
        self.assertIsInstance(product_info, SADProductInfo)

        with self.assertRaises(LibAD4Error):
            ad_get_product_info(INVALID_HANDLE)


if __name__ == '__main__':
    unittest.main()
