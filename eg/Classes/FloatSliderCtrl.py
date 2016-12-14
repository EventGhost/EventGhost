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
# CHANGELOG
# added:   keyword increment
# changed: modified the docstring to have more detail for the styles and also
#          added an entry for the increment keyword
# fixed:   the value label was not tracking the thumb properly some new math
#          fixed the issue
# added:   event binding and unbinding - uses the wx.ScrollEvent to create a
#          an event for the different scroll event types and properly attaches
#          the FloatSlider instance as an event object
# fixed:   some adjustment on the min/max/value labels to have them properly
#          line up
# added:   foreground and background colour changing
# fixed:   gray background behind the widget is not set to the system window
#          default
# fixed:   if there was no style used and the size was set the widget wouldn't
#          display
# changed: Swapped out the use of wx.Panel for use of wx.PyPanel since this is
#          a custom control
# added:   added almost all docstrings and also added comments on the voodoo
#          code
# changed: changed __init__ default for parameter id to wx.ID_ANY
# removed: **kwargs parameter from __init__, as there are no additional
#          keyword arguments that should be passed
# removed: validator parameter from __init__, because of how this custom
#          control functions the use of a validator would return incorrect data
# added:   private method for conversion of max, min, value to be passed to the
#          wxSlider instance
# added:   additional docstrings
# changed: how the formatting of the labels is done. the widget will now
#          automatically figure out how many decimal positions need to be
#          displayed based on the last digit that is a non 0 and will display
#          the proper number of positions needed instead of truncating
# added:   private method _GenerateFormat to handle the creation of the string
#          formatter for the labels

import wx


