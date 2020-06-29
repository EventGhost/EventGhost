# -*- coding: utf-8 -*-
import ctypes
from ctypes.wintypes import HANDLE, DWORD

kernel32 = ctypes.windll.Kernel32


# WINBASEAPI
# _Ret_maybenull_
# HANDLE
# WINAPI
# CreateEventW(
# _In_opt_ LPSECURITY_ATTRIBUTES lpEventAttributes,
# _In_ BOOL bManualReset,
# _In_ BOOL bInitialState,
# _In_opt_ LPCWSTR lpName
# );
CreateEventW = kernel32.CreateEventW
CreateEventW.restype = HANDLE
CreateEvent = CreateEventW

# WINBASEAPI
# DWORD
# WINAPI
# WaitForMultipleObjects(
# _In_ DWORD nCount,
# _In_reads_(nCount) CONST HANDLE* lpHandles,
# _In_ BOOL bWaitAll,
# _In_ DWORD dwMilliseconds
# );
WaitForMultipleObjects = kernel32.WaitForMultipleObjects
WaitForMultipleObjects.restype = DWORD
