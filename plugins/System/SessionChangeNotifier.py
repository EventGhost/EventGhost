# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

import time
from eg.WinApi.Dynamic import (
    GetLastError, WTSRegisterSessionNotification, WTSUserName, WTSFreeMemory,
    WTSUnRegisterSessionNotification, WTS_CURRENT_SERVER_HANDLE, 
    NOTIFY_FOR_ALL_SESSIONS, byref, WTSQuerySessionInformation, LPTSTR, DWORD,
)

WM_WTSSESSION_CHANGE = 0x02B1

WTS_WPARAM_DICT = {
    1: "ConsoleConnect",
    2: "ConsoleDisconnect",
    3: "RemoteConnect",
    4: "RemoteDisconnect",
    5: "SessionLogon",
    6: "SessionLogoff",
    7: "SessionLock",
    8: "SessionUnlock",
    9: "SessionRemoteControl"
}


class SessionChangeNotifier:
    inited = False
    
    def __init__(self, plugin):
        self.TriggerEvent = plugin.TriggerEvent
        self.retryCount = 0
        eg.messageReceiver.AddHandler(
            WM_WTSSESSION_CHANGE, 
            self.OnSessionChange
        )
        eg.scheduler.AddTask(0, self.Register)
    
    
    @eg.LogIt
    def Register(self):
        success = WTSRegisterSessionNotification(
            eg.messageReceiver.hwnd, 
            NOTIFY_FOR_ALL_SESSIONS
        )
        if success:
            self.inited = True
            return
        errorNum = GetLastError()
        # if we get the error RPC_S_INVALID_BINDING (1702), the system
        # hasn't started all needed services. For this reason we wait some
        # time and try it again.
        if errorNum == 1702:
            self.retryCount += 1
            if self.retryCount > 60:
                # if we tried it to often, give up
                eg.PrintError("WTSRegisterSessionNotification timeout")
                return
            eg.scheduler.AddTask(2.0, self.Register)
            return
        # some other error has happened
        raise SystemError("WTSRegisterSessionNotification", errorNum)
        
    
    def Close(self):
        if self.inited:
            WTSUnRegisterSessionNotification(eg.messageReceiver.hwnd)
        eg.messageReceiver.RemoveHandler(
            WM_WTSSESSION_CHANGE, 
            self.OnSessionChange
        )
        
        
    @eg.LogIt
    def OnSessionChange(self, hwnd, msg, wparam, lparam):
        eventstring = WTS_WPARAM_DICT.get(wparam, None)
        if eventstring is not None:
            pBuffer = LPTSTR()
            bytesReturned = DWORD()
            WTSQuerySessionInformation(
                WTS_CURRENT_SERVER_HANDLE, 
                lparam, 
                WTSUserName,
                byref(pBuffer),
                byref(bytesReturned)
            )
            userName = pBuffer.value
            WTSFreeMemory(pBuffer)
            self.TriggerEvent(eventstring, [userName])
        return 1
    