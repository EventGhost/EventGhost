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
from . import o_scope
from .utils import h_sizer, v_sizer
from .decoders import pronto
import requests


class CodePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)

        name_ctrl = self.name_ctrl = wx.TextCtrl(self, -1, ' ' * 15)
        name_label = wx.StaticText(self, -1, 'Name:')
        name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        name_sizer.Add(name_label, 0, wx.EXPAND | wx.ALL, 5)
        name_sizer.Add(name_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        protocol_ctrl = self.protocol_ctrl = wx.TextCtrl(self, -1, ' ' * 15, style=wx.TE_READONLY)
        protocol_label = wx.StaticText(self, -1, 'Protocol:')
        protocol_sizer = h_sizer(protocol_label, protocol_ctrl)

        frequency_ctrl = self.frequency_ctrl = wx.TextCtrl(self, -1, '00000', style=wx.TE_READONLY)
        frequency_label = wx.StaticText(self, -1, 'Frequency:')
        frequency_suffix = wx.StaticText(self, -1, 'hz')
        frequency_sizer = h_sizer(frequency_label, frequency_ctrl, frequency_suffix)

        line_1_sizer = wx.BoxSizer(wx.VERTICAL)
        line_1_sizer.Add(name_sizer, 1, wx.EXPAND)
        line_1_sizer.Add(protocol_sizer, 0, wx.EXPAND)
        line_1_sizer.Add(frequency_sizer, 0, wx.EXPAND)

        parameter_ctrl = self.parameter_ctrl = wx.TextCtrl(
            self,
            -1,
            '\n' * 3,
            style=wx.TE_MULTILINE | wx.TE_READONLY
        )
        parameter_label = wx.StaticText(self, -1, 'Parameters:')
        parameter_sizer = h_sizer(parameter_label, parameter_ctrl)

        original_rlc_ctrl = self.original_rlc_ctrl = wx.TextCtrl(
            self,
            -1,
            '',
            style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_BESTWRAP
        )
        original_rlc_label = wx.StaticText(self, -1, 'Original RLC')
        original_rlc_sizer = v_sizer(original_rlc_label, original_rlc_ctrl)

        original_pronto_ctrl = self.original_pronto_ctrl = wx.TextCtrl(
            self,
            -1,
            '',
            style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_BESTWRAP
        )
        original_pronto_label = wx.StaticText(self, -1, 'Original Pronto')
        original_pronto_sizer = v_sizer(original_pronto_label, original_pronto_ctrl)

        normalized_rlc_ctrl = self.normalized_rlc_ctrl = wx.TextCtrl(
            self,
            -1,
            '',
            style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_BESTWRAP
        )
        normalized_rlc_label = wx.StaticText(self, -1, 'Normalized RLC')
        normalized_rlc_sizer = v_sizer(normalized_rlc_label, normalized_rlc_ctrl)

        normalized_pronto_ctrl = self.normalized_pronto_ctrl = wx.TextCtrl(
            self,
            -1,
            '',
            style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_BESTWRAP
        )
        normalized_pronto_label = wx.StaticText(self, -1, 'Normalized Pronto')
        normalized_pronto_sizer = v_sizer(normalized_pronto_label, normalized_pronto_ctrl)

        scope_ctrl = self.scope_ctrl = o_scope.Oscilloscope(self)

        static_line2 = wx.StaticLine(self, -1, size=(0, 5), style=wx.LI_HORIZONTAL)
        static_line3 = wx.StaticLine(self, -1, size=(0, 5), style=wx.LI_HORIZONTAL)
        static_line4 = wx.StaticLine(self, -1, size=(0, 5), style=wx.LI_HORIZONTAL)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(original_rlc_sizer, 1, wx.EXPAND)
        sizer1.Add(normalized_rlc_sizer, 1, wx.EXPAND)

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(original_pronto_sizer, 1, wx.EXPAND)
        sizer2.Add(normalized_pronto_sizer, 1, wx.EXPAND)

        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(line_1_sizer, 1, wx.EXPAND)
        sizer3.Add(parameter_sizer, 1, wx.EXPAND)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer3, 0, wx.EXPAND)
        sizer.Add(static_line2, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(sizer1, 0, wx.EXPAND)
        sizer.Add(static_line3, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(sizer2, 0, wx.EXPAND)
        sizer.Add(static_line4, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(scope_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)

    def SetValue(self, name, code):
        self.name_ctrl.SetValue(name)

        decoder = code['decoder']
        self.protocol_ctrl.SetValue(decoder)

        frequency = code['frequency']
        self.frequency_ctrl.SetValue(str(frequency))

        data = []
        line = ''
        for i, param in enumerate(code['params']):
            val = '0x' + hex(code[param])[2:].upper().zfill(6)
            param += ' ' * (10 - len(param))
            if i % 2:
                line += '   |   ' + param + ' = ' + val
                data += [line]
                line = ''
            else:
                line += '  ' + param + ' = ' + val

        self.parameter_ctrl.SetValue('\n'.join(data))

        o_rlc = code['original_rlc']
        n_rlc = code['normalized_rlc']

        o_pronto = pronto.rlc_to_pronto(frequency, o_rlc)
        n_pronto = pronto.rlc_to_pronto(frequency, n_rlc)

        def get_timing(timing):
            if timing < 0:
                return str(timing)
            else:
                return '+' + str(timing)

        self.original_rlc_ctrl.SetValue(', '.join(get_timing(item) for item in o_rlc))
        self.original_pronto_ctrl.SetValue(o_pronto)
        self.normalized_rlc_ctrl.SetValue(', '.join(get_timing(item) for item in n_rlc))
        self.normalized_pronto_ctrl.SetValue(n_pronto)
        self.scope_ctrl.SetValue(o_rlc, n_rlc)


class CodesPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)

        choice_ctrl = self.choice_ctrl = wx.ComboBox(
            self,
            -1,
            choices=[]
        )

        choice_ctrl.Bind(wx.EVT_CHAR_HOOK, self.on_choice_enter)
        choice_ctrl.Bind(wx.EVT_COMBOBOX, self.on_choice)

        choice_label = wx.StaticText(self, -1, 'Select Code:')
        choice_sizer = h_sizer(choice_label, choice_ctrl)

        static_line1 = wx.StaticLine(self, -1, size=(0, 5), style=wx.LI_HORIZONTAL)
        code_panel = self.code_panel = CodePanel(self)

        code_panel.name_ctrl.Bind(wx.EVT_CHAR_HOOK, self.on_name_enter)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(choice_sizer, 0)
        sizer.Add(static_line1, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(code_panel, 1, wx.EXPAND)

        self.loaded_code = None

        self.SetSizer(sizer)
        self.update_choices()

    def on_name_enter(self, evt):
        if evt.GetKeyCode() == wx.WXK_RETURN:
            new_value = self.code_panel.name_ctrl.GetValue()
            old_value = self.choice_ctrl.GetValue()

            if old_value in Config.codes:
                code = Config.codes.pop(old_value)
            else:
                code = self.loaded_code

            Config.codes[new_value] = code
            self.update_choices()
            self.choice_ctrl.SetStringSelection(new_value)
            self.on_choice(evt)
        else:
            evt.Skip()

    def on_choice(self, evt=None):
        value = self.choice_ctrl.GetStringSelection()
        code = Config.codes[value]
        self.code_panel.SetValue(value, code)
        self.loaded_code = code
        if evt is not None:
            evt.Skip()

    def GetValue(self):
        return self.loaded_code

    @property
    def choices(self):
        choices = list(Config.codes.keys())
        return sorted(choices)

    def update_choices(self):
        choices = self.choices
        value = self.choice_ctrl.GetStringSelection()
        self.choice_ctrl.Clear()
        self.choice_ctrl.SetItems(choices)

        if value in choices:
            self.choice_ctrl.SetStringSelection(value)
        else:
            self.choice_ctrl.SetSelection(0)

        self.choice_ctrl.AutoComplete(choices)

    def on_choice_enter(self, evt):

        if evt.GetKeyCode() == wx.WXK_RETURN:
            value = self.choice_ctrl.GetValue()
            if value in self.choices:
                self.choice_ctrl.SetStringSelection(value)
                self.on_choice(evt)
        else:
            evt.Skip()

    def delete_code(self):
        name = self.choice_ctrl.GetStringSelection()
        del Config.codes[name]
        self.update_choices()
        self.on_choice()

    def load_code(self, code):
        decoder = code.decoder

        for code_name, stored_code in Config.codes.items():
            if stored_code['decoder'] == decoder:
                for param in stored_code['params']:
                    if stored_code[param] != getattr(code, param):
                        break
                else:
                    self.choice_ctrl.SetStringSelection(code_name)
                    self.on_choice()
                    break

                continue
        else:
            frequency = code.frequency
            o_rlc = code.original_code
            n_rlc = code.normalized_code

            try:
                response = requests.get('eventghost.net:43847')
                if response.status_code != 200:
                    raise requests.ConnectionError
            except requests.ConnectionError:
                name = str(code)
            else:
                token = response.content
                response = requests.get('eventghost.net:43847/' + token + '/get_name', params=dict(code))
                if response.status_code != 200:
                    name = str(code)
                else:
                    name = response.content

            params = dict(
                decoder=decoder,
                frequency=frequency,
                original_rlc=o_rlc,
                normalized_rlc=n_rlc,
                params=[]
            )
            for param in code.params:
                params['params'] += param
                params[param] = getattr(code, param)

            self.loaded_code = params
            self.code_panel.SetValue(name, params)
            self.choice_ctrl.SetValue(name)

    def new_code(self, code):
        decoder = code.decoder
        frequency = code.frequency
        o_rlc = code.original_code
        n_rlc = code.normalized_code

        try:
            response = requests.get('eventghost.net:43847')
            if response.status_code != 200:
                raise requests.ConnectionError
        except requests.ConnectionError:
            name = str(code)
        else:
            token = response.content
            response = requests.get('eventghost.net:43847/' + token + '/get_name', params=dict(code))
            if response.status_code != 200:
                name = str(code)
            else:
                name = response.content

        params = dict(
            decoder=decoder,
            frequency=frequency,
            original_rlc=o_rlc,
            normalized_rlc=n_rlc,
            params=[]
        )
        for param in code.params:
            params['params'] += param
            params[param] = getattr(code, param)

        Config.codes[name] = params

        self.update_choices()
        self.choice_ctrl.SetStringSelection(name)
        self.on_choice()


from . import Config  # NOQA
