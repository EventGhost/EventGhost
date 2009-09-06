# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

#pylint: disable-msg=C0103,C0301,C0302

# This file gets automatically extended by ctypeslib.dynamic_module, so don't
# edit it yourself.

import sys
from eg.WinApi import IsWin64
from eg.WinApi.Dynamic import *
if IsWin64():
    _Difxapi = WinDLL("DIFxAPI64")
else:
    _Difxapi = WinDLL("DIFxAPI32")
if not hasattr(sys, "frozen"): # detect py2exe
    try:
        ctypeslib = __import__("ctypeslib.dynamic_module")
    except ImportError :
        print "ctypeslib is not installed!"
    else:
        try:
            ctypeslib.dynamic_module.include(
                "#define UNICODE\n"
                "#define _WIN32_WINNT 0x500\n"
                "#define WIN32_LEAN_AND_MEAN\n"
                "#define NO_STRICT\n"
                "#include <windows.h>\n"
                "#include <Difxapi.h>\n"
            )
        except WindowsError:
            print "GCC_XML most likely not installed"
# everything after the following line is automatically created
#-----------------------------------------------------------------------------#
WSTRING = c_wchar_p

# values for enumeration 'DIFXAPI_LOG'
DIFXAPI_SUCCESS = 0
DIFXAPI_INFO = 1
DIFXAPI_WARNING = 2
DIFXAPI_ERROR = 3
DIFXAPI_LOG = c_int # enum
PCWSTR = WSTRING
DIFXLOGCALLBACK_W = WINFUNCTYPE(None, DIFXAPI_LOG, DWORD, PCWSTR, PVOID)
DIFLOGCALLBACK = DIFXLOGCALLBACK_W # alias
SetDifxLogCallbackW = _Difxapi.SetDifxLogCallbackW
SetDifxLogCallbackW.restype = None
SetDifxLogCallbackW.argtypes = [DIFXLOGCALLBACK_W, PVOID]
SetDifxLogCallback = SetDifxLogCallbackW # alias
class INSTALLERINFO_W(Structure):
    pass
PINSTALLERINFO_W = POINTER(INSTALLERINFO_W)
PCINSTALLERINFO_W = PINSTALLERINFO_W
DriverPackageInstallW = _Difxapi.DriverPackageInstallW
DriverPackageInstallW.restype = DWORD
DriverPackageInstallW.argtypes = [PCWSTR, DWORD, PCINSTALLERINFO_W, POINTER(BOOL)]
DriverPackageInstall = DriverPackageInstallW # alias
PWSTR = WSTRING
INSTALLERINFO_W._fields_ = [
    ('pApplicationId', PWSTR),
    ('pDisplayName', PWSTR),
    ('pProductName', PWSTR),
    ('pMfgName', PWSTR),
]
DRIVER_PACKAGE_FORCE = 4 # Variable c_int '4'
DRIVER_PACKAGE_LEGACY_MODE = 16 # Variable c_int '16'

