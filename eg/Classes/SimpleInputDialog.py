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
import threading


PROMPT = "Please type your input..."

class SimpleInputDialog(eg.TaskletDialog):

    def Configure(self, prompt=None, initialValue=""):
        if prompt is None:
            prompt = PROMPT
        eg.TaskletDialog.__init__(
            self, None, -1, PROMPT, style=wx.RESIZE_BORDER|wx.CAPTION
        )
        textCtrl = self.TextCtrl(initialValue, size=(300, -1))
        buttonRow = eg.ButtonRow(self, [wx.ID_OK])
        mainSizer = eg.VBoxSizer(
            (self.StaticText(prompt), 0, wx.EXPAND|wx.ALL, 5),
            (textCtrl, 0, wx.EXPAND|wx.ALL, 5),
            ((5, 5), 1, wx.EXPAND),
            (wx.StaticLine(self), 0, wx.EXPAND),
            (buttonRow.sizer, 0, wx.EXPAND),
        )
        self.SetSizerAndFit(mainSizer)
        self.SetMinSize(self.GetSize())
        while self.Affirmed():
            self.SetResult(textCtrl.GetValue())


    @classmethod
    def RawInput(cls, prompt):
        returnValue = []
        event = threading.Event()
        @eg.AsTasklet
        def Task():
            result = cls.GetResult(prompt)
            returnValue.append(result[0])
            event.set()

        wx.CallAfter(Task)
        event.wait()
        return returnValue[0]

