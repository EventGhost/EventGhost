README = """\
<u><b>1) Bluetooth</b></u>

Tested succesfully working with Bluetooth Software :
WIDCOMM Bluetooth Software 5.1.0.1100.

5.1.0.1100 is not the last version, but it's the most versatile version and
works with most of Bluetooth adapter in a patched version. 
See <a href"http://forum.gsmhosting.com/vbb/forumdisplay.php?f=237">
this thread</a> to help about patched WIDCOMM Bluetooth Software 5.1.0.1100
(Restart PC, right click on bluetooth icon in task bar and stop/start bluetooth 
device can help)

On remote, to activate discoverable mode, press simultaneously "start+enter". 
On PC choose "Next (no code)"

Check in "Device Manager" / "Human Interface Devices" that the
PS3 Remote appears as "HID-compliant game controller".
If not, if it appears as "HID Keyboard Device" in "Keyboards",
delete it, right click on bluetooth icon in task bar and 
stop/start bluetooth device to force new device detection. 
This time should appears as "HID-compliant game controller"

<u><b>2) Plugin</b></u>

This plugin generates: 

<ul>
<li>ENDURING events named like "HID.Eject"</li>
</ul>

and lot of additional NORMAL events for:

<ul>
<li>short click on remote, events name end with ".S" eg. "HID.Eject.S"</li>
<li>long click on remote, events name end with ".L"</li>
<li>double click on remote, events name end with ".D"</li>
</ul>

and special selectable or not events:

<ul>
<li>"Sleep" when remote is not used</li>
<li>"Hibernate" when remote is not use during a long time (also puts the remote into low-power mode
    if using the Widcomm Bluetooth stack)</li>
<li>"WakeUp" for first event after "Sleep" or "Hibernate"</li>
<li>"Zone.X" where X is relative to Zone Key in Remote (see Remote paper manual)
  event generated when a new key is pressed in another zone.
  each remote key belong of on zone except one, the key with strange
  symbol below the directional pad. this is by design.</li>
<li>"Release" can be generated for each relase of each key.</li>
</ul>

Of course all these additional events are not needed,
it's possible to do the same thing by EventGhost configuration
but it's far more simple to have these events available
ready to use, than play with timer inside EventGhost.

This remote can generate events when 2 keys are pressed simultaneously.
In this case the event code genered is an hexadecimal value.

Note: some keys combination generate the same event. 
This is a Remote issue.

After the "Hibernate" period expires, the remote will be put into a low-power (SNIFF) mode.
It may take a few seconds for the first button press to be registered in this mode.

The plugin will also automatically re-detect the PS3 remote after being in standby mode.
"""

eg.RegisterPlugin(
    name = "PlayStation 3 Bluetooth Remote",
    author = "Thierry Couquillou, Tim Delaney",
    version = "3.0.0",
    kind = "remote",
    guid = "{7224079E-1823-48B0-8ED6-30973BDDC96D}",
    url="http://www.eventghost.org/forum/viewtopic.php?t=640",
    description = "Hardware plugin for the PS3 Bluetooth Remote (based on the HID code of Bartman)",
    canMultiLoad = True,
    help = README,
)

import itertools
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

from ctypes import Structure, Union, c_byte, c_ubyte, c_char, c_int, c_long, c_ulong, c_ushort, c_wchar
from ctypes import pointer, byref, sizeof, POINTER
from ctypes.wintypes import ULONG, BOOLEAN, BOOL

