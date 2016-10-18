#!-*- coding: utf-8 -*-
"""
:author: Stefan Lehmann
:email: stefan.st.lehmann@gmail.com
:created: 2016-10-10

"""
import os
import sys
from ctypes import CDLL, c_char_p, c_int32, c_uint32, byref, c_float, \
    c_uint64, c_double
from .types import SADRangeInfo

LIB_NAME = 'libad4.dll'

encoding = sys.getdefaultencoding()

# Check for local library
basedir = os.path.dirname(os.path.abspath(__file__))
local_lib = os.path.join(basedir, LIB_NAME)

# Load libad4.dll
if os.path.isfile(local_lib):
    libad4_dll = CDLL(local_lib)
else:  # pragma: no cover
    libad4_dll = CDLL(LIB_NAME)


class LibAD4Error(Exception):

    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code


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
    :raises IOError: if an error occured, error_code contains the error number
                     return by libad4.dll

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
                                               return_code=return_code),
            return_code
        )

    return count.value


def ad_get_range_info(handle, channel, range_):
    """
    Get information about the range of a channel.

    :param int handle: device-handle
    :param int channel: channel number
    :rtype: SADRangeInfo
    :return: range information object
    :raises IOError: if an error occured, error_code contains the error number
                     return by libad4.dll

    """
    ad_get_range_info = libad4_dll.ad_get_range_info
    ad_get_range_info.argtypes = [c_int32, c_int32, c_int32]
    ad_get_range_info.restype = c_int32
    st_ad_range_info = SADRangeInfo()

    return_code = ad_get_range_info(handle, channel, range_,
                                    byref(st_ad_range_info))

    if return_code:
        raise LibAD4Error(
            'Error calling function ad_get_range_info'
            '({handle}, {channel}, {range_}), returncode: {return_code}'
            .format(
                handle=handle, channel=channel, range_=range_,
                return_code=return_code
            ), return_code
        )

    return st_ad_range_info


def ad_discrete_in(handle, channel, range_):
    """
    Read a single value of a given channel.

    :param int handle: device-handle
    :param int channel: channel number
    :param int range_: range number
    :rtype: int
    :raises IOError: if an error occured, error_code contains the error number
                     return by libad4.dll

    """
    ad_discrete_in = libad4_dll.ad_discrete_in
    ad_discrete_in.argtypes = [c_int32, c_int32, c_int32]
    ad_discrete_in.restype = c_int32
    data = c_uint32()

    return_code = ad_discrete_in(handle, channel, range_, byref(data))

    if return_code:
        raise LibAD4Error(
            'Error calling function ad_discrete_in({handle}, {channel}, {range_}), '
            'returncode: {return_code}'.format(
                handle=handle, channel=channel, range_=range_,
                return_code=return_code
            ), return_code
        )

    return data.value


def ad_discrete_in64(handle, channel, range_):
    """
    Read a single value of a given channel with 64bit resolution.

    :param int handle: device-handle
    :param int channel: channel number
    :param int range_: range number
    :rtype: int
    :raises IOError: if an error occured, error_code contains the error number
                     return by libad4.dll

    """
    ad_discrete_in64 = libad4_dll.ad_discrete_in64
    ad_discrete_in64.argtypes = [c_int32, c_int32, c_uint64]
    ad_discrete_in64.restype = c_int32
    data = c_uint64()

    return_code = ad_discrete_in64(handle, channel, range_, byref(data))

    if return_code:
        raise LibAD4Error(
            'Error calling function ad_discrete_in64({handle}, {channel}, {range_}), '
            'returncode: {return_code}'.format(
                handle=handle, channel=channel, range_=range_,
                return_code=return_code
            ), return_code
        )

    return data.value


def ad_discrete_inv(handle, channel_list, range_list):
    """
    :raises IOError: if an error occured, error_code contains the error number
                     return by libad4.dll

    """
    ad_discrete_inv = libad4_dll.ad_discrete_inv

    # Check for same length of channel_list and range_list
    if len(channel_list) != len(range_list):
        raise ValueError('range_list and channel_list need to have the same '
                         'length')

    # Prepare function parameters
    count = len(channel_list)
    int32_array = (c_int32 * count)

    ad_discrete_inv.argtypes = [c_int32, c_int32, int32_array, int32_array]
    ad_discrete_inv.restype = c_int32
    data = (c_uint64 * count)()

    # call c-function
    return_code = ad_discrete_inv(
        handle, count, int32_array(*channel_list),
        int32_array(*range_list), data
    )

    if return_code:
        raise LibAD4Error(
            'Error calling function ad_discrete_inv('
            '{handle}, {count}, {channel_list}, {range_list}), '
            'returncode: {return_code}'.format(
                handle=handle, count=count, channel_list=channel_list,
                range_list=range_list, return_code=return_code
            ), return_code
        )

    return [x for x in data]


def ad_discrete_out(handle, channel, range_, data):
    """
    Set an output to the given data value.

    :param int handle: device-handle
    :param int channel: channel number
    :param int range_: range number
    :param int data: data value
    :raises IOError: if an error occured, error_code contains the error number
                     return by libad4.dll

    For analog outputs 0x00000000 stands for the lowest output voltage (e.g. 0V)
    and 0x10000000 stands for the highest output voltage (e.g. 10V). As it is
    32bit the maximum value of 0xffffffff must not be exceeded.

    Use ad_float_to_sample() to translate a float value in a data value for
    usage with ad_discrete_out. You can use the helper function ad_analog_out()
    for direct usage with voltage values.

    """
    ad_discrete_out = libad4_dll.ad_discrete_out
    ad_discrete_out.argtypes = [c_int32, c_int32, c_int32, c_uint32]
    ad_discrete_out.restype = c_int32

    return_code = ad_discrete_out(handle, channel, range_, data)

    if return_code:
        raise LibAD4Error(
            'Error calling function ad_discrete_out('
            '{handle}, {channel}, {range_}, {data}), returncode: {return_code}'
            .format(
                handle=handle, channel=channel, range_=range_,
                data=data, return_code=return_code
            ), return_code
        )


