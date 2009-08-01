import time
import binascii
import ctypes
import _winreg
import sys
import threading
import win32con
import win32event
import win32file

#constants to identify the device info
DEVICE_PATH = 0
VENDOR_ID = 1
VENDOR_STRING = 2
PRODUCT_ID = 3
PRODUCT_STRING = 4
VERSION_NUMBER = MAX_INDEX = 5

class Text:
    errorRetrieval = "Error getting HID device info."
    errorReportLength = "Report length must not be zero for device "
    errorMultipleDevices = "Multiple devices found. Don't know which to use."
    vendorID = "Vendor ID "

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
                        return item[DEVICE_PATH]
                    path = item[DEVICE_PATH]

        if found == 1:
            return path

        #multiple devices found
        #don't know which to use
        if found > 1:
            eg.PrintError(self.text.errorMultipleDevices)

        return None