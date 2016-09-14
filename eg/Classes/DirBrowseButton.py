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

class DirBrowseButton(eg.FileBrowseButton):
    """
    A control to allow the user to type in a filename or browse with the
    standard file dialog to select a directory.
    """
    def __init__(
        self,
        parent,
        id=-1,
        pos = wx.DefaultPosition,
        size = wx.DefaultSize,
        style = wx.TAB_TRAVERSAL,
        labelText = 'Select a directory:',
        buttonText = 'Browse',
        toolTip = 'Type directory name or browse to select',
        dialogTitle = '',
        startDirectory = '.',
        changeCallback = None,
        dialogClass = wx.DirDialog,
        newDirectory = False,
        name = 'dirBrowseButton'
    ):
        eg.FileBrowseButton.__init__(
            self,
            parent,
            id,
            pos,
            size,
            style,
            labelText,
            buttonText,
            toolTip,
            dialogTitle,
            startDirectory,
            changeCallback = changeCallback,
            name = name
        )
        self.dialogClass = dialogClass
        self.newDirectory = newDirectory

    def OnBrowse(self, event=None):
        style = 0

        if not self.newDirectory:
            style |= wx.DD_DIR_MUST_EXIST

        dialog = self.dialogClass(self,
                                  message = self.dialogTitle,
                                  defaultPath = self.startDirectory,
                                  style = style)

        if dialog.ShowModal() == wx.ID_OK:
            self.SetValue(dialog.GetPath())
        dialog.Destroy()