class FloatSliderCtrl(wx.PyPanel):

    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        value=None,
        minValue=0.0,
        maxValue=100.0,
        increment=None,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.SL_HORIZONTAL,
        name=wx.SliderNameStr
    ):
        """
        This widget is a modified version of the wx.Slider Widget. It accepts
        all the same parameters as the wx Slider Widget. Except one added
        parameter you can set an increment value so if you want to have the
        slider skip by a specified amount it will, this widget also has fully
        functioning labels and ticks. with 2 modifications. it shows the float
        value and float min and max, but i also added a little "flare" to it
        and the value moves with the thumb control. there is 2 added functions
        as well one called GetIncrement and the other is SetIncrement i think
        the name is pretty self explanatory. enjoy the float slider

        :param parent: a wxWindow object
        :param id: wxID - if not set will automatically generate a new wxId.

        Default - wx.ID_ANY
        :param value: float(), str(), int() - The starting value of the slider.
        If not set will be set to the minValue parameter.

        Default - None
        :param minValue: float(), str(), int() - The lowest value the slider
        can be set to.

        Default - 0.0
        :param maxValue: float(), str(), int() - The highest value the slider
        can be set to.

        Default - 100.0
        :param increment: float(), str(), int() - The "step" size to take when
        the slider value is changed. If not set one will be generated using
        float(100 / (maxValue - minValue)).

        Default - None
        :param pos: Tuple for where you want the widget to be placed.

        Default - wx.DefaultPosition
        :param size: Tuple for the displayed size of the widget.

        Default - wx.DefaultSize
        :param style:
        wx.SL_HORIZONTAL: Displays the slider horizontally.
        wx.SL_VERTICAL: Displays the slider vertically.
        wx.SL_AUTOTICKS: Displays tick marks. Windows only.
        wx.SL_MIN_MAX_LABELS: Displays minimum, maximum labels.
        wx.SL_VALUE_LABEL: Displays value label.
        wx.SL_LABELS: Displays minimum, maximum and value labels.
        wx.SL_LEFT: Displays ticks on the left and forces the slider to be vertical.
        wx.SL_RIGHT: Displays ticks on the right and forces the slider to be vertical.
        wx.SL_TOP: Displays ticks on the top and forces slider to be horizontal.
        wx.SL_BOTTOM: Displays ticks on the bottom and forces the slider to be horizontal.
        wx.SL_SELRANGE: Allows the user to select a range on the slider. Windows only.
        wx.SL_INVERSE: Inverses the minimum and maximum endpoints on the slider.
         Not compatible with wx.SL_SELRANGE.

        Notice:
        SL_LEFT , SL_TOP , SL_RIGHT and SL_BOTTOM specify the position of the
        slider ticks in MSW implementation and that the min/max labels,
        if any, are positioned on the opposite side. So, to have a label on
        the left side of a vertical slider, wx.SL_RIGHT must be used.

        Warning: If using SL_AUTOTICKS as an example if you have an increment
        set at 0.001 and a min of 0.0 and a max of 10000.00 this will cause the
        widget to hang due to the sheer number of tick marks it tries to draw.

        Default - wx.SL_HORIZONTAL
        :param name: user identifier for the widget.

        Default - wx.SliderNameStr
        """

        self.selStart = None
        self.selEnd = None

        # checking the styles and making changes as necessary to pass to the
        # wxSlider widget
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

        # checking for styles that set the labels and remove them if there
        # because we do not want the wxSlider to generate the labels as we are
        # going to do that our selves
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

        self.top = top
        self.left = left
        self.horizontal = horizontal
        self.mLabel = mLabel
        self.vLabel = vLabel
        self.inverse = inverse

        # here we check if the value was set. and if not we set it to minValue
        # if that was not set to make the value 0.0
        if value is None:
            value = minValue

        self.value = float(value)
        self.minValue = float(minValue)
        self.maxValue = float(maxValue)

        # check to see if the increment was set and if not to set a generic one
        if increment is None:
            self.increment = float(100 / (self.maxValue - self.minValue))
        else:
            self.increment = float(increment)

        if size == wx.DefaultSize and horizontal:
            size = (-1, 80)
        elif size == wx.DefaultSize:
            size = (110, -1)
        elif size[0] == -1 and not horizontal:
            size = (110, size[1])
        elif size[1] == -1 and horizontal:
            size = (size[0], 80)

        if horizontal:
            sliderSize = (size[0], 32)
        else:
            sliderSize = (32, size[1])

        if horizontal and sliderSize[1] < 32 <= size[1]:
            sliderSize = (sliderSize[0], 32)

        wx.PyPanel.__init__(self, parent, -1, size=size, pos=pos)

        # converting the minValue/maxValue/value so we can pass the modified
        # values to the constructor of the wxSlider
        sliderVal, sliderMin, sliderMax = self._ConvertValues(
            self.value,
            self.minValue,
            self.maxValue
        )

        self.Slider = wx.Slider(
            self,
            id,
            value=sliderVal,
            minValue=sliderMin,
            maxValue=sliderMax,
            size=sliderSize,
            style=style,
            name=name
        )

        # create a sizer to place the wxSlider into this will control any of
        # the sizing automatically. we add a stretch spacer before and after
        # to ensure we have space to place our labels

        if horizontal:
            panelSizer = wx.BoxSizer(wx.VERTICAL)
        else:
            panelSizer = wx.BoxSizer(wx.HORIZONTAL)

        panelSizer.AddStretchSpacer()
        panelSizer.Add(self.Slider, 0, wx.EXPAND | wx.ALIGN_CENTER)
        panelSizer.AddStretchSpacer()


        # setting the colors of wxPyPanel to the system default doing a redraw
        # the slider will grab the colors and set them for the slider. this is
        # done so if the user wants to set the colors it will propagate to the
        # wxSlider

        self.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        )

        self.SetForegroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
        )

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self._OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Slider.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        # binding to the various events the wxSlider can generate so when
        # generated we can create a new event with this class set as the
        # event object
        self.Slider.Bind(wx.EVT_SCROLL_TOP, self._OnTop)
        self.Slider.Bind(wx.EVT_SCROLL_BOTTOM, self._OnBottom)
        self.Slider.Bind(wx.EVT_SCROLL_LINEUP, self._OnLineUp)
        self.Slider.Bind(wx.EVT_SCROLL_LINEDOWN, self._OnLineDown)
        self.Slider.Bind(wx.EVT_SCROLL_PAGEUP, self._OnPageUp)
        self.Slider.Bind(wx.EVT_SCROLL_PAGEDOWN, self._OnPageDown)
        self.Slider.Bind(wx.EVT_SCROLL_THUMBTRACK, self._OnThumbTrack)
        self.Slider.Bind(wx.EVT_SCROLL_THUMBRELEASE, self._OnThumbRelease)
        self.Slider.Bind(wx.EVT_SCROLL_CHANGED, self._OnChanged)

        self.floatFormat = self._GenerateFormat()
        self.SetSizer(panelSizer)
        self.Refresh()