def ad_discrete_out64(handle, channel, range_, data):
    """
    Set an output to the given data value. The full 64-bit resolution provided
    by this function can only be used by special 64-bit measurement systems.

    :param int handle: device-handle
    :param int channel: channel number
    :param int range_: range number
    :param int data: data value
    :raises IOError: if an error occured, error_code contains the error number
                     return by libad4.dll

    For analog outputs 0x0000000000000000 stands for the lowest output voltage
    (e.g. 0V) and 0x1000000000000000 stands for the highest output voltage
    (e.g. 10V). As it is 32bit the maximum value of 0xffffffffffffffff must
    not be exceeded.

    Use ad_float_to_sample64() to translate a float value in a data value for
    usage with ad_discrete_out. You can use the helper function ad_analog_out()
    for direct usage with voltage values.

    """
    ad_discrete_out = libad4_dll.ad_discrete_out
    ad_discrete_out.argtypes = [c_int32, c_int32, c_uint64, c_uint64]
    ad_discrete_out.restype = c_int32

    return_code = ad_discrete_out(handle, channel, range_, data)

    if return_code:
        raise LibAD4Error(
            'Error calling function ad_discrete_out64('
            '{handle}, {channel}, {range_}, {data}), returncode: {return_code}'
            .format(
                handle=handle, channel=channel, range_=range_,
                data=data, return_code=return_code
            ), return_code
        )


def ad_discrete_outv(handle, channel_list, range_list, data_list):
    """
    Set multiple outputs at once. Analog and digital outputs can be mixed.
    Despite the channel numbers the ranges for each channel has to be given.
    In contrast to ad_discrete_out() and ad_discrete_out64() the channel
    numbers, ranges and data for ad_discrete_outv() are given as lists. All
    lists need to have the same length.

    The field data need to be set according to ad_discrete_out64.

    :param int handle: device-handle
    :param [int] channel_list: list of channels (analog and digital)
    :param [int] range_list: list of the used range numbers
    :param [int] data_list: list of data values to write to the outputs

    :raises IOError: if an error occured, error_code contains the error number
                     return by libad4.dll


    """
    ad_discrete_outv = libad4_dll.ad_discrete_outv

    # Check for same length of channel_list and range_list
    if len(channel_list) != len(range_list):
        raise ValueError('range_list and channel_list need to have the same '
                         'length')

    # prepare the function parameters
    count = len(channel_list)
    int32_array = (c_int32 * count)
    uint64_array = (c_uint64 * count)

    ad_discrete_outv.argtypes = [c_int32, c_int32, int32_array, uint64_array,
                                 uint64_array]
    ad_discrete_outv.restype = c_int32

    return_code = ad_discrete_outv(
        handle, count, int32_array(*channel_list), uint64_array(*range_list),
        uint64_array(*data_list)
    )

    if return_code:
        raise LibAD4Error(
            'Error calling function ad_discrete_outv('
            '{handle}, {count}, {channel_list}, {range_list}, {data_list}), '
            'returncode: {return_code}'.format(
                handle=handle, count=count, channel_list=channel_list,
                range_list=range_list, return_code=return_code,
                data_list=data_list
            ), return_code
        )


def ad_sample_to_float(handle, channel, range_, data):
    """
    Convert a measurement value in the corresponding voltage value.

    :param int handle: device-handle
    :param int channel: channel number
    :param int range_: range number
    :param int data: measurement data
    :rtype: float

    """
    ad_sample_to_float = libad4_dll.ad_sample_to_float
    ad_sample_to_float.argtypes = [c_int32, c_int32, c_int32, c_uint32]
    ad_sample_to_float.restype = c_int32
    float_data = c_float()

    return_code = ad_sample_to_float(
        handle, channel, range_, data, byref(float_data))

    if return_code:
        raise LibAD4Error(
            'Error calling function ad_sample_to_float('
            '{handle}, {channel}, {range_}), returncode: {return_code}'
            .format(
                handle=handle, channel=channel, range_=range_,
                return_code=return_code
            ), return_code
        )

    return float_data.value


def ad_sample_to_float64(handle, channel, range_, data):
    """
    Convert a measurement value in the corresponding voltage value.

    :param int handle: device-handle
    :param int channel: channel number
    :param int range_: range number
    :param int data: measurement data
    :rtype: float

    """
    ad_sample_to_float64 = libad4_dll.ad_sample_to_float64
    ad_sample_to_float64.argtypes = [c_int32, c_int32, c_uint64, c_uint64]
    ad_sample_to_float64.restype = c_int32
    double_data = c_double()

    return_code = ad_sample_to_float64(
        handle, channel, range_, data, byref(double_data))

    if return_code:
        raise LibAD4Error(
            'Error calling function ad_sample_to_float64('
            '{handle}, {channel}, {range_}), returncode: {return_code}'
            .format(
                handle=handle, channel=channel, range_=range_,
                return_code=return_code
            ), return_code
        )

    return double_data.value


if __name__ == '__main__':  # pragma: no cover
    from .types import AD_CHA_TYPE_ANALOG_IN
    channels = [
        AD_CHA_TYPE_ANALOG_IN | 0x0001,
        AD_CHA_TYPE_ANALOG_IN | 0x0002
    ]
    ranges = [0, 0]

    handle = ad_open('memadfpusb')
    data = ad_discrete_inv(handle, channels, ranges)
    print(data)
    ad_close(handle)
