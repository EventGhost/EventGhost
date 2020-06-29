# -*- coding: utf-8 -*-
#
# plugins/MceRemote_Vista/__init__.py
#
# This file is a plugin for EventGhost.
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

import eg

eg.RegisterPlugin(
    name = "Microsoft MCE Remote (Vista+)",
    author = 'Kevin Schlosser',
    version = "2.0.0",
    kind = "remote",
    guid = "{A7DB04BB-9F0A-486A-BCA1-CA87B9620D54}",
    description = 'Plugin for the Microsoft MCE remote.',
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=6044",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACfklEQVR42q2TS2gTQRyH"
        "f5N9NNlts20abYyxVirWShGLUh8XoSpUUBEVUU+5CXoQr+LNm14UtRCpRcGLHnqoiooN"
        "VO1FRWrTaKgmqdJqGuwj3TTZ947bbLV37cAMM8zMx39+fEPwn42sGKD7zk3aeWg3TEut"
        "rC3bdrpZmZuWBlVXYFgGKKEQOAHDg+M4f/YCqQBuxa7T7XtaEWloRkkrwDQt6KZzwdZR"
        "VGSU1DmoRgm6pUBWC1DUMoK1q2BmQ24F77/G6ZfvI2isb0FRnYVYZtAe8aCUkzGSyuCj"
        "tADFLsEwNOi0CM1QYDnVrNcOuICHQzfoWCaJoD8MWZnGfoPB1k0BpN/k8DKbxvAGE1JA"
        "QHidF9lMHvnChPMuii3sCRdwre8czUykwDAMuLKKU1oV2CCL7Itx9LMycmtqsa2jAY1N"
        "EgaepWBxc2A5Dq30mAu40neGpr59AKUUliHB5z8KUwxi5vUDWCQNW2TRvrOpknkykYRQ"
        "7wXr4bFRO+ICrj6J0tHcq0ris3MHwbdcgiaX8XMohl2B+xAF4jyhBsqCgqQTsOhnwXNe"
        "NM4fdgG3By7S4amnoBaHT4m9gP84ivkUquf7cTL8Fh1tPjSv9eHxqIw48YL3MfBWiQj/"
        "6nIBzxN3afxHDJYTzLvBOvBMGfMFPyLcZ3QFCtixWcCiET1pFVpIAiE2aqrrEM4vAZIT"
        "Q/RR6jKo1zmgOrLYtAIzphSEZ2cQ8gGTio0E5SGFa6BrBiJSKxqm97mAWE83VUJjSEzG"
        "nXT5v34ugkqKDkPW4OEZCCIH4iEg1IPOttPQ0quXVe6910vh6EuX/F5U1hmWZV/a+LP0"
        "EBbRaJSs3Gf61/YbN1kg0OJlna4AAAAASUVORK5CYII="
    ),
)

import pyWinMCERemote  # NOQA
import decoders  # NOQA


class Config(eg.PersistentData):
    codes = {}
    decoder_order = decoders.IrDecoder.decoder_order
    decoder_tolerances = zip(decoder_order, [10] * len(decoder_order))
    size = (-1, -1)


import wx  # NOQA
import requests  # NOQA
import threading  # NOQA
from utils import h_sizer, v_sizer  # NOQA
import device_panel  # NOQA
import learn_dialog  # NOQA
import codes_panel  # NOQA
from decoders import pronto  # NOQA


class ActionBase(eg.ActionBase):

    def _get_device(self, manufacturer, model):
        if manufacturer:
            for device in self.plugin.devices:
                if device.manufacturer == manufacturer and device.model == model:
                    return device

            eg.PrintWarningNotice(
                'Microsoft MCE Remote (Vista+): Unable to '
                'locate ir device {0} {1} is it plugged in?'.format(
                    manufacturer,
                    model
                )
            )
        elif len(self.plugin.ir_devices):
            return self.plugin.devices[0]

        else:
            eg.PrintWarningNotice(
                'Microsoft MCE Remote (Vista+): '
                'Unable to locate ir device'
            )

    def Configure(self, manufacturer='', model=''):
        panel = eg.ConfigPanel()
        ctrl = device_panel.DevicePanel(panel, self.plugin)
        ctrl.SetStringSelection(manufacturer, model)

        panel.sizer.Add(ctrl)

        while panel.Affirmed():
            panel.SetResult(
                *ctrl.GetStringSelection()
            )


