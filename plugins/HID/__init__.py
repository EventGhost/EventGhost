import eg

eg.RegisterPlugin(
    name = "Generic HID",
    author = "Bartman",
    version = "1.0." + "$LastChangedRevision$".split()[1],
    kind = "remote",
    description = (
        'Communication with devices that follow the '
        'Human Interface Device (HID) standard.'
    ),
)

import time
import binascii
import ctypes
import _winreg
import sys
import threading
import win32con
import win32event
import win32file
import wx
import wx.lib.mixins.listctrl as listmix

from ctypes import Structure, Union, c_byte, c_char, c_int, c_long, c_ulong, c_ushort, c_wchar
from ctypes import pointer, byref, sizeof, POINTER
from ctypes.wintypes import ULONG, BOOLEAN

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
    errorMultipleDevices = "Multiple devices found. Don't know which to use."
    errorInvalidDataIndex = "Found data index not defined as button or control value."
    vendorID = "Vendor ID "

#structures for ctypes
class GUID(Structure):
    _fields_ = [
        ("Data1", c_ulong),
        ("Data2", c_ushort),
        ("Data3", c_ushort),
        ("Data4", c_byte * 8)
    ]

class SP_DEVICE_INTERFACE_DATA(Structure):
    _fields_ = [("cbSize", c_ulong),
        ("InterfaceClassGuid", GUID),
        ("Flags", c_ulong),
        ("Reserved", POINTER(ULONG))
    ]

class SP_DEVICE_INTERFACE_DETAIL_DATA_A(Structure):
    _fields_ = [("cbSize", c_ulong),
        ("DevicePath", c_char * 255)
    ]

class HIDD_ATTRIBUTES(Structure):
    _fields_ = [("cbSize", c_ulong),
        ("VendorID", c_ushort),
        ("ProductID", c_ushort),
        ("VersionNumber", c_ushort)
    ]

class HIDP_CAPS(Structure):
    _fields_ = [
        ("Usage", c_ushort),
        ("UsagePage", c_ushort),
        ("InputReportByteLength", c_ushort),
        ("OutputReportByteLength", c_ushort),
        ("FeatureReportByteLength", c_ushort),
        ("Reserved", c_ushort * 17),
        ("NumberLinkCollectionNodes", c_ushort),
        ("NumberInputButtonCaps", c_ushort),
        ("NumberInputValueCaps", c_ushort),
        ("NumberInputDataIndices", c_ushort),
        ("NumberOutputButtonCaps", c_ushort),
        ("NumberOutputValueCaps", c_ushort),
        ("NumberOutputDataIndices", c_ushort),
        ("NumberFeatureButtonCaps", c_ushort),
        ("NumberFeatureValueCaps", c_ushort),
        ("NumberFeatureDataIndices", c_ushort)
    ]

class HIDP_CAPS_UNION(Union):
    class HIDP_BUTTON_CAPS_RANGE(Structure):
        _fields_ = [
            ("UsageMin", c_ushort),
            ("UsageMax", c_ushort),
            ("StringMin", c_ushort),
            ("StringMax", c_ushort),
            ("DesignatorMin", c_ushort),
            ("DesignatorMax", c_ushort),
            ("DataIndexMin", c_ushort),
            ("DataIndexMax", c_ushort)
        ]

    class HIDP_BUTTON_CAPS_NOT_RANGE(Structure):
        _fields_ = [
            ("Usage", c_ushort),
            ("Reserved1", c_ushort),
            ("StringIndex", c_ushort),
            ("Reserved2", c_ushort),
            ("DesignatorIndex", c_ushort),
            ("Reserved3", c_ushort),
            ("DataIndex", c_ushort),
            ("Reserved4", c_ushort)
        ]

    _fields_ = [
        ("Range", HIDP_BUTTON_CAPS_RANGE),
        ("NotRange", HIDP_BUTTON_CAPS_NOT_RANGE)
    ]