# --------------------Event Handling and Private Methods------------------

    def DoGetBestSize(self, *args, **kwargs):
        return self.GetSizeTuple()

    def _GenerateFormat(self):
        """
        Internal use, creates the str formatter for the labels.
        :return: str() formatter. Example: "%.2f"
        """
        incT = '%f' % self.increment
        maxT = '%f' % self.maxValue
        minT = '%f' % self.minValue
        incDec = len(incT.rstrip('0').split('.')[1])
        maxDec = len(maxT.rstrip('0').split('.')[1])
        minDec = len(minT.rstrip('0').split('.')[1])
        decPos = max([incDec, maxDec, minDec])
        return '%.' + str(decPos) + 'f'

    def _ConvertValues(self, *args):
        """
        Internal use, converts any value parameters the wxSlider instance uses
        to a rounded int that is the value divided by the increment.
        :param args: float()(s)
        :return: tuple(round(v / self.increment) for v in args)
        """
        return tuple(round(v / self.increment) for v in args)

    def _CreateEvent(self, event):
        """
        Internal use, creates a new wxScrollEvent that has this wxPyPanel
        instance as the event object.
        :param event: wx event metric.
        :return: None
        """
        self._UpdateValues()
        event = wx.ScrollEvent(event, self.GetId())
        event.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(event)
        self.Slider.Refresh()
        self.Refresh()

    def _OnTop(self, evt):
        """
        Internal use, generation of the events for the egFloatSliderCtrl.
        :param evt: wxEvent instance.
        :return: None
        """
        self._CreateEvent(wx.wxEVT_SCROLL_TOP)

    def _OnBottom(self, evt):
        """
        Internal use, generation of the events for the egFloatSliderCtrl.
        :param evt: wxEvent instance.
        :return: None
        """
        self._CreateEvent(wx.wxEVT_SCROLL_BOTTOM)

    def _OnLineUp(self, evt):
        """
        Internal use, generation of the events for the egFloatSliderCtrl.
        :param evt: wxEvent instance.
        :return: None
        """
        self._CreateEvent(wx.wxEVT_SCROLL_LINEUP)

    def _OnLineDown(self, evt):
        """
        Internal use, generation of the events for the egFloatSliderCtrl.
        :param evt: wxEvent instance.
        :return: None
        """
        self._CreateEvent(wx.wxEVT_SCROLL_LINEDOWN)

    def _OnPageUp(self, evt):
        """
        Internal use, generation of the events for the egFloatSliderCtrl.
        :param evt: wxEvent instance.
        :return: None
        """
        self._CreateEvent(wx.wxEVT_SCROLL_PAGEUP)

    def _OnPageDown(self, evt):
        """
        Internal use, generation of the events for the egFloatSliderCtrl.
        :param evt: wxEvent instance.
        :return: None
        """
        self._CreateEvent(wx.wxEVT_SCROLL_PAGEDOWN)

    def _OnThumbTrack(self, evt):
        """
        Internal use, generation of the events for the egFloatSliderCtrl.
        :param evt: wxEvent instance.
        :return: None
        """
        self._CreateEvent(wx.wxEVT_SCROLL_THUMBTRACK)

    def _OnThumbRelease(self, evt):
        """
        Internal use, generation of the events for the egFloatSliderCtrl.
        :param evt: wxEvent instance.
        :return: None
        """
        self._CreateEvent(wx.wxEVT_SCROLL_THUMBRELEASE)

    def _OnChanged(self, evt):
        """
        Internal use, generation of the events for the egFloatSliderCtrl.
        :param evt: wxEvent instance.
        :return: None
        """
        self._CreateEvent(wx.wxEVT_SCROLL_CHANGED)

    def _OnSize(self, evt):
        """
        Internal use, refreshes the widget.
        :param evt: wxEvent instance.
        :return: None
        """
        self.Refresh()
        evt.Skip()

    def __getattr__(self, item):
        """
        Checks to see if the wxSlider instance has the attribute and if not
        raise AttributeError.
        """

        if item in self.__dict__:
            return self.__dict__[item]
        if hasattr(self.Slider, item):
            return getattr(self.Slider, item)

        raise AttributeError(
            '%r does not have attribute %r' % (repr(self), item)
        )

    def _UpdateValues(self):
        """
        Internal use, converting the wxSlider values to the values to be
        returned.
        :return None
        """
        sliderVal = self.Slider.GetValue()
        sliderMin = self.Slider.GetMin()
        sliderMax = self.Slider.GetMax()
        if sliderVal == sliderMin:
            self.value = self.minValue
        elif sliderVal == sliderMax:
            self.value = self.maxValue
        else:
            self.value = float(float(sliderVal) * self.increment)

