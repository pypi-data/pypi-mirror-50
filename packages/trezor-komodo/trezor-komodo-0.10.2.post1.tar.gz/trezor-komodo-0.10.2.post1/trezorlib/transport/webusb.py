# This file is part of the Trezor project.
#
# Copyright (C) 2012-2018 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import time
import os
import atexit
import usb1
import sys

from ..protocol_v1 import ProtocolV1
from ..protocol_v2 import ProtocolV2
from . import Transport, TransportException

DEV_TREZOR1 = (0x534c, 0x0001)
DEV_TREZOR2 = (0x1209, 0x53c1)
DEV_TREZOR2_BL = (0x1209, 0x53c0)

INTERFACE = 0
ENDPOINT = 1
DEBUG_INTERFACE = 1
DEBUG_ENDPOINT = 2


class WebUsbHandle:

    def __init__(self, device):
        self.device = device
        self.count = 0
        self.handle = None

    def open(self, interface):
        if self.count == 0:
            self.handle = self.device.open()
            if self.handle is None:
                if sys.platform.startswith('linux'):
                    args = ('Do you have udev rules installed? https://github.com/trezor/trezor-common/blob/master/udev/51-trezor.rules', )
                else:
                    args = ()
                raise IOError('Cannot open device', *args)
            self.handle.claimInterface(interface)
            self.count += 1

    def close(self, interface):
        if self.count == 1:
            self.handle.releaseInterface(interface)
            self.handle.close()
        if self.count > 0:
            self.count -= 1


class WebUsbTransport(Transport):
    '''
    WebUsbTransport implements transport over WebUSB interface.
    '''

    PATH_PREFIX = 'webusb'
    context = None

    def __init__(self, device, protocol=None, handle=None, debug=False):
        super(WebUsbTransport, self).__init__()

        if handle is None:
            handle = WebUsbHandle(device)

        if protocol is None:
            # force_v1 = os.environ.get('TREZOR_TRANSPORT_V1', '0')
            force_v1 = True

            if is_trezor2(device) and not int(force_v1):
                protocol = ProtocolV2()
            else:
                protocol = ProtocolV1()

        self.device = device
        self.protocol = protocol
        self.handle = handle
        self.debug = debug

    def get_path(self):
        return "%s:%s" % (self.PATH_PREFIX, dev_to_str(self.device))

    @classmethod
    def enumerate(cls):
        if cls.context is None:
            cls.context = usb1.USBContext()
            cls.context.open()
            atexit.register(cls.context.close)
        devices = []
        for dev in cls.context.getDeviceIterator(skip_on_error=True):
            if not (is_trezor1(dev) or is_trezor2(dev) or is_trezor2_bl(dev)):
                continue
            if not is_vendor_class(dev):
                continue
            try:
                # workaround for issue #223:
                # on certain combinations of Windows USB drivers and libusb versions,
                # Trezor is returned twice (possibly because Windows know it as both
                # a HID and a WebUSB device), and one of the returned devices is
                # non-functional.
                dev.getProduct()
                devices.append(WebUsbTransport(dev))
            except usb1.USBErrorNotSupported:
                pass
        return devices

    def find_debug(self):
        if isinstance(self.protocol, ProtocolV2):
            # TODO test this
            # For v2 protocol, lets use the same WebUSB interface, but with a different session
            protocol = ProtocolV2()
            debug = WebUsbTransport(self.device, protocol, self.handle)
            return debug
        if isinstance(self.protocol, ProtocolV1):
            # For v1 protocol, find debug USB interface for the same serial number
            protocol = ProtocolV1()
            debug = WebUsbTransport(self.device, protocol, None, True)
            return debug
        raise TransportException('Debug WebUSB device not found')

    def open(self):
        interface = DEBUG_INTERFACE if self.debug else INTERFACE
        self.handle.open(interface)
        self.protocol.session_begin(self)

    def close(self):
        interface = DEBUG_INTERFACE if self.debug else INTERFACE
        self.protocol.session_end(self)
        self.handle.close(interface)

    def read(self):
        return self.protocol.read(self)

    def write(self, msg):
        return self.protocol.write(self, msg)

    def write_chunk(self, chunk):
        endpoint = DEBUG_ENDPOINT if self.debug else ENDPOINT
        if len(chunk) != 64:
            raise TransportException('Unexpected chunk size: %d' % len(chunk))
        self.handle.handle.interruptWrite(endpoint, chunk)

    def read_chunk(self):
        endpoint = DEBUG_ENDPOINT if self.debug else ENDPOINT
        endpoint = 0x80 | endpoint
        while True:
            chunk = self.handle.handle.interruptRead(endpoint, 64)
            if chunk:
                break
            else:
                time.sleep(0.001)
        if len(chunk) != 64:
            raise TransportException('Unexpected chunk size: %d' % len(chunk))
        return bytearray(chunk)


def is_trezor1(dev):
    return (dev.getVendorID(), dev.getProductID()) == DEV_TREZOR1


def is_trezor2(dev):
    return (dev.getVendorID(), dev.getProductID()) == DEV_TREZOR2


def is_trezor2_bl(dev):
    return (dev.getVendorID(), dev.getProductID()) == DEV_TREZOR2_BL


def is_vendor_class(dev):
    configurationId = 0
    altSettingId = 0
    return dev[configurationId][INTERFACE][altSettingId].getClass() == usb1.libusb1.LIBUSB_CLASS_VENDOR_SPEC


def dev_to_str(dev):
    return ':'.join(str(x) for x in ['%03i' % (dev.getBusNumber(), )] + dev.getPortNumberList())


TRANSPORT = WebUsbTransport
