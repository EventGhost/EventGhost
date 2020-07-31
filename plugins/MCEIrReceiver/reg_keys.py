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

import _winreg

REG_PATH = 'SYSTEM\\CurrentControlSet\\Services\\HidIr\\Remotes'


def _set_value(path, key, name, value):
    try:
        handle = _winreg.OpenKey(
            _winreg.HKEY_LOCAL_MACHINE,
            path + '\\' + key,
            0,
            _winreg.KEY_ALL_ACCESS
        )
    except WindowsError:
        return False

    try:
        _winreg.SetValueEx(handle, name, 0, _winreg.REG_DWORD, value)
        return True
    except WindowsError:
        return False
    finally:
        _winreg.CloseKey(handle)


def _delete_value(path, key, value):
    try:
        handle = _winreg.OpenKey(
            _winreg.HKEY_LOCAL_MACHINE,
            path + '\\' + key,
            0,
            _winreg.KEY_ALL_ACCESS
        )
    except WindowsError:
        return False

    try:
        _winreg.DeleteValue(handle, value)
        return True
    except WindowsError:
        return False
    finally:
        _winreg.CloseKey(handle)


def _read_reg_keys(key):
    try:
        handle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, key, 0, _winreg.KEY_ALL_ACCESS)
    except WindowsError:
        return []

    res = []

    for i in range(_winreg.QueryInfoKey(handle)[0]):
        res += [_winreg.EnumKey(handle, i)]

    _winreg.CloseKey(handle)
    return res


def remove_keys():
    res = False

    for key in _read_reg_keys(REG_PATH):
        res = True if _delete_value(REG_PATH, key, 'CodeSetNum0') else res
        res = True if _delete_value(REG_PATH, key, 'CodeSetNum1') else res
        res = True if _delete_value(REG_PATH, key, 'CodeSetNum2') else res
        res = True if _delete_value(REG_PATH, key, 'CodeSetNum3') else res

    return res


def add_keys():
    res = False

    for key in _read_reg_keys(REG_PATH):
        res = True if _set_value(REG_PATH, key, 'CodeSetNum0', 1) else res
        res = True if _set_value(REG_PATH, key, 'CodeSetNum1', 2) else res
        res = True if _set_value(REG_PATH, key, 'CodeSetNum2', 3) else res
        res = True if _set_value(REG_PATH, key, 'CodeSetNum3', 4) else res

    return res
