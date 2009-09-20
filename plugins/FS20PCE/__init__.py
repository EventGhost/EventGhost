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

import re
import binascii
from eg.WinApi.HID import HIDThread
from eg.WinApi.HID import GetDevicePath
from eg.WinApi.HID import IsDeviceName

class Text:
    errorFind = "Error finding ELV FS20 PCE"

VENDOR_ID = 6383
PRODUCT_ID = 57364

DirectCommands = {
    0x22 : "Program.Time",
    0x23 : "Program.SendStatus",
    0x27 : "Program.Reset",
    0x28 : "Program.DimUpTime",
    0x29 : "Program.DimDownTime",
}

DelayedCommands = {
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
    0x14 : "Do.Dim.88%",
    0x15 : "Do.Dim.94%",
    0x16 : "Do.On",
    0x17 : "Do.PreviousValue",
    0x18 : "Do.Toggle",
    0x19 : "Do.Dim.LevelUp",
    0x20 : "Do.Dim.LevelDown",
    0x21 : "Do.Dim.UpAndDown",
}

DoubleCommands = {
    0x24 : ("Do.Off", "Do.PreviousValue"),
    0x25 : ("Do.On", "Do.Off"),
    0x26 : ("Do.PreviousValue", "Do.Off"),
    0x30 : ("Do.On", "Do.PreviousState"),
    0x31 : ("Do.PreviousValue", "Do.PreviousState"),
}

def GetRegEx(pattern, length):
    if pattern == "*":
        return None
    if (len(pattern) != length):
        raise ValueError("length must be exactly " + str(length))
    for char in pattern:
        if char != '1' and char != '2' and char != '3' and char != '4' and char != '?': 
            raise ValueError("only 1, 2, 3, 4 and ? are allowed")
    regExPattern = pattern.replace('?', '.')
    return re.compile(regExPattern)


class FS20PCE(eg.PluginClass):
    def __init__(self):
        self.version = None
        self.thread = None
        self.PendingEvents = {}
        self.devicePatterns = []
    
    def RawCallback(self, data):
        if not data or len(data) != 13 or ord(data[0]) != 2 or ord(data[1]) != 11:
            self.PrintError("invalid data")
            return
        
        self.version = ord(data[12])
        
        houseCode = binascii.hexlify(data[2:6])
        deviceCode = binascii.hexlify(data[6:8])
        command = ord(data[8])
        names = self.GetDeviceNames(houseCode, deviceCode)
        
        #cancel pending events
        for deviceName in names:
            if deviceName in self.PendingEvents:
                #cancel pending events for this device
                try:
                    timerEntry = self.PendingEvents[deviceName]
                    startTime, func, args, kwargs = timerEntry
                    eg.scheduler.CancelTask(timerEntry)
                    self.TriggerEvent(deviceName + ".Cancel", payload = args[1])
                    del self.PendingEvents[deviceName]
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
            else:
                eventTime = 0 
                
            if command in DirectCommands:
                commandStr0 = DirectCommands[command]
                commandStr1 = None
                payload0 = (eventTime)
            elif command in DelayedCommands:
                if (validTime and eventTime):
                    commandStr0 = None
                    commandStr1 = DelayedCommands[command]
                    payload0 = (eventTime, commandStr1)
                else:
                    commandStr0 = DelayedCommands[command]
                    commandStr1 = None
                    payload0 = None
            elif command in DoubleCommands:
                commandStr0, commandStr1 = DoubleCommands[command]
                payload0 = (eventTime, commandStr1)
            else:
                commandStr0 = binascii.hexlify(data[8]).upper()
                commandStr1 = None
                payload0 = None
                
            if (commandStr0):
                self.TriggerEvent(deviceName + "." + commandStr0, payload = payload0)
            else:
                self.TriggerEvent(deviceName + ".Timer", payload = payload0)
                
            if (commandStr1):
                if (eventTime > 0):
                    timerEntry = eg.scheduler.AddTask(eventTime, self.SchedulerCallback, deviceName, commandStr1)
                    self.PendingEvents[deviceName] = timerEntry
                else:
                    self.TriggerEvent(deviceName + "." + commandStr1)
            
    def SchedulerCallback(self, deviceName, commandStr):
        if deviceName in self.PendingEvents:
            #cancel pending events for this device
            try:
                timerEntry = self.PendingEvents[deviceName]
                startTime, func, args, kwargs = timerEntry
                if (args[1] == commandStr):
                    #maybe an old entry if commandStr does not match 
                    self.TriggerEvent(deviceName + "." + commandStr)
                    del self.PendingEvents[deviceName]
            except KeyError:
                #may happen due to multithreaded access to self.PendingEvents dict
                pass
        
    def GetDeviceNames(self, houseCode, deviceCode):
        names = [houseCode + "." + deviceCode]
        for houseCodeRegEx, deviceCodeRegEx, deviceName in self.devicePatterns:
            if (deviceName in names):
                continue
            houseCodeMatch = houseCodeRegEx == None or houseCodeRegEx.match(houseCode)
            deviceCodeMatch = deviceCodeRegEx == None or deviceCodeRegEx.match(deviceCode)
            if (houseCodeMatch and deviceCodeMatch):
                names.append(deviceName)
        return names
    
    def AddDeviceNamePattern(self, houseCodePattern, deviceCodePattern, deviceName):
        houseCodeRegEx = GetRegEx(houseCodePattern, 8)
        deviceCodeRegEx = GetRegEx(deviceCodePattern, 4)
        self.devicePatterns.append((houseCodeRegEx, deviceCodeRegEx, deviceName))
            
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
   
