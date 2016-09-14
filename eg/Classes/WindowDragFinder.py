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

# Local imports
import eg
from eg.Icons import GetInternalBitmap, GetInternalImage
from eg.WinApi import (
    BestWindowFromPoint,
    GetCursorPos,
    GetWindowThreadProcessId,
    HighlightWindow,
)

class WindowDragFinder(wx.PyWindow):
    def __init__(self, parent, startFunc, endFunc):
        self.startFunc = startFunc
        self.endFunc = endFunc

        self.text = eg.plugins.Window.FindWindow.text
        wx.PyWindow.__init__(self, parent, -1, style=wx.SIMPLE_BORDER)
        self.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        )
        self.lastTarget = None

        # load images
        self.dragBoxBitmap = GetInternalBitmap("findert")
        image = GetInternalImage('findertc')
        image.SetMaskColour(255, 0, 0)

        # since this image didn't come from a .cur file, tell it where the
        # hotspot is
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 15)
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 16)

        # make the image into a cursor
        self.cursor = wx.CursorFromImage(image)

        # the image of the drag target
        dragBoxImage = wx.StaticBitmap(self, -1, self.dragBoxBitmap)
        dragBoxImage.SetMinSize(self.dragBoxBitmap.GetSize())
        dragBoxImage.Bind(wx.EVT_LEFT_DOWN, self.OnDragboxClick)
        self.dragBoxImage = dragBoxImage

        # some description for the drag target
        dragBoxText = wx.StaticText(
            self,
            -1,
            self.text.drag2,
            style=wx.ALIGN_CENTRE
        )
        x1, y1 = dragBoxText.GetBestSize()
        dragBoxText.SetLabel(self.text.drag1)
        x2, y2 = dragBoxText.GetBestSize()
        dragBoxText.SetMinSize((max(x1, x2), max(y1, y2)))
        #dragBoxText.Bind(wx.EVT_LEFT_DOWN, self.OnDragboxClick)
        self.dragBoxText = dragBoxText

        self.Bind(wx.EVT_SIZE, self.OnSize)

        # put our drag target together
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(dragBoxImage, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(dragBoxText, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.SetMinSize(self.GetSize())
        wx.CallAfter(self.dragBoxImage.SetBitmap, self.dragBoxBitmap)

    @eg.LogIt
    def AcceptsFocusFromKeyboard(self):
        return False

    def GetValue(self):
        return self.lastTarget

    def OnDrag(self, event):
        # get the mouse coordinates
        point = GetCursorPos()
        # find the window under cursor
        hwnd = BestWindowFromPoint(point)
        # do we have targeted a new window?
        if hwnd != self.lastTarget:
            if self.lastTarget is not None:
                # unhighlight previous window
                HighlightWindow(self.lastTarget)
            _, pid = GetWindowThreadProcessId(hwnd)
            if pid == eg.processId:
                self.lastTarget = None
            else:
                HighlightWindow(hwnd)
                self.lastTarget = hwnd
        event.Skip()

    @eg.LogIt
    def OnDragboxClick(self, event):
        """ Handle left-click on findtool
        """
        if self.HasCapture():
            event.Skip()
            return
        self.startFunc()

        #nothing targeted in the beginning
        self.lastTarget = None

        wx.SetCursor(self.cursor)

        # hide the image while dragging
        self.dragBoxImage.Hide()
        self.dragBoxText.SetLabel(self.text.drag2)
        self.Layout()

        # from now on we want all mouse motion events
        self.Bind(wx.EVT_MOTION, self.OnDrag)
        # and the left up event
        self.Bind(wx.EVT_LEFT_UP, self.OnDragEnd)

        # and call Skip in for handling focus events etc.
        event.ResumePropagation(wx.EVENT_PROPAGATE_MAX)
        event.Skip()
        # start capturing the mouse exclusivly
        self.CaptureMouse()

    def OnDragEnd(self, dummyEvent):
        # unbind the unneeded events
        self.Unbind(wx.EVT_MOTION)
        self.Unbind(wx.EVT_LEFT_UP)

        # stop processing the mouse capture
        self.ReleaseMouse()

        if self.lastTarget is not None:
            # unhighlight last window if we have highlighted one
            HighlightWindow(self.lastTarget)

        self.endFunc()

        # revert box to normal image
        self.dragBoxText.SetLabel(self.text.drag1)
        self.dragBoxImage.Show()
        self.Layout()
        self.dragBoxImage.SetBitmap(self.dragBoxBitmap)

    def OnSize(self, dummyEvent):
        """
        Handles the wx.EVT_SIZE events.
        """
        if self.GetAutoLayout():
            self.Layout()
            self.dragBoxImage.SetBitmap(self.dragBoxBitmap)
