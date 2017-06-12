# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
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

# --------- 25/2/2017, 19:50 -7 ---------
# Added Windows XP support
# Thanks to Diz
# ---------------------------------------

import wx
import ctypes
from comtypes import GUID

import eg
from eg.WinApi.Dynamic import (
    windll,
    byref,
    cast,
    POINTER,
    PBT_APMBATTERYLOW,
    PBT_APMOEMEVENT,
    # PBT_APMPOWERSTATUSCHANGE,
    PBT_APMQUERYSUSPEND,
    PBT_APMQUERYSUSPENDFAILED,
    PBT_APMRESUMEAUTOMATIC,
    PBT_APMRESUMECRITICAL,
    PBT_APMRESUMESUSPEND,
    PBT_APMSUSPEND,
    WM_POWERBROADCAST,
)

UCHAR = ctypes.c_ubyte
DWORD = ctypes.wintypes.DWORD

PBT_POWERSETTINGCHANGE = 0x8013

PWR_AC = 0x0
PWR_DC = 0x1
PWR_UPS = 0x2

MON_OFF = 0x0
MON_ON = 0x1
MON_DIM = 0x2

SVR_OFF = 0x0
SVR_ON = 0x1

AWY_EXITING = 0x0
AWY_ENTERING = 0x1


if eg.WindowsVersion >= '8':
    GUID_CONSOLE_DISPLAY_STATE = GUID(
        '{6fe69556-704a-47a0-8f24-c28d936fda47}'
    )
else:
    GUID_CONSOLE_DISPLAY_STATE = GUID(
        '{02731015-4510-4526-99e6-e5a17ebd1aea}'
    )

GUID_SYSTEM_AWAYMODE = GUID(
    '{98a7f580-01f7-48aa-9c0f-44352c29e5C0}'
)
GUID_ACDC_POWER_SOURCE = GUID(
    '{5d3e9a59-e9D5-4b00-a6bd-ff34ff516548}'
)
GUID_BATTERY_PERCENTAGE_REMAINING = GUID(
    '{a7ad8041-b45a-4cae-87a3-eecbb468a9e1}'
)
GUID_GLOBAL_USER_PRESENCE = GUID(
    '{786E8A1D-B427-4344-9207-09E70BDCBEA9}'
)
GUID_POWER_SAVING_STATUS = GUID(
    '{E00958C0-C213-4ACE-AC77-FECCED2EEEA5}'
)
GUID_POWERSCHEME_PERSONALITY = GUID(
    '{245d8541-3943-4422-b025-13A784F679B7}'
)
GUID_MAX_POWER_SAVINGS = GUID(
    '{8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c}'
)
GUID_MIN_POWER_SAVINGS = GUID(
    '{a1841308-3541-4fab-bc81-f71556f20b4a}'
)
GUID_TYPICAL_POWER_SAVINGS = GUID(
    '{381b4222-f694-41f0-9685-ff5bb260df2e}'
)


POWER_MESSAGES = {
    GUID_CONSOLE_DISPLAY_STATE: {
        MON_OFF: 'Monitor.Off',
        MON_ON: 'Monitor.On',
        MON_DIM: 'Monitor.Dim'
    },
    GUID_SYSTEM_AWAYMODE: {
        AWY_EXITING: 'AwayMode.Exiting',
        AWY_ENTERING: 'AwayMode.Entering'
    },
    GUID_ACDC_POWER_SOURCE: {
        PWR_AC: 'PowerSource.Line',
        PWR_DC: 'PowerSource.Battery',
        PWR_UPS: 'PowerSource.UPS'
    },
    GUID_BATTERY_PERCENTAGE_REMAINING: {
        i: 'BatteryLevel.' + str(i) + '%' for i in range(101)
    },
    GUID_POWER_SAVING_STATUS: {
        SVR_OFF: 'PowerSaving.Off',
        SVR_ON: 'PowerSaving.On'
    },
    GUID_POWERSCHEME_PERSONALITY: {
        GUID_MIN_POWER_SAVINGS: 'PowerProfile.PowerSaver',
        GUID_MAX_POWER_SAVINGS: 'PowerProfile.HighPerformance',
        GUID_TYPICAL_POWER_SAVINGS: 'PowerProfile.Balanced'
    },
    PBT_APMRESUMEAUTOMATIC: 'ResumeAutomatic',
    PBT_APMRESUMESUSPEND: 'Resume',
    PBT_APMSUSPEND: 'Suspend'
    # PBT_APMPOWERSTATUSCHANGE: "PowerStatusChange",
}

