# -*- coding: utf-8 -*-
import os
import ctypes
from ctypes.wintypes import WCHAR, LONG
from devioctl_h import *


if os.environ.get("PROCESSOR_ARCHITECTURE") == "AMD64" or os.environ.get("PROCESSOR_ARCHITEW6432") == "AMD64":
    PACK_FORMAT = "q"  # pack/unpack format for 64 bit int
    IR_ULONG_PTR = ctypes.c_ulonglong
else:
    PACK_FORMAT = "i"  # pack/unpack format for 32 bit int
    IR_ULONG_PTR = ctypes.c_ulong

IR_PTR_SIZE = ctypes.sizeof(IR_ULONG_PTR)

if ctypes.sizeof(ctypes.c_void_p) == 8:
    ULONG_PTR = ctypes.c_ulonglong
else:
    ULONG_PTR = ctypes.c_ulong


POINTER = ctypes.POINTER


FILE_DEVICE_IRCLASS = 0x0F60
MAXIMUM_FILENAME_LENGTH = 256


# + + IOCTL_IR_GET_DEVCAPS Returns device capabilities. For legacy
# devices, the Capabilities registry entry can be used to populate
# this structure. For new devices, the implementation is left as an
# exercise for the reader. The capabilities structure gets rev'ed when
# new capabilities are added to the class driver. The class driver
# sends the largest possible structure size to the port driver. The
# port driver populates the capabilties structure, including the
# ProtocolVersion member. The class driver then uses the
# ProtocolVersion member to decide which version of IR_DEV_CAPS the
# port driver has filled in. Used in IR DDI Versions: V1, V2 V1: port
# driver must set ProtocolVersion to 0x100 and fill in required
# members of IR_DEV_CAPS_V1 structure. V2: port driver must set
# ProtocolVersion to 0x200 and fill in required members of
# IR_DEV_CAPS_V2 structure Parameters: lpOutBuffer - pointer to caller
# - allocated IR_DEV_CAPS_V2 structure nOutBufferSize - ctypes.sizeof
# (IR_DEV_CAPS_V2) - -
IOCTL_IR_GET_DEV_CAPS = CTL_CODE(
    FILE_DEVICE_IRCLASS,
    1,
    METHOD_BUFFERED,
    FILE_READ_ACCESS
)


class _IR_DEV_CAPS(ctypes.Structure):
    _fields_ = [
        ('ProtocolVersion', IR_ULONG_PTR),  # out
        ('NumTransmitPorts', IR_ULONG_PTR),  # out
        ('NumReceivePorts', IR_ULONG_PTR),  # out
        ('LearningReceiverMask', IR_ULONG_PTR),  # out
        ('DevCapsFlags', IR_ULONG_PTR),  # out
    ]


IR_DEV_CAPS = _IR_DEV_CAPS
PIR_DEV_CAPS = POINTER(_IR_DEV_CAPS)

DEV_CAPS_PROTOCOL_VERSION = 0x100
DEV_CAPS_PROTOCOL_VERSION_V1 = 0x100


# Valid capabilities bits for protocol V1
DEV_CAPS_SUPPORTS_LEGACY_SIGNING = 0x1
DEV_CAPS_HAS_UNIQUE_SERIAL = 0x2
DEV_CAPS_CAN_FLASH_RECEIVER_LED = 0x4
DEV_CAPS_IS_LEGACY = 0x8

V1_DEV_CAPS_VALID_BITS = 0xF


class _IR_DEV_CAPS_V2(IR_DEV_CAPS):
    _fields_ = [
        ('WakeProtocols', IR_ULONG_PTR),
        ('TunerPnpId', WCHAR * MAXIMUM_FILENAME_LENGTH)
    ]


IR_DEV_CAPS_V2 = _IR_DEV_CAPS_V2
PIR_DEV_CAPS_V2 = POINTER(_IR_DEV_CAPS_V2)


DEV_CAPS_PROTOCOL_VERSION_V2 = 0x200


# Valid capabilities bits for protocol V2
V2_DEV_CAPS_SUPPORTS_WAKE = 0x10
V2_DEV_CAPS_MULTIPLE_WAKE = 0x20
V2_DEV_CAPS_PROGRAMMABLE_WAKE = 0x40
V2_DEV_CAPS_VOLATILE_WAKE_PATTERN = 0x80

V2_DEV_CAPS_LEARNING_ONLY = 0x100
V2_DEV_CAPS_NARROW_BPF = 0x200
V2_DEV_CAPS_NO_SWDECODE_INPUT = 0x400
V2_DEV_CAPS_HWDECODE_INPUT = 0x800

