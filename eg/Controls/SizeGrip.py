
from wx import PyWindow
from win32api import GetSystemMetrics, GetModuleHandle
from win32gui import CreateWindow
from win32con import (
    WS_CHILD, WS_VISIBLE, SBS_SIZEGRIP, SBS_SIZEBOXTOPLEFTALIGN,
    SM_CYHSCROLL, SM_CXVSCROLL
)


class SizeGrip(PyWindow):
    
    def __init__(self, parent, id=-1):
        PyWindow.__init__(self, parent, id)
        w = GetSystemMetrics(SM_CYHSCROLL)
        h = GetSystemMetrics(SM_CXVSCROLL)
        self.SetMinSize((w, h))
        self.SetMaxSize((w, h))

        self.sizeGripHandle = CreateWindow(
            "Scrollbar",
            None,
            WS_CHILD|WS_VISIBLE|SBS_SIZEGRIP|SBS_SIZEBOXTOPLEFTALIGN,
            0, 0, 0, 0,
            self.GetHandle(),
            0,
            GetModuleHandle(None),
            None
        )


    def AcceptsFocus(self):
        return False
    
