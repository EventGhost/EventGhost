import eg
       
import wx
import time
import thread
import threading
import win32gui
import win32con
import winxpgui
from wx.lib.buttons import GenButton
from eg.WinAPI.win32types import GUITHREADINFO, GetGUIThreadInfo
from ctypes import pointer

btnList = [
    (
        "Play",
        "ZPPlay",
    ), (
        "Stop",
        "Stop",
    ), (
        "Open",
        "FileNav",
    ), (
        "DVD Menu",
        "DVDMenu"
    ), (
        "Mute",
        "Mute"
    ),
]


class AnimateButton(GenButton):
    
    def __init__(self, parent, label):
        GenButton.__init__(self, parent, -1, label)
        self.SetForegroundColour((255, 255, 255))
        self.SetBackgroundColour((0, 0, 200))
        self.Bind(wx.EVT_SET_FOCUS, self.OnGainFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnLoseFocus)
        self.Bind(wx.EVT_ENTER_WINDOW, self.SetFocusWrapper)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnButtonLeave)
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.SetUseFocusIndicator(False)
        self.SetFont(font)
        
        
    def OnGainFocus(self, event):
        GenButton.OnGainFocus(self, event)
        self.SetBackgroundColour((200, 0, 0))
        self.Refresh()
        self.GetParent().GetParent().currentButton = self
        
        
    def OnLoseFocus(self, event):
        GenButton.OnLoseFocus(self, event)
        self.SetBackgroundColour((0, 0, 200))
        self.Refresh()
        
        
    def OnButton(self, event):
        self.GetParent().GetParent().ShowMenu(False)
        self.GetParent().GetParent().TriggerEvent(self.eventString)
        event.Skip()
        
        
    def SetFocusWrapper(self, event):
        self.GetParent().GetParent().OnEnter(event)
        self.SetFocus()
        
        
    def OnButtonEnter(self, event):
        self.GetParent().GetParent().OnEnter(event)
        self.SetFocus()
        self.SetBackgroundColour((200, 0, 0))
        self.Refresh()
            
            
    def OnButtonLeave(self, event):
        self.GetParent().GetParent().OnLeave(event)
        #self.SetBackgroundColour((0, 0, 200))
        #self.Refresh()
            
    def EmulateDownClick(self):
        self.up = False
        self.Refresh()
        self.Update()
        
        
    def EmulateUpClick(self):
        self.up = True
        self.Notify()
        self.Refresh()
        self.Update()
        
        
        
