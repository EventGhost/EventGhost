eg.RegisterPlugin(
    name = "ELV FS20 PCE",
    author = "Bartman",
    version = "0.1." + "$LastChangedRevision: 614 $".split()[1],
    kind = "remote",
    canMultiLoad = False,
    description = (
        'Allows to receive events from FS20 remote controls.<br/>'
        '<a href="http://www.elv.de/"><img src=\"picture.jpg\"/></a>'
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=571",
)

import binascii
from eg.WinApi.HID import HIDThread
from eg.WinApi.HID import GetDevicePath
from eg.WinApi.HID import IsDeviceName

class Text:
    errorFind = "Error finding ELV FS20 PCE"

VENDOR_ID = 6383
PRODUCT_ID = 57364

Commands = {
    0x00 : "Do.Off",
    0x01 : "Do.Dim.6%",
    0x02 : "Do.Dim.13%", 
    0x03 : "Do.Dim.19%",
    0x04 : "Do.Dim.25%",
    0x05 : "Do.Dim.31%",
    0x06 : "Do.Dim.38%",
    0x07 : "Do.Dim.44%",
    0x08 : "Do.Dim.50%",
    0x09 : "Do.Dim.56%",
    0x10 : "Do.Dim.63%",
    0x11 : "Do.Dim.69%",
    0x12 : "Do.Dim.75%",
    0x13 : "Do.Dim.81%",
    0x14 : "Do.Dim.98%",
    0x15 : "Do.Dim.94%",
    0x16 : "Do.On",
    0x17 : "Do.Previous",
    0x18 : "Do.Toggle",
    0x19 : "Do.Dim.LevelUp",
    0x20 : "Do.Dim.LevelDown",
    0x21 : "Do.Dim.UpAndDown",
    0x22 : "Program.Time",
    0x23 : "Program.SendStatus",
    0x24 : "Do.OffPreviousValue",
    0x25 : "Do.OnOff",
    0x26 : "Do.PreviousValueOff",
    0x27 : "Program.Reset",
    0x28 : "Program.DimUpTime",
    0x29 : "Program.DimDownTime",
    0x30 : "Do.OnPreviousState",
    0x31 : "Do.PreviousValuePreviousState",
}

class FS20PCE(eg.PluginClass):
    def __init__(self):
        self.version = None
        self.thread = None
        self.PendingEvents = {}
    
    def RawCallback(self, data):
        if not data or len(data) != 13 or ord(data[0]) != 2 or ord(data[1]) != 11:
            self.PrintError("invalid data")
            return
        
        self.version = ord(data[12])
        
        houseCode = binascii.hexlify(data[2:6])
        deviceAddress = binascii.hexlify(data[6:8])
        combinedAddress = houseCode + "." + deviceAddress
        
        command = ord(data[8])
        if command in Commands:
            commandStr = Commands[command]
        else:
            commandStr = binascii.hexlify(data[8]).upper()
            
        if combinedAddress in self.PendingEvents:
            #cancel pending events for this device
            try:
                timerEntry = self.PendingEvents[combinedAddress]
                startTime, func, args, kwargs = timerEntry
                eg.scheduler.CancelTask(timerEntry)
                self.TriggerEvent(combinedAddress + "." + args[1] + ".Timer.Cancel")
                del self.PendingEvents[combinedAddress]
            except KeyError:
                #may happen due to multithreaded access to self.PendingEvents dict
                pass
            except ValueError:
                #may happen due to multithreaded access to eg.scheduler's internal list
                pass
        
        validTime = ord(data[9]) > 15
        if validTime:
            timeStr = binascii.hexlify(data[9:12])
            timeStr = timeStr[1:]#cut the one
            eventTime = float(timeStr) * 0.25
            if (commandStr.startswith("Do.")):
                #parsing time
                if (eventTime > 0):
                    timerEntry = eg.scheduler.AddTask(eventTime, self.SchedulerCallback, combinedAddress, commandStr)
                    self.PendingEvents[combinedAddress] = timerEntry
                    self.TriggerEvent(combinedAddress + "." + commandStr + ".Timer.Start", payload = eventTime)
                else:
                    self.TriggerEvent(combinedAddress + "." + commandStr)
            else:
                #put the time in the payload 
                self.TriggerEvent(combinedAddress + "." + commandStr, payload = eventTime)
        else:
            self.TriggerEvent(combinedAddress + "." + commandStr)
            
    def SchedulerCallback(self, combinedAddress, commandStr):
        if combinedAddress in self.PendingEvents:
            #cancel pending events for this device
            try:
                timerEntry = self.PendingEvents[combinedAddress]
                startTime, func, args, kwargs = timerEntry
                if (args[1] == commandStr):
                    #maybe an old entry if commandStr does not match 
                    self.TriggerEvent(combinedAddress + "." + commandStr + ".Timer.Finish")
                    del self.PendingEvents[combinedAddress]
            except KeyError:
                #may happen due to multithreaded access to self.PendingEvents dict
                pass
        
    def PrintVersion(self):
        #create the following python command to show version number
        #eg.plugins.FS20PCE.plugin.PrintVersion()
        if self.version == None:
            print "Need to receive data first. Please press a button and try again."
        else:
            versionMajor = self.version / 16
            versionMinor = self.version % 16
            print "Firmware version %d.%d" % (versionMajor, versionMinor) 
    
    def StopCallback(self):
        self.TriggerEvent("Stopped")
        self.thread = None

    def GetMyDevicePath(self):
        path = GetDevicePath(
            None,
            VENDOR_ID,
            PRODUCT_ID,
            None,
            0,
            True,
            0)
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
            if not IsDeviceName(event.payload, VENDOR_ID, PRODUCT_ID):
                return
            
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
   
