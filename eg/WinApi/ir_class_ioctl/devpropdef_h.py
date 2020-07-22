# -*- coding: utf-8 -*-
import ctypes
from ctypes.wintypes import ULONG
from guiddef_h import GUID, DEFINE_GUID


POINTER = ctypes.POINTER
DEVPROPTYPE = ULONG
PDEVPROPTYPE = POINTER(ULONG)

DEVPROPGUID = GUID
PDEVPROPGUID = POINTER(GUID)
DEVPROPID = ULONG
PDEVPROPID = POINTER(ULONG)


class DEVPROPKEY(ctypes.Structure):
    _fields_ = [
        ('fmtid', DEVPROPGUID),
        ('pid', ULONG),
    ]


PDEVPROPKEY = POINTER(DEVPROPKEY)


def DEFINE_DEVPROPKEY(l, w1, w2, b1, b2, b3, b4, b5, b6, b7, b8, pid):
    return DEVPROPKEY(
        DEFINE_GUID(l, w1, w2, b1, b2, b3, b4, b5, b6, b7, b8),
        pid
    )


DEVPROP_TYPEMOD_LIST = 0x00002000
DEVPROP_TYPE_STRING = 0x00000012
DEVPROP_TYPE_STRING_LIST = DEVPROP_TYPE_STRING | DEVPROP_TYPEMOD_LIST

# DEVPROP_TYPE_STRING
DEVPKEY_Device_BusReportedDeviceDesc = DEFINE_DEVPROPKEY(
    0x540B947E,
    0x8B40,
    0x45BC,
    0xA8,
    0xA2,
    0x6A,
    0x0B,
    0x89,
    0x4C,
    0xBD,
    0xA2,
    0x4
)

# DEVPROP_TYPE_STRING
DEVPKEY_Device_DeviceDesc = DEFINE_DEVPROPKEY(
    0xA45C254E,
    0xDF1C,
    0x4EFD,
    0x80,
    0x20,
    0x67,
    0xD1,
    0x46,
    0xA8,
    0x50,
    0xE0,
    0x2
)

# DEVPROP_TYPE_STRING_LIST
DEVPKEY_Device_HardwareIds = DEFINE_DEVPROPKEY(
    0xA45C254E,
    0xDF1C,
    0x4EFD,
    0x80,
    0x20,
    0x67,
    0xD1,
    0x46,
    0xA8,
    0x50,
    0xE0,
    0x3
)

# DEVPROP_TYPE_STRING
DEVPKEY_Device_BiosDeviceName = DEFINE_DEVPROPKEY(
    0x540B947E,
    0x8B40,
    0x45BC,
    0xA8,
    0xA2,
    0x6A,
    0x0B,
    0x89,
    0x4C,
    0xBD,
    0xA2,
    0xA
)

# DEVPROP_TYPE_STRING
DEVPKEY_Device_Manufacturer = DEFINE_DEVPROPKEY(
    0xA45C254E,
    0xDF1C,
    0x4EFD,
    0x80,
    0x20,
    0x67,
    0xD1,
    0x46,
    0xA8,
    0x50,
    0xE0,
    0xD
)

# DEVPROP_TYPE_STRING
DEVPKEY_Device_FriendlyName = DEFINE_DEVPROPKEY(
    0xA45C254E,
    0xDF1C,
    0x4EFD,
    0x80,
    0x20,
    0x67,
    0xD1,
    0x46,
    0xA8,
    0x50,
    0xE0,
    0xE
)

#  DEVPROP_TYPE_STRING
DEVPKEY_Device_Model = DEFINE_DEVPROPKEY(
    0x78C34FC8,
    0x104A,
    0x4ACA,
    0x9E,
    0xA4,
    0x52,
    0x4D,
    0x52,
    0x99,
    0x6E,
    0x57,
    0x27
)