V2_DEV_CAPS_EMULATOR_V1 = 0x1000
V2_DEV_CAPS_EMULATOR_V2 = 0x2000
V2_DEV_CAPS_ATTACHED_TO_TUNER = 0x4000

V2_DEV_CAPS_VALID_BITS = 0x7fff


# Wake protocols
V2_WAKE_PROTOCOL_RC6 = 0x1
V2_WAKE_PROTOCOL_QP = 0x2
V2_WAKE_PROTOCOL_SAMSUNG = 0x4
V2_WAKE_PROTOCOL_DONTCARE = 0x8

V2_VALID_WAKE_PROTOCOLS = 0xF


# + + IOCTL_IR_GET_EMITTERS Gets attached emitters and returns the
# information in a bitmask. Information returned in lpOutBuffer. Used
# in IR DDI Versions: V1, V2 Parameters: lpOutBuffer - pointer to
# caller - allocated buffer ctypes.sizeof(ULONG) nOutBufferSize -
# ctypes.sizeof(ULONG) - -
IOCTL_IR_GET_EMITTERS = CTL_CODE(
    FILE_DEVICE_IRCLASS,
    2,
    METHOD_BUFFERED,
    FILE_READ_ACCESS,
)

# + + IOCTL_IR_FLASH_RECEIVER Flash an LED on the given receiver. Used
# to tell the user where to point their remote, so a given
# "receiver box" with multiple receiver parts only needs one LED to
# flash. Used in IR DDI Versions: V1, V2 Parameters: lpInBuffer -
# pointer to caller - allocated buffer ctypes.sizeof(ULONG) with
# bitmask of receivers to flash nInBufferSize - ctypes.sizeof(ULONG) -
# -
IOCTL_IR_FLASH_RECEIVER = CTL_CODE(
    FILE_DEVICE_IRCLASS,
    3,
    METHOD_BUFFERED,
    FILE_WRITE_ACCESS,
)

# + + IOCTL_IR_RESET_DEVICE Resets the given device. When a device is
# reset, all pending transmit and receive IOCTLs are cancelled by the
# class driver Used in IR DDI Versions: V1, V2 Parameters: - -
IOCTL_IR_RESET_DEVICE = CTL_CODE(
    FILE_DEVICE_IRCLASS,
    4,
    METHOD_BUFFERED,
    FILE_WRITE_ACCESS,
)

# + + IOCTL_IR_TRANSMIT Transmits the given IR stream on the given
# port(s) at the given carrier frequency. On legacy devices, this
# maintains the pre - existing carrier frequency, port masks, and
# sample period values.
# (ie. it gets the old values, changes them, transmits, and then changes them back.)
# This IOCTL is synchronous. It does not return until the IR has
# actually been transmitted. Used in IR DDI Versions: V1, V2
# Parameters:
# lpInBuffer - pointer to caller - allocated IR_TRANSMIT_PARAMS structure
# nInBufferSize - ctypes.sizeof(IR_TRANSMIT_PARAMS)
# lpOutBuffer - pointer to caller - allocated IR_TRANSMIT_CHUNCK that contains the data to be transmitted
# nOutBufferSize - size of caller - allocated buffer. - -
IOCTL_IR_TRANSMIT = CTL_CODE(
    FILE_DEVICE_IRCLASS,
    5,
    METHOD_IN_DIRECT,
    FILE_WRITE_ACCESS,
)


class _IR_TRANSMIT_PARAMS(ctypes.Structure):
    _fields_ = [
        ('TransmitPortMask', IR_ULONG_PTR),  # in
        ('CarrierPeriod', IR_ULONG_PTR),  # in
        ('Flags', IR_ULONG_PTR),  # in
        ('PulseSize', IR_ULONG_PTR),  # in
    ]


IR_TRANSMIT_PARAMS = _IR_TRANSMIT_PARAMS
PIR_TRANSMIT_PARAMS = POINTER(_IR_TRANSMIT_PARAMS)


TRANSMIT_FLAGS_PULSE_MODE = 0x0001
TRANSMIT_FLAGS_DC_MODE = 0x0002


class _IR_TRANSMIT_CHUNK(ctypes.Structure):
    _fields_ = [
        ('OffsetToNextChunk', IR_ULONG_PTR),  # IR_TRANSMIT_CHUNK (or zero if no more chunks in buffer)
        ('RepeatCount', IR_ULONG_PTR),  # number of times to serially repeat "ByteCount" bytes of data
        ('ByteCount', IR_ULONG_PTR),  # count of data bytes to be sent
        ('Data', LONG * 80),  # Note: Each chunk is filled to integral ULONG_PTR boundary
    ]


