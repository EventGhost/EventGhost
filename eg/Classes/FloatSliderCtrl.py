# -*- coding: utf-8 -*-
#
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
# $LastChangedDate: 2016-07-13 00:51:00 -0600 $
# $LastChangedRevision: 501 $
# $LastChangedBy: K $


# this widget is a modified version of the wx.Slider Widget.
# It accepts all the same parameters as the wx Slider Widget. except one added
# parameter you can set an increment value so if you want to have the slider
# skip by a specified amount it will, this widget also has fully functioning
# labels and ticks. with 2 modifications. it shows the float value and float
# min and max, but i also added a little "flare" to it and the value moves with
# the thumb control. there is 2 added functions as well one called GetIncrement
# and the other is SetIncrement i think the name is pretty self explanatory.
# enjoy the float slider

import wx


class FloatSliderCtrl(wx.Panel):

    def __init__(
        self,
        parent,
        id=-1,
        value=-1,
        minValue=-1,
        maxValue=100.0,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.SL_HORIZONTAL,
        validator=wx.DefaultValidator,
        name=wx.SliderNameStr,
        **kwargs
    ):
        if style | wx.SL_HORIZONTAL == style:
            horizontal = True
        elif style | wx.SL_VERTICAL == style:
            horizontal = False
        else:
            horizontal = True

        if style | wx.SL_TOP == style:
            horizontal = True
            top = True
        elif style | wx.SL_BOTTOM == style:
            horizontal = True
            top = False
        else:
            top = False

        if style | wx.SL_RIGHT == style:
            horizontal = False
            left = False
        elif style | wx.SL_LEFT == style:
            horizontal = False
            left = True
        else:
            left = False

        if style | wx.SL_SELRANGE == style:
            style = style ^ wx.SL_SELRANGE

        if style | wx.SL_LABELS == style:
            style = style ^ wx.SL_LABELS
            mLabel = True
            vLabel = True
        else:
            mLabel = False
            vLabel = False

        if style | wx.SL_MIN_MAX_LABELS == style:
            style = style ^ wx.SL_MIN_MAX_LABELS
            mLabel = True

        if style | wx.SL_VALUE_LABEL == style:
            style = style ^ wx.SL_VALUE_LABEL
            vLabel = True

        if style | wx.SL_INVERSE == style:
            inverse = True
        else:
            inverse = False

        if value == -1:
            if minValue != -1:
                value = minValue
            else:
                value = 0.0

        if minValue == -1:
            minValue = 0.0

        if 'increment' in kwargs:
            increment = kwargs.pop('increment')
        else:
            increment = 100 / (maxValue - minValue)

        if vLabel or mLabel:
            if size == wx.DefaultSize:
                if horizontal:
                    size = (-1, 80)
                else:
                    size = (110, -1)
            elif size[0] == -1:
                if not horizontal:
                    size = (110, size[1])
            elif size[1] == -1:
                if horizontal:
                    size = (size[0], 80)

        if horizontal:
            slidersize = (size[0], size[1] * 0.20)
        else:
            slidersize = (size[0] * 0.43, size[1])

        if slidersize[1] < 30 <= size[1]:
            slidersize = (slidersize[0], 30)

        wx.Panel.__init__(self, parent, -1, size=size, pos=pos)

        sliderval, slidermin, slidermax = [
            round(v / increment) for v in (value, minValue, maxValue)
        ]

        self.Slider = wx.Slider(
            self,
            id,
            value=sliderval,
            minValue=slidermin,
            maxValue=slidermax,
            size=slidersize,
            style=style,
            name=name
        )

        self.minValue = minValue
        self.maxValue = maxValue
        self.value = value
        self.top = top
        self.left = left
        self.horizontal = horizontal
        self.mLabel = mLabel
        self.vLabel = vLabel
        self.inverse = inverse
        self.selStart = None
        self.selEnd = None
        self.increment = increment

        self.Slider.Bind(wx.EVT_SCROLL, self.OnSlider)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        if horizontal:
            panelSizer = wx.BoxSizer(wx.VERTICAL)

        else:
            panelSizer = wx.BoxSizer(wx.HORIZONTAL)

        panelSizer.AddStretchSpacer()
        panelSizer.Add(self.Slider, 0, wx.EXPAND | wx.ALIGN_CENTER)
        panelSizer.AddStretchSpacer()

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.SetSizer(panelSizer)
        self.Refresh()

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if hasattr(self.Slider, item):
            return getattr(self.Slider, item)

        raise AttributeError('FloatSliderCtrl does not have attribute ' + item)

    def OnEraseBackground(self, dummyEvent):
        pass

    def OnSize(self, evt):
        self.Refresh()
        evt.Skip()

    def OnPaint(self, evt):
        value = float(self.value)
        minValue = float(self.minValue)
        maxValue = float(self.maxValue)
        forecolour = self.Slider.GetForegroundColour()
        backcolour = self.Slider.GetBackgroundColour()
        bmp = wx.EmptyBitmap(*self.GetSizeTuple())
        font = self.Slider.GetFont()
        panelW, panelH = self.GetSize()
        sliderW, sliderH = self.Slider.GetSize()
        sliderX, sliderY = self.Slider.GetPosition()

        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetFont(font)
        # dc = wx.GCDC(dc)

        dc.SetBrush(wx.Brush(wx.Colour(*backcolour)))
        dc.SetPen(wx.Pen(wx.Colour(*backcolour), 0))
        dc.DrawRectangle(0, 0, panelW, panelH)
        dc.SetTextForeground(wx.Colour(*forecolour))
        dc.SetTextBackground(wx.Colour(*backcolour))

        if self.mLabel:
            maxText = '%3.2f' % maxValue
            minText = '%3.2f' % minValue

            if self.inverse:
                minText, maxText = maxText, minText

            minW, minH = dc.GetTextExtent(maxText)
            maxW, maxH = dc.GetTextExtent(minText)
            if self.horizontal:
                minX = sliderX
                maxX = sliderX + sliderW - maxW
                if self.top:
                    y = sliderY + sliderH
                    minY = y
                    maxY = y
                else:
                    y = sliderY - minH
                    minY = y
                    maxY = y
                maxX -= 4
            else:
                minY = sliderY
                maxY = sliderY + sliderH - maxH
                if self.left:
                    x = sliderX + sliderW
                    minX = x
                    maxX = x
                    maxY -= 5
                    minY += 1
                else:
                    x = sliderX - minW
                    minX = x
                    maxX = x
                    maxY -= 1
                    minY += 1
            dc.DrawText(minText, minX, minY)
            dc.DrawText(maxText, maxX, maxY)

        if self.vLabel:
            valText = '%3.2f' % value
            valW, valH = dc.GetTextExtent(valText)
            locRatio = value / (maxValue - minValue)

            if self.horizontal:
                loc = sliderW * locRatio
                if locRatio == 0:
                    valX = 1
                elif locRatio == 1:
                    valX = sliderW - valW - 3
                else:
                    valX = loc - (valW % locRatio) - (valW * locRatio)

                if self.top:
                    valY = sliderY - valH
                else:
                    valY = (panelH / 2) + (sliderH * 0.65)

            else:
                loc = sliderH * locRatio
                if locRatio == 0:
                    valY = 1
                elif locRatio == 1:
                    valY = sliderH - valH - 3
                else:
                    valY = loc - (valH * locRatio)

                if self.left:
                    valX = sliderX - valW - 3
                else:
                    valX = sliderX + sliderW

            dc.DrawText(valText, valX, valY)

        dc.Destroy()
        del dc

        pdc = wx.PaintDC(self)
        pdc.DrawBitmap(bmp, 0, 0)

        evt.Skip()

    def UpdatePanel(self):
        if self.inverse:
            minValue, maxValue = self.maxValue, self.minValue
        else:
            minValue, maxValue = self.minValue, self.maxValue

        self.minTextCtrl.SetLabel('%3.2f' % minValue)
        self.maxTextCtrl.SetLabel('%3.2f' % maxValue)

    def OnSlider(self, evt=None):
        sliderval = self.Slider.GetValue()
        slidermin = self.Slider.GetMin()
        slidermax = self.Slider.GetMax()
        if sliderval == slidermin:
            self.value = self.minValue
        elif sliderval == slidermax:
            self.value = self.maxValue
        else:
            self.value = sliderval * self.increment
        self.Refresh()
        if evt is not None:
            evt.Skip()

    def SetMinMaxLabel(self, flag=True):
        self.mLabel = flag

    def SetValueLabel(self, flag=True):
        self.vLabel = flag

    def IsMinMaxLabel(self):
        return self.mLabel

    def IsValueLabel(self):
        return self.vLabel

    def IsInverse(self):
        return self.inverse

    def GetValue(self):
        self.OnSlider()
        return self.value

    def GetMin(self):
        return self.minValue

    def GetMax(self):
        return self.maxValue

    def GetIncrement(self):
        return self.increment

    def GetSelStart(self):
        return self.selStart

    def GetSelEnd(self):
        return self.selEnd

    def SetSelection(self, min, max):
        self.selStart = min
        self.selEnd = max
        self.Slider.SetSelection(
            round(min / self.increment),
            round(max / self.increment)
        )

    def SetValue(self, value):
        self.Slider.SetValue(round(value / self.increment))
        self.value = value
        self.Refresh()

    def SetMin(self, minValue):
        self.Slider.SetMin(round(minValue / self.increment))
        self.minValue = minValue
        self.UpdatePanel()

    def SetMax(self, maxValue):
        self.Slider.SetMax(round(maxValue / self.increment))
        self.maxValue = maxValue
        self.UpdatePanel()

    def SetIncrement(self, increment):
        self.Slider.SetRange(
            round(self.minValue / increment),
            round(self.maxValue / increment)
        )
        self.Slider.SetValue(round(self.value / increment))
        self.increment = increment
        self.UpdatePanel()

    def SetRange(self, minValue, maxValue):
        self.Slider.SetRange(
            round(minValue / self.increment),
            round(maxValue / self.increment)
        )
        self.minValue = minValue
        self.maxValue = maxValue
        self.UpdatePanel()
