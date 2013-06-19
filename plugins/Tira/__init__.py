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
    name = "Home Electronics Tira",
    author = "Bitmonster",
    version = "1.0." + "$LastChangedRevision$".split()[1],
    kind = "remote",
    description = (
        'Hardware plugin for the <a href="http://www.home-electro.com/">'
        'Home Electronics Tira</a> transceiver.'
        '\n\n<p>'
        '<a href=http://www.home-electro.com/><p>'
        '<center><img src="tira.png" alt="Tira2" /></a></center>'
    ),
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

dll_path = abspath(join(dirname(__file__), "Tira2.dll"))

TIRA_SIX_BYTE_CALLBACK = WINFUNCTYPE(c_int, c_char_p)



class Tira(eg.RawReceiverPlugin):
    
    def __init__(self):
        self.dll = None
        eg.RawReceiverPlugin.__init__(self)
        self.inTest = False
        self.AddAllActions()
        
    
    def __start__(self, port=2):
        dll = WinDLL(dll_path)
        
        if dll.tira_init():
            raise eg.Exception("Tira init failed.")
        if dll.tira_start(port):
            raise eg.Exception("Tira start failed.")
        self.procHandler = TIRA_SIX_BYTE_CALLBACK(self.MyEventCallback)
        if dll.tira_set_handler(self.procHandler):
            raise eg.Exception("Tira set handler failed.")
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
        
        
    def MyEventCallback(self, event_ctring):
        eventsuffix = event_ctring
        self.TriggerEvent(eventsuffix)
        return 0
        
        
    def Configure(self, port=2):
        dialog = eg.ConfigurationDialog(self)
        st1 = wx.StaticText(dialog, -1, "Virtual COM Port:")
        dialog.sizer.Add(st1)
        portCtrl = eg.SerialPortChoice(dialog, value=port)
        
        dialog.sizer.Add(portCtrl)
        dialog.sizer.Add((10,10))
        
        yield dialog
        yield (portCtrl.GetValue(), )
        
    
class TransmitIR(eg.ActionClass):
    name = "Transmit IR"
    repeatCount = 1
        
    def __call__(self, irData="", repeatCount=1, frequency=-1):
        if self.plugin.dll.tira_transmit(
            repeatCount-1, frequency, c_char_p(irData), len(irData)
        ):
            raise eg.Exception("Error in tira transmit")
        
        
    def GetLabel(self, *args):
        return self.name
    
    
    def Configure(self, irData="", repeatCount=1, frequency=-1):
        def make_hex_string(buffer):
            result = ""
            for x in buffer:
                result += "%0.2X " % ord(x)
            return result
                
        def make_string_from_hex(buffer):
            result = ""
            for hexdigit in buffer.split(" "):
                if len(hexdigit) == 2:
                    result += chr(int(hexdigit, 16))
            return result
                
        dialog = eg.ConfigurationDialog(self)
        style = wx.TE_MULTILINE|wx.TE_BESTWRAP
        codeBox = wx.TextCtrl(
            dialog, 
            -1, 
            make_hex_string(irData), 
            size=(300, 150), 
            style=style
        )
        dialog.sizer.Add(codeBox, 1, wx.EXPAND)
        dialog.sizer.Add((5,5))
        
        lowerSizer = wx.BoxSizer(wx.HORIZONTAL)
        staticText = wx.StaticText(dialog, -1, "Repeat count:")
        lowerSizer.Add(staticText, 0, wx.ALIGN_CENTER_VERTICAL)
        
        repeatBox = eg.SpinIntCtrl(dialog, min=1, value=repeatCount)
        lowerSizer.Add(repeatBox)
        lowerSizer.Add((5,5), 1, wx.EXPAND)
        
        def OnCapture(event):
            dlg = IRLearnDialog(dialog, self.plugin.dll)
            dlg.ShowModal()
            if dlg.result is not None:
                codeBox.SetValue(make_hex_string(dlg.result))
        
        captureButton = wx.Button(dialog, -1, "Learn IR Code")
        lowerSizer.Add(captureButton, 0, wx.ALIGN_RIGHT)
        captureButton.Bind(wx.EVT_BUTTON, OnCapture)
        
        dialog.sizer.Add(lowerSizer, 0, wx.EXPAND)
        
        yield dialog
        yield (
            make_string_from_hex(codeBox.GetValue()),
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
        staticText = wx.StaticText(self, -1, text,
                                        style=wx.ST_NO_AUTORESIZE)
        def OnCancel(event):
            self.shouldRun = False
            
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
        dll.tira_start_capture()
        size = c_int()
        buffer = pointer(c_ubyte())
        while self.shouldRun:
            res = dll.tira_get_captured_data(byref(buffer), byref(size))
            if size.value != 0:
                break
            else:
                time.sleep(0.01)
        if self.shouldRun:
            result = ""
            for x in buffer[:size.value]:
                result += chr(x)
            self.result = result
            dll.tira_delete(buffer)
        else:
            dll.tira_cancel_capture()
        self.EndModal(wx.OK)
        

