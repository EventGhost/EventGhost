import time
import binascii
import ctypes
import _winreg
import sys
import threading
import win32con
import win32event
import win32file
import re

from ctypes import Structure, Union, c_byte, c_char, c_int, c_long, c_ulong, c_ushort, c_wchar
from ctypes import pointer, byref, sizeof, POINTER
from ctypes.wintypes import ULONG, BOOLEAN

DeviceRegEx = re.compile(r"\\\\\?\\(\w+)#VID_([0-9a-fA-F]+)\&PID_([0-9a-fA-F]+)#", re.IGNORECASE)

class Text:
    errorFind = "Error finding HID device: "
    errorOpen = "Error opening HID device: "
    errorRead = "Error reading HID device: "
    errorInvalidDataIndex = "Found data index not defined as button or control value."
    errorReportLength = "Report length must not be zero for device."
    errorRetrieval = "Error getting HID device info."
    errorReportLength = "Report length must not be zero for device "
    errorMultipleDevices = "Multiple devices found. Don't know which to use."
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

class HIDThread(threading.Thread):
    def __init__(self, deviceName, devicePath):
        self.handle = None
        self.text = Text
        self.deviceName = deviceName
        self.devicePath = devicePath
        self.abort = False
        self._overlappedRead = win32file.OVERLAPPED()
        self._overlappedRead.hEvent = win32event.CreateEvent(None, 1, 0, None)
        self._overlappedWrite = None
        self.RawCallback = None
        self.ButtonCallback = None
        self.ValueCallback = None
        self.StopCallback = None
        threading.Thread.__init__(self, name = self.devicePath)

    def AbortThread(self):
        self.abort = True
        if self._overlappedWrite:
            win32event.SetEvent(self._overlappedWrite.hEvent)
        win32event.SetEvent(self._overlappedRead.hEvent)

    def SetRawCallback(self, callback):
        self.RawCallback = callback;
        
    def SetButtonCallback(self, callback):
        self.ButtonCallback = callback
        
    def SetValueCallback(self, callback):
        self.ValueCallback = callback

    def SetStopCallback(self, callback):
        self.StopCallback = callback
        
    def WaitForInit(self):
        win32event.WaitForSingleObject(self._overlappedRead.hEvent, win32event.INFINITE)
        

    def Write(self, data, timeout):
        if self.handle:
            if not self._overlappedWrite:
                self._overlappedWrite = win32file.OVERLAPPED()
            err, n = win32file.WriteFile(self.handle, data, self._overlappedWrite)
            if err: #will be ERROR_IO_PENDING:
                # Wait for the write to complete.
                n = win32file.GetOverlappedResult(self.handle, self._overlappedWrite, 1)
                if n != len(data):
                    raise Exception("could not write full data")
            elif n != len(data):
                raise Exception("could not write full data")
            if timeout:#waits for response from device
                win32event.ResetEvent(self._overlappedRead.hEvent)
                res = win32event.WaitForSingleObject(self._overlappedRead.hEvent, timeout)
                if res == win32event.WAIT_TIMEOUT:
                    raise Exception("no response from device within timeout")
        else:
            raise Exception("invalid handle")
            return

    def run(self):
        #open file/device
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
            win32event.SetEvent(self._overlappedRead.hEvent)
            return

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
            eg.PrintError(self.text.errorReportLength + self.deviceName)
            
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
            else:
                ii = vCapsArr[i].Info.NotRange.DataIndex
                dataIndexType[ii] = 2

        #prepare data array with maximum possible length
        DataArrayType = HIDP_DATA * maxDataL
        data = DataArrayType()
        
        win32event.SetEvent(self._overlappedRead.hEvent)

        #initializing finished
        try:
            self.handle = handle
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
                    #device got disconnected so set status to waiting
    
                #parse data
                if len(buf) == n and not self.abort:
                    #raw data events
                    if self.RawCallback:
                        try:
                            self.RawCallback(buf)
                        except Exception:
                            eg.PrintTraceback()
    
                    #handling button presses and values
                    if maxDataL != 0:
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
                        values = {}
                        for i in range(dataL.value):
                            tmpIndex = data[i].DataIndex
                            if  tmpIndex >= len(dataIndexType):
                                eg.PrintError("invalid index for dataIndexType %d/%d" % (tmpIndex, len(dataIndexType)));
                            elif dataIndexType[tmpIndex] == 1:#button
                                #collect buttons pressed
                                btnPressed.append(tmpIndex)
                            elif dataIndexType[tmpIndex] == 2:#control value
                                values[tmpIndex] = int(data[i].Data.RawValue)
                            else:
                                eg.PrintError(self.text.errorInvalidDataIndex)
    
                        #value events
                        if (self.ValueCallback):
                            try:
                                self.ValueCallback(values)
                            except Exception:
                                eg.PrintTraceback()
                        
                        #button events
                        if self.ButtonCallback:
                            try:
                                self.ButtonCallback(btnPressed)
                            except Exception:
                                eg.PrintTraceback()
        finally:
            win32file.CloseHandle(handle)

            #free references
            hidDLL.HidD_FreePreparsedData(ctypes.byref(preparsedData))
    
            #HID thread finished
            if self.StopCallback:
                try:
                    self.StopCallback()
                except Exception:
                    eg.PrintTraceback()
            
            self.handle = None