class HIDP_BUTTON_CAPS(Structure):
    _fields_ = [
        ("UsagePage", c_ushort),
        ("ReportID", c_char),
        ("IsAlias", BOOLEAN),
        ("BitField", c_ushort),
        ("LinkCollection", c_ushort),
        ("LinkUsage", c_ushort),
        ("LinkUsagePage", c_ushort),
        ("IsRange", BOOLEAN),
        ("IsStringRange", BOOLEAN),
        ("IsDesignatorRange", BOOLEAN),
        ("IsAbsolute", BOOLEAN),
        ("Reserved", c_ulong * 10),
        ("Info", HIDP_CAPS_UNION)
    ]

class HIDP_VALUE_CAPS(Structure):
    _fields_ = [
        ("UsagePage", c_ushort),
        ("ReportID", c_char),
        ("IsAlias", BOOLEAN),
        ("BitField", c_ushort),
        ("LinkCollection", c_ushort),
        ("LinkUsage", c_ushort),
        ("LinkUsagePage", c_ushort),
        ("IsRange", BOOLEAN),
        ("IsStringRange", BOOLEAN),
        ("IsDesignatorRange", BOOLEAN),
        ("IsAbsolute", BOOLEAN),
        ("HasNull", BOOLEAN),
        ("Reserved", c_char),
        ("BitSize", c_ushort),
        ("ReportCount", c_ushort),
        ("Reserved2", c_ushort * 5),
        ("UnitsExp", c_ulong),
        ("Units", c_ulong),
        ("LogicalMin", c_long),
        ("LogicalMax", c_long),
        ("PhysicalMin", c_long),
        ("PhysicalMax", c_long),
        ("Info", HIDP_CAPS_UNION)
    ]

class HIDP_DATA(Structure):
    class HIDP_DATA_VALUE(Union):
        _fields_ = [
            ("RawValue", c_ulong),
            ("On", BOOLEAN),
        ]

    _fields_ = [
        ("DataIndex", c_ushort),
        ("Reserved", c_ushort),
        ("Data", HIDP_DATA_VALUE)
    ]

# Flags controlling what is included in the device information set built
# by SetupDiGetClassDevs
DIGCF_DEFAULT         = 0x00000001  # only valid with DIGCF_DEVICEINTERFACE
DIGCF_PRESENT         = 0x00000002
DIGCF_ALLCLASSES      = 0x00000004
DIGCF_PROFILE         = 0x00000008
DIGCF_DEVICEINTERFACE = 0x00000010

#constants to identify the device info
DEVICE_PATH = 0
VENDOR_ID = 1
VENDOR_STRING = 2
PRODUCT_ID = 3
PRODUCT_STRING = 4
VERSION_NUMBER = MAX_INDEX = 5


