## This file is part of EventGhost.
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

import eg

eg.RegisterPlugin(
    name = "Test Patterns",
    author = "Bitmonster",
    version = "0.1." + "$LastChangedRevision$".split()[1],
    description = "Plugin to show some test patterns.",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAV0lEQVR42mNkoBAwgogD"
        "Bw78B9H29g5Qwf/I0gz/GVH5SPKMowaMGkA9A4BK/qNogCpgZECXhvCBFoJpBwcHmAEH"
        "YEYC1drDmED1jQwI0MCABQweA8gHAM1iaBEreN/nAAAAAElFTkSuQmCC"
    ),
)


import wx
import threading
import Image
import ImageDraw
from math import sqrt
from threading import Timer
from eg.WinAPI.Utils import GetMonitorDimensions, BringHwndToFront


def rint(value):
    return int(round(value))
    
    
def pilToImage(pil,alpha=True):
    if alpha:
        image = apply( wx.EmptyImage, pil.size )
        image.SetData( pil.convert( "RGB").tostring() )
        image.SetAlphaData(pil.convert("RGBA").tostring()[3::4])
    else:
        image = wx.EmptyImage(pil.size[0], pil.size[1])
        new_image = pil.convert('RGB')
        data = new_image.tostring()
        image.SetData(data)
    return image


def imageToBitmap(image):
    return image.ConvertToBitmap()


def MakeTextBitmap(text):
    im = Image.new("RGB", (200,200), (0,0,0))
    draw = ImageDraw.Draw(im)
    draw.text((1,1), text)
    del draw
    return imageToBitmap(pilToImage(im, False))
    
    

