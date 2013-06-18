import eg
from ThreadWorker import ThreadWorker

import win32gui
import win32api
import win32con



class MessageReceiver(ThreadWorker):
    """
    A thread with a hidden window to receive win32 messages for different 
    purposes.
    """
    def __init__(self):
        self.messageProcs = {}
        self.multipleMessageProcs = {}
        ThreadWorker.__init__(self)
        
        
    def Init2(self):
        eg.whoami()
        wc = win32gui.WNDCLASS()
        wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = "HiddenMessageReceiver"
        wc.style = win32con.CS_VREDRAW|win32con.CS_HREDRAW;
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = self.messageProcs
        classAtom = win32gui.RegisterClass(wc)
        self.hwnd = win32gui.CreateWindow(
            classAtom,
            "HiddenMessageReceiver",
            win32con.WS_OVERLAPPED|win32con.WS_SYSMENU,
            0, 
            0,
            win32con.CW_USEDEFAULT, 
            win32con.CW_USEDEFAULT,
            0, 
            0,
            wc.hInstance, 
            None
        )
        self.wc = wc
        self.classAtom = classAtom
        self.hinst = wc.hInstance
        
        
    def AddHandler(self, mesg, handler):
        if mesg not in self.messageProcs:
            self.multipleMessageProcs[mesg] = [handler]
            self.messageProcs[mesg] = self.MyWndProc
        else:
            self.multipleMessageProcs[mesg].append(handler)
            
        
    def RemoveHandler(self, mesg, handler):
        self.multipleMessageProcs[mesg].remove(handler)
        if len(self.multipleMessageProcs[mesg]) == 0:
            del self.messageProcs[mesg]
            del self.multipleMessageProcs[mesg]
            
    
    def MyWndProc(self, hwnd, mesg, wParam, lParam):
        for handler in self.multipleMessageProcs[mesg]:
            res = handler(hwnd, mesg, wParam, lParam)
            if res == 0:
                return 0
        return 1
    
        
    def close(self):
        eg.whoami()
        self.hwnd = None
        self.stop()
        