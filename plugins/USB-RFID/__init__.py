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
    version = "0.1." + "$LastChangedRevision: 614 $".split()[1],
    kind = "other",
    canMultiLoad = False,
    description = __doc__,
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=1945",
    guid = '{017848B7-CC6D-45A8-989A-752A5CB1A8C9}'
)

import binascii
import sys
import wx.lib.mixins.listctrl as listmix
from eg.WinApi.HID import HIDThread
from eg.WinApi.HID import GetDevicePath
from eg.WinApi.HID import IsDeviceName

class Text:
    errorFind = "Error finding USB/RFID-Interface"

VENDOR_ID = 6383
PRODUCT_ID = 57368

class USBRFID(eg.PluginClass):
    def __init__(self):
        self.version = None
        self.thread = None
        
    def RawCallback(self, data):
		print binascii.hexlify(data)
    
    def PrintVersion(self):
        #create the following python command to show version number
        #eg.plugins.USBRFID.plugin.PrintVersion()
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
