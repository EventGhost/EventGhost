# -*- coding: utf-8 -*-
import ctypes
from ctypes.wintypes import HANDLE


kernel32 = ctypes.windll.Kernel32

OPEN_EXISTING = 3

# WINBASEAPI
# HANDLE
# WINAPI

# CreateFileW(
# _In_ LPCWSTR lpFileName,
# _In_ DWORD dwDesiredAccess,
# _In_ DWORD dwShareMode,
# _In_opt_ LPSECURITY_ATTRIBUTES lpSecurityAttributes,
# _In_ DWORD dwCreationDisposition,
# _In_ DWORD dwFlagsAndAttributes,
# _In_opt_ HANDLE hTemplateFile
# );
CreateFileW = kernel32.CreateFileW
CreateFileW.restype = HANDLE
CreateFile = CreateFileW
