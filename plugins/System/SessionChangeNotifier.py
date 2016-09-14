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

from ctypes import byref, c_int, c_void_p, GetLastError, POINTER, WinDLL
from ctypes.wintypes import BOOL, DWORD, HANDLE, HWND, LPWSTR

# Local imports
import eg

PVOID = c_void_p
LPTSTR = LPWSTR

_WtsApi32 = WinDLL("WtsApi32")

WTSRegisterSessionNotification = _WtsApi32.WTSRegisterSessionNotification
WTSRegisterSessionNotification.restype = BOOL
WTSRegisterSessionNotification.argtypes = [HWND, DWORD]
WTSUserName = 5
WTSFreeMemory = _WtsApi32.WTSFreeMemory
WTSFreeMemory.restype = None
WTSFreeMemory.argtypes = [PVOID]
WTSUnRegisterSessionNotification = _WtsApi32.WTSUnRegisterSessionNotification
WTSUnRegisterSessionNotification.restype = BOOL
WTSUnRegisterSessionNotification.argtypes = [HWND]
WTS_CURRENT_SERVER_HANDLE = 0  # Variable c_void_p
NOTIFY_FOR_ALL_SESSIONS = 1  # Variable c_int

# values for enumeration '_WTS_INFO_CLASS'
WTSInitialProgram = 0
WTSApplicationName = 1
WTSWorkingDirectory = 2
WTSOEMId = 3
WTSSessionId = 4
WTSWinStationName = 6
WTSDomainName = 7
WTSConnectState = 8
WTSClientBuildNumber = 9
WTSClientName = 10
WTSClientDirectory = 11
WTSClientProductId = 12
WTSClientHardwareId = 13
WTSClientAddress = 14
WTSClientDisplay = 15
WTSClientProtocolType = 16
_WTS_INFO_CLASS = c_int  # enum
WTS_INFO_CLASS = _WTS_INFO_CLASS
WTSQuerySessionInformationW = _WtsApi32.WTSQuerySessionInformationW
WTSQuerySessionInformationW.restype = BOOL
WTSQuerySessionInformationW.argtypes = [
    HANDLE, DWORD, WTS_INFO_CLASS, POINTER(LPWSTR), POINTER(DWORD)
]
WTSQuerySessionInformation = WTSQuerySessionInformationW  # alias

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
