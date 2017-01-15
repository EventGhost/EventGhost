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

# Local imports
import eg

import ctypes
from comtypes import GUID
from eg.WinApi.SystemInformation import GetWindowsVersionString

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

winVer = GetWindowsVersionString()[18:]
WIN_7 = not (winVer.startswith('10') or winVer.startswith('8'))

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

if WIN_7:
    monGUID = '{02731015-4510-4526-99e6-e5a17ebd1aea}'
else:
    monGUID = '{6fe69556-704a-47a0-8f24-c28d936fda47}'

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
GUID_CONSOLE_DISPLAY_STATE = GUID(monGUID)

POWER_MESSAGES = {
    GUID_CONSOLE_DISPLAY_STATE: {
        MON_OFF: dict(
            event='Monitor.Off',
            description='Monitor State is Off'
        ),
        MON_ON: dict(
            event='Monitor.On',
            description='Monitor State is On'
        ),
        MON_DIM: dict(
            event='Monitor.Dim',
            description=(
                'Monitor has been dimmed\n'
                '(usually when on battery)\n'
                '(Windows 8+)'
            )
        )
    },
    GUID_SYSTEM_AWAYMODE: {
        AWY_EXITING: dict(
            event='AwayMode.Exiting',
            description='Exiting Away Mode'
        ),
        AWY_ENTERING: dict(
            event='AwayMode.Entering',
            description='Entering Away Mode'
        )
    },
    GUID_ACDC_POWER_SOURCE: {
        PWR_AC: dict(
            event='PowerSource.Line',
            description='Line (AC) Power Source'
        ),
        PWR_DC: dict(
            event='PowerSource.Battery',
            description='Battery (DC) Power Source'
        ),
        PWR_UPS: dict(
            event='PowerSource.UPS',
            description='Battery Backup (UPS) Power Source'
        )
    },
    GUID_BATTERY_PERCENTAGE_REMAINING: {
        i: dict(
            event='BatteryLevel.' + str(i) + '%',
            description='Battery Level at ' + str(i) + '%'
        ) for i in range(101)
    },
    GUID_POWER_SAVING_STATUS: {
        SVR_OFF: dict(
            event='PowerSaving.Off',
            description=(
                'Power Saving Turned Off\n'
                '(usually when on battery)'
            )
        ),
        SVR_ON: dict(
            event='PowerSaving.On',
            description=(
                'Power Saving Turned On\n'
                '(usually when on battery'
            )
        )
    },
    GUID_POWERSCHEME_PERSONALITY: {
        GUID_MIN_POWER_SAVINGS: dict(
            event='PowerProfile.PowerSaver',
            description=(
                'Power Plan has been changed to\n'
                'Power Saving'
            )
        ),
        GUID_MAX_POWER_SAVINGS: dict(
            event='PowerProfile.HighPerformance',
            description=(
                'Power Plan has been changed to\n'
                'High Performance'
            )
        ),
        GUID_TYPICAL_POWER_SAVINGS: dict(
            event='PowerProfile.Balanced',
            description=(
                'Power Plan has been changed to\n'
                'Balanced'
            )
        )
    },
    PBT_APMBATTERYLOW: dict(
        event='BatteryLevel.Low',
        description=(
            'Battery Level is low\n'
            '(Available only before Windows Vista)'
        )
    ),
    PBT_APMOEMEVENT: dict(
        event='OemEvent',
        description=(
            'Have no clue. roll the dice\n'
            '(Available only before Windows Vista)'
        )
    ),
    PBT_APMQUERYSUSPENDFAILED: dict(
        event='QuerySuspendFailed',
        description=(
            'Permission to suspend the computer was denied\n'
            '(Available only before Windows Vista)'
        )
    ),
    PBT_APMRESUMECRITICAL: dict(
        event='ResumeCritical',
        description=(
            'Resume after critical suspension caused by a failing battery\n'
            '(Available only before Windows Vista)'
        )
    ),
    PBT_APMQUERYSUSPEND: dict(
        event='QuerySuspend',
        description=(
            'A request for permission to suspend the computer has been made\n'
            '(Available only before Windows Vista)'
        )
    ),
    PBT_APMRESUMEAUTOMATIC: dict(
        event='Resuming',
        description='System is Resuming from sleep or hibernation'
    ),
    PBT_APMRESUMESUSPEND: dict(
        event='Resumed',
        description='System has Resumed from sleep or hibernation'
    ),
    PBT_APMSUSPEND: dict(
        event='Suspend',
        description='System is going to sleep or hibernation'
    )
    # PBT_APMPOWERSTATUSCHANGE: "PowerStatusChange",
}


def Register(guid):
    return windll.user32.RegisterPowerSettingNotification(
        eg.messageReceiver.hwnd,
        byref(guid),
        0
    )


def Unregister(cls):
    return windll.user32.UnregisterDeviceNotification(cls)


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


def CreatePowerClass(lParam, cls):
    powerBroadcast = cast(lParam, POINTER(cls))
    powerSetting = powerBroadcast.contents.PowerSetting
    data = powerBroadcast.contents.Data
    msgs = POWER_MESSAGES.get(powerSetting, None)
    if msgs is not None:
        return msgs.get(data, None)


class PowerBroadcastNotifier:
    def __init__(self, plugin):

        def CreateEventList(d, e=()):
            if 'event' in d:
                e += ((d['event'], d['description']),)
            else:
                for key in sorted(d.keys()):
                    e = CreateEventList(d[key], e)
            return e

        self.plugin = plugin
        self.plugin.AddEvents(*CreateEventList(POWER_MESSAGES))

        self.monitorNotify = Register(GUID_CONSOLE_DISPLAY_STATE)
        self.awayNotify = Register(GUID_SYSTEM_AWAYMODE)
        self.sourceNotify = Register(GUID_ACDC_POWER_SOURCE)
        self.batteryNotify = Register(GUID_BATTERY_PERCENTAGE_REMAINING)
        self.savingNotify = Register(GUID_POWER_SAVING_STATUS)
        self.schemeNotify = Register(GUID_POWERSCHEME_PERSONALITY)

        eg.messageReceiver.AddHandler(
            WM_POWERBROADCAST,
            self.OnPowerBroadcast
        )

    def Close(self):
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
            msg = CreatePowerClass(lParam, msgCls.pop(0))

        if msg is not None:
            eg.eventThread.TriggerEventWait(
                suffix=msg['event'],
                prefix="System",
                source=self.plugin
            )

        if wParam == PBT_APMSUSPEND:
            eg.actionThread.CallWait(eg.actionThread.OnComputerSuspend)
        return 1
