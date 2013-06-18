import eg
from win32ts import (
    WTSRegisterSessionNotification, 
    WTSUnRegisterSessionNotification,
    NOTIFY_FOR_ALL_SESSIONS,
    WTSQuerySessionInformation,
    WTSUserName,
    WTS_CURRENT_SERVER_HANDLE)

WM_WTSSESSION_CHANGE = 0x02B1

WTS_WPARAM_DICT = {
    1: "ConsoleConnect",
    2: "ConsoleDisconnect",
    3: "RemoteConnect",
    4: "RemoteDisconnect",
    5: "SessionLogon",
    6: "SessionLogoff",
    7: "SessionLock",
    8: "SessionUnlock",
    9: "SessionRemoteControl"}


class SessionChangeNotifier:
    
    def __init__(self, plugin):
        self.TriggerEvent = plugin.TriggerEvent
        eg.messageReceiver.AddHandler(
            WM_WTSSESSION_CHANGE, 
            self.OnSessionChange)
        WTSRegisterSessionNotification(
            eg.messageReceiver.hwnd, 
            NOTIFY_FOR_ALL_SESSIONS)
    
    
    def Close(self):
        WTSUnRegisterSessionNotification(eg.messageReceiver.hwnd)
        eg.messageReceiver.RemoveHandler(
            WM_WTSSESSION_CHANGE, 
            self.OnSessionChange)
        
        
    def OnSessionChange(self, hwnd, msg, wparam, lparam):
        eg.whoami()
        eventstring = WTS_WPARAM_DICT.get(wparam, None)
        if eventstring is not None:
            userName = WTSQuerySessionInformation(
                WTS_CURRENT_SERVER_HANDLE, 
                lparam, 
                WTSUserName)
            self.TriggerEvent(eventstring, [userName])
        return 1