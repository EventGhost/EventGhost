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
    name = "ELV FS20 PCE",
    author = "Bartman",
    version = "1.2",
    kind = "remote",
    canMultiLoad = False,
    description = __doc__,
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=1945",
    guid = '{5EF0F083-8281-4aec-8399-9675DB0D8C58}'
)

import binascii
import sys
import wx.lib.mixins.listctrl as listmix
from wx.lib.masked import TextCtrl
from eg.WinApi.HID import HIDThread
from eg.WinApi.HID import GetDevicePath
from eg.WinApi.HID import IsDeviceName

class Text:
    errorFind = "Error finding ELV FS20 PCE"
    help0 = "You can assign a name to a combination of house code and device addresses."
    help1 = "Use '?' as a wild card to define groups."
    houseCode = "House code"
    deviceAddress = "Device address"
    groupName = "Group name"
    add = "Add"
    update = "Update"
    delete = "Delete"

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

def CheckPattern(pattern, value):
    i = 0
    for char in pattern:
        if char != '?' and char != value[i]:
            return False
        i += 1
    return True

class FS20PCE(eg.PluginClass):
    def __init__(self):
        self.version = None
        self.thread = None
        self.PendingEvents = {}
        self.mappings = None

    def RawCallback(self, data):
        if not data or len(data) != 13 or ord(data[0]) != 2 or ord(data[1]) != 11:
            self.PrintError("invalid data")
            return

        self.version = ord(data[12])

        houseCode = binascii.hexlify(data[2:6])
        deviceCode = binascii.hexlify(data[6:8])
        command = ord(data[8])
        names = self.GetGroupNames(houseCode, deviceCode)

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
                    timerEntry = eg.scheduler.AddShortTask(eventTime, self.SchedulerCallback, deviceName, commandStr1)
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

    def GetGroupNames(self, houseCode, deviceCode):
        names = [houseCode + "." + deviceCode]
        if self.mappings:
            for houseCodePattern, deviceCodePattern, deviceName in self.mappings:
                if (deviceName in names):
                    continue
                if CheckPattern(deviceCodePattern, deviceCode) and CheckPattern(houseCodePattern, houseCode):
                    names.append(deviceName)
        return names

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
        self.thread = HIDThread(self.name, newDevicePath, self.name)
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

    def Configure(self,
        mappings = None,
    ):
        #gui callbacks and helper methods
        def ValidChars(input):
            for char in input:
                if char != '1' and char != '2' and char != '3' and char != '4' and char != '?':
                    return False
            return True

        def ContainsItem(houseCode, deviceAddress, groupName):
            for i in range(0, mappingsList.GetItemCount()):
                if houseCode != mappingsList.GetItem(i, 0).GetText():
                    continue
                if deviceAddress != mappingsList.GetItem(i, 1).GetText():
                    continue
                if groupName != mappingsList.GetItem(i, 2).GetText():
                    continue
                return True
            return False

        def OnItemSelected(event):
            idx = mappingsList.GetFirstSelected()
            houseCodeTextCtrl.SetValue(mappingsList.GetItem(idx, 0).GetText())
            deviceAddressTextCtrl.SetValue(mappingsList.GetItem(idx, 1).GetText())
            groupNameCtrl.SetValue(mappingsList.GetItem(idx, 2).GetText())

        def EnableButtons(event):
            idx = mappingsList.GetFirstSelected()
            houseCode = houseCodeTextCtrl.GetValue()
            deviceAddress = deviceAddressTextCtrl.GetValue()
            groupName = groupNameCtrl.GetValue()
            valid = houseCodeTextCtrl.IsValid() and deviceAddressTextCtrl.IsValid() and len(groupName)

            itemSelected = idx != -1
            addButton.Enable(valid and not ContainsItem(houseCode, deviceAddress, groupName))
            updateButton.Enable(valid and itemSelected and \
                (houseCode != mappingsList.GetItem(idx, 0).GetText() \
                 or deviceAddress != mappingsList.GetItem(idx, 1).GetText() \
                 or groupName != mappingsList.GetItem(idx, 2).GetText()) \
                and not ContainsItem(houseCode, deviceAddress, groupName))
            deleteButton.Enable(itemSelected)
            event.Skip()

        def OnAddButton(event):
            idx = mappingsList.InsertStringItem(sys.maxint, houseCodeTextCtrl.GetValue())
            mappingsList.SetStringItem(idx, 1, deviceAddressTextCtrl.GetValue())
            mappingsList.SetStringItem(idx, 2, groupNameCtrl.GetValue())
            mappingsList.Select(idx)
            EnableButtons(event)
            event.Skip()

        def OnUpdateButton(event):
            idx = mappingsList.GetFirstSelected()
            mappingsList.SetStringItem(idx, 0, houseCodeTextCtrl.GetValue())
            mappingsList.SetStringItem(idx, 1, deviceAddressTextCtrl.GetValue())
            mappingsList.SetStringItem(idx, 2, groupNameCtrl.GetValue())
            EnableButtons(event)
            event.Skip()

        def OnDeleteButton(event):
            idx = mappingsList.GetFirstSelected()
            mappingsList.DeleteItem(idx)
            EnableButtons(event)
            event.Skip()

        panel = eg.ConfigPanel(self, resizable=True)

        #building dialog
        mappingsList = wx.ListCtrl(panel, -1, pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)

        #create list
        mappingsList.InsertColumn(0, Text.houseCode)
        mappingsList.InsertColumn(1, Text.deviceAddress)
        mappingsList.InsertColumn(2, Text.groupName)

        #add items
        if mappings:
            for item in mappings:
                idx = mappingsList.InsertStringItem(sys.maxint, item[0])
                mappingsList.SetStringItem(idx, 1, item[1])
                mappingsList.SetStringItem(idx, 2, item[2])

        #layout
        for i in range(mappingsList.GetColumnCount()):
            mappingsList.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            size = mappingsList.GetColumnWidth(i)
            mappingsList.SetColumnWidth(i, wx.LIST_AUTOSIZE)
            mappingsList.SetColumnWidth(i, max(size, mappingsList.GetColumnWidth(i) + 5))

        houseCodeTextCtrl = TextCtrl(
            panel,
            mask = "XXXXXXXX",
            choiceRequired = True,
            validFunc = ValidChars,
            defaultValue = "????????",
            formatcodes = "F",
        )

        deviceAddressTextCtrl = TextCtrl(
            panel,
            mask = "XXXX",
            choiceRequired = True,
            validFunc = ValidChars,
            defaultValue = "????",
            formatcodes = "F",
        )

        groupNameCtrl = wx.TextCtrl(panel)

        editSizer = wx.GridSizer(3, 2)
        editSizer.Add(wx.StaticText(panel, -1, Text.houseCode + ":"), wx.ALIGN_CENTER_VERTICAL)
        editSizer.Add(houseCodeTextCtrl, 0)
        editSizer.Add(wx.StaticText(panel, -1, Text.deviceAddress + ":"), wx.ALIGN_CENTER_VERTICAL)
        editSizer.Add(deviceAddressTextCtrl, 0)
        editSizer.Add(wx.StaticText(panel, -1, Text.groupName + ":"), wx.ALIGN_CENTER_VERTICAL)
        editSizer.Add(groupNameCtrl, 0)


        addButton = wx.Button(panel, -1, Text.add)
        updateButton = wx.Button(panel, -1, Text.update)
        deleteButton = wx.Button(panel, -1, Text.delete)

        buttonsSizer = wx.GridSizer(1, 3)
        buttonsSizer.Add(addButton)
        buttonsSizer.Add(deleteButton)
        buttonsSizer.Add(updateButton)

        houseCodeTextCtrl.Bind(wx.EVT_TEXT, EnableButtons)
        deviceAddressTextCtrl.Bind(wx.EVT_TEXT, EnableButtons)
        groupNameCtrl.Bind(wx.EVT_TEXT, EnableButtons);

        addButton.Bind(wx.EVT_BUTTON, OnAddButton)
        updateButton.Bind(wx.EVT_BUTTON, OnUpdateButton)
        deleteButton.Bind(wx.EVT_BUTTON, OnDeleteButton)

        mappingsList.Bind(wx.EVT_LIST_ITEM_SELECTED, OnItemSelected)
        mappingsList.Bind(wx.EVT_LIST_ITEM_SELECTED, EnableButtons)
        mappingsList.Bind(wx.EVT_LIST_ITEM_DESELECTED, EnableButtons)
        EnableButtons(wx.CommandEvent())

        panel.sizer.Add(wx.StaticText(panel, -1, Text.help0))
        panel.sizer.Add(wx.StaticText(panel, -1, Text.help1))
        panel.sizer.Add(mappingsList, 1, flag = wx.EXPAND)
        panel.sizer.Add(editSizer)
        panel.sizer.Add(buttonsSizer)

        while panel.Affirmed():
            newMappings = []
            for i in range(0, mappingsList.GetItemCount()):
                item = mappingsList.GetItem(i, 0).GetText(), \
                    mappingsList.GetItem(i, 1).GetText(), \
                    mappingsList.GetItem(i, 2).GetText()
                newMappings.append(item)
            panel.SetResult(newMappings)



