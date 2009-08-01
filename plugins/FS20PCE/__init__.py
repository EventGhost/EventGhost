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

Commands = {
    0x00 : "Power.Off",
    0x01 : "Power.Dim.1",
    0x02 : "Power.Dim.2", 
    0x03 : "Power.Dim.3",
    0x04 : "Power.Dim.4",
    0x05 : "Power.Dim.5",
    0x06 : "Power.Dim.6",
    0x07 : "Power.Dim.7",
    0x08 : "Power.Dim.8",
    0x09 : "Power.Dim.9",
    0x10 : "Power.Dim.10",
    0x11 : "Power.Dim.11",
    0x12 : "Power.Dim.12",
    0x13 : "Power.Dim.13",
    0x14 : "Power.Dim.14",
    0x15 : "Power.Dim.15",
    0x16 : "Power.On",
    0x17 : "Power.Previous",
    0x18 : "Power.Toggle",
    0x19 : "Power.Dim.Up",
    0x20 : "Power.Dim.Down",
    0x21 : "Power.Dim.UpAndDown",
    0x22 : "Program.Time",
    0x23 : "SendStatus",
    0x24 : "Power.Timed.OffPreviousValue",
    0x25 : "Power.Timed.OnOff",
    0x26 : "Power.Timed.PreviousValueOff",
    0x27 : "Program.Reset",
    0x28 : "Program.DimUpTime",
    0x29 : "Program.DimDownTime",
    0x30 : "Power.Timed.OnPreviousState",
    0x31 : "Power.Timed.PreviousValuePreviousState",
}

class FS20PCE(eg.PluginClass):
    def RawCallback(self, data):
        if not data or len(data) != 13 or ord(data[0]) != 2 or ord(data[1]) != 11:
            self.PrintError("invalid data")
            return
        
        #versionMajor = ord(data[12]) / 16
        #versionMinor = ord(data[12]) % 16
        
        houseCode = binascii.hexlify(data[2:6])
        deviceAddress = binascii.hexlify(data[6:8])
        command = ord(data[8])
        if command in Commands:
            commandStr = Commands[command]
        else:
            commandStr = binascii.hexlify(data[8]).upper()

        self.TriggerEvent(houseCode + "." + deviceAddress + "." + commandStr)
            
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
   
