#!-*- coding: utf-8 -*-
"""
:author: Stefan Lehmann
:email: stefan.st.lehmann@gmail.com
:created: 2016-10-10

"""
import os
import sys
from ctypes import CDLL, c_char_p, c_int32, c_uint32, byref, pointer, c_float
from .types import SADRangeInfo

LIB_NAME = 'libad4.dll'

encoding = sys.getdefaultencoding()

# Check for local library
basedir = os.path.dirname(os.path.abspath(__file__))
local_lib = os.path.join(basedir, LIB_NAME)

# Load libad4.dll
if os.path.isfile(local_lib):
    libad4_dll = CDLL(local_lib)
else:
    libad4_dll = CDLL(LIB_NAME)


class LibAD4Error(Exception):
    pass


def ad_open(name):
    """
    Open connection to a measurement system.

    :param str name: name of the device
    :return: device-handle for further function calls
    :rtype: int
    :raises IOError: if the connection couldn't be established

    Possible names for BMCM measurement devices are listed below:

    ====================== =================
    measurement device     name
    ====================== =================
    meM-AD                 memadusb
    meM-ADDA               memaddausb
    meM-ADf                memadfusb
    meM-ADfo               memadfpusb
    USB-AD16f              usbbase
    USB-AD14f              usbad14f
    USB-AD12f              usbad12f
    LAN-AD16f              lanbase:<ip-addr>
    ====================== =================

    Multiple devices can be addressed by adding the device number to the
    device name ('usbbase:0', 'usbbase:1').

    You can also use the serial number for addressing ('usbbase:@157').

    """
    ad_open = libad4_dll.ad_open
    ad_open.argtypes = [c_char_p]
    ad_open.restype = c_int32

    handle = ad_open(bytes(name, encoding))

    if handle == -1:
        raise IOError('Could not connect to device {}'.format(name))

    return handle


def ad_close(handle):
    """
    Close the connection to a measurement system.

    :param int handle: device-handle
    :raises IOError: if an error occured during disconnecting device,
                     contains the error number
    """
    ad_close = libad4_dll.ad_close
    ad_close.argtypes = [c_int32]
    ad_close.restype = c_int32

    res = ad_close(handle)

    if res:
        raise IOError(
            'Error while disconnecting device (error number {})'.format(res))


def ad_get_range_count(handle, channel):
    """
    Return the count of the measurement ranges of a channel.

    :param int handle: device-handle
    :param int channel: channel number
    :rtype: int
    :return: count of measurement ranges

    """
    ad_get_range_count = libad4_dll.ad_get_range_count
    ad_get_range_count.argtypes = [c_int32, c_int32]
    ad_get_range_count.restype = c_int32
    count = c_int32()

    return_code = ad_get_range_count(handle, channel, byref(count))

    if return_code:
        raise LibAD4Error(
            'Error calling function ad_get_range_count({handle}, {channel}), '
            'returncode: {return_code}'.format(handle=handle, channel=channel,
                                               return_code=return_code)
        )
    return count.value


def ad_get_range_info(handle, channel, range_):
    """
    Get information about the range of a channel.

    :param int handle: device-handle
    :param int channel: channel number
    :rtype: SADRangeInfo
    :return: range information object

    """
    ad_get_range_info = libad4_dll.ad_get_range_info
    ad_get_range_info.argtypes = [c_int32, c_int32, c_int32]
    ad_get_range_info.restype = c_int32
    st_ad_range_info = SADRangeInfo()

    return_code = ad_get_range_info(handle, channel, range_,
                                    byref(st_ad_range_info))

    if return_code:
        raise LibAD4Error(
            'Error calling function ad_get_range_info({handle}, {channel}, {range_}), '
            'returncode: {return_code}'.format(
                handle=handle, channel=channel, range_=range_,
                return_code=return_code
            )
        )

    return st_ad_range_info


def ad_discrete_in(handle, channel, range_):
    """
    Read a single value of a given channel.

    :param int handle: device-handle
    :param int channel: channel number
    :param int range_: range number
    :rtype: int

    """
    ad_discrete_in = libad4_dll.ad_discrete_in
    ad_discrete_in.argtypes = [c_int32, c_int32, c_int32]
    ad_discrete_in.restype = c_int32
    value = c_uint32()

    return_code = ad_discrete_in(handle, channel, range_, byref(value))

    if return_code:
        raise LibAD4Error(
            'Error calling function ad_discrete_in({handle}, {channel}, {range_}), '
            'returncode: {return_code}'.format(
                handle=handle, channel=channel, range_=range_,
                return_code=return_code
            )
        )

    return value.value


def ad_sample_to_float(handle, channel, range_, data):
    """
    Convert a measurement value in the corresponding voltage value.

    :param int handle: device-handle
    :param int channel: channel number
    :param int range_: range number
    :rtype: float

    """
    ad_sample_to_float = libad4_dll.ad_sample_to_float
    ad_sample_to_float.argtypes = [c_int32, c_int32, c_int32, c_uint32]
    ad_sample_to_float.restype = c_int32
    value = c_float()

    return_code = ad_sample_to_float(
        handle, channel, range_, data, byref(value))

    if return_code:
        raise LibAD4Error(
            'Error calling function ad_sample_to_float('
            '{handle}, {channel}, {range_}), returncode: {return_code}'
            .format(
                handle=handle, channel=channel, range_=range_,
                return_code=return_code
            )
        )

    return value.value


if __name__ == '__main__':
    from .types import AD_CHA_TYPE_ANALOG_IN
    channel = AD_CHA_TYPE_ANALOG_IN | 0x0001
    range_ = 0

    handle = ad_open('memadfpusb')
    data = ad_discrete_in(handle, channel, range_)
    value = ad_sample_to_float(handle, channel, range_, data)
    print(value)
    ad_close(handle)
