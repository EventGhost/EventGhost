# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
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

"""<rst>
Hardware plugin for the `TechnoTrend USB Infrared Receiver
<http://www.technotrend.com/2789/USB_Infrared_Receiver.html>`_.

|

.. image:: IR_receiver.jpg
   :align: center
   :target: http://www.technotrend.com/2789/USB_Infrared_Receiver.html
"""


import eg

eg.RegisterPlugin(
    name = "TechnoTrend USB IR Receiver",
    author = "Bitmonster",
    version = "1.1",
    kind = "remote",
    guid = "{66211720-B0DE-46E2-AD57-2D70F477DE02}",
    description = __doc__,
)

import os
from threading import Lock, Timer, Thread
from time import clock, sleep
from functools import partial

from eg.WinApi.Dynamic import (
    cdll, DWORD, POINTER, ULONG, HANDLE, BYTE, c_void_p, c_int, CFUNCTYPE, CDLL
)

USBIR_MODE_DIV = 2

# typedef void (*PIRCBFCN) (PVOID Context,
#                           PVOID Buf,
#                           ULONG len, // buffer length in bytes
#                           USBIR_MODES IRMode,
#                           HANDLE hOpen,
#                           BYTE DevIdx);
IRCALLBACKFUNC = CFUNCTYPE(
    c_void_p, # return type
    c_void_p, # Context
    POINTER(DWORD), # Buf
    ULONG, # len (buffer length in bytes)
    c_int, # IRMode (of enum USBIR_MODES)
    HANDLE, # hOpen
    BYTE # DevIdx
)


class TTIR(eg.IrDecoderPlugin):

    def __init__(self):
        eg.IrDecoderPlugin.__init__(self, 1)


    def __close__(self):
        self.irDecoder.Close()


    def __start__(self):
        self.dll = None
        self.hOpen = None
        pluginDir = os.path.abspath(os.path.dirname(__file__))
        dll = CDLL(os.path.join(pluginDir, "TTUSBIR.dll"))
        self.cCallback = IRCALLBACKFUNC(self.IrCallback)
        self.hOpen = dll.irOpen(0, USBIR_MODE_DIV, self.cCallback, 0)
        if self.hOpen == -1:
            raise self.Exceptions.DeviceNotFound
#        self.irGetUniqueCode = dll.ir_GetUniqueCode
#        self.irGetUniqueCode.restype  = DWORD
        self.dll = dll
        self.data = []
        self.timer = eg.ResettableTimer(self.OnTimeout)
        self.dataLock = Lock()
        self.lastTime = clock()
        self.startByte = 1
        self.dll.irSetPowerLED(self.hOpen, 0)
        self.ledTimer = eg.ResettableTimer(
            partial(self.dll.irSetPowerLED, self.hOpen, 0)
        )


    def OnComputerSuspend(self, dummySuspendType):
        self.dll.irClose(self.hOpen)


    def OnComputerResume(self, dummySuspendType):
        self.hOpen = self.dll.irOpen(
            0, USBIR_MODE_DIV, self.cCallback, 0
        )
        if self.hOpen == -1:
            raise self.Exceptions.DeviceNotFound


    def __stop__(self):
        if self.dll is not None:
            self.dll.irClose(self.hOpen)
            self.dll = None
            self.hOpen = None
            self.cCallback = None
        self.timer.Stop()
        self.ledTimer.Stop()


    def IrCallback(self, context, buf, length, irMode, hOpen, devIdx):
        if irMode == USBIR_MODE_DIV:
            self.dll.irSetPowerLED(self.hOpen, 1)
            self.ledTimer.Reset(1)
            self.timer.Reset(80)
            #self.lastTime = clock()
            self.dataLock.acquire()
            #print "---", length / 4, clock() - self.lastTime
            append = self.data.append
            for i in xrange(self.startByte, min(length/4, 500)):
                value = buf[i] & 0x00ffffff
                append(value)
                if value > 12000:
                    self.irDecoder.Decode(self.data, len(self.data))
                    self.data = []
                    append = self.data.append
            self.startByte = 0
            self.dataLock.release()


    def OnTimeout(self):
        if self.dataLock.acquire(0):
            data = self.data
            self.data = []
            self.startByte = 1
            self.dataLock.release()
            data.append(10000)
            self.irDecoder.Decode(data, len(data))

