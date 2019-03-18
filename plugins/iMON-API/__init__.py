# This file is part of EventGhost.
# Copyright (C) 2008 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.9   01.02.2012      brand10     First Beta Release
# ===============================================================================

import eg

eg.RegisterPlugin(
    name="SoundGraph iMON API",
    author="brand10 (HiLogic)",
    version="0.9",
    kind="remote",
    guid="{d00881c0-92d5-4ea1-bbf9-7ceb38c2c6ba}",
    description=ur"""<rst>
Plugin for the **SoundGraph iMON API**

.. image:: imon-vfd.jpg
   :align: left

Be sure iMON Manager 8.04.0629 or newer is installed and running!""",
)

import os

from eg.WinApi.Dynamic import (
    CDLL,
    HWND,
    WNDCLASS,
    WNDPROC,
    WM_USER,
    WS_OVERLAPPEDWINDOW,
    CW_USEDEFAULT,
    CFUNCTYPE,
    GetModuleHandle,
    CreateWindowEx,
    DestroyWindow,
    RegisterClass,
    UnregisterClass,
    WinError,
    byref,
    c_uint,
)

PLUGIN_DIR = os.path.abspath(os.path.split(__file__)[0])

# RCNInitResult
RCN_SUCCEEDED = 0
RCN_ERR_IN_USING = 0x0100
RCN_ERR_HW_DISCONNECTED = 0x0101
RCN_ERR_NOT_SUPPORTED_HW = 0x0102
RCN_ERR_PLUGIN_DISABLED = 0x0103
RCN_ERR_IMON_NO_REPLY = 0x0104
RCN_ERR_UNKNOWN = 0x0200

# RCNotifyCode
RCNM_PLUGIN_SUCCEED = 0
RCNM_PLUGIN_FAILED = 1
RCNM_IMON_RESTARTED = 2
RCNM_IMON_CLOSED = 3
RCNM_HW_CONNECTED = 4
RCNM_HW_DISCONNECTED = 5
RCNM_LCD_TEXT_SCROLL_DONE = 6
RCNM_RC_REMOTE = 0x1000
RCNM_RC_BUTTON_DOWN = 0x1001
RCNM_RC_BUTTON_UP = 0x1002
RCNM_KNOB_ACTION = 0x1003

# RCRemote
REMOTE_NONE = 0
REMOTE_IMON_RC = 101
REMOTE_IMON_RSC = 102
REMOTE_IMON_MM = 107
REMOTE_IMON_EX = 112
REMOTE_IMON_PAD = 115
REMOTE_IMON_24G = 116
REMOTE_MCE = 119
REMOTE_IMON_MINI = 124

# Remote Commands
RCCommand = {
    2: "Play",
    3: "Pause",
    4: "Stop",
    5: "Prev",
    6: "Next",
    7: "Rewind",
    8: "Forward",
    9: "Eject",
    10: "Volume+",
    11: "Volume-",
    12: "Mute",
    13: "Open",
    14: "Record",
    15: "QuickLaunch",
    16: "Channel+",
    17: "Channel-",
    18: "Up",
    19: "Down",

    20: "Left",
    21: "Right",
    22: "Enter",
    23: "Backspace",
    24: "Esc",
    25: "Space",
    26: "AppLauncher",
    27: "TaskSwitch",
    28: "Timer",
    29: "ShiftTab",
    30: "Tab",
    31: "MyMusic",
    32: "MyVideos",
    33: "MyPictures",
    34: "MyTV",

    36: "Thumbnail",
    37: "AspectRatio",
    38: "FullScreen",
    39: "MyDVD",

    40: "DVDMenu",
    41: "Subtitle",
    42: "Audio",
    43: "AppExit",
    44: "Windows",
    45: "Info",
    46: "MouseKeyboard",
    47: "Num1",
    48: "Num2",
    49: "Num3",
    50: "Num4",
    51: "Num5",
    52: "Num6",
    53: "Num7",
    54: "Num8",
    55: "Num9",
    56: "Num0",
    57: "Power",
    58: "Bookmark",

    60: "PlayPause",

    81: "Star",
    82: "Sharp",

    86: "Radio",
    87: "LiveTV",
    88: "RecordedTV",
    89: "TVGuide",
    90: "Clear",
    91: "Print",
    92: "Enter(Num)",
    93: "Messenger",
    94: "Videotext",
    95: "Red",
    96: "Green",
    97: "Yellow",
    98: "Blue",

    110: "Visualization",
    111: "Slideshow",
    112: "Angle",

    4096: "VolKnob_Push",
    4097: "VolKnob_LongPush",
    4098: "VolKnob_Left",
    4099: "VolKnob_Right",
    4100: "NavKnob_Push",
    4101: "NavKnob_LongPush",
    4102: "NavKnob_Left",
    4103: "NavKnob_Right",
}

