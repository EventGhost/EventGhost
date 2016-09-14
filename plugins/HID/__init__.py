eg.RegisterPlugin(
    name = "Generic HID",
    author = "Bartman",
    version = "1.5.1246",
    kind = "remote",
    guid = "{05A690D9-27C2-4AC5-B0DD-2F562619E922}",
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
from eg.WinApi.HID import HIDThread, GetDevicePath, GetDeviceDescriptions, DeviceDescription, IsDeviceName

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
    useDeviceIndex = "Use the device with index"
    errorFind = "Error finding HID device: "
    vendorID = "Vendor ID "

class HID(eg.PluginClass):
    def __init__(self):
        self.thread = None

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

    def GetMyDevicePath(self):
        path = GetDevicePath(
            self.devicePath,
            self.vendorID,
            self.productID,
            self.versionNumber,
            self.useDeviceIndex,
            self.deviceIndex,
            self.noOtherPort)
        return path;

    def SetupHidThread(self, newDevicePath):
        #create thread
        self.thread = HIDThread(self.vendorString + " " + self.productString, newDevicePath)
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
            if not IsDeviceName(event.payload, self.vendorID, self.productID):
                return

            #check if the right device was connected
            #getting devicePath
            newDevicePath = self.GetMyDevicePath()
            if not newDevicePath:
                #wrong device
                return

            self.SetupHidThread(newDevicePath)

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
        useDeviceIndex = False,
        deviceIndex = 0
    ):
        prefix = "HID: "
        #one or both strings empty should not happen
        if not vendorString or not productString:
            return "HID"

        #productString already contains manufacturer or vendor id only
        if productString.find(vendorString) != -1 or\
            vendorString[0:len(Text.vendorID)] == Text.vendorID:
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
        useDeviceIndex = False,
        deviceIndex = 0
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
        self.useDeviceIndex = useDeviceIndex
        self.deviceIndex = deviceIndex
        self.oldValues = {}

        if eventName:
            self.info.eventPrefix = eventName
        else:
            self.info.eventPrefix = "HID"

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
        useDeviceIndex = False,
        deviceIndex = 0
    ):
        deviceList = GetDeviceDescriptions()
        panel = eg.ConfigPanel(self, resizable=True)

        #building dialog
        hidList = wx.ListCtrl(panel, -1, pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)

        #create GUI
        hidList.InsertColumn(0, Text.deviceName)
        hidList.InsertColumn(1, Text.manufacturer)
        hidList.InsertColumn(2, Text.connected)

        path = GetDevicePath(
            devicePath,
            vendorID,
            productID,
            versionNumber,
            noOtherPort,
            useDeviceIndex,
            deviceIndex,
            deviceList)

        #fill list
        devices = {}
        idx = 0
        for item in deviceList:
            idx = hidList.InsertStringItem(sys.maxint, item.productString)
            hidList.SetStringItem(idx, 1, item.vendorString)
            hidList.SetStringItem(idx, 2, Text.yes)
            if item.devicePath == path:
                hidList.Select(idx)
            devices[idx] = item

        #add not connected device to bottom of list
        if not path and devicePath:
            item = DeviceDescription(
                devicePath,
                vendorID,
                vendorString,
                productID,
                productString,
                versionNumber)
            idx = hidList.InsertStringItem(sys.maxint, item.productString)
            hidList.SetStringItem(idx, 1, item.vendorString)
            hidList.SetStringItem(idx, 2, Text.no)
            hidList.Select(idx)
            devices[idx] = item

        #no device selected, disable ok and apply button
        panel.EnableButtons(hidList.GetFirstSelected() != -1)

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
            wx.StaticText(panel, -1, Text.eventName),
            (0, 0),
            flag = wx.ALIGN_CENTER_VERTICAL)
        eventNameCtrl = wx.TextCtrl(panel, value = eventName)
        eventNameCtrl.SetMaxLength(32)
        optionsSizer.Add(eventNameCtrl, (0, 1), (1, 2), flag = wx.EXPAND)

        #checkbox for enduring event option
        enduringEventsCtrl = wx.CheckBox(panel, -1, Text.enduringEvents)
        enduringEventsCtrl.SetValue(enduringEvents)
        optionsSizer.Add(enduringEventsCtrl, (1, 0), (1, 3))

        #checkbox for raw data events
        rawDataEventsCtrl = wx.CheckBox(panel, -1, Text.rawDataEvents)
        rawDataEventsCtrl.SetValue(rawDataEvents)
        optionsSizer.Add(rawDataEventsCtrl, (2, 0), (1, 3))

        #text
        optionsSizer.Add(
            wx.StaticText(panel, -1, Text.multipleDeviceOptions),
            (3, 0), (1, 3),
            flag = wx.ALIGN_CENTER_VERTICAL)

        #checkbox for use first device
        useDeviceIndexCtrl = wx.CheckBox(panel, -1, Text.useDeviceIndex)
        useDeviceIndexCtrl.SetValue(useDeviceIndex)
        optionsSizer.Add(useDeviceIndexCtrl, (4, 0), (1, 2), flag = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        #device index spin control
        deviceIndexCtrl = eg.SpinIntCtrl(panel, -1, deviceIndex, 0, 99, size=(100,-1))
        optionsSizer.Add(deviceIndexCtrl, (4, 2), (1, 1))

        #checkbox for no other port option
        noOtherPortCtrl = wx.CheckBox(panel, -1, Text.noOtherPort)
        noOtherPortCtrl.SetValue(noOtherPort)
        optionsSizer.Add(noOtherPortCtrl, (5, 0), (1, 3))

        panel.sizer.Add(optionsSizer, 0, wx.TOP, 10)

        def OnHidListSelect(event):
            panel.EnableButtons(hidList.GetFirstSelected() != -1)
            event.Skip()

        def OnRawDataEventsChange(event):
            enduringEventsCtrl.Enable(not rawDataEventsCtrl.GetValue())
            event.Skip()

        def OnEnduringEventsChange(event):
            rawDataEventsCtrl.Enable(not enduringEventsCtrl.GetValue())
            event.Skip()

        def OnUseDeviceIndexCtrlChange(event):
            noOtherPortCtrl.Enable(not useDeviceIndexCtrl.GetValue())
            deviceIndexCtrl.Enable(useDeviceIndexCtrl.GetValue())
            event.Skip()

        def OnNoOtherPortChange(event):
            useDeviceIndexCtrl.Enable(not noOtherPortCtrl.GetValue())
            deviceIndexCtrl.Enable(not noOtherPortCtrl.GetValue())
            event.Skip()

        OnRawDataEventsChange(wx.CommandEvent())
        OnEnduringEventsChange(wx.CommandEvent())
        OnUseDeviceIndexCtrlChange(wx.CommandEvent())
        OnNoOtherPortChange(wx.CommandEvent())
        rawDataEventsCtrl.Bind(wx.EVT_CHECKBOX, OnRawDataEventsChange)
        enduringEventsCtrl.Bind(wx.EVT_CHECKBOX, OnEnduringEventsChange)
        useDeviceIndexCtrl.Bind(wx.EVT_CHECKBOX, OnUseDeviceIndexCtrlChange)
        noOtherPortCtrl.Bind(wx.EVT_CHECKBOX, OnNoOtherPortChange)
        hidList.Bind(wx.EVT_LIST_ITEM_SELECTED, OnHidListSelect)
        hidList.Bind(wx.EVT_LIST_ITEM_DESELECTED, OnHidListSelect)

        while panel.Affirmed():
            device = devices[hidList.GetFirstSelected()]
            panel.SetResult(
                eventNameCtrl.GetValue(),
                enduringEventsCtrl.GetValue(),
                rawDataEventsCtrl.GetValue(),
                noOtherPortCtrl.GetValue(),
                device.devicePath,
                device.vendorId,
                device.vendorString,
                device.productId,
                device.productString,
                device.versionNumber,
                useDeviceIndexCtrl.GetValue(),
                deviceIndexCtrl.GetValue(),
            )