#helper class to iterate, find and open hid devices
class HIDHelper:
    text = Text
    deviceList = []

    def __init__(self):
        self.UpdateDeviceList()

    def UpdateDeviceList(self):
        self.deviceList = []

        #dll references
        setupapiDLL = ctypes.windll.setupapi
        hidDLL =  ctypes.windll.hid

        #prepare Interfacedata
        interfaceInfo = SP_DEVICE_INTERFACE_DATA()
        interfaceInfo.cbSize = sizeof(interfaceInfo)

        #prepare InterfaceDetailData Structure
        interfaceDetailData = SP_DEVICE_INTERFACE_DETAIL_DATA_A()
        interfaceDetailData.cbSize = 5

        #prepare HIDD_ATTRIBUTES
        hiddAttributes = HIDD_ATTRIBUTES()
        hiddAttributes.cbSize = sizeof(hiddAttributes)

        #get guid for HID device class
        g = GUID()
        hidDLL.HidD_GetHidGuid(byref(g))

        #get handle to the device information set
        hinfo = setupapiDLL.SetupDiGetClassDevsA(byref(g), None, None,
            DIGCF_PRESENT + DIGCF_DEVICEINTERFACE)

        #enumerate devices
        i = 0
        while setupapiDLL.SetupDiEnumDeviceInterfaces(hinfo,
            None, byref(g), i, byref(interfaceInfo)):
            device = {}
            i += 1

            #get the required size
            requiredSize = c_ulong()
            setupapiDLL.SetupDiGetDeviceInterfaceDetailA(hinfo,
                byref(interfaceInfo), None, 0, byref(requiredSize), None)
            if requiredSize.value > 250:
                eg.PrintError(self.text.errorRetrieval)
                continue #prevent a buffer overflow

            #get the actual info
            setupapiDLL.SetupDiGetDeviceInterfaceDetailA(
                hinfo,
                byref(interfaceInfo),
                byref(interfaceDetailData),
                requiredSize,
                pointer(requiredSize),
                None
            )
            device[DEVICE_PATH] = interfaceDetailData.DevicePath

            #get handle to HID device
            try:
                hidHandle = win32file.CreateFile(
                    device[DEVICE_PATH],
                    win32con.GENERIC_READ | win32con.GENERIC_WRITE,
                    win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
                    None,
                    win32con.OPEN_EXISTING,
                    0,
                    0
                )
                #skipping devices which cannot be opened
                #(e.g. mice & keyboards, which are opened exclusivly by OS)
                if int(hidHandle) <= 0:
                    continue
            except:
                continue

            #getting additional info
            hidDLL.HidD_GetAttributes(int(hidHandle), byref(hiddAttributes))
            device[VENDOR_ID] = hiddAttributes.VendorID
            device[PRODUCT_ID] = hiddAttributes.ProductID
            device[VERSION_NUMBER] = hiddAttributes.VersionNumber

            #prepare string buffer for device info strings
            hidpStringType = c_wchar * 128
            infoStr = hidpStringType()

            #getting manufacturer
            result = hidDLL.HidD_GetManufacturerString(
                int(hidHandle), byref(infoStr), ctypes.sizeof(infoStr))
            if not result or len(infoStr.value) == 0:
                #build a generic ManufacturerString with the vendor ID
                device[VENDOR_STRING] = self.text.vendorID + str(hiddAttributes.VendorID)
            else:
                device[VENDOR_STRING] = infoStr.value

            #getting device name
            result = hidDLL.HidD_GetProductString(
                int(hidHandle), byref(infoStr), ctypes.sizeof(infoStr))
            if not result or len(infoStr.value) == 0:
                #getting product name via registry
                devicePathSplit = device[DEVICE_PATH][4:].split("#")
                regHandle = _winreg.OpenKey(
                    _winreg.HKEY_LOCAL_MACHINE,
                    "SYSTEM\\CurrentControlSet\\Enum\\" + devicePathSplit[0] + \
                    "\\" + devicePathSplit[1] + "\\" + devicePathSplit[2])
                device[PRODUCT_STRING], regType = _winreg.QueryValueEx(regHandle, "DeviceDesc")
                _winreg.CloseKey(regHandle)
            else:
                device[PRODUCT_STRING] = infoStr.value

            #close handle
            win32file.CloseHandle(hidHandle)

            #add device to internal list
            self.deviceList.append(device)

        #end loop
        #destroy deviceinfolist
        setupapiDLL.SetupDiDestroyDeviceInfoList(hinfo)


    #gets the devicePath
    #the devicePath parameter is only used with multiple same devices
    def GetDevicePath(self,
        noOtherPort,
        devicePath,
        vendorID,
        productID,
        versionNumber,
        useFirstDevice = False
    ):
        found = 0
        path = ""
        for item in self.deviceList:
            if noOtherPort:
                #just search for devicepath
                if item[DEVICE_PATH] == devicePath:
                    #found right device
                    return devicePath
            else:
                #find the right vendor and product ids
                if item[VENDOR_ID] == vendorID \
                    and item[PRODUCT_ID] == productID \
                    and item[VERSION_NUMBER] == versionNumber:
                    found = found + 1
                    if (item[DEVICE_PATH] == devicePath) or (useFirstDevice):
                        #found right device
                        return devicePath
                    path = item[DEVICE_PATH]

        if found == 1:
            return path

        #multiple devices found
        #don't know which to use
        if found > 1:
            eg.PrintError(self.text.errorMultipleDevices)

        return None