class TransmitIR(ActionBase):
    name = "Transmit IR"

    def __call__(self, manufacturer, model, code):
        device = self._get_device(manufacturer, model)

        if device is None:
            return False

        try:
            frequency, code = eg.ParseString(code)
        except:
            frequency = None
            try:
                code = eg.ParseString(code)
            except:
                pass

        if frequency is None:
            frequency, code = pronto.pronto_to_rlc(code)

        device.transmit(code, frequency)

    def Configure(self, manufacturer='', model='', code=''):
        panel = eg.ConfigPanel()
        device_ctrl = device_panel.DevicePanel(panel, self.plugin)
        device_ctrl.SetStringSelection(manufacturer, model)

        edit_label = panel.StaticText("Pronto/RLC Code")
        edit_ctrl = panel.TextCtrl(code, style=wx.TE_MULTILINE)
        edit_tooltip = (
            'You can use either a pronto code or you can enter\n'
            'the frequency and rlc(Run Length Code) formatted in\n'
            'the following manner.\n'
            '{frequency, [rlc]}\n\n'
            'pressing Enter populates the rest of the protocol information.'
        )
        edit_ctrl.SetToolTipString(edit_tooltip)

        def on_enter(evt):
            key_code = evt.GetKeycode()
            if key_code == wx.WXK_RETURN:
                value = edit_ctrl.GetValue()
                try:
                    freq, rlc = eg.ParseString(value)
                except:
                    try:
                        value = eg.ParseString(value)
                    except:
                        pass

                    freq, rlc = pronto.pronto_to_rlc(value)

                c = decoders.IrDecoder.decode(rlc. len(rlc), frequency)
                if c is not None:
                    code_ctrl.load_code(c)
            else:
                evt.Skip()

        edit_ctrl.Bind(wx.EVT_CHAR_HOOK, on_enter)

        edit_sizer = v_sizer(edit_label, edit_ctrl)

        font = edit_ctrl.GetFont()
        font.SetFaceName("Courier New")
        edit_ctrl.SetFont(font)
        edit_ctrl.SetMinSize((-1, 100))

        code_ctrl = codes_panel.CodesPanel(panel)

        learn_button = panel.Button("Learn an IR Code...")
        panel.dialog.buttonRow.Add(learn_button)

        def on_learn_button(evt):
            dialog = learn_dialog.LearnDialog(self.plugin)
            res = dialog.ShowModal()
            dialog.Destroy()
            if res == wx.ID_OK:
                c = dialog.GetValue()
                if code is not None:
                    code_ctrl.load_code(c)

            evt.Skip()

        learn_button.Bind(wx.EVT_BUTTON, on_learn_button)

        panel.sizer.Add(device_ctrl, 0, wx.EXPAND)
        panel.sizer.Add(edit_sizer, 0, wx.EXPAND)
        panel.sizer.Add(code_ctrl, 0, wx.EXPAND)

        while panel.Affirmed():
            man, mod = device_ctrl.GetStringSelection()
            params = code_ctrl.GetValue()
            if params is None:
                val = edit_ctrl.GetValue()
            else:
                val = '{{{frequency}, {rlc}}}'.format(
                    frequency=params['frequency'],
                    rlc=params['normalized_code']
                )

            panel.SetResult(man, mod, val)


class GetDeviceInfo(ActionBase):
    name = "Get Mce IR device capability"

    def __call__(self, manufacturer, model):

        device = self._get_device(manufacturer, model)
        if device is None:
            return {}

        res = dict(
            manufacturer=device.manufacturer,
            model=device.model,
            num_connected_tx_ports=device.num_connected_tx_ports,
            tx_ports=device.tx_ports,
            num_rx_ports=device.num_rx_ports,
            rx_ports=device.rx_ports,
            can_flash_led=device.can_flash_led,
            supports_wake=device.supports_wake,
            supports_multiple_wake=device.supports_multiple_wake,
            supports_programmable_wake=device.supports_programmable_wake,
            has_volitile_wake=device.has_volitile_wake,
            is_learn_only=device.is_learn_only,
            has_narrow_bpf=device.has_narrow_bpf,
            has_software_decode_input=device.has_software_decode_input,
            has_hardware_decode_input=device.has_hardware_decode_input,
            has_attached_tuner=device.has_attached_tuner,
            emulator_version=device.emulator_version
        )
        return res


class TestIR(ActionBase):
    name = "Test IR Transmit capability"

    def __call__(self, manufacturer, model):

        device = self._get_device(manufacturer, model)

        if device is None:
            return False

        device.test_tx_ports()
        return True


from wx.lib import scrolledpanel


