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
    version = "0.2.1486",
    kind = "external",
    canMultiLoad = False,
    createMacrosOnAdd = False,
    description = __doc__,
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=2147",
    guid = '{D76A6D18-142A-4f75-8F93-9CDA86DBC310}'
)

import binascii
import math
import sys
import win32event
import wx.lib.mixins.listctrl as listmix
from wx.lib.masked import TextCtrl
import wx.lib.masked as masked
from eg.WinApi.HID import HIDThread
from eg.WinApi.HID import GetDevicePath
from eg.WinApi.HID import IsDeviceName

VENDOR_ID = 6383
PRODUCT_ID = 57365
TIME_OUT = 250

class Text:
    errorFind = "Error finding ELV FS20 PCS"

    timedActionName = "Timed actions"
    timedActionDescription = "Allows controlling FS20 devices with timed parameter."
    address = "Address:"
    timerValue = "Timer value:"
    repeat = "Repeat:"
    level = "Level:"
    repeatSuffix = "{0} ({1} times)"

class FS20PCS(eg.PluginClass):
    text = Text

    def AddNewAction(self, root, internalName, baseClass, classFuncCode, externalName, classDescription, classLabelFormat):
        class MyText:
            labelFormat = classLabelFormat
        class tmpAction(baseClass):
            text = MyText
            name = externalName
            description = classDescription
            funcCode = classFuncCode
        tmpAction.__name__ = internalName
        root.AddAction(tmpAction)

    def __init__(self):
        self.version = None
        self.thread = None

        self.AddNewAction(self, "Off", SimpleAction, 0x00, "Off", "Turns device off (dim to 0%)", "Turn off {0}")
        self.AddNewAction(self, "On", SimpleAction, 0x10, "On", "Turns device on (dim to 100%)", "Turn on {0}")
        self.AddNewAction(self, "PreviousValue", SimpleAction, 0x11, "On with previous value", "Turns device on with previous value", "Turn on {0} with previous value")
        self.AddNewAction(self, "Toggle", SimpleAction, 0x12, "Toggle", "Toggles between off and previous value", "Toggle {0} between off and previous value")
        self.AddNewAction(self, "DimDown", RepeatAction, 0x14, "Dim down", "Dims down", "Dim down {0}")
        self.AddNewAction(self, "DimUp", RepeatAction, 0x13, "Dim up", "Dims up", "Dim up {0}")
        self.AddAction(Dim)
        self.AddNewAction(self, "DimAlternating", RepeatAction, 0x15, "Alternating dim", "Dims up one level until maximum, then dim down", "Alternating dim {0}")

        group = self.AddGroup(self.text.timedActionName, self.text.timedActionDescription)
        self.AddNewAction(group, "OffTimer", TimerValueAction, 0x20, "Off in timer value", "Turns device off (dim to 0%) in timer value", "Turn off {0} in {1}")
        self.AddNewAction(group, "OnTimer", TimerValueAction, 0x30, "On in timer value", "Turns device on (dim to 100%) in timer value", "Turn on {0} in {1}")
        self.AddNewAction(group, "PreviousValueTimer", TimerValueAction, 0x31, "On with previous value in timer value", "Turns device on with previous value in timer value", "Turn on {0} with previous value in {1}")
        self.AddNewAction(group, "ToggleTimer", TimerValueAction, 0x32, "Toggle in timer value", "Toggles between off and previous value in timer value", "Toggle {0} between off and previous value in {1}")
        group.AddAction(DimTimer)
        self.AddNewAction(group, "OffPreviousValueInternal", SimpleAction, 0x18, "Off for internal timer value, previous value afterwards", "Turns off (dim to 0%) device for internal timer value and return to previous value afterwards", "Turn off {0} for internal timer value and return to previous value afterwards")
        self.AddNewAction(group, "OffPreviousValueTimer", TimerValueAction, 0x38, "Off for timer value, previous value afterwards", "Turns off (dim to 0%) device for timer value and return to previous value afterwards", "Turn off {0} for {1} and return to previous value afterwards")
        self.AddNewAction(group, "OnOffInternal", SimpleAction, 0x19, "On (dim to 100%) for internal timer value, off afterwards", "Turns on (device dim to 100%) for internal timer value and turns it off afterwards", "Turn on {0} for internal timer value and turn off afterwards")
        self.AddNewAction(group, "OnOffTimer", TimerValueAction, 0x39, "On (dim to 100%) for timer value, off afterwards", "Turns on (device dim to 100%) for timer value and turns it off afterwards", "Turn on {0} for {1} and turn off afterwards")
        self.AddNewAction(group, "PreviousValueOffInternal", SimpleAction, 0x1a, "Previous value for internal timer value, off afterwards", "Turns on device with previous value for internal timer value and turns it off afterwards", "Turn on {0} with previous value for internal timer value and turn off afterwards")
        self.AddNewAction(group, "PreviousValueOffTimer", TimerValueAction, 0x3a, "Previous value for timer value, off afterwards", "Turns on device with previous value for timer value and turns it off afterwards", "Turn on {0} with previous value for {1} and turn off afterwards")
        self.AddNewAction(group, "OnPreviousStateInternal", SimpleAction, 0x1e, "On for internal timer value, previous state afterwards", "Turns on (dim to 100%) device for internal timer value and return to previous state afterwards", "Turn on {0} for internal timer value and return to previous state afterwards")
        self.AddNewAction(group, "OnPreviousStateTimer", TimerValueAction, 0x3e, "On for timer value, previous state afterwards", "Turns on (dim to 100%) device for timer value and return to previous state afterwards", "Turn on {0} for {1} and return to previous state afterwards")
        self.AddNewAction(group, "PreviousValuePreviousStateInternal", SimpleAction, 0x1f, "Previous value for internal timer value, previous state afterwards", "Turns on device with previous value for internal timer value and return to previous state afterwards", "Turn on {0} with previous value for internal timer value and return to previous state afterwards")
        self.AddNewAction(group, "PreviousValuePreviousStateTimer", TimerValueAction, 0x3f, "Previous value for timer value, previous state afterwards", "Turns on device with previous value for timer value and return to previous state afterwards", "Turn on {0} with previous value for {1} and return to previous state afterwards")
        self.AddNewAction(group, "DimUpOffTimer", RepeatTimerValueAction, 0x33, "Dim up and turn off after timer value", "Dims up and turns off after timer value", "Dim up {0} and turn off after {1}")
        self.AddNewAction(group, "DimDownOffTimer", RepeatTimerValueAction, 0x34, "Dim down and turn off after timer value", "Dims down and turns off after timer value", "Dim down {0} and turn off after {1}")
        self.AddNewAction(group, "DimAlternatingOffTimer", RepeatTimerValueAction, 0x35, "Alternating dim and turn off after timer value", "Dims up one level until maximum, then dim down and turns off after timer value", "Alternating dim {0} and turn off after {1}")

        group = self.AddGroup("Programming", "Allows programming of FS20 devices. You should prefer timed actions and only use these for initial setup.")
        self.AddNewAction(group, "ProgramTimer", SimpleAction, 0x16, "Start/stop programming of internal timer", "Starts respectively stop programming of the internal timer", "Start/stop programming of internal timer for {0}")
        self.AddNewAction(group, "ProgramCode", SimpleAction, 0x17, "Program address", "Learn address. This is a dummy action which does nothing, but can be used for address learning procedure on some devices.", "Learn address {0}")
        self.AddNewAction(group, "ProgramFactoryDefaults", SimpleAction, 0x1b, "Reset device to factory defaults", "Reset device to factory defaults", "Reset {0} to factory defaults")
        self.AddNewAction(group, "ProgramInternalTimer", TimerValueAction, 0x36, "Program internal timer value", "Program internal timer value", "Program internal timer value for {0} to {1}")
        self.AddNewAction(group, "ProgramDimUpRampTimer", TimerValueAction, 0x3c, "Program dim up ramp timer value", "Program dim up ramp timer value", "Program dim up ramp timer value for {0} to {1}")
        self.AddNewAction(group, "ProgramDimDownRampTimer", TimerValueAction, 0x3d, "Program dim down ramp timer value", "Program dim down ramp timer value", "Program dim down ramp timer value for {0} to {1}")

    def RawCallback(self, data):
        if eg.debugLevel:
            print "FS20PCS RawCallBack", binascii.hexlify(data)

        if len(data) != 5 or data[0:3] != "\x02\x03\xA0":
            self.PrintError("data must have a length of 5 and start with 02 03 A0")
        errorId = ord(data[3:4])
        if errorId == 0:
            pass
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
        #create the following Python command to show version number
        #eg.plugins.FS20PCS.plugin.PrintVersion()
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

    def SendRawCommand(self, data, timeout = 0):
        if not self.thread:
            self.PrintError("Plug in is not running.")
            return
        dataLength = len(data)
        if eg.debugLevel:
            print "FS20PCS SendRawCommand", binascii.hexlify(data)
        newData = data + ((11 - dataLength) * '\x00')
        self.thread.Write(newData, timeout + 1000)#extra second to wait for response

    def Abort(self):
        self.SendRawCommand("\x01\x01\xf3")

    def RequestVersion(self):
        data = '\x01\x01\xf0'
        self.SendRawCommand(data)

    def SetupHidThread(self, newDevicePath):
        #create thread
        thread = HIDThread(self.name, newDevicePath, self.name)
        thread.SetStopCallback(self.StopCallback)
        thread.SetRawCallback(self.RawCallback)
        thread.start()
        thread.WaitForInit()
        self.thread = thread
        self.RequestVersion()

    def ReconnectDevice(self, event):
        """method to reconnect a disconnected device"""
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
    defaultAddress = 0 #GetAddressFromString("123412342222")

    funcCode = None
    name = None
    description = None

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
        panel.AddLine(self.plugin.text.address, maskedCtrl)
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
        panel.AddLine(self.plugin.text.timerValue, timerCtrl)
        return timerCtrl

    def AddRepeatControl(self, panel, repeatCount):
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
        panel.AddLine(self.plugin.text.repeat, repeatCtrl)
        return repeatCtrl

    def AddLevelControl(self, panel, level):
        def LevelCallback(value):
            return "%.02f%%" % (value * 100.00 / 16)

        levelCtrl = eg.Slider(
            panel,
            value=level,
            min=0,
            max=16,
            minLabel="0.00%",
            maxLabel="100.00%",
            style = wx.SL_AUTOTICKS|wx.SL_TOP,
            size=(300,-1),
            levelCallback=LevelCallback
        )
        levelCtrl.SetMinSize((300, -1))
        panel.AddLine(self.plugin.text.level, levelCtrl)
        return levelCtrl

