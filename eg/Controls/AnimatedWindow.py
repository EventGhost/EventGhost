import eg
import wx
import Image
from math import sin
import time


class AnimatedWindow(wx.PyWindow):
    
    def __init__(self, parent, id=-1):
        wx.PyWindow.__init__(self, parent, id)
        self.font = wx.Font(
            40, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD
        )
        im = Image.open("images/logo.png").convert("RGBA")
        self.im1 = Image.fromstring("L", im.size, im.tostring()[3::4])
        self.im2 = Image.new("L", im.size, 0)
        self.image = wx.EmptyImage(im.size[0], im.size[1], 32)
        self.image.SetData(im.convert('RGB').tostring())
        self.bmpWidth = im.size[0]
        self.bmpHeight = im.size[1]
        self.time = time.clock()
        self.count = 0
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TIMER, self.UpdateDrawing)
        self.OnSize(None)
        self.timer = wx.Timer(self)
        self.timer.Start(10)
        
        
    @eg.LogIt
    def AcceptsFocus(self):
        return False
        
        
    @eg.LogIt
    def AcceptsFocusFromKeyboard(self):
        return False
        
        
    def OnSize(self, event):
        self.width, self.height = self.GetClientSizeTuple()
        self.dcBuffer = wx.EmptyBitmap(self.width, self.height)
        self.y3 = (self.height - self.bmpHeight) / 4.0
        self.x3 = (self.width - self.bmpWidth) / 4.0
        textWidth, _, _, _ = self.GetFullTextExtent("EventGhost", self.font) 
        self.textOffset = (self.width - textWidth) / 2
        self.UpdateDrawing()


    def UpdateDrawing(self, event=None):
        dc = wx.BufferedDC(wx.ClientDC(self), self.dcBuffer)
        self.Draw(dc)


    def Draw(self, dc):
        dc.BeginDrawing()
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear() # make sure you clear the bitmap!
        dc.SetFont(self.font)
        dc.DrawText("EventGhost", self.textOffset, 50)
        t = time.clock() / 2.0
        y3 = self.y3
        x3 = self.x3
        y = (sin(t) + sin(1.8 * t)) * y3 + y3 * 2.0
        x = (sin(t * 0.8) + sin(1.9 * t)) * x3 + x3 * 2.0
        alpha = sin(t) / 2.0 + 0.5
        
        im = Image.blend(self.im1, self.im2, alpha)
        self.image.SetAlphaData(im.tostring()) 
        bmp = wx.BitmapFromImage(self.image, 24)
        dc.DrawBitmap(bmp, x, y, True)
        dc.EndDrawing()