class DrawFrame(wx.Frame):
    
    def __init__(self, parent=None):
        wx.Frame.__init__(
            self, parent, -1, style=wx.NO_BORDER|wx.FRAME_NO_TASKBAR
        )
        self.drawing = self.Draw
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DCLICK, self.LeftDblClick)
        self.Bind(wx.EVT_KEY_DOWN, self.OnChar)
        self.Bind(wx.EVT_MOTION, self.ShowCursor)
        self.timer = None
        
        
    def OnChar(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            wx.Frame.Show(self, False)
        event.Skip()
            
        
    def OnPaint(self, event=None):
        dc = wx.PaintDC(self)
        self.drawing(dc)


    def Draw(self, dc):
        return
        
        
    def SetDrawing(self, drawFunc, display=0):
        self.drawing = drawFunc
        d = GetMonitorDimensions()[display]
        self.SetDimensions(d.x, d.y, d.width, d.height)
        wx.Frame.Show(self, True)
        BringHwndToFront(self.GetHandle())
        self.SetCursor(wx.StockCursor(wx.CURSOR_BLANK))
        self.Refresh()


    def LeftDblClick(self, event):
        wx.Frame.Show(self, False)
    
    
    def ShowCursor(self, event):
        self.SetCursor(wx.NullCursor)
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(2.0, self.HideCursor)
        self.timer.start()
        event.Skip()
        
        
    def HideCursor(self):
        wx.CallAfter(self.SetCursor, wx.StockCursor(wx.CURSOR_BLANK))



class TestPatterns(eg.PluginClass):
    
    def __init__(self):
        self.frame = DrawFrame(None)
        self.AddAllActions()


    def __close__(self):
        self.frame.Destroy()
        self.frame = None


        
class Focus(eg.ActionClass):
        
    def __call__(self, foregroundColour, backgroundColour, display=0):
        frame = self.plugin.frame
        bmp = wx.EmptyBitmap(40, 40)
        mdc = wx.MemoryDC()
        mdc.SelectObject(bmp)
        mdc.SetPen(wx.Pen(foregroundColour, 1))
        mdc.SetBackground(wx.Brush(backgroundColour))
        mdc.Clear()
        lines = [
            (0, 0), (3, 0), (3, 8), (0, 8), (0, 5), (8, 5), (8, 8),
            (5, 8), (5, 0), (8, 0), (8, 3), (0, 3), (0, 0),
        ]
        for x in (4, 16, 28):
            for y in (4, 16, 28):
                mdc.DrawLines(lines, x, y)
        lines2 = (
            [
                (1, 1), (14, 1), (14, 39), (1, 39), (1, 26), (39, 26), 
                (39, 39), (26, 39), (26, 1), (39, 1), (39, 14), (1, 14), 
                (1, 1),
            ],
            [(2, 14), (2, 2), (14, 2)],
            [(38, 14), (38, 2), (26, 2)],
            [(38, 26), (38, 38), (26, 38)],
            [(14, 38), (2, 38), (2, 26)],
        )
        for lines in lines2:
            mdc.DrawLines(lines)
        mdc.SelectObject(wx.NullBitmap)
        
        def draw(dc):
            w, h = dc.GetSizeTuple()
            startX = (40 - (w % 40)) / 2
            startY = (40 - (h % 40)) / 2
            for x in range(-startX, w, 40):
                for y in range(-startY, h, 40):
                    dc.DrawBitmap(bmp, x, y, False)
            
        frame.SetDrawing(draw, display)
    
    
    def GetLabel(self, *args):
        return self.name
    
    
    def Configure(
        self, 
        foregroundColour=(255,255,255), 
        backgroundColour=(0,0,0),
        display=0,
    ):
        dialog = eg.ConfigurationDialog(self, resizeable=True)
        sizer = wx.FlexGridSizer(3, 2, 5, 5)
        
        st = wx.StaticText(dialog, -1, "Foreground Colour:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
        
        foregroundColourButton = eg.ColourSelectButton(
            dialog, -1, eg.text.General.choose, foregroundColour
        )
        sizer.Add(foregroundColourButton, 0, wx.EXPAND)
        
        st = wx.StaticText(dialog, -1, "Background Colour:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
        
        backgroundColourButton = eg.ColourSelectButton(
            dialog, -1, eg.text.General.choose, backgroundColour
        )
        sizer.Add(backgroundColourButton, 0, wx.EXPAND)
        
        st = wx.StaticText(dialog, -1, "Display:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
        
        displayChoice = eg.DisplayChoice(dialog, -1, display)
        sizer.Add(displayChoice, 0, wx.EXPAND)

        dialog.sizer.Add(sizer, 1, wx.EXPAND)
        
        if dialog.AffirmedShowModal():
            return (
                foregroundColourButton.GetColour(), 
                backgroundColourButton.GetColour(), 
                displayChoice.GetSelection()
            )
        
            
    
class IreWindow(eg.ActionClass):
    aspectChoices = [
        "1:1 Pixelmapping",
        "4:3 Frame",
        "16:9 Frame",
        "4:3 CCIR 601 Frame",
        "16:9 CCIR 601 Frame",
    ]
        
    def __call__(self, foregroundColour, backgroundColour, coverage):
        frame = self.plugin.frame
        frame.SetForegroundColour(foregroundColour)
        frame.SetBackgroundColour(backgroundColour)
        def draw(dc):
            dc.SetPen(wx.Pen(foregroundColour, 1))
            dc.SetBrush(wx.Brush(foregroundColour))
            w, h = frame.GetSizeTuple()
            area = (w * h) * coverage / 100
            width = height = sqrt(area)
            dc.DrawRectangle((w - width) / 2, (h - height) / 2, width, height)
            
        frame.SetDrawing(draw)
    
    
    def GetLabel(self, *args):
        return self.name
    
    
    def Configure(
        self, 
        foregroundColour=(255,255,255), 
        backgroundColour=(0,0,0),
        coverage=25.0,
        aspectRatio = 0,
    ):
        dialog = eg.ConfigurationDialog(self)
        sizer = wx.FlexGridSizer(5, 2, 5, 5)
        
        st = wx.StaticText(dialog, -1, "Foreground Colour:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)

        foregroundColourButton = eg.ColourSelectButton(
            dialog, -1, eg.text.General.choose, foregroundColour
        )
        sizer.Add(foregroundColourButton, 0, wx.EXPAND)
        
        st = wx.StaticText(dialog, -1, "Background Colour:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)

        backgroundColourButton = eg.ColourSelectButton(
            dialog, -1, eg.text.General.choose, backgroundColour
        )
        sizer.Add(backgroundColourButton, 0, wx.EXPAND)
                
        st = wx.StaticText(dialog, -1, "Percent Coverage:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)

        coverageCtrl = eg.SpinNumCtrl(dialog, min=0, max=100, value=coverage)
        sizer.Add(coverageCtrl, 0, wx.EXPAND)
        
        st = wx.StaticText(dialog, -1, "Aspect Ratio:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)

        aspectChoice = wx.Choice(dialog, choices=self.aspectChoices)
        sizer.Add(aspectChoice, 0, wx.EXPAND)
        
        dialog.sizer.Add(sizer, 1, wx.EXPAND)

        if dialog.AffirmedShowModal():
            return (
                foregroundColourButton.GetColour(), 
                backgroundColourButton.GetColour(), 
                coverageCtrl.GetValue()
            )
        
        
        
class Checkerboard(eg.ActionClass):
    
    def __call__(self, foregroundColour, backgroundColour, hCount, vCount, display):
        frame = self.plugin.frame
        frame.SetForegroundColour(foregroundColour)
        frame.SetBackgroundColour(backgroundColour)
        def draw(dc):
            dc.SetPen(wx.Pen(foregroundColour, 1))
            dc.SetBrush(wx.Brush(foregroundColour))
            w, h = dc.GetSizeTuple()
            width = 1.0 * w / hCount
            height = 1.0 * h / vCount
            for x in range(0, hCount):
                for y in range(x % 2, vCount, 2):
                    xpos1 = int(round(width * x))
                    xpos2 = int(round(width * (x + 1)))
                    ypos1 = int(round(height * y))
                    ypos2 = int(round(height * (y + 1)))
                    dc.DrawRectangle(
                        xpos1, 
                        ypos1, 
                        xpos2 - xpos1, 
                        ypos2 - ypos1
                    )
            
        frame.SetDrawing(draw, display)
    
    
    def GetLabel(self, *args):
        return self.name
    
    
    def Configure(
        self, 
        foregroundColour=(255,255,255), 
        backgroundColour=(0,0,0),
        hCount=4, 
        vCount=4,
        display=0
    ):
        dialog = eg.ConfigurationDialog(self)
        sizer = wx.FlexGridSizer(5, 2, 5, 5)
        
        st = wx.StaticText(dialog, -1, "Foreground Colour:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)

        foregroundColourButton = eg.ColourSelectButton(
            dialog, -1, eg.text.General.choose, foregroundColour
        )
        sizer.Add(foregroundColourButton, 0, wx.EXPAND)
        
        st = wx.StaticText(dialog, -1, "Background Colour:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)

        backgroundColourButton = eg.ColourSelectButton(
            dialog, -1, eg.text.General.choose, backgroundColour
        )
        sizer.Add(backgroundColourButton, 0, wx.EXPAND)
        
        st = wx.StaticText(dialog, -1, "Num Horizontal Boxes:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)

        hCountCtrl = eg.SpinIntCtrl(dialog, min=0, max=100, value=hCount)
        sizer.Add(hCountCtrl, 0, wx.EXPAND)
        
        st = wx.StaticText(dialog, -1, "Num Vertical Boxes:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)

        vCountCtrl = eg.SpinIntCtrl(dialog, min=0, max=100, value=vCount)
        sizer.Add(vCountCtrl, 0, wx.EXPAND)
        
        st = wx.StaticText(dialog, -1, "Display:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
        
        displayChoice = eg.DisplayChoice(dialog, -1, display)
        sizer.Add(displayChoice, 0, wx.EXPAND)

        dialog.sizer.Add(sizer, 1, wx.EXPAND)

        if dialog.AffirmedShowModal():
            return (
                foregroundColourButton.GetColour(), 
                backgroundColourButton.GetColour(), 
                hCountCtrl.GetValue(),
                vCountCtrl.GetValue(),
                displayChoice.GetSelection(),
            )



class Grid(eg.ActionClass):
    
    def __call__(
        self, 
        foregroundColour=(255,255,255),
        backgroundColour=(0,0,0),
        hCount=4, 
        vCount=4,
        display=0
    ):
        def draw(dc):
            dc.SetBackground(wx.Brush(backgroundColour))
            dc.Clear()
            dc.SetPen(wx.Pen(foregroundColour, 1))
            dc.SetBrush(wx.Brush(foregroundColour))
            w, h = dc.GetSizeTuple()
            width = 1.0 * w / hCount
            height = 1.0 * h / vCount
            for i in range(1, hCount):
                x = int(round(width * i))
                dc.DrawLine(x, 0, x, h)
            for i in range(1, vCount):
                y = int(round(height * i))
                dc.DrawLine(0, y, w, y)
            w -= 1
            h -= 1
            dc.DrawLine(0, 0, 0, h)
            dc.DrawLine(w, 0, w, h)
            dc.DrawLine(0, 0, w, 0)
            dc.DrawLine(0, h, w, h)
            
        self.plugin.frame.SetDrawing(draw, display)
        
        
    def GetLabel(self, *args):
        return self.name
    
    
    def Configure(
        self, 
        foregroundColour=(255,255,255), 
        backgroundColour=(0,0,0),
        hCount=16, 
        vCount=9,
        display=0
    ):
        dialog = eg.ConfigurationDialog(self)
        sizer = wx.FlexGridSizer(5, 2, 5, 5)
        
        st = wx.StaticText(dialog, -1, "Foreground Colour:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)

        foregroundColourButton = eg.ColourSelectButton(
            dialog, -1, eg.text.General.choose, foregroundColour
        )
        sizer.Add(foregroundColourButton, 0, wx.EXPAND)
        
        st = wx.StaticText(dialog, -1, "Background Colour:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)

        backgroundColourButton = eg.ColourSelectButton(
            dialog, -1, eg.text.General.choose, backgroundColour
        )
        sizer.Add(backgroundColourButton, 0, wx.EXPAND)
        
        st = wx.StaticText(dialog, -1, "Num Horizontal Boxes:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)

        hCountCtrl = eg.SpinIntCtrl(dialog, min=0, max=100, value=hCount)
        sizer.Add(hCountCtrl, 0, wx.EXPAND)
        
        st = wx.StaticText(dialog, -1, "Num Vertical Boxes:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)

        vCountCtrl = eg.SpinIntCtrl(dialog, min=0, max=100, value=vCount)
        sizer.Add(vCountCtrl, 0, wx.EXPAND)
        
        st = wx.StaticText(dialog, -1, "Display:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
        
        displayChoice = eg.DisplayChoice(dialog, -1, display)
        sizer.Add(displayChoice, 0, wx.EXPAND)

        dialog.sizer.Add(sizer, 1, wx.EXPAND)

        if dialog.AffirmedShowModal():
            return (
                foregroundColourButton.GetColour(), 
                backgroundColourButton.GetColour(), 
                hCountCtrl.GetValue(),
                vCountCtrl.GetValue(),
                displayChoice.GetSelection(),
            )

        
        
class Lines(eg.ActionClass):
    
    def __call__(
        self, 
        foregroundColour=(255,255,255),
        backgroundColour=(0,0,0),
        lineSize=1, 
        orientation=0,
        display=0
    ):
        def draw(dc):
            dc.SetBackground(wx.Brush(backgroundColour))
            dc.Clear()
            dc.SetPen(wx.Pen(foregroundColour, lineSize))
            dc.SetBrush(wx.Brush(foregroundColour))
            w, h = dc.GetSizeTuple()
            if orientation == 0:
                for y in range(0, h, lineSize * 2):
                    dc.DrawLine(0, y, w, y)
            elif orientation == 1:
                for x in range(0, w, lineSize * 2):
                    dc.DrawLine(x, 0, x, h)
                
            
        self.plugin.frame.SetDrawing(draw, display)
        
        
    def GetLabel(self, *args):
        return self.name
    
    
    def Configure(
        self, 
        foregroundColour=(255,255,255), 
        backgroundColour=(0,0,0),
        lineSize=1, 
        orientation=0,
        display=0
    ):
        dialog = eg.ConfigurationDialog(self)
        orientationCtrl = wx.RadioBox(
            dialog, 
            label="Orientation",
            choices=[
                "Horizontal",
                "Vertical",
            ],
            style=wx.RA_SPECIFY_ROWS 
        )
        orientationCtrl.SetSelection(orientation)
        dialog.sizer.Add(orientationCtrl, 0, wx.EXPAND)
        dialog.sizer.Add((5, 5))
        
        sizer = wx.FlexGridSizer(5, 2, 5, 5)
        
        st = wx.StaticText(dialog, -1, "Foreground Colour:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)

        foregroundColourButton = eg.ColourSelectButton(
            dialog, -1, eg.text.General.choose, foregroundColour
        )
        sizer.Add(foregroundColourButton, 0, wx.EXPAND)
        
        st = wx.StaticText(dialog, -1, "Background Colour:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)

        backgroundColourButton = eg.ColourSelectButton(
            dialog, -1, eg.text.General.choose, backgroundColour
        )
        sizer.Add(backgroundColourButton, 0, wx.EXPAND)
        
        st = wx.StaticText(dialog, -1, "Line Size:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)

        lineSizeCtrl = eg.SpinIntCtrl(dialog, min=1, max=100, value=lineSize)
        sizer.Add(lineSizeCtrl, 0, wx.EXPAND)
                
        st = wx.StaticText(dialog, -1, "Display:")
        sizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
        
        displayChoice = eg.DisplayChoice(dialog, -1, display)
        sizer.Add(displayChoice, 0, wx.EXPAND)

        dialog.sizer.Add(sizer, 1, wx.EXPAND)

        if dialog.AffirmedShowModal():
            return (
                foregroundColourButton.GetColour(), 
                backgroundColourButton.GetColour(), 
                lineSizeCtrl.GetValue(),
                orientationCtrl.GetSelection(),
                displayChoice.GetSelection(),
            )

        
        
class Close(eg.ActionClass):
    
    def __call__(self):
        self.plugin.frame.Show(False)