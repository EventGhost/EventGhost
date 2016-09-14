# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import wx
from math import sin
from time import clock

# Local imports
from eg.Icons import GetInternalBitmap, GetInternalImage

class AnimatedWindow(wx.PyWindow):
    def __init__(self, parent):
        wx.PyWindow.__init__(self, parent)
        self.font = wx.Font(
            40, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD
        )
        self.SetBackgroundColour((255, 255, 255))
        self.logo1 = GetInternalBitmap("opensource-55x48")
        self.logo2 = GetInternalBitmap("python-powered")
        self.logo3 = GetInternalBitmap("logo2")
        self.image = GetInternalImage("logo")
        self.bmpWidth = self.image.GetWidth()
        self.bmpHeight = self.image.GetHeight()
        self.time = clock()
        self.count = 0
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TIMER, self.UpdateDrawing)
        self.OnSize(None)
        self.timer = wx.Timer(self)
        self.timer.Start(10)

    def AcceptsFocus(self):
        return False

    def AcceptsFocusFromKeyboard(self):
        return False

    def Draw(self, deviceContext):
        deviceContext.BeginDrawing()
        deviceContext.DrawBitmap(self.backbuffer, 0, 0, False)
        t = clock() / 2.0
        y3 = self.y3
        x3 = self.x3
        y = (sin(t) + sin(1.8 * t)) * y3 + y3 * 2.0
        x = (sin(t * 0.8) + sin(1.9 * t)) * x3 + x3 * 2.0
        alpha = sin(t) / 2.0 + 0.5
        image = self.image.AdjustChannels(1.0, 1.0, 1.0, alpha)
        bmp = wx.BitmapFromImage(image, 24)
        deviceContext.DrawBitmap(bmp, x, y, True)
        deviceContext.EndDrawing()

    def MakeBackground(self):
        self.backbuffer = wx.EmptyBitmap(self.width, self.height)
        deviceContext = wx.MemoryDC()
        deviceContext.SelectObject(self.backbuffer)
        deviceContext.BeginDrawing()
        deviceContext.SetBackground(wx.Brush(self.GetBackgroundColour()))
        deviceContext.Clear()  # make sure you clear the bitmap!
        deviceContext.SetFont(self.font)
        deviceContext.SetTextForeground((128, 128, 128))

        width1 = self.logo1.GetWidth()
        width2 = self.logo2.GetWidth()
        height1 = self.logo1.GetHeight()
        height2 = self.logo2.GetHeight()
        height = max(height1, height2)

        deviceContext.DrawBitmap(
            self.logo1,
            self.width - width1 - width2,
            self.height - height + (height - height1) // 2,
            True
        )
        deviceContext.DrawBitmap(
            self.logo2,
            self.width - width2,
            self.height - height + (height - height2) // 2,
            True
        )
        deviceContext.DrawBitmap(
            self.logo3,
            (self.width - self.logo3.GetWidth()) // 2,
            (self.height - self.logo3.GetHeight()) // 3,
            True
        )
        deviceContext.EndDrawing()

    def OnSize(self, dummyEvent):
        self.width, self.height = self.GetClientSizeTuple()
        self.dcBuffer = wx.EmptyBitmap(self.width, self.height)
        self.y3 = (self.height - self.bmpHeight) / 4.0
        self.x3 = (self.width - self.bmpWidth) / 4.0
        self.MakeBackground()
        self.UpdateDrawing()

    def UpdateDrawing(self, dummyEvent=None):
        deviceContext = wx.BufferedDC(wx.ClientDC(self), self.dcBuffer)
        self.Draw(deviceContext)
