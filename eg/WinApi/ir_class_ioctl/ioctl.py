# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2019 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.


"""
This file is part of the **pyWinMCERemote**
project https://github.com/kdschlosser/pyWinMCERemote

:platform: Windows
:license: GPL version 2 or newer
:synopsis: Windos API entry point

.. moduleauthor:: Kevin Schlosser @kdschlosser <kevin.g.schlosser@gmail.com>
"""

from devpropdef_h import *
from fileapi_h import *
from ioapi_h import *
from ioapiset_h import *
from irclass_ioctl_h import *
from winnt_h import *
from winerror_h import *
from winbase_h import *
from usbiodef_h import *
from synchapi_h import *
from setupapi_h import *
from minwinbase_h import *
from guiddef_h import *
from devioctl_h import *
from handleapi_h import *

import os
import ctypes
import threading
import six
import _winreg
import requests
from ctypes.wintypes import (
    LPVOID,
    BOOL,
    DWORD,
    INT,
    HANDLE,
    LONG
)

import json

BASE_PATH = os.path.dirname(__file__)

data_file = os.path.join(BASE_PATH, 'usb_vendors.json')

try:
    with open(data_file, 'r') as f:
        data_file = f.read()

    DEVICE_MAPPING = json.loads(data_file)
    DATA_LOADED = True
except (OSError, ValueError):
    DEVICE_MAPPING = {}
    DATA_LOADED = False


del data_file
del json


def load_device_data():
    global DATA_LOADED

    if DATA_LOADED:
        return

    DATA_LOADED = True

    try:
        response = requests.get('http://www.linux-usb.org/usb.ids', timeout=1)
        if response.status_code != 200:
            raise requests.ConnectionError

    except requests.ConnectionError:
        pass
    else:
        ids = response.content
        current_vendor = {}

        for line in ids.split('\n'):
            if not line.strip():
                continue

            if line.startswith('#'):
                continue

            if not line.startswith('\t'):
                vid, mfg_name = list(item.strip() for item in line.split(' ', 1))
                try:
                    vid = int('0x' + vid, 16)
                except ValueError:
                    current_vendor = None
                    continue

                current_vendor = {}
                DEVICE_MAPPING[vid] = dict(
                    name=mfg_name,
                    devices=current_vendor
                )
            elif current_vendor is not None:
                line = line.strip()
                pid, product_name = list(item.strip() for item in line.split(' ', 1))
                try:
                    pid = int('0x' + pid, 16)
                except ValueError:
                    continue

                current_vendor[pid] = product_name


os.environ['PATH'] = ';'.join([item for item in os.environ['PATH'].split(';') if item.strip()] + [BASE_PATH])

LONGLONG = ctypes.c_longlong

POINTER = ctypes.POINTER
HDEVINFO = LPVOID
NULL = None

UCHAR = ctypes.c_ubyte
PUCHAR = POINTER(UCHAR)
UBYTE = ctypes.c_ubyte
BYTE = ctypes.c_byte


def _first_high_bit(mask):
    for i in range(32):
        if mask & (1 << i) != 0:
            return i

    return -1


def _first_low_bit(mask):
    for i in range(32):
        if mask & (1 << i) == 0:
            return i

    return -1


def _get_high_bit(mask, bit_count):
    count = 0
    for i in range(32):
        bit_mask = 1 << i
        if mask & bit_mask:
            if count + 1 == bit_count:
                return bit_mask
            else:
                count += 1

    return 0


def _get_reg_value(path, key):
    d = _read_reg_values(path, None)

    if key in d:
        return d[key]


def _read_reg_keys(path, key):
    if key:
        key = path + '\\' + key
    else:
        key = path

    try:
        handle = _winreg.OpenKeyEx(_winreg.HKEY_LOCAL_MACHINE, key)
    except WindowsError:
        return []

    res = []

    for i in range(_winreg.QueryInfoKey(handle)[0]):
        res += [_winreg.EnumKey(handle, i)]

    _winreg.CloseKey(handle)
    return res


IRCLASS_REGISTRY_PATH = 'SYSTEM\\CurrentControlSet\\Control\\DeviceClasses\\{7951772d-cd50-49b7-b103-2baac494fc57}'
USB_REGISTRY_PATH = 'SYSTEM\\ControlSet001\\services\\usbcir\\Enum'


def _read_reg_values(path, key):
    if key:
        key = path + '\\' + key
    else:
        key = path

    try:
        handle = _winreg.OpenKeyEx(_winreg.HKEY_LOCAL_MACHINE, key)
    except WindowsError:
        return {}

    res = {}

    for i in range(_winreg.QueryInfoKey(handle)[1]):
        name, value, _ = _winreg.EnumValue(handle, i)
        res[_convert_mbcs(name)] = _convert_mbcs(value)

    _winreg.CloseKey(handle)
    return res


def _convert_mbcs(s):
    dec = getattr(s, "decode", None)
    if dec is not None:
        try:
            s = dec("mbcs")
        except UnicodeError:
            pass
    return s


