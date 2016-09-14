# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
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

import eg

eg.RegisterPlugin(
    name = "Test Pattern",
    author = "Bitmonster",
    version = "0.1",
    description = "Plugin to show some test patterns.",
    guid = "{17BC05D0-C600-4244-ABB1-02C1DA6229A0}",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAV0lEQVR42mNkoBAwgogD"
        "Bw78B9H29g5Qwf/I0gz/GVH5SPKMowaMGkA9A4BK/qNogCpgZECXhvCBFoJpBwcHmAEH"
        "YEYC1drDmED1jQwI0MCABQweA8gHAM1iaBEreN/nAAAAAElFTkSuQmCC"
    ),
)

import wx
import threading
import colorsys
from math import sqrt, sin, cos
import math
from threading import Timer
import cStringIO
from base64 import b64decode
from eg.WinApi.Utils import GetMonitorDimensions, BringHwndToFront

class Text:
    foregroundColour = "Foreground colour"
    backgroundColour = "Background colour"
    display = "Display:"
    aspectRatio = "Aspect ratio:"
    aspectRatios = [
        "1:1 Pixelmapping",
        "4:3 Frame",
        "16:9 Frame",
        "4:3 ITU-R BT.601 PAL",
        "16:9 ITU-R BT.601 PAL",
    ]
    coverage = "Coverage (percent):"
    orientation = "Orientation:"
    orientations = ["Horizontal", "Vertical"]
    numVerticalElements = "Number of vertical elements:"
    numHorizontalElements = "Number of horizontal elements:"
    numElements = "Number of elements:"
    useAntiAlias = "Use Anti-Aliasing"
    firstColour = "First colour"
    secondColour = "Second colour"
    lastColour = "Last colour"
    dotDiameter = "Dot Diameter:"
    makeDoubleBars = "Make Double Bars"
    showNumbers = "Show Numbers"
    numberFont = "Number Font:"
    lineSize = "Line Size:"
    radius1 = "Radius:"
    radius2 = "% (0=fill entire screen)"
    testText = "Test text:"
    offset = "Offset every second line"


#FOCUS_PATTERN = b64decode(
#    "iVBORw0KGgoAAAANSUhEUgAAACgAAAAoAQMAAAC2MCouAAAABlBMVEUAAAD///+l2Z/d"
#    "AAAAAnRSTlMA/1uRIrUAAABkSURBVHjaY2AAg/p/DPb/oWQCE4MCM0N+1ff11QyZXlNW"
#    "ekPJ/F//1/9mSHQSUXSGslFkweoheuv/AwEDA5DNwMAPFK9g4ASq8YCS/EC9PxgYgeY4"
#    "QNkosmD1EL0Qc6jgHoTvAMSAW32HrwidAAAAAElFTkSuQmCC"
#)
FOCUS_PATTERN = b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAACgAAAAoAQMAAAC2MCouAAAABlBMVEUAAAD///+l2Z/d"
    "AAAAZElEQVR4nGNgAIP6fwz2/6FkAhODAjNDftX39dUMmV5TVnpDyfxf/9f/Zkh0ElF0"
    "hrJRZMHqIXrr/wMBAwOQzcDADxSvYOAEqvGAkvxAvT8YGIHmOEDZKLJg9RC9EHOo4B6E"
    "7wDEgFt9VLehNwAAAABJRU5ErkJggg=="
)

FOCUS_IMAGE = wx.ImageFromStream(cStringIO.StringIO(FOCUS_PATTERN))

ASPECT_RATIOS = [
    # aspectRatio, isCCIR601
    (None, False),
    (4.0 / 3.0, False),
    (16.0 / 9.0, False),
    ((720.0 / 702.0) * (4.0 / 3.0), True),
    ((720.0 / 702.0) * (16.0 / 9.0), True),
]


def AddColon(txt):
    return "%s%s" % (txt, ":")

