# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
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
    name = "UIR / Irman",
    author = "Bitmonster",
    version = "1.1." + "$LastChangedRevision$".split()[1],
    kind = "remote",
    canMultiLoad = True,
    description = (
        'Hardware plugin for the <a href="http://fly.cc.fer.hr/~mozgic/UIR/">'
        'Universal Infrared Receiver V1 (UIR)</a> '
        'and the <a href="http://www.evation.com/irman/index.html">'
        'Evation.com Irman</a> '
        'device.'
        '\n\n<p><center><img src="irman_front.jpg" alt="Irman" /></a></center>'
    ),
)


import wx
import time
import threading
import win32event


class UIR(eg.RawReceiverPlugin):
    lastReceivedTime = 0
    
    def __start__(self, port, byteCount=6, initSequence=True):
        self.byteCount = byteCount
        self.serialThread = serialThread = eg.SerialThread()
        serialThread.Open(port, 9600)
        serialThread.SetRts()
        serialThread.SetDtr()
        serialThread.Start()
        time.sleep(0.05)
        serialThread.Flush()
        if initSequence:
            serialThread.Write("I")
            time.sleep(0.05)
            serialThread.Write("R")
            if serialThread.Read(2, 1.0) != "OK":
                self.serialThread.Close()
                raise self.Exceptions.DeviceInitFailed
        serialThread.SetReadEventCallback(self.OnReceive)
    
    
    def __stop__(self):
        self.serialThread.Close()
    
    
    def OnReceive(self, serialThread):
        data = serialThread.Read(self.byteCount, 0.1)
        if len(data) < self.byteCount:
            return
        self.TriggerEvent("".join("%02X" % ord(byte) for byte in data))
            
        
    def Configure(self, port=0, byteCount=6, initSequence=True):
        panel = eg.ConfigPanel()
        portCtrl = panel.SerialPortChoice(port)
        byteCountCtrl = panel.SpinIntCtrl(byteCount, min=1, max=32)
        initSequenceCtrl = panel.CheckBox(
            initSequence, 
            "Initialise device on start"
        )
        panel.AddLine('COM Port:', portCtrl)
        panel.AddLine('Event Byte Count:', byteCountCtrl, '(default=6)')
        panel.AddLine(initSequenceCtrl)
        
        while panel.Affirmed():
            panel.SetResult(
                portCtrl.GetValue(), 
                byteCountCtrl.GetValue(), 
                initSequenceCtrl.GetValue()
            )
                    
        