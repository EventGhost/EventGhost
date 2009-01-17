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

"""<rst>

Hardware plugin for the `Streamzap PC Remote`_.

|

.. image:: crr.jpg
   :align: center

.. _Streamzap PC Remote: http://www.streamzap.com/products/pcremote/
"""

import eg

eg.RegisterPlugin(
    name = "Streamzap PC Remote",
    author = "Bitmonster",
    version = "1.0." + "$LastChangedRevision$".split()[1],
    kind = "remote",
    description = __doc__,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAOElEQVR42mNkoBAwDl4D"
        "/gMRIxEWMFKimWgD8BnISIlmkg3AZhh9DaBPIBJjK0EDSDFkEOcFYgEAwk8kEWJRdKUA"
        "AAAASUVORK5CYII="
    ),
)


import threading
import os
import array
from time import sleep
from ctypes import cdll, c_ubyte, byref
from ctypes.wintypes import DWORD


SAMPLE_TIME = 0.000256

MyDecoder = eg.IrDecoder(SAMPLE_TIME)
MyDecoder.RC5_THRESHOLD = 5
MyDecoder.suppressRc5ToggleBit = False

pluginDir = os.path.abspath(os.path.split(__file__)[0])
dllPath = os.path.join(pluginDir, "irdata.dll")


EVENTS = (
    ("Power", ("RC5_3465", "RC5_3C65")),
    ("Mute", ("RC5_68CB", "RC5_78CB")),
    ("Num1", ("RC5_68C1", "RC5_78C1")),
    ("Num2", ("RC5_3461", "RC5_3C61")),
    ("Num3", ("RC5_68C3", "RC5_78C3")),
    ("Num4", ("RC5_3462", "RC5_3C62")),
    ("Num5", ("RC5_68C5", "RC5_78C5")),
    ("Num6", ("RC5_3463", "RC5_3C63")),
    ("Num7", ("RC5_68C7", "RC5_78C7")),
    ("Num8", ("RC5_3464", "RC5_3C64")),
    ("Num9", ("RC5_68C9", "RC5_78C9")),
    ("Num0", ("RC5_3460", "RC5_3C60")),
    ("ChannelUp", ("RC5_3466", "RC5_3C66")),
    ("ChannelDown", ("RC5_3467", "RC5_3C67")),
    ("VolumeUp", ("RC5_68CD", "RC5_78CD")),
    ("VolumeDown", ("RC5_68CF", "RC5_78CF")),
    ("Up", ("RC5_3468", "RC5_3C68")),
    ("Left", ("RC5_68D1", "RC5_78D1")),
    ("Ok", ("RC5_3469", "RC5_3C69")),
    ("Right", ("RC5_68D3", "RC5_78D3")),
    ("Down", ("RC5_346A", "RC5_3C6A")),
    ("Menu", ("RC5_68D5", "RC5_78D5")),
    ("Exit", ("RC5_346B", "RC5_3C6B")),
    ("Play", ("RC5_68D7", "RC5_78D7")),
    ("Pause", ("RC5_346C", "RC5_3C6C")),
    ("Stop", ("RC5_68D9", "RC5_78D9")),
    ("PreviousTrack", ("RC5_346D", "RC5_3C6D")),
    ("NextTrack", ("RC5_68DB", "RC5_78DB")),
    ("Record", ("RC5_346E", "RC5_3C6E")),
    ("Rewind", ("RC5_68DD", "RC5_78DD")),
    ("Forward", ("RC5_346F", "RC5_3C6F")),
    ("Red", ("RC5_3470", "RC5_3C70")),
    ("Green", ("RC5_68E1", "RC5_78E1")),
    ("Yellow", ("RC5_3471", "RC5_3C71")),
    ("Blue", ("RC5_68E3", "RC5_78E3")),
)

eventList = []
mapTable = {}
for name, (code1, code2) in EVENTS:
    mapTable[code1] = (name, 0.140, None)
    mapTable[code2] = (name, 0.140, None)
    eventList.append((name, None))
    


class Streamzap(eg.RawReceiverPlugin):
    
    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)
        self.mapTable = mapTable
        self.RegisterEvents(eventList)


    def __start__(self, comport=0):
        self.abortThread = False
        self.lastException = None
        startupEvent = threading.Event()
        self.thread = threading.Thread(
            target=self.ReceiveThread, 
            args=(startupEvent,)
        )
        self.thread.start()
        startupEvent.wait(5.0)
        if self.lastException:
            raise self.lastException
        

    def __stop__(self):
        self.abortThread = True
        self.thread.join(5.0)
        
    
    def ReceiveThread(self, startupEvent):
        # This is the code executing in the new thread. 
        try:
            dll = cdll.LoadLibrary(dllPath)
        except:
            self.lastException = self.Exceptions.DriverNotFound
            startupEvent.set()
            return
        
        if dll.sz_Open() != 1:
            self.lastException = self.Exceptions.DriverNotOpen
            startupEvent.set()
            return
            
        dll.sz_Flush()
        
        dwNumBytesRead = DWORD()
        byteIRdata = c_ubyte()
        irData = array.array("B")
        for i in range(0, 512):
            irData.append(0)
        i = 0
        
        startupEvent.set()
        szReadFile = dll.sz_ReadFile
        Decode = MyDecoder.Decode
        while not self.abortThread:
            szReadFile(byref(byteIRdata), byref(dwNumBytesRead))
            val = byteIRdata.value

            if dwNumBytesRead.value == 0:
                sleep(0.01)
            else:
                if val > 150 or i == 511:
                    event = Decode(irData, i)
                    if event is not None:
                        self.TriggerEvent(event)
                    i = 0
                else:
                    irData[i] = val
                    i += 1
                    
        dll.sz_Close()
 

