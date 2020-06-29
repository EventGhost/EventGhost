# -*- coding: utf-8 -*-
#
# plugins/MceRemote_Vista/__init__.py
#
# This file is a plugin for EventGhost.
# Copyright © 2005-2020 EventGhost Project <http://www.eventghost.net/>
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
from .utils import v_sizer

TIME_FORMAT = '''\
{0}μs
{1}ms
{2}sec
'''


def remap(value, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    new_range = new_max - new_min
    return (((value - old_min) * new_range) / old_range) + new_min


class Oscilloscope(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.original_o_scope = Scope(self)
        original_o_scope_label = wx.StaticText(self, -1, 'Original Code')
        self.cleaned_o_scope = Scope(self)
        cleaned_o_scope_label = wx.StaticText(self, -1, 'Normalized Code')

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(v_sizer(original_o_scope_label, self.original_o_scope), 1, wx.EXPAND)
        sizer.Add(v_sizer(cleaned_o_scope_label, self.cleaned_o_scope), 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetMinSize((-1, 50))

    def SetValue(self, o_code, n_code):
        self.original_o_scope.SetValue(o_code)
        self.cleaned_o_scope.SetValue(n_code)


class Scope(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_SUNKEN)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOTION, self.OnMoveMouse)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.data = []
        self.rects = []
        self.gauge = wx.Rect(0, 0, 1, 1)
        self.slider_rect = wx.Rect(0, 0, 1, 1)
        self.position = 0
        self.mouse_x = 0
        self.slide = False
        self.total_time = 0

    def OnLeave(self, evt):
        if self.HasCapture():
            self.slide = False
            self.ReleaseMouse()
            self.Refresh()
            self.Update()

        evt.Skip()

    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.slide = False
            self.ReleaseMouse()
            self.Refresh()
            self.Update()
        evt.Skip()

    def OnLeftDown(self, evt):
        x, y = evt.GetPosition()
        if self.slider_rect.Contains(wx.Point(x, y)):
            self.slide = True
        else:
            self.slide = False

        self.mouse_x = x
        self.CaptureMouse()
        self.Refresh()
        self.Update()

        evt.Skip()

    def OnMoveMouse(self, evt):
        x, y = evt.GetPosition()

        if self.HasCapture():
            width = self.GetClientSize()[0]

            if self.slide:
                new_percent = float(x) / float(width)
                old_percent = float(self.mouse_x) / float(width)
                percent_change = old_percent - new_percent
                amount_change = int(round((self.total_time // 50) * percent_change))
                self.mouse_x = x

                if x < self.mouse_x:
                    self.position += amount_change
                else:
                    self.position -= amount_change
            else:
                change = x - self.mouse_x
                self.position += change
                self.mouse_x = x

            if self.position > (self.total_time // 50) - width:
                self.position = (self.total_time // 50) - width

            elif self.position < 0:
                self.position = 0

            self.Refresh()
            self.Update()

        temp_x = x + self.position
        for i, rect in enumerate(self.rects):
            if rect.Contains(wx.Point(temp_x, y)):
                timing = self.data[i]
                if timing < 0:
                    timing = -timing
                    text = 'Idle\n'
                else:
                    text = 'Pulse\n'

                text += TIME_FORMAT.format(timing, timing / 1000.0, (timing / 1000.0) / 1000.0)
                self.SetToolTipString(text)
                break
        else:
            if self.gauge.Contains(wx.Point(x, y)):
                x += self.position
                timing = remap(x, 3, self.total_time // 50, 0, self.total_time)
                text = TIME_FORMAT.format(timing, timing / 1000.0, (timing / 1000.0) / 1000.0)
                self.SetToolTipString(text)

            else:
                self.SetToolTipString('')

        evt.Skip()

    def SetValue(self, value):
        self.data = value
        self.data = []
        self.rects = []
        self.gauge = wx.Rect(0, 0, 1, 1)
        self.slider_rect = wx.Rect(0, 0, 1, 1)
        self.position = 0
        self.mouse_x = 0
        self.slide = False

        total_time = 0
        for item in self.data:
            if item < 0:
                item = -item

            total_time += item

        self.total_time = total_time

        self.Refresh()
        self.Update()

    def DoGetBestSize(self):
        height = self.GetSize()[1]
        if self.total_time:
            width = (self.total_time // 50) + 5
        else:
            width = -1
        return wx.Size(width, height)

    def GetBestSize(self):
        height = self.GetSize()[1]
        if self.total_time:
            width = (self.total_time // 50) + 5
        else:
            width = -1
        return wx.Size(width, height)

    def OnSize(self, evt):
        def _do():
            self.Refresh()
            self.Update()

        wx.CallAfter(_do)
        evt.Skip()

    def OnPaint(self, _):
        client_width, height = self.GetClientSize()
        if self.total_time:
            width = self.total_time // 50
            bmp = wx.EmptyBitmap(width + 5, height)
        else:
            width = client_width
            bmp = wx.EmptyBitmap(width, height)

        dc = wx.MemoryDC()
        dc.SelectObject(bmp)

        amount_visible = remap(client_width, 0, width + 5, 0, client_width)
        current_position = remap(self.position, 0, width + 5, 0, client_width)

        dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0, 255)))
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0, 255), 1))
        dc.DrawRectangle(0, 0, width + 5, height)
        #
        # dc.SetBrush(wx.Brush(wx.Colour(190, 190, 190, 255)))
        # dc.SetPen(wx.Pen(wx.Colour(190, 190, 190, 255), 1))
        # dc.DrawRectangle(3, height - 13, client_width - 6, 12)

        position_start = current_position + self.position
        position_end = position_start + amount_visible

        in_pen = wx.Pen(wx.Colour(219, 172, 79, 255), 1)
        out_pen = wx.Pen(wx.Colour(75, 110, 177, 255), 1)

        dc.SetBrush(wx.Brush(wx.Colour(75, 75, 75, 255)))
        dc.SetPen(wx.Pen(wx.Colour(75, 75, 75, 255), 1))
        dc.DrawRectangle(position_start, height - 20, amount_visible, 17)

        lines = []

        pulse_on = height - 18
        pulse_off = height - 3

        last_point = (5 + self.position, pulse_off)

        total_time = 0

        if self.position:
            current_pen = out_pen
        else:
            current_pen = in_pen

        pens = []

        for item in self.data:
            if item > 0:
                y = pulse_on
            else:
                y = pulse_off
                item = -item

            total_time += item // 50

            x = remap(total_time, 0, self.total_time // 50, 0, client_width) + 5 + self.position

            if x > position_start:
                if x > position_end:
                    diff = x - position_end
                    current_pen = out_pen
                else:
                    diff = x - position_start
                    current_pen = in_pen

                if last_point[0] < position_start:
                    pens += [out_pen, out_pen]
                    start_1 = last_point
                    end_1 = (last_point[0], y)
                    start_2 = end_1
                    end_2 = (position_start, y)
                    start_3 = end_2

                    lines += [start_1 + end_1, start_2 + end_2]

                    if x < position_end:
                        end_3 = (x, y)
                        pens += [in_pen]
                        lines += [start_3 + end_3]
                        current_pen = in_pen
                        last_point = end_3
                    else:
                        end_3 = (position_end, y)
                        start_4 = end_3
                        end_4 = (x, y)
                        pens += [in_pen, out_pen]
                        lines += [start_3 + end_3, start_4 + end_4]
                        current_pen = out_pen
                        last_point = end_4
                    continue

                if x > position_end > last_point[0] or last_point[0] < position_start:
                    if total_time > self.position + amount_visible:
                        pens += [in_pen, in_pen, out_pen]
                    else:
                        pens += [out_pen, out_pen, in_pen]

                    x1 = x - diff
                    x2 = x

                    start_1 = last_point
                    end_1 = (last_point[0], y)
                    start_2 = end_1
                    end_2 = (x1, y)
                    start_3 = end_2
                    end_3 = (x2, y)
                    lines += [start_1 + end_1, start_2 + end_2, start_3 + end_3]
                    last_point = end_3

                    continue

            pens += [current_pen, current_pen]
            start_1 = last_point
            end_1 = (last_point[0], y)
            start_2 = end_1
            end_2 = (x, y)

            lines += [start_1 + end_1, start_2 + end_2]
            last_point = end_2

        dc.DrawLineList(lines, pens)

        self.slider_rect = wx.Rect(current_position, height - 20, amount_visible, 17)
        self.gauge = wx.Rect(3, height - 20, client_width - 6, 17)

        lines = []

        pulse_on = 10
        pulse_off = height - 25

        last_point = (5, pulse_off)
        x = 5
        del self.rects[:]

        for item in self.data:
            if item > 0:
                y = pulse_on
            else:
                y = pulse_off
                item = -item

            x += item // 50

            start_1 = last_point
            end_1 = (last_point[0], y)
            start_2 = end_1
            end_2 = (x, y)

            self.rects += [wx.Rect(last_point[0], pulse_on, item // 50, pulse_off - 10)]
            lines += [start_1 + end_1, start_2 + end_2]
            last_point = end_2

        pens = [wx.Pen(wx.Colour(0, 255, 0, 255), 1)] * len(lines)
        dc.DrawLineList(lines, pens)

        dc.SelectObject(wx.NullBitmap)
        dc.Destroy()
        del dc

        pdc = wx.PaintDC(self)

        pdc.DrawBitmap(bmp, -self.position, 0)