class Ps3Remote:
    button = {}
    button["000000FFFFFFFFFFFF00"]= "Release"

    button["00000016FFFFFFFFFF01"]= "Eject"
    button["00000064FFFFFFFFFF01"]= "Audio"
    button["00000065FFFFFFFFFF01"]= "Angle"
    button["00000063FFFFFFFFFF01"]= "Subtitle"

    button["00000000FFFFFFFFFF01"]= "Num1"
    button["00000001FFFFFFFFFF01"]= "Num2"
    button["00000002FFFFFFFFFF01"]= "Num3"
    button["00000003FFFFFFFFFF01"]= "Num4"
    button["00000004FFFFFFFFFF01"]= "Num5"
    button["00000005FFFFFFFFFF01"]= "Num6"
    button["00000006FFFFFFFFFF01"]= "Num7"
    button["00000007FFFFFFFFFF01"]= "Num8"
    button["00000008FFFFFFFFFF01"]= "Num9"
    button["0000000FFFFFFFFFFF01"]= "Clear"
    button["00000009FFFFFFFFFF01"]= "Num0"
    button["00000028FFFFFFFFFF01"]= "Time"

    button["00000081FFFFFFFFFF01"]= "Red"
    button["00000082FFFFFFFFFF01"]= "Green"
    button["00000083FFFFFFFFFF01"]= "Yellow"
    button["00000080FFFFFFFFFF01"]= "Blue"

    button["00000070FFFFFFFFFF01"]= "Display"
    button["0000001AFFFFFFFFFF01"]= "TopMenu"
    button["00000040FFFFFFFFFF01"]= "PopUpMenu"
    button["0000000EFFFFFFFFFF01"]= "Return"

    button["10000054FFFFFFFFFF01"]= "Up"
    button["300000FFFFFFFFFFFF01"]= "RightUp"
    button["20000055FFFFFFFFFF01"]= "Right"
    button["600000FFFFFFFFFFFF01"]= "RightDown"
    button["40000056FFFFFFFFFF01"]= "Down"
    button["C00000FFFFFFFFFFFF01"]= "LeftDown"
    button["80000057FFFFFFFFFF01"]= "Left"
    button["900000FFFFFFFFFFFF01"]= "LeftUp"
    button["0000080BFFFFFFFFFF01"]= "Enter"

    button["0010005CFFFFFFFFFF01"]= "Triangle"
    button["0020005DFFFFFFFFFF01"]= "Circle"
    button["0080005FFFFFFFFFFF01"]= "Square"
    button["0040005EFFFFFFFFFF01"]= "Cross"

    button["0004005AFFFFFFFFFF01"]= "L1"
    button["00010058FFFFFFFFFF01"]= "L2"
    button["02000051FFFFFFFFFF01"]= "L3"

    button["00000143FFFFFFFFFF01"]= "Zarbi"
    button["01000050FFFFFFFFFF01"]= "Select"
    button["08000053FFFFFFFFFF01"]= "Start"

    button["0008005BFFFFFFFFFF01"]= "R1"
    button["00020059FFFFFFFFFF01"]= "R2"
    button["04000052FFFFFFFFFF01"]= "R3"

    button["00000033FFFFFFFFFF01"]= "Scan-"
    button["00000032FFFFFFFFFF01"]= "Play"
    button["00000034FFFFFFFFFF01"]= "Scan+"

    button["00000030FFFFFFFFFF01"]= "Prev"
    button["00000038FFFFFFFFFF01"]= "Stop"
    button["00000031FFFFFFFFFF01"]= "Next"

    button["00000060FFFFFFFFFF01"]= "SlowStep-"
    button["00000039FFFFFFFFFF01"]= "Pause"
    button["00000061FFFFFFFFFF01"]= "SlowStep+"

    zone = {}
    zone["000000FFFFFFFFFFFF00"]= "none"

    zone["00000016FFFFFFFFFF01"]= "Zone.A1"
    zone["00000064FFFFFFFFFF01"]= "Zone.A1"
    zone["00000065FFFFFFFFFF01"]= "Zone.A1"
    zone["00000063FFFFFFFFFF01"]= "Zone.A1"

    zone["00000000FFFFFFFFFF01"]= "Zone.A2"
    zone["00000001FFFFFFFFFF01"]= "Zone.A2"
    zone["00000002FFFFFFFFFF01"]= "Zone.A2"
    zone["00000003FFFFFFFFFF01"]= "Zone.A2"
    zone["00000004FFFFFFFFFF01"]= "Zone.A2"
    zone["00000005FFFFFFFFFF01"]= "Zone.A2"
    zone["00000006FFFFFFFFFF01"]= "Zone.A2"
    zone["00000007FFFFFFFFFF01"]= "Zone.A2"
    zone["00000008FFFFFFFFFF01"]= "Zone.A2"
    zone["0000000FFFFFFFFFFF01"]= "Zone.A2"
    zone["00000009FFFFFFFFFF01"]= "Zone.A2"
    zone["00000028FFFFFFFFFF01"]= "Zone.A2"

    zone["00000081FFFFFFFFFF01"]= "Zone.A3"
    zone["00000082FFFFFFFFFF01"]= "Zone.A3"
    zone["00000083FFFFFFFFFF01"]= "Zone.A3"
    zone["00000080FFFFFFFFFF01"]= "Zone.A3"

    zone["00000070FFFFFFFFFF01"]= "Zone.A3"
    zone["0000001AFFFFFFFFFF01"]= "Zone.A3"
    zone["00000040FFFFFFFFFF01"]= "Zone.A3"
    zone["0000000EFFFFFFFFFF01"]= "Zone.A3"

    zone["10000054FFFFFFFFFF01"]= "Zone.Pad"
    zone["300000FFFFFFFFFFFF01"]= "Zone.Pad"
    zone["20000055FFFFFFFFFF01"]= "Zone.Pad"
    zone["600000FFFFFFFFFFFF01"]= "Zone.Pad"
    zone["40000056FFFFFFFFFF01"]= "Zone.Pad"
    zone["C00000FFFFFFFFFFFF01"]= "Zone.Pad"
    zone["80000057FFFFFFFFFF01"]= "Zone.Pad"
    zone["900000FFFFFFFFFFFF01"]= "Zone.Pad"
    zone["0000080BFFFFFFFFFF01"]= "Zone.Pad"

    zone["0010005CFFFFFFFFFF01"]= "Zone.B1"
    zone["0020005DFFFFFFFFFF01"]= "Zone.B1"
    zone["0080005FFFFFFFFFFF01"]= "Zone.B1"
    zone["0040005EFFFFFFFFFF01"]= "Zone.B1"

    zone["0004005AFFFFFFFFFF01"]= "Zone.B2"
    zone["00010058FFFFFFFFFF01"]= "Zone.B2"
    zone["02000051FFFFFFFFFF01"]= "Zone.B2"

    zone["00000143FFFFFFFFFF01"]= "none"
    zone["01000050FFFFFFFFFF01"]= "Zone.B2"
    zone["08000053FFFFFFFFFF01"]= "Zone.B2"

    zone["0008005BFFFFFFFFFF01"]= "Zone.B2"
    zone["00020059FFFFFFFFFF01"]= "Zone.B2"
    zone["04000052FFFFFFFFFF01"]= "Zone.B2"

    zone["00000033FFFFFFFFFF01"]= "Zone.C"
    zone["00000032FFFFFFFFFF01"]= "Zone.C"
    zone["00000034FFFFFFFFFF01"]= "Zone.C"

    zone["00000030FFFFFFFFFF01"]= "Zone.C"
    zone["00000038FFFFFFFFFF01"]= "Zone.C"
    zone["00000031FFFFFFFFFF01"]= "Zone.C"

    zone["00000060FFFFFFFFFF01"]= "Zone.C"
    zone["00000039FFFFFFFFFF01"]= "Zone.C"
    zone["00000061FFFFFFFFFF01"]= "Zone.C"

