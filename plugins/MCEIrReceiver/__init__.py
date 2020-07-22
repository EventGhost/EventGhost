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
    name="Windows Media Center IR Receiver",
    author='Kevin Schlosser',
    version="0.1.0",
    kind="remote",
    guid="{83900293-1A63-4789-996E-4C7B53F30072}",
    description=(
        'Plugin for the Windows Media Center Edition IR receivers.\n\n'
        'This plugin is a replacement for the existing MCE Remote (Vista+) plugin. '
        'If you are currently using the "Vista+" plugin you will need to stop and'
        'disable the service or uninstall the service via the plugins config.\n\n'
        'Differences between the 2 plugins.\n\n'
        'No service to be installed.\n'
        'Supports multiple receivers/transmitters.\n'
        'NO button lag.\n'
        'Code written in 100% Python.\n'
    ),
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=6044",
    icon=(
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


import wx  # NOQA
import os  # NOQA
import threading  # NOQA
from utils import h_sizer, v_sizer  # NOQA
import reg_keys  # NOQA
import pyIRDecoder  # NOQA
from pyIRDecoder import ir_code  # NOQA
from eg.WinApi import ir_class_ioctl  # NOQA
from eg.WinApi.ir_class_ioctl import ioctl  # NOQA


class Text(eg.TranslatableStrings):
    label = 'MCE Transceiver:'
    server_label = 'Use Friendly Names:'
    frame_0_label = 'Frame 0'
    frame_1_label = 'Frame 1'
    frame_2_label = 'Frame 2'
    frequency_label = 'Frequency:'
    code_label = 'Code'
    pronto_tab = 'Pronto Hex'
    rlc_tab = 'Run-Length Code'
    code_tab = 'Saved Code'


# noinspection PyPep8Naming
class RLCPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)

        frame_0_label = wx.StaticText(self, -1, Text.frame_0_label)
        self.frame0 = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE)
        frame_0_sizer = v_sizer(frame_0_label, self.frame0)

        frame_1_label = wx.StaticText(self, -1, Text.frame_1_label)
        self.frame1 = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE)
        frame_1_sizer = v_sizer(frame_1_label, self.frame1)

        frame_2_label = wx.StaticText(self, -1, Text.frame_2_label)
        self.frame2 = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE)
        frame_2_sizer = v_sizer(frame_2_label, self.frame2)

        frequency_label = wx.StaticText(self, -1, Text.frequency_label)
        self.frequency_ctrl = wx.TextCtrl(self, -1, '00000')
        frequency_sizer = h_sizer(frequency_label, self.frequency_ctrl)
        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(frequency_sizer, 0, wx.ALL | 5)
        sizer.Add(frame_0_sizer, 0, wx.ALL | 5)
        sizer.Add(frame_1_sizer, 0, wx.ALL | 5)
        sizer.Add(frame_2_sizer, 0, wx.ALL | 5)

        self.SetSizer(sizer)

    def GetValue(self):
        frame0 = self.frame0.GetValue().strip()
        frame1 = self.frame1.GetValue().strip()
        frame2 = self.frame2.GetValue().strip()

        if not frame0 and not frame1 and not frame2:
            return None, None

        if '{' in frame0 or '{' in frame1 or '{' in frame2:
            if '{' not in frame0:
                frame0 = str(list(int(item.strip()) for item in frame0.split(',')))

            if '{' not in frame1:
                frame1 = str(list(int(item.strip()) for item in frame1.split(',')))

            if '{' not in frame2:
                frame2 = str(list(int(item.strip()) for item in frame2.split(',')))

        else:
            frame0 = list(int(item.strip()) for item in frame0.split(','))
            frame1 = list(int(item.strip()) for item in frame1.split(','))
            frame2 = list(int(item.strip()) for item in frame2.split(','))

        frequency = self.frequency_ctrl.GetValue()

        if '{' not in frequency:
            frequency = int(frequency)

        return (
            [
                frame0,
                frame1,
                frame2
            ],
            frequency,
        )

    def SetValue(self, code, frequency):
        frame0, frame1, frame2 = code

        def _get_value(val):
            if val > 0:
                return '+' + str(val)
            return str(val)

        if isinstance(frame0, list):
            frame0 = ', '.join(_get_value(item) for item in frame0)
        if isinstance(frame1, list):
            frame1 = ', '.join(_get_value(item) for item in frame1)
        if isinstance(frame2, list):
            frame2 = ', '.join(_get_value(item) for item in frame2)

        self.frame0.SetValue(frame0)
        self.frame0.SetValue(frame1)
        self.frame0.SetValue(frame2)

        self.frequency_ctrl.SetValue(str(frequency))


