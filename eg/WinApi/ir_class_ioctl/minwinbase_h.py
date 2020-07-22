# -*- coding: utf-8 -*-
import ctypes
from ctypes.wintypes import LPVOID, DWORD, HANDLE

if ctypes.sizeof(ctypes.c_void_p) == 8:
    ULONG_PTR = ctypes.c_ulonglong
else:
    ULONG_PTR = ctypes.c_ulong


POINTER = ctypes.POINTER


class _OVERLAPPED(ctypes.Structure):
    class _DUMMYUNIONNAME(ctypes.Union):
        class _DUMMYSTRUCTNAME(ctypes.Structure):
            _fields_ = [
                ('Offset', DWORD),
                ('OffsetHigh', DWORD),
            ]

        _fields_ = [
            ('DUMMYSTRUCTNAME', _DUMMYSTRUCTNAME),
            ('Pointer', LPVOID),
        ]

    _fields_ = [
        ('Internal', ULONG_PTR),
        ('InternalHigh', ULONG_PTR),
        ('DUMMYUNIONNAME', _DUMMYUNIONNAME),
        ('hEvent', HANDLE),
    ]


OVERLAPPED = _OVERLAPPED
LPOVERLAPPED = POINTER(_OVERLAPPED)
