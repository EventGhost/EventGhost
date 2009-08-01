import time
import binascii
import ctypes
import _winreg
import sys
import threading
import win32con
import win32event
import win32file
from ctypes import Structure, Union, c_byte, c_char, c_int, c_long, c_ulong, c_ushort, c_wchar
from ctypes import pointer, byref, sizeof, POINTER
from ctypes.wintypes import ULONG, BOOLEAN

class Text:
    errorFind = "Error finding HID device: "
    errorOpen = "Error opening HID device: "
    errorRead = "Error reading HID device: "
    errorInvalidDataIndex = "Found data index not defined as button or control value."
    errorReportLength = "Report length must not be zero for device."

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
        self.plugin = plugin
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
            plugin.PrintError(self.text.errorFind + self.deviceName)
            self.plugin.status = 2
            return

        threading.Thread.__init__(self, name = self.devicePath)

        #setting members
        self.helper = helper
        self.enduringEvents = enduringEvents
        self.rawDataEvents = rawDataEvents
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
            self.plugin.PrintError(self.text.errorOpen + self.deviceName)
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
                self.plugin.PrintError(self.text.errorRead + self.deviceName)
                self.abort = True
                #device got disconnected so set status to waiting
                self.plugin.status = 2

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
                            self.plugin.PrintError(self.text.errorInvalidDataIndex)
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