# noinspection PyPep8Naming
class ProntoPanel(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)

        label = wx.StaticText(self, -1, Text.pronto_label)
        self.ctrl = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE)

        sizer = v_sizer(label, self.ctrl)
        self.SetSizer(sizer)

    def GetValue(self):
        value = self.ctrl.GetValue().strip()
        if value:
            return value

    def SetValue(self, value):
        self.ctrl.SetValue(value)


class CodePanel(eg.IrCodeCtrl):

    def __init__(self, *args, **kwargs):
        eg.IrCodeCtrl.__init__(self, *args, **kwargs)

        ctrl = self.GetChildren()[0]
        label = wx.StaticText(self, -1, Text.code_label + ':')

        sizer = h_sizer(label, ctrl)
        self.SetSizer(sizer)


# noinspection PyPep8Naming
class TransmitIR(eg.ActionBase):
    name = "Transmit IR"

    # noinspection PyPep8
    def __call__(self, code, frequency=0):

        if isinstance(code, ir_code.IRCode):
            frequency = code.frequency
            code = code.normalized_mce_rlc

        elif isinstance(code, list):
            for i, rlc in enumerate(code):
                if not isinstance(rlc, list):
                    # noinspection PyBroadException
                    try:
                        rlc = eg.ParseString(rlc)
                    except:
                        eg.PrintError('MCE_Vista+: Unable to send code. Unknown data type')
                        return False

                rlc = pyIRDecoder.rlc_to_mce(rlc)
                code[i] = rlc

            if not isinstance(frequency, int):
                # noinspection PyBroadException
                try:
                    frequency = eg.ParseString(frequency)
                except:
                    eg.PrintError('MCE_Vista+: Unable to send code. Unknown data type')
                    return False

        elif frequency == -1:
            # noinspection PyBroadException
            try:
                code = eg.ParseString(code)
            except:
                pass

            # noinspection PyBroadException
            try:
                frequency, code = pyIRDecoder.pronto_to_mce(code)
            except:
                eg.PrintError('MCE_Vista+: Unable to send code. Unknown data type')
                return False

        elif frequency == -2 and isinstance(code, basestring) and '.' in code:
            codes = [c for decoder in self.plugin.ir_decoder for c in decoder]
            for c in codes:
                if c.name == code:
                    code = c
                    break
            else:
                eg.PrintError('MCE_Vista+: Unable to send code "{0}"'.format(code))
                return False

            frequency = code.frequency
            code = code.normalized_mce_rlc

        else:
            eg.PrintError('MCE_Vista+: Unable to send code. Unknown data type')
            return False

        if isinstance(code[0], list):
            code = [item for sublist in code for item in sublist]

        self.plugin.device.transmit(code, frequency)

    def Configure(self, code=None, frequency=None):
        panel = eg.ConfigPanel()

        dialog = panel.dialog

        rlc_ctrl = RLCPanel(self)
        pronto_ctrl = ProntoPanel(self)
        code_ctrl = CodePanel(self, -1, self.plugin.ir_decoder)

        panel.sizer.Add(code_ctrl)

        dialog.notebook.SetPageText(0, Text.code_tab)
        dialog.notebook.AddPage(pronto_ctrl, Text.pronto_tab)
        dialog.notebook.AddPage(rlc_ctrl, Text.rlc_tab)

        if code is None:
            dialog.notebook.SetSelection(0)
            code_ctrl.SetSelection(0)
        elif isinstance(code, basestring):
            if '.' in code:
                code_ctrl.SetStringSelection(code)
                dialog.notebook.SetSelection(0)
            else:
                pronto_ctrl.SetValue(code)
                dialog.notebook.SetSelection(1)
        else:
            rlc_ctrl.SetValue(code, frequency)
            dialog.notebook.SetSelection(2)

        while panel.Affirmed():
            pronto_code = pronto_ctrl.GetValue()
            rlc_code, rlc_frequency = rlc_ctrl.GetValue()
            saved_code = code_ctrl.GetStringSelection()

            if pronto_code is not None:
                res = (pronto_code, -1)
            elif rlc_code is not None:
                res = (rlc_code, rlc_frequency)
            else:
                res = (saved_code, -2)

            panel.SetResult(*res)


