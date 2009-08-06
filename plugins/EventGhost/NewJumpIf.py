# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import eg
import wx


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
            'If successful jump to "%s"',
            'If unsuccessful jump to "%s"',
            'Jump to "%s"',
            'If successful jump to "%s" and return',
            'If unsuccessful jump to "%s" and return',
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


    def GetLabel(self, link, kind=0, gosub=False):
        return self.text.labels[kind + int(gosub) * 3] % link.target.name


    def Configure(self, link=None, kind=0, gosub=False):
        text = self.text
        if link is None:
            link = eg.TreeLink(eg.currentConfigureItem)
        panel = eg.ConfigPanel()
        kindCtrl = panel.Choice(kind, choices=text.choices)
        linkCtrl = panel.MacroSelectButton(
            eg.text.General.choose,
            text.mesg1,
            text.mesg2,
            link.target
        )
        gosubCtrl = panel.CheckBox(gosub, text.text3)

        panel.SetColumnFlags(1, wx.EXPAND)
        panel.AddLine(text.text1, kindCtrl)
        panel.AddLine(text.text2, linkCtrl)
        panel.AddLine(None, gosubCtrl)

        while panel.Affirmed():
            link.SetTarget(linkCtrl.GetValue())
            panel.SetResult(link, kindCtrl.GetValue(), gosubCtrl.GetValue())

