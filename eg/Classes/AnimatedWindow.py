# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$


import wx
from math import sin
import time
 

class AnimatedWindow(wx.PyWindow):
    
    def __init__(self, parent):
        wx.PyWindow.__init__(self, parent)
        self.font = wx.Font(
            40, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD
        )
        self.SetBackgroundColour((255,255,255))
        self.logo1 = wx.Bitmap("images/opensource-55x48.png")
        self.logo2 = wx.Bitmap("images/python-powered-w-100x40.png")
        self.logo3 = wx.Bitmap("images/logo2.png")
        self.image = wx.Image("images/logo.png", wx.BITMAP_TYPE_PNG)
        self.bmpWidth = self.image.GetWidth()
        self.bmpHeight = self.image.GetHeight()
        self.time = time.clock()
        self.count = 0
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TIMER, self.UpdateDrawing)
        self.OnSize(None)
        self.timer = wx.Timer(self)
        self.timer.Start(10)
        
        
    def MakeBackground(self):
        self.backbuffer = wx.EmptyBitmap(self.width, self.height)
        dc = wx.MemoryDC()
        dc.SelectObject(self.backbuffer)
        dc.BeginDrawing()
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear() # make sure you clear the bitmap!
        dc.SetFont(self.font)
        dc.SetTextForeground((128, 128, 128))
        
        w1 = self.logo1.GetWidth()
        w2 = self.logo2.GetWidth()
        h1 = self.logo1.GetHeight()
        h2 = self.logo2.GetHeight()
        h = max(h1, h2)
        
        dc.DrawBitmap(
            self.logo1, 
            self.width - w1 - w2, 
            self.height - h + (h - h1) // 2, 
            True
        )
        dc.DrawBitmap(
            self.logo2, 
            self.width - w2, 
            self.height - h + (h - h2) // 2, 
            True
        )
        dc.DrawBitmap(
            self.logo3, 
            (self.width - self.logo3.GetWidth()) // 2, 
            (self.height - self.logo3.GetHeight()) // 3, 
            True
        )
        dc.EndDrawing()
        
        
    def AcceptsFocus(self):
        return False
        
        
    def AcceptsFocusFromKeyboard(self):
        return False
        
        
    def OnSize(self, event):
        self.width, self.height = self.GetClientSizeTuple()
        self.dcBuffer = wx.EmptyBitmap(self.width, self.height)
        self.y3 = (self.height - self.bmpHeight) / 4.0
        self.x3 = (self.width - self.bmpWidth) / 4.0
        self.MakeBackground()
        self.UpdateDrawing()


    def UpdateDrawing(self, event=None):
        dc = wx.BufferedDC(wx.ClientDC(self), self.dcBuffer)
        self.Draw(dc)


    def Draw(self, dc):
        dc.BeginDrawing()
        dc.DrawBitmap(self.backbuffer, 0, 0, False)
        t = time.clock() / 2.0
        y3 = self.y3
        x3 = self.x3
        y = (sin(t) + sin(1.8 * t)) * y3 + y3 * 2.0
        x = (sin(t * 0.8) + sin(1.9 * t)) * x3 + x3 * 2.0
        alpha = sin(t) / 2.0 + 0.5
        image = self.image.AdjustChannels(1.0, 1.0, 1.0, alpha)
        bmp = wx.BitmapFromImage(image, 24)
        dc.DrawBitmap(bmp, x, y, True)
        dc.EndDrawing()


