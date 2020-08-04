# -*- coding: utf-8 -*-
import ctypes
from ctypes.wintypes import BOOL

kernel32 = ctypes.windll.Kernel32

# WINBASEAPI
# BOOL
# WINAPI
# DeviceIoControl(
# _In_ HANDLE hDevice,
# _In_ DWORD dwIoControlCode,
# _In_reads_bytes_opt_(nInBufferSize) LPVOID lpInBuffer,
# _In_ DWORD nInBufferSize,
# _Out_writes_bytes_to_opt_(nOutBufferSize,*lpBytesReturned) LPVOID lpOutBuffer,
# _In_ DWORD nOutBufferSize,
# _Out_opt_ LPDWORD lpBytesReturned,
# _Inout_opt_ LPOVERLAPPED lpOverlapped
# );
DeviceIoControl = kernel32.DeviceIoControl
DeviceIoControl.restype = BOOL

# WINBASEAPI
# BOOL
# WINAPI
# GetOverlappedResult(
# _In_ HANDLE hFile,
# _In_ LPOVERLAPPED lpOverlapped,
# _Out_ LPDWORD lpNumberOfBytesTransferred,
# _In_ BOOL bWait
# );
GetOverlappedResult = kernel32.GetOverlappedResult
GetOverlappedResult.restype = BOOL
