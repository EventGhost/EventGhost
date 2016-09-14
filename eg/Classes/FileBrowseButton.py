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
from wx.lib.filebrowsebutton import FileBrowseButton as _FileBrowseButton

# Local imports
from eg.Icons import GetInternalBitmap

class FileBrowseButton(_FileBrowseButton):
    """
    A control to allow the user to type in a filename or browse with the
    standard file dialog to select a file.
    """
    def createBrowseButton(self):
        """
        Create the browse-button control
        """
        button = wx.BitmapButton(self, -1, GetInternalBitmap("searchFolder"))
        width, height = button.GetSize()
        button.SetMinSize((width + 8, height))
        button.SetToolTipString(self.toolTip)
        button.Bind(wx.EVT_BUTTON, self.OnBrowse)
        return button

    def createDialog(self, parent, id, pos, size, style, name=""):
        """
        Setup the graphic representation of the dialog
        """
        wx.Panel.__init__(self, parent, id, pos, size, style, name)
        self.SetMinSize(size)  # play nice with sizers

        box = wx.BoxSizer(wx.HORIZONTAL)

        self.textControl = self.createTextControl()
        box.Add(self.textControl, 1, wx.CENTER, 5)

        self.browseButton = self.createBrowseButton()
        box.Add(self.browseButton, 0, wx.LEFT | wx.CENTER, 5)

        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()
        if isinstance(size, tuple):
            size = apply(wx.Size, size)
        self.SetDimensions(
            -1, -1, size.width, size.height, wx.SIZE_USE_EXISTING
        )

    def Enable(self, enable=True):
        self.textControl.Enable(enable)
        return self.browseButton.Enable(enable)

    def OnChanged(self, evt):
        if self.callCallback and self.changeCallback:
            self.changeCallback(evt)
        #ADDED:
        evt.Skip()
