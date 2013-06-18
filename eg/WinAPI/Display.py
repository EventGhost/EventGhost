import win32con
from win32types import *


ENUM_CURRENT_SETTINGS = 0xFFFFFFFE
EDS_RAWMODE = 2

TCHAR = c_char
INDENT = "    "

def dumps(obj, name=None, indent=""):
    res = []
    append = res.append
    if name is None:
        name = obj.__class__.__name__
    #append(indent + obj.__class__.__bases__[0].__name__ + " ")
    append(name + "(\n")
    bitfields = getattr(obj, "_" + obj.__class__.__name__ + "__bitfields", ())
    bitfieldnames = [name for name, values in bitfields]
    
    for name, cType in obj._fields_:
        if issubclass(cType, (Union, Structure)):
            append(indent + INDENT + name + " = ")
            append(dumps(getattr(obj, name), indent=indent + INDENT))
            append(",\n")
        elif name in bitfieldnames:
            append(indent + INDENT + name + " = ")
            flags = getattr(obj, name)
            flagNames = []
            for name, mask in bitfields[bitfieldnames.index(name)][1]:
                mask = getattr(win32con, name)
                if flags & mask:
                    flags &= ~mask
                    flagNames.append(name)
            append(" | ".join(flagNames))
            if flags:
                append("<unknown %i>" % flags)
            append(",\n")
        else:
            append(indent + INDENT + name + " = " + repr(getattr(obj, name)) + ",\n")
    append(indent + ")")
    return "".join(res)
        
        
def dump(obj, name=None):
    print dumps(obj, name)
    


class DISPLAY_DEVICE(Structure):
    __bitfields = (
        (
            "StateFlags", 
            (
                ("DISPLAY_DEVICE_ATTACHED_TO_DESKTOP", win32con.DISPLAY_DEVICE_ATTACHED_TO_DESKTOP),
                ("DISPLAY_DEVICE_MIRRORING_DRIVER", win32con.DISPLAY_DEVICE_MIRRORING_DRIVER),
                ("DISPLAY_DEVICE_MODESPRUNED", win32con.DISPLAY_DEVICE_MODESPRUNED),
                ("DISPLAY_DEVICE_PRIMARY_DEVICE", win32con.DISPLAY_DEVICE_PRIMARY_DEVICE),
                ("DISPLAY_DEVICE_REMOVABLE", win32con.DISPLAY_DEVICE_REMOVABLE),
                ("DISPLAY_DEVICE_VGA_COMPATIBLE", win32con.DISPLAY_DEVICE_VGA_COMPATIBLE),
            )
        ),
    )
    
    _fields_ = [
        ('cb', DWORD),
        ('DeviceName', TCHAR * 32),
        ('DeviceString', TCHAR * 128),
        ('StateFlags', DWORD),
        ('DeviceID', TCHAR * 128),
        ('DeviceKey', TCHAR * 128),
    ]
    
    def __init__(self):
        self.cb = sizeof(DISPLAY_DEVICE)
        
    
PDISPLAY_DEVICE = POINTER(DISPLAY_DEVICE)