class Text:
    manufacturer = "Manufacturer"
    deviceName = "Device Name"
    connected = "Connected"
    eventName = "Event prefix (optional):"
    yes = "Yes"
    no = "No"
    eventsSettings = "Remote Events Settings"
    enduringEvents = "Trigger enduring events for buttons"
    rawDataEvents = "Use raw Data as event name"
    ps3Settings = "PS3 Remote Events Settings"
    ps3DataEvents = "Use ps3 Remote Key as event name"
    ps3Release = "Generate ps3 Remote Release event"
    ps3Zone = "Generate ps3 Remote Zone event"
    shortKeyTime = "Short press if lower than"
    longKeyTime = "Long press if greater than"
    sleepTime = "Sleep event generated after"
    hibernateTime = "Hibernate event generated after"
    seconds = "seconds"
    noOtherPort = "Use selected device only if connected to current port"
    errorFind = "Error finding HID device: "
    errorOpen = "Error opening HID device: "
    errorRead = "Error reading HID device: "
    errorRetrieval = "Error getting HID device info."
    errorMultipleDevices = "Multiple devices found. Don't know which to use."
    errorInvalidDataIndex = "Found data index not defined as button or control value."
    vendorID = "Vendor ID "
    enteredLowPower = "%s entered low-power mode"
    exitedLowPower = "%s exited low-power mode"

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
VERSION_NUMBER= 5
BLUETOOTH_ADDRESS = 6
BLUETOOTH_LINK_MODE = MAX_INDEX = 7

#link mode
(
    LINK_MODE_NORMAL,
    LINK_MODE_HOLD,
    LINK_MODE_SNIFF,
    LINK_MODE_PARK,
) = xrange(4)

# See if we've got widcomm - if not, we won't be changing the link mode
ALLOW_CANCEL_SNIFF = True

try:
    widcommDLL = ctypes.cdll.widcommsdk
except WindowsError:
    widcommDLL = None
else:
    IsStackServerUp = getattr(widcommDLL, '?IsStackServerUp@CBtIf@@QAEHXZ')
    IsStackServerUp.restype = BOOL

    if not IsStackServerUp():
        widcommDLL = None

if widcommDLL is None:

    def set_sniff_mode(bd_addr):
        return False

    def cancel_sniff_mode(bd_addr):
        return False

    def read_link_mode(bd_addr):
        return None

else:
    SetSniffMode = getattr(widcommDLL, '?SetSniffMode@CBtIf@@SAHQAE@Z')
    SetSniffMode.restype = BOOL
    CancelSniffMode = getattr(widcommDLL, '?CancelSniffMode@CBtIf@@SAHQAE@Z')
    CancelSniffMode.restype = BOOL
    ReadLinkMode = getattr(widcommDLL, '?ReadLinkMode@CBtIf@@SAHQAEPAE@Z')
    ReadLinkMode.restype = BOOLEAN

    def set_sniff_mode(bd_addr):
        result = SetSniffMode(bd_addr)
        return bool(result)

    def cancel_sniff_mode(bd_addr):
        if ALLOW_CANCEL_SNIFF:            
            result = CancelSniffMode(bd_addr)
            return bool(result)

        return False

    def read_link_mode(bd_addr):
        mode = c_ubyte(0)
        result = ReadLinkMode(bd_addr, byref(mode))

        if result:
            return mode.value
        
        return None

