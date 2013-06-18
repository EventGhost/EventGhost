import eg
import wx
import os
from eg.WinAPI.Utils import GetNameOfPID
from eg.IconTools import GetIcon
from win32process import EnumProcesses
from win32gui import EnumWindows
from win32process import GetWindowThreadProcessId
from eg.WinAPI.Utils import GetHwndIcon
import ctypes

class TestListCtrl(wx.ListCtrl, wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin.__init__(self)

import win32api
ourProcessID = win32api.GetCurrentProcessId()

class KillApplication(eg.ActionClass):
    name = "Kill Application"
    
    def __call__(self, appName):
        pass
    
    
    def Configure(self, appName=""):
        dialog = eg.ConfigurationDialog(self, resizeable=True)
        appList = TestListCtrl(
            dialog,
            style = wx.LC_REPORT|wx.LC_SINGLE_SEL
        )
        path = os.path.dirname(__file__)
        imageList = wx.ImageList(16, 16)
        imageList.Add(GetIcon(os.path.join(path, "cwindow.png")))
        appList.SetImageList(imageList, wx.IMAGE_LIST_SMALL)

        appList.InsertColumn(1, "Program")
        processes = EnumProcesses()
        pids = {}
        for pid in processes:
            pids[pid] = []
            
        hwnds = []
        def EnumProc(hwnd, data):
            data.append(hwnd)
            return True
        EnumWindows(EnumProc, hwnds)
        
        for hwnd in hwnds:
            threadID, pid = GetWindowThreadProcessId(hwnd)
            if pid == ourProcessID:
                continue
            #if not self.includeInvisible and not IsWindowVisible(hwnd):
            #    continue
            pids[pid].append(hwnd)

        programs = []
        for pid in processes:
            processName = GetNameOfPID(pid)
            if not processName:
                continue
            programs.append(processName)
        programs.sort()
        iconHandle = ctypes.c_ulong()
        i = 0
        for processName in programs:
            iconIndex = 0
            numIcons = ctypes.windll.shell32.ExtractIconExW(
                processName,
                0,
                0,
                ctypes.byref(iconHandle),
                1
            )
            if numIcons == 1:
                icon = wx.NullIcon
                icon.SetHandle(iconHandle.value)
                icon.SetSize((16,16))
                iconIndex = imageList.AddIcon(icon)
            appList.InsertImageStringItem(i, processName, iconIndex)
            i += 1
            
        dialog.sizer.Add(appList, 1, wx.EXPAND)
        
        appTextCtrl = wx.TextCtrl(dialog)
        dialog.sizer.Add(appTextCtrl, 0, wx.EXPAND)
        
        def OnSelectionChanged(event):
            index = appList.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
            if index != -1:
                appTextCtrl.SetValue(appList.GetItemText(index))
        appList.Bind(wx.EVT_LIST_ITEM_SELECTED, OnSelectionChanged)
        
        if dialog.AffirmedShowModal():
            return (
                ""
            )


class TestPlugin(eg.PluginClass):

    def __init__(self):
        self.AddAllActions()



class PopupMenu(eg.ActionClass):
    
    def __call__(self):
        wx.CallAfter(self.DoIt)
        
    def DoIt(self):
        menu = wx.Menu("Test")
        menu.Append(wx.NewId(), "Test1")
        menu.Append(wx.NewId(), "Test2")
        menu.Append(wx.NewId(), "Test3")
        menu.Append(wx.NewId(), "Test4")
        menu.Append(wx.NewId(), "Test5")
        from eg.WinAPI.Utils import BringHwndToFront
        frame = wx.Frame(None, -1, style=wx.FRAME_NO_TASKBAR )
        #frame.Show()
        def OnClose(event):
            eg.whoami()
            frame.Destroy()
            
        frame.Bind(wx.EVT_MENU_CLOSE, OnClose)
        BringHwndToFront(frame.GetHandle())
        frame.PopupMenu(menu)
        
import win32api
import _winreg

from eg.WinAPI.win32types import *

GetRawInputDeviceList = user32.GetRawInputDeviceList 
GetRawInputDeviceInfo = user32.GetRawInputDeviceInfoA

RIM_TYPEHID = 2
RIM_TYPEKEYBOARD = 1
RIM_TYPEMOUSE = 0

RIDI_PREPARSEDDATA = 0x20000005
RIDI_DEVICENAME    = 0x20000007
RIDI_DEVICEINFO    = 0x2000000b


class RAWINPUTDEVICELIST(Structure):
    _fields_ = [
        ("hDevice", HANDLE),
        ("dwType", DWORD),
    ]
    

class RID_DEVICE_INFO_MOUSE(Structure):
    _fields_ = [
        ("dwId", DWORD),
        ("dwNumberOfButtons", DWORD),
        ("dwSampleRate", DWORD),
        ("fHasHorizontalWheel", BOOL),
    ]
    

class RID_DEVICE_INFO_KEYBOARD(Structure):
    _fields_ = [
        ("dwType", DWORD),
        ("dwSubType", DWORD),
        ("dwKeyboardMode", DWORD),
        ("dwNumberOfFunctionKeys", DWORD),
        ("dwNumberOfIndicators", DWORD),
        ("dwNumberOfKeysTotal", DWORD),
    ]
    
    
class RID_DEVICE_INFO_HID(Structure):
    _fields_ = [
        ("dwVendorId", DWORD),
        ("dwProductId", DWORD),
        ("dwVersionNumber", DWORD),
        ("usUsagePage", DWORD),
        ("usUsage", DWORD),
    ]
    

class RID_DEVICE_INFO(Structure):
    class _U1(Union):
        _fields_ = [
            ("mouse", RID_DEVICE_INFO_MOUSE),
            ("keyboard", RID_DEVICE_INFO_KEYBOARD),
            ("hid", RID_DEVICE_INFO_HID),
        ]
        
    _fields_ = [
        ("cbSize", DWORD),
        ("dwType", DWORD),
        ("_u1", _U1),
    ]
    _anonymous_ = ("_u1", )


INDENT = "  "

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
        
        
def dump(obj, name=None, indent=""):
    print indent + dumps(obj, name, indent)
    

class RawInput(eg.ActionClass):
    
    def __call__(self):
        puiNumDevices = UINT()
        GetRawInputDeviceList(
            0, 
            byref(puiNumDevices), 
            sizeof(RAWINPUTDEVICELIST)
        )
        pRawInputDeviceList = (RAWINPUTDEVICELIST * puiNumDevices.value)()
        puiNumDevices.value = sizeof(pRawInputDeviceList)
        num = GetRawInputDeviceList(
            byref(pRawInputDeviceList), 
            byref(puiNumDevices), 
            sizeof(RAWINPUTDEVICELIST)
        )
        pData = RID_DEVICE_INFO()
        pData.cbSize = sizeof(RID_DEVICE_INFO)
        pcbSize = UINT()
        for i in range(num):
            hDevice = pRawInputDeviceList[i].hDevice
            dwType = pRawInputDeviceList[i].dwType
            print "Device: %d:" % i
            GetRawInputDeviceInfo(
                hDevice, 
                RIDI_DEVICENAME, 
                0, 
                byref(pcbSize)
            )
            buf = create_string_buffer(pcbSize.value + 1)
            GetRawInputDeviceInfo(
                hDevice,
                RIDI_DEVICENAME,
                buf,
                byref(pcbSize)
            )
            print "  DeviceName: %r" % buf.value
            key = "System\\CurrentControlSet\\Enum\\" 
            key += buf.raw[4:].split("{", 1)[0].replace("#", "\\")
            hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, key)
            value, _ = _winreg.QueryValueEx(hkey, "DeviceDesc")
            mfg, _ = _winreg.QueryValueEx(hkey, "Mfg")
            _winreg.CloseKey(hkey)
            print "  DeviceDesc: %r" % value
            print "  Mfg: %r" % mfg
            pcbSize.value = sizeof(RID_DEVICE_INFO)
            GetRawInputDeviceInfo(
                hDevice,
                RIDI_DEVICEINFO,
                byref(pData),
                byref(pcbSize)
            )
            if dwType == RIM_TYPEMOUSE:
                dump(pData.mouse, indent="  ")
            elif dwType == RIM_TYPEKEYBOARD:
                dump(pData.keyboard, indent="  ")
            elif dwType == RIM_TYPEHID:
                dump(pData.hid, indent="  ")
            else:
                print "unknown type", dwType
                