class SimpleAction(ActionBase):
    """Base class for all action that only take an address as input
    """

    def __call__(self, address):
        self.plugin.SendRawCommand("\x01\x06\xf1" + GetAddressBytes(address) + chr(self.funcCode))

    def GetLabel(self, address):
        return self.text.labelFormat.format(GetStringFromAddress(address, True))

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
        label = self.text.labelFormat.format(GetStringFromAddress(address, True))
        if repeatCount > 1:
            label = self.plugin.text.repeatSuffix.format(label, repeatCount)
        return label

    def Configure(self, address = None, repeatCount = 1):
        panel = eg.ConfigPanel()

        maskedCtrl = self.AddAddressControl(panel, address)
        repeatCtrl = self.AddRepeatControl(panel, repeatCount)

        while panel.Affirmed():
            address = GetAddressFromString(maskedCtrl.GetPlainValue())
            ActionBase.defaultAddress = address
            panel.SetResult(address, repeatCtrl.GetValue())

class RepeatTimerValueAction(ActionBase):
    """Base class for all action that take an address, timer value and repeat Count
    """

    def __call__(self, address, timeCode, repeatCount):
        self.plugin.SendRawCommand("\x01\x07\xf2" + GetAddressBytes(address) +  chr(self.funcCode) + chr(timeCode) + chr(repeatCount), repeatCount * TIME_OUT)

    def GetLabel(self, address, timeCode, repeatCount):
        label = self.text.labelFormat.format(GetStringFromAddress(address, True), FormatTimeValue(GetTimeValue(timeCode)))
        if repeatCount > 1:
            label = self.plugin.text.repeatSuffix.format(label, repeatCount)
        return label

    def Configure(self, address = None, timeCode = 0, repeatCount = 1):
        panel = eg.ConfigPanel()

        maskedCtrl = self.AddAddressControl(panel, address)
        timerCtrl = self.AddTimerControl(panel, timeCode)
        repeatCtrl = self.AddRepeatControl(panel, repeatCount)

        while panel.Affirmed():
            address = GetAddressFromString(maskedCtrl.GetPlainValue())
            ActionBase.defaultAddress = address
            panel.SetResult(address, GetTimeCodeByIndex(timerCtrl.GetValue()), repeatCtrl.GetValue())



