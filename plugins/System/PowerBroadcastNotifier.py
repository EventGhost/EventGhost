# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$


from eg.WinApi.Dynamic import (
    WM_POWERBROADCAST, PBT_APMSUSPEND, PBT_APMRESUMEAUTOMATIC, 
    PBT_APMBATTERYLOW, PBT_APMOEMEVENT, PBT_APMPOWERSTATUSCHANGE, 
    PBT_APMQUERYSUSPEND, PBT_APMQUERYSUSPENDFAILED, PBT_APMRESUMECRITICAL,
    PBT_APMRESUMESUSPEND, 
)

PBT_POWERSETTINGCHANGE = 0x8013

PbtMessages = {
    PBT_APMBATTERYLOW: "BatteryLow", # not in vista, use 
                                     # PBT_APMPOWERSTATUSCHANGE instead
    PBT_APMOEMEVENT: "OemEvent",
    PBT_APMPOWERSTATUSCHANGE: "PowerStatusChange",
    PBT_APMQUERYSUSPEND: "QuerySuspend",
    PBT_APMQUERYSUSPENDFAILED: "QuerySuspendFailed",
    PBT_APMRESUMEAUTOMATIC: "ResumeAutomatic",
    PBT_APMRESUMECRITICAL: "ResumeCritical",
    PBT_APMRESUMESUSPEND: "Resume",
    PBT_APMSUSPEND: "Suspend",
    PBT_POWERSETTINGCHANGE: "PowerSettingsChange",
}


class PowerBroadcastNotifier:
    
    def __init__(self, plugin):
        self.plugin = plugin
        eg.messageReceiver.AddHandler(WM_POWERBROADCAST, self.OnPowerBroadcast)


    def Close(self):
        eg.messageReceiver.RemoveHandler(WM_POWERBROADCAST, self.OnPowerBroadcast)
        
        
    @eg.LogIt
    def OnPowerBroadcast(self, hwnd, msg, wparam, lparam):
        if wparam == PBT_APMRESUMEAUTOMATIC:
            eg.actionThread.CallWait(eg.actionThread.OnComputerResume)
        msg = PbtMessages.get(wparam, None)
        if msg is not None:
            eg.eventThread.TriggerEventWait(
                msg, 
                prefix="System", 
                source=self.plugin
            )
        if wparam == PBT_APMSUSPEND:
            eg.actionThread.CallWait(eg.actionThread.OnComputerSuspend)
        return 1
