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

import wx
import eg

    
class NewJumpIf(eg.ActionClass):
    name = "Jump"
    description = \
        "Jumps to another macro, if the specified condition is "\
        "fulfilled."
    iconFile = "icons/NewJumpIf"
    class text:
        text1 = "If:"
        text2 = "Jump to:"
        text3 = "and return after execution"
        mesg1 = "Select the macro..."
        mesg2 = \
            "Please select the macro that should be executed, if the "\
            "condition is fulfilled."
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
        if (bool(eg.result) != bool(kind)) or kind == 2:
            if gosub:
                eg.programReturnStack.append(eg.programCounter)
            next = link.target
            next_id = next.parent.GetChildIndex(next)
            eg.SetProgramCounter((next, next_id))
        return eg.result
    
        
    def GetLabel(self, link, kind=0, gosub=False):
        return self.text.labels[kind + int(gosub) * 3] % link.target.name


    def Configure(self, link=None, kind=0, gosub=False):
        dialog = eg.ConfigurationDialog(self)
        text = self.text
        if link is None:
            link = eg.TreeLink(eg.currentConfigureItem)
        ch = wx.Choice(dialog, choices=text.choices)
        ch.SetSelection(kind)
        label1 = wx.StaticText(dialog, -1, text.text1)
        label2 = wx.StaticText(dialog, -1, text.text2)
        button = eg.BrowseMacroButton(
            dialog,
            eg.text.General.choose,
            text.mesg1,
            text.mesg2,
            link.target
        )
        gosubCB = wx.CheckBox(dialog, -1, text.text3)
        gosubCB.SetValue(gosub)
        sizer = wx.FlexGridSizer(2,2,5,5)
        sizer.AddGrowableCol(1, 1)
        sizer.AddGrowableRow(1, 1)
        sizer.Add(label1, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(ch, 0, wx.EXPAND)
        sizer.Add(label2, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(button, 1, wx.EXPAND)
        sizer.Add((0,0))
        sizer.Add(gosubCB, 0, wx.EXPAND)
        dialog.sizer.Add(sizer, 0, wx.EXPAND)
        
        if dialog.AffirmedShowModal():
            link.SetTarget(button.GetValue())
            return (link, ch.GetSelection(), gosubCB.GetValue())