def check_link_mode_sniff(device):
    if device is None:
        return

    mode = read_link_mode(device[BLUETOOTH_ADDRESS])

    if mode == LINK_MODE_SNIFF and mode != device[BLUETOOTH_LINK_MODE]:
        device[BLUETOOTH_LINK_MODE] = mode
        print Text.enteredLowPower % (device_name(device),)

def check_link_mode_no_sniff(device):
    if device is None:
        return

    mode = read_link_mode(device[BLUETOOTH_ADDRESS])

    if mode == LINK_MODE_NORMAL and mode != device[BLUETOOTH_LINK_MODE]:
        device[BLUETOOTH_LINK_MODE] = mode
        print Text.exitedLowPower % (device_name(device),)

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
        hidDLL = ctypes.windll.hid

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
                regkey = "SYSTEM\\CurrentControlSet\\Enum\\" + devicePathSplit[0] + \
                    "\\" + devicePathSplit[1] + "\\" + devicePathSplit[2]
                regHandle = _winreg.OpenKey( _winreg.HKEY_LOCAL_MACHINE, regkey)
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

        # try to find Bluetooth device IDs
        self.findBluetoothDeviceIds(self.deviceList)

    def findBluetoothDeviceIds(self, deviceList):
        # try to find Bluetooth device ID - we'll check the Widcomm section of the registry
        regkey = "SYSTEM\\CurrentControlSet\\Enum\\{95C7A0A0-3094-11D7-A202-00508B9D7D5A}"
        mapping = self.findBluetoothDeviceIdNameMapping(regkey)

        for d in deviceList:
            devicePathSplit = d[DEVICE_PATH][4:].split("#")
            parentId = devicePathSplit[2]

            for parentIdPrefix in mapping:
                if parentId.startswith(parentIdPrefix):
                    d[BLUETOOTH_ADDRESS] = mapping[parentIdPrefix]
                    d[BLUETOOTH_LINK_MODE] = read_link_mode(d[BLUETOOTH_ADDRESS])
                    break
            else:
                d[BLUETOOTH_ADDRESS] = None
                d[BLUETOOTH_LINK_MODE] = None

    def findBluetoothDeviceIdNameMapping(self, regkey, stack=None, mapping=None):
        # iterate through all the subkeys, looking for the 'ParentIdPrefix' and 'BdAddr'
        # values. 'LocationInformation' will match the PRODUCT_STRING above.
        if stack is None:
            stack = []

        if mapping is None:
            mapping = {}

        appended_parent = False
        try:
            regHandle = _winreg.OpenKey( _winreg.HKEY_LOCAL_MACHINE, regkey)
        except WindowsError:
            return mapping

        try:
            parentIdPrefix, regType = _winreg.QueryValueEx(regHandle, "ParentIdPrefix")
            stack.append(parentIdPrefix)
            appended_parent = True
        except EnvironmentError:
            pass

        try:
            bdaddr, regType = _winreg.QueryValueEx(regHandle, "BdAddr")

            if stack:
                mapping[stack[-1]] = bdaddr
                
        except EnvironmentError:
            pass

        subkeys = []

        try:
            for i in itertools.count(0):
                subkeys.append(_winreg.EnumKey(regHandle, i))
        except EnvironmentError:
            pass

        _winreg.CloseKey(regHandle)

        for k in subkeys:
            subkey = regkey + '\\' + k
            self.findBluetoothDeviceIdNameMapping(subkey, stack, mapping)

        if appended_parent:
            stack.pop()

        return mapping

    def _get_device(self,
        noOtherPort,
        devicePath,
        vendorID,
        productID,
        versionNumber
    ):
        found = 0
        path = ""
        for item in self.deviceList:
            if noOtherPort:
                #just search for devicepath
                if item[DEVICE_PATH] == devicePath:
                    #found right device
                    return item
            else:
                #find the right vendor and product ids
                if item[VENDOR_ID] == vendorID \
                    and item[PRODUCT_ID] == productID \
                    and item[VERSION_NUMBER] == versionNumber:
                    found = found + 1
                    if item[DEVICE_PATH] == devicePath:
                        #found right device
                        return item

        if found == 1:
            return item

        #multiple devices found
        #don't know which to use
        if found > 1:
            eg.PrintError(self.text.errorMultipleDevices)

        return None

    #gets the devicePath
    #the devicePath parameter is only used with multiple same devices
    def GetDevicePath(self,
        noOtherPort,
        devicePath,
        vendorID,
        productID,
        versionNumber
    ):
        device = self._get_device(noOtherPort, devicePath, vendorID, productID, versionNumber)

        if device is None:
            return None

        return device[DEVICE_PATH]

    #gets the device bluetooth address
    #the devicePath parameter is only used with multiple same devices
    def GetDeviceBTAddress(self,
        noOtherPort,
        devicePath,
        vendorID,
        productID,
        versionNumber
    ):
        device = self._get_device(noOtherPort, devicePath, vendorID, productID, versionNumber)

        if device is None:
            return None

        return device[BLUETOOTH_ADDRESS]


