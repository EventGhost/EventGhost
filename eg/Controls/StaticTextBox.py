import wx


class StaticTextBox(wx.PyWindow):
    
    def __init__(self, parent, id=-1, label='', pos=(-1,-1), size=(-1,-1)):
        wx.Window.__init__(
            self, 
            parent, 
            id, 
            pos, 
            size,
            style=wx.SUNKEN_BORDER
        )
        self.SetMinSize(self.GetSize())
        sizer = wx.BoxSizer(wx.VERTICAL)
        textCtrl = wx.StaticText(self, -1, label)
        sizer.Add((0,0), 1, wx.EXPAND)
        sizer.Add(textCtrl, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5)
        sizer.Add((0,0), 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.textCtrl = textCtrl


    def OnSize(self, event):
        if self.GetAutoLayout():
            self.Layout()


    def SetLabel(self, label):
        self.textCtrl.SetLabel(label)


    def AcceptsFocus(self):
        return False
    
