import eg
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
        
        if dialog.AffirmedShowModal():
            return (
                portCtrl.GetValue(),
            )
        
    
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
        
        if dialog.AffirmedShowModal():
            return (
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
        

