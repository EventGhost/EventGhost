# -*- coding: utf-8 -*-
import ctypes
from ctypes.wintypes import BOOL

kernel32 = ctypes.windll.Kernel32

# WINBASEAPI
# BOOL
# WINAPI
# CancelIo(
# _In_ HANDLE hFile
# );
CancelIo = kernel32.CancelIo
CancelIo.restype = BOOL
