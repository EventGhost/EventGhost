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
from .utils import h_sizer

import eg


class DeviceDataPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_SUNKEN)

        left_panel = wx.Panel(self, -1, style=wx.BORDER_SUNKEN)
        middle_panel = wx.Panel(self, -1, style=wx.BORDER_SUNKEN)
        right_panel = wx.Panel(self, -1, style=wx.BORDER_SUNKEN)

        device_path_label = wx.StaticText(left_panel, -1, 'Device Path:')
        device_path_ctrl = wx.StaticText(left_panel, -1, '' * 10)
        device_path_sizer = h_sizer(device_path_label, device_path_ctrl)

        hardware_id_label = wx.StaticText(left_panel, -1, 'Hardware Id:')
        hardware_id_ctrl = wx.StaticText(left_panel, -1, '' * 10)
        hardware_id_sizer = h_sizer(hardware_id_label, hardware_id_ctrl)

        vid_label = wx.StaticText(left_panel, -1, 'Vendor Id:')
        vid_ctrl = wx.StaticText(left_panel, -1, '' * 10)
        vid_sizer = h_sizer(vid_label, vid_ctrl)

        pid_label = wx.StaticText(left_panel, -1, 'Product Id:')
        pid_ctrl = wx.StaticText(left_panel, -1, '' * 10)
        pid_sizer = h_sizer(pid_label, pid_ctrl)

        led_flash_label = wx.StaticText(left_panel, -1, 'Can Flash LED:')
        lef_flash_ctrl = wx.StaticText(left_panel, -1, '' * 10)
        led_flash_sizer = h_sizer(led_flash_label, lef_flash_ctrl)

        learn_only_label = wx.StaticText(left_panel, -1, 'Learn Only:')
        learn_only_ctrl = wx.StaticText(left_panel, -1, '' * 10)
        learn_only_sizer = h_sizer(learn_only_label, learn_only_ctrl)

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(device_path_sizer, 0, wx.EXPAND)
        left_sizer.Add(hardware_id_sizer, 0, wx.EXPAND)
        left_sizer.Add(vid_sizer, 0, wx.EXPAND)
        left_sizer.Add(pid_sizer, 0, wx.EXPAND)
        left_sizer.Add(led_flash_sizer, 0, wx.EXPAND)
        left_sizer.Add(learn_only_sizer, 0, wx.EXPAND)

        left_panel.SetSizer(left_sizer)

        con_tx_label = wx.StaticText(middle_panel, -1, 'TX Port Count:')
        con_tx_ctrl = wx.StaticText(middle_panel, -1, '' * 10)
        con_tx_sizer = h_sizer(con_tx_label, con_tx_ctrl)

        tx_port_label = wx.StaticText(middle_panel, -1, 'TX Ports:')
        tx_port_ctrl = wx.StaticText(middle_panel, -1, '' * 10)
        tx_port_sizer = h_sizer(tx_port_label, tx_port_ctrl)

        num_rx_port_label = wx.StaticText(middle_panel, -1, 'RX Port Count:')
        num_rx_port_ctrl = wx.StaticText(middle_panel, -1, '' * 10)
        num_rx_port_sizer = h_sizer(num_rx_port_label, num_rx_port_ctrl)

        rx_port_label = wx.StaticText(middle_panel, -1, 'RX Ports:')
        rx_port_ctrl = wx.StaticText(middle_panel, -1, '' * 10)
        rx_port_sizer = h_sizer(rx_port_label, rx_port_ctrl)

        emulator_version_label = wx.StaticText(middle_panel, -1, 'Emulator Version:')
        emulator_version_ctrl = wx.StaticText(middle_panel, -1, '' * 10)
        emulator_version_sizer = h_sizer(emulator_version_label, emulator_version_ctrl)

        narrow_bpf_label = wx.StaticText(middle_panel, -1, 'Narrow Band Pass Filter:')
        narrow_bpf_ctrl = wx.StaticText(middle_panel, -1, '' * 10)
        narrow_bpf_sizer = h_sizer(narrow_bpf_label, narrow_bpf_ctrl)

        middle_sizer = wx.BoxSizer(wx.VERTICAL)
        middle_sizer.Add(con_tx_sizer, 0, wx.EXPAND)
        middle_sizer.Add(tx_port_sizer, 0, wx.EXPAND)
        middle_sizer.Add(num_rx_port_sizer, 0, wx.EXPAND)
        middle_sizer.Add(rx_port_sizer, 0, wx.EXPAND)
        middle_sizer.Add(emulator_version_sizer, 0, wx.EXPAND)
        middle_sizer.Add(narrow_bpf_sizer, 0, wx.EXPAND)

        middle_panel.SetSizer(middle_sizer)

        wake_label = wx.StaticText(right_panel, -1, 'Has Wake:')
        wake_ctrl = wx.StaticText(right_panel, -1, '' * 10)
        wake_sizer = h_sizer(wake_label, wake_ctrl)

        multiple_wake_label = wx.StaticText(right_panel, -1, 'Multiple Wake:')
        multiple_wake_ctrl = wx.StaticText(right_panel, -1, '' * 10)
        multiple_wake_sizer = h_sizer(multiple_wake_label, multiple_wake_ctrl)

        program_wake_label = wx.StaticText(right_panel, -1, 'Programmable Wake:')
        program_wake_ctrl = wx.StaticText(right_panel, -1, '' * 10)
        program_wake_sizer = h_sizer(program_wake_label, program_wake_ctrl)

        vol_wake_label = wx.StaticText(right_panel, -1, 'Volitile Wake:')
        vol_wake_ctrl = wx.StaticText(right_panel, -1, '' * 10)
        vol_wake_sizer = h_sizer(vol_wake_label, vol_wake_ctrl)

        software_decode_label = wx.StaticText(right_panel, -1, 'Has Software Decode:')
        software_decode_ctrl = wx.StaticText(right_panel, -1, '' * 10)
        software_decode_sizer = h_sizer(software_decode_label, software_decode_ctrl)

        attached_tuner_label = wx.StaticText(right_panel, -1, 'Has Attached Tuner::')
        attached_tuner_ctrl = wx.StaticText(right_panel, -1, '' * 10)
        attached_tuner_sizer = h_sizer(attached_tuner_label, attached_tuner_ctrl)

        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer.Add(wake_sizer, 0, wx.EXPAND)
        right_sizer.Add(multiple_wake_sizer, 0, wx.EXPAND)
        right_sizer.Add(program_wake_sizer, 0, wx.EXPAND)
        right_sizer.Add(vol_wake_sizer, 0, wx.EXPAND)
        right_sizer.Add(software_decode_sizer, 0, wx.EXPAND)
        right_sizer.Add(attached_tuner_sizer, 0, wx.EXPAND)

        right_panel.SetSizer(right_sizer)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.Add(left_panel, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(middle_panel, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(right_panel, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)

        eg.EqualizeWidths((
            device_path_label,
            hardware_id_label,
            vid_label,
            pid_label,
            led_flash_label,
            con_tx_label,
            tx_port_label,
            num_rx_port_label,
            rx_port_label,
            emulator_version_label,
            narrow_bpf_label,
            wake_label,
            multiple_wake_label,
            program_wake_label,
            vol_wake_label,
            software_decode_label,
            attached_tuner_label
        ))

        def set_value(device):
            device_path_ctrl.SetLabel(str(device.device_path))
            hardware_id_ctrl.SetLabel(str(device.hardware_id))
            vid_ctrl.SetLabel(str(device.vid))
            pid_ctrl.SetLabel(str(device.pid))
            lef_flash_ctrl.SetLabel(str(device.can_flash_led))
            learn_only_ctrl.SetLabel(str(device.is_learn_only))
            con_tx_ctrl.SetLabel(str(device.num_connected_tx_ports))
            tx_port_ctrl.SetLabel(str(device.tx_ports))
            num_rx_port_ctrl.SetLabel(str(device.num_rx_ports))
            rx_port_ctrl.SetLabel(str(device.rx_ports))
            emulator_version_ctrl.SetLabel(str(device.emulator_version))
            narrow_bpf_ctrl.SetLabel(str(device.has_narrow_bpf))
            wake_ctrl.SetLabel(str(device.supports_wake))
            multiple_wake_ctrl.SetLabel(str(device.supports_multiple_wake))
            program_wake_ctrl.SetLabel(str(device.supports_programmable_wake))
            vol_wake_ctrl.SetLabel(str(device.has_volitile_wake))
            software_decode_ctrl.SetLabel(str(device.has_software_decode_input))
            attached_tuner_ctrl.SetLabel(str(device.has_attached_tuner))

        self.SetValue = set_value


class DevicePanel(wx.Panel):

    def __init__(self, parent, plugin):
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        self.plugin = plugin

        choices = [device.manufacturer + ' : ' + device.model for device in plugin.devices]
        device_label = wx.StaticText(self, -1, 'Device:')
        device_ctrl = self.device_ctrl = wx.Choice(self, -1, choices=choices)
        device_sizer = h_sizer(device_label, device_ctrl)
        device_panel = self.device_panel = DeviceDataPanel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(device_sizer, 0, wx.EXPAND)
        sizer.Add(device_panel, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

        device_ctrl.SetSelection(1)
        self.on_choice()

        device_ctrl.Bind(wx.EVT_CHOICE, self.on_choice)

    def on_choice(self, _=None):
        device = self.GetValue()
        if device is not None:
            self.device_panel.SetValue(device)

    def GetStringSelection(self):
        manufacturer, model = self.device_ctrl.GetStringSelection().split(' : ')
        return manufacturer, model

    def SetStringSelection(self, manufacturer, model):
        value = manufacturer + ' : ' + model
        if value in self.device_ctrl.GetItems():
            self.device_ctrl.SetStringSelection(value)

        else:
            self.device_ctrl.SetSelection(0)

        self.on_choice()

    def GetValue(self):
        try:
            manufacturer, model = self.device_ctrl.GetStringSelection().split(' : ')
        except ValueError:
            return

        for device in self.plugin.devices:
            if device.manufacturer == manufacturer and device.model == model:
                return device
