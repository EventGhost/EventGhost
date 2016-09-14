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
    Hardware plugin for the `Universal Infrared Receiver V1 (UIR)`__ and the
    `Evation.com Irman`__ device.

    |

    .. image:: irman_front.jpg
       :align: center

    __ http://fly.cc.fer.hr/~mozgic/UIR/
    __ http://www.evation.com/irman/index.html
"""

import eg

eg.RegisterPlugin(
    name = "UIR / Irman",
    author = "Bitmonster",
    version = "1.2",
    kind = "remote",
    guid = "{799EB51F-0A75-4027-AB04-52E20939A511}",
    canMultiLoad = True,
    description = __doc__,
)


import wx
import time


class UIR(eg.RawReceiverPlugin):

    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)
        self.AddEvents()


    def __start__(self, port, byteCount=6, init=True):
        self.byteCount = byteCount
        self.serialThread = serialThread = eg.SerialThread()
        serialThread.Open(port, 9600)
        serialThread.SetRts()
        serialThread.SetDtr()
        serialThread.Start()
        time.sleep(0.05)
        serialThread.Flush()
        if init:
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


    def Configure(self, port=0, byteCount=6, init=True):
        panel = eg.ConfigPanel()
        portCtrl = panel.SerialPortChoice(port)
        byteCountCtrl = panel.SpinIntCtrl(byteCount, min=1, max=32)
        initCtrl = panel.CheckBox(init, "Initialize device on start")
        panel.AddLine('COM Port:', portCtrl)
        panel.AddLine('Event Byte Count:', byteCountCtrl, '(default=6)')
        panel.AddLine(initCtrl)
        while panel.Affirmed():
            panel.SetResult(
                portCtrl.GetValue(),
                byteCountCtrl.GetValue(),
                initCtrl.GetValue()
            )