# ----------------Drawing the Widget-------------------
    def OnEraseBackground(self, evt):
        """
        Internal use, stops the widget from flickering when redrawn, this is an
        empty method.
        :param evt: wxEvent instance.
        :return: None
        """
        pass

    def OnPaint(self, evt):
        """
        Internal use, handles the drawing of the widget.
        :param evt: wxEvent instance.
        :return: None
        """

        value = self.value
        # reversing the max/min if wx.SL_INVERSE was set
        if self.inverse:
            maxValue = self.minValue
            minValue = self.maxValue
            sliderRange = minValue - maxValue
        else:
            minValue = self.minValue
            maxValue = self.maxValue
            sliderRange = maxValue - minValue

        # grabbing the colours and setting the wxSlider as the same and the
        # colours will also be used in the drawing of the labels
        forecolour = self.GetForegroundColour()
        backcolour = self.GetBackgroundColour()
        self.Slider.SetForegroundColour(forecolour)
        self.Slider.SetBackgroundColour(backcolour)

        panelW, panelH = self.GetSizeTuple()
        sliderW, sliderH = self.Slider.GetSize()
        sliderX, sliderY = self.Slider.GetPosition()

        bmp = wx.EmptyBitmap(panelW, panelH)
        font = self.GetFont()
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetFont(font)

        # drawing the background for the labels
        dc.SetBrush(wx.Brush(wx.Colour(*backcolour)))
        dc.SetPen(wx.Pen(wx.Colour(*backcolour), 0))
        dc.DrawRectangle(0, 0, panelW, panelH)
        dc.SetTextForeground(wx.Colour(*forecolour))
        dc.SetTextBackground(wx.Colour(*backcolour))

        if self.mLabel:
            print 'mLabel'
            # converting the max/min to strings
            maxText = self.floatFormat % maxValue
            minText = self.floatFormat % minValue

            # getting the size in pixels of the max/min values
            minW, minH = dc.GetTextExtent(minText)
            maxW, maxH = dc.GetTextExtent(maxText)

            if self.horizontal:
                if self.top:
                    y = sliderY + sliderH
                else:
                    y = sliderY - minH
                minX = sliderX
                maxX = panelW - maxW
                minY = y
                maxY = y
            else:
                if self.left:
                    x = sliderX + sliderW + 3
                else:
                    x = sliderX - minW
                minY = sliderY
                maxY = sliderY + sliderH - maxH
                minX = x
                maxX = x
            dc.DrawText(minText, minX, minY)
            dc.DrawText(maxText, maxX, maxY)

        if self.vLabel:
            print 'vLabel'
            valText = self.floatFormat % value
            valW, valH = dc.GetTextExtent(valText)

            if self.horizontal:
                slider = float(sliderW)
                val = valW
            else:
                slider = float(sliderH)
                val = valH
            sldRatio = float(slider) / sliderRange
            loc = sldRatio * value

            if value == minValue:
                pos = 0
            elif value == maxValue:
                pos = slider - val
            else:
                pos = loc - (val * (loc / slider))

            if self.top:
                pos = (pos, sliderY - valH)
            elif self.left:
                pos = (sliderX - valW - 3, pos)
            elif self.horizontal:
                pos = (pos, sliderY + sliderH)
            else:
                pos = (sliderX + sliderW, pos)
            dc.DrawText(valText, *pos)

        dc.Destroy()
        del dc

        pdc = wx.PaintDC(self)
        pdc.DrawBitmap(bmp, 0, 0)

        evt.Skip()


