# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

from ctypes import byref, sizeof, Structure, windll
from ctypes.wintypes import BYTE, DWORD, LPVOID, POINTER, WCHAR, WORD

VER_NT_WORKSTATION = 1
VER_SUITE_ENTERPRISE = 0x0002
VER_SUITE_DATACENTER = 0x0080
VER_SUITE_PERSONAL = 0x0200
VER_SUITE_BLADE = 0x0400
VER_SUITE_STORAGE_SERVER = 0x2000
VER_SUITE_COMPUTE_SERVER = 0x4000
VER_SUITE_WH_SERVER = 0x8000
PROCESSOR_ARCHITECTURE_IA64 = 6
PROCESSOR_ARCHITECTURE_AMD64 = 9
SM_TABLETPC = 86
SM_MEDIACENTER = 87
SM_STARTER = 88
SM_SERVERR2 = 89

EDITIONS = {
    0x06: "%s Business",
    0x10: "%s Business N",
    0x12: "%s HPC Edition",
    0x08: "%s Datacenter (full installation)",
    0x0C: "%s Datacenter (core installation)",
    0x27: "%s Datacenter without Hyper-V (core installation)",
    0x25: "%s Datacenter without Hyper-V (full installation)",
    0x04: "%s Enterprise",
    0x46: "%s Enterprise E",
    0x1B: "%s Enterprise N",
    0x0A: "%s Enterprise (full installation)",
    0x0E: "%s Enterprise (core installation)",
    0x29: "%s Enterprise without Hyper-V (core installation)",
    0x0F: "%s Enterprise for Itanium-based Systems",
    0x26: "%s Enterprise without Hyper-V (full installation)",
    0x02: "%s Home Basic",
    0x43: "%s Home Basic E",
    0x05: "%s Home Basic N",
    0x03: "%s Home Premium",
    0x44: "%s Home Premium E",
    0x1A: "%s Home Premium N",
    0x2A: "Microsoft Hyper-V %s",
    0x1E: "Windows Essential Business %s Management Server",
    0x20: "Windows Essential Business %s Messaging Server",
    0x1F: "Windows Essential Business %s Security Server",
    0x30: "%s Professional",
    0x45: "%s Professional E",
    0x31: "%s Professional N",
    0x18: "Windows %s for Windows Essential Server Solutions",
    0x23: "Windows %s without Hyper-V for Windows Essential Server Solutions",
    0x21: "%s Foundation",
    0x09: "Windows Small Business %s",
    0x07: "%s Standard (full installation)",
    0x0D: "%s Standard (core installation)",
    0x28: "%s Standard without Hyper-V (core installation)",
    0x24: "%s Standard without Hyper-V (full installation)",
    0x0B: "%s Starter",
    0x42: "%s Starter E",
    0x2F: "%s Starter N",
    0x17: "Storage %s Enterprise",
    0x14: "Storage %s Express",
    0x15: "Storage %s Standard",
    0x16: "Storage %s Workgroup",
    0x00: "%s An unknown product",
    0x01: "%s Ultimate",
    0x47: "%s Ultimate E",
    0x1C: "%s Ultimate N",
    0x11: "Web %s (full installation)",
    0x1D: "Web %s (core installation)",
}

GetSystemMetrics = windll.user32.GetSystemMetrics

class OSVERSIONINFOEX(Structure):
    _fields_ = [
        ('dwOSVersionInfoSize', DWORD),
        ('dwMajorVersion', DWORD),
        ('dwMinorVersion', DWORD),
        ('dwBuildNumber', DWORD),
        ('dwPlatformId', DWORD),
        ('szCSDVersion', WCHAR * 128),
        ('wServicePackMajor', WORD),
        ('wServicePackMinor', WORD),
        ('wSuiteMask', WORD),
        ('wProductType', BYTE),
        ('wReserved', BYTE),
    ]


class SYSTEM_INFO(Structure):
    _fields_ = [
        ('wProcessorArchitecture', WORD),
        ('wReserved', WORD),
        ('dwPageSize', DWORD),
        ('lpMinimumApplicationAddress', LPVOID),
        ('lpMaximumApplicationAddress', LPVOID),
        ('dwActiveProcessorMask', POINTER(DWORD)),
        ('dwNumberOfProcessors', DWORD),
        ('dwProcessorType', DWORD),
        ('dwAllocationGranularity', DWORD),
        ('wProcessorLevel', WORD),
        ('wProcessorRevision', WORD),
    ]