class DeviceDescription():
    def __init__(self, devicePath, vendorId, vendorString, productId, productString, versionNumber):
        self.devicePath = devicePath
        self.vendorId = vendorId
        self.vendorString = vendorString
        self.productId = productId
        self.productString = productString
        self.versionNumber = versionNumber
        
def GetDeviceDescriptions():
    """
    gets inforamtions about the available HID as a list of DeviceDescription objects
    """
    deviceList = []

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
        i += 1

        #get the required size
        requiredSize = c_ulong()
        setupapiDLL.SetupDiGetDeviceInterfaceDetailA(hinfo,
            byref(interfaceInfo), None, 0, byref(requiredSize), None)
        if requiredSize.value > 250:
            eg.PrintError(Text.errorRetrieval)
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
        devicePath = interfaceDetailData.DevicePath

        #get handle to HID device
        try:
            hidHandle = win32file.CreateFile(
                devicePath,
                win32con.GENERIC_READ | win32con.GENERIC_WRITE,
                win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
                None,
                win32con.OPEN_EXISTING,
                0,
                0
            )
            #skipping devices which cannot be opened
            #(e.g. mice & keyboards, which are opened exclusively by OS)
            if int(hidHandle) <= 0:
                continue
        except:
            continue

        #getting additional info
        hidDLL.HidD_GetAttributes(int(hidHandle), byref(hiddAttributes))

        #prepare string buffer for device info strings
        hidpStringType = c_wchar * 128
        infoStr = hidpStringType()

        #getting manufacturer
        result = hidDLL.HidD_GetManufacturerString(
            int(hidHandle), byref(infoStr), ctypes.sizeof(infoStr))
        if not result or len(infoStr.value) == 0:
            #build a generic ManufacturerString with the vendor ID
            vendorString = Text.vendorID + str(hiddAttributes.VendorID)
        else:
            vendorString = infoStr.value

        #getting device name
        result = hidDLL.HidD_GetProductString(
            int(hidHandle), byref(infoStr), ctypes.sizeof(infoStr))
        if not result or len(infoStr.value) == 0:
            #getting product name via registry
            devicePathSplit = devicePath[4:].split("#")
            regHandle = _winreg.OpenKey(
                _winreg.HKEY_LOCAL_MACHINE,
                "SYSTEM\\CurrentControlSet\\Enum\\" + devicePathSplit[0] + \
                "\\" + devicePathSplit[1] + "\\" + devicePathSplit[2])
            productString, regType = _winreg.QueryValueEx(regHandle, "DeviceDesc")
            _winreg.CloseKey(regHandle)
        else:
            productString = infoStr.value

        #close handle
        win32file.CloseHandle(hidHandle)

        #create object with all the infos
        device = DeviceDescription(
            devicePath,
            hiddAttributes.VendorID,
            vendorString,
            hiddAttributes.ProductID,
            productString,
            hiddAttributes.VersionNumber)
        vendorString
            
        #add device to internal list
        deviceList.append(device)

    #end loop
    #destroy deviceinfolist
    setupapiDLL.SetupDiDestroyDeviceInfoList(hinfo)
    return deviceList;


def IsDeviceName(deviceNameList, vid, pid):
    """
    checks if the given vid and pid are match in the deviceNameList from System.DeviceAttached
    """
    if not deviceNameList:
        return False
    match = DeviceRegEx.match(deviceNameList[0])
    if not match:
        return False
    deviceClass, vidStr, pidStr = match.groups()
    return deviceClass == "HID" and pid == int(pidStr, 16)  and vid == int(vidStr, 16)


def GetDevicePath(
    devicePath,
    vendorId,
    productId,
    versionNumber, #pass None to ignore
    useDeviceIndex, #use True to get a specific device 
    deviceIndex, #use -1 to require the same devicePath if multiple found
    noOtherPort, #if True the devicePath has to be the same 
    deviceList = None
):
    """
    gets the devicePath
    the devicePath parameter is only used with multiple same devices
    """
    if not deviceList:
        deviceList = GetDeviceDescriptions()
    found = 0
    device = None
    for item in deviceList:
        if noOtherPort:
            #just search for devicepath
            if item.devicePath == devicePath:
                #found right device
                return devicePath
        else:
            #find the right device by vendor and product ids
            validVendorId = item.vendorId == vendorId
            validProductId = item.productId == productId
            if versionNumber == None:
                validVersionNumber = True
            else:
                validVersionNumber = item.versionNumber == versionNumber
            if validVendorId and validProductId and validVersionNumber:
                if item.devicePath == devicePath or (useDeviceIndex and deviceIndex == found):
                    #found right device
                    return item.devicePath
                found = found + 1
                device = item

    if found == 1:
        return device.devicePath

    #multiple devices found
    #don't know which to use
    if found > 1:
        eg.PrintError(Text.errorMultipleDevices)

    return None