class DEVMODE(Structure): 
    class _U1(Union):
        class _U1A(Structure):
            _fields_ = [
                ("dmOrientation", c_short), 
                ("dmPaperSize", c_short), 
                ("dmPaperLength", c_short), 
                ("dmPaperWidth", c_short), 
                ("dmScale", c_short), 
                ("dmCopies", c_short), 
                ("dmDefaultSource", c_short), 
                ("dmPrintQuality", c_short), 
            ]

        class _U1B(Structure):
            _fields_ = [
                ("x", c_long), 
                ("y", c_long), 
            ]

        _fields_ = [
            ("printer", _U1A), 
            ("dmPosition", _U1B), 
        ]

    _anonymous_ = ("union1", )
    
    _fields_ = [
        ("dmDeviceName", c_char * 32), 
        ("dmSpecVersion", c_short), 
        ("dmDriverVersion", c_short), 
        ("dmSize", c_short), 
        ("dmDriverExtra", c_short), 
        ("dmFields", DWORD), 
        ("union1", _U1),
        ("dmColor", c_short), 
        ("dmDuplex", c_short), 
        ("dmYResolution", c_short), 
        ("dmTTOption", c_short), 
        ("dmCollate", c_short), 
        ("dmFormName", c_char * 32), 
        ("dmLogPixels", WORD), 
        ("dmBitsPerPel", DWORD), 
        ("dmPelsWidth", DWORD), 
        ("dmPelsHeight", DWORD), 
        ("dmDisplayFlags", DWORD), 
        ("dmDisplayFrequency", DWORD), 
        ("dmDriverExtraData", c_char * 1024),
    ]

    __bitfields = (
        (
            "dmFields", 
            (
                ("DM_ORIENTATION", win32con.DM_ORIENTATION),
                ("DM_PAPERSIZE", win32con.DM_PAPERSIZE),
                ("DM_PAPERLENGTH", win32con.DM_PAPERLENGTH),
                ("DM_PAPERWIDTH", win32con.DM_PAPERWIDTH),
                ("DM_SCALE", win32con.DM_SCALE),
                ("DM_COPIES", win32con.DM_COPIES),
                ("DM_DEFAULTSOURCE", win32con.DM_DEFAULTSOURCE),
                ("DM_PRINTQUALITY", win32con.DM_PRINTQUALITY),
                ("DM_POSITION", win32con.DM_POSITION),
                ("DM_DISPLAYORIENTATION", win32con.DM_DISPLAYORIENTATION),
                ("DM_DISPLAYFIXEDOUTPUT", win32con.DM_DISPLAYFIXEDOUTPUT),
                ("DM_COLOR", win32con.DM_COLOR),
                ("DM_DUPLEX", win32con.DM_DUPLEX),
                ("DM_YRESOLUTION", win32con.DM_YRESOLUTION),
                ("DM_COLLATE", win32con.DM_COLLATE),
                ("DM_FORMNAME", win32con.DM_FORMNAME),
                ("DM_LOGPIXELS", win32con.DM_LOGPIXELS),
                ("DM_BITSPERPEL", win32con.DM_BITSPERPEL),
                ("DM_PELSWIDTH", win32con.DM_PELSWIDTH),
                ("DM_PELSHEIGHT", win32con.DM_PELSHEIGHT),
                ("DM_DISPLAYFLAGS", win32con.DM_DISPLAYFLAGS),
                ("DM_NUP", win32con.DM_NUP),
                ("DM_DISPLAYFREQUENCY", win32con.DM_DISPLAYFREQUENCY),
                ("DM_ICMMETHOD", win32con.DM_ICMMETHOD),
                ("DM_ICMINTENT", win32con.DM_ICMINTENT),
                ("DM_MEDIATYPE", win32con.DM_MEDIATYPE),
                ("DM_DITHERTYPE", win32con.DM_DITHERTYPE),
                ("DM_PANNINGWIDTH", win32con.DM_PANNINGWIDTH),
                ("DM_PANNINGHEIGHT", win32con.DM_PANNINGHEIGHT),
            )
        ),
    )
    
    def __init__(self):
        self.dmSize = sizeof(DEVMODE) - 1024
        self.dmDriverExtra = 1024
        
        
user32 = windll.User32
EnumDisplayDevices = user32.EnumDisplayDevicesA
EnumDisplaySettingsEx = user32.EnumDisplaySettingsExA
ChangeDisplaySettingsEx = user32.ChangeDisplaySettingsExA