class HIDThread(threading.Thread):
    def __init__(self,
        plugin,
        helper,
        enduringEvents,
        rawDataEvents,
        noOtherPort,
        devicePath,
        vendorID,
        vendorString,
        productID,
        productString,
        versionNumber,
        useFirstDevice
    ):
        self.text = Text
        self.deviceName = vendorString + " " + productString
        self.abort = False
        self._overlappedRead = win32file.OVERLAPPED()
        self._overlappedRead.hEvent = win32event.CreateEvent(None, 1, 0, None)

        #getting devicePath
        self.devicePath = helper.GetDevicePath(
            noOtherPort,
            devicePath,
            vendorID,
            productID,
            versionNumber,
            useFirstDevice
        )

        if not self.devicePath:
            eg.PrintError(self.text.errorFind + self.deviceName)
            return

        threading.Thread.__init__(self, name = self.devicePath)

        #setting members
        self.plugin = plugin
        self.helper = helper
        self.enduringEvents = enduringEvents
        self.rawDataEvents = rawDataEvents
        self.start()


    def AbortThread(self):
        self.abort = True
        win32event.SetEvent(self._overlappedRead.hEvent)


    def run(self):
        #open file/devcice
        try:
            handle = win32file.CreateFile(
                self.devicePath,
                    win32con.GENERIC_READ | win32con.GENERIC_WRITE,
                    win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
                None, # no security
                win32con.OPEN_EXISTING,
                win32con.FILE_ATTRIBUTE_NORMAL | win32con.FILE_FLAG_OVERLAPPED,
                0
            )
        except:
            eg.PrintError(self.text.errorOpen + self.deviceName)
            return

        #getting data to get the right buffer size
        hidDLL =  ctypes.windll.hid
        setupapiDLL = ctypes.windll.setupapi

        #get preparsed data
        preparsedData = c_ulong()
        result = hidDLL.HidD_GetPreparsedData(
            int(handle),
            ctypes.byref(preparsedData)
        )

        #getCaps
        hidpCaps = HIDP_CAPS()
        result = hidDLL.HidP_GetCaps(preparsedData, ctypes.byref(hidpCaps))

        n = hidpCaps.InputReportByteLength
        rt = c_int(0)   #report type input
        rl = c_ulong(n)  #report length
        maxDataL = hidDLL.HidP_MaxDataListLength(rt, preparsedData)

        #getting button caps
        bCapsArrL = c_ushort(hidpCaps.NumberInputButtonCaps)
        bCapsArrType = HIDP_BUTTON_CAPS * bCapsArrL.value
        bCapsArr = bCapsArrType()

        hidDLL.HidP_GetButtonCaps(
            rt,
            ctypes.byref(bCapsArr),
            ctypes.byref(bCapsArrL),
            preparsedData
        )

        #getting value caps
        vCapsArrL = c_ushort(hidpCaps.NumberInputValueCaps)
        vCapsArrType = HIDP_VALUE_CAPS * vCapsArrL.value
        vCapsArr = vCapsArrType()

        hidDLL.HidP_GetValueCaps(
            rt,
            ctypes.byref(vCapsArr),
            ctypes.byref(vCapsArrL),
            preparsedData
        )

        #parsing caps
        # prepare a list to find and store for each index
        # whether it is a button or value
        oldValues = {}
        dataIndexType = [0] * hidpCaps.NumberInputDataIndices

        #list entries depending on caps
        for i in range(bCapsArrL.value):
            if bCapsArr[i].IsRange:
                for ii in range(
                    bCapsArr[i].Info.Range.DataIndexMin,
                    bCapsArr[i].Info.Range.DataIndexMax + 1
                ):
                    dataIndexType[ii] = 1
            else:
                ii = bCapsArr[i].Info.NotRange.DataIndex
                dataIndexType[ii] = 1


        for i in range(vCapsArrL.value):
            if vCapsArr[i].IsRange:
                for ii in range(
                    vCapsArr[i].Info.Range.DataIndexMin,
                    vCapsArr[i].Info.Range.DataIndexMax + 1
                ):
                    dataIndexType[ii] = 2
                    oldValues[ii] = sys.maxint
            else:
                ii = vCapsArr[i].Info.NotRange.DataIndex
                dataIndexType[ii] = 2
                oldValues[ii] = sys.maxint

        #prepare data array with maximum possible length
        DataArrayType = HIDP_DATA * maxDataL
        data = DataArrayType()

        while not self.abort:
            #try to read and wait for an event to happen
            try:
                win32event.ResetEvent(self._overlappedRead.hEvent)
                rc, buf = win32file.ReadFile(handle, n, self._overlappedRead)
                #waiting for an event
                win32event.WaitForSingleObject(
                    self._overlappedRead.hEvent,
                    win32event.INFINITE
                )
            except:
                eg.PrintError(self.text.errorRead + self.deviceName)
                self.abort = True

            #parse data
            if len(buf) == n and not self.abort:
                #raw data events
                if maxDataL == 0 or self.rawDataEvents:
                    read = str(buf)
                    self.plugin.TriggerEvent(
                        binascii.hexlify(read).upper()
                    )
                else:
                    dataL = c_ulong(maxDataL)
                    result = hidDLL.HidP_GetData(
                        rt,
                        ctypes.byref(data),
                        ctypes.byref(dataL),
                        preparsedData,
                        ctypes.c_char_p(str(buf)),
                        rl
                    )
                    #parse data to trigger events
                    btnPressed = []
                    for i in range(dataL.value):
                        tmpIndex = data[i].DataIndex
                        if dataIndexType[tmpIndex] == 1:#button
                            #collect buttons pressed
                            btnPressed.append(str(tmpIndex))
                        elif dataIndexType[tmpIndex] == 2:#control value
                            newValue = int(data[i].Data.RawValue)
                            if newValue == oldValues[tmpIndex]:
                                continue
                            oldValues[tmpIndex] = newValue
                            self.plugin.TriggerEvent(
                                "Value." + str(tmpIndex),
                                payload = newValue
                            )
                        else:
                            eg.PrintError(self.text.errorInvalidDataIndex)
                    if len(btnPressed):
                        #one or more buttons pressed
                        #btnPressed.sort()
                        evtName = "Button." + "+".join(btnPressed)
                        if self.enduringEvents:
                            self.plugin.TriggerEnduringEvent(evtName)
                        else:
                            self.plugin.TriggerEvent(evtName)
                    elif self.enduringEvents:
                        #no buttons pressed anymore
                        self.plugin.EndLastEvent()
                    else:
                        #trigger event so that releasing all buttons
                        #can get noticed even w/o enduring events
                        self.plugin.TriggerEvent("Button.None")

        #loop aborted
        if self.enduringEvents:
            self.plugin.EndLastEvent()

        win32file.CloseHandle(handle)

        #free references
        hidDLL.HidD_FreePreparsedData(ctypes.byref(preparsedData))

        #HID thread finished


