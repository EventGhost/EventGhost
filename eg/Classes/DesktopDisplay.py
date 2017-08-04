# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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


import win32api
import wx


NID_INTEGRATED_TOUCH = 0x01
NID_EXTERNAL_TOUCH = 0x02


class BlackoutFrame(wx.Frame):

    def __init__(self, handler):
        self.handler = handler
        wx.Frame.__init__(
            self,
            None,
            -1,
            style=wx.BORDER_NONE | wx.STAY_ON_TOP,
            pos=(handler.x, handler.y),
            size=(handler.w, handler.h)
        )

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Show()

    def OnPaint(self, evt=None):
        try:
            size = (self.handler.w, self.handler.h)
            pos = (self.handler.x, self.handler.y)
        except DisplayException:
            self.handler.blackout = False
            return

        if self.GetSizeTuple() != size:
            self.SetSize(size)

        if self.GetPositionTuple() != pos:
            self.SetPosition(pos)

        bmp = wx.EmptyBitmap(*size)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetBackground(wx.Brush(wx.Colour(0, 0, 0)))
        dc.Destroy()
        del dc

        if evt is not None:
            dc = wx.PaintDC(self)
            dc.DrawBitmap(bmp, 0, 0)


class Display(object):

    def __init__(self, idx):
        self._idx = idx
        self._frame = None

    @property
    def _handle(self):
        displays = win32api.EnumDisplayMonitors()

        if len(displays) - 1 >= self._idx:
            return displays[self._idx][0]

        if self._frame is not None:
            self._frame.Destroy()
            self._frame = None

        raise DesktopDisplay.DisplayNumberError(self._idx)

    @property
    def blackout(self):
        return self._frame is not None

    @blackout.setter
    def blackout(self, flag):
        if flag and self._frame is None:
            self._frame = BlackoutFrame(self)
        elif not flag and self._frame:
            self._frame.Destroy()
            self._frame = None

    def _metrics(self, idx1, idx2=None):
        metrics = win32api.GetMonitorInfo(self._handle)
        if idx2 is None:
            return metrics['Monitor'][idx1]
        else:
            return metrics['Monitor'][idx1] + -metrics['Monitor'][idx2]


    @property
    def x(self):
        return self._metrics(0)

    @property
    def y(self):
        return self._metrics(1)

    @property
    def w(self):
        return self._metrics(2, 0)

    @property
    def h(self):
        return self._metrics(3, 1)

    @property
    def primary(self):
        metrics = win32api.GetMonitorInfo(self._handle)
        return bool(metrics['Flags'])

    @property
    def number(self):
        metrics = win32api.GetMonitorInfo(self._handle)
        display = win32api.EnumDisplayDevices(metrics['Device'])
        return int(display.DeviceName[4:].split('\\')[0][7:])

    @property
    def name(self):
        metrics = win32api.GetMonitorInfo(self._handle)
        display = win32api.EnumDisplayDevices(metrics['Device'])
        return display.DeviceString

    @property
    def size(self):
        metrics = win32api.GetMonitorInfo(self._handle)
        w = metrics['Monitor'][2] + -metrics['Monitor'][0]
        h = metrics['Monitor'][3] + -metrics['Monitor'][1]
        return w, h

    @property
    def pos(self):
        metrics = win32api.GetMonitorInfo(self._handle)
        x = metrics['Monitor'][0]
        y = metrics['Monitor'][1]
        return x, y

    def __str__(self):
        return (
            'Name: {0}, '
            'Number: {1}, '
            'Width: {2}, '
            'Height: {3}, '
            'X: {4}, '
            'Y: {5}, '
            'Primary: {6}'.format(
                self.name,
                self.number,
                self.w,
                self.h,
                self.x,
                self.y,
                self.primary
            )
        )


class DisplayException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)


class DesktopDisplay(object):

    DisplayException = DisplayException
    Display = Display

    class DisplayNameError(DisplayException):
        pass


    class DisplayNumberError(DisplayException):
        pass


    def __init__(self):
        self._displays = []
        self.Refresh()

    def Refresh(self):
        displays = []

        for i, display_handles in enumerate(win32api.EnumDisplayMonitors()):
            metrics = win32api.GetMonitorInfo(display_handles[0])
            display = win32api.EnumDisplayDevices(metrics['Device'])
            try:
                if self._displays[i]['key'] != display.DeviceKey:
                    if self._displays[i]['display'].blackout:
                        self._displays[i]['display'].blackout = False

                self._displays[i]['key'] = display.DeviceKey
                displays += [self._displays[i]]

            except IndexError:
                displays += [dict(key=display.DeviceKey, display=Display(i))]
        for display_data in self._displays[:]:
            if display_data not in displays:
                display = display_data['display']
                if display.blackout:
                    display.blackout = False

                self._displays.remove(display_data)
        self._displays = displays[:]

    def EnumDisplays(self):
        self.Refresh()
        return list(display['display'] for display in self._displays)

    def GetDisplay(self, display):
        if isinstance(display, int):
            number = display
            name = None
        else:
            name = display
            number = None

        displays = self.EnumDisplays()
        if name is not None:
            for display in displays:
                if display.name == name:
                    return display
            raise DesktopDisplay.DisplayNameError(name)
        if number is not None:
            if len(displays) - 1 >= number > -1:
                return displays[number]
            raise DesktopDisplay.DisplayNumberError(number)

    @property
    def size(self):
        return win32api.GetSystemMetrics(78), win32api.GetSystemMetrics(79)

    @property
    def displayCount(self):
        return win32api.GetSystemMetrics(80)

    @property
    def isTouchScreen(self):
        try:
            if win32api.GetSystemMetrics(86):
                if eg.WindowsVersion >= 7:
                    touch = win32api.GetSystemMetrics(94)
                    if touch in (NID_INTEGRATED_TOUCH, NID_EXTERNAL_TOUCH):
                        return True
                    return False
                return True
        except:
            pass
        return False

    @property
    def isMultiTouch(self):
        return self.maxTouchCount > 1

    @property
    def maxTouchCount(self):
        if self.isTouchScreen:
            return win32api.GetSystemMetrics(95)
        else:
            return 0

    @property
    def displays(self):
        return self.EnumDisplays()

DesktopDisplay = DesktopDisplay()