def _get_device_hw_ids():
    found_devices = []

    count = _get_reg_value(
        USB_REGISTRY_PATH,
        'Count'
    )

    if count is None:
        count = 0

    for i in range(count):
        hw_id = _get_reg_value(
            USB_REGISTRY_PATH,
            str(i)
        )
        if hw_id is not None:
            hw_id = [itm for itm in hw_id.split('\\') if itm.upper().startswith('VID')]
            if hw_id:
                found_devices += [hw_id[0]]

    return found_devices


def _get_device_class_ports():
    device_paths = _read_reg_keys(IRCLASS_REGISTRY_PATH, None)
    found_ports = []

    for device_path in device_paths:
        ports = _read_reg_keys(IRCLASS_REGISTRY_PATH, device_path)

        for port in ports:
            values = _read_reg_values(
                IRCLASS_REGISTRY_PATH,
                device_path + '\\' + port + '\\control'
            )

            if 'linked' in values and values['linked']:
                found_ports += [(device_path[4:] + port).replace('#', '\\')]

    return found_ports


# {064F8C82-77B2-445e-B85D-C4E20F942FE1}
GUID_DEVINTERFACE_IRPORT = DEFINE_GUID(
    0x64f8c82,
    0x77b2,
    0x445e,
    0xb8,
    0x5d,
    0xc4,
    0xe2,
    0xf,
    0x94,
    0x2f,
    0xe1
)
# {7951772D-CD50-49B7-B103-2BAAC494FC57}
GUID_CLASS_IRBUS = DEFINE_GUID(
    0x7951772d,
    0xcd50,
    0x49b7,
    0xb1,
    0x03,
    0x2b,
    0xaa,
    0xc4,
    0x94,
    0xfc,
    0x57
)


def _get_device_property(DeviceInfoSet, DeviceInfoData, PropertyKey):

    if PropertyKey == DEVPKEY_Device_HardwareIds:
        PropertyType = DEVPROPTYPE(DEVPROP_TYPE_STRING_LIST)
    else:
        PropertyType = DEVPROPTYPE(DEVPROP_TYPE_STRING)

    PropertyBuffer = NULL
    PropertyBufferSize = DWORD(0)
    RequiredSize = DWORD()
    Flags = DWORD(0)

    SetupDiGetDevicePropertyW(
        DeviceInfoSet,
        ctypes.byref(DeviceInfoData),
        ctypes.byref(PropertyKey),
        ctypes.byref(PropertyType),
        PropertyBuffer,
        PropertyBufferSize,
        ctypes.byref(RequiredSize),
        Flags
    )

    PropertyBuffer = (BYTE * RequiredSize.value)()
    PropertyBufferSize = DWORD(RequiredSize.value)
    RequiredSize = DWORD()

    SetupDiGetDevicePropertyW(
        DeviceInfoSet,
        ctypes.byref(DeviceInfoData),
        ctypes.byref(PropertyKey),
        ctypes.byref(PropertyType),
        PropertyBuffer,
        PropertyBufferSize,
        ctypes.byref(RequiredSize),
        Flags
    )

    res = bytearray()
    for i in range(PropertyBufferSize.value):
        char = PropertyBuffer[i]

        if char == 0x00:
            continue

        res.append(char)

    return res.decode('utf-8').encode('utf-8')


def _get_device_data(hardware_id):
    DeviceInfoSet = SetupDiGetClassDevs(
        ctypes.byref(GUID_DEVINTERFACE_USB_DEVICE),
        NULL,
        NULL,
        DIGCF_PRESENT | DIGCF_DEVICEINTERFACE
    )
    if DeviceInfoSet == INVALID_HANDLE_VALUE:
        raise ctypes.WinError()

    DeviceInterfaceData = SP_DEVICE_INTERFACE_DATA()
    DeviceInterfaceData.cbSize = ctypes.sizeof(SP_DEVICE_INTERFACE_DATA)
    DeviceInfoData = SP_DEVINFO_DATA()
    DeviceInfoData.cbSize = ctypes.sizeof(SP_DEVINFO_DATA)
    MemberIndex = 0
    device_info = None

    while True:
        if not SetupDiEnumDeviceInterfaces(
            DeviceInfoSet,
            None,
            ctypes.byref(GUID_DEVINTERFACE_USB_DEVICE),
            MemberIndex,
            ctypes.byref(DeviceInterfaceData)
        ):
            err = ctypes.GetLastError()
            if err == ERROR_NO_MORE_ITEMS:
                break
            else:
                raise ctypes.WinError(err)

        RequiredSize = DWORD()
        SetupDiGetDeviceInterfaceDetail(
            DeviceInfoSet,
            ctypes.byref(DeviceInterfaceData),
            None,
            0,
            ctypes.byref(RequiredSize),
            ctypes.byref(DeviceInfoData)
        )
        DevicePath = ctypes.create_string_buffer(RequiredSize.value)
        pDeviceInterfaceDetailData = ctypes.cast(DevicePath, PSP_DEVICE_INTERFACE_DETAIL_DATA)
        pDeviceInterfaceDetailData.contents.cbSize = ctypes.sizeof(
            SP_DEVICE_INTERFACE_DETAIL_DATA
        )
        SetupDiGetDeviceInterfaceDetail(
            DeviceInfoSet,
            ctypes.byref(DeviceInterfaceData),
            pDeviceInterfaceDetailData,
            RequiredSize.value,
            ctypes.byref(RequiredSize),
            None
        )

        hw_id = _get_device_property(DeviceInfoSet, DeviceInfoData, DEVPKEY_Device_HardwareIds)

        if hardware_id in hw_id:
            desc = _get_device_property(DeviceInfoSet, DeviceInfoData, DEVPKEY_Device_BusReportedDeviceDesc)
            mfg = ''  # _get_device_property(DeviceInfoSet, DeviceInfoData, DEVPKEY_Device_Manufacturer)
            name = _get_device_property(DeviceInfoSet, DeviceInfoData, DEVPKEY_Device_DeviceDesc)
            model = ''  # _get_device_property(DeviceInfoSet, DeviceInfoData, DEVPKEY_Device_Model)

            device_info = [desc, hw_id, mfg, name, model]
            break

        MemberIndex += 1

    SetupDiDestroyDeviceInfoList(DeviceInfoSet)

    return device_info