class Display(object):
    
    def __init__(self, iDevNum, displayDeviceStruct):
        self.iDevNum = iDevNum
        self.displayDeviceStruct = displayDeviceStruct
        self.DeviceName = displayDeviceStruct.DeviceName
        self.DeviceString = displayDeviceStruct.DeviceString
        self.isPrimary = bool(displayDeviceStruct.StateFlags & win32con.DISPLAY_DEVICE_PRIMARY_DEVICE)
        self.dm = DEVMODE()
        self.dmp = pointer(self.dm)
        self.lpszDeviceName = c_char_p.from_param(self.DeviceName)
    
    
    def Refresh(self):
        name = self.lpszDeviceName
        dmp = self.dmp
        EnumDisplaySettingsEx(name, 0, dmp, 0)
        EnumDisplaySettingsEx(name, ENUM_CURRENT_SETTINGS, dmp, 0)
        dm = self.dm
        self.x = dm.dmPosition.x
        self.y = dm.dmPosition.y
        self.width = dm.dmPelsWidth
        self.height = dm.dmPelsHeight
        self.frequency = dm.dmDisplayFrequency
        self.bitsPerPixel = dm.dmBitsPerPel        
    
    
    def Serialize(self):
        dmp = self.dmp
        EnumDisplaySettingsEx(self.lpszDeviceName, ENUM_CURRENT_SETTINGS, dmp, 0)
        dm = self.dm
        return (
            self.DeviceName,
            dm.dmPosition.x,
            dm.dmPosition.y,
            dm.dmPelsWidth,
            dm.dmPelsHeight,
            dm.dmDisplayFrequency,
            dm.dmBitsPerPel,
            bool(self.displayDeviceStruct.StateFlags & win32con.DISPLAY_DEVICE_ATTACHED_TO_DESKTOP),
            bool(self.displayDeviceStruct.StateFlags & win32con.DISPLAY_DEVICE_PRIMARY_DEVICE),
        )
            
            
    def GetDisplayModes(self, all=False):
        name = c_char_p.from_param(self.DeviceName)
        dm = DEVMODE()
        dmp = pointer(dm)
        modes = {}
        if all:
            flag = EDS_RAWMODE
        else:
            flag = 0
        iModeNum = 0
        while 0 != EnumDisplaySettingsEx(name, iModeNum, dmp, flag):
            iModeNum += 1
            resolution = (dm.dmPelsWidth, dm.dmPelsHeight)
            deepth_dict = modes.setdefault(resolution, {})
            frequency_list = deepth_dict.setdefault(dm.dmBitsPerPel, [])
            frequency_list.append(dm.dmDisplayFrequency)
        return modes


    def SetDisplayMode(self, size, frequency, bitdepth, flags=0):
        dm = DEVMODE()
        dm.dmPelsWidth = size[0]
        dm.dmPelsHeight = size[1]
        dm.dmBitsPerPel = bitdepth
        dm.dmDisplayFrequency = frequency
        dm.dmFields = (
            win32con.DM_BITSPERPEL
            |win32con.DM_PELSWIDTH
            |win32con.DM_PELSHEIGHT
            |win32con.DM_DISPLAYFREQUENCY
        )
        ChangeDisplaySettingsEx(self.lpszDeviceName, pointer(dm), 0, flags, 0)


    def Detach(self):
        dm = DEVMODE()
        dm.dmFields = (
            win32con.DM_PELSWIDTH 
            | win32con.DM_PELSHEIGHT 
            | win32con.DM_BITSPERPEL 
            | win32con.DM_POSITION
            | win32con.DM_DISPLAYFREQUENCY
            | win32con.DM_DISPLAYFLAGS
        )
        ChangeDisplaySettingsEx(
            self.lpszDeviceName, 
            pointer(dm), 
            0, 
            win32con.CDS_UPDATEREGISTRY, 
            0
        )
        
        
    def SetPrimary(self):
        self.isPrimary = True
        dm = DEVMODE()
        dm.dmPosition.x = 0
        dm.dmPosition.y = 0
        dm.dmFields = win32con.DM_POSITION
        ret = ChangeDisplaySettingsEx(
            self.lpszDeviceName, 
            pointer(dm), 
            0, 
            win32con.CDS_UPDATEREGISTRY, 
            0
        )
        return ret
    
    
    def GetCurrentMode(self):
        self.Refresh()
        return (
            (self.width, self.height),
            self.frequency, 
            self.bitsPerPixel
        )
        
        
    def GetRectangle(self):
        """
        Returns the displays position and size as a tuple.
        
        The fields are: (left, top, width, height)
        """
        self.Refresh()
        return (
            self.x,
            self.y,
            self.width,
            self.height,
        )
        
        