if eg.WindowsVersion.IsXP():
    POWER_MESSAGES.update({
        PBT_APMBATTERYLOW: 'BatteryLevel.Low', # pre win vista
        PBT_APMOEMEVENT: 'OemEvent', # pre win vista
        PBT_APMQUERYSUSPENDFAILED: 'QuerySuspendFailed', # pre win vista
        PBT_APMRESUMECRITICAL: 'ResumeCritical', # pre win vista
        PBT_APMQUERYSUSPEND: 'QuerySuspend', # pre win vista
    })
else:
    def Register(guid):
        return windll.user32.RegisterPowerSettingNotification(
            eg.messageReceiver.hwnd,
            byref(guid),
            0
        )


    def Unregister(cls):
        windll.user32.UnregisterPowerSettingNotification(cls)


def CreatePowerClass(lParam, cls):
    powerBroadcast = cast(lParam, POINTER(cls))
    powerSetting = powerBroadcast.contents.PowerSetting
    data = powerBroadcast.contents.Data
    msgs = POWER_MESSAGES.get(powerSetting, None)
    if msgs is not None:
        return msgs.get(data, None)


class POWERBROADCAST_SETTING(ctypes.Structure):
    _fields_ = [
        ("PowerSetting", GUID),
        ("Length", DWORD),
        ("Data", UCHAR)
    ]


class BATTERY_PERCENTAGE_REMAINING(ctypes.Structure):
    _fields_ = [
        ("PowerSetting", GUID),
        ("Length", DWORD),
        ("Data", DWORD)
    ]


class POWERSCHEME_PERSONALITY(ctypes.Structure):
    _fields_ = [
        ("PowerSetting", GUID),
        ("Length", DWORD),
        ("Data", GUID)
    ]


class PowerBroadcastNotifier:
    def __init__(self, plugin):
        self.plugin = plugin
        self.monitorNotify = None
        self.awayNotify = None
        self.sourceNotify = None
        self.batteryNotify = None
        self.savingNotify = None
        self.schemeNotify = None

        if eg.WindowsVersion >= 'Vista':
            wx.CallAfter(self.RegisterMessages)

        eg.messageReceiver.AddHandler(
            WM_POWERBROADCAST,
            self.OnPowerBroadcast
        )

    def RegisterMessages(self):
        self.monitorNotify = Register(GUID_CONSOLE_DISPLAY_STATE)
        self.awayNotify = Register(GUID_SYSTEM_AWAYMODE)
        self.sourceNotify = Register(GUID_ACDC_POWER_SOURCE)
        self.batteryNotify = Register(GUID_BATTERY_PERCENTAGE_REMAINING)
        self.savingNotify = Register(GUID_POWER_SAVING_STATUS)
        self.schemeNotify = Register(GUID_POWERSCHEME_PERSONALITY)

    def Close(self):
        if eg.WindowsVersion >= 'Vista':
            Unregister(self.monitorNotify)
            Unregister(self.awayNotify)
            Unregister(self.sourceNotify)
            Unregister(self.batteryNotify)
            Unregister(self.savingNotify)
            Unregister(self.schemeNotify)

        eg.messageReceiver.RemoveHandler(
            WM_POWERBROADCAST,
            self.OnPowerBroadcast
        )

    @eg.LogIt
    def OnPowerBroadcast(self, hwnd, uMsg, wParam, lParam):
        if wParam == PBT_APMRESUMEAUTOMATIC:
            eg.actionThread.CallWait(eg.actionThread.OnComputerResume)

        msg = POWER_MESSAGES.get(wParam, None)

        msgCls = [
            POWERBROADCAST_SETTING,
            POWERSCHEME_PERSONALITY,
            BATTERY_PERCENTAGE_REMAINING
        ]

        while msg is None and msgCls:
            try:
                msg = CreatePowerClass(lParam, msgCls.pop(0))
            except ValueError:
                continue

        if msg is not None:
            eg.eventThread.TriggerEventWait(
                suffix=msg,
                prefix="System",
                source=self.plugin
            )

        if wParam == PBT_APMSUSPEND:
            eg.actionThread.CallWait(eg.actionThread.OnComputerSuspend)
        return 1