IR_TRANSMIT_CHUNK = _IR_TRANSMIT_CHUNK
PIR_TRANSMIT_CHUNK = POINTER(_IR_TRANSMIT_CHUNK)


# + + IOCTL_IR_RECEIVE Receives IR. Does not return until IR is
# available. If there is no more IR data available than space in the
# buffer, IrReceiveParms - >DataEnd is set to TRUE. The provided
# timeout is used to define the end of a keypress. So, once the driver
# starts receiving IR from the hardware, it will continue to add it to
# the buffer until the specified time passes with no IR. Used in IR
# DDI Versions: V1, V2 Parameters: lpOutBuffer - pointer to caller -
# allocated IR_RECEIVE_PARAMS structure nOutBufferSize -
# ctypes.sizeof(IR_RECEIVE_PARAMS) - -
IOCTL_IR_RECEIVE = CTL_CODE(
    FILE_DEVICE_IRCLASS,
    6,
    METHOD_OUT_DIRECT,
    FILE_READ_ACCESS,
)


class _IR_RECEIVE_PARAMS(ctypes.Structure):
    _fields_ = [
        ('DataEnd', IR_ULONG_PTR),  # out
        ('ByteCount', IR_ULONG_PTR),  # in
        ('Data', LONG * 100),  # out
    ]


IR_RECEIVE_PARAMS = _IR_RECEIVE_PARAMS
PIR_RECEIVE_PARAMS = POINTER(_IR_RECEIVE_PARAMS)


# + + IOCTL_IR_PRIORITY_RECEIVE This request is sent from CIRClass and
# receives Run Length Coded (RLC) IR data when the device is running
# in Priority Receive mode. If the device is not already in Priority
# Receive mode, initiated by having previously received an
# IOCTL_ENTER_PRIORITY_RECEIVE, the CIR Port driver fails this request
# immediately. If in Priority Receive mode, the request will remain
# pending until one of two events occurs:
# 1) The data buffer provided in the request has been completely filled with data.
# 2) An IR timeout occurs. The length of time required for the IR
# timeout was specified when entering Priority Receive mode. While in
# Priority Receive mode and processing IOCTL_IR_PRIORITY_RECEIVE
# requests, IOCTL_IR_RECEIVE requests remain pending and are not
# filled with IR data.
# Used in IR DDI Versions: V1, V2
# Parameters:
# lpOutBuffer - pointer to caller - allocated IR_PRIORITY_RECEIVE_PARAMS structure
# nOutBufferSize - ctypes.sizeof(IR_PRIORITY_RECEIVE_PARAMS) - -
#
IOCTL_IR_PRIORITY_RECEIVE = CTL_CODE(
    FILE_DEVICE_IRCLASS,
    8,
    METHOD_OUT_DIRECT,
    FILE_READ_ACCESS,
)


class _IR_PRIORITY_RECEIVE_PARAMS(ctypes.Structure):
    _fields_ = [
        ('DataEnd', IR_ULONG_PTR),  # out
        ('ByteCount', IR_ULONG_PTR),  # in
        ('CarrierFrequency', ULONG),  # out
        ('Data', LONG * 100),  # out
    ]


IR_PRIORITY_RECEIVE_PARAMS = _IR_PRIORITY_RECEIVE_PARAMS
PIR_PRIORITY_RECEIVE_PARAMS = POINTER(_IR_PRIORITY_RECEIVE_PARAMS)


# + + IOCTL_IR_HANDSHAKE This IOCTL is sent from CIRClass before
# creating the HID child device to represent the port. This IOCTL is
# to be completed synchronously by the port as an indication that it
# is prepared to return RLC IR data to the class driver. Used in IR
# DDI Versions: V1, V2 Parameters: - -
IOCTL_IR_HANDSHAKE = CTL_CODE(
    FILE_DEVICE_IRCLASS,
    9,
    METHOD_BUFFERED,
    FILE_ANY_ACCESS,
)

# + + IOCTL_IR_ENTER_PRIORITY_RECEIVE This request is sent to prepare
# the port to enter Priority Receive mode. While the device is in
# Priority Receive mode, all IOCTL_IR_RECEIVE requests should be
# starved and IOCTL_IR_PRIORITY_RECEIVE requests should be completed.
# Used in IR DDI Versions: V1, V2 Parameters: lpOutBuffer - pointer to
# caller - allocated IOCTL_IR_ENTER_PRIORITY_RECEIVE_PARAMS structure
# nOutBufferSize -
# ctypes.sizeof(IOCTL_IR_ENTER_PRIORITY_RECEIVE_PARAMS) - -
IOCTL_IR_ENTER_PRIORITY_RECEIVE = CTL_CODE(
    FILE_DEVICE_IRCLASS,
    10,
    METHOD_BUFFERED,
    FILE_WRITE_ACCESS,
)