def GetDisplays():
    res = []
    displayDevice = DISPLAY_DEVICE()
    iDevNum = 0
    while True:
        if EnumDisplayDevices(0, iDevNum, pointer(displayDevice), 0) == 0:
            break
        #DISPLAY_DEVICE_ATTACHED_TO_DESKTOP = 1
        if not (displayDevice.StateFlags & win32con.DISPLAY_DEVICE_MIRRORING_DRIVER):
            disp = Display(iDevNum, displayDevice)
            res.append(disp)
            displayDevice = DISPLAY_DEVICE()
        iDevNum += 1
    return res


def GetDisplayModes(debug=False):
    res = []
    displayDevice = DISPLAY_DEVICE()
    devMode = DEVMODE()
    iDevNum = 0
    while True:
        if EnumDisplayDevices(0, iDevNum, pointer(displayDevice), 0) == 0:
            break
        iDevNum += 1
        if debug:
            dump(displayDevice)
        if displayDevice.StateFlags & win32con.DISPLAY_DEVICE_MIRRORING_DRIVER:
            continue
        EnumDisplaySettingsEx(
            displayDevice.DeviceName, 
            ENUM_CURRENT_SETTINGS, 
            pointer(devMode), 
            0
        )
        if debug:
            dump(devMode)
        res.append(
            (
                displayDevice.DeviceName,
                devMode.dmPosition.x,
                devMode.dmPosition.y,
                devMode.dmPelsWidth,
                devMode.dmPelsHeight,
                devMode.dmDisplayFrequency,
                devMode.dmBitsPerPel,
                bool(displayDevice.StateFlags & win32con.DISPLAY_DEVICE_ATTACHED_TO_DESKTOP),
                bool(displayDevice.StateFlags & win32con.DISPLAY_DEVICE_PRIMARY_DEVICE),
                devMode.dmDisplayFlags,
            )
        )
    return tuple(res)


def SetDisplayModes(*args):
    for (
        lpszDeviceName, 
        x, 
        y, 
        width, 
        height, 
        freq, 
        bitdepth, 
        isAttached, 
        isPrimary,
        displayFlags
    ) in args:
        devMode = DEVMODE()
        if isAttached:
            devMode.dmPosition.x = x
            devMode.dmPosition.y = y
            devMode.dmPelsWidth = width
            devMode.dmPelsHeight = height
            devMode.dmBitsPerPel = bitdepth
            devMode.dmDisplayFrequency = freq
            devMode.dmDisplayFlags = displayFlags
        devMode.dmFields = (
            win32con.DM_POSITION
            |win32con.DM_BITSPERPEL
            |win32con.DM_PELSWIDTH
            |win32con.DM_PELSHEIGHT
            |win32con.DM_DISPLAYFLAGS
            |win32con.DM_DISPLAYFREQUENCY
        )
        flags = (win32con.CDS_UPDATEREGISTRY | win32con.CDS_NORESET)
        if isPrimary:
            flags |= win32con.CDS_SET_PRIMARY
        ChangeDisplaySettingsEx(
            lpszDeviceName, 
            pointer(devMode), 
            0, 
            flags, 
            0
        )
    ChangeDisplaySettingsEx(0, 0, 0, 0, 0)          
    
    
if __name__ == "__main__":
    print GetDisplayModes(True)