class DrawingFrame(wx.Frame):

    def __init__(self, parent=None):
        wx.Frame.__init__(
            self,
            parent,
            style=wx.NO_BORDER|wx.FRAME_NO_TASKBAR|wx.CLIP_CHILDREN
        )
        self.drawing = None
        self.displayNum = 0
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DCLICK, self.LeftDblClick)
        self.Bind(wx.EVT_KEY_DOWN, self.OnChar)
        self.Bind(wx.EVT_MOTION, self.ShowCursor)
        self.timer = None
        self.SetBackgroundColour((0, 0, 0))


    def OnChar(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            wx.Frame.Show(self, False)
        event.Skip()


    def OnPaint(self, event=None):
        wx.BufferedPaintDC(self, self._buffer)


    def SetDrawing(self, drawFunc, args):
        self.drawing = drawFunc
        d = GetMonitorDimensions()[self.displayNum]
        self.SetDimensions(d.x, d.y, d.width, d.height)
        self._buffer = wx.EmptyBitmap(d.width, d.height)
        dc = wx.BufferedDC(wx.ClientDC(self), self._buffer)
        self.drawing(dc, *args)
        #self.Refresh(eraseBackground=False)
        wx.Frame.Show(self, True)
        BringHwndToFront(self.GetHandle(), False)
        self.SetCursor(wx.StockCursor(wx.CURSOR_BLANK))


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



class TestPatterns(eg.PluginBase):
    text = Text

    def __init__(self):
        self.frame = DrawingFrame(None)
        self.AddAction(SetDisplay)
        self.AddAction(Focus)
        self.AddAction(IreWindow)
        self.AddAction(Checkerboard)
        self.AddAction(Grid)
        self.AddAction(Dots)
        self.AddAction(Lines)
        self.AddAction(Bars)
        self.AddAction(SiemensStar)
        self.AddAction(Burst)
        self.AddAction(Geometry)
        self.AddAction(PixelCropping)
        self.AddAction(ZonePlate)
        self.AddAction(Readability)
        self.AddAction(Close)


    def __close__(self):
        wx.CallAfter(self.frame.Destroy)
        self.frame = None



class TestPatternAction(eg.ActionBase):

    def __call__(self, *args):
        self.plugin.frame.SetDrawing(self.Draw, args)


    def Draw(self, *args):
        raise NotImplemented


    def GetLabel(self, *dummyArgs):
        return self.name



class SetDisplay(eg.ActionBase):
    name = "Set Display"

    def __call__(self, display=0):
        self.plugin.frame.displayNum = display


    def GetLabel(self, display=0):
        return self.name + ": %d" % (display + 1)


    def Configure(self, display=0):
        panel = eg.ConfigPanel()
        displayChoice = panel.DisplayChoice(display)
        panel.AddLine(self.plugin.text.display, displayChoice)

        while panel.Affirmed():
            panel.SetResult(displayChoice.GetValue())



class Focus(TestPatternAction):

    def Draw(
        self,
        dc,
        foregroundColour,
        backgroundColour,
        display=0, # deprecated
    ):
        image = FOCUS_IMAGE.Copy()
        image.ConvertToMono(255, 255, 255)
        bmp = wx.BitmapFromImage(image, 1)
        bmpWidth, bmpHeight = bmp.GetSize()
        #bmp.SetMask(None)

        mdc = wx.MemoryDC()
        bmp2 = wx.EmptyBitmap(bmpWidth, bmpHeight, 1)
        mdc.SelectObject(bmp2)
        mdc.SetTextForeground((255, 255, 255))
        mdc.SetTextBackground((0, 0, 0))
        mdc.DrawBitmap(bmp, 0, 0, False)
        mdc.SelectObject(wx.NullBitmap)
        bmp = bmp2

        dc.SetTextForeground(backgroundColour)
        dc.SetTextBackground(foregroundColour)
        w, h = dc.GetSizeTuple()
        startX = (bmpWidth - (w % bmpWidth)) / 2
        startY = (bmpHeight - (h % bmpHeight)) / 2
        for x in range(-startX, w, bmpWidth):
            for y in range(-startY, h, bmpHeight):
                dc.DrawBitmap(bmp, x, y, False)


    def Configure(
        self,
        foregroundColour=(255, 255, 255),
        backgroundColour=(0, 0, 0),
        display=0, #deprecated
    ):
        text = self.plugin.text
        panel = eg.ConfigPanel()
        foregroundColourCtrl = panel.ColourSelectButton(
            foregroundColour,
            title = text.foregroundColour
        )
        backgroundColourCtrl = panel.ColourSelectButton(
            backgroundColour,
            title = text.backgroundColour
        )
        panel.AddLine(AddColon(text.foregroundColour), foregroundColourCtrl)
        panel.AddLine(AddColon(text.backgroundColour), backgroundColourCtrl)

        while panel.Affirmed():
            panel.SetResult(
                foregroundColourCtrl.GetValue(),
                backgroundColourCtrl.GetValue(),
            )



class IreWindow(TestPatternAction):
    name = "IRE Window"

    def Draw(
        self,
        dc,
        foregroundColour,
        backgroundColour,
        coverage,
        aspectRatio=0,
        display=0, # deprecated
    ):
        dc.SetBackground(wx.Brush(backgroundColour))
        dc.Clear()
        dc.SetPen(wx.Pen(foregroundColour, 1))
        dc.SetBrush(wx.Brush(foregroundColour))
        dc.SetPen(wx.Pen(foregroundColour, 1))
        dc.SetBrush(wx.Brush(foregroundColour))
        w, h = dc.GetSizeTuple()
        area = (w * h) * coverage / 100
        width = height = sqrt(area)
        dc.DrawRectangle((w - width) / 2, (h - height) / 2, width, height)


    def Configure(
        self,
        foregroundColour=(255, 255, 255),
        backgroundColour=(0, 0, 0),
        coverage=25.0,
        aspectRatio=0,
        display=0, # deprecated
    ):
        text = self.plugin.text
        panel = eg.ConfigPanel()

        foregroundColourCtrl = panel.ColourSelectButton(
            foregroundColour,
            title = text.foregroundColour
        )
        backgroundColourCtrl = panel.ColourSelectButton(
            backgroundColour,
            title = text.backgroundColour
        )
        coverageCtrl = panel.SpinNumCtrl(coverage, min=0, max=100)
        aspectChoice = panel.Choice(aspectRatio, text.aspectRatios)

        panel.AddLine(AddColon(text.foregroundColour), foregroundColourCtrl)
        panel.AddLine(AddColon(text.backgroundColour), backgroundColourCtrl)
        panel.AddLine(text.coverage, coverageCtrl)
        panel.AddLine(text.aspectRatio, aspectChoice)

        while panel.Affirmed():
            panel.SetResult(
                foregroundColourCtrl.GetValue(),
                backgroundColourCtrl.GetValue(),
                coverageCtrl.GetValue(),
                aspectChoice.GetValue(),
            )



class Checkerboard(TestPatternAction):

    def Draw(
        self,
        dc,
        foregroundColour=(255, 255, 255),
        backgroundColour=(0, 0, 0),
        hCount=4,
        vCount=4,
        display=0, #deprecated
    ):
        dc.SetBackground(wx.Brush(backgroundColour))
        dc.Clear()
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


    def Configure(
        self,
        foregroundColour=(255, 255, 255),
        backgroundColour=(0, 0, 0),
        hCount=4,
        vCount=4,
        display=0, #deprecated
    ):
        text = self.plugin.text
        panel = eg.ConfigPanel()
        foregroundColourCtrl = panel.ColourSelectButton(
            foregroundColour,
            title = text.foregroundColour
        )
        backgroundColourCtrl = panel.ColourSelectButton(
            backgroundColour,
            title = text.backgroundColour
        )
        hCountCtrl = panel.SpinIntCtrl(hCount, min=0, max=100)
        vCountCtrl = panel.SpinIntCtrl(vCount, min=0, max=100)

        panel.AddLine(AddColon(text.foregroundColour), foregroundColourCtrl)
        panel.AddLine(AddColon(text.backgroundColour), backgroundColourCtrl)
        panel.AddLine(text.numHorizontalElements, hCountCtrl)
        panel.AddLine(text.numVerticalElements, vCountCtrl)

        while panel.Affirmed():
            panel.SetResult(
                foregroundColourCtrl.GetValue(),
                backgroundColourCtrl.GetValue(),
                hCountCtrl.GetValue(),
                vCountCtrl.GetValue(),
            )



class Grid(TestPatternAction):

    def Draw(
        self,
        dc,
        foregroundColour=(255, 255, 255),
        backgroundColour=(0, 0, 0),
        hCount=4,
        vCount=4,
        display=0, # deprecated
    ):
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


    def Configure(
        self,
        foregroundColour=(255, 255, 255),
        backgroundColour=(0, 0, 0),
        hCount=16,
        vCount=9,
        display=0, # deprecated
    ):
        text = self.plugin.text
        panel = eg.ConfigPanel()

        foregroundColourCtrl = panel.ColourSelectButton(
            foregroundColour,
            title = text.foregroundColour
        )
        backgroundColourCtrl = panel.ColourSelectButton(
            backgroundColour,
            title = text.backgroundColour
        )
        hCountCtrl = panel.SpinIntCtrl(hCount, min=0, max=100)
        vCountCtrl = panel.SpinIntCtrl(vCount, min=0, max=100)

        panel.AddLine(AddColon(text.foregroundColour), foregroundColourCtrl)
        panel.AddLine(AddColon(text.backgroundColour), backgroundColourCtrl)
        panel.AddLine(text.numHorizontalElements, hCountCtrl)
        panel.AddLine(text.numVerticalElements, vCountCtrl)

        while panel.Affirmed():
            panel.SetResult(
                foregroundColourCtrl.GetValue(),
                backgroundColourCtrl.GetValue(),
                hCountCtrl.GetValue(),
                vCountCtrl.GetValue(),
            )



class Dots(TestPatternAction):

    def Draw(
        self,
        dc,
        foregroundColour=(255, 255, 255),
        backgroundColour=(0, 0, 0),
        hCount=4,
        vCount=4,
        diameter=1,
        antialiasing=False
    ):
        diameter *= 1.0
        dc.SetBackground(wx.Brush(backgroundColour))
        dc.Clear()
        if antialiasing and diameter > 1:
            gc = wx.GraphicsContext.Create(dc)
            gc.Translate(0, 0)
            gc.Scale(1.0, 1.0)
            d = diameter + 1
        else:
            gc = dc
            d = diameter + 2
        gc.SetPen(wx.Pen(backgroundColour, 0))
        gc.SetBrush(wx.Brush(foregroundColour))
        w, h = dc.GetSizeTuple()
        if hCount == 1:
            xOffset = (w - diameter) / 2.0  - 1
            width = 0
        else:
            xOffset = -1
            width = (w - diameter) / (hCount - 1)
        if vCount == 1:
            yOffset = (h - diameter) / 2.0 - 1
            height = 0
        else:
            yOffset = -1
            height = (h - diameter) / (vCount - 1)

        for y in range(vCount):
            for x in range(hCount):
                gc.DrawEllipse(x * width + xOffset, y * height + yOffset, d, d)


    def Configure(
        self,
        foregroundColour=(255,255,255),
        backgroundColour=(0,0,0),
        hCount=16,
        vCount=9,
        diameter=1,
        antialiasing=False
    ):
        text = self.plugin.text
        panel = eg.ConfigPanel()

        foregroundColourCtrl = panel.ColourSelectButton(
            foregroundColour,
            title = text.foregroundColour
        )
        backgroundColourCtrl = panel.ColourSelectButton(
            backgroundColour,
            title = text.backgroundColour
        )
        hCountCtrl = panel.SpinIntCtrl(hCount, min=1, max=100)
        vCountCtrl = panel.SpinIntCtrl(vCount, min=1, max=100)
        diameterCtrl = panel.SpinIntCtrl(diameter, min=1)
        anialiasingCtrl = panel.CheckBox(antialiasing, text.useAntiAlias)

        panel.AddLine(AddColon(text.foregroundColour), foregroundColourCtrl)
        panel.AddLine(AddColon(text.backgroundColour), backgroundColourCtrl)
        panel.AddLine(text.numHorizontalElements, hCountCtrl)
        panel.AddLine(text.numVerticalElements, vCountCtrl)
        panel.AddLine(text.dotDiameter, diameterCtrl)
        panel.AddLine(anialiasingCtrl)

        while panel.Affirmed():
            panel.SetResult(
                foregroundColourCtrl.GetValue(),
                backgroundColourCtrl.GetValue(),
                hCountCtrl.GetValue(),
                vCountCtrl.GetValue(),
                diameterCtrl.GetValue(),
                anialiasingCtrl.GetValue(),
            )


class ZonePlate(TestPatternAction):

    def Draw(self, dc, scale=128):
        dc.Clear()
        width, height = dc.GetSizeTuple()
        sineTab = [
            int(127.5 * sin(math.pi * (i - 127.5) / 127.5) + 127.5)
            for i in range(256)
        ]
        cx = width / 2
        cy = height / 2
        bmp = wx.EmptyBitmap(width, height, 24)
        pixelData = wx.NativePixelData(bmp)
        pixels = pixelData.GetPixels()
        y = -cy
        for i in range(height):
            x = -cx
            for j in range(width):
                d = ((x * x + y * y) * scale) >> 8
                val = sineTab[d & 0xFF]
                pixels.Set(val, val, val)
                pixels.nextPixel()
                x += 1
            y += 1
            pixels.MoveTo(pixelData, 0, y + cy)
        dc.DrawBitmap(bmp, 0, 0, False)


    def Configure(self, scale=128):
        panel = eg.ConfigPanel()
        scaleCtrl = panel.SpinIntCtrl(scale, min=0)
        panel.AddLine("Scale:", scaleCtrl)

        while panel.Affirmed():
            panel.SetResult(scaleCtrl.GetValue())



class Lines(TestPatternAction):

    def Draw(
        self,
        dc,
        foregroundColour=(255,255,255),
        backgroundColour=(0,0,0),
        lineSize=1,
        orientation=0,
        display=0, # deprecated
    ):
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


    def Configure(
        self,
        foregroundColour=(255,255,255),
        backgroundColour=(0,0,0),
        lineSize=1,
        orientation=0,
        display=0, # deprecated
    ):
        text = self.plugin.text
        panel = eg.ConfigPanel()
        orientationCtrl = panel.Choice(orientation, text.orientations)
        foregroundColourCtrl = panel.ColourSelectButton(
            foregroundColour,
            title = text.foregroundColour
        )
        backgroundColourCtrl = panel.ColourSelectButton(
            backgroundColour,
            title = text.backgroundColour
        )
        lineSizeCtrl = panel.SpinIntCtrl(lineSize, min=1, max=100)

        panel.AddLine(text.orientation, orientationCtrl)
        panel.AddLine(AddColon(text.foregroundColour), foregroundColourCtrl)
        panel.AddLine(AddColon(text.backgroundColour), backgroundColourCtrl)
        panel.AddLine(text.lineSize, lineSizeCtrl)

        while panel.Affirmed():
            panel.SetResult(
                foregroundColourCtrl.GetValue(),
                backgroundColourCtrl.GetValue(),
                lineSizeCtrl.GetValue(),
                orientationCtrl.GetSelection(),
            )



class Bars(TestPatternAction):

    def Draw(
        self,
        dc,
        firstColour=(0,0,0),
        lastColour=(255,255,255),
        barCount=16,
        orientation=0,
        makeDoubleBars=False,
        showNumbers=True,
        fontStr=u'0;-19;0;0;0;400;0;0;0;0;3;2;1;34;Arial',
    ):
        dc.SetBackground(wx.Brush(firstColour))
        dc.Clear()
        w, h = dc.GetSizeTuple()
        if orientation == 0:
            barSize = int(w * 1.0 / barCount)
        else:
            barSize = int(h * 1.0 / barCount)
        r1, g1, b1 = firstColour
        r2, g2, b2 = lastColour
        dc.SetFont(wx.FontFromNativeInfoString(fontStr))
        if makeDoubleBars:
            w1 = w / 2
            h1 = h / 2
        else:
            w1 = w
            h1 = h
        for n1 in range(barCount):
            n2 = (barCount - n1 - 1)
            r = r1 + (1.0 * (r2 - r1) / (barCount - 1)) * n1
            g = g1 + (1.0 * (g2 - g1) / (barCount - 1)) * n1
            b = b1 + (1.0 * (b2 - b1) / (barCount - 1)) * n1
            dc.SetPen(wx.Pen((r, g, b), 1))
            dc.SetBrush(wx.Brush((r, g, b)))
            numberStr = str(n1 + 1)
            tw, th = dc.GetTextExtent(numberStr)
            if orientation == 0:
                dc.DrawRectangle(n1 * barSize, 0, barSize, h1)
                if makeDoubleBars:
                    dc.DrawRectangle(n2 * barSize, h1, barSize, h)
                    ty1 = h / 2 * 0.95 - th
                    ty2 = h / 2 * 1.05
                else:
                    ty1 = (h * 0.66 - th)
                tx1 = n1 * barSize + ((barSize - tw) / 2)
                tx2 = n2 * barSize + ((barSize - tw) / 2)
            else:
                dc.DrawRectangle(0, n1 * barSize, w1, barSize)
                if makeDoubleBars:
                    dc.DrawRectangle(w1, n2 * barSize, w1, barSize)
                    tx1 = w / 2 * 0.95 - tw
                    tx2 = w / 2 * 1.05
                else:
                    tx1 = w * 0.66 - tw
                ty1 = n1 * barSize + ((barSize - th) / 2)
                ty2 = n2 * barSize + ((barSize - th) / 2)
            if showNumbers:
                v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[2]
                if v < 0.5:
                    dc.SetTextBackground((0, 0, 0))
                    dc.SetTextForeground((255, 255, 255))
                else:
                    dc.SetTextBackground((255, 255, 255))
                    dc.SetTextForeground((0, 0, 0))
                dc.DrawText(numberStr, tx1, ty1)
                if makeDoubleBars:
                    dc.DrawText(numberStr, tx2, ty2)


    def Configure(
        self,
        firstColour=(0,0,0),
        lastColour=(255,255,255),
        barCount=16,
        orientation=0,
        makeDoubleBars=False,
        showNumbers=True,
        fontStr=u'0;-19;0;0;0;400;0;0;0;0;3;2;1;34;Arial',
    ):
        text = self.plugin.text
        panel = eg.ConfigPanel()
        orientationCtrl = panel.Choice(orientation, text.orientations)
        firstColourButton = panel.ColourSelectButton(
            firstColour,
            title = text.firstColour
        )
        lastColourButton = panel.ColourSelectButton(
            lastColour,
            title = text.lastColour
        )
        barCountCtrl = panel.SpinIntCtrl(barCount, min=1, max=100)
        makeDoubleBarsCtrl = panel.CheckBox(
            makeDoubleBars,
            text.makeDoubleBars
        )
        showNumbersCtrl = panel.CheckBox(showNumbers, text.showNumbers)
        fontCtrl = panel.FontSelectButton(fontStr)
        panel.AddLine(text.orientation, orientationCtrl)
        panel.AddLine(AddColon(text.firstColour), firstColourButton)
        panel.AddLine(AddColon(text.lastColour), lastColourButton)
        panel.AddLine(text.numElements, barCountCtrl)
        panel.AddLine(makeDoubleBarsCtrl)
        panel.AddLine(showNumbersCtrl)
        panel.AddLine(text.numberFont, fontCtrl)

        while panel.Affirmed():
            panel.SetResult(
                firstColourButton.GetValue(),
                lastColourButton.GetValue(),
                barCountCtrl.GetValue(),
                orientationCtrl.GetValue(),
                makeDoubleBarsCtrl.GetValue(),
                showNumbersCtrl.GetValue(),
                fontCtrl.GetValue()
            )



class SiemensStar(TestPatternAction):
    name = "Siemens Star"

    def Draw(
        self,
        dc,
        backgroundColour=(0, 0, 0),
        firstColour=(0, 0, 0),
        secondColour=(255, 255, 255),
        numBeams=16,
        radius=100.0,
        display=0, # deprecated
    ):
        dc.SetBackground(wx.Brush(backgroundColour))
        dc.Clear()
        w, h = dc.GetSizeTuple()
        gc = wx.GraphicsContext.Create(dc)
        gc.Translate(w / 2.0, h / 2.0)
        gc.Scale(1.0, 1.0)
        if radius == 0.0:
            r = max(w, h) * 2.0
        else:
            r = min(w, h) * (radius / 200.0)
        beamSize = (1.0 / numBeams) * math.pi * 2.0
        path = gc.CreatePath()
        for n in range(numBeams):
            phi1 = (n-0.25) * beamSize
            phi2 = (n+0.25) * beamSize
            path.MoveToPoint(0, 0)
            path.AddArc(0, 0, r, phi1, phi2)
            path.AddLineToPoint(0, 0)
            path.CloseSubpath()
        path2 = gc.CreatePath()
        path2.AddArc(0, 0, r, 0, math.pi * 2.0)
        gc.SetPen(wx.Pen("white", 1, style=wx.TRANSPARENT))
        gc.SetBrush(wx.Brush(firstColour))
        gc.FillPath(path2)
        gc.SetBrush(wx.Brush(secondColour))
        gc.FillPath(path)


    def Configure(
        self,
        backgroundColour=(0, 0, 0),
        firstColour=(0, 0, 0),
        secondColour=(255, 255, 255),
        numBeams=16,
        radius=100.0,
        display=0, # deprecated
    ):
        text = self.plugin.text
        panel = eg.ConfigPanel()
        backgroundColourCtrl = panel.ColourSelectButton(
            backgroundColour,
            title = text.backgroundColour
        )
        firstColourButton = panel.ColourSelectButton(
            firstColour,
            title = text.firstColour
        )
        secondColourButton = panel.ColourSelectButton(
            secondColour,
            title = text.secondColour
        )
        beamCountCtrl = panel.SpinIntCtrl(numBeams, min=2)
        radiusCtrl = panel.SpinNumCtrl(radius, max=100.0)

        panel.AddLine(AddColon(text.backgroundColour), backgroundColourCtrl)
        panel.AddLine(AddColon(text.firstColour), firstColourButton)
        panel.AddLine(AddColon(text.secondColour), secondColourButton)
        panel.AddLine(text.numElements, beamCountCtrl)
        panel.AddLine(text.radius1, radiusCtrl, text.radius2)

        while panel.Affirmed():
            panel.SetResult(
                backgroundColourCtrl.GetValue(),
                firstColourButton.GetValue(),
                secondColourButton.GetValue(),
                beamCountCtrl.GetValue(),
                radiusCtrl.GetValue(),
            )


class Burst(TestPatternAction):

    def Draw(
        self,
        dc,
        firstColour,
        secondColour,
        numBeams,
    ):
        dc.SetBackground(wx.Brush("black"))
        dc.Clear()
        w, h = dc.GetSizeTuple()
        numBars = numBeams
        r1, g1, b1 = firstColour
        r2, g2, b2 = secondColour
        k = numBars * math.pi / w
        rgbTuples = zip(firstColour, secondColour)
        for x in range(w):
            factor = 0.5 + cos(x * k) / 2
            rgb = [c1 * factor + c2 * (1.0 - factor) for c1, c2 in rgbTuples]
            dc.SetPen(wx.Pen(rgb, 1))
            dc.DrawLine(x, 0, x, h)


    def Configure(
        self,
        firstColour=(0, 0, 0),
        secondColour=(255, 255, 255),
        numBeams=16,
    ):
        text = self.plugin.text
        panel = eg.ConfigPanel()
        firstColourButton = panel.ColourSelectButton(
            firstColour,
            title = text.firstColour
        )
        secondColourButton = panel.ColourSelectButton(
            secondColour,
            title = text.secondColour
        )
        beamCountCtrl = panel.SpinIntCtrl(numBeams, min=1)

        panel.AddLine(AddColon(text.firstColour), firstColourButton)
        panel.AddLine(AddColon(text.secondColour), secondColourButton)
        panel.AddLine(text.numElements, beamCountCtrl)

        while panel.Affirmed():
            panel.SetResult(
                firstColourButton.GetValue(),
                secondColourButton.GetValue(),
                beamCountCtrl.GetValue(),
            )



class Geometry(TestPatternAction):

    def Draw(
        self,
        dc,
        aspectRatioIndex=0
    ):
        dc.SetBackground(wx.Brush("black"))
        dc.Clear()
        w, h = dc.GetSizeTuple()
        gc = wx.GraphicsContext.Create(dc)
        gc.PushState()
        gc.SetPen(wx.Pen("white", 3.0))
        gc.SetBrush(wx.TRANSPARENT_BRUSH)

        aspectRatio, isCCIR601 = ASPECT_RATIOS[aspectRatioIndex]
        if aspectRatio is None:
            gc.Scale(h / 1000.0, h / 1000.0)
            gc.Translate(1000.0 * (w * 1.0 / h) / 2, 500)
        elif w > h:
            gc.Scale(w / (aspectRatio * 1000.0), h / 1000.0)
            gc.Translate(500 * aspectRatio, 500)
        gc.DrawEllipse(-450, -450, 900, 900)
        gc.PopState()
        dc.SetPen(wx.Pen("white", 2))
        if isCCIR601:
            offset = int(round(w * 8.0 / 720.0))
            dc.SetBrush(wx.GREY_BRUSH)
            dc.DrawRectangle(1, 1, offset-1, h-1)
            dc.DrawRectangle(w-offset, 1, offset, h-1)

        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(1, 1, w-1, h-1)
        dc.DrawLine(0, h/2, w, h/2)
        dc.DrawLine(w/2, 0, w/2, h)


    def GetLabel(self, aspektRatio):
        return self.name + ": " + self.plugin.text.aspectRatios[aspektRatio]


    def Configure(
        self,
        aspectRatio=0,
    ):
        text = self.plugin.text
        panel = eg.ConfigPanel()
        aspectCtrl = panel.Choice(aspectRatio, text.aspectRatios)
        panel.AddLine(text.aspectRatio, aspectCtrl)

        while panel.Affirmed():
            panel.SetResult(aspectCtrl.GetValue())



class PixelCropping(TestPatternAction):
    name = "Pixel Cropping"

    def Draw(self, dc):
        numLines = 40
        textColour = (255, 255, 255)

        w, h = dc.GetSizeTuple()

        xMax = w - 1
        yMax = h - 1

        space = w / 200 # separation between connecting lines and text
        minConnectionLineLength = w / 100
        cornerLength = w / 50

        lineLength = space + numLines + minConnectionLineLength
        textOffset = lineLength + space

        dc.SetBackground(wx.Brush("black"))
        dc.Clear()
        dc.SetTextForeground(textColour)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        font = wx.Font(
            w / 65.0,
            wx.FONTFAMILY_SWISS,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD
        )
        dc.SetFont(font)

        textWidth, textHeight = dc.GetTextExtent(str(numLines))

        hBoxWidth = numLines + 2 * space + textWidth
        vBoxWidth = numLines + 2 * space + textHeight

        hBarLength = int((w - hBoxWidth * 3.0) / numLines)
        vBarLength = int((h - vBoxWidth * 2.0) / numLines)

        hOffset = (w - (hBarLength * numLines)) / 2
        vOffset = (h - (vBarLength * numLines)) / 2

        numPositions = [0] + range(4, numLines, 5)
        dc.SetPen(wx.Pen((128, 128, 128), 1))
        dc.DrawRectangle(0, 0, w, h)
        dc.SetPen(wx.Pen("white", 1))

        dc.DrawLine(0, 0, cornerLength, 0)
        dc.DrawLine(0, 0, 0, cornerLength)

        dc.DrawLine(0, yMax, cornerLength, yMax)
        dc.DrawLine(0, yMax, 0, yMax - cornerLength)

        dc.DrawLine(xMax, 0, xMax - cornerLength, 0)
        dc.DrawLine(xMax, 0, xMax, cornerLength)

        dc.DrawLine(xMax, yMax, xMax - cornerLength, yMax)
        dc.DrawLine(xMax, yMax, xMax, yMax - cornerLength)

        for n in range(numLines):
            x1 = hOffset + n * hBarLength
            x2 = x1 + hBarLength
            y1 = n
            y2 = yMax - n
            dc.DrawLine(x1, y1, x2, y1)
            dc.DrawLine(x1, y2, x2, y2)

            x1 = n
            x2 = xMax - n
            y1 = vOffset + n * vBarLength
            y2 = y1 + vBarLength
            dc.DrawLine(x1, y1, x1, y2)
            dc.DrawLine(x2, y1, x2, y2)

        for n in numPositions:
            numStr = str(n+1)
            (
                textWidth,
                textHeight,
                descent,
                externalLeading
            ) = dc.GetFullTextExtent(numStr)
            vCenterTextOffset = (textHeight - descent) / 2

            x1 = hOffset + (n * hBarLength) + (hBarLength / 2)
            y1 = n + space
            dc.DrawLine(x1, y1, x1, lineLength)
            dc.DrawLine(x1, yMax - y1 , x1, yMax - lineLength)

            x2 = x1 - (textWidth / 2)
            dc.DrawText(numStr, x2, textOffset - descent)
            dc.DrawText(numStr, x2, yMax - (textOffset + textHeight - descent))

            x1 = n + space
            y1 = vOffset + (n * vBarLength) + (vBarLength / 2)
            dc.DrawLine(x1, y1, lineLength, y1)
            dc.DrawLine(xMax - x1, y1, xMax - lineLength, y1)

            y2 = y1 - vCenterTextOffset
            dc.DrawText(numStr, textOffset, y2)
            dc.DrawText(numStr, xMax - (textOffset + textWidth), y2)

        # draw centered description
        font = wx.Font(
            w / 40.0,
            wx.FONTFAMILY_SWISS,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD
        )
        dc.SetFont(font)#, textColour)
        text = (self.name + "\n%d x %d") % (w, h)
        y = 0
        data = []
        for line in text.splitlines():
            textWidth, textHeight = dc.GetTextExtent(line)
            x = (w - textWidth) / 2
            data.append((line, x, y))
            y += textHeight
        offset = (h - y) / 2
        for line, x, y in data:
            dc.DrawText(line, x, offset + y)



class Readability(TestPatternAction):

    def Draw(
        self,
        dc,
        testText,
        textColour,
        backgroundColour,
        fontStr,
        offsetLines,
    ):
        dc.SetBackground(wx.Brush(backgroundColour))
        dc.Clear()
        dc.SetTextForeground(textColour)
        dc.SetFont(wx.FontFromNativeInfoString(fontStr))
        tw, th, descent, externalLeading = dc.GetFullTextExtent(testText)
        if offsetLines:
            offset = -(tw / 2)
        else:
            offset = 0
        w, h = dc.GetSizeTuple()
        lineNum = 0
        y = 0
        while y < h:
            if (lineNum % 2):
                x = offset
            else:
                x = 0
            while x < w:
                dc.DrawText(testText, x, y)
                x += tw
            y += th
            lineNum += 1


    def Configure(
        self,
        testText="The quick brown fox jumps over the lazy dog. ",
        textColour=(255, 255, 255),
        backgroundColour=(0, 0, 0),
        fontStr='0;-11;0;0;0;400;0;0;0;0;3;2;1;34;Arial',
        offsetLines=True,
    ):
        text = self.plugin.text
        panel = eg.ConfigPanel()
        textCtrl = panel.TextCtrl(testText, size=(250, -1))
        textColourCtrl = panel.ColourSelectButton(
            textColour,
            title = text.foregroundColour
        )
        backgroundColourCtrl = panel.ColourSelectButton(
            backgroundColour,
            title = text.backgroundColour
        )
        fontCtrl = panel.FontSelectButton(fontStr)
        offsetCtrl = panel.CheckBox(offsetLines, text.offset)
        panel.AddLine(text.testText, textCtrl)
        panel.AddLine(AddColon(text.foregroundColour), textColourCtrl)
        panel.AddLine(AddColon(text.backgroundColour), backgroundColourCtrl)
        panel.AddLine("Text font:", fontCtrl)
        panel.AddLine(offsetCtrl)

        while panel.Affirmed():
            panel.SetResult(
                textCtrl.GetValue(),
                textColourCtrl.GetValue(),
                backgroundColourCtrl.GetValue(),
                fontCtrl.GetValue(),
                offsetCtrl.GetValue()
            )



class Close(eg.ActionBase):

    def __call__(self):
        self.plugin.frame.Show(False)

