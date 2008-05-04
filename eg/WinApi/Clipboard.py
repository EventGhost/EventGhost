# This file is part of EventGhost.
# Copyright (C) 2008 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate: 2007-12-12 21:48:49 +0100 (Mi, 12 Dez 2007) $
# $LastChangedRevision: 314 $
# $LastChangedBy: bitmonster $

from time import sleep
from eg.WinApi.Dynamic import (
    cast,
    sizeof,
    create_unicode_buffer,
    c_char_p,
    c_wchar_p,
    OpenClipboard,
    EmptyClipboard,
    CloseClipboard,
    GetClipboardData,
    SetClipboardData,
    GlobalLock,
    GlobalUnlock,
    GlobalAlloc,
    CF_TEXT,
    CF_UNICODETEXT,
    GHND,
)
import ctypes
memcpy = ctypes.cdll.msvcrt.memcpy

    
def SaveOpenClipboard():
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
    

def GetClipboardText():
    if not SaveOpenClipboard():
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


def SetClipboardText(text):
    buffer = create_unicode_buffer(text)      
    bufferSize = sizeof(buffer)
    hGlobalMem = GlobalAlloc(GHND, bufferSize)
    lpGlobalMem = GlobalLock(hGlobalMem)
    memcpy(lpGlobalMem, buffer, bufferSize) 
    GlobalUnlock(hGlobalMem)
    if not SaveOpenClipboard():
        return
    try:
        EmptyClipboard()
        SetClipboardData(CF_UNICODETEXT, hGlobalMem)
    finally:
        CloseClipboard()

        