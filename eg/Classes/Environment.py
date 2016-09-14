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

import os
import winreg
from collections import OrderedDict

class Environment:
    IGNORE_LIST = (
        "PROCESSOR_ARCHITECTURE",
        "USERNAME",
    )

    KEY_LIST = (
        (
            winreg.HKEY_LOCAL_MACHINE,
            "System\CurrentControlSet\Control\Session Manager\Environment"
        ),
        (
            winreg.HKEY_CURRENT_USER,
            "Environment"
        ),
    )

    PROTECTED_VARS = {}

    @staticmethod
    def AppendPath(val):
        if os.environ.get("PATH"):
            path = os.environ["PATH"] + os.pathsep + val
        else:
            path = val
        Environment.Set("PATH", path)

    @staticmethod
    def Clear():
        os.environ.clear()

    @staticmethod
    def ClearSafe():
        for var in os.environ.keys():
            if var not in Environment.PROTECTED_VARS:
                del os.environ[var]

    @staticmethod
    def Get():
        return Environment.Sort(os.environ)

    @staticmethod
    def GetLatest():
        result = {}

        for key, subkey in Environment.KEY_LIST:
            try:
                i = 0
                with winreg.OpenKey(key, subkey) as hand:
                    while True:
                        var, val = winreg.EnumValue(hand, i)[:2]
                        if var not in Environment.IGNORE_LIST:
                            if var.upper() == "PATH":
                                if "PATH" in result:
                                    result["PATH"] += os.pathsep + val
                                else:
                                    result["PATH"] = val
                            else:
                                result[var] = val
                        i += 1
            except WindowsError:
                pass

        return Environment.Sort(result)

    @staticmethod
    def Refresh():
        Environment.ClearSafe()

        for var, val in Environment.GetLatest().iteritems():
            Environment.Set(var, val)

    @staticmethod
    def Set(var, val):
        os.environ[var] = os.path.expandvars(val)

    @staticmethod
    def Sort(data):
        return OrderedDict(sorted(data.items(), key=lambda i: i[0]))


for var in set(os.environ).difference(Environment.GetLatest()).union(Environment.IGNORE_LIST):
    if var.upper() != "PATH":
        Environment.PROTECTED_VARS[var] = os.environ[var]
