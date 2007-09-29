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

import eg

import win32con


PBT_POWERSETTINGCHANGE = 0x8013

PbtMessages = {
    win32con.PBT_APMBATTERYLOW: "BatteryLow", # not in vista, use 
                                              # PBT_APMPOWERSTATUSCHANGE instead
    win32con.PBT_APMOEMEVENT: "OemEvent",
    win32con.PBT_APMPOWERSTATUSCHANGE: "PowerStatusChange",
    win32con.PBT_APMQUERYSUSPEND: "QuerySuspend",
    win32con.PBT_APMQUERYSUSPENDFAILED: "QuerySuspendFailed",
    win32con.PBT_APMRESUMEAUTOMATIC: "ResumeAutomatic",
    win32con.PBT_APMRESUMECRITICAL: "ResumeCritical",
    win32con.PBT_APMRESUMESUSPEND: "Resume",
    win32con.PBT_APMSUSPEND: "Suspend",
    PBT_POWERSETTINGCHANGE: "PowerSettingsChange",
}


class PowerBroadcastNotifier:
    
    def __init__(self, plugin):
        self.plugin = plugin
        eg.messageReceiver.AddHandler(
            win32con.WM_POWERBROADCAST, 
            self.OnPowerBroadcast
        )


    def Close(self):
        eg.messageReceiver.RemoveHandler(
            win32con.WM_POWERBROADCAST, 
            self.OnPowerBroadcast
        )
        
        
    @eg.LogIt
    def OnPowerBroadcast(self, hwnd, msg, wparam, lparam):
        msg = PbtMessages.get(wparam, None)
        if msg is not None:
            eg.eventThread.TriggerEventWait(
                msg, 
                prefix="System", 
                source=self.plugin
            )
        return 1