# Remote Type
RCRemote = {
    101: "iMON RC Remote",
    102: "iMON RSC Remote",
    107: "iMON MM Remote",
    112: "iMON EX Remote",
    115: "iMON PAD Remote",
    116: "iMON 2.4G Remote",
    119: "MCE Remote",
    124: "iMON Mini Remote",
}


class APIMessageReceiver(eg.ThreadWorker):
    def Setup(self, plugin):
        """
        This will be called inside the thread at the beginning.
        """
        self.plugin = plugin

        wc = WNDCLASS()
        wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "HiddenAPIMessageReceiver"
        wc.lpfnWndProc = WNDPROC(self.MyWndProc)

        if not RegisterClass(byref(wc)):
            raise WinError()

        self.hwnd = CreateWindowEx(
            0,
            wc.lpszClassName,
            "iMON-API Message Receiver",
            WS_OVERLAPPEDWINDOW,
            CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT,
            0, 0, wc.hInstance, None
        )

        if not self.hwnd:
            raise WinError()

        self.wc = wc
        self.hinst = wc.hInstance
        self.dll = CDLL(os.path.join(PLUGIN_DIR, "iMONRemoteControl.dll"))

        # API Method-Definitions
        self.ApiInit = CFUNCTYPE(HWND, c_uint)
        self.ApiUninit = CFUNCTYPE(None)
        # self.IsInited = CFUNCTYPE(None)
        # self.IsPluginMode = CFUNCTYPE(None)

        self.ApiInit = self.dll.IMON_RcApi_Init
        self.ApiUninit = self.dll.IMON_RcApi_Uninit
        # self.IsInited = self.dll.IMON_RcApi_IsInited
        # self.IsPluginMode = self.dll.IMON_RcApi_IsPluginModeEnabled

        if self.ApiInit(self.hwnd, WM_USER) != 0:
            raise Exception("iMON API-call failed")

    @eg.LogIt
    def Finish(self):
        """
        This will be called inside the thread when it finishes. It will even
        be called if the thread exits through an exception.
        """
        self.ApiUninit()
        DestroyWindow(self.hwnd)
        UnregisterClass(self.wc.lpszClassName, self.hinst)
        self.Stop()  # is this needed?

    # @eg.LogIt
    def MyWndProc(self, dummyHwnd, mesg, wParam, lParam):
        if mesg == WM_USER:
            # All OK
            if (wParam == RCNM_PLUGIN_SUCCEED) or (wParam == RCNM_IMON_RESTARTED) or (wParam == RCNM_HW_CONNECTED):
                print "iMON_API: Init successful"

            # Error handling
            if wParam == RCNM_PLUGIN_FAILED:
                self.plugin.PrintError("iMON_API: Can't get control of remote")

            if wParam == RCNM_HW_DISCONNECTED:
                self.plugin.PrintError("iMON_API: Hardware disconnected")

            if wParam == RCNM_IMON_CLOSED:
                self.plugin.PrintError("iMON_API: iMON Manager is not running")

            # Command handling
            if wParam == RCNM_RC_REMOTE:
                if lParam in RCRemote:
                    self.plugin.remote = RCRemote[lParam]
                    # print "Remote: " + RCRemote[lParam]

            if wParam == RCNM_RC_BUTTON_DOWN:
                if lParam in RCCommand:
                    self.plugin.lastEvent = self.plugin.TriggerEnduringEvent(RCCommand[lParam])

            if wParam == RCNM_RC_BUTTON_UP:
                self.plugin.lastEvent.SetShouldEnd()
                self.plugin.lastEvent = None

            if wParam == RCNM_KNOB_ACTION:
                if lParam in RCCommand:
                    self.plugin.lastEvent = self.plugin.TriggerEvent(RCCommand[lParam])

        return 1


class iMON_API(eg.PluginBase):
    @eg.LogIt
    #    def __init__(self):
    # self.AddEvents()
    # self.AddAction(TransmitIr)

    def __start__(self):
        self.msgThread = APIMessageReceiver(self)
        self.msgThread.Start()

    def __stop__(self):
        self.msgThread.Stop()

    # @eg.LogIt
    # def OnTimeout(self):

    # @eg.LogIt
    # def OnComputerSuspend(self, dummySuspendType):

    # @eg.LogIt
    # def OnComputerResume(self, dummySuspendType):
