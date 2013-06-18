import eg
from win32con import WM_DEVICECHANGE
from eg.WinAPI.win32types import (
    DEV_BROADCAST_DEVICEINTERFACE,
    DEV_BROADCAST_VOLUME,
    DBT_DEVICEARRIVAL,
    DBT_DEVICEREMOVECOMPLETE,
    DBT_DEVTYP_VOLUME,
    DBT_DEVTYP_DEVICEINTERFACE,
    RegisterDeviceNotification,
    UnregisterDeviceNotification,
    pointer,
)



def DriveLettersFromMask(mask):
    return [
        chr(65 + driveNum) 
            for driveNum in range(0, 26) 
                if (mask & (2 ** driveNum))
    ]
        


class DeviceChangeNotifier:
    
    def __init__(self, plugin):
        self.TriggerEvent = plugin.TriggerEvent
        eg.messageReceiver.AddHandler(WM_DEVICECHANGE, self.OnDeviceChange)
        self.handle = RegisterDeviceNotification(
            eg.messageReceiver.hwnd, 
            pointer(
                DEV_BROADCAST_DEVICEINTERFACE(
                    dbcc_devicetype = DBT_DEVTYP_DEVICEINTERFACE,
                    dbcc_classguid = "{53f56307-b6bf-11d0-94f2-00a0c91efb8b}"
                )
            ),
            0
        )
    
    
    def Close(self):
        UnregisterDeviceNotification(self.handle)
        eg.messageReceiver.RemoveHandler(WM_DEVICECHANGE, self.OnDeviceChange)
        
        
    def OnDeviceChange(self, hwnd, msg, wparam, lparam):
        #
        # WM_DEVICECHANGE:
        #  wParam - type of change: arrival, removal etc.
        #  lParam - what's changed?
        #    if it's a volume then...
        #  lParam - what's changed more exactly
        #
        if wparam == DBT_DEVICEARRIVAL:
            dbcv = DEV_BROADCAST_VOLUME.from_address(lparam)
            if dbcv.dbcv_devicetype == DBT_DEVTYP_VOLUME:
                for driveLetter in DriveLettersFromMask(dbcv.dbcv_unitmask):
                    self.TriggerEvent("DriveMounted." + driveLetter)
        elif wparam == DBT_DEVICEREMOVECOMPLETE:
            dbcv = DEV_BROADCAST_VOLUME.from_address(lparam)
            if dbcv.dbcv_devicetype == DBT_DEVTYP_VOLUME:
                for driveLetter in DriveLettersFromMask(dbcv.dbcv_unitmask):
                    self.TriggerEvent("DriveRemoved." + driveLetter)
        return 1