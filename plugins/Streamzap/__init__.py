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
    version = "1.1",
    kind = "remote",
    hardwareId = "USB\\VID_0E9C&PID_0000",
    guid = "{C188351F-44E3-459D-92FC-66F51104B1DB}",
    description = __doc__,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAOElEQVR42mNkoBAwDl4D"
        "/gMRIxEWMFKimWgD8BnISIlmkg3AZhh9DaBPIBJjK0EDSDFkEOcFYgEAwk8kEWJRdKUA"
        "AAAASUVORK5CYII="
    ),
)


import threading
from os.path import abspath, split, join
from time import sleep
from ctypes import cdll, c_ubyte, byref
from ctypes.wintypes import DWORD


DLL_PATH = join(abspath(split(__file__)[0]), "irdata.dll")

CODES = {
    0x0009C272: "Ok",
    0x00204272: "Ok",
    0x002709C2: "Left",
    0x008109C2: "Left",
    0x002709C8: "Right",
    0x008109C8: "Right",
    0x008109C0: "Up",
    0x002709C0: "Up",
    0x0020427C: "Down",
    0x0009C27C: "Down",
    0x02042402: "Num1",
    0x009C2402: "Num1",
    0x00270902: "Num2",
    0x00810902: "Num2",
    0x02042408: "Num3",
    0x009C2408: "Num3",
    0x0081090C: "Num4",
    0x0027090C: "Num4",
    0x0081090E: "Num5",
    0x0027090E: "Num5",
    0x00810908: "Num6",
    0x00270908: "Num6",
    0x02042420: "Num7",
    0x009C2420: "Num7",
    0x00810930: "Num8",
    0x00270930: "Num8",
    0x00810932: "Num9",
    0x00270932: "Num9",
    0x02042400: "Num0",
    0x009C2400: "Num0",
    0x0020424E: "Power",
    0x0009C24E: "Power",
    0x00810938: "Mute",
    0x00270938: "Mute",
    0x00810924: "ChannelUp",
    0x00270924: "ChannelUp",
    0x00810920: "ChannelDown",
    0x00270920: "ChannelDown",
    0x00810926: "VolumeUp",
    0x00270926: "VolumeUp",
    0x02042480: "VolumeDown",
    0x009C2480: "VolumeDown",
    0x0020427E: "Menu",
    0x0009C27E: "Menu",
    0x00204278: "Exit",
    0x0009C278: "Exit",
    0x008109E0: "Play",
    0x002709E0: "Play",
    0x00810990: "Pause",
    0x00270990: "Pause",
    0x00810992: "Stop",
    0x00270992: "Stop",
    0x00810992: "Stop",
    0x00270992: "Stop",
    0x0009C266: "PreviousTrack",
    0x00204266: "PreviousTrack",
    0x00270998: "NextTrack",
    0x00810998: "NextTrack",
    0x00270984: "Record",
    0x00810984: "Record",
    0x00270986: "Rewind",
    0x00810986: "Rewind",
    0x00270980: "Forward",
    0x00810980: "Forward",
    0x009C2100: "Red",
    0x02042100: "Red",
    0x009C2102: "Green",
    0x02042102: "Green",
    0x00810842: "Yellow",
    0x00270842: "Yellow",
    0x02042108: "Blue",
    0x009C2108: "Blue",
}

# Even though the Streamzap should be able to deliver raw timecode diagrams,
# it doesn't work right. Sometimes the last pulse is missing. So we use a
# simple decoder especially for this remote, that only reacts to known
# Streamzap codes.

def Decode(data):
    buf = 2
    for value in data:
        if value < 5:
            pass
        elif value < 10:
            buf |= 1
        else:
            return None
        buf <<= 1
    return buf



class Streamzap(eg.PluginBase):

    def __init__(self):
        eg.PluginBase.__init__(self)
        self.AddEvents()


    def __start__(self):
        self.timer = eg.ResettableTimer(self.OnTimeout)
        self.lastCode = None
        self.abortThread = False
        self.lastException = None
        startupEvent = threading.Event()
        self.thread = threading.Thread(
            target=self.ReceiveThread,
            name="StreamzapReceiveThread",
            args=(startupEvent,)
        )
        self.thread.start()
        startupEvent.wait(5.0)
        if self.lastException:
            self.timer.Stop()
            raise self.lastException


    def __stop__(self):
        self.abortThread = True
        self.timer.Stop()
        self.thread.join(5.0)


    def ReceiveThread(self, startupEvent):
        # This is the code executing in the new thread.
        try:
            dll = cdll.LoadLibrary(DLL_PATH)
        except WindowsError:
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
        irData = []
        i = 0
        szReadFile = dll.sz_ReadFile
        startupEvent.set()
        while not self.abortThread:
            szReadFile(byref(byteIRdata), byref(dwNumBytesRead))
            val = byteIRdata.value

            if dwNumBytesRead.value == 0:
                sleep(0.001)
            else:
                i += 1
                if val > 78 or i == 511:
                    code = Decode(irData)
                    eventname = CODES.get(code, None)
                    if eventname is None:
                        self.EndLastEvent()
                        self.lastCode = None
                    else:
                        if code != self.lastCode:
                            self.TriggerEnduringEvent(eventname)
                            self.lastCode = code
                        self.timer.Reset(140)
                    irData = []
                    i = 0
                    continue
                irData.append(val)

        dll.sz_Close()


    def OnTimeout(self):
        self.EndLastEvent()
        self.lastCode = None

