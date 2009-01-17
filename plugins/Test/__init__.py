eg.RegisterPlugin(
    name = "Asus P5W DH remote",
    author = "",
    version = "1.0." + "$LastChangedRevision: 314 $".split()[1],
    kind = "remote",
    description = (
        'Plugin for USB IR Reciever of Asus P5W DH Motherboard'
    ),
)

import os
from threading import Timer
from msvcrt import get_osfhandle
import _winreg
import ctypes

from ctypes import Structure, Union, c_byte, c_char, c_int, c_long, c_ulong, c_ushort, c_wchar
from ctypes import pointer, byref, sizeof, POINTER, cast
from ctypes.wintypes import ULONG, BOOLEAN, BYTE

from eg.WinApi.Dynamic import (
    WinDLL,
    windll,
    WINFUNCTYPE,
    POINTER,
    HWND ,
    HMODULE ,
    c_uint,
    c_void_p,
    c_char_p,
    WNDCLASS,
    GetDesktopWindow,
    WNDPROC,
    CreateWindow,
    WinError,
    RegisterClass,
    WS_OVERLAPPEDWINDOW,
    CW_USEDEFAULT,
    WM_TIMER,
    pointer,
    DestroyWindow,
    UnregisterClass,
    GetTickCount,
    DWORD,
    HANDLE,
    WPARAM,
    create_string_buffer,
)

class RAWINPUTDEVICE(Structure):
    _fields_ = [
      ("usUsagePage", c_ushort),
        ("usUsage", c_ushort),
        ("dwFlags", DWORD),
        ("hwndTarget", HWND),
    ]
       
class RAWHID(Structure):
   _fields_ = [
      ("dwSizeHid", DWORD),
      ("dwCount", DWORD),
      ("bRawData", BYTE),
   ]
   
class RAWINPUTHEADER(Structure):
    _fields_ = [
        ("dwType", DWORD),
        ("dwSize", DWORD),
        ("hDevice", HANDLE),
        ("wParam", WPARAM),
    ]
           
class RAWINPUT(Structure):
   class RAWINPUT_DATA_VALUE(Union):
      _fields_ = [
         ("mouse", DWORD),
         ("keyboard", DWORD),
         ("hid",RAWHID),
      ]
   _fields_ = [
      ("header", RAWINPUTHEADER),
      ("data", RAWINPUT_DATA_VALUE),
   ]
      
WM_INPUT              = 0x00FF   
RIDEV_PAGEONLY        = 0x00000020
RIDEV_INPUTSINK       = 0x00000100
RID_INPUT            = 0x10000003
RIM_TYPEMOUSE         = 0
RIM_TYPEKEYBOARD      = 1
RIM_TYPEHID           = 2


class AsusMessageReceiver(eg.ThreadWorker):
    """
    A thread with a hidden window to receive win32 messages from the driver
    """
    hwnd = None
    dll = None
    button = None
   
    @eg.LogIt
    def Setup(self, plugin):
        """
        This will be called inside the thread at the beginning.
        """
       
        self.plugin = plugin

        wc = WNDCLASS()
        wc.hInstance = GetDesktopWindow()
        wc.lpszClassName = "AsusPluginEventSinkWndClass"
        wc.lpfnWndProc = WNDPROC(self.MyWndProc)
        if not RegisterClass(byref(wc)):
            raise WinError()
        self.hwnd = CreateWindow(
            wc.lpszClassName, 
            "AsusPlugin Event Window", 
            WS_OVERLAPPEDWINDOW, 
            CW_USEDEFAULT, 
            CW_USEDEFAULT, 
            CW_USEDEFAULT, 
            CW_USEDEFAULT, 
            0, 
            0, 
            wc.hInstance, 
            None
        )
        if not self.hwnd:
            raise WinError()
        self.wc = wc
        self.hinst = wc.hInstance
       
        rid = RAWINPUTDEVICE()
        rid.usUsagePage = 0x01
        rid.usUsage = 0x02
        rid.dwFlags = RIDEV_INPUTSINK
        rid.hwndTarget = self.hwnd
        windll.user32.RegisterRawInputDevices(byref(rid), 1, sizeof(rid))
       
    @eg.LogIt
    def Finish(self):
        """
        This will be called inside the thread when it finishes. It will even
        be called if the thread exits through an exception.
        """
        if self.hwnd:
            windll.user32.KillTimer(self.hwnd, 1)

        if self.hwnd:
            DestroyWindow(self.hwnd)
            UnregisterClass(self.wc.lpszClassName, self.hinst)       
       
    #@eg.LogIt
    def MyWndProc(self, hwnd, msg, wParam, lParam):
        if msg == WM_INPUT:
            dwSize = c_uint(0)
            windll.user32.GetRawInputData(lParam, RID_INPUT, 0, byref(dwSize), sizeof(RAWINPUTHEADER))

            bytebuf = c_byte * dwSize.value
            lpb = bytebuf()               
            windll.user32.GetRawInputData(lParam, RID_INPUT, byref(lpb), byref(dwSize), sizeof(RAWINPUTHEADER))
            raw = cast(lpb, POINTER(RAWINPUT))
            print raw.contents.header.hDevice
            if raw.contents.header.dwType == RIM_TYPEMOUSE:
                print "found"
                
                charbuf = c_char * 100;
                if (raw.data.hid.bRawData[2]==0):
                    windll.user32.KillTimer(self.hwnd, 1)
                else:
                    button = raw.data.hid.bRawData[2]
                    self.TriggerEvent(button)
                    windll.user32.SetTimer(self.hwnd, 1, 400, NULL)
        if msg == WM_TIMER:
            self.TriggerEvent(button)
            windll.user32.SetTimer(self.hwnd, 1, 100, NULL)
               
        return 1
   
    def OnTimeOut(self):
        self.keyStillPressed = False
        self.lastEvent.SetShouldEnd()
       
       

class AsusIR(eg.PluginClass):
   
    class text:
        buttonTimeout = "Button release timeout (seconds):"
        buttonTimeoutDescr = (
            "(If you get unintended double presses of the buttons, "
            "increase this value.)"
        )

    def __start__(self, waitTime=0.15):
        self.msgThread = AsusMessageReceiver(self)
        self.msgThread.Start()


    @eg.LogIt
    def OnComputerSuspend(self, suspendType):
        self.__stop__()
   
   
    @eg.LogIt
    def OnComputerResume(self, suspendType):
        self.__start__()     
         
                       
    def __stop__(self):
        self.msgThread.Stop()
        
from eg.cFunctions import GetProcessDict
from threading import Thread
from time import sleep
from os.path import splitext

oldProcesses = GetProcessDict()
oldPids = set(oldProcesses.iterkeys())

def ThreadFunc():
    global processDict, pids
    
    while True:
        newProcesses = GetProcessDict()
        newPids = set(newProcesses.iterkeys())
        for pid in newPids.difference(pids):
            name = splitext(newProcesses[pid])[0]
            eg.TriggerEvent("Created."+ name, prefix="Process")
        for pid in pids.difference(newPids):
            name = splitext(processDict[pid])[0]
            eg.TriggerEvent("Destroyed."+ name, prefix="Process")
        processDict = newProcesses
        pids = newPids
        sleep(0.1)
        
Thread(target=ThreadFunc).start()