class TimerValueAction(ActionBase):
    """Base class for all action that take an address and timer value
    """

    def __call__(self, address, timeCode):
        self.plugin.SendRawCommand("\x01\x06\xf1" + GetAddressBytes(address) +  chr(self.funcCode) + chr(timeCode))

    def GetLabel(self, address, timeCode):
        return self.text.labelFormat.format(GetStringFromAddress(address, True), FormatTimeValue(GetTimeValue(timeCode)))

    def Configure(self, address = None, timeCode = 0):
        panel = eg.ConfigPanel()

        maskedCtrl = self.AddAddressControl(panel, address)
        timerCtrl = self.AddTimerControl(panel, timeCode)

        while panel.Affirmed():
            address = GetAddressFromString(maskedCtrl.GetPlainValue())
            ActionBase.defaultAddress = address
            panel.SetResult(address, GetTimeCodeByIndex(timerCtrl.GetValue()))

class Dim(ActionBase):
    class Text:
        labelFormat = "Set dim-level to {1:.02f}% for {0}"

    name = "Dim"
    description = "Sets dim level immediately"
    text = Text

    def __call__(self, address, level):
        self.plugin.SendRawCommand("\x01\x06\xf1" + GetAddressBytes(address) + chr(level))

    def GetLabel(self, address, level):
        return self.text.labelFormat.format(GetStringFromAddress(address, True), (level * 100.00 / 16))

    def Configure(self, address = None, level = 8):
        panel = eg.ConfigPanel()
        maskedCtrl = self.AddAddressControl(panel, address)
        levelCtrl = self.AddLevelControl(panel, level)

        while panel.Affirmed():
            address = GetAddressFromString(maskedCtrl.GetPlainValue())
            ActionBase.defaultAddress = address
            panel.SetResult(address, levelCtrl.GetValue())

class DimTimer(ActionBase):
    class Text:
        labelFormat = "Set dim-level to {1:.02f}% for {0} in {2}"

    name = "Dim in timer value"
    description = "Sets the dim level in timer value"
    text = Text

    def __call__(self, address, level, timeCode):
        self.plugin.SendRawCommand("\x01\x06\xf1" + GetAddressBytes(address) + chr(level + 32) + chr(timeCode))

    def GetLabel(self, address, level, timeCode):
        return self.text.labelFormat.format(GetStringFromAddress(address, True), (level * 100.00 / 16), FormatTimeValue(GetTimeValue(timeCode)))

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