def _get_ir_receiver_paths():
    DeviceInfoSet = SetupDiGetClassDevs(
        ctypes.byref(GUID_CLASS_IRBUS),
        NULL,
        NULL,
        DIGCF_PRESENT | DIGCF_DEVICEINTERFACE
    )
    if DeviceInfoSet == INVALID_HANDLE_VALUE:
        raise ctypes.WinError()

    DeviceInterfaceData = SP_DEVICE_INTERFACE_DATA()
    DeviceInterfaceData.cbSize = ctypes.sizeof(SP_DEVICE_INTERFACE_DATA)
    DeviceInfoData = SP_DEVINFO_DATA()
    DeviceInfoData.cbSize = ctypes.sizeof(SP_DEVINFO_DATA)
    MemberIndex = 0
    device_paths = []

    while True:
        if not SetupDiEnumDeviceInterfaces(
            DeviceInfoSet,
            None,
            ctypes.byref(GUID_CLASS_IRBUS),
            MemberIndex,
            ctypes.byref(DeviceInterfaceData)
        ):
            err = ctypes.GetLastError()
            if err == ERROR_NO_MORE_ITEMS:
                break
            else:
                raise ctypes.WinError(err)

        RequiredSize = DWORD()
        SetupDiGetDeviceInterfaceDetail(
            DeviceInfoSet,
            ctypes.byref(DeviceInterfaceData),
            None,
            0,
            ctypes.byref(RequiredSize),
            ctypes.byref(DeviceInfoData)
        )
        DevicePath = ctypes.create_string_buffer(RequiredSize.value)
        pDeviceInterfaceDetailData = ctypes.cast(DevicePath, PSP_DEVICE_INTERFACE_DETAIL_DATA)
        pDeviceInterfaceDetailData.contents.cbSize = ctypes.sizeof(
            SP_DEVICE_INTERFACE_DETAIL_DATA
        )
        SetupDiGetDeviceInterfaceDetail(
            DeviceInfoSet,
            ctypes.byref(DeviceInterfaceData),
            pDeviceInterfaceDetailData,
            RequiredSize.value,
            ctypes.byref(RequiredSize),
            None
        )

        device_path = ctypes.wstring_at(ctypes.addressof(pDeviceInterfaceDetailData.contents) + 4)

        device_paths += [device_path]
        MemberIndex += 1

    SetupDiDestroyDeviceInfoList(DeviceInfoSet)

    return device_paths


def _open_ir_receiver(device_path):
    lpFileName = ctypes.create_unicode_buffer(device_path)
    dwDesiredAccess = DWORD(GENERIC_READ | GENERIC_WRITE)
    dwShareMode = DWORD(0)
    lpSecurityAttributes = NULL
    dwCreationDisposition = DWORD(OPEN_EXISTING)
    dwFlagsAndAttributes = DWORD(FILE_FLAG_OVERLAPPED)
    hTemplateFile = NULL

    handle = CreateFile(
        lpFileName,
        dwDesiredAccess,
        dwShareMode,
        lpSecurityAttributes,
        dwCreationDisposition,
        dwFlagsAndAttributes,
        hTemplateFile
    )

    return handle


def _get_ir_capabilities(hDevice):
    outBuffer = IR_DEV_CAPS()

    if _io_control(IOCTL_IR_GET_DEV_CAPS, hDevice, NULL, outBuffer):
        if outBuffer.ProtocolVersion == DEV_CAPS_PROTOCOL_VERSION_V2:
            _io_control(IOCTL_IR_GET_DEV_CAPS, hDevice, NULL, outBuffer)
            outBuffer_2 = IR_DEV_CAPS_V2()

            if _io_control(IOCTL_IR_GET_DEV_CAPS, hDevice, NULL, outBuffer_2):
                return outBuffer_2

        return outBuffer


_found_devices = []
_get_ir_device_lock = threading.Lock()


def reset_device_list():
    with _get_ir_device_lock:
        del _found_devices[:]


