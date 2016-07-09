# Xbox(original) remote control plugin for EventGhost by jinxdone. Based on the Generic HID plugin by Bartman.
#
"""<rst>
Xbox remote control plugin, based on the Generic Human Interface Device (HID) plugin.

For this plugin to work you need the `XBCDRC drivers <http://www.redcl0ud.com/xbcd_rc.html>`__ by redcl0ud

|

.. image:: xbcdrc.png
   :align: center
"""

eg.RegisterPlugin(
    name = "Xbox Remote Control",
    author = (
        "jinxdone",
        "Bartman",
    ),
    version = "0.1.3.348",
    kind = "remote",
    guid = "{00F14717-738A-40C0-8BEC-F56F5D9AAF7E}",
    canMultiLoad = False,
    description = __doc__,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAeJJREFUOMul"
        "k09I02EYxz/Pu/e33J80R6UUlEsolDCCYkSJ5S3oD1RCHaJDSEhQEHjpItShSxAU1M2SCCLo0EU6"
        "RV2KQCwkaqXk2PyTy0bbbGtuv/ftEK0xo0Y+3+vz+fLl+fKIxbKcUSxzFIAoccWRYq2QaCmKltLv"
        "BEZkWz/T0q5i0iLxv8H+Dkls6mWGVZID0AAWowJDkt91wc4m4mRkXF7aYRuphr298rQtTM5ZQNl5"
        "Uw8glUcUJe7RmyQDnaSfDOJO+b1v7eVCj5x3HresL23ojhB8FWVy9IztKjPVLSiPuKcHSTUdI/Nh"
        "DD31HDe7EfaG0fEQI4/C9kjlvq6OaVzrWXND0gdLBPd34fMdRi8s4j5oYvhZqC5aU42fR2zD6maM"
        "D3TaUJAcKnOL7QXJD9Rk0HZN3rQ2EwiV0BNRTOorxc27WbnikIwuqbT6BuvOytjJPhqddwTv3cZ4"
        "/Jh6B919kex0EvfhXWKLd+y+MmAr1HCA8asxZo5fIQXKIhiLBcH41vL93AsSPUMk2KNf/2LKcHAn"
        "c5feMxmO8A2UtSyV8lI6MUC27z6zTiufygaBDuY7rzPha6T4J7BSIHbHKb5s7efjz3RB8moLSaVx"
        "/wVXStdRknbmRDy4xrWe//3GH4uN7Ni6Xm5TAAAAAElFTkSuQmCC"

    )
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
    multipleDeviceOptions = "Options for multiple same devices"
    noOtherPort = "Use selected device only if connected to current port"
    useFirstDevice = "Use first device found"
    errorFind = "Error finding an Xbox IR receiver"
    errorOpen = "Error opening an Xbox IR receiver"
    errorRead = "Error reading an Xbox IR receiver"
    errorRetrieval = "Error getting HID device info."
    errorReportLength = "Report length must not be zero for device "
    errorMultipleDevices = "Multiple devices found. Don't know which to use."
    errorInvalidDataIndex = "Found data index not defined as button or control value."
    vendorID = "Vendor ID "
    unknownCode = "Unknown code received: "
    configurationText = "If you receive unknown codes please report these to the EventGhost forum so we can add support for them"

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
                    and item[PRODUCT_ID] == productID:
                    found = found + 1
                    if (item[DEVICE_PATH] == devicePath) or (useFirstDevice):
                        #found right device
                        return item[DEVICE_PATH]
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
        noOtherPort,
        devicePath,
        vendorID,
        vendorString,
        productID,
        productString,
        versionNumber,
        useFirstDevice
    ):
        self.plugin = plugin
        self.text = Text
        self.deviceName = vendorString + " " + productString
        self.abort = False
        self._overlappedRead = win32file.OVERLAPPED()
        self._overlappedRead.hEvent = win32event.CreateEvent(None, 1, 0, None)

        self.xbcdrc_mapping = {
            '006d50a': 'DISPLAY', '0066a05': 'DISPLAY', '0066afd': 'DISPLAY',
            '006e20a': 'REVERSE', '00671f5': 'REVERSE', '006710d': 'REVERSE',
            '006ea0a': 'PLAY', '00675f5': 'PLAY', '006750d': 'PLAY',
            '006e30a': 'FORWARD', '0067105': 'FORWARD', '00671fd': 'FORWARD',
            '006dd0a': 'SKIP-', '0066e05': 'SKIP-', '0066efd': 'SKIP-',
            '006e00a': 'STOP', '00670f5': 'STOP', '006700d': 'STOP',
            '006e60a': 'PAUSE', '00673f5': 'PAUSE', '006730d': 'PAUSE',
            '006df0a': 'SKIP+', '0066f05': 'SKIP+', '0066ffd': 'SKIP+',
            '006e50a': 'TITLE', '0067205': 'TITLE', '00672fd': 'TITLE',
            '006c30a': 'INFO', '0066105': 'INFO', '00661fd': 'INFO',
            '006a60a': 'UP', '00653f5': 'UP', '006530d': 'UP',
            '006a70a': 'DOWN', '0065305': 'DOWN', '00653fd': 'DOWN',
            '006a90a': 'LEFT', '0065405': 'LEFT', '00654fd': 'LEFT',
            '006a80a': 'RIGHT', '00654f5': 'RIGHT', '006540d': 'RIGHT',
            '0060b0a': 'SELECT', '0060505': 'SELECT', '00605fd': 'SELECT',
            '006f70a': 'MENU', '0067b05': 'MENU', '0067bfd': 'MENU',
            '006d80a': 'BACK', '0066cf5': 'BACK', '0066c0d': 'BACK',
            '006ce0a': '1', '00667f5': '1', '006670d': '1',
            '006cd0a': '2', '0066605': '2', '00666fd': '2',
            '006cc0a': '3', '00666f5': '3', '006660d': '3',
            '006cb0a': '4', '0066505': '4', '00665fd': '4',
            '006ca0a': '5', '00665f5': '5', '006650d': '5',
            '006c90a': '6', '0066405': '6', '00664fd': '6',
            '006c80a': '7', '00664f5': '7', '006640d': '7',
            '006c70a': '8', '0066305': '8', '00663fd': '8',
            '006c60a': '9', '00663f5': '9', '006630d': '9',
            '006cf0a': '0', '0066705': '0', '00667fd': '0',
            '0064f0a': 'AUDIO',
            '006af0a': 'ENT.',
            '006d100': 'LT',
            '006890a': 'LAST',
            '006c000': 'MUTE',
            '006e70a': 'A*B',
            '006f90a': 'EXIT',
            '0067f0a': 'D',
            '0068c0a': 'REC'
        }

        #getting devicePath
        self.devicePath = helper.GetDevicePath(
            noOtherPort,
            devicePath,
            vendorID,
            productID,
            versionNumber,
            useFirstDevice
        )
        plugin.devicePath = self.devicePath

        if not self.devicePath:
            plugin.PrintError(self.text.errorFind)
            self.plugin.status = 2
            return

        threading.Thread.__init__(self, name = self.devicePath)

        #setting members
        self.helper = helper
        self.enduringEvents = enduringEvents
        self.start()


    def AbortThread(self):
        self.abort = True
        win32event.SetEvent(self._overlappedRead.hEvent)
        self.plugin.status = 2

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
            self.plugin.PrintError(self.text.errorOpen)
            self.plugin.status = 3
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
        if n == 0:
            self.abort = True
            self.plugin.PrintError(self.text.errorReportLength + self.deviceName)

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

        #initiziling finished. setting status
        self.plugin.status = 1

        # Some added variables -jinxdone
        btnup_count = 0
        old_event = ""
        event_gen = False

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
                self.plugin.PrintError(self.text.errorRead)
                self.abort = True
                #device got disconnected so set status to waiting
                self.plugin.status = 2


            #parse data
            if len(buf) == n and not self.abort:
                mystr = binascii.hexlify(str(buf))[3:10]
                if mystr[0] == "0":
                    if mystr == "0000000":
                        continue
                    try:
                        mystr = self.xbcdrc_mapping[mystr]
                    except:
                        self.plugin.PrintError(self.plugin.text.unknownCode + mystr)
                        continue
                    #if mystr == old_event:
                    #    continue
                    #old_event = mystr
                    #button down event
                    if self.enduringEvents:
                        btnup_count = 0
                        if event_gen == False:
                            #enduring events
                            self.plugin.TriggerEnduringEvent(mystr)
                            event_gen = True
                    else:
                        #normal events
                        self.plugin.TriggerEvent(mystr)
                else:
                    #button up event
                    if self.enduringEvents and event_gen == True:
                        btnup_count += 1
                        if btnup_count > 13:
                            #print("Ending event..")
                            self.plugin.EndLastEvent()
                            btnup_count = 0
                            event_gen = False

        #loop aborted
        if self.enduringEvents:
            self.plugin.EndLastEvent()

        win32file.CloseHandle(handle)

        #free references
        hidDLL.HidD_FreePreparsedData(ctypes.byref(preparsedData))

        #HID thread finished



