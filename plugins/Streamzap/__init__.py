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

eg.RegisterPlugin(
    name = "Streamzap PC Remote",
    author = "Bitmonster",
    version = "1.0." + "$LastChangedRevision$".split()[1],
    kind = "remote",
    description = (
        'Hardware plugin for the '
        '<a href="http://www.streamzap.com/products/pcremote/">'
        'Streamzap PC Remote</a>.'
        '\n\n<p>'
        '<center><p><a href=http://www.streamzap.com/products/pcremote/>'
        '<img src="crr.jpg" alt="Streamzap" /></a></center>'
    ),
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAOElEQVR42mNkoBAwDl4D"
        "/gMRIxEWMFKimWgD8BnISIlmkg3AZhh9DaBPIBJjK0EDSDFkEOcFYgEAwk8kEWJRdKUA"
        "AAAASUVORK5CYII="
    ),
)


import thread
import threading
import time
import os
import array

from ctypes import cdll, c_ubyte, byref
from ctypes.wintypes import DWORD


SAMPLE_TIME = 0.000256

MyDecoder = eg.IrDecoder(SAMPLE_TIME)
MyDecoder.RC5_THRESHOLD = 5
MyDecoder.suppressRc5ToggleBit = False

plugin_dir = os.path.abspath(os.path.split(__file__)[0])
dll_path = os.path.join(plugin_dir, "irdata.dll")


mapTable = {
    "RC5_3465": ("Power", 0.140, None),
    "RC5_3C65": ("Power", 0.140, None),
    "RC5_68CB": ("Mute", 0.140, None),
    "RC5_78CB": ("Mute", 0.140, None),
    "RC5_68C1": ("Num1", 0.140, None),
    "RC5_78C1": ("Num1", 0.140, None),
    "RC5_3461": ("Num2", 0.140, None),
    "RC5_3C61": ("Num2", 0.140, None),
    "RC5_68C3": ("Num3", 0.140, None),
    "RC5_78C3": ("Num3", 0.140, None),
    "RC5_3462": ("Num4", 0.140, None),
    "RC5_3C62": ("Num4", 0.140, None),
    "RC5_68C5": ("Num5", 0.140, None),
    "RC5_78C5": ("Num5", 0.140, None),
    "RC5_3463": ("Num6", 0.140, None),
    "RC5_3C63": ("Num6", 0.140, None),
    "RC5_68C7": ("Num7", 0.140, None),
    "RC5_78C7": ("Num7", 0.140, None),
    "RC5_3464": ("Num8", 0.140, None),
    "RC5_3C64": ("Num8", 0.140, None),
    "RC5_68C9": ("Num9", 0.140, None),
    "RC5_78C9": ("Num9", 0.140, None),
    "RC5_3460": ("Num0", 0.140, None),
    "RC5_3C60": ("Num0", 0.140, None),
    "RC5_3466": ("ChannelUp", 0.140, None),
    "RC5_3C66": ("ChannelUp", 0.140, None),
    "RC5_3467": ("ChannelDown", 0.140, None),
    "RC5_3C67": ("ChannelDown", 0.140, None),
    "RC5_68CD": ("VolumeUp", 0.140, None),
    "RC5_78CD": ("VolumeUp", 0.140, None),
    "RC5_68CF": ("VolumeDown", 0.140, None),
    "RC5_78CF": ("VolumeDown", 0.140, None),
    "RC5_3468": ("Up", 0.140, None),
    "RC5_3C68": ("Up", 0.140, None),
    "RC5_68D1": ("Left", 0.140, None),
    "RC5_78D1": ("Left", 0.140, None),
    "RC5_3469": ("Ok", 0.140, None),
    "RC5_3C69": ("Ok", 0.140, None),
    "RC5_68D3": ("Right", 0.140, None),
    "RC5_78D3": ("Right", 0.140, None),
    "RC5_346A": ("Down", 0.140, None),
    "RC5_3C6A": ("Down", 0.140, None),
    "RC5_68D5": ("Menu", 0.140, None),
    "RC5_78D5": ("Menu", 0.140, None),
    "RC5_346B": ("Exit", 0.140, None),
    "RC5_3C6B": ("Exit", 0.140, None),
    "RC5_68D7": ("Play", 0.140, None),
    "RC5_78D7": ("Play", 0.140, None),
    "RC5_346C": ("Pause", 0.140, None),
    "RC5_3C6C": ("Pause", 0.140, None),
    "RC5_68D9": ("Stop", 0.140, None),
    "RC5_78D9": ("Stop", 0.140, None),
    "RC5_346D": ("PreviousTrack", 0.140, None),
    "RC5_3C6D": ("PreviousTrack", 0.140, None),
    "RC5_68DB": ("NextTrack", 0.140, None),
    "RC5_78DB": ("NextTrack", 0.140, None),
    "RC5_346E": ("Record", 0.140, None),
    "RC5_3C6E": ("Record", 0.140, None),
    "RC5_68DD": ("Rewind", 0.140, None),
    "RC5_78DD": ("Rewind", 0.140, None),
    "RC5_346F": ("Forward", 0.140, None),
    "RC5_3C6F": ("Forward", 0.140, None),
    "RC5_3470": ("Red", 0.140, None),
    "RC5_3C70": ("Red", 0.140, None),
    "RC5_68E1": ("Green", 0.140, None),
    "RC5_78E1": ("Green", 0.140, None),
    "RC5_3471": ("Yellow", 0.140, None),
    "RC5_3C71": ("Yellow", 0.140, None),
    "RC5_68E3": ("Blue", 0.140, None),
    "RC5_78E3": ("Blue", 0.140, None),
}



class Streamzap(eg.RawReceiverPlugin):
    
    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)
        self.mapTable = mapTable


    def __start__(self, comport=0):
        self.abort_thread = False
        startupEvent = threading.Event()
        self.thread = thread.start_new_thread(self.ReceiveThread, (startupEvent,))
        startupEvent.wait(5.0)
        

    def __stop__(self):
        self.abort_thread = True
        
    
    def HandleException(self, msg):    
        def Do():
            raise self.Exception(msg)
        eg.actionThread.Call(Do)
    
    
    def ReceiveThread(self, startupEvent):
        # This is the code executing in the new thread. 
        try:
            dll = cdll.LoadLibrary(dll_path)
        except:
            self.HandleException("Streamzap DLL not found.")
            startupEvent.set()
            return
        
        if dll.sz_Open() != 1:
            self.HandleException(
                "Cannot open Streamzap driver!\n"
                "Please check that the receiver is connected "
                "properly and no other application is accessing "
                "the driver."
            )
            startupEvent.set()
            return
            
            
        dll.sz_Flush()
        
        dwNumBytesRead = DWORD()
        byteIRdata = c_ubyte()
        ir_data = array.array("B")
        for i in range(0, 512):
            ir_data.append(0)
        i = 0
        
        startupEvent.set()
        while not self.abort_thread:
            dll.sz_ReadFile(byref(byteIRdata), byref(dwNumBytesRead))
            val = byteIRdata.value

            if dwNumBytesRead.value == 0:
                time.sleep(0.01)
            else:
                if val > 150 or i == 511:
                    event = MyDecoder.Decode(ir_data, i)
                    if event is not None:
                        self.TriggerEvent(event)
                    i = 0
                else:
                    ir_data[i] = val
                    i += 1
                    
        dll.sz_Close()
 

