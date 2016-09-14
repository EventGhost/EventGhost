# -*- coding: utf-8 -*-
#
# plugins/MceRemote/__init__.py
#
# This file is a plugin for EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import eg

eg.RegisterPlugin(
    name = "Microsoft MCE Remote",
    author = (
        "Bitmonster",
        "James Lee",
    ),
    version = "1.1.1093",
    kind = "remote",
    guid = "{02181DB1-F29D-4CCB-BF91-7A86EFB0D22C}",
    description = 'Plugin for the Microsoft MCE remote.',
    help = """
        <center><img src="MCEv2.jpg"/></center>
    """,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACfklEQVR42q2TS2gTQRyH"
        "f5N9NNlts20abYyxVirWShGLUh8XoSpUUBEVUU+5CXoQr+LNm14UtRCpRcGLHnqoiooN"
        "VO1FRWrTaKgmqdJqGuwj3TTZ947bbLV37cAMM8zMx39+fEPwn42sGKD7zk3aeWg3TEut"
        "rC3bdrpZmZuWBlVXYFgGKKEQOAHDg+M4f/YCqQBuxa7T7XtaEWloRkkrwDQt6KZzwdZR"
        "VGSU1DmoRgm6pUBWC1DUMoK1q2BmQ24F77/G6ZfvI2isb0FRnYVYZtAe8aCUkzGSyuCj"
        "tADFLsEwNOi0CM1QYDnVrNcOuICHQzfoWCaJoD8MWZnGfoPB1k0BpN/k8DKbxvAGE1JA"
        "QHidF9lMHvnChPMuii3sCRdwre8czUykwDAMuLKKU1oV2CCL7Itx9LMycmtqsa2jAY1N"
        "EgaepWBxc2A5Dq30mAu40neGpr59AKUUliHB5z8KUwxi5vUDWCQNW2TRvrOpknkykYRQ"
        "7wXr4bFRO+ICrj6J0tHcq0ris3MHwbdcgiaX8XMohl2B+xAF4jyhBsqCgqQTsOhnwXNe"
        "NM4fdgG3By7S4amnoBaHT4m9gP84ivkUquf7cTL8Fh1tPjSv9eHxqIw48YL3MfBWiQj/"
        "6nIBzxN3afxHDJYTzLvBOvBMGfMFPyLcZ3QFCtixWcCiET1pFVpIAiE2aqrrEM4vAZIT"
        "Q/RR6jKo1zmgOrLYtAIzphSEZ2cQ8gGTio0E5SGFa6BrBiJSKxqm97mAWE83VUJjSEzG"
        "nXT5v34ugkqKDkPW4OEZCCIH4iEg1IPOttPQ0quXVe6910vh6EuX/F5U1hmWZV/a+LP0"
        "EBbRaJSs3Gf61/YbN1kg0OJlna4AAAAASUVORK5CYII="
    ),
)

import wx
import os
import _winreg as reg
from threading import Timer
from msvcrt import get_osfhandle

from eg.WinApi.Dynamic import (
    WinDLL,
    byref,
    WinError,
    GetModuleHandle,
    CreateWindowEx,
    DestroyWindow,
    RegisterClass,
    UnregisterClass,
    LoadCursor,
    WNDCLASS,
    WNDPROC,
    WM_USER,
    WS_OVERLAPPEDWINDOW,
    CW_USEDEFAULT,
)

