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

import _winreg as reg


def remove_keys():
    key1 = 'SYSTEM\\CurrentControlSet\\Services\\HidIr\\Remotes\\745a17a0-74d3-11d0-b6fe-00a0c90f57da'
    key2 = 'SYSTEM\\CurrentControlSet\\Services\\HidIr\\Remotes\\745a17a0-74d3-11d0-b6fe-00a0c90f57db'

    key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, key1, 0, reg.KEY_ALL_ACCESS)
    reg.DeleteValue(key, 'CodeSetNum0')
    reg.DeleteValue(key, 'CodeSetNum1')
    reg.DeleteValue(key, 'CodeSetNum2')
    reg.DeleteValue(key, 'CodeSetNum3')
    reg.CloseKey(key)

    key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, key2, 0, reg.KEY_ALL_ACCESS)
    reg.DeleteValue(key, 'CodeSetNum0')
    reg.DeleteValue(key, 'CodeSetNum1')
    reg.DeleteValue(key, 'CodeSetNum2')
    reg.DeleteValue(key, 'CodeSetNum3')

    reg.CloseKey(key)


def add_keys():
    key1 = 'SYSTEM\\CurrentControlSet\\Services\\HidIr\\Remotes\\745a17a0-74d3-11d0-b6fe-00a0c90f57da'
    key2 = 'SYSTEM\\CurrentControlSet\\Services\\HidIr\\Remotes\\745a17a0-74d3-11d0-b6fe-00a0c90f57db'

    key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, key1, 0, reg.KEY_ALL_ACCESS)
    reg.SetValueEx(key, 'CodeSetNum0', 0, reg.REG_DWORD, 1)
    reg.SetValueEx(key, 'CodeSetNum1', 0, reg.REG_DWORD, 2)
    reg.SetValueEx(key, 'CodeSetNum2', 0, reg.REG_DWORD, 3)
    reg.SetValueEx(key, 'CodeSetNum3', 0, reg.REG_DWORD, 4)

    key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, key2, 0, reg.KEY_ALL_ACCESS)
    reg.SetValueEx(key, 'CodeSetNum0', 0, reg.REG_DWORD, 1)
    reg.SetValueEx(key, 'CodeSetNum1', 0, reg.REG_DWORD, 2)
    reg.SetValueEx(key, 'CodeSetNum2', 0, reg.REG_DWORD, 3)
    reg.SetValueEx(key, 'CodeSetNum3', 0, reg.REG_DWORD, 4)

    reg.CloseKey(key)
