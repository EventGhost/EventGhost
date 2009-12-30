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

import array
import binascii
import sys
import wx.lib.mixins.listctrl as listmix
from wx.lib.masked import TextCtrl
from eg.WinApi.HID import HIDThread
from eg.WinApi.HID import GetDevicePath
from eg.WinApi.HID import IsDeviceName

class Text:
    errorFind = "Error finding ELV FS20 PCS"
    help0 = "You can assign a name to a combination of house code and device addresses."
    help1 = "Use '?' as a wild card to define groups."
    houseCode = "House code"
    deviceAddress = "Device address"
    groupName = "Group name"
    add = "Add"
    update = "Update"
    delete = "Delete"

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
        self.PendingEvents = {}
        self.mappings = None
        
    def RawCallback(self, data):
        if len(data) != 5 or data[0:3] != "\x02\x03\xA0":
            eg.PrintError("data must have a length of 5 and start with 02 03 A0")
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
            eg.PrintError("Unknown command id")
        elif errorId == 4:
            eg.PrintError("invalid command length")
        elif errorId == 5:
            eg.PrintError("nothing to abort")
        else:
            eg.PrintError("Unknown Error")
            
    def PrintVersion(self):
        #create the following python command to show version number
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
    
    def SendCommand(self, commandId, houseCode, address, extension):
        pass
    
    def SendRawCommand(self, data, timeout):
        if not self.thread:
            eg.PrintError("Plug in is not running.")
            return
        dataLength = len(data)
        print "Writing", dataLength, binascii.hexlify(data)
        newData = data + ((11 - dataLength) * '\x00')
        self.thread.Write(newData, timeout)
    
    def RequestVersion(self):
        data = '\x01\x01\xF0'
        self.SendRawCommand(data, 1000)
    
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

    def __start__(self, mappings = None):
        self.mappings = mappings
        
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

   
