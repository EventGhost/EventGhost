eg.RegisterPlugin(
    name = "Generic HID",
    author = "Bartman",
    version = "1.0." + "$LastChangedRevision$".split()[1],
    kind = "remote",
    canMultiLoad = True,
    description = (
        'Communication with devices that follow the '
        'Human Interface Device (HID) standard.'
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=571",
)

import time
import binascii
import sys
import wx.lib.mixins.listctrl as listmix
from eg.WinApi.HID import HIDHelper
from eg.WinApi.HID import HIDThread

class Text:
    manufacturer = "Manufacturer"
    deviceName = "Device Name"
    connected = "Connected"
    eventName = "Event prefix (optional):"
    yes = "Yes"
    no = "No"
    enduringEvents = "Trigger enduring events for buttons"
    rawDataEvents = "Use raw Data as event name"
    multipleDeviceOptions = "Options for multiple same devices"
    noOtherPort = "Use selected device only if connected to current port"
    useFirstDevice = "Use first device found"
    errorFind = "Error finding HID device: "
    errorOpen = "Error opening HID device: "
    errorRead = "Error reading HID device: "
    errorRetrieval = "Error getting HID device info."
    errorReportLength = "Report length must not be zero for device "
    errorMultipleDevices = "Multiple devices found. Don't know which to use."
    errorInvalidDataIndex = "Found data index not defined as button or control value."
    vendorID = "Vendor ID "

class HID(eg.PluginClass):
    helper = None
    text = Text
    thread = None

    def RawCallback(self, data):
        self.TriggerEvent(binascii.hexlify(data).upper())
   
    def ButtonCallback(self, data):
        if len(data):
            #one or more buttons pressed
            btnPressed = []
            for num in data:
                btnPressed.append(str(num))
            evtName = "Button." + "+".join(btnPressed)
            if self.enduringEvents:
                self.TriggerEnduringEvent(evtName)
            else:
                self.TriggerEvent(evtName)
        elif self.enduringEvents:
            #no buttons pressed anymore
            self.EndLastEvent()
        else:
            #trigger event so that releasing all buttons
            #can get noticed even w/o enduring events
            self.TriggerEvent("Button.None")
    
    def ValueCallback(self, data):
        for key, value in data.items():
            if key in self.oldValues and value == self.oldValues[key]:
                continue
            self.oldValues[key] = value
            self.TriggerEvent("Value." + str(key), payload = value)
        
    def StopCallback(self):
        self.TriggerEvent("Stopped")
        self.thread = None
    
    def SetupHidThread(self):
        #create thread
        self.thread = HIDThread(
            self.helper,
            self.noOtherPort,
            self.devicePath,
            self.vendorID,
            self.vendorString,
            self.productID,
            self.productString,
            self.versionNumber,
            self.useFirstDevice
        )
        self.thread.start()
        self.thread.SetStopCallback(self.StopCallback)
        if self.rawDataEvents:
            self.thread.SetRawCallback(self.RawCallback)
        else:
            self.thread.SetButtonCallback(self.ButtonCallback)
            self.thread.SetValueCallback(self.ValueCallback)
    
    def ReconnectDevice(self, event):
        """method to reconnect a disconnect device"""
        if self.thread == None:
            #updating device list
            self.helper.UpdateDeviceList()
            
            #check if the right device was connected
            #getting devicePath
            self.devicePath = self.helper.GetDevicePath(
                self.noOtherPort,
                self.devicePath,
                self.vendorID,
                self.productID,
                self.versionNumber,
                self.useFirstDevice
            )
            if not self.devicePath:
                #wrong device
                return
            
            self.SetupHidThread()

    def GetLabel(self,
        eventName,
        enduringEvents,
        rawDataEvents,
        noOtherPort,
        devicePath,
        vendorID,
        vendorString,
        productID,
        productString,
        versionNumber,
        useFirstDevice = False
    ):
        prefix = "HID: "
        #one or both strings empty should not happen
        if not vendorString or not productString:
            return "HID"

        #productString already contains manufacturer or vendor id only
        if productString.find(vendorString) != -1 or\
            vendorString[0:len(self.text.vendorID)] == self.text.vendorID:
            return prefix + productString

        return prefix + vendorString + " " + productString


    def __start__(self,
        eventName,
        enduringEvents,
        rawDataEvents,
        noOtherPort,
        devicePath,
        vendorID,
        vendorString,
        productID,
        productString,
        versionNumber,
        useFirstDevice = False
    ):

        #saving parameters so they can be used to reconnect a device
        self.eventName = eventName
        self.enduringEvents = enduringEvents
        self.rawDataEvents = rawDataEvents
        self.noOtherPort = noOtherPort
        self.devicePath = devicePath
        self.vendorID = vendorID
        self.vendorString = vendorString
        self.productID = productID
        self.productString = productString
        self.versionNumber = versionNumber
        self.useFirstDevice = useFirstDevice
        self.oldValues = {}

        if eventName:
            self.info.eventPrefix = eventName
        else:
            self.info.eventPrefix = "HID"
        #ensure helper object is up to date
        if not self.helper:
            self.helper = HIDHelper()
        else:
            self.helper.UpdateDeviceList()

        self.SetupHidThread()
        
        #Bind plug in to RegisterDeviceNotification message 
        eg.Bind("System.DeviceAttached", self.ReconnectDevice)

    def __stop__(self):
        self.thread.AbortThread()
        
        #unbind from RegisterDeviceNotification message
        eg.Unbind("System.DeviceAttached", self.ReconnectDevice)

    def Configure(self,
        eventName = "",
        enduringEvents = True,
        rawDataEvents = False,
        noOtherPort = False,
        devicePath = None,
        vendorID = None,
        vendorString = None,
        productID = None,
        productString = None,
        versionNumber = None,
        useFirstDevice = False
    ):
        #ensure helper object is up to date
        if not self.helper:
            self.helper = HIDHelper()
        else:
            self.helper.UpdateDeviceList()

        panel = eg.ConfigPanel(self, resizable=True)

        #building dialog
        hidList = wx.ListCtrl(panel, -1, pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)

        #create GUI
        hidList.InsertColumn(0, self.text.deviceName)
        hidList.InsertColumn(1, self.text.manufacturer)
        hidList.InsertColumn(2, self.text.connected)


        path = self.helper.GetDevicePath(noOtherPort,
            devicePath, vendorID, productID, versionNumber, useFirstDevice)

        #fill list
        devices = {}
        idx = 0
        for item in self.helper.deviceList:
            idx = hidList.InsertStringItem(sys.maxint, item[eg.WinApi.HID.PRODUCT_STRING])
            hidList.SetStringItem(idx, 1, item[eg.WinApi.HID.VENDOR_STRING])
            hidList.SetStringItem(idx, 2, self.text.yes)
            if item[eg.WinApi.HID.DEVICE_PATH] == path:
                hidList.Select(idx)
            devices[idx] = item

        #add not connected device to bottom of list
        if not path:
            if devicePath:
                item = {
                    eg.WinApi.HID.DEVICE_PATH: devicePath,
                    eg.WinApi.HID.VENDOR_ID: vendorID,
                    eg.WinApi.HID.VENDOR_STRING: vendorString,
                    eg.WinApi.HID.PRODUCT_ID: productID,
                    eg.WinApi.HID.PRODUCT_STRING: productString,
                    eg.WinApi.HID.VERSION_NUMBER: versionNumber,
                }
                idx = hidList.InsertStringItem(sys.maxint, item[eg.WinApi.HID.PRODUCT_STRING])
                hidList.SetStringItem(idx, 1, item[eg.WinApi.HID.VENDOR_STRING])
                hidList.SetStringItem(idx, 2, self.text.no)
                hidList.Select(idx)
                devices[idx] = item

        if hidList.GetFirstSelected() == -1:
            #no device selected, disable ok and apply button
            panel.dialog.buttonRow.okButton.Enable(False)
            panel.dialog.buttonRow.applyButton.Enable(False)

        #layout
        for i in range(hidList.GetColumnCount()):
            hidList.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            size = hidList.GetColumnWidth(i)
            hidList.SetColumnWidth(i, wx.LIST_AUTOSIZE)
            hidList.SetColumnWidth(i, max(size, hidList.GetColumnWidth(i) + 5))

        panel.sizer.Add(hidList, 1, flag = wx.EXPAND)

        #sizers
        optionsSizer = wx.GridBagSizer(0, 5)

        #eventname
        optionsSizer.Add(
            wx.StaticText(panel, -1, self.text.eventName),
            (0, 0),
            flag = wx.ALIGN_CENTER_VERTICAL)
        eventNameCtrl = wx.TextCtrl(panel, value = eventName)
        eventNameCtrl.SetMaxLength(32)
        optionsSizer.Add(eventNameCtrl, (0, 1), (1, 2), flag = wx.EXPAND)

        #checkbox for enduring event option
        enduringEventsCtrl = wx.CheckBox(panel, -1, self.text.enduringEvents)
        enduringEventsCtrl.SetValue(enduringEvents)
        optionsSizer.Add(enduringEventsCtrl, (1, 0), (1, 3))

        #checkbox for raw data events
        rawDataEventsCtrl = wx.CheckBox(panel, -1, self.text.rawDataEvents)
        rawDataEventsCtrl.SetValue(rawDataEvents)
        optionsSizer.Add(rawDataEventsCtrl, (2, 0), (1, 3))

        #text
        optionsSizer.Add(
            wx.StaticText(panel, -1, self.text.multipleDeviceOptions),
            (3, 0), (1, 3),
            flag = wx.ALIGN_CENTER_VERTICAL)
        
        #checkbox for use first device
        useFirstDeviceCtrl = wx.CheckBox(panel, -1, self.text.useFirstDevice)
        useFirstDeviceCtrl.SetValue(useFirstDevice)
        optionsSizer.Add(useFirstDeviceCtrl, (4, 0), (1, 3))

        #checkbox for no other port option
        noOtherPortCtrl = wx.CheckBox(panel, -1, self.text.noOtherPort)
        noOtherPortCtrl.SetValue(noOtherPort)
        optionsSizer.Add(noOtherPortCtrl, (5, 0), (1, 3))

        panel.sizer.Add(optionsSizer, 0, wx.TOP, 10)

        def OnHidListSelect(event):
            panel.dialog.buttonRow.okButton.Enable(True)
            panel.dialog.buttonRow.applyButton.Enable(True)
            event.Skip()

        def OnRawDataEventsChange(event):
            enduringEventsCtrl.Enable(not rawDataEventsCtrl.GetValue())
            event.Skip()

        def OnEnduringEventsChange(event):
            rawDataEventsCtrl.Enable(not enduringEventsCtrl.GetValue())
            event.Skip()

        def OnUseFirstDeviceCtrlChange(event):
            noOtherPortCtrl.Enable(not useFirstDeviceCtrl.GetValue())
            event.Skip()

        def OnNoOtherPortChange(event):
            useFirstDeviceCtrl.Enable(not noOtherPortCtrl.GetValue())
            event.Skip()

        OnRawDataEventsChange(wx.CommandEvent())
        OnEnduringEventsChange(wx.CommandEvent())
        OnUseFirstDeviceCtrlChange(wx.CommandEvent())
        OnNoOtherPortChange(wx.CommandEvent())
        rawDataEventsCtrl.Bind(wx.EVT_CHECKBOX, OnRawDataEventsChange)
        enduringEventsCtrl.Bind(wx.EVT_CHECKBOX, OnEnduringEventsChange)
        useFirstDeviceCtrl.Bind(wx.EVT_CHECKBOX, OnUseFirstDeviceCtrlChange)
        noOtherPortCtrl.Bind(wx.EVT_CHECKBOX, OnNoOtherPortChange)
        hidList.Bind(wx.EVT_LIST_ITEM_SELECTED, OnHidListSelect)

        while panel.Affirmed():
            device = devices[hidList.GetFirstSelected()]
            panel.SetResult(
                eventNameCtrl.GetValue(),
                enduringEventsCtrl.GetValue(),
                rawDataEventsCtrl.GetValue(),
                noOtherPortCtrl.GetValue(),
                device[eg.WinApi.HID.DEVICE_PATH],
                device[eg.WinApi.HID.VENDOR_ID],
                device[eg.WinApi.HID.VENDOR_STRING],
                device[eg.WinApi.HID.PRODUCT_ID],
                device[eg.WinApi.HID.PRODUCT_STRING],
                device[eg.WinApi.HID.VERSION_NUMBER],
                useFirstDeviceCtrl.GetValue()
            )

