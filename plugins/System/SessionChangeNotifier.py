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

import eg
from win32ts import (
    WTSRegisterSessionNotification, 
    WTSUnRegisterSessionNotification,
    NOTIFY_FOR_ALL_SESSIONS,
    WTSQuerySessionInformation,
    WTSUserName,
    WTS_CURRENT_SERVER_HANDLE)

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
    9: "SessionRemoteControl"}


class SessionChangeNotifier:
    inited = False
    
    def __init__(self, plugin):
        try:
            WTSRegisterSessionNotification(
                eg.messageReceiver.hwnd, 
                NOTIFY_FOR_ALL_SESSIONS
            )
        except NotImplementedError:
            # Only available on Windows XP and above
            return
        
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
    