import wx


class FontButton(wx.Button):
    
    def __init__(
        self, 
        parent, 
        id=-1,
        label="Font", 
        pos=wx.DefaultPosition, 
        size=wx.DefaultSize, 
        style=0, 
        validator=wx.DefaultValidator, 
        name="font button", 
        fontInfo=None
    ):
        self.fontInfo = fontInfo
        wx.Button.__init__(
            self, 
            parent, 
            id, 
            label, 
            pos, 
            size, 
            style,
            validator, 
            name
        )
        self.Bind(wx.EVT_BUTTON, self.OnFontButton)
        
        
    def OnFontButton(self, event):
        data = wx.FontData()
        if self.fontInfo is not None:
            font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD)
            nfi = wx.NativeFontInfo()
            nfi.FromString(self.fontInfo)
            font.SetNativeFontInfo(nfi)
            data.SetInitialFont(font)
        dlg = wx.FontDialog(self.GetParent(), data)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            self.fontInfo = font.GetNativeFontInfo().ToString()
        dlg.Destroy()       
        
        
    def GetValue(self):
        return self.fontInfo
    
    