#BOOL WINAPI MceIrRegisterEvents(HWND hWnd)
#------------------------------------------
#To register the window that will receives messages on keystroke events (from
#MceIr only)
#(IR code analysis is automatically suspended during a learning phase)
#
#hWnd : handle to the window which will receives WM_USER messages
#       wParam values is ID_MCEIR_KEYCODE
#       LOWORD(lParam) contains the key code (see MceIr.h for the list)
#       HIWORD(lParam) contains the repeat count (0 means a new keystroke)
#returns TRUE is successfull
#
#BOOL WINAPI MceIrUnregisterEvents()
#-----------------------------------
#To stop receiving keystrokes from IR
#
#returns TRUE is successfull
#
#BOOL WINAPI MceIrSetRepeatTimes(DWORD FirstRepeat, DWORD NextRepeats)
#---------------------------------------------------------------------
#To specify the repeat rate when a key remains pressed
#FirstRepeat : Time (in ms) to wait before sending a second WM_USER message
#              (HIWORD(lParam) will be 1)
#NextRepeats : Interval between next messages until the key is released
#
#returns TRUE is successfull
#
#BOOL WINAPI MceIrRecordToFile(HANDLE hFile, DWORD Timeout)
#----------------------------------------------------------
#To record raw IR code (learning function). This function waits for the IR
#receiver to become silent for 1 second, then enters the recording phase.
#
#hFile  : handle to the file in which raw IR codes will be stored
#        (must be opened previously then closed when function returns)
#Timeout: applies to the recording phase and occurs is nothing is received from the MceIr (in ms)
#
#returns TRUE is successfull
#
#BOOL WINAPI MceIrPlaybackFromFile(HANDLE hFile)
#-----------------------------------------------
#To playback a previously recorded file.
#
#hFile  : handle to the file in which raw IR codes has been stored
#        (must be opened previously then closed when function returns)
#
#returns TRUE is successfull
#
#BOOL WINAPI MceIrSuspend()
#-----------------------------------------------
#Call this function before entering a suspend power state
#    (WM_POWERBROADCAST + PBT_APMSUSPEND event)
#
#BOOL WINAPI MceIrResume()
#-----------------------------------------------
#Call this function on resuming a suspend power state
#    (WM_POWERBROADCAST + PBT_APMRESUMEAUTOMATIC event)
#
#BOOL WINAPI MceIrSelectBlaster()
#-----------------------------------------------
#To select a blaster port on which further IR playback will be send
#
#BOOL WINAPI MceIrCheckFile(HANDLE hFile)
#-----------------------------------------------
#To check in the API support playing this file



KEY_MAP = {
    0x7b9a: "TV_Power", 0x7ba1: "Blue", 0x7ba2: "Yellow", 0x7ba3: "Green",
    0x7ba4: "Red", 0x7ba5: "Teletext", 0x7baf: "Radio", 0x7bb1: "Print",
    0x7bb5: "Videos", 0x7bb6: "Pictures", 0x7bb7: "Recorded_TV",
    0x7bb8: "Music", 0x7bb9: "TV", 0x7bd9: "Guide", 0x7bda: "LiveTV",
    0x7bdb: "DVDMenu", 0x7bdc: "Back", 0x7bdd: "Ok", 0x7bde: "Right",
    0x7bdf: "Left", 0x7be0: "Down", 0x7be1: "Up", 0x7be2: "Star",
    0x7be3: "Pound", 0x7be4: "Replay", 0x7be5: "Skip", 0x7be6: "Stop",
    0x7be7: "Pause", 0x7be8: "Record", 0x7be9: "Play", 0x7bea: "Rewind",
    0x7beb: "Forward", 0x7bec: "ChannelDown", 0x7bed: "ChannelUp",
    0x7bee: "VolumeDown", 0x7bef: "VolumeUp", 0x7bf0: "Details",
    0x7bf1: "Mute", 0x7bf2: "Start", 0x7bf3: "Power", 0x7bf4: "Enter",
    0x7bf5: "Escape", 0x7bf6: "Num9", 0x7bf7: "Num8", 0x7bf8: "Num7",
    0x7bf9: "Num6", 0x7bfa: "Num5", 0x7bfb: "Num4", 0x7bfc: "Num3",
    0x7bfd: "Num2", 0x7bfe: "Num1", 0x7bff: "Num0",
    # Only available on the MCE Keyboard:
    0x7b96: "Messenger",
}

HID_SUB_KEY = (
    "SYSTEM\\CurrentControlSet\\Services\\HidIr\\Remotes\\"
    "745a17a0-74d3-11d0-b6fe-00a0c90f57da"
)