def GetWindowsVersionString():
    system_info = SYSTEM_INFO()
    osvi = OSVERSIONINFOEX()
    osvi.dwOSVersionInfoSize = sizeof(OSVERSIONINFOEX)
    windll.kernel32.GetVersionExW(byref(osvi))
    try:
        MyGetSystemInfo = windll.kernel32.GetNativeSystemInfo
    except AttributeError:
        MyGetSystemInfo = windll.kernel32.GetSystemInfo
    MyGetSystemInfo(byref(system_info))
    name = ""
    major_version = osvi.dwMajorVersion
    minor_version = osvi.dwMinorVersion

    if major_version == 5:
        suiteMask = osvi.wSuiteMask
        if minor_version == 0:
            if osvi.wProductType == VER_NT_WORKSTATION:
                name = "2000 Professional"
            else:
                if suiteMask & VER_SUITE_DATACENTER:
                    name = "2000 Datacenter Server"
                elif suiteMask & VER_SUITE_ENTERPRISE:
                    name = "2000 Advanced Server"
                else:
                    name = "2000 Server"
        elif minor_version == 1:
            if GetSystemMetrics(SM_MEDIACENTER):
                name = "XP Media Center Edition"
            elif GetSystemMetrics(SM_TABLETPC):
                name = "XP Tablet PC Edition"
            elif GetSystemMetrics(SM_STARTER):
                name = "XP Starter Edition"
            elif suiteMask & VER_SUITE_PERSONAL:
                name = "XP Home Edition"
            else:
                name = "XP Professional"
        elif minor_version == 2:
            if GetSystemMetrics(SM_SERVERR2):
                name = "Server 2003 R2"
            elif suiteMask == VER_SUITE_STORAGE_SERVER:
                name = "Storage Server 2003"
            elif suiteMask == VER_SUITE_WH_SERVER:
                name = "Home Server"
            elif osvi.wProductType == VER_NT_WORKSTATION:
                # Windows XP Professional x64 Edition
                name = "XP Professional"
            else:
                name = "Server 2003"
            if osvi.wProductType != VER_NT_WORKSTATION:
                if suiteMask & VER_SUITE_COMPUTE_SERVER:
                    name += " Compute Cluster Edition"
                elif suiteMask & VER_SUITE_DATACENTER:
                    name += " Datacenter Edition"
                elif suiteMask & VER_SUITE_ENTERPRISE:
                    name += " Enterprise Edition"
                elif suiteMask & VER_SUITE_BLADE:
                    name += " Web Edition"
                else:
                    name += " Standard Edition"
    elif major_version >= 6:
        try:
            os_type = {
                (6, 0, True): "Vista",
                (6, 0, False): "Server 2008",
                (6, 1, True): "7",
                (6, 1, False): "Server 2008 R2",
                (6, 2, True): "8",
                (6, 2, False): "Server 2012",
                (6, 3, True): "8.1",
                (6, 3, False): "Server 2012 R2",
                (10, 0, True): "10",
                (10, 0, False): "Server 2016",
            }[(
                major_version,
                minor_version,
                osvi.wProductType == VER_NT_WORKSTATION,
            )]
        except KeyError:
            os_type = "Unknown OS %d.%d" % (major_version, minor_version)
        dwType = DWORD()
        windll.kernel32.GetProductInfo(
            major_version, minor_version, 0, 0, byref(dwType)
        )
        try:
            name = EDITIONS[dwType.value] % os_type
        except KeyError:
            name = "%s (Unknown Edition %d)" % (os_type, dwType.value)

    if osvi.wServicePackMajor:
        name += " SP%d" % osvi.wServicePackMajor
        if osvi.wServicePackMinor:
            name += ".%d" % osvi.wServicePackMinor

    if system_info.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_AMD64:
        name += ", 64-bit"
    elif system_info.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_IA64:
        name += ", Itanium"
    else:
        name += ", 32-bit"
    name += " (build %d)" % osvi.dwBuildNumber
    return "Microsoft Windows " + name

if __name__ == "__main__":
    print GetWindowsVersionString()
