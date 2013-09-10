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

from Utils import PyGetCursorPos as GetCursorPos
from Utils import PyGetWindowThreadProcessId as GetWindowThreadProcessId
from Utils import PyEnumProcesses as EnumProcesses
from Utils import PySendMessageTimeout as SendMessageTimeout
from Utils import PyFindWindow as FindWindow
from Utils import HighlightWindow, BestWindowFromPoint, IsWin64

from cFunctions import (
    GetWindowText,
    GetClassName,
    GetProcessName,
    GetTopLevelWindowList as _GetTopLevelWindowList,
    GetWindowChildsList,
)
from Dynamic import (
    WM_COMMAND,
    WM_USER,
)
import Clipboard

def GetTopLevelWindowList(includeInvisible):
    """cFunctions.GetTopLevelWindowList() may return hwnds that are a larger positive number than can be converted
    to a signed int. We need to convert such hwnds to a negative value before passing them to any function that
    takes a hwnd."""

    topWindowsHwnds = _GetTopLevelWindowList(includeInvisible)

    for i, hwnd in enumerate(topWindowsHwnds):
        if hwnd & 0x80000000:
            hwnd2 = hwnd - 0x100000000
            #print 'hwnd too large: %s -> %s' % (hwnd, hwnd2)
            topWindowsHwnds[i] = hwnd2

    return topWindowsHwnds