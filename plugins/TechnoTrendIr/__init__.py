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


eg.RegisterPlugin(
    name = "TechnoTrend USB-IR Receiver",
    author = "Bitmonster",
    version = "1.0." + "$LastChangedRevision$".split()[1],
    kind = "remote",
    description = (
        'Hardware plugin for the '
        '<a href="http://shop.technotrend.de/shop.php?mode=show_detail&group=6&id=545">'
        'TechnoTrend USB-IR Receiver</a>.'
        '\n\n<p>'
        '<center><img src="IR_receiver.jpg" /></center>'
    ),
)

import os
from eg.WinApi.Dynamic import (
    cdll, DWORD, POINTER, ULONG, HANDLE, BYTE, c_void_p, c_int, CFUNCTYPE
)

# enum USBIR_MODES
USBIR_MODE_NONE = 0
USBIR_MODE_RAW = 1
USBIR_MODE_DIV = 2
USBIR_MODE_ALL_CODES = 3 # special mode for decting the type of a remote control
USBIR_MODE_RC5 = 4
USBIR_MODE_NOKIA = 5
USBIR_MODE_NEC = 6
USBIR_MODE_RCMM8 = 7 # USBIR_MODE_RCMM,
USBIR_MODE_RC6 = 8 # RC6 Mode 6A
USBIR_MODE_RECS80 = 9
USBIR_MODE_DENON = 10 # = Sharp
USBIR_MODE_MOTOROLA = 11
USBIR_MODE_SONYSIRC = 12

#    typedef void (*PIRCBFCN) (PVOID Context, PVOID Buf, ULONG len, // buffer length in bytes
#                                USBIR_MODES IRMode, HANDLE hOpen, BYTE DevIdx);
IRCALLBACKFUNC = CFUNCTYPE(
    c_void_p, # return type
    c_void_p, # Context
    POINTER(DWORD), # Buf
    ULONG, # len (buffer length in bytes)
    c_int, # IRMode (of enum USBIR_MODES)
    HANDLE, # hOpen
    BYTE # DevIdx
)


class TTIR(eg.RawReceiverPlugin):
    
    def __start__(self):
        self.dll = None
        self.hOpen = None
        pluginDir = os.path.abspath(os.path.split(__file__)[0])
        dll = cdll.LoadLibrary(os.path.join(pluginDir, "TTUSBIR.dll"))
        self.cCallback = IRCALLBACKFUNC(self.IrCallback)
        self.hOpen = dll.irOpen(0, USBIR_MODE_ALL_CODES, self.cCallback, 0)
        if self.hOpen == -1:
            raise self.Exceptions.DeviceNotFound
        self.ir_GetUniqueCode = dll.ir_GetUniqueCode
        self.ir_GetUniqueCode.restype  = DWORD
        self.dll = dll
        
    
    def OnComputerSuspend(self, suspendType):
        self.dll.irClose(self.hOpen)
    
    
    def OnComputerResume(self, suspendType):
        self.hOpen = self.dll.irOpen(0, USBIR_MODE_ALL_CODES, self.cCallback, 0)
        if self.hOpen == -1:
            raise self.Exceptions.DeviceNotFound
    
    
    def __stop__(self):
        if self.dll is not None:
            self.dll.irClose(self.hOpen)
    
    
    def IrCallback(self, context, buf, length, irMode, hOpen, devIdx):
        if irMode == USBIR_MODE_ALL_CODES: 
            # special mode for decting the type of a remote control
            for i in range(0, min(length // 8, 400)):
                irMode2 = buf[i * 2]
                code2 = buf[i * 2 + 1]
                code = self.ir_GetUniqueCode(code2, irMode2)
                self.TriggerEvent("%08X" % code)
            
    
    