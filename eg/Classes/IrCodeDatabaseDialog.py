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
import requests


def h_sizer(label, *ctrls):
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(label, 0, wx.EXPAND | wx.ALL, 5)

    for ctrl in ctrls:
        sizer.Add(ctrl, 1, wx.EXPAND | wx.ALL, 5)

    return sizer


class Text(eg.TranslatableStrings):
    title = 'Add IR Code'
    tab_label = 'Database IR Codes'
    manufacturer_label = 'Manufacturer:'
    category_label = 'Category:'
    model_label = 'Model:'
    key_label = 'Key:'


class IrCodeDatabaseDialog(eg.TaskletDialog):
    instance = None

    def Configure(self, decoder):
        if IrCodeDatabaseDialog.instance:
            IrCodeDatabaseDialog.instance.Raise()
            return

        IrCodeDatabaseDialog.instance = self

        eg.TaskletDialog.__init__(
            self,
            parent=eg.mainFrame,
            title=Text.title,
        )

        notebook = wx.Notebook(self, -1)

        database_panel = eg.Panel(notebook)

        mfgs = requests.get('www.eventghost.net:43847/ir_codes/manufacturers')
        mfgs = mfgs.content

        manufacturer_label = wx.StaticText(self, -1, Text.manufacturer_label)
        self.manufacturer_ctrl = wx.Choice(self, -1, choices=mfgs.split('\n'))
        manufacturer_sizer = h_sizer(manufacturer_label, self.manufacturer_ctrl)
        self.manufacturer_ctrl.Bind(wx.EVT_CHOICE, self.on_manufacturer)

        category_label = wx.StaticText(self, -1, Text.category_label)
        self.category_ctrl = wx.Choice(self, -1, choices=[])
        category_sizer = h_sizer(category_label, self.category_ctrl)
        self.category_ctrl.Bind(wx.EVT_CHOICE, self.on_category)

        model_label = wx.StaticText(self, -1, Text.model_label)
        self.model_ctrl = wx.Choice(self, -1, choices=[])
        model_sizer = h_sizer(model_label, self.model_ctrl)
        self.model_ctrl.Bind(wx.EVT_CHOICE, self.on_model)

        key_label = wx.StaticText(self, -1, Text.key_label)
        self.key_ctrl = wx.Choice(self, -1, choices=[])
        key_sizer = h_sizer(key_label, self.key_ctrl)

        database_sizer = wx.BoxSizer(wx.VERTICAL)
        database_sizer.Add(manufacturer_sizer, 0, wx.EXPAND)
        database_sizer.Add(category_sizer, 0, wx.EXPAND)
        database_sizer.Add(model_sizer, 0, wx.EXPAND)
        database_sizer.Add(key_sizer, 0, wx.EXPAND)

        eg.EqualizeWidths((
            self.manufacturer_ctrl,
            self.category_ctrl,
            self.model_ctrl,
            self.key_ctrl
        ))
        eg.EqualizeWidths((
            manufacturer_label,
            category_label,
            model_label,
            key_label
        ))

        notebook.AddPage(database_panel, Text.tab_label)
        database_panel.SetSizer(database_sizer)

        buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL))

        sizer = eg.VBoxSizer(
            (notebook, 1, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 5),
            (buttonRow.sizer, 0, wx.EXPAND),
        )
        self.SetSizerAndFit(sizer)
        self.SetMinSize(self.GetSize())
        notebook.ChangeSelection(0)

        while self.Affirmed():
            manufacturer = self.manufacturer_ctrl.GetStringSelection()
            category = self.category_ctrl.GetStringSelection()
            model = self.model_ctrl.GetStringSelection()
            key = self.key_ctrl.GetStringSelection()
            params = requests.get(
                'www.eventghost.net:43847/ir_codes/' + manufacturer + '/' + category + '/' + model + '/' + key
            )
            params = params.json()

            decoder_name = params.pop('decoder')
            code_name = params.pop('name')
            rlc = params.pop('rlc')

            for d in decoder:
                if d.name == decoder_name:
                    from pyIRDecoder import ir_code
                    code = ir_code.IRCode(d, rlc[:], rlc[:], params, name=code_name)
                    break
            else:
                code = None

            self.SetResult(code)

        IrCodeDatabaseDialog.instance = None

    def on_manufacturer(self, _):
        manufacturer = self.manufacturer_ctrl.GetStringSelection()
        choices = requests.get('www.eventghost.net:43847/ir_codes/' + manufacturer + '/categories')
        choices = choices.content.split('\n')
        self.category_ctrl.Clear()
        self.category_ctrl.SetItems(choices)
        self.category_ctrl.SetSelection(0)
        self.on_category(None)

    def on_category(self, _):
        manufacturer = self.manufacturer_ctrl.GetStringSelection()
        category = self.category_ctrl.GetStringSelection()
        choices = requests.get('www.eventghost.net:43847/ir_codes/' + manufacturer + '/' + category + '/models')
        choices = choices.content.split('\n')
        self.model_ctrl.Clear()
        self.model_ctrl.SetItems(choices)
        self.model_ctrl.SetSelection(0)
        self.on_model(None)

    def on_model(self, _):
        manufacturer = self.manufacturer_ctrl.GetStringSelection()
        category = self.category_ctrl.GetStringSelection()
        model = self.model_ctrl.GetStringSelection()
        choices = requests.get(
            'www.eventghost.net:43847/ir_codes/' + manufacturer + '/' + category + '/' + model + '/keys'
        )

        choices = choices.content.split('\n')
        self.key_ctrl.Clear()
        self.key_ctrl.SetItems(choices)
        self.key_ctrl.SetSelection(0)
