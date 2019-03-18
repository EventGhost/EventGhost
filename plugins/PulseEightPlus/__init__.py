# -*- coding: utf-8 -*-
# super_class_updated
# This file is part of the libCEC(R) library.
#
# libCEC(R) is Copyright (C) 2011-2015 Pulse-Eight Limited.
# All rights reserved.
# libCEC(R) is an original work, containing original code.
#
# libCEC(R) is a trademark of Pulse-Eight Limited.
#
# This program is dual-licensed; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301  USA
#
#
# Alternatively, you can license this library under a commercial license,
# please contact Pulse-Eight Licensing for more information.
#
# For more information contact:
# Pulse-Eight Licensing       <license@pulse-eight.com>
#     http://www.pulse-eight.com/
#     http://www.pulse-eight.net/
#
#
# The code contained within this file also falls under the GNU license of
# EventGhost
#
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

import eg


eg.RegisterPlugin(
    name='Pulse-Eight CEC+',
    author='K',
    version='0.4.7b',
    kind='remote',
    guid='{E5A6943F-A70E-434C-8B29-2F002AB6E56B}',
    url='http://libcec.pulse-eight.com/',
    description=(
        '<rst>'
        'Integration with libCEC, which adds support for Pulse-Eight\'s ' 
        '`CEC adapters <http://www.pulse-eight.com/>`_.\n\n'
        '|\n\n'
        '.. image:: cec.png\n\n'
        '**Notice:** '
        'Make sure you select the correct HDMI port number on the device that '
        'the CEC adapter is connected to, '
        'or remote control input won\'t work.\n'
    ),
    createMacrosOnAdd=True,
    canMultiLoad=False,
    hardwareId="USB\\VID_2548&PID_1002",
)

import threading # NOQA
import wx # NOQA
import time # NOQA
import os # NOQA
from __cec_core import (
    get_adapter_ports,
    PyCECAdapter,
    PyCECConfiguration,
    KEY_CODES,
    TUNER_STATUS_TO_STRING,
    PLAYER_STATUS_TO_STRING
)# NOQA


from .text import Text

from gui_controls import (
    AdapterConfig,
    AdapterCtrl,
    DeviceCtrl,
    AdapterListCtrl
)# NOQA


class AdapterCallbacks(object):
    def __init__(
        self,
        plugin,
        adapter,
        log_info,
        log_notice,
        log_warning,
        log_error,
        log_debug,
        log_file
    ):
        self.plugin = plugin
        self.adapter = adapter

        self.log_info = log_info
        self.log_notice = log_notice
        self.log_warning = log_warning
        self.log_error = log_error
        self.log_debug = log_debug
        self.log_file = log_file

        adapter.trigger_event = self.trigger_event
        adapter.print_error = self.print_error
        adapter.print_warning = self.print_warning
        adapter.print_notice = self.print_notice
        adapter.print_info = self.print_info
        adapter.print_debug = self.print_debug
        self.log_file_path = os.path.join(
            eg.configDir,
            'CEC',
            self.adapter.name
        )

        if log_file:
            if not os.path.exists(self.log_file_path):
                os.makedirs(self.log_file_path)

    def trigger_event(self, event, payload=None):
        event = '{0}.{1}'.format(
            self.adapter.lib_cec_device.osd_name,
            event
        )

        self.plugin.TriggerEvent(event, payload)

        if self.log_file:
            event_file = os.path.join(self.log_file_path, 'event.txt')
            msg = 'EVENT: {0} PAYLOAD: {1}'.format(event, payload)

            msg = time.strftime('%c - ' + msg, time.localtime(time.time()))
            with open(event_file, 'a') as f:
                f.write(msg + '\n')

    def print_error(self, msg):
        if self.log_error:
            msg = 'CEC ERROR: {0}: {1}'.format(
                self.adapter.lib_cec_device.osd_name,
                msg
            )
            eg.PrintError(msg)

            if self.log_file:
                error_file = os.path.join(self.log_file_path, 'error.txt')
                msg = time.strftime('%c - ' + msg, time.localtime(time.time()))
                with open(error_file, 'a') as f:
                    f.write(msg + '\n')

    def print_warning(self, msg):
        if self.log_warning:
            msg = 'CEC WARNING: {0}: {1}'.format(
                self.adapter.lib_cec_device.osd_name,
                msg
            )
            eg.PrintWarningNotice(msg)
            if self.log_file:
                warning_file = os.path.join(self.log_file_path, 'warning.txt')
                msg = time.strftime('%c - ' + msg, time.localtime(time.time()))
                with open(warning_file, 'a') as f:
                    f.write(msg + '\n')

    def print_notice(self, msg):
        if self.log_notice:
            msg = 'CEC NOTICE: {0}: {1}'.format(
                self.adapter.lib_cec_device.osd_name,
                msg
            )
            eg.PrintNotice(msg)

            if self.log_file:
                notice_file = os.path.join(self.log_file_path, 'notice.txt')
                msg = time.strftime('%c - ' + msg, time.localtime(time.time()))
                with open(notice_file, 'a') as f:
                    f.write(msg + '\n')

    def print_info(self, msg):
        if self.log_info:
            msg = 'CEC INFO: {0}: {1}'.format(
                self.adapter.lib_cec_device.osd_name,
                msg
            )
            eg.Print(msg)

            if self.log_file:
                info_file = os.path.join(self.log_file_path, 'info.txt')
                msg = time.strftime('%c - ' + msg, time.localtime(time.time()))
                with open(info_file, 'a') as f:
                    f.write(msg + '\n')

    def print_debug(self, msg):
        if self.log_debug:
            msg = 'CEC DEBUG: {0}: {1}'.format(
                self.adapter.lib_cec_device.osd_name,
                msg
            )
            eg.PrintDebugNotice(msg)

            if self.log_file:
                debug_file = os.path.join(self.log_file_path, 'debug.txt')
                msg = time.strftime('%c - ' + msg, time.localtime(time.time()))
                with open(debug_file, 'a') as f:
                    f.write(msg + '\n')


