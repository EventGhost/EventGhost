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
Hardware plugin for the `Home Electronics Tira`__ transceiver.

|

.. image:: tira.png
   :align: center

__ http://www.home-electro.com/
"""

import eg

eg.RegisterPlugin(
    name = "Home Electronics Tira",
    author = "Bitmonster",
    version = "1.0",
    kind = "remote",
    guid = "{B0E45461-630A-4FFC-BA92-9A8281DC112C}",
    description = __doc__,
    url = "http://www.eventghost.org/forum/viewtopic.php?t=569",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAADYUlEQVR42m2Te0yTVxjG"
        "n9Pv0tJ26BQbWkMrif5hgBoU4pgsBJhx08RKtIrxAmJkKiwo848RGRabsZvJQDQRLyFe"
        "g6BGTUB0Ik1M8EbjhsPLlMJENGQtVVCgX/v17HydWyTuTZ6cNyfn/Z3nvHkPwYSgwDa2"
        "VL+718K05G1uE4AzbOWZrjItDBFWxP939ghTKk6hHXHQURnjhINm8CVIsw14KQFp0Jek"
        "4vVrpeQJ0yyQyK1vIwYBePeITxPqRuOe9AuIjXmBZ896AjKytcDtGAITs2NiFUQGxjng"
        "4nYFsPpfwCRRwqtvhJ/uZu6MXb05V96U38B9XzN36K8Ru0EQfjOp1RiwJg3CPPU51LwH"
        "R4+KOQqAFhQcgetqBhKy7uFWUhq2eA/jYH0eZqb9iZvLrHLwXqCXiH6OjprNwqQhGuNq"
        "Cwe7Z6u8b76OAIIm0wD8/smIMoxjeH00F3IK5B9L7FnbhrEveh/Kqzfih6pDWL6uCLn2"
        "Itk3nMX9crl7acRBYWEd2q5kISH9Pm4kp8F42I+eXiOdtchDPIkm+nFHHb3RvR4L5p9Q"
        "tbR8gWnWb+VwOs/5ag0KIEynTBlindVBYxjDWL4WD1ZkY5m9FotKr6FxZDm2DlXjQFMx"
        "SopqaWmpg6zN3xzyTp7OtVabIw7kiopKnD2dA2vm73DNziC2rnPkdOMaasp8QfqTDJjv"
        "OonbD+34KLUJl1vXQp/ohJCth79GbyMWSy9taFiFL7fuRXxKH9oTM6m3xEBFIQDJoMaH"
        "G32kkt9Bfj5WRr/a/iOKi6oI9Pu9MKuCuB/OI2r1WJ/Sr0BADVV0GPrCEcvwng9woGYT"
        "zvfkoDXwKdI76+F+ZEfynPPBjo7PBNBaO8BdADREeQJ5d3BnxHuuhIJxluP1ufTarwu5"
        "c9cLzN0XRSJGSZDGxBDQz0O1dwUoA9AofsIkRn4D4zU3X8DnixuhIo+1tsWNI23Xdapb"
        "7RnYUHMCdx7GQXTvXilRXRNzIEy4XQlCKMrLK7C70ql40ybP7bzU/9Si8z2fRlPsXbL7"
        "gZEXPc4dkqx1MQD/HkCJsrIyVFV9F8mt1k4M+qZjcMCIlDNdcI8aIeY5IYF9D2jwvwCH"
        "w4FduxyRfN48t6a3bwYGHpvwSXEn3H/EQrzrlKSwNqwA/gbEbU6NEWivbAAAAABJRU5E"
        "rkJggg=="
    ),
)

import wx
import time
import threading
from os.path import abspath, join, dirname
from ctypes import (
    c_int,
    c_char_p,
    WINFUNCTYPE,
    WinDLL,
    byref,
    c_ubyte,
    c_uint,
    POINTER,
    pointer,
    addressof
)

DLL_PATH = abspath(join(dirname(__file__), "Tira2.dll"))

TIRA_SIX_BYTE_CALLBACK = WINFUNCTYPE(c_int, c_char_p)



class Tira(eg.RawReceiverPlugin):

    def __init__(self):
        self.dll = None
        eg.RawReceiverPlugin.__init__(self)
        self.inTest = False
        self.AddAction(TransmitIR)


    def __start__(self, port=2):
        dll = WinDLL(DLL_PATH)
        if dll.tira_init():
            raise self.Exceptions.DeviceInitFailed(
                "Function tira_init failed."
            )
        if dll.tira_start(port):
            raise self.Exceptions.DeviceInitFailed(
                "Function tira_start failed."
            )
        self.procHandler = TIRA_SIX_BYTE_CALLBACK(self.MyEventCallback)
        if dll.tira_set_handler(self.procHandler):
            raise self.Exceptions.DeviceInitFailed(
                "Function tira_set_handler failed."
            )
        self.dll = dll


    def __stop__(self):
        if self.dll is None:
            return
        if self.dll.tira_stop():
            raise eg.Exception("Tira stop failed.")


    def __close__(self):
        if self.dll is None:
            return
        if self.dll.tira_cleanup():
            raise eg.Exception("Tira cleanup failed.")


    def MyEventCallback(self, eventString):
        eventsuffix = eventString
        self.TriggerEvent(eventsuffix)
        return 0


    def Configure(self, port=2):
        panel = eg.ConfigPanel(self)
        portCtrl = panel.SerialPortChoice(port)
        panel.AddLine("Virtual COM Port:", portCtrl)
        while panel.Affirmed():
            panel.SetResult(portCtrl.GetValue())



class TransmitIR(eg.ActionBase):
    name = "Transmit IR"
    repeatCount = 1

    def __call__(self, irData="", repeatCount=1, frequency=-1):
        if self.plugin.dll is None:
            raise self.Exceptions.DeviceNotReady
        if self.plugin.dll.tira_transmit(
            repeatCount-1, frequency, c_char_p(irData), len(irData)
        ):
            raise self.Exception("Error in tira_transmit")


    def GetLabel(self, *dummyArgs):
        return self.name


    def Configure(self, irData="", repeatCount=1, frequency=-1):
        def MakeHexString(data):
            return " ".join([("%0.2X" % ord(c)) for c in data])

        def MakeStringFromHex(data):
            result = ""
            for hexdigit in data.split(" "):
                if len(hexdigit) == 2:
                    result += chr(int(hexdigit, 16))
            return result

        panel = eg.ConfigPanel(self)
        style = wx.TE_MULTILINE|wx.TE_BESTWRAP
        codeBox = wx.TextCtrl(
            panel,
            -1,
            MakeHexString(irData),
            size=(300, 150),
            style=style
        )
        panel.sizer.Add(codeBox, 1, wx.EXPAND)
        panel.sizer.Add((5, 5))

        lowerSizer = wx.BoxSizer(wx.HORIZONTAL)
        staticText = wx.StaticText(panel, -1, "Repeat count:")
        lowerSizer.Add(staticText, 0, wx.ALIGN_CENTER_VERTICAL)

        repeatBox = eg.SpinIntCtrl(panel, min=1, value=repeatCount)
        lowerSizer.Add(repeatBox)
        lowerSizer.Add((5, 5), 1, wx.EXPAND)

        def OnCapture(dummyEvent):
            dlg = IRLearnDialog(panel, self.plugin.dll)
            dlg.ShowModal()
            if dlg.result is not None:
                codeBox.SetValue(MakeHexString(dlg.result))
            dlg.Destroy()

        captureButton = wx.Button(panel, -1, "Learn IR Code")
        lowerSizer.Add(captureButton, 0, wx.ALIGN_RIGHT)
        captureButton.Bind(wx.EVT_BUTTON, OnCapture)

        panel.sizer.Add(lowerSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                MakeStringFromHex(codeBox.GetValue()),
                repeatBox.GetValue(),
                -1,
            )



class IRLearnDialog(wx.Dialog):

    def __init__(self, parent, dll):
        self.dll = dll
        self.result = None
        self.shouldRun = True
        wx.Dialog.__init__(self, parent, -1,
            "Learn IR Code",
            style=wx.CAPTION
        )

        text = (
            "1. Aim remote directly at the Tira approximately 1 inches "
            "from Tira face.\n\n"
            "2. PRESS and HOLD the desired button on your remote until "
            "learning is complete..."
        )
        staticText = wx.StaticText(self, -1, text, style=wx.ST_NO_AUTORESIZE)
        def OnCancel(dummyEvent):
            self.shouldRun = False
            self.EndModal(wx.OK)

        cancelButton = wx.Button(self, -1, eg.text.General.cancel)
        cancelButton.Bind(wx.EVT_BUTTON, OnCancel)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(staticText, 1, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(
            cancelButton,
            0,
            wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL,
            5
        )

        self.SetSizer(mainSizer)
        self.SetAutoLayout(True)
        mainSizer.Fit(self)

        self.captureThread = threading.Thread(target=self.CaptureLoop)
        self.captureThread.start()


    def CaptureLoop(self):
        #featureValue = c_uint(0x1)
        #self.dll.tira_access_feature(0xF0000000, 1, byref(featureValue), 0x0)
        dll = self.dll
        if dll is None:
            return
        dll.tira_start_capture()
        size = c_int()
        data = pointer(c_ubyte())
        while self.shouldRun:
            dll.tira_get_captured_data(byref(data), byref(size))
            if size.value != 0:
                break
            else:
                time.sleep(0.01)
        if self.shouldRun:
            result = ""
            for x in data[:size.value]:
                result += chr(x)
            self.result = result
            dll.tira_delete(data)
        else:
            dll.tira_cancel_capture()

