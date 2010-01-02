"""<rst>
Allows to send commands to FS20 receivers.

|

|fS20Image|_

`Direct shop link <http://www.elv.de/output/controller.aspx?cid=74&detail=10&detail2=27743>`__

.. |fS20Image| image:: picture.jpg
.. _fS20Image: http://www.elv.de/
"""

eg.RegisterPlugin(
    name = "ELV FS20 PCS",
    author = "Bartman",
    version = "0.1." + "$LastChangedRevision: 614 $".split()[1],
    kind = "external",
    canMultiLoad = False,
    description = __doc__,
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=2147",
    guid = '{D76A6D18-142A-4f75-8F93-9CDA86DBC310}'
)

import binascii
import math
import sys
import wx.lib.mixins.listctrl as listmix
from wx.lib.masked import TextCtrl
import wx.lib.masked as masked
from eg.WinApi.HID import HIDThread
from eg.WinApi.HID import GetDevicePath
from eg.WinApi.HID import IsDeviceName

class Text:
    errorFind = "Error finding ELV FS20 PCS"

VENDOR_ID = 6383
PRODUCT_ID = 57365

COMMAND_FIRMWARE = 0xF0
COMMAND_SEND_ONCE = 0xF1
COMMAND_SEND_REPEAT = 0xF2
COMMAND_ABORT = 0xF3

class FS20PCS(eg.PluginClass):
    def __init__(self):
        self.version = None
        self.thread = None
        self.waitingForResponse = False
        self.AddAction(Off)
        self.AddAction(On)
        self.AddAction(Dim)
        self.AddAction(ToggleDim)
        self.AddAction(DimDown)
        self.AddAction(DimUp)
        self.AddAction(Toggle)
        self.AddAction(Abort)


    def RawCallback(self, data):
        if eg.debugLevel:
            print "FS20PCS RawCallBack", binascii.hexlify(data)

        if len(data) != 5 or data[0:3] != "\x02\x03\xA0":
            self.PrintError("data must have a length of 5 and start with 02 03 A0")
        errorId = ord(data[3:4])
        if errorId == 0:
            self.waitingForResponse = False
            #everything is fine
        elif errorId == 1:
            #Firmware version was requested
            self.version = ord(data[4:5])
        elif errorId == 2:
            #Firmware version was requested
            self.version = ord(data[4:5])
        elif errorId == 3:
            self.PrintError("Unknown command id")
        elif errorId == 4:
            self.PrintError("invalid command length")
        elif errorId == 5:
            self.PrintError("nothing to abort")
        else:
            self.PrintError("Unknown Error")

    def PrintVersion(self):
        #create the following python command to show version number
        #eg.plugins.FS20PCS.plugin.PrintVersion()
        versionMajor = self.version / 16
        versionMinor = self.version % 16
        print "Firmware version %d.%d" % (versionMajor, versionMinor)

    def StopCallback(self):
        self.TriggerEvent("Stopped")
        self.waitingForResponse = False
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

    def SendRawCommand(self, data, timeout):
        if not self.thread:
            self.PrintError("Plug in is not running.")
            return
        dataLength = len(data)
        if eg.debugLevel:
            print "FS20PCS SendRawCommand", binascii.hexlify(data)
        newData = data + ((11 - dataLength) * '\x00')
        try:
            self.waitingForResponse = True
            self.thread.Write(newData, timeout + 1000)#extra seconds to wait for response
        except:
            self.waitingForResponse = False

    def Abort(self):
        if self.waitingForResponse:
            self.SendRawCommand("\x01\x01\xf3", 0)
        
    def RequestVersion(self):
        data = '\x01\x01\xF0'
        self.SendRawCommand(data, 0)

    def SetupHidThread(self, newDevicePath):
        #create thread
        self.thread = HIDThread(self.name, newDevicePath)
        self.thread.SetStopCallback(self.StopCallback)
        self.thread.SetRawCallback(self.RawCallback)
        self.thread.start()
        self.RequestVersion()

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


def GetStringFromAddress(address, formatted = False):
    valueStr = ""
    for i in range(11, -1, -1):
        x = (address >> i*2) & 0x03
        valueStr += str(x + 1)
        if i == 4 and formatted:
            valueStr += " - "
        if i == 8 and formatted:
            valueStr += " "
    return valueStr

def GetAddressFromString(addressString):
    address = 0
    for i in range(12):
        address <<= 2
        address += int(addressString[i]) - 1
    return address