class PulseEight(eg.PluginBase):
    text = Text

    def __init__(self):
        super(PulseEight, self).__init__()
        super(PulseEight, self).__init__()
        self.adapters = []
        self.__startup_threads = []
        self.__startup_event = threading.Event()
        self.__adapter_ports = []
        self.__adapter_ports_lock = threading.Lock()
        self.__adapter_config = []
        self.__started = False

        def do():
            with self.__adapter_ports_lock:
                self.__adapter_ports = get_adapter_ports()

        t = threading.Thread(target=do)
        t.daemon = True
        t.start()

        power_group = self.AddGroup(Text.power_group_lbl)
        power_group.AddAction(GetDevicePower)
        power_group.AddAction(PowerOnDevice)
        power_group.AddAction(StandbyDevice)
        power_group.AddAction(PowerOnAll)
        power_group.AddAction(StandbyAll)

        volume_group = self.AddGroup(Text.volume_group_lbl)
        volume_group.AddAction(GetVolume)
        volume_group.AddAction(VolumeUp)
        volume_group.AddAction(VolumeDown)
        volume_group.AddAction(SetVolume)

        mute_group = self.AddGroup(Text.mute_group_lbl)
        mute_group.AddAction(GetMute)
        mute_group.AddAction(MuteOn)
        mute_group.AddAction(MuteOff)
        mute_group.AddAction(ToggleMute)

        self.AddAction(SendRemoteKey)
        self.AddAction(SetDeviceActiveSource)
        self.AddAction(SetHDMI)
        self.AddAction(IsActiveSource)
        self.AddAction(IsDeviceActive)
        self.AddAction(GetDeviceVendor)
        self.AddAction(GetDeviceOSDName)
        self.AddAction(GetTunerStatus)
        self.AddAction(GiveTunerStatus)
        self.AddAction(TunerChannelUp)
        self.AddAction(TunerChannelDown)
        self.AddAction(TunerStatusEvents)
        self.AddAction(PlayerStatusEvents)
        self.AddAction(SetPlayerMode)
        self.AddAction(GetPlayerStatus)
        self.AddAction(GivePlayerStatus)
        self.AddAction(DisplayMessage)
        # self.AddAction(SetAdapterDeviceType)
        # self.AddAction(SetAdapterOSDName)
        self.AddAction(RestartAdapter)
        self.AddAction(RawCommand)

        remote_group = self.AddGroup(Text.remote_group_lbl)
        remote_group.AddActionsFromList(REMOTE_ACTIONS)

    def OnComputerResume(self, _):
        self.start_adapters()

    def OnComputerSuspend(self, _):
        self.__stop__()

    @property
    def adapter_ports(self):
        with self.__adapter_ports_lock:
            return self.__adapter_ports

    @adapter_ports.setter
    def adapter_ports(self, value):
        with self.__adapter_ports_lock:
            self.__adapter_ports = value

    def __device_plugged(self, event):

        if 'VID_2548&PID_1002&MI_02' in event.payload[0]:
            def do():
                adapter_ports = get_adapter_ports()

                for port in adapter_ports:
                    if port not in self.adapter_ports:
                        break
                else:
                    return

                self.adapter_ports = adapter_ports

                if not self.__started:
                    return

                for adapter in self.adapters[:]:
                    if adapter.port == port:
                        return
                else:
                    for adapter_config in self.__adapter_config:
                        if adapter_config.strDevicePort == port:
                            adapter = PyCECAdapter(adapter_config)
                            callbacks = AdapterCallbacks(
                                self,
                                adapter,
                                adapter_config.log_info,
                                adapter_config.log_notice,
                                adapter_config.log_warning,
                                adapter_config.log_error,
                                adapter_config.log_debug,
                                adapter_config.log_file
                            )

                            setattr(
                                adapter,
                                '_adapter_callback_class',
                                callbacks
                            )

                            adapter.log_level = 31
                            adapter.source_events = True
                            adapter.command_events = True
                            adapter.menu_events = True
                            adapter.keypress_events = True
                            adapter.status_events = True

                            self.adapters += [adapter]

                            self.TriggerEvent(
                                'Adapter.{0}.Connected'.format(
                                    adapter_config.strDeviceName
                                )
                            )

            t = threading.Thread(target=do)
            t.daemon = True
            t.start()
        return False

    def __device_unplugged(self, event):
        if 'VID_2548&PID_1002&MI_02' in event.payload[0]:
            def do():
                adapter_ports = get_adapter_ports()

                for port in self.adapter_ports:
                    if port not in adapter_ports:
                        break
                else:
                    return
                self.adapter_ports = adapter_ports

                for adapter in self.adapters[:]:
                    if adapter.port == port:
                        for adapter_config in self.__adapter_config:
                            if adapter_config.strDevicePort == port:
                                break
                        else:
                            return

                        self.adapters.remove(adapter)
                        adapter.source_events = False
                        adapter.command_events = False
                        adapter.menu_events = False
                        adapter.keypress_events = False
                        adapter.status_events = False

                        self.TriggerEvent(
                            'Adapter.{0}.Disconnected'.format(
                                adapter_config.strDeviceName
                            )
                        )
                        adapter.Close()

            t = threading.Thread(target=do)
            t.daemon = True
            t.start()
        return False

    def __start__(self, adapters=()):
        del self.__adapter_config[:]

        for adapter in adapters:
            if len(adapter) == 18:
                adapter += (False,)
            (
                adapter_name,
                adapter_port,
                adapter_types,
                hdmi_port,
                power_off,
                power_standby,
                avr_audio,
                wake_avr,
                keypress_combo,
                keypress_combo_timeout,
                keypress_repeat,
                keypress_release_delay,
                keypress_double_tap,
                log_info,
                log_notice,
                log_warning,
                log_error,
                log_debug,
                log_file
            ) = adapter

            adapter_config = PyCECConfiguration(
                adapter_name=adapter_name,
                adapter_port=adapter_port,
                adapter_types=adapter_types,
                hdmi_port=hdmi_port,
                power_off=power_off,
                power_standby=power_standby,
                wake_avr=wake_avr,
                keypress_combo=keypress_combo,
                keypress_combo_timeout=keypress_combo_timeout,
                keypress_repeat=keypress_repeat,
                keypress_release_delay=keypress_release_delay,
                keypress_double_tap=keypress_double_tap,
                avr_audio=avr_audio
            )

            setattr(adapter_config, 'log_info', log_info)
            setattr(adapter_config, 'log_notice', log_notice)
            setattr(adapter_config, 'log_warning', log_warning)
            setattr(adapter_config, 'log_error', log_error)
            setattr(adapter_config, 'log_debug', log_debug)
            setattr(adapter_config, 'log_file', log_file)
            self.__adapter_config += [adapter_config]

        self.start_adapters()

    def start_adapters(self):
        def do(config):

            eg.Print(
                'CEC: Starting adapter {0} on port '
                '{1}'.format(config.strDeviceName, config.strDevicePort)
            )

            if config.strDevicePort in self.adapter_ports:
                if self.__startup_event.isSet():
                    self.__startup_threads.remove(threading.currentThread())
                    return

                adapter = PyCECAdapter(config)
                callbacks = AdapterCallbacks(
                    self,
                    adapter,
                    config.log_info,
                    config.log_notice,
                    config.log_warning,
                    config.log_error,
                    config.log_debug,
                    config.log_file
                )

                setattr(adapter, '_adapter_callback_class', callbacks)

                adapter.log_level = 31
                adapter.source_events = True
                adapter.command_events = True
                adapter.menu_events = True
                adapter.keypress_events = True
                adapter.status_events = True
                self.adapters += [adapter]

                self.TriggerEvent(
                    'Adapter.{0}.Connected'.format(config.strDeviceName)
                )
            else:
                eg.PrintError(
                    'CEC: Failed to load adapter {0} on port '
                    '{1}'.format(config.strDeviceName, config.strDevicePort)
                )

            self.__startup_threads.remove(threading.currentThread())

            if not self.__startup_threads:
                self.__bind()
                self.__started = True

        while self.__started:
            pass

        self.__startup_event.clear()

        eg.Print('CEC: Loading Adapters...')

        for adapter_config in self.__adapter_config:
            if self.__startup_event.isSet():
                break
            t = threading.Thread(target=do, args=(adapter_config,))
            t.daemon = True
            self.__startup_threads += [t]
            t.start()

    def __bind(self):
        if 'System.DeviceAttached' in eg.notificationHandlers:
            handlers = (
                eg.notificationHandlers['System.DeviceAttached'].listeners
            )
            for handler in handlers:
                if handler == self.__device_plugged:
                    break
                else:
                    eg.Bind('System.DeviceAttached', self.__device_plugged)
        else:
            eg.Bind('System.DeviceAttached', self.__device_plugged)

        if 'System.DeviceRemoved' in eg.notificationHandlers:
            handlers = (
                eg.notificationHandlers['System.DeviceAttached'].listeners
            )
            for handler in handlers:
                if handler == self.__device_unplugged:
                    break
                else:
                    eg.Bind('System.DeviceRemoved', self.__device_unplugged)
        else:
            eg.Bind('System.DeviceRemoved', self.__device_unplugged)

    def __unbind(self):
        try:
            eg.Unbind('System.DeviceAttached', self.__device_plugged)
        except:
            pass

        try:
            eg.Unbind('System.DeviceRemoved', self.__device_unplugged)
        except:
            pass

    def __stop__(self):
        self.__unbind()

        if self.__startup_threads:
            self.__startup_event.set()
            for thread in self.__startup_threads:
                thread.join()

        while self.adapters:
            adapter = self.adapters.pop(0)

            for adapter_config in self.__adapter_config:
                if adapter_config.strDevicePort == adapter.port:
                    break
            else:
                continue

            adapter.source_events = False
            adapter.command_events = False
            adapter.menu_events = False
            adapter.keypress_events = False
            adapter.status_events = False
            adapter.Close()
            self.TriggerEvent(
                'Adapter.{0}.Disconnected'.format(
                    adapter_config.strDeviceName
                )
            )

        del self.adapters[:]
        self.__started = False

    def Configure(self, adapters=()):
        global adapter_count
        adapter_count = 0

        self.__unbind()

        def add_adapter(prt):
            global adapter_count

            adptr = AdapterConfig('New Adapter')
            adapter_ctrl.add_adapter(adptr)
            adptr.adapter_port = prt
            adptr.connected = True
            adapter_count -= 1

        def device_plugged(evt):
            if 'VID_2548&PID_1002&MI_02' in evt.payload[0]:
                def do():
                    adapter_ports = get_adapter_ports()

                    for port in adapter_ports:
                        if port not in self.adapter_ports:
                            break
                    else:
                        return

                    for adapter in adapter_ctrl:
                        if adapter.adapter_port == port:
                            adapter.connected = True
                            return self.__device_plugged(evt)
                    else:
                        wx.CallAfter(add_adapter, port)

                t_plugged = threading.Thread(target=do)
                t_plugged.daemon = True
                t_plugged.start()
            return False

        def device_unplugged(evt):
            if 'VID_2548&PID_1002&MI_02' in evt.payload[0]:
                def do():
                    adapter_ports = get_adapter_ports()

                    for port in self.adapter_ports:
                        if port not in adapter_ports:
                            break
                    else:
                        return

                    for adapter in adapter_ctrl:
                        if adapter.adapter_port == port:
                            adapter.connected = False
                            return self.__device_unplugged(evt)

                t_unplugged = threading.Thread(target=do)
                t_unplugged.daemon = True
                t_unplugged.start()
            return False

        panel = eg.ConfigPanel()

        busy_ctrl = panel.StaticText('Scanning for adapters....')

        busy_sizer = wx.BoxSizer(wx.HORIZONTAL)
        busy_sizer.AddStretchSpacer(1)
        busy_sizer.Add(busy_ctrl, 0, wx.EXPAND | wx.ALL, 10)
        busy_sizer.AddStretchSpacer(1)

        adapter_ctrl = AdapterListCtrl(panel)
        adapter_box = wx.StaticBox(panel, -1, "CEC Adapters")
        adapter_sizer = wx.StaticBoxSizer(adapter_box, wx.VERTICAL)
        adapter_sizer.Add(adapter_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        ok_button = panel.dialog.buttonRow.okButton
        cancel_button = panel.dialog.buttonRow.cancelButton
        apply_button = panel.dialog.buttonRow.applyButton

        ok_button.Enable(False)
        cancel_button.Enable(False)
        apply_button.Enable(False)

        def populate():
            def on_close(evt):
                event.set()
                t.join(3.0)
                panel.dialog.OnCancel(evt)

            global adapter_count
            adapter_count = len(adapters)

            def add_adptr(adptr):
                global adapter_count
                if len(adptr) == 18:
                    adptr += (False,)

                (
                    adapter_name,
                    adapter_port,
                    adapter_type,
                    hdmi_port,
                    power_off,
                    power_standby,
                    avr_audio,
                    wake_avr,
                    keypress_combo,
                    keypress_combo_timeout,
                    keypress_repeat,
                    keypress_release_delay,
                    keypress_double_tap,
                    log_info,
                    log_notice,
                    log_warning,
                    log_error,
                    log_debug,
                    log_file
                ) = adptr

                adptr = AdapterConfig(adapter_name)
                adapter_ctrl.add_adapter(adptr)

                adptr.adapter_name = adapter_name
                adptr.adapter_port = adapter_port
                adptr.adapter_types = adapter_type
                adptr.hdmi_port = hdmi_port
                adptr.power_off = power_off
                adptr.power_standby = power_standby
                adptr.avr_audio = avr_audio
                adptr.wake_avr = wake_avr
                adptr.keypress_combo = keypress_combo
                adptr.keypress_combo_timeout = keypress_combo_timeout
                adptr.keypress_repeat = keypress_repeat
                adptr.keypress_release_delay = keypress_release_delay
                adptr.keypress_double_tap = keypress_double_tap
                adptr.log_info = log_info
                adptr.log_notice = log_notice
                adptr.log_warning = log_warning
                adptr.log_error = log_error
                adptr.log_debug = log_debug
                adptr.log_file = log_file
                adapter_count -= 1

            for a in adapters:
                wx.CallAfter(add_adptr, a)

            while adapter_count:
                event.wait(0.05)

            panel.dialog.Bind(wx.EVT_CLOSE, on_close)
            cancel_button.Enable(True)

            try:
                for port in self.adapter_ports[:]:
                    for adptr_config in adapter_ctrl:
                        if event.isSet():
                            return
                        if adptr_config.adapter_port == port:
                            adptr_config.connected = True
                            break
                    else:
                        adapter_count += 1
                        wx.CallAfter(add_adapter, port)

                while adapter_count:
                    event.wait(0.05)
            except:
                return

            if event.isSet():
                return
            for adapter in adapter_ctrl:
                if adapter.connected is None:
                    adapter.connected = False

            eg.Bind('System.DeviceAttached', device_plugged)
            eg.Bind('System.DeviceRemoved', device_unplugged)

            busy_ctrl.Hide()
            ok_button.Enable(True)
            apply_button.Enable(True)

            panel.dialog.Bind(wx.EVT_CLOSE, panel.dialog.OnCancel)

        panel.sizer.Add(busy_sizer, 0, wx.EXPAND)
        panel.sizer.Add(adapter_sizer, 1, wx.EXPAND | wx.ALL, 10)

        event = threading.Event()
        t = threading.Thread(target=populate)
        t.daemon = True
        t.start()

        while panel.Affirmed():
            panel.SetResult(adapter_ctrl.get_value())

        try:
            eg.Unbind('System.DeviceAttached', device_plugged)
        except:
            pass

        try:
            eg.Unbind('System.DeviceRemoved', device_unplugged)
        except:
            pass

        self.__bind()


class AdapterBase(eg.ActionBase):

    def GetLabel(self, com_port=None, adapter_name=None, *_):
        if None in (com_port, adapter_name):
            return '%s: Action Not Configured' % self.name

        return '%s: Adapter: %s on %s' % (self.name, adapter_name, com_port)

    def _find_adapter(self, com_port, adapter_name):
        if com_port is None and adapter_name is None:
            return None

        for adapter in self.plugin.adapters:
            if (
                com_port == adapter.port and
                adapter_name == adapter.lib_cec_device.osd_name
            ):
                return adapter
            elif (
                com_port == adapter.port and
                adapter_name == adapter.lib_cec_device.name
            ):
                return adapter

            elif com_port == adapter.port:
                return adapter

    def __call__(self, *args):
        raise NotImplementedError

    def Configure(self, com_port=None, adapter_name=None):
        panel = eg.ConfigPanel()

        adapter_ctrl = AdapterCtrl(
            panel,
            com_port,
            adapter_name,
            self.plugin.adapters
        )

        panel.sizer.Add(adapter_ctrl, 0, wx.EXPAND)

        if adapter_name is None and len(self.plugin.adapters) == 1:
            def do():
                panel.dialog.buttonRow.okButton.Enable()
                panel.dialog.buttonRow.applyButton.Enable()

            wx.CallAfter(do)

        while panel.Affirmed():
            panel.SetResult(*adapter_ctrl.GetValue())


class DeviceBase(AdapterBase):

    def GetLabel(self, com_port=None, adapter_name=None, device=None):

        if device is None:
            return '%s: Action Not Configured' % self.name

        return '%s: Adapter: %s on %s' % (
            self.name.replace('a Device', device).replace('Device', device),
            adapter_name,
            com_port
        )

    def _process_call(self, device):
        raise NotImplementedError

    def __call__(self, com_port=None, adapter_name=None, device='TV'):
        adapter = self._find_adapter(com_port, adapter_name)

        if adapter is None:
            eg.PrintNotice(
                'CEC: Adapter %s on com port %s not found' %
                (adapter_name, com_port)
            )
        elif device in adapter:
            dev = adapter[device]
            return self._process_call(dev)
        else:
            eg.PrintNotice(
                'CEC: Device %s not found in adapter %s' %
                (device, adapter_name)
            )

    def Configure(self, com_port=None, adapter_name=None, device='TV'):
        panel = eg.ConfigPanel()

        adapter_ctrl = AdapterCtrl(
            panel,
            com_port,
            adapter_name,
            self.plugin.adapters
        )

        device_ctrl = DeviceCtrl(panel)
        device_ctrl.UpdateDevices(
            self._find_adapter(*adapter_ctrl.GetValue())
        )

        if adapter_name is None and len(self.plugin.adapters) == 1:
            device_ctrl.UpdateDevices(
                self._find_adapter(*adapter_ctrl.GetValue())
            )

            def do():
                panel.dialog.buttonRow.okButton.Enable()
                panel.dialog.buttonRow.applyButton.Enable()

            wx.CallAfter(do)

        def on_choice(evt):
            device_ctrl.UpdateDevices(
                self._find_adapter(*adapter_ctrl.GetValue())
            )
            evt.Skip()

        adapter_ctrl.Bind(wx.EVT_CHOICE, on_choice)
        panel.sizer.Add(adapter_ctrl, 0, wx.EXPAND)
        panel.sizer.Add(device_ctrl, 0, wx.EXPAND)

        while panel.Affirmed():
            com_port, adapter_name = adapter_ctrl.GetValue()
            panel.SetResult(
                com_port,
                adapter_name,
                device_ctrl.GetValue()
            )


class RestartAdapter(AdapterBase):

    def __call__(self, com_port=None, adapter_name=None):
        adapter = self._find_adapter(com_port, adapter_name)
        self.plugin.adapters[self.plugin.adapters.index(adapter)] = (
            adapter.Restart()
        )


class VolumeUp(AdapterBase):

    def __call__(self, com_port=None, adapter_name=None):
        adapter = self._find_adapter(com_port, adapter_name)
        return adapter.volume_up()


class VolumeDown(AdapterBase):

    def __call__(self, com_port=None, adapter_name=None):
        adapter = self._find_adapter(com_port, adapter_name)
        return adapter.volume_down()


class GetVolume(AdapterBase):

    def __call__(self, com_port=None, adapter_name=None):
        adapter = self._find_adapter(com_port, adapter_name)
        return adapter.volume


class GetMute(AdapterBase):
    def __call__(self, com_port=None, adapter_name=None):
        adapter = self._find_adapter(com_port, adapter_name)
        return adapter.mute


class ToggleMute(AdapterBase):
    def __call__(self, com_port=None, adapter_name=None):
        adapter = self._find_adapter(com_port, adapter_name)
        return adapter.toggle_mute()


class MuteOn(AdapterBase):
    def __call__(self, com_port=None, adapter_name=None):
        adapter = self._find_adapter(com_port, adapter_name)
        adapter.mute = True
        return adapter.mute


class MuteOff(AdapterBase):
    def __call__(self, com_port=None, adapter_name=None):
        adapter = self._find_adapter(com_port, adapter_name)
        adapter.mute = False
        return adapter.mute


class PowerOnAll(AdapterBase):
    def __call__(self, com_port=None, adapter_name=None):
        adapter = self._find_adapter(com_port, adapter_name)
        adapter.power = True


class StandbyAll(AdapterBase):
    def __call__(self, com_port=None, adapter_name=None):
        adapter = self._find_adapter(com_port, adapter_name)
        adapter.power = False


class StandbyDevice(DeviceBase):
    def _process_call(self, device):
        device.power = False
        return device.power


class GetDevicePower(DeviceBase):
    def _process_call(self, device):
        return device._adapter.PowerStatusToString(device.power).title()


class PowerOnDevice(DeviceBase):
    def _process_call(self, device):
        device.power = True
        return device.power


class GetDeviceVendor(DeviceBase):
    def _process_call(self, device):
        return device.vendor


class IsActiveSource(DeviceBase):
    def _process_call(self, device):
        return device.active_source


class IsDeviceActive(DeviceBase):
    def _process_call(self, device):
        return device.active_device


class GetDeviceOSDName(DeviceBase):
    def _process_call(self, device):
        return device.osd_name


class SetDeviceActiveSource(DeviceBase):
    def _process_call(self, device):
        device.active_source = True
        return device.active_source


class RawCommand(AdapterBase):

    def GetLabel(self, com_port=None, adapter_name=None, command=None):

        if command is None:
            return 'Send Raw Command: Action Not Configured'

        return 'Send Raw Command %s: Adapter: %s on %s' % (
            str(command),
            adapter_name,
            com_port
        )

    def __call__(self, com_port=None, adapter_name=None, command=""):

        if isinstance(command, unicode):
            command = ''.join(map(chr, list(command)))

        adapter = self._find_adapter(com_port, adapter_name)

        packet = adapter.CommandFromString(command)
        return adapter.raw_command(packet=packet)

    def Configure(self, com_port=None, adapter_name=None, command=''):
        panel = eg.ConfigPanel()

        adapter_ctrl = AdapterCtrl(
            panel,
            com_port,
            adapter_name,
            self.plugin.adapters
        )

        command_st = panel.StaticText(Text.command_lbl)
        command_ctrl = panel.TextCtrl(command)

        command_sizer = wx.BoxSizer(wx.HORIZONTAL)
        command_sizer.Add(command_st, 0, wx.EXPAND | wx.ALL, 5)
        command_sizer.Add(command_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(adapter_ctrl, 0, wx.EXPAND)
        panel.sizer.Add(command_sizer, 0, wx.EXPAND)

        if adapter_name is None and len(self.plugin.adapters) == 1:
            def do():
                panel.dialog.buttonRow.okButton.Enable()
                panel.dialog.buttonRow.applyButton.Enable()

            wx.CallAfter(do)

        while panel.Affirmed():
            com_port, adapter_name = adapter_ctrl.GetValue()
            panel.SetResult(com_port, adapter_name, command_ctrl.GetValue())


class SetHDMI(AdapterBase):

    def GetLabel(self, com_port=None, adapter_name=None, source=None):

        if source is None:
            return 'Set Source: Action Not Configured'

        return 'Set Source %s: Adapter: %s on %s' % (
            str(source),
            adapter_name,
            com_port
        )

    def __call__(self, com_port=None, adapter_name=None, source='TV'):

        adapter = self._find_adapter(com_port, adapter_name)
        template = '4F:82:{port}0:00'

        hdmi_port = source.upper().split('I')[-1].strip()
        if not hdmi_port.isdigit():
            eg.PrintError('Set Source: incorrect source specified')
            return

        ports = {
            '10': 'A',
            '11': 'B',
            '12': 'C',
            '13': 'D',
            '14': 'E',
            '15': 'F'
        }

        if hdmi_port in ports:
            hdmi_port = ports[hdmi_port]

        command = template.format(port=hdmi_port)
        packet = adapter.CommandFromString(command)
        return adapter.raw_command(packet=packet)

    def Configure(self, com_port=None, adapter_name=None, source='HDMI 1'):
        panel = eg.ConfigPanel()

        choices = list('HDMI ' + str(i) for i in range(1, 16))

        adapter_ctrl = AdapterCtrl(
            panel,
            com_port,
            adapter_name,
            self.plugin.adapters
        )

        source_st = panel.StaticText(Text.source_lbl)
        source_ctrl = wx.Choice(panel, -1, choices=choices)
        source_ctrl.SetStringSelection(source)

        source_sizer = wx.BoxSizer(wx.HORIZONTAL)
        source_sizer.Add(source_st, 0, wx.EXPAND | wx.ALL, 5)
        source_sizer.Add(source_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(adapter_ctrl, 0, wx.EXPAND)
        panel.sizer.Add(source_sizer, 0, wx.EXPAND)

        if adapter_name is None and len(self.plugin.adapters) == 1:
            def do():
                panel.dialog.buttonRow.okButton.Enable()
                panel.dialog.buttonRow.applyButton.Enable()

            wx.CallAfter(do)

        while panel.Affirmed():
            com_port, adapter_name = adapter_ctrl.GetValue()
            panel.SetResult(
                com_port,
                adapter_name,
                source_ctrl.GetStringSelection()
            )


class SetVolume(AdapterBase):

    def GetLabel(self, com_port=None, adapter_name=None, volume=None):

        if volume is None:
            return 'Set Volume: Action Not Configured'
        return 'Set Volume to %s: Adapter: %s on %s' % (
            str(volume),
            adapter_name,
            com_port
        )

    def __call__(self, com_port=None, adapter_name=None, volume=0):
        adapter = self._find_adapter(com_port, adapter_name)
        adapter.volume = volume
        return adapter.volume

    def Configure(self, com_port=None, adapter_name=None, volume=0):
        panel = eg.ConfigPanel()

        adapter_ctrl = AdapterCtrl(
            panel,
            com_port,
            adapter_name,
            self.plugin.adapters
        )
        volume_st = panel.StaticText(Text.volume_lbl)
        volume_ctrl = panel.SpinIntCtrl(volume, min=0, max=100)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(volume_st, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(volume_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(adapter_ctrl, 0, wx.EXPAND)
        panel.sizer.Add(sizer, 0, wx.EXPAND)

        if adapter_name is None and len(self.plugin.adapters) == 1:
            def do():
                panel.dialog.buttonRow.okButton.Enable()
                panel.dialog.buttonRow.applyButton.Enable()

            wx.CallAfter(do)

        while panel.Affirmed():
            com_port, adapter_name = adapter_ctrl.GetValue()
            panel.SetResult(com_port, adapter_name, volume_ctrl.GetValue())


class SendRemoteKey(AdapterBase):

    def GetLabel(
        self,
        com_port=None,
        adapter_name=None,
        device=None,
        key=None
    ):
        if key is None:
            key = getattr(self, 'value', None)

        if None in (device, key, com_port, adapter_name):
            if key is None:
                return 'Send Remote Key: Action Not Configured'
            return 'Send "%s" Remote Key: Action Not Configured' % key

        return 'Send "%s" Remote Key to %s: Adapter: %s on %s' % (
            key,
            device,
            adapter_name,
            com_port
        )

    def __call__(
        self,
        com_port=None,
        adapter_name=None,
        device=None,
        key=None
    ):
        if key is None:
            key = getattr(self, 'value', None)
            if key is None or (com_port is None and adapter_name is None):
                eg.PrintNotice(
                    'CEC: This action needs to be configured before use.'
                )
                return

        if key not in KEY_CODES:
            eg.PrintNotice(
                'CEC: Key name {0} not found.'.format(key)
            )
            return

        adapter = self._find_adapter(com_port, adapter_name)

        if adapter is None:
            eg.PrintNotice(
                'CEC: Adapter %s on com port %s not found' %
                (adapter_name, com_port)
            )
        elif device in adapter:
                dev = adapter[device]
                dev.key_press(KEY_CODES[key])
                time.sleep(0.05)
                dev.key_release()

        else:
            eg.PrintNotice(
                'CEC: Device %s not found in adapter %s' %
                (device, adapter_name)
            )

    def Configure(
        self,
        com_port=None,
        adapter_name=None,
        device=None,
        key=None
    ):
        panel = eg.ConfigPanel()

        adapter_ctrl = AdapterCtrl(
            panel,
            com_port,
            adapter_name,
            self.plugin.adapters
        )

        device_ctrl = DeviceCtrl(panel)

        if adapter_name is None and len(self.plugin.adapters) == 1:
            device_ctrl.UpdateDevices(
                self._find_adapter(*adapter_ctrl.GetValue())
            )

            def do():
                panel.dialog.buttonRow.okButton.Enable()
                panel.dialog.buttonRow.applyButton.Enable()

            wx.CallAfter(do)

        else:
            adapter = self._find_adapter(com_port, adapter_name)

            if adapter is not None:
                device_ctrl.UpdateDevices(adapter, device)

        def on_choice(evt):
            device_ctrl.UpdateDevices(
                self._find_adapter(*adapter_ctrl.GetValue())
            )

            evt.Skip()

        adapter_ctrl.Bind(wx.EVT_CHOICE, on_choice)
        panel.sizer.Add(adapter_ctrl, 0, wx.EXPAND)
        panel.sizer.Add(device_ctrl, 0, wx.EXPAND)

        if not hasattr(self, 'value'):
            if key is None:
                key = ''

            key_st = panel.StaticText(Text.key_lbl)
            key_ctrl = panel.Choice(
                0,
                choices=sorted(KEY_CODES.keys())
            )

            key_ctrl.SetStringSelection(key)

            key_sizer = wx.BoxSizer(wx.HORIZONTAL)
            key_sizer.Add(key_st, 0, wx.EXPAND | wx.ALL, 5)
            key_sizer.Add(key_ctrl, 0, wx.EXPAND | wx.ALL, 5)
            panel.sizer.Add(key_sizer, 0, wx.EXPAND)
        else:
            key_ctrl = None

        while panel.Affirmed():
            com_port, adapter_name = adapter_ctrl.GetValue()
            panel.SetResult(
                com_port,
                adapter_name,
                device_ctrl.GetValue(),
                None if key_ctrl is None else key_ctrl.GetStringSelection()
            )

class SetPlayerMode(AdapterBase):

    def __call__(self, com_port, adapter_name, device, mode):
        mode = mode.lower().replace(' ', '_')
        adapter = self._find_adapter(com_port, adapter_name)

        if adapter is None:
            eg.PrintNotice(
                'CEC: Adapter %s on com port %s not found' %
                (adapter_name, com_port)
            )
        elif device in adapter:
            dev = adapter[device]
            getattr(dev, mode)()
        else:
            eg.PrintNotice(
                'CEC: Device %s not found in adapter %s' %
                (device, adapter_name)
            )

    def Configure(
        self,
        com_port=None,
        adapter_name=None,
        device=None,
        mode='Play'
    ):

        choices = [
            'Play',
            'Pause',
            'Stop',
            'Eject',
            'Fast Forward',
            'Rewind',
            'Skip Forward',
            'Skip Back'
        ]

        panel = eg.ConfigPanel()

        adapter_ctrl = AdapterCtrl(
            panel,
            com_port,
            adapter_name,
            self.plugin.adapters
        )

        device_st = panel.StaticText(Text.device_lbl)
        device_ctrl = eg.Choice(panel, 0, choices=[])

        device_sizer = wx.BoxSizer(wx.HORIZONTAL)
        device_sizer.Add(device_st, 0, wx.EXPAND | wx.ALL, 5)
        device_sizer.Add(device_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        mode_st = panel.StaticText(Text.mode_lbl)
        mode_ctrl = wx.Choice(panel, -1, choices=choices)
        mode_ctrl.SetStringSelection(mode)

        mode_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mode_sizer.Add(mode_st, 0, wx.EXPAND | wx.ALL, 5)
        mode_sizer.Add(mode_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        def update_devices(adapter, dev_name=None):
            if dev_name is None:
                if device_ctrl.GetItems():
                    dev_name = device_ctrl.GetStringSelection()
                else:
                    dev_name = ''

            dev_choices = list(
                d.osd_name
                for d in adapter
                if d.is_player
            )
            device_ctrl.SetItems(dev_choices)

            if dev_name in dev_choices:
                device_ctrl.SetStringSelection(dev_name)
            else:
                device_ctrl.SetSelection(0)

        def on_adapter_choice(evt):
            adapter = self._find_adapter(*adapter_ctrl.GetValue())
            if adapter is not None:
                update_devices(adapter)
            evt.Skip()

        if adapter_name is None and len(self.plugin.adapters) == 1:
            update_devices(
                self._find_adapter(*adapter_ctrl.GetValue())
            )

            def do():
                panel.dialog.buttonRow.okButton.Enable()
                panel.dialog.buttonRow.applyButton.Enable()

            wx.CallAfter(do)

        else:
            adapter = self._find_adapter(com_port, adapter_name)

            if adapter is not None:
                update_devices(adapter, device)

        adapter_ctrl.Bind(wx.EVT_CHOICE, on_adapter_choice)

        panel.sizer.Add(adapter_ctrl, 0, wx.EXPAND)
        panel.sizer.Add(device_sizer, 0, wx.EXPAND)
        panel.sizer.Add(mode_sizer, 0, wx.EXPAND)

        while panel.Affirmed():
            com_port, adapter_name = adapter_ctrl.GetValue()
            panel.SetResult(
                com_port,
                adapter_name,
                device_ctrl.GetStringSelection(),
                mode_ctrl.GetStringSelection()
            )


class GetStatusBase(DeviceBase):
    _device_type = None

    def _process_call(self, device):
        return device.status

    def Configure(self, com_port=None, adapter_name=None, device=None):
        panel = eg.ConfigPanel()

        adapter_ctrl = AdapterCtrl(
            panel,
            com_port,
            adapter_name,
            self.plugin.adapters
        )

        device_st = panel.StaticText(Text.device_lbl)
        device_ctrl = eg.Choice(panel, 0, choices=[])

        device_sizer = wx.BoxSizer(wx.HORIZONTAL)
        device_sizer.Add(device_st, 0, wx.EXPAND | wx.ALL, 5)
        device_sizer.Add(device_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        def update_devices(adapter, dev_name=None):
            if dev_name is None:
                if device_ctrl.GetItems():
                    dev_name = device_ctrl.GetStringSelection()
                else:
                    dev_name = ''

            dev_choices = list(
                d.osd_name
                for d in adapter
                if getattr(d, self._device_type)
            )
            device_ctrl.SetItems(dev_choices)

            if dev_name in dev_choices:
                device_ctrl.SetStringSelection(dev_name)
            else:
                device_ctrl.SetSelection(0)

        def on_adapter_choice(evt):
            adapter = self._find_adapter(*adapter_ctrl.GetValue())
            if adapter is not None:
                update_devices(adapter)
            evt.Skip()

        if adapter_name is None and len(self.plugin.adapters) == 1:
            update_devices(
                self._find_adapter(*adapter_ctrl.GetValue())
            )

            def do():
                panel.dialog.buttonRow.okButton.Enable()
                panel.dialog.buttonRow.applyButton.Enable()

            wx.CallAfter(do)

        else:
            adapter = self._find_adapter(com_port, adapter_name)

            if adapter is not None:
                update_devices(adapter, device)

        adapter_ctrl.Bind(wx.EVT_CHOICE, on_adapter_choice)

        panel.sizer.Add(adapter_ctrl, 0, wx.EXPAND)
        panel.sizer.Add(device_sizer, 0, wx.EXPAND)

        while panel.Affirmed():
            com_port, adapter_name = adapter_ctrl.GetValue()
            panel.SetResult(
                com_port,
                adapter_name,
                device_ctrl.GetStringSelection()
            )


class GetPlayerStatus(GetStatusBase):
    _device_type = 'is_player'


class GetTunerStatus(GetStatusBase):
    _device_type = 'is_tuner'


class StatusEventsBase(AdapterBase):
    _device_type = None

    def __call__(self, com_port, adapter_name, device, events):
        adapter = self._find_adapter(com_port, adapter_name)

        if adapter is None:
            eg.PrintNotice(
                'CEC: Adapter %s on com port %s not found' %
                (adapter_name, com_port)
            )
        elif device in adapter:
            dev = adapter[device]
            dev.enable_notifications = events
        else:
            eg.PrintNotice(
                'CEC: Device %s not found in adapter %s' %
                (device, adapter_name)
            )

    def Configure(
        self,
        com_port=None,
        adapter_name=None,
        device=None,
        events=False
    ):

        choices = [
            'Off',
            'On'
        ]

        panel = eg.ConfigPanel()

        adapter_ctrl = AdapterCtrl(
            panel,
            com_port,
            adapter_name,
            self.plugin.adapters
        )

        device_st = panel.StaticText(Text.device_lbl)
        device_ctrl = eg.Choice(panel, 0, choices=[])

        device_sizer = wx.BoxSizer(wx.HORIZONTAL)
        device_sizer.Add(device_st, 0, wx.EXPAND | wx.ALL, 5)
        device_sizer.Add(device_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        event_st = panel.StaticText(Text.events_lbl)
        event_ctrl = wx.Choice(panel, -1, choices=choices)
        event_ctrl.SetSelection(int(events))

        event_sizer = wx.BoxSizer(wx.HORIZONTAL)
        event_sizer.Add(event_st, 0, wx.EXPAND | wx.ALL, 5)
        event_sizer.Add(event_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        def update_devices(adapter, dev_name=None):
            if dev_name is None:
                if device_ctrl.GetItems():
                    dev_name = device_ctrl.GetStringSelection()
                else:
                    dev_name = ''

            dev_choices = list(
                d.osd_name
                for d in adapter
                if getattr(d, self._device_type)
            )
            device_ctrl.SetItems(dev_choices)

            if dev_name in dev_choices:
                device_ctrl.SetStringSelection(dev_name)
            else:
                device_ctrl.SetSelection(0)

        def on_adapter_choice(evt):
            adapter = self._find_adapter(*adapter_ctrl.GetValue())
            if adapter is not None:
                update_devices(adapter)
            evt.Skip()

        if adapter_name is None and len(self.plugin.adapters) == 1:
            update_devices(
                self._find_adapter(*adapter_ctrl.GetValue())
            )

            def do():
                panel.dialog.buttonRow.okButton.Enable()
                panel.dialog.buttonRow.applyButton.Enable()

            wx.CallAfter(do)

        else:
            adapter = self._find_adapter(com_port, adapter_name)

            if adapter is not None:
                update_devices(adapter, device)

        adapter_ctrl.Bind(wx.EVT_CHOICE, on_adapter_choice)

        panel.sizer.Add(adapter_ctrl, 0, wx.EXPAND)
        panel.sizer.Add(device_sizer, 0, wx.EXPAND)
        panel.sizer.Add(event_sizer, 0, wx.EXPAND)

        while panel.Affirmed():
            com_port, adapter_name = adapter_ctrl.GetValue()
            panel.SetResult(
                com_port,
                adapter_name,
                device_ctrl.GetStringSelection(),
                bool(event_ctrl.GetSelection())
            )


class PlayerStatusEvents(StatusEventsBase):
    _device_type = 'is_player'


class TunerStatusEvents(StatusEventsBase):
    _device_type = 'is_tuner'


class DisplayMessage(AdapterBase):

    def __call__(self, com_port, adapter_name, device, message, duration):
        adapter = self._find_adapter(com_port, adapter_name)

        if adapter is None:
            eg.PrintNotice(
                'CEC: Adapter %s on com port %s not found' %
                (adapter_name, com_port)
            )
        elif device in adapter:
            dev = adapter[device]
            dev.display_osd_message(message, duration)
        else:
            eg.PrintNotice(
                'CEC: Device %s not found in adapter %s' %
                (device, adapter_name)
            )

    def Configure(
        self,
        com_port=None,
        adapter_name=None,
        device=None,
        message='',
        duration=30
    ):
        panel = eg.ConfigPanel()

        adapter_ctrl = AdapterCtrl(
            panel,
            com_port,
            adapter_name,
            self.plugin.adapters
        )

        device_st = panel.StaticText(Text.device_lbl)
        device_ctrl = eg.Choice(panel, 0, choices=[])

        device_sizer = wx.BoxSizer(wx.HORIZONTAL)
        device_sizer.Add(device_st, 0, wx.EXPAND | wx.ALL, 5)
        device_sizer.Add(device_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        message_st = panel.StaticText(Text.message_lbl)
        message_ctrl = panel.TextCtrl(message, style=wx.TE_MULTILINE)

        message_sizer = wx.BoxSizer(wx.HORIZONTAL)
        message_sizer.Add(message_st, 0, wx.EXPAND | wx.ALL, 5)
        message_sizer.Add(message_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        duration_st = panel.StaticText(Text.duration_lbl)
        duration_ctrl = panel.SpinIntCtrl(duration)

        duration_sizer = wx.BoxSizer(wx.HORIZONTAL)
        duration_sizer.Add(duration_st, 0, wx.EXPAND | wx.ALL, 5)
        duration_sizer.Add(duration_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        def update_devices(adapter, dev_name=None):
            if dev_name is None:
                if device_ctrl.GetItems():
                    dev_name = device_ctrl.GetStringSelection()
                else:
                    dev_name = ''

            dev_choices = list(d.osd_name for d in adapter)
            device_ctrl.SetItems(dev_choices)

            if dev_name in dev_choices:
                device_ctrl.SetStringSelection(dev_name)
            else:
                device_ctrl.SetSelection(0)

        def on_adapter_choice(evt):
            adapter = self._find_adapter(*adapter_ctrl.GetValue())
            if adapter is not None:
                update_devices(adapter)
            evt.Skip()

        if adapter_name is None and len(self.plugin.adapters) == 1:
            update_devices(
                self._find_adapter(*adapter_ctrl.GetValue())
            )

            def do():
                panel.dialog.buttonRow.okButton.Enable()
                panel.dialog.buttonRow.applyButton.Enable()

            wx.CallAfter(do)

        else:
            adapter = self._find_adapter(com_port, adapter_name)

            if adapter is not None:
                update_devices(adapter, device)

        adapter_ctrl.Bind(wx.EVT_CHOICE, on_adapter_choice)

        panel.sizer.Add(adapter_ctrl, 0, wx.EXPAND)
        panel.sizer.Add(device_sizer, 0, wx.EXPAND)
        panel.sizer.Add(message_sizer, 1, wx.EXPAND)
        panel.sizer.Add(duration_sizer, 0, wx.EXPAND)

        while panel.Affirmed():
            com_port, adapter_name = adapter_ctrl.GetValue()
            panel.SetResult(
                com_port,
                adapter_name,
                device_ctrl.GetStringSelection(),
                message_ctrl.GetValue(),
                duration_ctrl.GetValue()
            )


class ChannelBase(DeviceBase):

    def Configure(
        self,
        com_port=None,
        adapter_name=None,
        device=None
    ):
        panel = eg.ConfigPanel()

        adapter_ctrl = AdapterCtrl(
            panel,
            com_port,
            adapter_name,
            self.plugin.adapters
        )

        device_st = panel.StaticText(Text.device_lbl)
        device_ctrl = eg.Choice(panel, 0, choices=[])

        device_sizer = wx.BoxSizer(wx.HORIZONTAL)
        device_sizer.Add(device_st, 0, wx.EXPAND | wx.ALL, 5)
        device_sizer.Add(device_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        def update_devices(adapter, dev_name=None):
            if dev_name is None:
                if device_ctrl.GetItems():
                    dev_name = device_ctrl.GetStringSelection()
                else:
                    dev_name = ''

            dev_choices = list(
                d.osd_name
                for d in adapter
                if d.is_tuner
            )
            device_ctrl.SetItems(dev_choices)

            if dev_name in dev_choices:
                device_ctrl.SetStringSelection(dev_name)
            else:
                device_ctrl.SetSelection(0)

        def on_adapter_choice(evt):
            adapter = self._find_adapter(*adapter_ctrl.GetValue())
            if adapter is not None:
                update_devices(adapter)
            evt.Skip()

        adapter = self._find_adapter(com_port, adapter_name)

        if adapter is not None:
            update_devices(adapter, device)

        adapter_ctrl.Bind(wx.EVT_CHOICE, on_adapter_choice)

        panel.sizer.Add(adapter_ctrl, 0, wx.EXPAND)
        panel.sizer.Add(device_sizer, 0, wx.EXPAND)

        while panel.Affirmed():
            com_port, adapter_name = adapter_ctrl.GetValue()
            panel.SetResult(
                com_port,
                adapter_name,
                device_ctrl.GetStringSelection()
            )


class TunerChannelUp(ChannelBase):
    def _process_call(self, device):
        device.channel_up()


class TunerChannelDown(ChannelBase):
    def _process_call(self, device):
        device.channel_down()


class GiveStatusBase(eg.ActionBase):
    _transmit = None
    _choices = []

    def __call__(self, status):
        suffix = eg.event.suffix.split('.')
        adapter_name = suffix[0]
        source_name = suffix[1]
        destination_name = eg.event.payload

        for adapter in self.plugin.adapters:
            if adapter.name == adapter_name:
                break
        else:
            eg.PrintNotice('CEC: Adapter %s not found' % adapter_name)
            return

        if source_name in adapter:
            source_device = adapter[source_name]
        else:
            eg.PrintNotice(
                'CEC: Source Device %s not found in adapter %s' %
                (source_name, adapter_name)
            )
            return

        if destination_name in adapter:
            destination_device = adapter[destination_name]
        else:
            eg.PrintNotice(
                'CEC: Destination Device %s not found in adapter %s' %
                (destination_name, adapter_name)
            )
            return

        for name, code in self._choices:
            if name == status:
                break
        else:
            valid_statuses = ', '.join(item[0] for item in self._choices)
            eg.PrintNotice(
                'CEC: Invalid status {0}.\n Allowed statuses: {1}'.format(
                    status,
                    valid_statuses
                )
            )
            return

        transmit = getattr(source_device, self._transmit)
        transmit(destination_device.logical_address, code)

    def Configure(self, status=None):

        panel = eg.ConfigPanel()
        choices = list(item[0] for item in self._choices)

        if status is None:
            choices.insert(0, '')
            status = ''

        status_st = panel.StaticText(Text.status_lbl)
        status_ctrl = wx.Choice(panel, -1, choices=choices)
        status_ctrl.SetStringSelection(status)

        status_sizer = wx.BoxSizer(wx.HORIZONTAL)
        status_sizer.Add(status_st, 0, wx.EXPAND | wx.ALL, 5)
        status_sizer.Add(status_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        def on_status_choice(evt):
            choices.remove('')
            value = status_ctrl.GetStringSelection()
            status_ctrl.Clear()
            status_ctrl.AppendItems(choices)
            status_ctrl.SetStringSelection(value)
            status_ctrl.Unbind(wx.EVT_CHOICE, handler=on_status_choice)
            evt.Skip()

        if '' in choices:
            status_ctrl.Bind(wx.EVT_CHOICE, on_status_choice)

        panel.sizer.Add(status_sizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                status_ctrl.GetStringSelection()
            )


class GivePlayerStatus(GiveStatusBase):
    _transmit = 'transmit_deck_info'
    _choices = sorted(
        (value.title(), key) for key, value in PLAYER_STATUS_TO_STRING.items()
    )


class GiveTunerStatus(GiveStatusBase):
    _transmit = 'transmit_tuner_status'
    _choices = sorted(
        (value.title(), key) for key, value in TUNER_STATUS_TO_STRING.items()
    )


REMOTE_ACTIONS = ()

for remote_key in KEY_CODES:
    key_func = remote_key
    for rep in ('Samsung', 'Blue', 'Red', 'Green', 'Yellow'):
        key_func = key_func.replace(' (%s)' % rep, '')
    key_func = key_func.replace('.', 'DOT').replace('+', '_').replace(' ', '_')

    REMOTE_ACTIONS += ((
        SendRemoteKey,
        'fn' + key_func.upper(),
        'Remote Key: ' + remote_key,
        'Remote Key ' + remote_key,
        remote_key
    ),)
