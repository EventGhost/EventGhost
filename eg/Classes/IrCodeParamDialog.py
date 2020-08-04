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
    title = 'Add IR Code'
    tab_label = 'IR Code Parameters'


class IrCodeParamDialog(eg.TaskletDialog):
    instance = None

    def Configure(self, decoder):
        if IrCodeParamDialog.instance:
            IrCodeParamDialog.instance.Raise()
            return

        IrCodeParamDialog.instance = self

        eg.TaskletDialog.__init__(
            self,
            parent=eg.mainFrame,
            title=Text.title,
        )

        notebook = wx.Notebook(self, -1)

        settings_panel = eg.Panel(notebook)
        notebook.AddPage(settings_panel, Text.tab_label)
        labels = []
        controls = []

        settings_sizer = wx.BoxSizer(wx.VERTICAL)

        for name, min_value, max_value in decoder.encode_parameters:
            label = name.replace('_', ' ').title() + ':'
            label = settings_panel.StaticText(label)
            labels += [label]

            values = list(range(min_value, max_value))

            if hasattr(decoder, name):
                if getattr(decoder, name) != values:
                    values = list(str(item for item in getattr(decoder, name)))

                    ctrl = wx.Choice(settings_panel, -1, choices=values)
                    ctrl.SetSelection(0)
                else:
                    ctrl = settings_panel.SpinIntCtrl(
                        value=min_value,
                        min=min_value,
                        max=max_value
                    )
            else:
                ctrl = settings_panel.SpinIntCtrl(
                    value=min_value,
                    min=min_value,
                    max=max_value
                )

            controls += [ctrl]

            ctrl_sizer = h_sizer(label, ctrl)
            settings_sizer.Add(ctrl_sizer)

        eg.EqualizeWidths(tuple(labels))
        eg.EqualizeWidths(tuple(controls))

        settings_panel.SetSizer(settings_sizer)

        buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL))

        sizer = eg.VBoxSizer(
            (notebook, 1, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 5),
            (buttonRow.sizer, 0, wx.EXPAND),
        )
        self.SetSizerAndFit(sizer)
        self.SetMinSize(self.GetSize())
        notebook.ChangeSelection(0)

        while self.Affirmed():

            params = {}

            for i, (param_name, _, __) in enumerate(decoder.encode_parameters):
                control = controls[i]

                if isinstance(control, eg.SpinIntCtrl):
                    value = control.GetValue()
                else:
                    value = control.GetStringSelection()

                    try:
                        value = int(value)
                    except TypeError:
                        pass

                params[param_name] = value

            code = decoder.encode(**params)

            self.SetResult(code)

        IrCodeParamDialog.instance = None
