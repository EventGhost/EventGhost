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

class NewJumpIf(eg.ActionBase):
    name = "Jump"
    description = (
        "Jumps to another macro, if the specified condition is "
        "fulfilled."
    )
    iconFile = "icons/NewJumpIf"

    class text:
        text1 = "If:"
        text2 = "Jump to:"
        text3 = "and return after execution"
        mesg1 = "Select the macro..."
        mesg2 = (
            "Please select the macro that should be executed, if the "
            "condition is fulfilled."
        )
        choices = [
            "last action was successful",
            "last action was unsuccessful",
            "always"
        ]
        labels = [
            'If successful, jump to "%s"',
            'If unsuccessful, jump to "%s"',
            'Jump to "%s"',
            'If successful, jump to "%s" and return',
            'If unsuccessful, jump to "%s" and return',
            'Jump to "%s" and return'
        ]

    def __call__(self, link, kind=0, gosub=False):
        if kind == 2 or (bool(eg.result) != bool(kind)):
            if gosub:
                eg.programReturnStack.append(eg.programCounter)
            nextItem = link.target
            nextIndex = nextItem.parent.GetChildIndex(nextItem)
            eg.indent += 1
            eg.programCounter = (nextItem, nextIndex)
        return eg.result

    def Configure(self, link=None, kind=0, gosub=False):
        text = self.text
        panel = eg.ConfigPanel()
        kindCtrl = panel.Choice(kind, choices=text.choices)
        linkCtrl = panel.MacroSelectButton(
            eg.text.General.choose,
            text.mesg1,
            text.mesg2,
            link
        )
        gosubCtrl = panel.CheckBox(gosub, text.text3)

        labels = (
            panel.StaticText(text.text1),
            panel.StaticText(text.text2),
        )
        eg.EqualizeWidths(labels)
        sizer = wx.FlexGridSizer(3, 2, 15, 5)
        sizer.AddGrowableCol(1, 1)
        sizer.Add(labels[0], 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(kindCtrl)
        sizer.Add(labels[1], 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(linkCtrl, 1, wx.EXPAND)
        sizer.Add((0, 0))
        sizer.Add(gosubCtrl)
        panel.sizer.Add(sizer, 1, wx.EXPAND, wx.ALIGN_CENTER_VERTICAL)

        while panel.Affirmed():
            panel.SetResult(
                linkCtrl.GetValue(),
                kindCtrl.GetValue(),
                gosubCtrl.GetValue()
            )

    def GetLabel(self, link, kind=0, gosub=False):
        return self.text.labels[kind + int(gosub) * 3] % link.target.name
