"""<rst>
Allows to send commands to FS20 receivers.

|

|fS20Image|_

`Direct shop link <http://www.elv.de/output/controller.aspx?cid=74&detail=10&detail2=27743>`__

.. |fS20Image| image:: picture.jpg
.. _fS20Image: http://www.elv.de/
"""
import time

eg.RegisterPlugin(
    name = "ELV FS20 PCS",
    author = "Bartman",
    version = "0.2." + "$LastChangedRevision: 614 $".split()[1],
    kind = "external",
    canMultiLoad = False,
    createMacrosOnAdd = True,
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
TIME_OUT = 250

class FS20PCS(eg.PluginClass):
    def __init__(self):
        self.version = None
        self.thread = None
        self.waitingForResponse = False
        self.AddAction(Off)
        self.AddAction(On)
        self.AddAction(PreviousValue)
        self.AddAction(Toggle)
        self.AddAction(DimDown)
        self.AddAction(DimUp)
        self.AddAction(Dim)
        self.AddAction(DimTimer)
        self.AddAction(DimAlternating)
        
        self.AddAction(OffPreviousValueInternal)
        self.AddAction(OnOffInternal)
        self.AddAction(PreviousValueOffInternal)
        self.AddAction(OnPreviousStateInternal)
        self.AddAction(PreviousValuePreviousStateInternal)
        
        self.AddAction(OffPreviousValueTimer)
        self.AddAction(OnOffTimer)
        self.AddAction(PreviousValueOffTimer)
        self.AddAction(OnPreviousStateTimer)
        self.AddAction(PreviousValuePreviousStateTimer)
        
        self.AddAction(ProgramTimer)
        self.AddAction(ProgramCode)
        self.AddAction(ProgramFactoryDefaults)
        
        self.AddAction(ProgramInternalTimer)
        self.AddAction(ProgramDimUpRampTimer)
        self.AddAction(ProgramDimDownRampTimer)

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

    def SendRawCommand(self, data, timeout = 0):
        if not self.thread:
            self.PrintError("Plug in is not running.")
            return
        dataLength = len(data)
        if eg.debugLevel:
            print "FS20PCS SendRawCommand", binascii.hexlify(data)
        newData = data + ((11 - dataLength) * '\x00')
        try:
            self.waitingForResponse = True
            self.thread.Write(newData, timeout + 1000)#extra second to wait for response
        except:
            self.waitingForResponse = False

    def Abort(self):
        if self.waitingForResponse:
            self.SendRawCommand("\x01\x01\xf3")
        
    def RequestVersion(self):
        data = '\x01\x01\xf0'
        self.SendRawCommand(data)

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

def GetAddressBytes(address):
    x, a0 = divmod(address, 256)
    a2, a1 = divmod(x, 256)
    return chr(a2) + chr(a1) + chr(a0) 

def GetStringFromAddress(address, formatted = False):
    valueStr = ""
    for i in range(11, -1, -1):
        x = (address >> i*2) & 0x03
        valueStr += str(x + 1)
        if formatted:
            if i == 4:
                valueStr += " - "
            if i == 8:
                valueStr += " "
    return valueStr

def GetAddressFromString(addressString):
    address = 0
    for i in range(12):
        address <<= 2
        address += int(addressString[i]) - 1
    return address

def GetTimeCodeByIndex(index):
    if index < 16:
        return index
    return index + ((index / 8) - 1) * 8

def GetTimeCodeIndex(timeCode):
    if timeCode < 16:
        return timeCode
    return timeCode - (timeCode / 16) * 8

def GetTimeValue(timeCode):
    return (2**(timeCode / 16)) * 0.25 * (timeCode % 16)
    
def FormatTimeValue(timeValue):
    if timeValue >= 3600:
        hours = math.floor(timeValue / 3600)
        minutes = math.floor((timeValue - (hours * 3600)) / 60)
        seconds = timeValue - (hours * 3600) - minutes * 60
        return "%0d h %00d m %00d s" % (hours, minutes, seconds)
    elif timeValue >= 60:
        minutes = math.floor(timeValue / 60)
        seconds = timeValue - minutes * 60
        return "%00d m %00d s" % (minutes, seconds)
    else:
        return "%0.02f sec" % timeValue

class ActionBase(eg.ActionBase):
    defaultAddress = GetAddressFromString("123412342222") #0x094001
    
    funcCode = None
    name = None
    description = None
    labelFormat = None

    
    def GetAddressBytes(self, address):
        x, a0 = divmod(address, 256)
        a2, a1 = divmod(x, 256)
        return chr(a2) + chr(a1) + chr(a0) 

    def AddAddressControl(self, panel, address):
        if address is None:
            address = self.defaultAddress
        maskedCtrl = masked.TextCtrl(
            parent=panel,
            mask="#### #### - ####",
            defaultValue="1111 1111 - 1111",
            excludeChars="056789",
            formatcodes="F",
            validRequired=False,
        )
        maskedCtrl.SetValue(GetStringFromAddress(address))
        panel.AddLine("Address:", maskedCtrl)
        return maskedCtrl

    def AddTimerControl(self, panel, timeCode):
        def TimerCallback(value):
            timeCodeForValue = GetTimeCodeByIndex(value)
            return FormatTimeValue(GetTimeValue(timeCodeForValue))
        
        timerCtrl = eg.Slider(
            panel, 
            value=GetTimeCodeIndex(timeCode), 
            min=0, 
            max=111, 
            minLabel=FormatTimeValue(0),
            maxLabel=FormatTimeValue(15360),
            style = wx.SL_TOP,
            size=(300,-1),
            levelCallback=TimerCallback
        )
        timerCtrl.SetMinSize((300, -1))
        panel.AddLine("Timer value:", timerCtrl)
        return timerCtrl

    def AddRepeatControl(self, panel, repeatCount, maxValue):
        repeatCtrl = eg.Slider(
            panel, 
            value=repeatCount, 
            min=1, 
            max=maxValue, 
            minLabel="1",
            maxLabel=str(maxValue),
            style = wx.SL_TOP,
            size=(300,-1),
        )
        repeatCtrl.SetMinSize((300, -1))
        panel.AddLine("Repeat:", repeatCtrl)
        return repeatCtrl

    def AddLevelControl(self, panel, level):
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
        panel.AddLine("Level:", levelCtrl)
        return levelCtrl

class SimpleAction(ActionBase):
    """Base class for all action that only take an address as input 
    """
        
    def __call__(self, address):
        self.plugin.SendRawCommand("\x01\x06\xf1" + GetAddressBytes(address) + chr(self.funcCode))
        
    def GetLabel(self, address):
        return self.labelFormat.format(GetStringFromAddress(address, True))

    def Configure(self, address = None):
        panel = eg.ConfigPanel()

        maskedCtrl = self.AddAddressControl(panel, address)

        while panel.Affirmed():
            address = GetAddressFromString(maskedCtrl.GetPlainValue())
            ActionBase.defaultAddress = address
            panel.SetResult(address)
            

class RepeatAction(ActionBase):
    """Base class for all action that take an address and repeat Count 
    """
    
    def __call__(self, address, repeatCount):
        self.plugin.SendRawCommand("\x01\x07\xf2" + GetAddressBytes(address) +  chr(self.funcCode) + "\x00" + chr(repeatCount), repeatCount * TIME_OUT)
        
    def GetLabel(self, address, repeatCount):
        label = self.labelFormat.format(GetStringFromAddress(address, True))
        if repeatCount > 1:
            label = label + " " + str(repeatCount) + " times"
        return label

    def Configure(self, address = None, repeatCount = 1):
        panel = eg.ConfigPanel()

        maskedCtrl = self.AddAddressControl(panel, address)
        repeatCtrl = self.AddRepeatControl(panel, repeatCount, self.maxRepeatCount)
        ActionBase.defaultAddress = address

        while panel.Affirmed():
            address = GetAddressFromString(maskedCtrl.GetPlainValue())
            ActionBase.defaultAddress = address
            panel.SetResult(address, repeatCtrl.GetValue())

class TimerValueAction(ActionBase):
    """Base class for all action that take an address and repeat Count 
    """
    
    def __call__(self, address, timeCode):
        self.plugin.SendRawCommand("\x01\x06\xf1" + GetAddressBytes(address) +  chr(self.funcCode) + chr(timeCode))
        
    def GetLabel(self, address, timeCode):
        return self.labelFormat.format(GetStringFromAddress(address, True), FormatTimeValue(GetTimeValue(timeCode)))

    def Configure(self, address = None, timeCode = 0):
        panel = eg.ConfigPanel()

        maskedCtrl = self.AddAddressControl(panel, address)
        timerCtrl = self.AddTimerControl(panel, timeCode)
        ActionBase.defaultAddress = address

        while panel.Affirmed():
            address = GetAddressFromString(maskedCtrl.GetPlainValue())
            ActionBase.defaultAddress = address
            panel.SetResult(address, GetTimeCodeByIndex(timerCtrl.GetValue()))

class Off(SimpleAction):
    funcCode = 0x00
    name = "Off"
    description = "Turns device off (dim to 0%)"
    labelFormat = "Turn off {0}"
    
class On(SimpleAction):
    funcCode = 0x10
    name = "On"
    description = "Turns device on (dim to 100%)"
    labelFormat = "Turn on {0}"

class PreviousValue(SimpleAction):
    funcCode = 0x11
    name = "On with previous value"
    description = "Turns device on with previous value"
    labelFormat = "Turn on {0} with previous value"

class Toggle(SimpleAction):
    funcCode = 0x12
    name = "Toggle"
    description = "Toggles between off and previous value"
    labelFormat = "Toggle {0} between off and previous value"

class DimUp(RepeatAction):
    funcCode = 0x13
    name = "Dim up"
    description = "Dims up"
    labelFormat = "Dim up {0}"
    maxRepeatCount = 16

class DimDown(RepeatAction):
    funcCode = 0x14
    name = "Dim down"
    description = "Dims down"
    labelFormat = "Dim down {0}"
    maxRepeatCount = 16

class DimAlternating(RepeatAction):
    funcCode = 0x15
    name = "Alternating dim"
    description = "Dims up one level until maximum, then dim down"
    labelFormat = "Alternating dim {0}"
    maxRepeatCount = 255

class ProgramTimer(SimpleAction):
    funcCode = 0x16
    name = "Start/stop programming of internal timer"
    description = "Starts respectively stop programming of the internal timer"
    labelFormat = "Start/stop programming of internal timer for {0}"

class ProgramCode(SimpleAction):
    funcCode = 0x17
    name = "Program address"
    description = "Learn address"
    labelFormat = "Learn address {0}"

class OffPreviousValueInternal(SimpleAction):
    funcCode = 0x18
    name = "Off for internal timer value, previous value afterwards"
    description = "Turns off (dim to 0%) device for internal timer value and return to previous value afterwards"
    labelFormat = "Turn off {0} for internal timer value and return to previous value afterwards"

class OnOffInternal(SimpleAction):
    funcCode = 0x19
    name = "On (dim to 100%) for internal timer value, off afterwards"
    description = "Turns on (device dim to 100%) for internal timer value and turns it off afterwards"
    labelFormat = "Turn on {0} for internal timer value and turn off afterwards"

class PreviousValueOffInternal(SimpleAction):
    funcCode = 0x1a
    name = "Previous value for internal timer value, off afterwards"
    description = "Turns on device with previous value for internal timer value and turns it off afterwards"
    labelFormat = "Turn on {0} with previous value for internal timer value and turn off afterwards"

class ProgramFactoryDefaults(SimpleAction):
    funcCode = 0x1b
    name = "Reset to factory defaults"
    description = "Reset to factory defaults"
    labelFormat = "Reset {0} to factory defaults"

class OnPreviousStateInternal(SimpleAction):
    funcCode = 0x1e
    name = "On for internal timer value, previous state afterwards"
    description = "Turns on (dim to 100%) device for internal timer value and return to previous state afterwards"
    labelFormat = "Turn on {0} for internal timer value and return to previous state afterwards"

class PreviousValuePreviousStateInternal(SimpleAction):
    funcCode = 0x1f
    name = "Previous value for internal timer value, previous state afterwards"
    description = "Turns on device with previous value for internal timer value and return to previous state afterwards"
    labelFormat = "Turn on {0} with previous value for internal timer value and return to previous state afterwards"

class ProgramInternalTimer(TimerValueAction):
    funcCode = 0x36
    name = "Program internal timer value"
    description = "Program internal timer value"
    labelFormat = "Program internal timer value for {0} to {1}"

class ProgramDimUpRampTimer(TimerValueAction):
    funcCode = 0x3c
    name = "Program dim up ramp timer value"
    description = "Program dim up ramp timer value"
    labelFormat = "Program dim up ramp timer value for {0} to {1}"

class ProgramDimDownRampTimer(TimerValueAction):
    funcCode = 0x3d
    name = "Program dim down ramp timer value"
    description = "Program dim down ramp timer value"
    labelFormat = "Program dim down ramp timer value for {0} to {1}"

class OffTimer(TimerValueAction):
    funcCode = 0x20
    name = "Off in timer value"
    description = "Turns device off (dim to 0%) in timer value"
    labelFormat = "Turn off {0} in {1}"
    
class OnTimer(TimerValueAction):
    funcCode = 0x30
    name = "On in timer value"
    description = "Turns device on (dim to 100%) in timer value"
    labelFormat = "Turn on {0} in {1}"

class PreviousValueTimer(TimerValueAction):
    funcCode = 0x31
    name = "On with previous value in timer value"
    description = "Turns device on with previous value in timer value"
    labelFormat = "Turn on {0} with previous value in {1}"

class ToggleTimer(TimerValueAction):
    funcCode = 0x32
    name = "Toggle in timer value"
    description = "Toggles between off and previous value in timer value"
    labelFormat = "Toggle {0} between off and previous value in {1}"
    
class OffPreviousValueTimer(TimerValueAction):
    funcCode = 0x38
    name = "Off for timer value, previous value afterwards"
    description = "Turns off (dim to 0%) device for timer value and return to previous value afterwards"
    labelFormat = "Turn off {0} for timer value and return to previous value afterwards"

class OnOffTimer(TimerValueAction):
    funcCode = 0x39
    name = "On (dim to 100%) for timer value, off afterwards"
    description = "Turns on (device dim to 100%) for timer value and turns it off afterwards"
    labelFormat = "Turn on {0} for timer value and turn off afterwards"

class PreviousValueOffTimer(TimerValueAction):
    funcCode = 0x3a
    name = "Previous value for timer value, off afterwards"
    description = "Turns on device with previous value for timer value and turns it off afterwards"
    labelFormat = "Turn on {0} with previous value for timer value and turn off afterwards"

class OnPreviousStateTimer(TimerValueAction):
    funcCode = 0x3e
    name = "On for timer value, previous state afterwards"
    description = "Turns on (dim to 100%) device for timer value and return to previous state afterwards"
    labelFormat = "Turn on {0} for timer value and return to previous state afterwards"

class PreviousValuePreviousStateTimer(TimerValueAction):
    funcCode = 0x3f
    name = "Previous value for timer value, previous state afterwards"
    description = "Turns on device with previous value for timer value and return to previous state afterwards"
    labelFormat = "Turn on {0} with previous value for timer value and return to previous state afterwards" 

class Dim(ActionBase):
    name = "Dim"
    description = "Sets dim level immediately"
    labelFormat = "Set dim-level to {1:.02f} % for {0}"
    
    def __call__(self, address, level):
        self.plugin.SendRawCommand("\x01\x06\xf1" + GetAddressBytes(address) + chr(level))
    
    def GetLabel(self, address, level):
        return self.labelFormat.format(GetStringFromAddress(address, True), (level * 100.00 / 16))
    
    def Configure(self, address = None, level = 8):
        panel = eg.ConfigPanel()
        maskedCtrl = self.AddAddressControl(panel, address)
        levelCtrl = self.AddLevelControl(panel, level)
        
        while panel.Affirmed():
            address = GetAddressFromString(maskedCtrl.GetPlainValue())
            ActionBase.defaultAddress = address
            panel.SetResult(address, levelCtrl.GetValue())

class DimTimer(ActionBase):
    name = "Dim in timer value"
    description = "Sets the dim level in timer value"
    labelFormat = "Set dim-level to {1:.02f} % for {0} in {2}"
    
    def __call__(self, address, level, timeCode):
        self.plugin.SendRawCommand("\x01\x06\xf1" + GetAddressBytes(address) + chr(level + 32) + chr(timeCode))
    
    def GetLabel(self, address, level, timeCode):
        return self.labelFormat.format(GetStringFromAddress(address, True), (level * 100.00 / 16), FormatTimeValue(GetTimeValue(timeCode)))
    
    def Configure(self, address = None, level = 8, timeCode = 0):
        panel = eg.ConfigPanel()
        maskedCtrl = self.AddAddressControl(panel, address)
        levelCtrl = self.AddLevelControl(panel, level)
        timerCtrl = self.AddTimerControl(panel, timeCode)
        
        while panel.Affirmed():
            address = GetAddressFromString(maskedCtrl.GetPlainValue())
            ActionBase.defaultAddress = address
            panel.SetResult(
                address, 
                levelCtrl.GetValue(),
                GetTimeCodeByIndex(timerCtrl.GetValue()))