PLUGIN_DIR = os.path.abspath(os.path.split(__file__)[0])


class MceMessageReceiver(eg.ThreadWorker):
    """
    A thread with a hidden window to receive win32 messages from the driver
    """
    def Setup(self, plugin, waitTime):
        """
        This will be called inside the thread at the beginning.
        """
        self.plugin = plugin
        self.waitTime = waitTime
        self.timer = Timer(0, self.OnTimeOut)
        self.lastEvent = None

        wc = WNDCLASS()
        wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "HiddenMceMessageReceiver"
        wc.lpfnWndProc = WNDPROC(self.MyWndProc)
        if not RegisterClass(byref(wc)):
            raise WinError()
        self.hwnd = CreateWindowEx(
            0,
            wc.lpszClassName,
            "MCE Remote Message Receiver",
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

        self.dll = WinDLL(os.path.join(PLUGIN_DIR, "MceIr.dll"))
        if not self.dll.MceIrRegisterEvents(self.hwnd):
            raise self.plugin.Exceptions.DeviceNotFound
        self.dll.MceIrSetRepeatTimes(1,1)


    @eg.LogIt
    def Finish(self):
        """
        This will be called inside the thread when it finishes. It will even
        be called if the thread exits through an exception.
        """
        self.dll.MceIrUnregisterEvents()
        DestroyWindow(self.hwnd)
        UnregisterClass(self.wc.lpszClassName, self.hinst)
        self.Stop() # is this needed?


    #@eg.LogIt
    def MyWndProc(self, dummyHwnd, mesg, dummyWParam, lParam):
        if mesg == WM_USER:
            self.timer.cancel()
            key = lParam & 0xFFFF
            #repeatCounter = (lParam >> 16)
            if key in KEY_MAP:
                eventString = KEY_MAP[key]
            else:
                eventString = "%X" % key
            if not self.lastEvent:
                self.lastEvent = self.plugin.TriggerEnduringEvent(eventString)
            self.timer = Timer(self.waitTime, self.OnTimeOut)
            self.timer.start()
        return 1


    def OnTimeOut(self):
        if self.lastEvent:
            self.lastEvent.SetShouldEnd()
        self.lastEvent = None



class MceRemote(eg.PluginBase):

    class text:
        buttonTimeout = "Button release timeout (seconds):"
        buttonTimeoutDescr = (
            "(If you get unintended double presses of the buttons, "
            "increase this value.)"
        )
        disableHid = "Disable HID service for this remote (recommended)"
        hidDialogCaption = "EventGhost: MCE Remote Plugin"
        hidDialogMessage = (
            "The plugin has changed the state of the HID service for this "
            "remote. To let the changes take effect, you need to manually "
            "restart the system."
        )
        hidErrorMessage = (
            "The plugin was not able to change the state of the HID service. "
            "You must be logged in as Administrator to change the state."
        )

    def __init__(self):
        self.AddEvents()
        self.AddAction(TransmitIr)


    @eg.LogIt
    def __start__(self, waitTime=0.15, disableHid=True):
        self.CheckHidState(disableHid)
        self.msgThread = MceMessageReceiver(self, waitTime)
        self.msgThread.Start(10.0)


    @eg.LogIt
    def OnComputerSuspend(self, dummySuspendType):
        self.msgThread.CallWait(self.msgThread.dll.MceIrSuspend)


    @eg.LogIt
    def OnComputerResume(self, dummySuspendType):
        self.msgThread.CallWait(self.msgThread.dll.MceIrResume)


    def __stop__(self):
        self.msgThread.Stop()


    def ShowHidMessage(self, disableHid):
        """
        Informs the user, that the system needs to restart the system to let
        the HID registry changes take effect.
        """
        try:
            self.SetHidState(disableHid)
        except WindowsError:
            dialog = wx.MessageDialog(
                None,
                self.text.hidErrorMessage,
                self.text.hidDialogCaption,
                wx.OK|wx.ICON_ERROR|wx.STAY_ON_TOP
            )
        else:
            dialog = wx.MessageDialog(
                None,
                self.text.hidDialogMessage,
                self.text.hidDialogCaption,
                wx.OK|wx.ICON_INFORMATION|wx.STAY_ON_TOP
            )
        dialog.ShowModal()
        dialog.Destroy()


    def SetHidState(self, disableHid):
        """
        Sets the HID registry values. Will raise WindowsError if not
        successful.
        """
        key = reg.OpenKey(
            reg.HKEY_LOCAL_MACHINE, HID_SUB_KEY, 0, reg.KEY_ALL_ACCESS
        )
        for i in xrange(4):
            valueName = 'CodeSetNum%i' % i
            if disableHid:
                reg.DeleteValue(key, valueName)
            else:
                reg.SetValueEx(key, valueName, 0, reg.REG_DWORD, i + 1)


    def CheckHidState(self, disableHid):
        """
        Checks the HID registry values and calls self.ShowHidMessage
        if needed.
        """
        try:
            key = reg.OpenKey(
                reg.HKEY_LOCAL_MACHINE, HID_SUB_KEY, 0, reg.KEY_READ
            )
        except WindowsError:
            raise self.Exceptions.DeviceNotFound

        needsChange = False
        for i in xrange(4):
            valueName = 'CodeSetNum%i' % i
            try:
                dummyValue, dummyValueType = reg.QueryValueEx(key, valueName)
                disabled = False
            except WindowsError:
                disabled = True
            if disableHid != disabled:
                needsChange = True
                break
        reg.CloseKey(key)
        if needsChange:
            wx.CallAfter(self.ShowHidMessage, disableHid)


    def Configure(self, waitTime=0.15, disableHid=True):
        panel = eg.ConfigPanel()
        waitTimeCtrl = panel.SpinNumCtrl(waitTime, integerWidth=3)
        disableHidCtrl = panel.CheckBox(disableHid, self.text.disableHid)
        panel.AddLine(self.text.buttonTimeout, waitTimeCtrl)
        panel.AddLine(self.text.buttonTimeoutDescr)
        panel.AddLine()
        panel.AddLine(disableHidCtrl)

        while panel.Affirmed():
            panel.SetResult(
                waitTimeCtrl.GetValue(),
                disableHidCtrl.GetValue()
            )



class TransmitIr(eg.ActionBase):
    name = "Transmit IR"

    def __call__(self, code=""):
        tmpFile = os.tmpfile()
        tmpFile.write(code)
        tmpFile.seek(0)
        self.plugin.msgThread.dll.MceIrPlaybackFromFile(
            get_osfhandle(tmpFile.fileno())
        )


    def Configure(self, code=""):
        panel = eg.ConfigPanel()
        code = ' '.join([("%02X" % ord(c)) for c in code])

        editCtrl = wx.TextCtrl(panel, -1, code, style=wx.TE_MULTILINE)
        font = editCtrl.GetFont()
        font.SetFaceName("Courier New")
        editCtrl.SetFont(font)
        editCtrl.SetMinSize((-1, 100))

        def Learn(dummyEvent):
            tmpFile = os.tmpfile()
            self.plugin.msgThread.dll.MceIrRecordToFile(
                get_osfhandle(tmpFile.fileno()),
                10000
            )
            tmpFile.seek(0)
            code = tmpFile.read()
            tmpFile.close()
            editCtrl.SetValue(' '.join([("%02X" % ord(c)) for c in code]))
        learnButton = wx.Button(panel, -1, "Learn IR Code")
        learnButton.Bind(wx.EVT_BUTTON, Learn)

        panel.sizer.Add(editCtrl, 1, wx.EXPAND)
        panel.sizer.Add((5, 5))
        panel.sizer.Add(learnButton, 0, wx.ALIGN_RIGHT)
        while panel.Affirmed():
            code = editCtrl.GetValue().replace(" ", "").decode("hex_codec")
            panel.SetResult(code)