class MCE_Vista(eg.PluginBase):

    def __init__(self):
        self.AddAction(GetDeviceInfo)
        self.AddAction(TransmitIR)
        self.AddAction(TestIR)

        t = threading.Thread(target=pyWinMCERemote.load_device_data)
        t.daemon = True
        t.start()

    def Configure(self):
        panel = eg.ConfigPanel()

        dialog = panel.dialog
        button_row = panel.dialog.buttonRow
        notebook = dialog.notebook

        code_delete_button = wx.Button(dialog, -1, 'Delete Code')
        code_learn_button = wx.Button(dialog, -1, 'Learn Code')
        code_add_button = wx.Button(dialog, -1, 'Add Code')

        button_row.Add(code_learn_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 6)
        button_row.Add(code_add_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 6)
        button_row.Add(code_delete_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 6)

        code_delete_button.Hide()
        code_learn_button.Hide()
        code_add_button.Hide()

        def on_delete_button(evt):
            codes_page.delete_code()
            evt.Skip()

        code_delete_button.Bind(wx.EVT_BUTTON, on_delete_button)

        def on_add_button(evt):
            evt.Skip()

        code_add_button.Bind(wx.EVT_BUTTON, on_add_button)

        def on_learn_button(_):
            ld = learn_dialog.LearnDialog(self)
            result = ld.ShowModal()
            ld.Destroy()

            if result == wx.ID_OK:
                codes_page.new_code(ld.code)

        code_learn_button.Bind(wx.EVT_BUTTON, on_learn_button)

        codes_page = codes_panel.CodesPanel(notebook)
        notebook.AddPage(codes_page, "Codes")

        def on_page_changed(evt):
            index = evt.GetSelection()

            code_delete_button.Show(index == 1)
            code_learn_button.Show(index == 1)
            code_add_button.Show(index == 1)

        notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, on_page_changed)
        wx.CallAfter(panel.EnableButtons, True)
        tolerance_ctrls = []
        boxed_group = eg.BoxedGroup(panel, 'Decoder Tolerances')
        tolerance_panel = scrolledpanel.ScrolledPanel(panel, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)

        for decoder, tolerance in Config.decoder_tolerances:
            ctrl = ToleranceCtrl(tolerance_panel, decoder)
            ctrl.SetValue(tolerance)
            sizer.Add(ctrl, 0, wx.EXPAND)
            tolerance_ctrls += [ctrl]

        eg.EqualizeWidths(tuple(ctrl.label for ctrl in tolerance_ctrls))
        tolerance_panel.SetupScrolling()
        tolerance_panel.SetSizer(sizer)
        boxed_group.Add(tolerance_panel, 1, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(boxed_group, 1, wx.EXPAND)

        wx.CallAfter(panel.dialog.SetSize, Config.size)

        while panel.Affirmed():
            for ctrl in tolerance_ctrls:
                tolerance = ctrl.GetValue()
                decoder = ctrl.GetLabel()
                for i, item in enumerate(Config.decoder_tolerances):
                    if item[0] == decoder:
                        Config.decoder_tolerances[i] = (decoder, tolerance)
                        break

            panel.SetResult()

        size = panel.dialog.GetSize()
        Config.size = (size[0], size[1])

    @eg.LogIt
    def __start__(self):
        decoders.IrDecoder.decoder_order = Config.decoder_order

        for decoder, tolerance in Config.decoder_tolerances:
            decoders.IrDecoder.set_tolerance(decoder, tolerance)

        self.devices = pyWinMCERemote.get_ir_devices()

        for device in self.devices:
            device.bind(self._callback)
            device.start_receive()

    def _callback(self, device, frequency, rlc):
        code = decoders.IrDecoder.decode(rlc, len(rlc), frequency)
        if code is not None:
            self.info.eventPrefix = device.manufacturer + '.' + device.model

            for code_name, stored_code in Config.codes.items():
                if stored_code['decoder'] == code.decoder:
                    for param in stored_code['params']:
                        if getattr(code, param) != stored_code[param]:
                            break
                    else:
                        self.TriggerEvent(code_name, code)
                        break
            else:
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

                self.TriggerEvent(name, code)

    def __stop__(self):
        for device in self.devices:
            device.unbind(self._callback)
            device.stop_receive()

        Config.decoder_order = decoders.IrDecoder.decoder_order


class ToleranceCtrl(wx.BoxSizer):

    def __init__(self, parent, decoder):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)

        self.decoder = decoder
        self.ctrl = eg.SpinIntCtrl(parent, -1, value=10, min=1)
        self.label = wx.StaticText(parent, -1, decoder + ':')

        self.Add(self.label, 0, wx.EXPAND | wx.ALL, 5)
        self.Add(self.ctrl, 0, wx.EXPAND | wx.ALL, 5)

    def GetLabel(self):
        return self.decoder

    def SetValue(self, value):
        self.ctrl.SetValue(value)

    def GetValue(self):
        return self.ctrl.GetValue()
