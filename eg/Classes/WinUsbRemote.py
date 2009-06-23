import sys
import os

import eg
from eg.WinApi.Dynamic import (
    cast,
    POINTER,
    c_ubyte,
    WinDLL,
    WM_USER,
)

P_UBYTE = POINTER(c_ubyte)


class WinUsbRemote(object):
    threadId = None
    dll = None
    
    def __init__(
        self, 
        deviceInterfaceGuid, 
        callback, 
        dataSize=1, 
        suppressRepeat=False
    ):
        if self.dll is None:
            self.__class__.dll = WinDLL(
                os.path.join(
                    eg.MAIN_DIR, 
                    "lib%d%d" % sys.version_info[:2], 
                    "site-packages", 
                    "WinUsbWrapper.dll"
                )
            )
        
        self.callback = callback
        self.dataSize = dataSize
        self.msgId = eg.messageReceiver.AddWmUserHandler(self.WindowProcedure)
        self.threadId = self.dll.Start(
            eg.messageReceiver.hwnd,
            self.msgId,
            unicode(deviceInterfaceGuid),
            dataSize,
            int(suppressRepeat)
        )
        
    
    def IsOk(self):
        return bool(self.threadId)
    
    
    def Close(self):
        self.dll.End(self.threadId)
        eg.messageReceiver.RemoveWmUserHandler(self.WindowProcedure)


    def WindowProcedure(self, hwnd, msg, wParam, lParam):
        p = cast(lParam, P_UBYTE)
        value = [p[i] for i in range(self.dataSize)]
        self.callback(value)
        return 1
        