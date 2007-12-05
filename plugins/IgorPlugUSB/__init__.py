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
    name = "IgorPlug-USB",
    author = "Bitmonster",
    version = "1.0." + "$LastChangedRevision$".split()[1],
    kind = "remote",
    description = (
        'Plugin for <a href="http://www.cesko.host.sk/">'
        'Igor Cesko\'s USB IR</a> receiver.'
    ),
)


from thread import start_new_thread
from  ctypes import windll, byref, c_ubyte, c_int, create_string_buffer
from threading import Timer, Event
from time import clock, sleep


SAMPLE_TIME = 0.0000853


class IgorPlugUSB(eg.RawReceiverPlugin):
    
    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)
        self.irDecoder = eg.IrDecoder(SAMPLE_TIME)
        
        
    def __start__(self):
        self.dll = None
        self.threadShouldStop = False
        try:
            self.dll = windll.IgorUSB
        except:
            raise eg.Exception("No IgorPlug-USB driver installed!")
        start_new_thread(self.ReceiveThread, ())
    
    
    def __stop__(self):
        self.threadShouldStop = True
        
        
    def ReceiveThread(self):
        dll = self.dll
        timeCodeDiagram = (c_ubyte * 256)()
        diagramLength = c_int(0)
        portDirection = c_ubyte()
        dll.DoGetDataPortDirection(byref(portDirection))
        portDirection.value |= 3
        dll.DoSetDataPortDirection(portDirection)
        dll.DoSetOutDataPort(1)
        Decode = self.irDecoder.Decode
        self.flashThreadIsRunning = False
        while not self.threadShouldStop:
            dll.DoGetInfraCode(timeCodeDiagram, 0, byref(diagramLength))
            if diagramLength.value:
                self.StartLedFlashing()
                event = Decode(timeCodeDiagram, diagramLength.value)
                self.TriggerEvent(event)
            else:
                sleep(0.01)
        dll.DoSetOutDataPort(0)
        self.dll = None
        
        
    def StartLedFlashing(self):
        self.ledTimeout = clock() + 0.1
        if not self.flashThreadIsRunning:
            self.flashThreadIsRunning = True
            start_new_thread(self.LedFlashingThread, ())
            
            
    def LedFlashingThread(self):
        while self.ledTimeout > clock():
            self.dll.DoSetOutDataPort(3)
            sleep(0.08)
            self.dll.DoSetOutDataPort(1)
            sleep(0.08)
        self.flashThreadIsRunning = False
            
