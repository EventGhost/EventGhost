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

#pylint: disable-msg=C0103,C0301,C0302

# This file gets automatically extended by ctypeslib.dynamic_module, so don't
# edit it yourself.

import sys

# Local imports
from eg.WinApi.Dynamic import *

_psapi = WinDLL("Psapi")
if __name__ == "__main__":
    try:
        ctypeslib = __import__("ctypeslib.dynamic_module")
    except ImportError:
        print "ctypeslib is not installed!"
    else:
        try:
            ctypeslib.dynamic_module.include(
                "#define UNICODE\n"
                "#define _WIN32_WINNT 0x500\n"
                "#define WIN32_LEAN_AND_MEAN\n"
                "#define NO_STRICT\n"
                "#include <windows.h>\n"
                "#include <Psapi.h>\n"
            )
        except WindowsError:
            print "GCC_XML most likely not installed"

#-----------------------------------------------------------------------------#
# everything after the following line is automatically created
#-----------------------------------------------------------------------------#
EnumProcesses = _psapi.EnumProcesses
EnumProcesses.restype = BOOL
EnumProcesses.argtypes = [POINTER(DWORD), DWORD, LPDWORD]
