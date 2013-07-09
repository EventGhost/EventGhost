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

from eg.WinApi.Dynamic import *
_Mpr = WinDLL("Mpr")
import sys
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
                "#include <Winnetwk.h>\n"
            )
        except WindowsError:
            print "GCC_XML most likely not installed"
# everything after the following line is automatically created
#-----------------------------------------------------------------------------#
WNetGetUniversalNameW = _Mpr.WNetGetUniversalNameW
WNetGetUniversalNameW.restype = DWORD
WNetGetUniversalNameW.argtypes = [LPCWSTR, DWORD, LPVOID, LPDWORD]
WNetGetUniversalName = WNetGetUniversalNameW # alias
UNIVERSAL_NAME_INFO_LEVEL = 1 # Variable c_int '1'
class _UNIVERSAL_NAME_INFOW(Structure):
    pass
UNIVERSAL_NAME_INFOW = _UNIVERSAL_NAME_INFOW
UNIVERSAL_NAME_INFO = UNIVERSAL_NAME_INFOW
_UNIVERSAL_NAME_INFOW._fields_ = [
    ('lpUniversalName', LPWSTR),
]
NO_ERROR = 0 # Variable c_long '0l'
ERROR_NO_NET_OR_BAD_PATH = 1203 # Variable c_long '1203l'
ERROR_BAD_DEVICE = 1200 # Variable c_long '1200l'
ERROR_NOT_SUPPORTED = 50 # Variable c_long '50l'

