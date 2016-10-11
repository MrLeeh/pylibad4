#!-*- coding: utf-8 -*-
"""
:author: Stefan Lehmann
:email: stefan.st.lehmann@gmail.com
:created: 2016-10-10

"""
import os
import sys
from ctypes import CDLL, c_char_p, c_int32

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


if __name__ == '__main__':
    ad_open('memadfpusb')
