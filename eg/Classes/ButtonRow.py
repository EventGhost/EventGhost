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

STANDARD_IDS = (wx.ID_OK, wx.ID_CANCEL, wx.ID_APPLY, wx.ID_HELP)

class ButtonRow(object):
    def __init__(self, parent, buttonIds, resizeGrip=False, center=False):
        self.parent = parent
        self.numSpecialCtrls = 0
        buttonSizer = wx.StdDialogButtonSizer()
        defaultButton = None
        text = eg.text.General
        for ctrl in buttonIds:
            if ctrl not in STANDARD_IDS:
                buttonSizer.Add(ctrl)

        if wx.ID_OK in buttonIds:
            okButton = wx.Button(parent, wx.ID_OK, text.ok)
            okButton.Bind(wx.EVT_BUTTON, self.OnOK)
            buttonSizer.AddButton(okButton)
            defaultButton = okButton
            self.okButton = okButton

        if wx.ID_CANCEL in buttonIds:
            cancelButton = wx.Button(parent, wx.ID_CANCEL, text.cancel)
            cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
            buttonSizer.AddButton(cancelButton)
            if not defaultButton:
                defaultButton = cancelButton
            self.cancelButton = cancelButton

        if wx.ID_APPLY in buttonIds:
            applyButton = wx.Button(parent, wx.ID_APPLY, text.apply)
            applyButton.Bind(wx.EVT_BUTTON, self.OnApply)
            buttonSizer.AddButton(applyButton)
            if not defaultButton:
                defaultButton = applyButton
            self.applyButton = applyButton

        if wx.ID_HELP in buttonIds:
            helpButton = wx.Button(parent, wx.ID_HELP, text.help)
            helpButton.Bind(wx.EVT_BUTTON, self.OnHelp)
            buttonSizer.AddButton(helpButton)
            if not defaultButton:
                defaultButton = helpButton
            self.helpButton = helpButton

        buttonSizer.Realize()
        defaultButton.SetDefault()

        self.sizer = sizer = wx.BoxSizer(wx.HORIZONTAL)
        if resizeGrip:
            self.sizeGrip = eg.SizeGrip(parent)
            if center:
                sizer.Add(self.sizeGrip.GetSize(), 0, wx.EXPAND)
                sizer.Add((1, 1), 1, wx.EXPAND)
                sizer.Add(buttonSizer, 0, wx.TOP | wx.BOTTOM, 6)
                sizer.Add((1, 1), 1, wx.EXPAND)
            else:
                sizer.Add(self.sizeGrip.GetSize(), 1, wx.EXPAND)
                sizer.Add(buttonSizer, 0, wx.TOP | wx.BOTTOM, 6)
            sizer.Add(self.sizeGrip, 0, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT)
        else:
            if center:
                sizer.Add((3, 3), 1, wx.EXPAND)
                sizer.Add(buttonSizer, 0, wx.TOP | wx.BOTTOM, 6)
                sizer.Add((3, 3), 1, wx.EXPAND)
            else:
                sizer.Add((3, 3), 1)
                sizer.Add(buttonSizer, 0, wx.TOP | wx.BOTTOM, 6)
                sizer.Add((3, 3), 0)

    def Add(
        self,
        ctrl,
        proportion=0,
        flags=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT,
        border=5
    ):
        if self.numSpecialCtrls == 0:
            self.sizer.Insert(0, (15, 5))
        self.sizer.Insert(
            self.numSpecialCtrls + 1,
            ctrl,
            proportion,
            flags,
            border
        )
        self.numSpecialCtrls += 1

    def OnApply(self, event):
        if hasattr(self.parent, "OnApply"):
            self.parent.OnApply(event)
        else:
            event.Skip()

    def OnCancel(self, event):
        if hasattr(self.parent, "OnCancel"):
            self.parent.OnCancel(event)
        else:
            event.Skip()

    def OnHelp(self, event):
        if hasattr(self.parent, "OnHelp"):
            self.parent.OnHelp(event)
        else:
            event.Skip()

    def OnOK(self, event):
        if hasattr(self.parent, "OnOK"):
            self.parent.OnOK(event)
        else:
            event.Skip()