class _IOCTL_IR_ENTER_PRIORITY_RECEIVE_PARAMS(ctypes.Structure):
    _fields_ = [
        ('Receiver', IR_ULONG_PTR),  # in
        ('TimeOut', IR_ULONG_PTR),  # in
    ]


IOCTL_IR_ENTER_PRIORITY_RECEIVE_PARAMS = _IOCTL_IR_ENTER_PRIORITY_RECEIVE_PARAMS
PIOCTL_IR_ENTER_PRIORITY_RECEIVE_PARAMS = POINTER(_IOCTL_IR_ENTER_PRIORITY_RECEIVE_PARAMS)


# + + IOCTL_IR_EXIT_PRIORITY_RECEIVE This request is sent to end
# Priority Receive mode. Upon receipt of the request, the port should
# abort any outstanding IOCTL_IR_PRIORITY_RECEIVE requests and fail
# any future IOCTL_IR_PRIORITY_RECEIVE requests
# (before receiving a new IOCTL_IR_ENTER_PRIORITY_RECEIVE request). As
# a result of receiving this IOCTL, the CIR Port driver is responsible
# for restoring the device to the state that it was in before receipt
# of the IOCTL_IR_ENTER_PRIORITY_RECEIVE. Used in IR DDI Versions: V1,
# V2 Parameters: - -
IOCTL_IR_EXIT_PRIORITY_RECEIVE = CTL_CODE(
    FILE_DEVICE_IRCLASS,
    11,
    METHOD_BUFFERED,
    FILE_WRITE_ACCESS,
)

# + + IOCTL_IR_USER_OPEN This IOCTL is sent from the class driver when
# a user has indirectly opened the port driver through IRCLASS. This
# IOCTL is informational only, allowing the port to do any
# initialization or bookkeeping required to handle requests not
# directly originating from IRCLASS. Used in IR DDI Versions: V1, V2
# Parameters: - -
IOCTL_IR_USER_OPEN = CTL_CODE(
    FILE_DEVICE_IRCLASS,
    12,
    METHOD_BUFFERED,
    FILE_WRITE_ACCESS,
)

# + + IOCTL_IR_USER_CLOSE This IOCTL is sent from IRCLASS when a user
# has indirectly closed the port driver. This IOCTL is informational
# only, allowing the port to do any cleanup required when closed by a
# user. Used in IR DDI Versions: V1, V2 Parameters: - -
IOCTL_IR_USER_CLOSE = CTL_CODE(
    FILE_DEVICE_IRCLASS,
    13,
    METHOD_BUFFERED,
    FILE_WRITE_ACCESS,
)

# + + IOCTL_IR_SET_WAKE_PATTERN This IOCTL is sent from IRCLASS to
# configure the wake pattern. This is done dynamically in response to
# user input, so it could be done at any time. Used in IR DDI
# Versions: V2 only Parameters: lpInBuffer - pointer to caller -
# allocated IR_SET_WAKE_PATTERN_PARAMS structure nInBufferSize -
# ctypes.sizeof(IR_SET_WAKE_PATTERN_PARAMS) - -
IOCTL_IR_SET_WAKE_PATTERN = CTL_CODE(
    FILE_DEVICE_IRCLASS,
    14,
    METHOD_BUFFERED,
    FILE_WRITE_ACCESS,
)


class _IOCTL_IR_SET_WAKE_PATTERN_PARAMS(ctypes.Structure):
    _fields_ = [
        ('Protocol', IR_ULONG_PTR),  # in
        ('Payload', IR_ULONG_PTR),  # in
        ('Address', IR_ULONG_PTR),  # in
    ]


IOCTL_IR_SET_WAKE_PATTERN_PARAMS = _IOCTL_IR_SET_WAKE_PATTERN_PARAMS
PIOCTL_IR_SET_WAKE_PATTERN_PARAMS = POINTER(_IOCTL_IR_SET_WAKE_PATTERN_PARAMS)


# Valid wake keys. A good implementation will be able to wake on all
# key codes but this is not required.
WAKE_KEY_POWER_TOGGLE = 0x0C
WAKE_KEY_DISCRETE_ON = 0x29
WAKE_KEY_ALL_KEYS = 0xFFFF