class TimerThread(threading.Thread):

    def __init__(self,
        plugin,
        name,
        interval,
        prefix,
        evtName,
    ):
        self.start_time = time.time()
        self.plugin = plugin
        self.name = name
        self.interval = interval
        self.prefix = prefix
        self.evtName = evtName

        threading.Thread.__init__(self, name = name)

        self.finished = threading.Event()
        self.abort = False

    def run(self):
        now = time.time()
        elapsed = now - self.start_time
        remaining = max(0, min(self.interval, self.interval - elapsed))
        self.finished.wait(remaining)
        self.finished.clear()

        if not self.abort:
            eg.TriggerEvent(self.evtName, prefix = self.prefix)

    def stop(self):
        self.abort = True
        self.finished.set()



DEVICE = None

class HIDThread(threading.Thread):

    def __init__(self,
        plugin,
        helper,
        enduringEvents,
        rawDataEvents,
        ps3DataEvents,
        ps3Release,
        ps3Zone,
        shortKeyTime,
        longKeyTime,
        sleepTime,
        hibernateTime,
        noOtherPort,
        devicePath,
        vendorID,
        vendorString,
        productID,
        productString,
        versionNumber,
    ):
        self.ps3Remote = Ps3Remote
        self.text = Text
        self.deviceName = vendorString + " " + productString
        self.abort = False
        self._overlappedRead = win32file.OVERLAPPED()
        self._overlappedRead.hEvent = win32event.CreateEvent(None, 1, 0, None)

        self.evtName = "None"
        self.zoneName = "None"
        self.maskRegularEvent = False
        self.regularEvent = False
        self.Started = True
        self.timeStarted = time.time()

        #getting devicePath
        self.devicePath = helper.GetDevicePath(
            noOtherPort,
            devicePath,
            vendorID,
            productID,
            versionNumber
        )

        if not self.devicePath:
            self.stop_enduring_event()
            eg.PrintError(self.text.errorFind + self.deviceName)
            return

        threading.Thread.__init__(self, name = self.devicePath)

        #setting members
        self.plugin = plugin
        self.helper = helper
        self.enduringEvents = enduringEvents
        self.rawDataEvents = rawDataEvents
        self.ps3DataEvents = ps3DataEvents
        self.ps3Release = ps3Release
        self.ps3Zone = ps3Zone
        self.shortKeyTime = shortKeyTime
        self.longKeyTime = longKeyTime
        self.sleepTime = sleepTime
        self.hibernateTime = hibernateTime

        global DEVICE
        DEVICE = helper._get_device(
            noOtherPort,
            devicePath,
            vendorID,
            productID,
            versionNumber
        )

        self.bdAddr = DEVICE[BLUETOOTH_ADDRESS]
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
            self.stop_enduring_event()
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
                self.stop_enduring_event()
                eg.PrintError(self.text.errorRead + self.deviceName)
                self.abort = True

            #parse data
            if len(buf) == n and not self.abort:
                #raw data events
                if self.ps3DataEvents:
                    read = str(buf)
                    keycode = binascii.hexlify(read).upper()[2:22]

                    try:
                        evtName = self.ps3Remote.button[keycode]
                        zoneName = self.ps3Remote.zone[keycode]
                        regularEvent = True
                    except KeyError:
                        evtName = keycode
                        zoneName = "Extended"
                        regularEvent = False

                    # Make sure any time we get a keypress, we come out of low-power mode
                    cancel_sniff_mode(self.bdAddr)

                    if result:
                        eg.scheduler.AddTask(1.0, check_link_mode_no_sniff, DEVICE)

                    if self.enduringEvents:
                        self.stop_enduring_event()                        
                        prefix = self.plugin.info.eventPrefix

                        currentTime = time.time()
                        elapsedTime = currentTime - self.timeStarted
                        self.timeStarted = time.time()

                        if self.Started:
                            if not self.regularEvent or evtName == "Release":
                                if elapsedTime < self.shortKeyTime:
                                    self.plugin.TriggerEvent(self.evtName + ".S")
                            self.Started = False

                        if evtName == "Release":
                            if self.sleepTime > 0:
                                self.Timer2 = TimerThread(self.plugin, "Timer2", self.sleepTime, prefix, "Sleep")
                                self.Timer2.start()
                            if self.hibernateTime > 0:
                                self.Timer3 = TimerThread(self.plugin, "Timer3", self.hibernateTime, prefix, "Hibernate")
                                self.Timer3.start()
                            if self.ps3Release:
                                self.plugin.TriggerEvent(evtName)
                            self.maskRegularEvent = False
                        else:
                            if not self.maskRegularEvent or not regularEvent:
                                if elapsedTime > self.sleepTime and self.sleepTime > 0:
                                    self.plugin.TriggerEvent("WakeUp")
                                    self.zoneName = "None"
                                if self.ps3Zone and self.zoneName != zoneName and zoneName != "none":
                                    self.plugin.TriggerEvent(zoneName)
                                self.plugin.TriggerEnduringEvent(evtName)
                                if elapsedTime < self.shortKeyTime and evtName == self.evtName:
                                    self.Timer1 = TimerThread(self.plugin, "Timer1", self.longKeyTime, prefix, evtName + ".M")
                                    self.Timer1.start()
                                    eg.TriggerEvent(evtName + ".D", prefix = prefix)
                                else:
                                    self.Timer1 = TimerThread(self.plugin, "Timer1", self.longKeyTime, prefix, evtName + ".L")
                                    self.Timer1.start()
                                    self.Started = True
                                self.evtName = evtName
                                self.zoneName = zoneName
                                self.regularEvent = regularEvent

                            if not regularEvent:
                                self.maskRegularEvent = True

                    else:
                        self.plugin.TriggerEvent(evtName)


                elif maxDataL == 0 or self.rawDataEvents:
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
            self.stop_enduring_event()

        win32file.CloseHandle(handle)

        #free references
        hidDLL.HidD_FreePreparsedData(ctypes.byref(preparsedData))

        #HID thread finished

    def stop_enduring_event(self):
        try:
            enduringEvents = self.enduringEvents
        except AttributeError:
            enduringEvents = False

        if enduringEvents:
            try:
                if self.Timer1.isAlive():
                    self.Timer1.stop()
            except AttributeError:
                pass
            else:
                del self.Timer1

            try:
                if self.Timer2.isAlive():
                    self.Timer2.stop()
            except AttributeError:
                pass
            else:
                del self.Timer2

            try:
                if self.Timer3.isAlive():
                    self.Timer3.stop()
            except AttributeError:
                pass
            else:
                del self.Timer3

            self.plugin.EndLastEvent()

