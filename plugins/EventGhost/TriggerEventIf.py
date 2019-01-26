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

class TriggerEventIf(eg.ActionBase):

    name = "Trigger Event If"
    description = (
        "Causes an event to be generated, if the specified condition is "
        "fulfilled. (optionally after some time)."
    )
    iconFile = "icons/Plugin"

    class text:
        label = [
            'If last action was successful Trigger event "%s" after %.2f seconds',
            'If last action was unsuccessful Trigger event "%s" after %.2f seconds',
            'Always Trigger event "%s" after %.2f seconds',
            'If last action was successful Trigger event "%s"',
            'If last action was unsuccessful Trigger event "%s"',
            'Always Trigger event "%s"'
            ]
        text1 = "Event Prefix:"
        text2 = "Event Suffix:"
        text3 = "Event Payload:"
        text4 = "Delay the firing of the event:"
        text5 = "seconds. (0 = fire immediately)"
        text6 = "If:"
        choices = [
            "last action was successful",
            "last action was unsuccessful",
            "always"
        ]

    def __call__(self, prefix, suffix="", payload="", waitTime=0, kind=0):

        if kind == 2 or (bool(eg.result) != bool(kind)):

            kwargs = dict(prefix=eg.ParseString(prefix))

            if suffix != "":
                kwargs['suffix'] = eg.ParseString(suffix)
            if payload != "":
                try: kwargs['payload'] = eval(payload)
                except: kwargs['payload'] = eg.ParseString(payload)
            if not waitTime:
                eg.TriggerEvent(**kwargs)
            else:
                eg.scheduler.AddShortTask(waitTime, eg.TriggerEvent, eventString)
        return eg.result

    def GetLabel(self, prefix="", suffix="", payload="", waitTime=0, kind=0):

        if suffix != "":
            prefix += '.'+suffix
        if payload != "":
            prefix += ' '+str(payload)
        if waitTime:
            return self.text.label[kind] % (prefix, waitTime)
        else:
            return self.text.label[kind+3] % prefix

    def Configure(self, prefix="", suffix="", payload="", waitTime=0, kind=0):
        panel = eg.ConfigPanel()
        text = self.text

        prefixCtrl = panel.TextCtrl(prefix, size=(250, -1))
        suffixCtrl = panel.TextCtrl(suffix, size=(250, -1))
        payloadCtrl = panel.TextCtrl(payload, size=(250, -1))
        waitTimeCtrl = panel.SpinNumCtrl(waitTime, integerWidth=5)
        kindCtrl = panel.Choice(kind, choices=text.choices)

        sizer1 = eg.HBoxSizer(
            (panel.StaticText(text.text1), 0, wx.ALIGN_CENTER_VERTICAL, 5),
            (prefixCtrl, 0, wx.LEFT, 5),
        )
        sizer2 = eg.HBoxSizer(
            (panel.StaticText(text.text2), 0, wx.ALIGN_CENTER_VERTICAL, 5),
            (suffixCtrl, 0, wx.LEFT, 5),
        )
        sizer3 = eg.HBoxSizer(
            (panel.StaticText(text.text3), 0, wx.ALIGN_CENTER_VERTICAL, 5),
            (payloadCtrl, 0, wx.LEFT, 5),
        )
        sizer4 = eg.HBoxSizer(
            (panel.StaticText(text.text4), 0, wx.ALIGN_CENTER_VERTICAL),
            (waitTimeCtrl, 0, wx.ALL, 5),
            (panel.StaticText(text.text5), 0, wx.ALIGN_CENTER_VERTICAL),
        )
        sizer5 = eg.HBoxSizer(
            (panel.StaticText(text.text6), 0, wx.ALIGN_CENTER_VERTICAL, 5),
            (kindCtrl, 0, wx.LEFT, 5),
        )
        panel.sizer.AddMany((
                            (sizer1, 0, wx.EXPAND),
                            (sizer2, 0, wx.EXPAND),
                            (sizer3, 0, wx.EXPAND),
                            (sizer4, 0, wx.EXPAND),
                            (sizer5, 0, wx.EXPAND)
                            ))

        while panel.Affirmed():
            panel.SetResult(
                prefixCtrl.GetValue(),
                suffixCtrl.GetValue(),
                payloadCtrl.GetValue(),
                waitTimeCtrl.GetValue(),
                kindCtrl.GetValue(),
            )