#!-*- coding: utf-8 -*-
"""
:author: Stefan Lehmann
:email: stefan.st.lehmann@gmail.com
:created: 2016-10-11

"""

from ctypes import Structure, c_double, c_char, c_int


"""
High order byte defines channel type,
low orer 24bits define channel id

"""
AD_CHA_TYPE_MASK            = 0xff000000
AD_CHA_TYPE_ANALOG_IN       = 0x01000000
AD_CHA_TYPE_ANALOG_OUT      = 0x02000000
AD_CHA_TYPE_DIGITAL_IO      = 0x03000000
AD_CHA_TYPE_SYNC            = 0x05000000
AD_CHA_TYPE_ROUTE           = 0x06000000
AD_CHA_TYPE_CAN             = 0x07000000
AD_CHA_TYPE_COUNTER         = 0x08000000
AD_CHA_TYPE_ANALOG_COUNTER  = 0x09000000

AD_RETURN_CODE_OK = 0
AD_RETURN_CODE_6 = 6
AD_RETURN_CODE_87 = 87


class SADRangeInfo(Structure):

    _fields_ = [
        ('min', c_double),
        ('max', c_double),
        ('res', c_double),
        ('bps', c_int),
        ('unit', c_char * 24)
    ]
