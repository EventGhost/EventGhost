"""<rst>
Receives events from ELV USB/RFID-Interface.

|

|productImage|_

`Direct shop link <http://www.elv.de/output/controller.aspx?cid=74&detail=10&detail2=28049>`__

.. |productImage| image:: picture.jpg
.. _productImage: http://www.elv.de/
"""

eg.RegisterPlugin(
    name = "USB/RFID-Interface",
    author = "Bartman",
    version = "0.1.1455",
    kind = "other",
    canMultiLoad = False,
    description = __doc__,
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=1945",
    guid = '{017848B7-CC6D-45A8-989A-752A5CB1A8C9}'
)

import binascii
import sys
from eg.WinApi.HID import HIDThread
from eg.WinApi.HID import GetDevicePath
from eg.WinApi.HID import IsDeviceName

class Text:
    errorFind = "Error finding USB/RFID-Interface"
    duration = "Duration:"

VENDOR_ID = 6383
PRODUCT_ID = 57368

class USB_RFID(eg.PluginClass):
    text = Text

    def __init__(self):
        self.version = None
        self.thread = None

        self.AddNewAction("GreenLED", 0xf2, "Green LED", "Turn on green LED", "Turn on green LED for {0}0 ms")
        self.AddNewAction("RedLED", 0xf1, "Red LED", "Turn on red LED", "Turn on red LED for {0}0 ms")
        self.AddNewAction("Buzzer", 0xf3, "Buzzer", "Turn on buzzer", "Turn on buzzer for {0}0 ms")

    def AddNewAction(self, internalName, classFuncCode, externalName, classDescription, classLabelFormat):
        class MyText:
            labelFormat = classLabelFormat
        class tmpAction(ActionBase):
            text = MyText
            name = externalName
            description = classDescription
            funcCode = classFuncCode
        tmpAction.__name__ = internalName
        self.AddAction(tmpAction)

    def RawCallback(self, data):
        if eg.debugLevel:
            print "USB_RFID RawCallBack", binascii.hexlify(data)

        if len(data) != 9 or data[0:3] != "\x02\x07\xA0":
            self.PrintError("data must have a length of 9 and start with 02 07 A0")
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
            self.PrintError("invalid command length")
        elif errorId == 4 or errorId == 5:
            eventstring = binascii.hexlify(data[4:5]).upper() + "." + binascii.hexlify(data[5:]).upper()
            knownCode = False
            for eventHandler in eg.eventTable.get(self.info.eventPrefix + "." + eventstring, []):
                knownCode = True
                break
            self.TriggerEvent(eventstring)
            if not knownCode:
                self.TriggerEvent("Unknown")

        else:
            self.PrintError("Unknown Error")

    def PrintVersion(self):
        #create the following python command to show version number
        #eg.plugins.USB-RFID.plugin.PrintVersion()
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
        self.thread = HIDThread(self.name, newDevicePath, self.name)
        self.thread.SetStopCallback(self.StopCallback)
        self.thread.SetRawCallback(self.RawCallback)
        self.thread.start()
        self.thread.WaitForInit()
        self.RequestVersion()

    def RequestVersion(self):
        self.thread.Write('\x01\x01\xf0\x00\x00', 1000)

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

class ActionBase(eg.ActionBase):
    funcCode = None
    name = None
    description = None

    def __call__(self, duration):
        self.plugin.thread.Write("\x01\x02" + chr(self.funcCode) + chr(duration) + "\x00", 1000)

    def GetLabel(self, duration):
        #print str(duration) + "0 ms"
        #pass
        return self.text.labelFormat.format(duration)

    def Configure(self, duration = 100):
        panel = eg.ConfigPanel()

        def LevelCallback(value):
            return str(value) + "0 ms"

        durationCtrl = eg.Slider(
            panel,
            value=duration,
            min=1,
            max=255,
            minLabel="10 ms",
            maxLabel="2550 ms",
            style = wx.SL_TOP,
            size=(300,-1),
            levelCallback=LevelCallback
        )
        durationCtrl.SetMinSize((300, -1))

        panel.AddLine(self.plugin.text.duration, durationCtrl)

        while panel.Affirmed():
            panel.SetResult(durationCtrl.GetValue())


