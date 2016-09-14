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

class MessageDialog(wx.Dialog):
    """
    A replacement for wx.MessageDialog, that wraps the message, if the
    dialog would get to wide.
    """
    def __init__(
        self,
        parent,
        message,
        caption=eg.APP_NAME,
        style=wx.OK | wx.CANCEL,
        pos=wx.DefaultPosition
    ):
        if parent is None and eg.document.frame:
            parent = eg.document.frame
        dialogStyle = wx.DEFAULT_DIALOG_STYLE
        if style & wx.STAY_ON_TOP:
            dialogStyle |= wx.STAY_ON_TOP
        wx.Dialog.__init__(self, parent, -1, caption, pos, style=dialogStyle)

        if style & wx.ICON_EXCLAMATION:
            artId = wx.ART_WARNING
        elif style & wx.ICON_HAND:
            artId = wx.ART_ERROR
        elif style & wx.ICON_ERROR:
            artId = wx.ART_ERROR
        elif style & wx.ICON_QUESTION:
            artId = wx.ART_QUESTION
        elif style & wx.ICON_INFORMATION:
            artId = wx.ART_INFORMATION
        else:
            artId = None

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        if artId is not None:
            bmp = wx.ArtProvider.GetBitmap(artId, wx.ART_CMN_DIALOG, (32, 32))
            staticBitmap = wx.StaticBitmap(self, -1, bmp)
            sizer.Add(staticBitmap, 0, wx.ALL, 12)
        staticText = wx.StaticText(self, -1, message)
        staticText.Wrap(400)
        sizer.Add(staticText, 0, wx.ALIGN_CENTER | wx.LEFT | wx.TOP | wx.RIGHT, 6)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        text = eg.text.General
        if wx.YES_NO & style:
            yesButton = wx.Button(self, wx.ID_YES, text.yes)
            buttonSizer.Add(yesButton, 0, wx.LEFT | wx.RIGHT, 3)
            noButton = wx.Button(self, wx.ID_NO, text.no)
            buttonSizer.Add(noButton, 0, wx.LEFT | wx.RIGHT, 3)
            if wx.NO_DEFAULT & style:
                self.SetDefaultItem(noButton)
                noButton.SetFocus()
            else:
                self.SetDefaultItem(yesButton)
                yesButton.SetFocus()
            yesButton.Bind(wx.EVT_BUTTON, self.OnYesButton)
            noButton.Bind(wx.EVT_BUTTON, self.OnNoButton)
        else:
            okButton = wx.Button(self, wx.ID_OK, text.ok)
            buttonSizer.Add(okButton, 0, wx.LEFT | wx.RIGHT, 3)
        if wx.CANCEL & style:
            cancelButton = wx.Button(self, wx.ID_CANCEL, text.cancel)
            buttonSizer.Add(cancelButton, 0, wx.LEFT | wx.RIGHT, 3)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sizer)
        mainSizer.Add(buttonSizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 12)
        self.SetSizerAndFit(mainSizer)
        if parent and pos == wx.DefaultPosition:
            self.CenterOnParent()

    def OnNoButton(self, event):
        self.EndModal(wx.ID_NO)
        event.Skip()

    def OnYesButton(self, event):
        self.EndModal(wx.ID_YES)
        event.Skip()