def get_ir_devices():
    with _get_ir_device_lock:
        if _found_devices:
            return _found_devices

        for device_path in _get_ir_receiver_paths():
            hDevice = _open_ir_receiver(device_path)

            if hDevice == INVALID_HANDLE_VALUE:
                continue

            hDevice = HANDLE(hDevice)

            try:
                caps = _get_ir_capabilities(hDevice)

                if caps is None:
                    CloseHandle(hDevice)
                    continue

                desc, hw_id, mfg, name, model = _get_device_data(_get_device_hw_ids()[0])
                device = IRDevice(device_path, desc, hw_id, mfg, name, model, caps)
                if device not in _found_devices:
                    _found_devices.append(device)
            except WindowsError as err:
                if err.errno == 121:
                    continue

                else:
                    raise err

        return _found_devices


def _io_control(ioControlCode, hDevice, inBuffer, outBuffer, outBufferSize=None):
    dwIoControlCode = DWORD(ioControlCode)

    if inBuffer is NULL:
        lpInBuffer = NULL
        nInBufferSize = INT(0)
    elif 'PyCPointerType' in str(type(inBuffer)):
        lpInBuffer = inBuffer
        nInBufferSize = INT(ctypes.sizeof(inBuffer.contents.__class__))
    else:
        lpInBuffer = ctypes.byref(inBuffer)
        nInBufferSize = INT(ctypes.sizeof(inBuffer.__class__))

    if outBuffer is NULL:
        lpOutBuffer = NULL
        nOutBufferSize = INT(0)

    elif 'PyCPointerType' in str(type(outBuffer)):
        lpOutBuffer = outBuffer
        if outBufferSize is None:
            nOutBufferSize = INT(ctypes.sizeof(outBuffer.contents.__class__))
        else:
            nOutBufferSize = INT(outBufferSize)
    else:
        lpOutBuffer = ctypes.byref(outBuffer)

        if outBufferSize is None:
            nOutBufferSize = INT(ctypes.sizeof(outBuffer.__class__))
        else:
            nOutBufferSize = INT(outBufferSize)

    lpNumberOfBytesTransferred = DWORD()
    lpOverlapped = OVERLAPPED()

    lpEventAttributes = NULL
    bManualReset = BOOL(False)
    bInitialState = BOOL(False)
    lpName = NULL

    lpOverlapped.hEvent = CreateEvent(
        lpEventAttributes,
        bManualReset,
        bInitialState,
        lpName
    )

    if not DeviceIoControl(
        hDevice,
        dwIoControlCode,
        lpInBuffer,
        nInBufferSize,
        lpOutBuffer,
        nOutBufferSize,
        ctypes.byref(lpNumberOfBytesTransferred),
        ctypes.byref(lpOverlapped)
    ):
        err = ctypes.GetLastError()

        if err != ERROR_IO_PENDING:
            CancelIo(hDevice)
            CloseHandle(lpOverlapped.hEvent)
            return 0
        nCount = DWORD(1)
        bWaitAll = BOOL(False)
        dwMilliseconds = DWORD(INFINITE)

        lpHandles = (HANDLE * 1)(lpOverlapped.hEvent)

        response = WaitForMultipleObjects(
            nCount,
            lpHandles,
            bWaitAll,
            dwMilliseconds
        )

        if response == WAIT_OBJECT_0:
            bWait = BOOL(True)
            lpNumberOfBytesTransferred = DWORD()

            if not GetOverlappedResult(
                hDevice,
                ctypes.byref(lpOverlapped),
                ctypes.byref(lpNumberOfBytesTransferred),
                bWait
            ):
                CancelIo(hDevice)
                CloseHandle(lpOverlapped.hEvent)

                err = ctypes.GetLastError()
                raise ctypes.WinError(err)

            CloseHandle(lpOverlapped.hEvent)

            return lpNumberOfBytesTransferred.value

        CancelIo(hDevice)
        CloseHandle(lpOverlapped.hEvent)
        raise ctypes.WinError()

    CloseHandle(lpOverlapped.hEvent)
    return lpNumberOfBytesTransferred.value


class IRDeviceInstanceSingleton(type):

    def __init__(cls, name, bases, dct):
        super(IRDeviceInstanceSingleton, cls).__init__(name, bases, dct)
        cls._instances = {}

    def __call__(cls, device_path, desc, hw_id, mfg, name, model, caps):
        if device_path not in cls._instances:
            cls._instances[device_path] = (
                super(IRDeviceInstanceSingleton, cls).__call__(device_path, desc, hw_id, mfg, name, model, caps)
            )

        return cls._instances[device_path]


class Handle(object):

    def __init__(self, device_path):
        self._handle = None

        self.device_path = device_path
        self.__reference_count = 0

    def __enter__(self):
        if self._handle is None:
            self._handle = HANDLE(_open_ir_receiver(self.device_path))

        self.__reference_count += 1

        return self._handle

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__reference_count -= 1

        if self.__reference_count == 0:
            CloseHandle(self._handle)
            self._handle = None


# BOOL SetEvent(
#   HANDLE hEvent
# );
SetEvent = kernel32.SetEvent
SetEvent.restype = BOOL

LONG_MIN = -2147483648


