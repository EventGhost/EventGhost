import wx
import eg
from eg.IconTools import GetIcon



class StatusBar(wx.StatusBar):
    
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)
        self.sizeChanged = False
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.SetFieldsCount(2)
        self.SetStatusWidths([-1, 40])
        self.icons = [
            GetIcon("images\\Tray1.png"),
            GetIcon("images\\Tray3.png"),
            GetIcon("images\\Tray2.png"),
        ]
        self.icon = wx.StaticBitmap(self, -1, self.icons[0], (0,0), (16,16))
        rect = self.GetFieldRect(0)
        self.cb = wx.CheckBox(self, -1, eg.text.MainFrame.onlyLogAssigned)
        #self.cb.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_MENUBAR))
        self.cb.SetValue(eg.onlyLogAssigned)
        self.cb.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)
        self.cb.SetPosition((rect.x+2, rect.y+2))
        self.Reposition()


    def OnSize(self, evt):
        self.Reposition()  # for normal size events
        self.sizeChanged = True


    def OnIdle(self, evt):
        if self.sizeChanged:
            self.Reposition()


    def Reposition(self):
        rect = self.GetFieldRect(1)
        y = rect.y + (rect.height - 16) / 2
        self.icon.SetPosition((rect.x + 5, y))
        self.sizeChanged = False
                
        
    def OnCheckBox(self, event):
        eg.whoami()
        eg.onlyLogAssigned = self.cb.GetValue()
        
        
    def SetState(self, flag):
        self.icon.SetBitmap(self.icons[flag])
            