def device_name(device):
    return device[VENDOR_STRING] + " " + device[PRODUCT_STRING]

def handle_wake_up(event):
    global ALLOW_CANCEL_SNIFF

    if event.string == 'System.Resume':
        ALLOW_CANCEL_SNIFF = True

    device = DEVICE

    if device is None:
        return

    bd_addr = device[BLUETOOTH_ADDRESS]
    result = cancel_sniff_mode(bd_addr)

    if result:
        eg.scheduler.AddTask(1.0, check_link_mode_no_sniff, DEVICE)

def handle_sleep(event):
    device = DEVICE

    if device is None:
        return

    bd_addr = device[BLUETOOTH_ADDRESS]
    result = set_sniff_mode(bd_addr)

    if result:
        eg.scheduler.AddTask(1.0, check_link_mode_sniff, DEVICE)

def handle_init(event):
    # Put the PS3 remote to sleep if it isn't already
    handle_sleep(event)

def handle_machine_sleep(event):
    global ALLOW_CANCEL_SNIFF

    if event.string == 'System.Suspend':
        ALLOW_CANCEL_SNIFF = False

    return handle_sleep(event)

INSTANCE = None

def handle_device_attached(event):
    instance = INSTANCE

    if not isinstance(instance, PS3):
        return

    eg.actionThread.Call(instance.__stop__)
    eg.actionThread.Call(instance.__start__, *instance.args)