class XBCDRC(eg.PluginClass):
    helper = None
    text = Text
    thread = None
    status = -1
    # -1: not initizilized
    #  0: stopped
    #  1: running
    #  2: waiting for device
    #  3: error

    # Added to detect removing of the device, so state is updated and
    # can be recognized again when reattached -jinxdone
    def DeviceRemoved(self, event):
        """method to reconnect a disconnect device"""
        if self.status == 1:
            tmppath = event.payload[0].lower()
            if tmppath == self.devicePath:
                self.status = 2


    def ReconnectDevice(self, event):
        """method to reconnect a disconnect device"""
        if self.status == 2:
            #updating devicelist
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

            #create thread
            self.thread = HIDThread(
                self,
                self.helper,
                self.enduringEvents,
                self.noOtherPort,
                self.devicePath,
                self.vendorID,
                self.vendorString,
                self.productID,
                self.productString,
                self.versionNumber,
                self.useFirstDevice
            )

    # Modified version because of the changed config dialog.. -jinxdone
    def GetLabel(self, eventName, enduringEvents):
        return "XBCDRC"


    def __start__(self,
        eventName,
        enduringEvents
    ):

            #saving parameters so they cn be used to reconnect a device
        self.eventName = eventName
        self.enduringEvents = enduringEvents

        #saving parameters so they cn be used to reconnect a device
        self.eventName = eventName
        self.enduringEvents = enduringEvents
        #Settings from generic hid plugin set with xbox ir defaults..
        self.noOtherPort = False
        self.devicePath = ''
        self.vendorID = 1118
        self.vendorString = 'Vendor ID 1118'
        self.productID = 644
        self.productString = ''
        self.versionNumber = 0
        self.useFirstDevice = True

        if eventName:
            self.info.eventPrefix = eventName
        else:
            self.info.eventPrefix = "XBCDRC"
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
            self.noOtherPort,
            self.devicePath,
            self.vendorID,
            self.vendorString,
            self.productID,
            self.productString,
            self.versionNumber,
            self.useFirstDevice
        )
        #Bind plugin to RegisterDeviceNotification message
        eg.Bind("System.DeviceAttached", self.ReconnectDevice)

        # Added event -jinxdone
        #Bind plugin to RegisterDeviceNotification message
        eg.Bind("System.DeviceRemoved", self.DeviceRemoved)

    def __stop__(self):
        self.thread.AbortThread()

        #unbind from RegisterDeviceNotification message
        eg.Unbind("System.DeviceAttached", self.ReconnectDevice)
        self.status = 0



    def Configure(self,
        eventName = "",
        enduringEvents = True
    ):
        #ensure helper object is up to date
        if not self.helper:
            self.helper = HIDHelper()
        else:
            self.helper.UpdateDeviceList()

        panel = eg.ConfigPanel(self, resizable=True)

        #layout

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

        panel.sizer.Add(optionsSizer, 0, wx.TOP, 10)

        configurationText = wx.StaticText(panel, -1, self.text.configurationText, (0, 0), (350, 40))
        panel.sizer.Add(configurationText, 0, wx.TOP, 30)

        while panel.Affirmed():
            panel.SetResult(
                eventNameCtrl.GetValue(),
                enduringEventsCtrl.GetValue()
            )

