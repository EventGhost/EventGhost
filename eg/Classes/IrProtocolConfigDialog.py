# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2020 EventGhost Project <http://www.eventghost.net/>
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
import eg


def h_sizer(label, *ctrls):
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(label, 0, wx.EXPAND | wx.ALL, 5)

    for ctrl in ctrls:
        sizer.Add(ctrl, 1, wx.EXPAND | wx.ALL, 5)

    return sizer


class Text(eg.TranslatableStrings):
    title = 'IR Decoder Settings'
    frequency_tolerance = 'Frequency Tolerance:'
    timing_tolerance = 'Timing Tolerance:'

    frequency_tooltip = (
        'How much the frequency is allowed to differ from the specification for the protocol'
    )
    timing_tooltip = (
        'How much a timing is allowed to differ from the specification for the protocol'
    )


class IrProtocolConfigDialog(eg.TaskletDialog):
    instance = None

    def Configure(self, decoder):
        if IrProtocolConfigDialog.instance:
            IrProtocolConfigDialog.instance.Raise()
            return

        IrProtocolConfigDialog.instance = self

        eg.TaskletDialog.__init__(
            self,
            parent=eg.mainFrame,
            title=Text.title,
        )

        notebook = wx.Notebook(self, -1)

        settings_panel = eg.Panel(notebook)
        notebook.AddPage(settings_panel, Text.settings_tab)

        freq_label = settings_panel.StaticText(Text.frequency_tolerance)
        freq_ctrl = settings_panel.SpinNumCtrl(
            value=decoder.frequency_tolerance,
            min=0.01,
            max=30.00,
            increment=0.01
        )
        freq_ctrl.SetToolTipString(Text.frequency_tooltip)
        freq_sizer = h_sizer(freq_label, freq_ctrl)

        timing_label = settings_panel.StaticText(Text.timing_tolerance)
        timing_ctrl = settings_panel.SpinNumCtrl(
            value=decoder.tolerance,
            min=0.01,
            max=30.00,
            increment=0.01
        )
        timing_ctrl.SetToolTipString(Text.timing_tooltip)
        timing_sizer = h_sizer(timing_label, timing_ctrl)

        eg.EqualizeWidths((freq_label, timing_label))

        settings_sizer = wx.BoxSizer(wx.VERTICAL)
        settings_sizer.Add(freq_sizer)
        settings_sizer.Add(timing_sizer)
        settings_panel.SetSizer(settings_sizer)

        buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL))

        sizer = eg.VBoxSizer(
            (notebook, 1, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 5),
            (buttonRow.sizer, 0, wx.EXPAND),
        )
        self.SetSizerAndFit(sizer)
        self.SetMinSize(self.GetSize())
        notebook.ChangeSelection(0)

        freq = freq_ctrl.GetValue()
        timing = timing_ctrl.GetValue()

        while self.Affirmed():
            freq = freq_ctrl.GetValue()
            timing = timing_ctrl.GetValue()
            self.SetResult()

        if self.__dict__['_IrProtocolDialog__lastEventId'] == wx.ID_OK:
            decoder.frequency_tolerance = freq
            decoder.tolerance = timing

        IrProtocolConfigDialog.instance = None
