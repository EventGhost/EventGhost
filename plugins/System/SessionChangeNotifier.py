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
import ctypes
from win32ts import (
    WTSUnRegisterSessionNotification,
    WTSQuerySessionInformation,
    WTSUserName,
    WTS_CURRENT_SERVER_HANDLE,
    NOTIFY_FOR_ALL_SESSIONS,
)
import win32api

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
        # WTSRegisterSessionNotification seems to have an odd bug (throwing an
        # exception at an unexpected location). Therefor we use the ctypes
        # version
        WTSRegisterSessionNotification = ctypes.windll.WtsApi32.WTSRegisterSessionNotification
        for tries in range(60):
            success = WTSRegisterSessionNotification(
                eg.messageReceiver.hwnd, 
                NOTIFY_FOR_ALL_SESSIONS
            )
            if success:
                break
            errorNum = win32api.GetLastError()
            # if we get the error RPC_S_INVALID_BINDING (1702), the system
            # hasn't started all needed services. For this reason we wait some
            # time and try it again.
            if errorNum == 1702:
                time.sleep(1.0)
                continue
            # some other error has happened
            raise SystemError("WTSRegisterSessionNotification", errorNum)
            #return
        else:
            raise SystemError("WTSRegisterSessionNotification timeout")
            
        
        self.TriggerEvent = plugin.TriggerEvent
        eg.messageReceiver.AddHandler(
            WM_WTSSESSION_CHANGE, 
            self.OnSessionChange
        )
        self.inited = True
    
    
    def Close(self):
        if not self.inited:
            return
        WTSUnRegisterSessionNotification(eg.messageReceiver.hwnd)
        eg.messageReceiver.RemoveHandler(
            WM_WTSSESSION_CHANGE, 
            self.OnSessionChange
        )
        
        
    @eg.LogIt
    def OnSessionChange(self, hwnd, msg, wparam, lparam):
        eventstring = WTS_WPARAM_DICT.get(wparam, None)
        if eventstring is not None:
            userName = WTSQuerySessionInformation(
                WTS_CURRENT_SERVER_HANDLE, 
                lparam, 
                WTSUserName)
            self.TriggerEvent(eventstring, [userName])
        return 1
    