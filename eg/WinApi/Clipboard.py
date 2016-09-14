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

from time import sleep
import ctypes

# Local imports
import eg
from Dynamic import (
    c_char_p,
    c_wchar_p,
    cast,
    CF_TEXT,
    CF_UNICODETEXT,
    CloseClipboard,
    create_unicode_buffer,
    EmptyClipboard,
    GetClipboardData,
    GHND,
    GlobalAlloc,
    GlobalLock,
    GlobalUnlock,
    OpenClipboard,
    SetClipboardData,
    sizeof,
)

memcpy = ctypes.cdll.msvcrt.memcpy

def GetClipboardText():
    if not SafeOpenClipboard():
        return
    text = u""

    try:
        hClipMem = GetClipboardData(CF_UNICODETEXT)
        if hClipMem:
            text = cast(GlobalLock(hClipMem), c_wchar_p).value
            GlobalUnlock(hClipMem)
        else:
            hClipMem = GetClipboardData(CF_TEXT)
            if hClipMem:
                text = cast(GlobalLock(hClipMem), c_char_p).value
                GlobalUnlock(hClipMem)
                text = text.decode(eg.systemEncoding)
    finally:
        CloseClipboard()

    # replace CR+LF with \n
    text = text.replace("\r\n", "\n")
    return text

def SafeOpenClipboard():
    # some programs seem to poll the clipboard and therefore OpenClipboard
    # returns FALSE. To increase our chances to get the clipboard lock, we
    # try it ten times with a small delay in-between.
    i = 0
    while not OpenClipboard(0):
        i += 1
        if i >= 10:
            return False
        sleep(0.01)
    return True

def SetClipboardText(text):
    charBuffer = create_unicode_buffer(text)
    charBufferSize = sizeof(charBuffer)
    hGlobalMem = GlobalAlloc(GHND, charBufferSize)
    lpGlobalMem = GlobalLock(hGlobalMem)
    memcpy(lpGlobalMem, charBuffer, charBufferSize)
    GlobalUnlock(hGlobalMem)
    if not SafeOpenClipboard():
        return
    try:
        EmptyClipboard()
        SetClipboardData(CF_UNICODETEXT, hGlobalMem)
    finally:
        CloseClipboard()