class PS3(eg.PluginClass):
    helper = None
    text = Text
    thread = None

    def __start__(self, *args):
        global INSTANCE
        INSTANCE = self

        # We store the arguments away so that we can use them again later (i.e. when we resume
        # from standby and need to restart ourself).
        self.args = args
        self.__start(*args)

    def __start(self,
        eventName,
        enduringEvents,
        rawDataEvents,
        ps3DataEvents,
        ps3Release,
        ps3Zone,
        shortKeyTime,
        longKeyTime,
        sleepTime,
        hibernateTime,
        noOtherPort,
        devicePath,
        vendorID,
        vendorString,
        productID,
        productString,
        versionNumber,

        # For backwards-compatibility with 2.0.2 and 3.0.0 - if a new config option is added this can just be replaced
        dummy=None
    ):

        # Set up bindings to ensure that we handle power states, etc correctly.
        eg.Bind('Main.OnInit', handle_init)

        eg.Bind('HID.WakeUp', handle_wake_up)
        eg.Bind('System.Resume', handle_wake_up)

        eg.Bind('HID.Hibernate', handle_sleep)
        eg.Bind('System.QuerySuspend', handle_machine_sleep)
        eg.Bind('System.Suspend', handle_machine_sleep)

        # If we get one of these, we __stop__ and __start__ the plugin so that we
        # pick up the device (if necessary).
        eg.Bind('System.DeviceAttached', handle_device_attached)

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
        self.thread = HIDThread(self,
            self.helper,
            enduringEvents,
            rawDataEvents,
            ps3DataEvents,
            ps3Release,
            ps3Zone,
            shortKeyTime,
            longKeyTime,
            sleepTime,
            hibernateTime,
            noOtherPort,
            devicePath,
            vendorID,
            vendorString,
            productID,
            productString,
            versionNumber
        )

    def __stop__(self):
        global INSTANCE
        INSTANCE = None

        self.thread.AbortThread()

        eg.Unbind('Main.OnInit', handle_init)

        eg.Unbind('HID.Hibernate', handle_sleep)
        eg.Unbind('System.QuerySuspend', handle_machine_sleep)
        eg.Unbind('System.Suspend', handle_machine_sleep)

        eg.Unbind('HID.Wake', handle_wake_up)
        eg.Unbind('System.Resume', handle_wake_up)

        eg.Unbind('System.DeviceAttached', handle_device_attached)

    def Configure(self,
        eventName = "",
        enduringEvents = True,
        rawDataEvents = False,
        ps3DataEvents = False,
        ps3Release = False,
        ps3Zone = False,
        shortKeyTime = 0.3,
        longKeyTime = 0.5,
        sleepTime = 5.0,
        hibernateTime = 60.0,
        noOtherPort = False,
        devicePath = None,
        vendorID = None,
        vendorString = None,
        productID = None,
        productString = None,
        versionNumber = None,

        # For backwards-compatibility with 2.0.2 and 3.0.0 - if a new config option is added this can just be replaced
        dummy=None
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
            if not devicePath:
                #just select first entry on first start
                hidList.Select(0)
            else:
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

        panel.sizer.Add((15,15))

        #sizers
        eventsGroupSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, self.text.eventsSettings),
            wx.VERTICAL
        )

        eventsSizer = wx.GridBagSizer(0, 5)

        #eventname
        eventsSizer.Add(
            wx.StaticText(panel, -1, self.text.eventName),
            (0, 0),
            flag = wx.ALIGN_CENTER_VERTICAL)
        eventNameCtrl = wx.TextCtrl(panel, value = eventName)
        eventNameCtrl.SetMaxLength(32)
        eventsSizer.Add(eventNameCtrl, (0, 1), (1, 2), flag = wx.EXPAND)

        #checkbox for no other port option
        noOtherPortCtrl = wx.CheckBox(panel, -1, self.text.noOtherPort)
        noOtherPortCtrl.SetValue(noOtherPort)
        eventsSizer.Add(noOtherPortCtrl, (1, 0), (1, 3))

        #checkbox for enduring event option
        enduringEventsCtrl = wx.CheckBox(panel, -1, self.text.enduringEvents)
        enduringEventsCtrl.SetValue(enduringEvents)
        eventsSizer.Add(enduringEventsCtrl, (2, 0), (1, 3))

        #checkbox for raw data events
        rawDataEventsCtrl = wx.CheckBox(panel, -1, self.text.rawDataEvents)
        rawDataEventsCtrl.SetValue(rawDataEvents)
        eventsSizer.Add(rawDataEventsCtrl, (3, 0), (1, 3))

        eventsGroupSizer.Add(eventsSizer, 0, wx.ALL, 10)
        panel.sizer.Add(eventsGroupSizer, 0, wx.EXPAND)


        panel.sizer.Add((15,15))

        #sizers
        ps3GroupSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, self.text.ps3Settings),
            wx.VERTICAL
        )

        ps3Sizer = wx.GridBagSizer(0, 5)

        #checkbox for ps3 data events
        ps3DataEventsCtrl = wx.CheckBox(panel, -1, self.text.ps3DataEvents)
        ps3DataEventsCtrl.SetValue(ps3DataEvents)
        ps3Sizer.Add(ps3DataEventsCtrl, (0, 0), (1, 3))

        #checkbox for ps3 release event
        ps3ReleaseCtrl = wx.CheckBox(panel, -1, self.text.ps3Release)
        ps3ReleaseCtrl.SetValue(ps3Release)
        ps3Sizer.Add(ps3ReleaseCtrl, (1, 0), (1, 3))

        #checkbox for ps3 zone event
        ps3ZoneCtrl = wx.CheckBox(panel, -1, self.text.ps3Zone)
        ps3ZoneCtrl.SetValue(ps3Zone)
        ps3Sizer.Add(ps3ZoneCtrl, (2, 0), (1, 3))

        #short key time
        ps3Sizer.Add(
            wx.StaticText(panel, -1, self.text.shortKeyTime),
            (3, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        shortKeyTimeCtrl = eg.SpinNumCtrl(
            panel, -1, shortKeyTime, size=(200,-1), integerWidth=7, increment=0.05
        )
        ps3Sizer.Add(shortKeyTimeCtrl, (3, 1), flag = wx.EXPAND)
        ps3Sizer.Add(
            wx.StaticText(panel, -1, self.text.seconds),
            (3, 2), (1, 2),
            flag = wx.ALIGN_CENTER_VERTICAL)

        #long key time
        ps3Sizer.Add(
            wx.StaticText(panel, -1, self.text.longKeyTime),
            (4, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        longKeyTimeCtrl = eg.SpinNumCtrl(
            panel, -1, longKeyTime, size=(200,-1), integerWidth=7, increment=0.05
        )
        ps3Sizer.Add(longKeyTimeCtrl, (4, 1), flag = wx.EXPAND)
        ps3Sizer.Add(
            wx.StaticText(panel, -1, self.text.seconds),
            (4, 2), (1, 2),
            flag = wx.ALIGN_CENTER_VERTICAL)

        #sleep time
        ps3Sizer.Add(
            wx.StaticText(panel, -1, self.text.sleepTime),
            (5, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        sleepTimeCtrl = eg.SpinNumCtrl(
            panel, -1, sleepTime, size=(200,-1), integerWidth=7, increment=1.00
        )
        ps3Sizer.Add(sleepTimeCtrl, (5, 1), flag = wx.EXPAND)
        ps3Sizer.Add(
            wx.StaticText(panel, -1, self.text.seconds),
            (5, 2), (1, 2),
            flag = wx.ALIGN_CENTER_VERTICAL)

        #hibernate time
        ps3Sizer.Add(
            wx.StaticText(panel, -1, self.text.hibernateTime),
            (6, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        hibernateTimeCtrl = eg.SpinNumCtrl(
            panel, -1, hibernateTime, size=(200,-1), integerWidth=7, increment=1.00
        )
        ps3Sizer.Add(hibernateTimeCtrl, (6, 1), flag = wx.EXPAND)
        ps3Sizer.Add(
            wx.StaticText(panel, -1, self.text.seconds),
            (6, 2), (1, 2),
            flag = wx.ALIGN_CENTER_VERTICAL)


        ps3GroupSizer.Add(ps3Sizer, 0, wx.ALL, 10)
        panel.sizer.Add(ps3GroupSizer, 0, wx.EXPAND)


        def OnHidListSelect(event):
            panel.dialog.buttonRow.okButton.Enable(True)
            panel.dialog.buttonRow.applyButton.Enable(True)
            event.Skip()

        def OnRawDataEventsChange(event):
            enduringEventsCtrl.Enable(not rawDataEventsCtrl.GetValue())
            ps3DataEventsCtrl.Enable(not rawDataEventsCtrl.GetValue())
            event.Skip()

        def OnEnduringEventsChange(event):
            rawDataEventsCtrl.Enable(not enduringEventsCtrl.GetValue())
            ps3ReleaseCtrl.Enable(enduringEventsCtrl.GetValue() and ps3DataEventsCtrl.GetValue())
            ps3ZoneCtrl.Enable(enduringEventsCtrl.GetValue() and ps3DataEventsCtrl.GetValue())
            event.Skip()

        def OnPs3DataEventsChange(event):
            rawDataEventsCtrl.Enable(not ps3DataEventsCtrl.GetValue())
            ps3ReleaseCtrl.Enable(enduringEventsCtrl.GetValue() and ps3DataEventsCtrl.GetValue())
            ps3ZoneCtrl.Enable(enduringEventsCtrl.GetValue() and ps3DataEventsCtrl.GetValue())
            event.Skip()

        def OnPs3ReleaseChange(event):
            rawDataEventsCtrl.Enable(not ps3DataEventsCtrl.GetValue())
            event.Skip()

        def OnPs3ZoneChange(event):
            rawDataEventsCtrl.Enable(not ps3DataEventsCtrl.GetValue())
            event.Skip()

        OnRawDataEventsChange(wx.CommandEvent())
        OnPs3DataEventsChange(wx.CommandEvent())
        OnPs3ReleaseChange(wx.CommandEvent())
        OnPs3ZoneChange(wx.CommandEvent())
        OnEnduringEventsChange(wx.CommandEvent())

        rawDataEventsCtrl.Bind(wx.EVT_CHECKBOX, OnRawDataEventsChange)
        ps3DataEventsCtrl.Bind(wx.EVT_CHECKBOX, OnPs3DataEventsChange)
        ps3ReleaseCtrl.Bind(wx.EVT_CHECKBOX, OnPs3ReleaseChange)
        ps3ZoneCtrl.Bind(wx.EVT_CHECKBOX, OnPs3ZoneChange)
        enduringEventsCtrl.Bind(wx.EVT_CHECKBOX, OnEnduringEventsChange)
        hidList.Bind(wx.EVT_LIST_ITEM_SELECTED, OnHidListSelect)
        
        while panel.Affirmed():
            device = devices[hidList.GetFirstSelected()]
                
            panel.SetResult(
                eventNameCtrl.GetValue(),
                enduringEventsCtrl.GetValue(),
                rawDataEventsCtrl.GetValue(),
                ps3DataEventsCtrl.GetValue(),
                ps3ReleaseCtrl.GetValue(),
                ps3ZoneCtrl.GetValue(),
                shortKeyTimeCtrl.GetValue(),
                longKeyTimeCtrl.GetValue(),
                sleepTimeCtrl.GetValue(),
                hibernateTimeCtrl.GetValue(),
                noOtherPortCtrl.GetValue(),
                device[DEVICE_PATH],
                device[VENDOR_ID],
                device[VENDOR_STRING],
                device[PRODUCT_ID],
                device[PRODUCT_STRING],
                device[VERSION_NUMBER]
            )