class AnimatedFrame(wx.Frame):
    
    def __init__(self):
        self.lastHwnd = None
        self.menuVisible = False
        self.currentButton = None
        self.enterCount = 0
        self.direction = False
        self.timer = threading.Timer(0, self.FireTimer)
        style = wx.NO_BORDER|wx.STAY_ON_TOP|wx.FRAME_NO_TASKBAR|wx.FRAME_SHAPED
        wx.Frame.__init__(self, None, -1, "OSD Menu", style=style)
        
        self.SetBackgroundColour((0, 0, 0))
        panel = wx.Panel(self)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        self.Bind(wx.EVT_ACTIVATE, self.OnActivate)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.region = wx.Region()
        buttons = []
        for buttonData in btnList:
            button = AnimateButton(panel, buttonData[0])
            button.eventString = buttonData[1]
            sizer.Add(button, 0, flag=wx.ALL|wx.EXPAND, border=5)
            buttons.append(button)
        self.buttons = buttons
        
        panel.SetFocus()
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)
        sizer.Fit(panel)
        minSize = sizer.GetMinSize()
        panel.SetMinSize(minSize)
        self.SetSize(minSize)
        self.width = self.GetSizeTuple()[0]
        
        #self.offset = 2100
        self.offset = 0
        for btn in buttons:
            self.region.UnionRect(btn.GetRect())
        self.SetShape(self.region)
        self.SetPosition((self.offset - self.width, 220))
        self.ShowOnNewPosition(-self.width, True)
        self.Show()
        thread.start_new_thread(self.Animate, ())


    def ShowOnNewPosition(self, x, direction):
        w, h = self.GetSizeTuple()
        region = wx.Region(-1 * x, 0, w - x, h)
        region.IntersectRegion(self.region)
        if region.IsEmpty():
            region = wx.Region(-1 * x, 0, w - x, h)
        if direction:
            self.SetPosition((self.offset + x, -1))
            self.SetShape(region)
        else:
            self.SetShape(region)
            self.SetPosition((self.offset + x, -1))
        #self.Update()
            
            
    def ShowMenu(self, show_flag=True):
        self.direction = show_flag
        if show_flag and not self.menuVisible:
            self.menuVisible = True
            guiTreadInfo = GUITHREADINFO()
            if GetGUIThreadInfo(0, pointer(guiTreadInfo)):
                self.lastHwnd = guiTreadInfo.hwndFocus
            else:
                self.lastHwnd = None
            #self.lastHwnd = win32gui.GetForegroundWindow()
            #eg.WinAPI.Utils.BringHwndToFront(self.GetHandle())
            #win32gui.SetWindowPos(self.GetHandle(),
            #                    win32con.HWND_TOPMOST,
            #                    0,0,0,0,
            #                    win32con.SWP_NOMOVE|win32con.SWP_NOSIZE)#|win32con.SWP_NOACTIVATE)
            self.currentButton.SetFocus()
        
        
    def Animate(self):
        x = 0
        width = self.width
        while 1:
            if self.direction:
                if x < width:
                    x += 8
                    x = min(x, width)
                    wx.CallAfter(self.ShowOnNewPosition, x - width, True)
            else:
                if x > 0:
                    x -= 8
                    x = max(0, x)
                    wx.CallAfter(self.ShowOnNewPosition, x - width, False)
                elif x == 0:
                    if self.menuVisible:
                        self.menuVisible = False
                        #win32gui.SetWindowPos(self.GetHandle(),
                        #    win32con.HWND_BOTTOM,
                        #    0,0,0,0,
                        #    win32con.SWP_NOMOVE|win32con.SWP_NOSIZE)
                        #if self.lastHwnd:
                        #    wx.CallAfter(eg.WinAPI.Utils.BringHwndToFront, self.lastHwnd)
                    
                    ms = wx.GetMouseState()
                    if ms.x == 0:
                        #self.buttons[0].SetFocus()
                        self.ShowMenu()
            time.sleep(0.01)


    def FireTimer(self, direction):
        self.ShowMenu(direction)
        
        
    def OnActivate(self, event):
        eg.whoami()
        if (event.GetActive()):
            return
        self.ShowMenu(event.GetActive())
        
        
    def OnEnter(self, event):
        self.enterCount += 1
        if self.enterCount == 1:
            self.timer.cancel()
            self.ShowMenu(True)
            
            
    def OnLeave(self, event):
        self.enterCount -= 1
        if self.enterCount == 0 and self.IsShown():
            self.timer.cancel()
            self.timer = threading.Timer(1.0, self.FireTimer, (False,))
            self.timer.start()
            
            
    def DoDown(self):
        try:
            pos = self.buttons.index(self.currentButton)
        except:
            pos = 0
        pos += 1
        if pos >= len(self.buttons):
            pos = 0
        self.buttons[pos].SetFocus()
        
    
    def DoUp(self):
        try:
            pos = self.buttons.index(self.currentButton)
        except:
            pos = len(self.buttons)
        pos -= 1
        if pos < 0:
            pos = len(self.buttons) - 1
        self.buttons[pos].SetFocus()
    
    
    def DoEnter(self):
        if self.currentButton is not None:
            wx.CallAfter(self.currentButton.EmulateDownClick)
            eg.event.AddUpFunc(wx.CallAfter, self.currentButton.EmulateUpClick)
            
            
font = wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)



class OsdMenu(eg.PluginClass):
    
    def __init__(self):
        def make():
            self.frame = AnimatedFrame()
            self.frame.TriggerEvent = self.TriggerEvent
        wx.CallAfter(make)
        self.AddAllActions()
        
    
    
class Show(eg.ActionClass):
    
    def __call__(self):
        frame = self.plugin.frame
        frame.ShowMenu(not frame.direction)
        
        
        
class Down(eg.ActionClass):
    
    def __call__(self):
        self.plugin.frame.DoDown()
        
        
        
class Up(eg.ActionClass):
    
    def __call__(self):
        self.plugin.frame.DoUp()
        
        
        
class Enter(eg.ActionClass):
    
    def __call__(self):
        self.plugin.frame.DoEnter()
        
        