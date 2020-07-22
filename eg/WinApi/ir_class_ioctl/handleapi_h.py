# -*- coding: utf-8 -*-
import ctypes
from ctypes.wintypes import BOOL


kernel32 = ctypes.windll.Kernel32

INVALID_HANDLE_VALUE = -1

# WINBASEAPI
# BOOL
# WINAPI
# CloseHandle(
# _In_ _Post_ptr_invalid_ HANDLE hObject
# );
CloseHandle = kernel32.CloseHandle
CloseHandle.restype = BOOL
