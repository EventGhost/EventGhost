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
    name = "IgorPlug-USB",
    author = "Bitmonster",
    version = "1.1." + "$LastChangedRevision$".split()[1],
    kind = "remote",
    description = (
        'Plugin for <a href="http://www.cesko.host.sk/">'
        'Igor Cesko\'s USB IR</a> receiver.'
    ),
)


from threading import Thread, Event
from  ctypes import windll, byref, c_ubyte, c_int
from time import sleep
from functools import partial


class IgorPlugUSB(eg.PluginBase):
    
    def __init__(self):
        eg.PluginBase.__init__(self)
        self.irDecoder = eg.IrDecoder(self, 85.3)

        
    def __start__(self, led1=0, led2=0):
        self.stopEvent = Event()
        try:
            self.dll = windll.IgorUSB
        except:
            raise self.Exceptions.DriverNotFound
        self.ledIrOnFlags = 0
        self.ledIrOffFlags = 0
        if led1 == 1:
            self.ledIrOffFlags |= 1
            self.ledIrOnFlags |= 1
        elif led1 == 2:
            self.ledIrOnFlags |= 1
        if led2 == 1:
            self.ledIrOffFlags |= 2
            self.ledIrOnFlags |= 2
        elif led2 == 2:
            self.ledIrOnFlags |= 2
        self.ledTimer = eg.ResettableTimer(
            partial(self.dll.DoSetOutDataPort, self.ledIrOffFlags)
        )
        self.receiveThread = Thread(
            target=self.ReceiveThread, 
            args=(self.stopEvent, )
        )
        self.receiveThread.start()
    
    
    def __stop__(self):
        self.stopEvent.set()
        self.ledTimer.Stop()
        self.receiveThread.join(2.0)
        
        
    def __close__(self):
        self.irDecoder.Close()
        
        
    def ReceiveThread(self, stopEvent):
        dll = self.dll
        ledReset = self.ledTimer.Reset
        ledIrOnFlags = self.ledIrOnFlags
        timeCodeDiagram = (c_ubyte * 256)()
        diagramLength = c_int(0)
        portDirection = c_ubyte()
        dll.DoGetDataPortDirection(byref(portDirection))
        portDirection.value |= 3
        dll.DoSetDataPortDirection(portDirection)
        dll.DoSetOutDataPort(self.ledIrOffFlags)
        decode = self.irDecoder.Decode
        dll.DoGetInfraCode(timeCodeDiagram, 0, byref(diagramLength))
        while not stopEvent.isSet():
            dll.DoGetInfraCode(timeCodeDiagram, 0, byref(diagramLength))
            if diagramLength.value:
                dll.DoSetOutDataPort(ledIrOnFlags)
                ledReset(1)
                timeCodeDiagram[diagramLength.value] = 255
                decode(timeCodeDiagram, diagramLength.value + 1)
            else:
                sleep(0.01)
        dll.DoSetOutDataPort(self.ledIrOffFlags)
        
        
    def Configure(self, led1=2, led2=0):
        panel = eg.ConfigPanel()
        choices = ["Always Off", "Always On", "Blink on IR reception"]
        led1Ctrl = panel.RadioBox(led1, choices=choices)
        led2Ctrl = panel.RadioBox(led2, choices=choices)
        group1 = panel.BoxedGroup("LED 1", led1Ctrl)
        group2 = panel.BoxedGroup("LED 2", led2Ctrl)
        sizer = eg.HBoxSizer(group1, (15, 15), group2)
        panel.sizer.Add(sizer)
        while panel.Affirmed():
            panel.SetResult(led1Ctrl.GetValue(), led2Ctrl.GetValue())
            
