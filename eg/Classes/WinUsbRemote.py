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

import sys
from os.path import join

import eg
from eg.WinApi.Dynamic import cast, c_ubyte, POINTER, WinDLL

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


    def IsOk(self):
        return bool(self.threadId)


    def Open(self):
        msgId = eg.messageReceiver.AddWmUserHandler(self.MsgHandler)
        self.threadId = self.dll.Start(
            eg.messageReceiver.hwnd,
            msgId,
            self.deviceInterfaceGuid,
            self.dataSize,
            int(self.suppressRepeat)
        )


    def Close(self):
        self.dll.End(self.threadId)
        self.threadId = None
        eg.messageReceiver.RemoveWmUserHandler(self.MsgHandler)


    def MsgHandler(self, dummyHwnd, dummyMsg, dummyWParam, lParam):
        dataArray = cast(lParam, PUBYTE)
        value = tuple(dataArray[i] for i in range(self.dataSize))
        self.callback(value)
        return 1

