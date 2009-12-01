"""<rst>
Allows to receive events from FS20 remote controls.

|

**Notice:**
You can use the configuration dialog to build groups or assign a name to a device.
Allowed characters are 1, 2, 3, 4 and ? which acts as a wild card.
Setting up groups is optional as events with the house code and device address are always generated.  

|fS20Image|_

`Direct shop link <http://www.elv.de/output/controller.aspx?cid=74&detail=10&detail2=27407>`__

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
    #description = (
    #    'Allows to receive events from FS20 remote controls.<br/>'
    #    '<a href="http://www.elv.de/"><img src=\"picture.jpg\"/></a>'
    #),
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=1945",
)

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

class FS20PCS(eg.PluginClass):
    def __init__(self):
        self.version = None
        self.thread = None
        self.PendingEvents = {}
        self.mappings = None
        
    def OnComputerSuspend(self, suspendType):
        if self.thread:
            self.thread.AbortThread()
        print "OnComputerSuspend"
    
    def OnComputerResume(self, suspendType):
        newDevicePath = self.GetMyDevicePath()
        if not newDevicePath:
            #device not found
            self.PrintError(Text.errorFind)
        else:
            self.SetupHidThread(newDevicePath)
        print "OnComputerResume"
        
    def RawCallback(self, data):
        print binascii.hexlify(data)
            
    def PrintVersion(self):
        #create the following python command to show version number
        #eg.plugins.FS20PCS.plugin.PrintVersion()
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

   