@six.add_metaclass(IRDeviceInstanceSingleton)
class IRDevice(object):
    def __init__(self, device_path, desc, hw_id, mfg, name, model, caps):
        self.timing_tolerance = 15.0
        self.handle = Handle(device_path)
        self.device_path = device_path
        self.description = desc
        self.name = name
        self._model = model
        self.hardware_id = hw_id
        self._manufacturer = mfg
        hw_id = hw_id.split('\\')[1]
        vid, pid = hw_id.split('&')[:2]
        self.vid = '0x' + vid.split('_')[-1]
        self.pid = '0x' + pid.split('_')[-1]
        self.num_tx_ports = caps.NumTransmitPorts
        self._learn_mask = caps.LearningReceiverMask
        self._capabilities = caps.DevCapsFlags

        if caps.ProtocolVersion == DEV_CAPS_PROTOCOL_VERSION_V2:
            self.version = 2
            self._wake_protocols = caps.WakeProtocols
            self.tuner_id = ctypes.wstring_at(ctypes.addressof(caps) + 24)

        else:
            self.version = 1
            self._wake_protocols = None
            self.tuner_id = None

        self._packet_timeout = 14

        self._end_event = threading.Event()
        self._process_event = threading.Event()
        self._learn_lock = threading.Lock()
        self._receive_thread = None
        self._process_thread = None
        self._callbacks = []
        self._process_queue = []
        self.use_alternate_receive = True
        self.packet_size = 100
        self.hEvent = None

    @property
    def manufacturer(self):
        vd = int(self.vid, 16)
        if vd in DEVICE_MAPPING:
            return DEVICE_MAPPING[vd]['name']

        return self._manufacturer

    @property
    def model(self):
        vd = int(self.vid, 16)
        pd = int(self.pid, 16)

        if vd in DEVICE_MAPPING:
            vendor = DEVICE_MAPPING[vd]
            if pd in vendor['devices']:
                return vendor['devices'][pd]

        return self._model

    def bind(self, callback):
        if callback not in self._callbacks:
            self._callbacks += [callback]
            return True
        return False

    def unbind(self, callback):
        if callback in self._callbacks:
            self._callbacks.remove(callback)
            return True

        return False

    def stop_receive(self):
        try:
            if self._receive_thread is not None:
                self._end_event.set()
                if self.hEvent is not None:
                    SetEvent(self.hEvent)

                if (
                    threading.current_thread() != self._receive_thread and
                    self._receive_thread.is_alive()
                ):
                    self._receive_thread.join(1.0)

                self._receive_thread = None
                self._process_thread = None
        except AttributeError:
            pass

    @property
    def is_running(self):
        return self._receive_thread is not None

    def start_receive(self):
        if self._receive_thread is None:
            self._receive_thread = threading.Thread(target=self.__receive_loop)
            self._receive_thread.daemon = True
            self._end_event.clear()
            self._receive_thread.start()

    def __process_loop(self):
        frequency = 0
        result = []

        while not self._end_event.is_set():
            while len(self._process_queue):
                freq, data = self._process_queue.pop(0)

                while data:
                    item = data.pop(0)

                    if not result:
                        if freq is None:
                            if 6500 < item or item == 0:
                                frequency = item
                            else:
                                frequency = 0
                                result.append(item)
                        else:
                            frequency = max(frequency, freq)
                            if item == 0:
                                continue

                            result.append(item)
                    elif item == 0:
                        continue
                    else:
                        result.append(item)

                    if len(result) > 5:
                        for callback in self._callbacks[:]:
                            if callback(self, frequency, result[:]):
                                del result[:]
                                frequency = 0

            self._process_event.wait()
            self._process_event.clear()

    def __receive_loop(self):
        # self._process_thread = threading.Thread(target=self.__process_loop)
        # self._process_thread.daemon = True
        # self._process_thread.start()
        buf = []

        lpNumberOfBytesTransferred = DWORD()
        lpOverlapped = OVERLAPPED()

        lpEventAttributes = NULL
        bManualReset = BOOL(False)
        bInitialState = BOOL(False)
        lpName = NULL

        lpOverlapped.hEvent = CreateEvent(
            lpEventAttributes,
            bManualReset,
            bInitialState,
            lpName
        )

        with self.handle as hDevice:
            if self.use_alternate_receive:
                port = self.__get_first_rx_port()

                if port is None:
                    # del self._process_queue[:]
                    # self._process_event.set()
                    # self._process_thread.join(1.0)
                    self._receive_thread = None
                    return

                with self._learn_lock:
                    inBuffer = IOCTL_IR_ENTER_PRIORITY_RECEIVE_PARAMS()
                    inBuffer.Receiver = port
                    inBuffer.TimeOut = self._packet_timeout

                    _io_control(
                        IOCTL_IR_ENTER_PRIORITY_RECEIVE,
                        hDevice,
                        inBuffer,
                        NULL
                    )

                dwIoControlCode = IOCTL_IR_PRIORITY_RECEIVE
                outBuffer = IR_PRIORITY_RECEIVE_PARAMS()

                outBuffer.DataEnd = ctypes.c_ulonglong(0)
                outBuffer.CarrierFrequency = ULONG(0)
                outBuffer.ByteCount = 392
                outBuffer.Data = (LONG * 100)(*([LONG_MIN] * 100))
                outBufferSize = ctypes.sizeof(IR_PRIORITY_RECEIVE_PARAMS)

            else:
                dwIoControlCode = IOCTL_IR_RECEIVE
                outBuffer = IR_RECEIVE_PARAMS()
                outBuffer.DataEnd = ctypes.c_ulonglong(0)
                outBuffer.ByteCount = 396
                outBuffer.Data = (LONG * 100)(*([LONG_MIN] * 100))
                outBufferSize = ctypes.sizeof(IR_RECEIVE_PARAMS)

            while not self._end_event.is_set():
                with self._learn_lock:
                    outBuffer.Data = (LONG * 100)(*([LONG_MIN] * 100))
                    outBuffer.DataEnd = ctypes.c_ulonglong(0)
                    if dwIoControlCode == IOCTL_IR_PRIORITY_RECEIVE:
                        outBuffer.CarrierFrequency = ULONG(0)

                    if not DeviceIoControl(
                        hDevice,
                        DWORD(dwIoControlCode),
                        NULL,
                        INT(0),
                        ctypes.byref(outBuffer),
                        INT(outBufferSize),
                        ctypes.byref(lpNumberOfBytesTransferred),
                        ctypes.byref(lpOverlapped)
                    ):
                        err = ctypes.GetLastError()

                        if err != ERROR_IO_PENDING:
                            CancelIo(hDevice)
                            CloseHandle(lpOverlapped.hEvent)
                            raise ctypes.WinError()

                        bWaitAll = BOOL(False)
                        dwMilliseconds = DWORD(INFINITE)

                        if dwIoControlCode == IOCTL_IR_PRIORITY_RECEIVE:
                            lpEventAttributes = NULL
                            bManualReset = BOOL(False)
                            bInitialState = BOOL(False)
                            lpName = NULL

                            hEvent = self.hEvent = CreateEvent(
                                lpEventAttributes,
                                bManualReset,
                                bInitialState,
                                lpName
                            )

                            nCount = DWORD(2)
                            lpHandles = (HANDLE * 2)(lpOverlapped.hEvent, hEvent)
                        else:
                            nCount = DWORD(1)
                            lpHandles = (HANDLE * 1)(lpOverlapped.hEvent)

                        response = WaitForMultipleObjects(
                            nCount,
                            lpHandles,
                            bWaitAll,
                            dwMilliseconds
                        )

                        if response == WAIT_OBJECT_0:
                            bWait = BOOL(True)

                            if not GetOverlappedResult(
                                hDevice,
                                ctypes.byref(lpOverlapped),
                                ctypes.byref(lpNumberOfBytesTransferred),
                                bWait
                            ):
                                err = ctypes.GetLastError()

                                if self.hEvent is not None:
                                    CloseHandle(self.hEvent)
                                    self.hEvent = None

                                CancelIo(hDevice)
                                ResetEvent(HANDLE(lpOverlapped.hEvent))
                                continue

                                # raise ctypes.WinError(err)

                        else:
                            if self.hEvent is not None:
                                CloseHandle(self.hEvent)
                                self.hEvent = None

                            CancelIo(hDevice)
                            break

                    if self.hEvent is not None:
                        CloseHandle(self.hEvent)
                        self.hEvent = None

                    ResetEvent(HANDLE(lpOverlapped.hEvent))

                    for i in range(100):
                        data = outBuffer.Data[i]
                        if data not in (LONG_MIN, 0):
                            buf += [data]

                    if dwIoControlCode == IOCTL_IR_PRIORITY_RECEIVE:
                        freq = outBuffer.CarrierFrequency
                        for callback in self._callbacks[:]:
                            callback(self, freq, buf[:])

                        del buf[:]

                    else:
                        for callback in self._callbacks[:]:
                            callback(self, 0, buf[:])

                        del buf[:]
                    # self._process_queue.append((freq, buf[:]))
                    # self._process_event.set()

            if self.use_alternate_receive:
                _io_control(IOCTL_IR_EXIT_PRIORITY_RECEIVE, hDevice, NULL, NULL)

        CloseHandle(lpOverlapped.hEvent)

        # del self._process_queue[:]
        # self._process_event.set()
        # self._process_thread.join(1.0)
        self._receive_thread = None

    def learn(self, timeout=10.0, event=None):
        import time

        if self._receive_thread is not None and self.hEvent is not None:
            SetEvent(self.hEvent)

        self._learn_lock.acquire()

        with self.handle as hDevice:
            def exit_learn():
                SetEvent(self.hEvent)
                if not self.use_alternate_receive:
                    _io_control(
                        IOCTL_IR_EXIT_PRIORITY_RECEIVE,
                        hDevice,
                        NULL,
                        NULL
                    )

                self._learn_lock.release()

            if not self.use_alternate_receive:
                port = self.__get_first_learn_port()

                if port is None:
                    return

                inBuffer = IOCTL_IR_ENTER_PRIORITY_RECEIVE_PARAMS()
                inBuffer.Receiver = port
                inBuffer.TimeOut = self._packet_timeout

                _io_control(
                    IOCTL_IR_ENTER_PRIORITY_RECEIVE,
                    hDevice,
                    inBuffer,
                    NULL
                )

            result = []
            frequency = None

            start_time = time.time()

            while time.time() - start_time < timeout and not event.is_set():
                if self.can_flash_led:
                    port = self.__get_first_learn_port()

                    inBuffer = ULONG(0 | (1 << port))
                    _io_control(
                        IOCTL_IR_FLASH_RECEIVER,
                        hDevice,
                        inBuffer,
                        NULL
                    )

                dwIoControlCode = IOCTL_IR_PRIORITY_RECEIVE
                outBuffer = IR_PRIORITY_RECEIVE_PARAMS()
                outBuffer.ByteCount = 32
                outBufferSize = ctypes.sizeof(IR_PRIORITY_RECEIVE_PARAMS)

                lpNumberOfBytesTransferred = DWORD()
                lpOverlapped = OVERLAPPED()

                lpEventAttributes = NULL
                bManualReset = BOOL(False)
                bInitialState = BOOL(False)
                lpName = NULL

                lpOverlapped.hEvent = CreateEvent(
                    lpEventAttributes,
                    bManualReset,
                    bInitialState,
                    lpName
                )

                if not DeviceIoControl(
                    hDevice,
                    DWORD(dwIoControlCode),
                    NULL,
                    INT(0),
                    ctypes.byref(outBuffer),
                    INT(outBufferSize),
                    ctypes.byref(lpNumberOfBytesTransferred),
                    ctypes.byref(lpOverlapped)
                ):
                    err = ctypes.GetLastError()

                    if err != ERROR_IO_PENDING:
                        CancelIo(hDevice)
                        CloseHandle(lpOverlapped.hEvent)
                        raise ctypes.WinError()

                    bWaitAll = BOOL(False)
                    dwMilliseconds = DWORD(INFINITE)

                    lpEventAttributes = NULL
                    bManualReset = BOOL(False)
                    bInitialState = BOOL(False)
                    lpName = NULL

                    hEvent = self.hEvent = CreateEvent(
                        lpEventAttributes,
                        bManualReset,
                        bInitialState,
                        lpName
                    )

                    nCount = DWORD(2)
                    lpHandles = (HANDLE * 2)(lpOverlapped.hEvent, hEvent)

                    response = WaitForMultipleObjects(
                        nCount,
                        lpHandles,
                        bWaitAll,
                        dwMilliseconds
                    )

                    if response == WAIT_OBJECT_0:
                        bWait = BOOL(True)

                        if not GetOverlappedResult(
                            hDevice,
                            ctypes.byref(lpOverlapped),
                            ctypes.byref(lpNumberOfBytesTransferred),
                            bWait
                        ):
                            CancelIo(hDevice)
                            CloseHandle(hEvent)
                            self.hEvent = None
                            CloseHandle(lpOverlapped.hEvent)
                            raise ctypes.WinError()

                        CloseHandle(hEvent)

                    else:
                        CancelIo(hDevice)
                        CloseHandle(hEvent)
                        self.hEvent = None
                        CloseHandle(lpOverlapped.hEvent)
                        raise ctypes.WinError()

                CloseHandle(lpOverlapped.hEvent)

                if self._end_event.is_set():
                    exit_learn()
                    return

                byte_count = lpNumberOfBytesTransferred.value
                byte_count -= ((ctypes.sizeof(IR_ULONG_PTR) * 2) + ctypes.sizeof(ULONG))

                if not byte_count:
                    continue

                byte_count //= ctypes.sizeof(LONG)

                if frequency is None:
                    frequency = outBuffer.CarrierFrequency.value
                else:
                    frequency = max(frequency, outBuffer.CarrierFrequency.value)

                for i in range(byte_count):
                    item = outBuffer.Data[i]
                    result.append(item)

                    if item < -6500:
                        if len(result) > 5:
                            exit_learn()
                            return frequency, result[:]

                        del result[:]
                        frequency = None

            exit_learn()
            return 0, []

    def __get_first_rx_port(self):
        for i in range(32):
            if self._learn_mask & (1 << i) == 0:
                return i

    def __get_first_learn_port(self):
        for i in range(32):
            if self._learn_mask & (1 << i) != 0:
                return i

    @property
    def packet_timeout(self):
        return self._packet_timeout

    @packet_timeout.setter
    def packet_timeout(self, value):
        self._packet_timeout = value

    def test_tx_ports(self):
        rlc = [
            2650, -900,
            400, -500, 400, -500, 400, -950, 400, -950, 1300, -950, 400, -500, 400, -500, 400, -500,
            400, -500, 400, -500, 400, -500, 400, -500,  400, -500, 400, -500, 400, -500, 850, -500,
            400, -500, 400, -500, 400, -950, 400, -500,  400, -500, 400, -500, 400, -500, 850, -950,
            400, -500, 400, -500, 400, -500, 400, -500,  400, -500, 400, -500, 400, -500, 400, -500,
            850, -69700
        ]
        frequency = 38000

        inBuffer = IR_TRANSMIT_PARAMS()
        inBuffer.TransmitPortMask = IR_ULONG_PTR(0)
        inBuffer.CarrierPeriod = IR_ULONG_PTR(int(1000000.0 / frequency))
        inBuffer.Flags = IR_ULONG_PTR(0)
        inBuffer.PulseSize = IR_ULONG_PTR(0)

        outBuffer = IR_TRANSMIT_CHUNK()
        outBuffer.OffsetToNextChunk = IR_ULONG_PTR(0)
        outBuffer.RepeatCount = IR_ULONG_PTR(1)
        outBuffer.ByteCount = IR_ULONG_PTR(len(rlc))
        outBuffer.Data = (LONG * len(rlc))(*rlc)

        ports = {}
        for port in self.tx_ports:
            inBuffer.TransmitPortMask = IR_ULONG_PTR(0 | (1 << port))

            with self.handle as hDevice:
                ports[port] = _io_control(IOCTL_IR_TRANSMIT, hDevice, ctypes.byref(inBuffer), ctypes.byref(outBuffer))

        return ports

    def transmit(self, rlc, frequency=0, port=-1):
        # if isinstance(rlc, (list, tuple)):
        # elif isinstance(rlc, (decoder.RC6IRCode, decoder.IrCode)):
        #     frequency = rlc.frequency
        #     rlc = rlc.rlc_code

        inBuffer = IR_TRANSMIT_PARAMS()
        inBuffer.TransmitPortMask = IR_ULONG_PTR(0)
        inBuffer.CarrierPeriod = IR_ULONG_PTR(int(1000000.0 / frequency))
        inBuffer.Flags = IR_ULONG_PTR(0)
        inBuffer.PulseSize = IR_ULONG_PTR(0)

        outBuffer = IR_TRANSMIT_CHUNK()
        outBuffer.OffsetToNextChunk = IR_ULONG_PTR(0)
        outBuffer.RepeatCount = IR_ULONG_PTR(0)
        outBuffer.ByteCount = IR_ULONG_PTR(len(rlc))
        outBuffer.Data = (LONG * len(rlc))(*rlc)

        if port == -1:
            ports = 0

            for p in self.tx_ports:
                ports |= (1 << p)

            inBuffer.TransmitPortMask = IR_ULONG_PTR(ports)

        elif port in self.tx_ports:
            inBuffer.TransmitPortMask = IR_ULONG_PTR(0 | (1 << port))

        else:
            return False

        with self.handle as hDevice:
            _io_control(IOCTL_IR_TRANSMIT, hDevice, ctypes.byref(inBuffer), ctypes.byref(outBuffer))

        return True

    @property
    def num_connected_tx_ports(self):
        return len(self.tx_ports)

    @property
    def tx_ports(self):
        outBuffer = ULONG(0)
        ports = []

        with self.handle as hDevice:
            _io_control(IOCTL_IR_GET_EMITTERS, hDevice, NULL, outBuffer)

        for i in range(32):
            if outBuffer.value & (1 << i):
                ports += [i]

        return ports

    @property
    def num_rx_ports(self):
        return len(self.rx_ports)

    @property
    def rx_ports(self):
        ports = []

        for i in range(32):
            if self._learn_mask & (1 << i):
                ports += [i]

        return ports

    @property
    def can_flash_led(self):
        return bool(self._capabilities & DEV_CAPS_CAN_FLASH_RECEIVER_LED)

    @property
    def supports_wake(self):
        if self.version == 1:
            return False

        return bool(self._capabilities & V2_DEV_CAPS_SUPPORTS_WAKE)

    @property
    def supports_multiple_wake(self):
        if self.version == 1:
            return False

        return bool(self._capabilities & V2_DEV_CAPS_MULTIPLE_WAKE)

    @property
    def supports_programmable_wake(self):
        if self.version == 1:
            return False

        return bool(self._capabilities & V2_DEV_CAPS_PROGRAMMABLE_WAKE)

    @property
    def has_volitile_wake(self):
        if self.version == 1:
            return False

        return bool(self._capabilities & V2_DEV_CAPS_VOLATILE_WAKE_PATTERN)

    @property
    def is_learn_only(self):
        if self.version == 1:
            return False

        return bool(self._capabilities & V2_DEV_CAPS_LEARNING_ONLY)

    @property
    def has_narrow_bpf(self):
        if self.version == 1:
            return False

        return bool(self._capabilities & V2_DEV_CAPS_NARROW_BPF)

    @property
    def has_software_decode_input(self):
        if self.version == 1:
            return False

        return not bool(self._capabilities & V2_DEV_CAPS_NO_SWDECODE_INPUT)

    @property
    def has_hardware_decode_input(self):
        if self.version == 1:
            return False

        return bool(self._capabilities & V2_DEV_CAPS_HWDECODE_INPUT)

    @property
    def has_attached_tuner(self):
        if self.version == 1:
            return False

        return bool(self._capabilities & V2_DEV_CAPS_ATTACHED_TO_TUNER)

    @property
    def emulator_version(self):
        if self.version == 2:

            if bool(self._capabilities & V2_DEV_CAPS_EMULATOR_V1):
                return 1

            if bool(self._capabilities & V2_DEV_CAPS_EMULATOR_V2):
                return 2

    def reset(self):
        with self.handle as hDevice:
            return _io_control(IOCTL_IR_RESET_DEVICE, hDevice, NULL, NULL)

    def __del__(self):
        self.stop_receive()
