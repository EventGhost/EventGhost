import eg

class PluginInfo(eg.PluginInfo):
    name = "Raw Input Device"
    
import wx
import win32api
import win32gui
import win32con

from eg.WinAPI.win32types import *
from eg.WinAPI.RawInput import (
    RAWINPUTDEVICE, 
    RAWINPUTHEADER, 
    RAWINPUT,
    RegisterRawInputDevices, 
    GetRawInputData
)



RIDEV_INPUTSINK = 256
RID_INPUT  = 0x10000003
RID_HEADER = 0x10000005

class RawInput(eg.PluginClass):
    
    def __start__(self):
        eg.whoami()
        self.frame = wx.Frame(None)
        self.hwnd = self.frame.GetHandle()
        # Set the WndProc to our function
        self.oldWndProc = win32gui.SetWindowLong(
            self.hwnd,
            win32con.GWL_WNDPROC,
            self.MyWndProc
        )
        rid = RAWINPUTDEVICE()
        rid.usUsagePage = 1
        rid.usUsage = 6
        rid.dwFlags = RIDEV_INPUTSINK
        rid.hwndTarget = self.hwnd
        RegisterRawInputDevices(pointer(rid), 1, sizeof(RAWINPUTDEVICE))
        

    def MyWndProc(self, hWnd, msg, wParam, lParam):
        # Display what we've got.
        # Restore the old WndProc.  Notice the use of wxin32api
        # instead of win32gui here.  This is to avoid an error due to
        # not passing a callable object.
        if msg == win32con.WM_DESTROY:
            win32api.SetWindowLong(self.hwnd,
                                   win32con.GWL_WNDPROC,
                                   self.oldWndProc)
        elif msg == 255:
            eg.whoami()
            buf = RAWINPUT()
            cbSize = UINT(sizeof(buf))
            res = GetRawInputData(
                lParam,
                RID_INPUT,
                byref(buf),
                byref(cbSize),
                sizeof(RAWINPUTHEADER)
            )
            print res, cbSize.value, buf.keyboard.VKey
                
        

        # Pass all messages (in this case, yours may be different) on
        # to the original WndProc
        return win32gui.CallWindowProc(self.oldWndProc,
                                       hWnd, msg, wParam, lParam)

        