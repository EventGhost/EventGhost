# -*- coding: utf-8 -*-
import ctypes
from ctypes.wintypes import LPVOID, BOOL, DWORD, WCHAR
from guiddef_h import GUID


if ctypes.sizeof(ctypes.c_void_p) == 8:
    ULONG_PTR = ctypes.c_ulonglong
else:
    ULONG_PTR = ctypes.c_ulong

HDEVINFO = LPVOID
POINTER = ctypes.POINTER

# Flags controlling what is included in the device information set built by SetupDiGetClassDevs
DIGCF_DEFAULT = 0x00000001
DIGCF_PRESENT = 0x00000002
DIGCF_ALLCLASSES = 0x00000004
DIGCF_PROFILE = 0x00000008
DIGCF_DEVICEINTERFACE = 0x00000010

setupapi = ctypes.windll.SetupApi

# WINSETUPAPI
# HDEVINFO
# WINAPI
# SetupDiGetClassDevsW(
# _In_opt_ CONST GUID *ClassGuid,
# _In_opt_ PCWSTR Enumerator,
# _In_opt_ HWND hwndParent,
# _In_ DWORD Flags
# );
SetupDiGetClassDevsW = setupapi.SetupDiGetClassDevsW
SetupDiGetClassDevsW.restype = HDEVINFO
SetupDiGetClassDevs = SetupDiGetClassDevsW

# WINSETUPAPI
# BOOL
# WINAPI
# SetupDiEnumDeviceInfo(
# _In_ HDEVINFO DeviceInfoSet,
# _In_ DWORD MemberIndex,
# _Out_ PSP_DEVINFO_DATA DeviceInfoData
# );
SetupDiEnumDeviceInfo = setupapi.SetupDiEnumDeviceInfo
SetupDiEnumDeviceInfo.restype = BOOL

# WINSETUPAPI
# BOOL
# WINAPI
# SetupDiEnumDeviceInterfaces(
# _In_ HDEVINFO DeviceInfoSet,
# _In_opt_ PSP_DEVINFO_DATA DeviceInfoData,
# _In_ CONST GUID *InterfaceClassGuid,
# _In_ DWORD MemberIndex,
# _Out_ PSP_DEVICE_INTERFACE_DATA DeviceInterfaceData
# );
SetupDiEnumDeviceInterfaces = setupapi.SetupDiEnumDeviceInterfaces
SetupDiEnumDeviceInterfaces.restype = BOOL

# WINSETUPAPI
# BOOL
# WINAPI
# SetupDiGetDeviceInterfaceDetailW(
# _In_ HDEVINFO DeviceInfoSet,
# _In_ PSP_DEVICE_INTERFACE_DATA DeviceInterfaceData,
# _Out_writes_bytes_to_opt_(
# DeviceInterfaceDetailDataSize, *RequiredSize) PSP_DEVICE_INTERFACE_DETAIL_DATA_W DeviceInterfaceDetailData,
# _In_ DWORD DeviceInterfaceDetailDataSize,
# _Out_opt_ _Out_range_(>=, sizeof(SP_DEVICE_INTERFACE_DETAIL_DATA_W)) PDWORD RequiredSize,
# _Out_opt_ PSP_DEVINFO_DATA DeviceInfoData
# );
SetupDiGetDeviceInterfaceDetailW = setupapi.SetupDiGetDeviceInterfaceDetailW
SetupDiGetDeviceInterfaceDetailW.restype = BOOL
SetupDiGetDeviceInterfaceDetail = SetupDiGetDeviceInterfaceDetailW

# WINSETUPAPI
# BOOL
# WINAPI
# SetupDiDestroyDeviceInfoList(
# _In_ HDEVINFO DeviceInfoSet
# );
SetupDiDestroyDeviceInfoList = setupapi.SetupDiDestroyDeviceInfoList
SetupDiDestroyDeviceInfoList.restype = BOOL

# WINSETUPAPI BOOL SetupDiGetDevicePropertyW(
#   HDEVINFO         DeviceInfoSet,
#   PSP_DEVINFO_DATA DeviceInfoData,
#   const DEVPROPKEY *PropertyKey,
#   DEVPROPTYPE      *PropertyType,
#   PBYTE            PropertyBuffer,
#   DWORD            PropertyBufferSize,
#   PDWORD           RequiredSize,
#   DWORD            Flags
# );
SetupDiGetDevicePropertyW = setupapi.SetupDiGetDevicePropertyW
SetupDiGetDevicePropertyW.restype = BOOL


class _SP_DEVINFO_DATA(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('cbSize', DWORD),
        ('ClassGuid', GUID),
        ('DevInst', DWORD),  # DEVINST handle
        ('Reserved', ULONG_PTR),
    ]


SP_DEVINFO_DATA = _SP_DEVINFO_DATA
PSP_DEVINFO_DATA = POINTER(_SP_DEVINFO_DATA)


class _SP_DEVICE_INTERFACE_DATA(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('cbSize', DWORD),
        ('InterfaceClassGuid', GUID),
        ('Flags', DWORD),
        ('Reserved', ULONG_PTR),
    ]


SP_DEVICE_INTERFACE_DATA = _SP_DEVICE_INTERFACE_DATA
PSP_DEVICE_INTERFACE_DATA = POINTER(_SP_DEVICE_INTERFACE_DATA)


class _SP_DEVICE_INTERFACE_DETAIL_DATA_W(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('cbSize', DWORD),
        ('DevicePath', WCHAR * 1)
    ]


SP_DEVICE_INTERFACE_DETAIL_DATA_W = _SP_DEVICE_INTERFACE_DETAIL_DATA_W
PSP_DEVICE_INTERFACE_DETAIL_DATA_W = POINTER(_SP_DEVICE_INTERFACE_DETAIL_DATA_W)

SP_DEVICE_INTERFACE_DETAIL_DATA = SP_DEVICE_INTERFACE_DETAIL_DATA_W
PSP_DEVICE_INTERFACE_DETAIL_DATA = PSP_DEVICE_INTERFACE_DETAIL_DATA_W
