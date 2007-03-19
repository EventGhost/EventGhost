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

from wx.lib.filebrowsebutton import FileBrowseButton
import wx
import types


def createDialog( self, parent, id, pos, size, style ):
    """Setup the graphic representation of the dialog"""
    wx.Panel.__init__ (self, parent, id, pos, size, style)
    self.SetMinSize(size) # play nice with sizers

    box = wx.BoxSizer(wx.HORIZONTAL)

    self.textControl = self.createTextControl()
    box.Add(self.textControl, 1, wx.CENTER, 5)

    self.browseButton = self.createBrowseButton()
    box.Add(self.browseButton, 0, wx.LEFT|wx.CENTER, 5)

    self.SetAutoLayout(True)
    self.SetSizer(box)
    self.Layout()
    if type(size) == types.TupleType:
        size = apply(wx.Size, size)
    self.SetDimensions(-1, -1, size.width, size.height, wx.SIZE_USE_EXISTING)


def createBrowseButton( self):
    """Create the browse-button control"""
    button = wx.BitmapButton(self, -1, wx.Bitmap("images/searchFolder.png"))
    w, h = button.GetSize()
    button.SetMinSize((w + 8, h))
    button.SetToolTipString(self.toolTip)
    button.Bind(wx.EVT_BUTTON, self.OnBrowse)
    return button


FileBrowseButton.createDialog = createDialog
FileBrowseButton.createBrowseButton = createBrowseButton

