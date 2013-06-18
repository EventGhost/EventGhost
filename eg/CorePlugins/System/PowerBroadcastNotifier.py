import eg

import win32con

PBT_POWERSETTINGCHANGE = 0x8013

PbtMessages = {
    win32con.PBT_APMBATTERYLOW: "BatteryLow",
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
        
        
    def OnPowerBroadcast(self, hwnd, msg, wparam, lparam):
        eg.whoami()
        msg = PbtMessages.get(wparam, None)
        if msg is not None:
            eg.eventThread.TriggerEventWait(
                msg, 
                prefix="System", 
                source=self.plugin
            )
        return 1
