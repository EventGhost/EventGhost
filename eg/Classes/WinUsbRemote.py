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

from os.path import join

# Local imports
import eg
from eg.WinApi.Dynamic import c_ubyte, cast, POINTER, WinDLL

PUBYTE = POINTER(c_ubyte)

class WinUsbRemote(object):
    threadId = None
    dll = None

    def __init__(
        self,
        deviceInterfaceGuid,
        callback,
        dataSize=1,
        suppressRepeat=False
    ):
        self.callback = callback
        self.dataSize = dataSize
        self.suppressRepeat = suppressRepeat
        self.deviceInterfaceGuid = unicode(deviceInterfaceGuid)
        if self.dll is None:
            self.__class__.dll = WinDLL(
                join(eg.sitePackagesDir, "WinUsbWrapper.dll").encode('mbcs')
            )
        self.Open()

    def Close(self):
        self.dll.End(self.threadId)
        self.threadId = None
        eg.messageReceiver.RemoveWmUserHandler(self.MsgHandler)

    def IsOk(self):
        return bool(self.threadId)

    def MsgHandler(self, dummyHwnd, dummyMsg, dummyWParam, lParam):
        dataArray = cast(lParam, PUBYTE)
        value = tuple(dataArray[i] for i in range(self.dataSize))
        self.callback(value)
        return 1

    def Open(self):
        msgId = eg.messageReceiver.AddWmUserHandler(self.MsgHandler)
        self.threadId = self.dll.Start(
            eg.messageReceiver.hwnd,
            msgId,
            self.deviceInterfaceGuid,
            self.dataSize,
            int(self.suppressRepeat)
        )
