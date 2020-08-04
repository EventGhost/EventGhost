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


def v_sizer(label, *ctrls):
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(label, 0, wx.EXPAND | wx.ALL, 5)
    for ctrl in ctrls:
        sizer.Add(ctrl, 1, wx.EXPAND | wx.ALL, 5)

    return sizer


def h_sizer(label, *ctrls):
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(label, 0, wx.EXPAND | wx.ALL, 5)

    for ctrl in ctrls:
        sizer.Add(ctrl, 1, wx.EXPAND | wx.ALL, 5)

    return sizer


class Text(eg.TranslatableStrings):
    title = 'Add IR Code'
    rlc_tab = 'RLC'
    pronto_tab = 'Pronto Hex'
    help_tab = 'Help'
    pronto_label = 'Pronto Code'
    frame0_label = 'RLC Frame 0'
    frame1_label = 'RLC Frame 1'
    frame2_label = 'RLC Frame 2'
    frequency_label = 'Frequency:'


class IrCodeTextDialog(eg.TaskletDialog):

    instance = None

    def Configure(self, decoder):
        if IrCodeTextDialog.instance:
            IrCodeTextDialog.instance.Raise()
            return

        IrCodeTextDialog.instance = self

        eg.TaskletDialog.__init__(
            self,
            parent=eg.mainFrame,
            title=Text.title,
        )

        notebook = wx.Notebook(self, -1)

        pronto_panel = eg.Panel(notebook)

        pronto_label = wx.StaticText(pronto_panel, -1, Text.pronto_label)
        pronto_ctrl = wx.TextCtrl(pronto_panel, -1, '', style=wx.TE_MULTILINE)
        pronto_sizer = v_sizer(pronto_label, pronto_ctrl)

        pronto_panel.SetSizer(pronto_sizer)
        notebook.AddPage(pronto_panel, Text.pronto_tab)

        rlc_panel = eg.Panel(notebook)

        frame0_label = wx.StaticText(rlc_panel, -1, Text.frame0_label)
        frame0_ctrl = wx.TextCtrl(rlc_panel, -1, '', style=wx.TE_MULTILINE)
        frame0_sizer = v_sizer(frame0_label, frame0_ctrl)

        frame1_label = wx.StaticText(rlc_panel, -1, Text.frame1_label)
        frame1_ctrl = wx.TextCtrl(rlc_panel, -1, '', style=wx.TE_MULTILINE)
        frame1_sizer = v_sizer(frame1_label, frame1_ctrl)

        frame2_label = wx.StaticText(rlc_panel, -1, Text.frame2_label)
        frame2_ctrl = wx.TextCtrl(rlc_panel, -1, '', style=wx.TE_MULTILINE)
        frame2_sizer = v_sizer(frame2_label, frame2_ctrl)

        frequency_label = wx.StaticText(rlc_panel, -1, Text.frequency_label)
        frequency_ctrl = wx.TextCtrl(rlc_panel, -1, '00000')
        frequency_sizer = h_sizer(frequency_label, frequency_ctrl)
        rlc_sizer = wx.BoxSizer(wx.VERTICAL)

        rlc_sizer.Add(frequency_sizer, 0, wx.ALL | 5)
        rlc_sizer.Add(frame0_sizer, 0, wx.ALL | 5)
        rlc_sizer.Add(frame1_sizer, 0, wx.ALL | 5)
        rlc_sizer.Add(frame2_sizer, 0, wx.ALL | 5)

        rlc_panel.SetSizer(rlc_sizer)
        notebook.AddPage(rlc_panel, Text.rlc_tab)

        buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL))

        sizer = eg.VBoxSizer(
            (notebook, 1, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 5),
            (buttonRow.sizer, 0, wx.EXPAND),
        )
        self.SetSizerAndFit(sizer)
        self.SetMinSize(self.GetSize())
        notebook.ChangeSelection(0)

        import pyIRDecoder

        while self.Affirmed():
            pronto_code = pronto_ctrl.GetValue().strip()
            try:
                frequency, code = pyIRDecoder.pronto_to_rlc(pronto_code)
            except:
                def _get_frame(ctrl):
                    value = ctrl.GetValue().strip()
                    value = value.replace('[', '').replace(']', '')
                    return list(int(item.strip()) for item in value.split(','))

                frame0 = _get_frame(frame0_ctrl)
                frame1 = _get_frame(frame0_ctrl)
                frame2 = _get_frame(frame0_ctrl)
                frequency = int(frequency_ctrl.GetValue().strip())
                code = [
                    frame0,
                    frame1,
                    frame2,
                ]

            code = decoder.decode(code, frequency=frequency)
            self.SetResult(code)

        IrCodeTextDialog.instance = None
