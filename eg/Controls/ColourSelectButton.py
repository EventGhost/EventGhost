import wx
import wx.lib.colourselect as csel



class ColourSelectButton(csel.ColourSelect):
    
    def __init__(
        self, 
        parent, 
        id, 
        label="", 
        colour=wx.BLACK,
        pos=wx.DefaultPosition, 
        size=wx.DefaultSize,
        callback=None, 
        style=0
    ):
        csel.ColourSelect.__init__(
            self, 
            parent, 
            id, 
            label, 
            colour, 
            pos, 
            size,
            callback, 
            style
        )
        self.Bind(wx.EVT_SIZE, self._OnSize)
        
        
    def _OnSize(self, event):
        bmp = self.MakeBitmap()
        self.SetBitmap(bmp)
        if self.label:
            w = self.GetParent().GetTextExtent(self.label)[0] + 18
        else:
            w = 20
        self.SetMinSize((w,-1))
        event.Skip()
        
        
    def MakeBitmap(self):
        bdr = 8
        width, height = self.GetSize()
        _, height = self.GetDefaultSize()
        bmp = wx.EmptyBitmap(width-bdr, height-bdr)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetFont(self.GetFont())
        label = self.GetLabel()
        # Just make a little colored bitmap
        dc.SetBackground(wx.Brush(self.colour))
        dc.Clear()

        if label:
            # Add a label to it
            avg = reduce(lambda a, b: a + b, self.colour.Get()) / 3
            fcolour = avg > 128 and wx.BLACK or wx.WHITE
            dc.SetTextForeground(fcolour)
            dc.DrawLabel(
                label, 
                (0,0, width-bdr, height-bdr),
                wx.ALIGN_CENTER
            )
            
        dc.SelectObject(wx.NullBitmap)
        return bmp
    
    
    def GetColour(self):
        # Converts the wx.Colour object to an RGB-tuple. 
        colour = csel.ColourSelect.GetColour(self)
        return colour.Red(), colour.Green(), colour.Blue()
