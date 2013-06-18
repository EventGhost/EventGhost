
import eg
import wx
from eg.cFunctions import StartLircReceiver, StopLircReceiver



class Lirc(eg.RawReceiverPlugin):
    canMultiLoad = True
    
    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)
        self.handle = None;
        self.irDecoder = eg.IrDecoder2(0.000001, self)
    
    
    def __start__(self, port=0):
        self.handle = StartLircReceiver(self.irDecoder.Decode, port)
        
        
    def __stop__(self):
        if self.handle is not None:
            StopLircReceiver(self.handle)
        
        
    def __close__(self):
        self.irDecoder.Stop()
        
        
    def Configure(self, port=0):
        dialog = eg.ConfigurationDialog(self)
        st1 = wx.StaticText(dialog, -1, "COM Port:")
        dialog.sizer.Add(st1)
        portCtrl = eg.SerialPortChoice(dialog, value=port)
        
        dialog.sizer.Add(portCtrl)
        dialog.sizer.Add((10,10))
        
        if dialog.AffirmedShowModal():
            return (
                portCtrl.GetValue(),
            )

        
    