class HID(eg.PluginClass):
    helper = None
    canMultiLoad = True
    text = Text
    thread = None

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

        #productString already contains manufacturer of vendor id only
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
        if eventName:
            self.info.eventPrefix = eventName
        else:
            self.info.eventPrefix = "HID"
        #ensure helper object is up to date
        if not self.helper:
            self.helper = HIDHelper()
        else:
            self.helper.UpdateDeviceList()

        #create thread
        self.thread = HIDThread(
            self,
            self.helper,
            enduringEvents,
            rawDataEvents,
            noOtherPort,
            devicePath,
            vendorID,
            vendorString,
            productID,
            productString,
            versionNumber,
            useFirstDevice
        )

    def __stop__(self):
        self.thread.AbortThread()


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

        dialog = eg.ConfigurationDialog(self, resizeable=True)

        #building dialog
        hidList = wx.ListCtrl(dialog, -1, pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)

        #create GUI
        hidList.InsertColumn(0, self.text.deviceName)
        hidList.InsertColumn(1, self.text.manufacturer)
        hidList.InsertColumn(2, self.text.connected)


        path = self.helper.GetDevicePath(noOtherPort,
            devicePath, vendorID, productID, versionNumber)

        #fill list
        devices = {}
        idx = 0
        for item in self.helper.deviceList:
            idx = hidList.InsertStringItem(sys.maxint, item[PRODUCT_STRING])
            hidList.SetStringItem(idx, 1, item[VENDOR_STRING])
            hidList.SetStringItem(idx, 2, self.text.yes)
            if item[DEVICE_PATH] == path:
                hidList.Select(idx)
            devices[idx] = item

        #add not connected device to bottom of list
        if not path:
            if devicePath:
                item = {
                    DEVICE_PATH: devicePath,
                    VENDOR_ID: vendorID,
                    VENDOR_STRING: vendorString,
                    PRODUCT_ID: productID,
                    PRODUCT_STRING: productString,
                    VERSION_NUMBER: versionNumber,
                }
                idx = hidList.InsertStringItem(sys.maxint, item[PRODUCT_STRING])
                hidList.SetStringItem(idx, 1, item[VENDOR_STRING])
                hidList.SetStringItem(idx, 2, self.text.no)
                hidList.Select(idx)
                devices[idx] = item

        if hidList.GetFirstSelected() == -1:
            #no device selected, disable ok button
            dialog.buttonRow.okButton.Enable(False)

        #layout
        for i in range(hidList.GetColumnCount()):
            hidList.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            size = hidList.GetColumnWidth(i)
            hidList.SetColumnWidth(i, wx.LIST_AUTOSIZE)
            hidList.SetColumnWidth(i, max(size, hidList.GetColumnWidth(i) + 5))

        dialog.sizer.Add(hidList, 1, flag = wx.EXPAND)

        #sizers
        optionsSizer = wx.GridBagSizer(0, 5)

        #eventname
        optionsSizer.Add(
            wx.StaticText(dialog, -1, self.text.eventName),
            (0, 0),
            flag = wx.ALIGN_CENTER_VERTICAL)
        eventNameCtrl = wx.TextCtrl(dialog, value = eventName)
        eventNameCtrl.SetMaxLength(32)
        optionsSizer.Add(eventNameCtrl, (0, 1), (1, 2), flag = wx.EXPAND)

        #checkbox for enduring event option
        enduringEventsCtrl = wx.CheckBox(dialog, -1, self.text.enduringEvents)
        enduringEventsCtrl.SetValue(enduringEvents)
        optionsSizer.Add(enduringEventsCtrl, (1, 0), (1, 3))

        #checkbox for raw data events
        rawDataEventsCtrl = wx.CheckBox(dialog, -1, self.text.rawDataEvents)
        rawDataEventsCtrl.SetValue(rawDataEvents)
        optionsSizer.Add(rawDataEventsCtrl, (2, 0), (1, 3))

        #text
        optionsSizer.Add(
            wx.StaticText(dialog, -1, self.text.multipleDeviceOptions),
            (3, 0), (1, 3),
            flag = wx.ALIGN_CENTER_VERTICAL)
        
        #checkbox for use first device
        useFirstDeviceCtrl = wx.CheckBox(dialog, -1, self.text.useFirstDevice)
        useFirstDeviceCtrl.SetValue(useFirstDevice)
        optionsSizer.Add(useFirstDeviceCtrl, (4, 0), (1, 3))

        #checkbox for no other port option
        noOtherPortCtrl = wx.CheckBox(dialog, -1, self.text.noOtherPort)
        noOtherPortCtrl.SetValue(noOtherPort)
        optionsSizer.Add(noOtherPortCtrl, (5, 0), (1, 3))

        dialog.sizer.Add(optionsSizer)

        def OnHidListSelect(event):
            dialog.buttonRow.okButton.Enable(True)
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

        if dialog.AffirmedShowModal():
            device = devices[hidList.GetFirstSelected()]
            return (
                eventNameCtrl.GetValue(),
                enduringEventsCtrl.GetValue(),
                rawDataEventsCtrl.GetValue(),
                noOtherPortCtrl.GetValue(),
                device[DEVICE_PATH],
                device[VENDOR_ID],
                device[VENDOR_STRING],
                device[PRODUCT_ID],
                device[PRODUCT_STRING],
                device[VERSION_NUMBER],
                useFirstDeviceCtrl.GetValue()
            )

