eg.RegisterPlugin(
    name = "ELV FS20 PCE",
    author = "Bartman",
    version = "0.1." + "$LastChangedRevision: 614 $".split()[1],
    kind = "remote",
    canMultiLoad = False,
    description = (
        'Allows to recieve events from FS20 remote controls.<br/>'
        '<a href="http://elv.de/"><img src=\"picture.jpg\"/></a>'
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=571",
)

import binascii
from eg.WinApi.HID import HIDThread
from eg.WinApi.HID import GetDevicePath
from eg.WinApi.HID import GetDeviceDescriptions
from eg.WinApi.HID import DeviceDescription

class Text:
    errorFind = "Error finding ELV FS20 PCE"

class FS20PCE(eg.PluginClass):
    def RawCallback(self, data):
        self.TriggerEvent(binascii.hexlify(data).upper())
            
    def StopCallback(self):
        self.TriggerEvent("Stopped")
        self.thread = None

    def GetMyDevicePath(self):
        path = GetDevicePath(
            None,
            6383,
            57364,
            None,
            0,
            False)
        return path;
    
    def SetupHidThread(self, newDevicePath):
        #create thread
        self.thread = HIDThread(self.name, newDevicePath)
        self.thread.start()
        self.thread.SetStopCallback(self.StopCallback)
        self.thread.SetRawCallback(self.RawCallback)
    
    def ReconnectDevice(self, event):
        """method to reconnect a disconnect device"""
        if self.thread == None:
            #updating device list
            
            #check if the right device was connected
            #getting devicePath
            newDevicePath = self.GetMyDevicePath()
            if not newDevicePath:
                #wrong device
                return
            
            self.SetupHidThread(newDevicePath)

    def __start__(self):
        #Bind plug in to RegisterDeviceNotification message 
        eg.Bind("System.DeviceAttached", self.ReconnectDevice)
        
        newDevicePath = self.GetMyDevicePath()
        if not newDevicePath:
            #device not found
            self.PrintError(Text.errorFind)
        else:
            self.SetupHidThread(newDevicePath)

    def __stop__(self):
        if self.thread:
            self.thread.AbortThread()
        
        #unbind from RegisterDeviceNotification message
        eg.Unbind("System.DeviceAttached", self.ReconnectDevice)
   
