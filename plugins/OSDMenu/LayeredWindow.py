import wx, win32api, win32con, win32gui, ctypes, time

## ctypes
updateLayeredWindow = ctypes.windll.user32.UpdateLayeredWindow

BYTE = ctypes.c_ubyte
LONG = ctypes.c_long

##transparentColor = (255, 255, 255)
transparentColor = (0,0,0)

class LayeredWindow(wx.Frame):
    def __init__(self, alpha=255, **kwargs):
        super(LayeredWindow, self).__init__(None, wx.ID_ANY, "On Screen",
            style=wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.TRANSPARENT_WINDOW | wx.NO_BORDER)

        self.alpha=alpha
        for kw in kwargs.keys():
            if kw=="size" : self.SetSize(kwargs[kw])

    def UpdateWindow(self, alpha=''):
        if alpha=='' : alpha = self.alpha
        ## Set WS_EX_LAYERED
        style = win32gui.GetWindowLong(self.GetHandle(), win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(self.GetHandle(), win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED)
        
        screenDC = win32gui.GetDC(win32gui.GetDesktopWindow())
        cScreenDC = win32gui.CreateCompatibleDC(screenDC)
       
        win32gui.SelectObject(cScreenDC, self.bmp.GetHandle())
        point1 = POINT(*self.GetPosition())
        size1 = SIZE(*self.GetClientSize())
        point2 = POINT(0,0)
        blend = BLENDFUNCTION(0, 0, alpha, 1)
        ret = updateLayeredWindow(self.GetHandle(),screenDC,
                ctypes.byref(point1), ctypes.byref(size1),cScreenDC,
                ctypes.byref(point2),win32api.RGB(*transparentColor),
                ctypes.byref(blend),win32con.ULW_ALPHA)
        return ret

    def FadeIn(self, steps):
        for i in range(0, steps):
            self.DrawWindow()
            self.UpdateWindow((self.alpha//steps)*i)
            self.Show()
        self.DrawWindow()
        self.UpdateWindow(self.alpha)
        self.Show()

    def FadeOut(self, steps):
        for i in range(0, steps):
            self.DrawWindow()
            self.UpdateWindow(self.alpha*(steps-i)//steps)
            time.sleep(0.01)
        self.Close()
    
    def DrawWindow(self):
        pass


class POINT(ctypes.Structure):
    _fields_ = [('x', LONG), ('y', LONG)]

class SIZE(ctypes.Structure):
    _fields_ = [('cx', LONG),('cy', LONG)]

class BLENDFUNCTION(ctypes.Structure):
    _fields_ = [('BlendOp', BYTE),('BlendFlags', BYTE),('SourceConstantAlpha', BYTE),('AlphaFormat', BYTE)]