class GetDeviceInfo(eg.ActionBase):
    name = "Get Mce IR device capability"

    def __call__(self):
        device = self.plugin.device

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


class TestIR(eg.ActionBase):
    name = "Test IR Transmit capability"

    def __call__(self):
        self.plugin.device.test_tx_ports()
        return True


class GetLastCode(eg.ActionBase):

    name = 'Get Last Code'

    def __call__(self):
        return self.plugin.ir_decoder.last_code


# noinspection PyPep8Naming
class MCEIrReceiver(eg.PluginBase):

    text = Text

    def __init__(self):
        self.AddAction(GetDeviceInfo)
        self.AddAction(TransmitIR)
        self.AddAction(TestIR)
        self.device = None

        if not ioctl.DATA_LOADED:
            t = threading.Thread(target=ir_class_ioctl.load_device_data)
            t.daemon = True
            t.start()

    def Configure(self, device_name='', use_server=True):
        panel = eg.ConfigPanel()

        devices = ir_class_ioctl.get_ir_devices()
        choices = list(device.name for device in devices if not device.is_running)

        label = panel.StaticText(self.text.label)
        ctrl = wx.Choice(panel, -1, choices=sorted(choices))

        server_ctrl = wx.CheckBox(panel, -1, self.text.server_label)
        server_ctrl.SetValue(use_server)

        panel.sizer.Add(h_sizer(label, ctrl))
        panel.sizer.Add(server_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        if device_name in devices:
            ctrl.SetStringSelection(device_name)
        else:
            ctrl.SetSelection(0)

        while panel.Affirmed():
            panel.SetResult(ctrl.GetStringSelection(), server_ctrl.GetValue())

    @eg.LogIt
    def __start__(self, device_name, use_server):
        config_filename = self.info.name + '(' + device_name + ').xml'
        config_path = os.path.join(eg.configDir, 'ir_decoders', config_filename)

        devices = ir_class_ioctl.get_ir_devices()
        for device in devices:
            if device.name == device_name:
                if device.is_running:
                    raise self.Exception(
                        'MCE receiver "{0}" is already in use'.format(device_name)
                    )
                self.device = device
                break
        else:
            raise self.Exception(
                'unable to locate MCE receiver "{0}"'.format(device_name)
            )

        self.info.eventPrefix = device_name
        self.ir_decoder = eg.IrDecoder(self, config_path=config_path)

        if use_server:
            self.ir_decoder.config.database_url = 'http://eventghost.net:43847'
        else:
            self.ir_decoder.config.database_url = None

        if self.ir_decoder.config.run_setup:
            reg_keys.remove_keys()
            self.ir_decoder.config.run_setup = False

        self.device.bind(self._callback)
        self.device.start_receive()

    def _callback(self, _, frequency, rlc):
        self.ir_decoder.DecodeStream(rlc, frequency=frequency)

    def __stop__(self):
        self.device.unbind(self._callback)
        self.device.stop_receive()
        self.ir_decoder.Close()
