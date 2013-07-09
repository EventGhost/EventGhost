# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import eg
from eg.WinApi.Dynamic import (
    WM_POWERBROADCAST, PBT_APMSUSPEND, PBT_APMRESUMEAUTOMATIC,
    PBT_APMBATTERYLOW, PBT_APMOEMEVENT, PBT_APMPOWERSTATUSCHANGE,
    PBT_APMQUERYSUSPEND, PBT_APMQUERYSUSPENDFAILED, PBT_APMRESUMECRITICAL,
    PBT_APMRESUMESUSPEND,
)

PBT_POWERSETTINGCHANGE = 0x8013

PBT_MESSAGES = {
    PBT_APMBATTERYLOW: "BatteryLow", # not in vista, use
                                     # PBT_APMPOWERSTATUSCHANGE instead
    PBT_APMOEMEVENT: "OemEvent",
    PBT_APMPOWERSTATUSCHANGE: "PowerStatusChange",
    PBT_APMQUERYSUSPEND: "QuerySuspend", # removed in Vista
    PBT_APMQUERYSUSPENDFAILED: "QuerySuspendFailed", # removed in Vista
    PBT_APMRESUMEAUTOMATIC: "ResumeAutomatic",
    PBT_APMRESUMECRITICAL: "ResumeCritical",
    PBT_APMRESUMESUSPEND: "Resume",
    PBT_APMSUSPEND: "Suspend",
    PBT_POWERSETTINGCHANGE: "PowerSettingsChange",
}


class PowerBroadcastNotifier:

    def __init__(self, plugin):
        self.plugin = plugin
        eg.messageReceiver.AddHandler(
            WM_POWERBROADCAST,
            self.OnPowerBroadcast
        )


    def Close(self):
        eg.messageReceiver.RemoveHandler(
            WM_POWERBROADCAST,
            self.OnPowerBroadcast
        )


    @eg.LogIt
    def OnPowerBroadcast(self, dummyHwnd, msg, wparam, dummyLParam):
        if wparam == PBT_APMRESUMEAUTOMATIC:
            eg.actionThread.Func(eg.actionThread.OnComputerResume)()
        msg = PBT_MESSAGES.get(wparam, None)
        if msg is not None:
            eg.eventThread.TriggerEventWait(
                msg,
                prefix="System",
                source=self.plugin
            )
        if wparam == PBT_APMSUSPEND:
            eg.actionThread.Func(eg.actionThread.OnComputerSuspend)()
        return 1