class ActionBase(eg.ActionBase):
    defaultAddress = 0x094001
    funccode = None # must be assigned by subclass

    def __call__(self, address, timeCode, repeatCount):
        if repeatCount > 1:
            data = "\x01\x07\xf2"
        else:
            data = "\x01\x06\xf1"
            
        x, a0 = divmod(address, 256)
        a2, a1 = divmod(x, 256)
        data += chr(a2)
        data += chr(a1)
        data += chr(a0)
        
        if timeCode == 0:
            data += chr(self.funccode)
            data += "\x00"
        else:
            data += chr(self.funccode + 32)
            data += chr(timeCode);
        
        if repeatCount > 1:
            data += chr(repeatCount)
        self.plugin.SendRawCommand(data, repeatCount * 250)

    def GetLabel(self, address, timeCode, repeatCount):
        return self.name + " " + GetStringFromAddress(address, True)

    def Configure(self, address = None, timeCode = 0, repeatCount = 1):
        if address is None:
            address = self.defaultAddress
            
        timerIndex = 0
        
        timerValues = []
        startRange = 0
        for i in range(0,13):
            timeFactor = (2**i) * 0.25
            for j in range(startRange,16):
                tempTimeCode = (i*16) + j
                if timeCode == tempTimeCode:
                    timerIndex = len(timerValues)

                tempTimeValue = timeFactor * j
                hours = math.floor(tempTimeValue / 3600)
                minutes = math.floor((tempTimeValue - (hours * 3600)) / 60)
                seconds = tempTimeValue - (hours * 3600) - minutes * 60
                if hours > 0:
                    tempTimeFormatted = "%0d h %00d m %00d s" % (hours, minutes, seconds)
                elif minutes > 0:
                    tempTimeFormatted = "%00d m %00d s" % (minutes, seconds)
                else:
                    tempTimeFormatted = "%0.02f sec" % tempTimeValue
                timerValues.append((tempTimeCode, tempTimeValue, tempTimeFormatted))
            startRange = 8 #prevents duplicate entries

        panel = eg.ConfigPanel()

        maskedCtrl = masked.TextCtrl(
            parent=panel,
            mask="#### #### - ####",
            defaultValue="1111 1111 - 1111",
            excludeChars="056789",
            formatcodes="F",
            validRequired=False,
        )
        maskedCtrl.SetValue(GetStringFromAddress(address))
        
        def TimerCallback(value):
            return timerValues[value][2]
        
        timerCtrl = eg.Slider(
            panel, 
            value=timerIndex, 
            min=0, 
            max=len(timerValues) - 1, 
            minLabel=timerValues[0][2],
            maxLabel=timerValues[len(timerValues) - 1][2],
            style = wx.SL_TOP,
            size=(300,-1),
            levelCallback=TimerCallback
        )
        timerCtrl.SetMinSize((300, -1))

        repeatCtrl = eg.Slider(
            panel, 
            value=repeatCount, 
            min=1, 
            max=255, 
            minLabel="1",
            maxLabel="255",
            style = wx.SL_TOP,
            size=(300,-1),
        )
        repeatCtrl.SetMinSize((300, -1))

        panel.AddLine("Address:", maskedCtrl)
        panel.AddLine("Timer value:", timerCtrl)
        panel.AddLine("Repeat:", repeatCtrl)

        while panel.Affirmed():
            address = GetAddressFromString(maskedCtrl.GetPlainValue())
            ActionBase.defaultAddress = address
            panel.SetResult(address, timerValues[timerCtrl.GetValue()][0], repeatCtrl.GetValue())
            

class Dim(ActionBase):
    name = "Set dim-level"
    
    def __call__(self, address, level):
        x, a0 = divmod(address, 256)
        a2, a1 = divmod(x, 256)
        self.plugin.WriteFhz(0x04, 0x02, 0x01, 0x01, a2, a1, a0, level)
    
    
    def GetLabel(self, address, level):
        return "Set dim-level to %.02f %%" % (level * 100.00 / 16)
    
    
    def Configure(self, address=None, level=1):       
        if address is None:
            address = self.defaultAddress
        panel = eg.ConfigPanel()
            
        maskedCtrl = masked.TextCtrl(
            parent=panel,
            mask="#### #### - ####",
            defaultValue="1111 1111 - 1111",
            excludeChars="056789",
            formatcodes="F",
            validRequired=False,
        )
        maskedCtrl.SetValue(GetStringFromAddress(address))
        
        def LevelCallback(value):
            return "%.02f %%" % (value * 100.00 / 16)
        
        levelCtrl = eg.Slider(
            panel, 
            value=level, 
            min=0, 
            max=16, 
            minLabel="0.00 %",
            maxLabel="100.00 %",
            style = wx.SL_AUTOTICKS|wx.SL_TOP,
            size=(300,-1),
            levelCallback=LevelCallback
        )
        levelCtrl.SetMinSize((300, -1))
        
        panel.AddLine("Address:", maskedCtrl)
        panel.AddLine("Level:", levelCtrl)
        
        while panel.Affirmed():
            address = GetAddressFromString(maskedCtrl.GetPlainValue())
            ActionBase.defaultAddress = address
            panel.SetResult(
                address, 
                levelCtrl.GetValue(),
            )

class Off(ActionBase):
    funccode = 0x00
    
    
    
class On(ActionBase):
    funccode = 0x10


class ToggleDim(ActionBase):
    name = "Toggle dimming"
    funccode = 0x15


class DimUp(ActionBase):
    name = "Dim up"
    funccode = 0x13


class DimDown(ActionBase):
    name = "Dim down"
    funccode = 0x14


class Toggle(ActionBase):
    funccode = 0x12

class Abort(eg.ActionBase):
    name = "Abort transmitting"
    
    def __call__(self):
        self.plugin.Abort()