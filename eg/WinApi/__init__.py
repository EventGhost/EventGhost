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

# Local imports
import Clipboard  # NOQA
from cFunctions import (  # NOQA
    GetClassName,
    GetProcessName,
    GetTopLevelWindowList as _GetTopLevelWindowList,
    GetWindowChildsList,
    GetWindowText,
)
from Dynamic import (  # NOQA
    WM_COMMAND,
    WM_USER,
)
from Utils import (  # NOQA
    BestWindowFromPoint,
    HighlightWindow,
    IsWin64,
    PyEnumProcesses as EnumProcesses,
    PyFindWindow as FindWindow,
    PyGetCursorPos as GetCursorPos,
    PyGetWindowThreadProcessId as GetWindowThreadProcessId,
    PySendMessageTimeout as SendMessageTimeout,
)

def GetTopLevelWindowList(includeInvisible):
    """
    cFunctions.GetTopLevelWindowList() may return hwnds that are a larger
    positive number than can be converted to a signed int. We need to convert
    such hwnds to a negative value before passing them to any function that
    takes a hwnd.
    """
    topWindowsHwnds = _GetTopLevelWindowList(includeInvisible)

    for i, hwnd in enumerate(topWindowsHwnds):
        if hwnd & 0x80000000:
            hwnd2 = hwnd - 0x100000000
            #print 'hwnd too large: %s -> %s' % (hwnd, hwnd2)
            topWindowsHwnds[i] = hwnd2

    return topWindowsHwnds