# -----------------Public Methods---------------------
    def IsMinMaxLabel(self):
        """
        Retruns whether or not the min/max labels are displayed.
        :return: bool()
        """
        return self.mLabel

    def IsValueLabel(self):
        """
        Retruns whether or not the value label is displayed.
        :return: bool()
        """
        return self.vLabel

    def IsInverse(self):
        """
        Retruns whether or not the wx.SL_INVERSE was set.
        :return: bool()
        """
        return self.inverse

    def GetValue(self):
        """
        Retruns a float of the current slider value.
        :return: float()
        """
        self._UpdateValues()
        return self.value

    def GetMin(self):
        """
        Retruns a float of the current min value.
        :return: float()
        """
        return self.minValue

    def GetMax(self):
        """
        Retruns a float of the current max value.
        :return: float()
        """
        return self.maxValue

    def GetIncrement(self):
        """
        Retruns a float of the current increment value.
        :return: float()
        """
        return self.increment

    def GetSelStart(self):
        """
        Retruns a float of the current selection start value, or None if one
        has not been set.
        :return: float(), None
        """
        return self.selStart

    def GetSelEnd(self):
        """
        Retruns a float of the current selection end value, or None if one
        has not been set.
        :return: float(), None
        """
        return self.selEnd

    def SetSelection(self, min, max):
        """
        Sets the selection start and end points
        :param min: float() int() or a str() of a float of the start point.
        :param max: float() int() or a str() of a float of the end point.
        :return: None
        """
        self.selStart = float(min)
        self.selEnd = float(max)
        self.Slider.SetSelection(
            *self._ConvertValues(self.selStart, self.selEnd)
        )

    def SetMinMaxLabel(self, flag=True):
        """
        This allows for dynamic displaying of the min/max labels.
        :param flag: True/False, default is True.
        :return: None
        """
        self.mLabel = flag

    def SetValueLabel(self, flag=True):
        """
        This allows for dynamic displaying of the value label.
        :param flag: True/False, default is True.
        :return: None
        """
        self.vLabel = flag

    def SetValue(self, value):
        """
        Sets the value for the slider. Will convert to a float if a
        str of a float or an int is passed.
        :param value: float() int() or a str() of a float.
        :return: None
        """
        self.value = float(value)
        self.Slider.SetValue(*self._ConvertValues(self.value))
        self.Refresh()

    def SetMin(self, minValue):
        """
        Sets the min value for the slider. Will convert to a float if a
        str of a float or an int is passed.
        :param minValue: float() int() or a str() of a float.
        :return: None
        """
        self.minValue = float(minValue)
        self.floatFormat = self._GenerateFormat()
        self.Slider.SetMin(*self._ConvertValues(self.minValue))
        self.Refresh()

    def SetMax(self, maxValue):
        """
        Sets the max value for the slider. Will convert to a float if a
        str of a float or an int is passed.
        :param maxValue: float() int() or a str() of a float.
        :return: None
        """
        self.maxValue = float(maxValue)
        self.floatFormat = self._GenerateFormat()
        self.Slider.SetMax(*self._ConvertValues(self.maxValue))
        self.Refresh()

    def SetIncrement(self, increment):
        """
        Sets the increment for the slider. Will convert to a float if a
        str of a float or an int is passed.
        :param increment: float() int() or a str() of a float.
        :return: None
        """
        self.increment = float(increment)

        value, minValue, maxValue = self._ConvertValues(
            self.value,
            self.minValue,
            self.maxValue
        )
        self.floatFormat = self._GenerateFormat()
        self.Slider.SetRange(minValue, maxValue)
        self.Slider.SetValue(value)
        self.Refresh()

    def SetRange(self, minValue, maxValue):
        """
        Sets the min and max values for the slider. Will convert to a float if
        a str of a float or an int is passed.
        :param minValue: float() int() or a str() of a float.
        :param maxValue: float() int() or a str() of a float.
        :return: None
        """
        self.minValue = float(minValue)
        self.maxValue = float(maxValue)
        self.floatFormat = self._GenerateFormat()
        self.Slider.SetRange(
            *self._ConvertValues(self.minValue, self.maxValue)
        )
        self.Refresh()
