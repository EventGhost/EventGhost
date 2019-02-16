# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2018 EventGhost Project <http://www.eventghost.net/>
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


import sys # NOQA
import os # NOQA
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'libs'))

import eg


eg.RegisterPlugin(
    name="Samsung Smart TV IP Control +",
    author="K",
    version="0.4.1b",
    kind="external",
    description=(
        'This plugin supports all Samsung Smart TV\'s made on or after 2008.\n'
        'The TV can have either a wired or wireless network connection'
    ),
    createMacrosOnAdd=True,
    canMultiLoad=False,
    guid='{70C46E47-3DC9-4BF8-B817-6F20B324F2BB}'
)

import threading # NOQA
import wx # NOQA
from samsungctl import discover # NOQA
from samsungctl import Config # NOQA
from wx.lib import itemspicker # NOQA
from wx.lib import scrolledpanel # NOQA


class SamsungConfig(eg.PersistentData):
    tv_data = {}


class Text(eg.TranslatableStrings):
    tv_label = 'TV:'
    ip_label = 'IP Address:'
    model_label = 'Model:'
    type_label = 'Panel Type:'
    size_label = 'Panel Size:'
    device_id_label = 'Device Id:'
    name_label = 'TV Name:'
    technology_label = 'Panel Technology:'
    resolution_label = 'Panel Resolution:'
    region_label = 'Mfg Region:'
    year_label = 'Mfg Year:'
    tuner_label = 'Tuner Count:'
    dtv_label = 'DTV Support:'
    pvr_label = 'PVR Support:'
    voice_label = 'Voice Support:'
    frame_label = 'Frame TV Support:'
    gamepad_label = 'GamePad Support:'
    os_label = 'Operating System:'
    firmware_label = 'Firmware Version:'
    network_label = 'Network Type:'
    wifi_label = 'Wifi MAC Address:'
    volume_label = 'Volume:'
    brightness_label = 'Brightness:'
    source_label = 'Source:'
    color_temperature_label = 'Color Temperature:'
    url_label = 'URL:'
    app_label = 'App Id:'
    sharpness_label = 'Sharpness:'
    contrast_label = 'Contrast:'
    mute_label = 'Mute:'
    key_label = 'Remote Key:'

    class SetSource:
        name = 'Set Source'
        description = 'Set the input/source'

    class GetSource:
        name = 'Get Source'
        description = 'Get the input/source'

    class GetSources:
        name = 'Get Source List'
        description = 'Gets a List of the available sources'

    class SetVolume:
        name = 'Set Volume'
        description = 'Set the volume'

    class GetVolume:
        name = 'Get Volume'
        description = 'Get the Volume'

    class SetBrightness:
        name = 'Set Brightness'
        description = 'Set the brightness'

    class GetBrightness:
        name = 'Get Brightness'
        description = 'Get the brightness'

    class SetContrast:
        name = 'Set Contrast'
        description = 'Set the contrast'

    class GetContrast:
        name = 'Get Contrast'
        description = 'Get the contrast'

    class SetSharpness:
        name = 'Set Sharpness'
        description = 'Set the sharpness'

    class GetSharpness:
        name = 'Get Sharpness'
        description = 'Get the sharpness'

    class SetColorTemperature:
        name = 'Set Color Temperature'
        description = 'Set the color temperature'

    class GetColorTemperature:
        name = 'Get Color Temperature'
        description = 'Get the color temperature'

    class SetMute:
        name = 'Set Mute'
        description = 'Set the volume mute'

    class GetMute:
        name = 'Get Mute'
        description = 'Get the volume mute'

    class GetPower:
        name = 'Get Power'
        description = 'Get the power state'

    class GetChannel:
        name = 'Get Channel'
        description = 'Get the channel'

    class GetChannels:
        name = 'Get Channel List'
        description = 'Get a list of the available channels'

    class RunBrowser:
        name = 'Open Browser'
        description = 'Opens the browser to the entered URL'

    class RunApplication:
        name = 'Run Application'
        description = 'Run the entered application'

    class SendKey:
        name = "Send Key"
        description = "Send a remote control button"


class TVDataCtrl(scrolledpanel.ScrolledPanel):

    def __init__(self, parent):
        scrolledpanel.ScrolledPanel.__init__(
            self,
            parent,
            -1,
            style=wx.BORDER_SUNKEN,
            size=(-1, -1)
        )
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.header1 = header1 = wx.StaticText(self, -1, ' ' * 20)
        font1 = header1.GetFont()
        font1.SetPixelSize((0, 35))
        header1.SetFont(font1)

        self.header2 = header2 = wx.StaticText(self, -1, ' ' * 20)
        font2 = header2.GetFont()
        font2.SetPixelSize((0, 28))
        header2.SetFont(font2)

        line = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)

        sizer.Add(header1, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(header2, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 10)
        sizer.Add(line, 0, wx.EXPAND | wx.ALL, 5)

        self.ctrls = []

        def create(label, ctrl=None):
            st = wx.StaticText(self, -1, label)
            if ctrl is None:
                ctrl = wx.StaticText(self, -1, ' ' * 20)
                self.ctrls += [ctrl]

            t_sizer = h_sizer(st, ctrl)
            sizer.Add(t_sizer, 0, wx.EXPAND | wx.LEFT, 5)

        self.name_ctrl = wx.TextCtrl(self, -1, ' ' * 20)
        create(Text.name_label, self.name_ctrl)

        self.model_ctrl = wx.StaticText(self, -1, ' ' * 20)
        create(Text.model_label, self.model_ctrl)

        create(Text.size_label)
        create(Text.type_label)
        create(Text.technology_label)
        create(Text.resolution_label)
        create(Text.year_label)
        create(Text.region_label)
        create(Text.tuner_label)
        create(Text.dtv_label)
        create(Text.pvr_label)
        create(Text.voice_label)
        create(Text.frame_label)
        create(Text.gamepad_label)
        create(Text.firmware_label)
        create(Text.os_label)
        create(Text.network_label)
        create(Text.wifi_label)

        self.name_st = text_widgets[0]
        self.model_st = text_widgets[1]
        self.widgets = text_widgets[2:]

        equalize_widths()
        self.hide_widgets = ()
        self.show_widgets = ()
        self.SetSizer(sizer)
        self.SetupScrolling(scroll_x=False, scroll_y=True)
        self.Hide()

    def Show(self, flag=True):
        wx.Panel.Show(self, flag)
        if self.hide_widgets:
            self.show_widgets[0].Show(flag)
            self.show_widgets[1].Show(flag)
            self.hide_widgets[0].Hide()
            self.hide_widgets[1].Hide()
            self.Refresh()
            self.Update()

    def GetValue(self):
        return self.name_ctrl.GetValue()

    def SetValues(self, tv, name=None):
        if name is None:
            self.header1.SetLabel(tv.name)
            self.header2.SetLabel(tv.device_id)
            self.model_ctrl.SetLabel(tv.model)
            self.hide_widgets = (self.name_st, self.name_ctrl)
            self.show_widgets = (self.model_st,  self.model_ctrl)

        else:
            self.header1.SetLabel(tv.model)
            self.header2.SetLabel(tv.device_id)
            self.name_ctrl.SetValue(name)

            self.hide_widgets = (self.model_st,  self.model_ctrl)
            self.show_widgets = (self.name_st, self.name_ctrl)

        for i, label in enumerate((
            str(tv.size) + '"',
            tv.panel_type,
            tv.panel_technology,
            tv.resolution,
            str(tv.year),
            tv.region,
            str(tv.tuner_count),
            str(tv.dtv_support),
            str(tv.pvr_support),
            str(tv.voice_support),
            str(tv.frame_tv_support),
            str(tv.game_pad_support),
            str(tv.firmware_version),
            tv.operating_system,
            tv.network_type,
            tv.wifi_mac
        )):
            self.ctrls[i].SetLabel(label)


class PickerCtrl(wx.SplitterWindow):
    def __init__(self, parent):
        wx.SplitterWindow.__init__(
            self,
            parent,
            -1,
            style=wx.SP_3D,
            size=(500, 300)
        )

        self.found_tvs = {}
        self.event = threading.Event()
        self.empty_panel = wx.Panel(
            self,
            -1,
            style=wx.BORDER_NONE,
            size=(450, 100)
        )

        picker_panel = wx.Panel(self, -1, style=wx.BORDER_NONE)

        self.message_ctrl = wx.StaticText(picker_panel, -1, 'Scanning for devices....')
        message_sizer = wx.BoxSizer(wx.HORIZONTAL)
        picker_sizer = wx.BoxSizer(wx.VERTICAL)
        message_sizer.AddStretchSpacer(1)
        message_sizer.Add(self.message_ctrl, 0, wx.EXPAND | wx.ALL, 10)
        message_sizer.AddStretchSpacer(1)
        picker_sizer.Add(message_sizer, 0, wx.EXPAND)

        self.picker = itemspicker.ItemsPicker(
            picker_panel,
            -1,
            [],
            ipStyle=(
                itemspicker.IP_SORT_CHOICES |
                itemspicker.IP_SORT_SELECTED |
                itemspicker.IP_REMOVE_FROM_CHOICES
            )
        )
        picker_sizer.Add(self.picker, 1, wx.EXPAND)

        picker_panel.SetSizer(picker_sizer)

        self.picker.Bind(
            itemspicker.EVT_IP_SELECTION_CHANGED,
            self.on_selection_changed
        )

        self.SplitHorizontally(picker_panel, self.empty_panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.picker, 0, wx.ALL, 10)
        self.SetSizer(sizer)

        t = threading.Thread(target=self.get_tvs)
        t.daemon = True
        t.start()

    def GetValues(self):
        self.event.set()
        items = self.picker.GetSelections()

        for item in items:
            window, tv = self.found_tvs[item]
            model, device_id = item.rsplit(':', 1)

            if tv is not None:
                config = dict(tv.config)
                config['name'] = item.encode('utf-8')
                config['model'] = model.encode('utf-8')
                SamsungConfig.tv_data[tv.device_id] = config

        for device_id, data in list(SamsungConfig.tv_data.items())[:]:
            if data['model'] + ':' + device_id not in items:
                del(SamsungConfig.tv_data[device_id])

        for window, tv in self.found_tvs.values():
            if tv is not None:
                window.Destroy()

    def get_tvs(self):
        loaded_tvs = []

        add_items = []
        for device_id, value in SamsungConfig.tv_data.items():
            model = value['model']
            name = value['name']
            add_items += [model + ':' + device_id]
            self.found_tvs[model + ':' + device_id] = (name, None)

        self.picker.SetSelections(add_items)

        try:
            while not self.event.isSet():
                for tv in discover():
                    if self.event.isSet():
                        break

                    def do(t):
                        device_id = t.device_id

                        if device_id not in loaded_tvs:
                            loaded_tvs.append(device_id)
                            model = t.model
                            tv_label = model + ':' + device_id

                            data_ctrl = TVDataCtrl(self)
                            data_ctrl.SetValues(t, model)
                            self.found_tvs[tv_label] = (data_ctrl, t)

                            if tv_label in add_items:
                                add_items.remove(tv_label)
                                old_window = self.GetWindow2()
                                old_window.Hide()
                                self.ReplaceWindow(old_window, data_ctrl)
                                data_ctrl.Show()
                            else:
                                items = self.picker.GetItems()
                                self.picker.SetItems(items + [tv_label])

                    wx.CallAfter(do, tv)

                if self.message_ctrl.GetLabel():
                    self.message_ctrl.SetLabel('')

        except wx.PyDeadObjectError:
            pass

    def on_selection_changed(self, evt):
        items = evt.GetItems()

        if items:
            new_window = self.found_tvs[items[0]][0]

            if isinstance(new_window, (str, unicode)):
                new_window = self.empty_panel
        else:
            new_window = self.empty_panel

        old_window = self.GetWindow2()
        old_window.Hide()
        self.ReplaceWindow(old_window, new_window)
        new_window.Show()
        evt.Skip()


class SamsungSmartTVPlus(eg.PluginBase):

    def __init__(self):
        eg.PluginBase.__init__(self)
        self.tvs = {}
        self.AddAction(SetSource)
        self.AddAction(GetSource)
        self.AddAction(GetSources)
        self.AddAction(SetVolume)
        self.AddAction(GetVolume)
        self.AddAction(SetBrightness)
        self.AddAction(GetBrightness)
        self.AddAction(SetContrast)
        self.AddAction(GetContrast)
        self.AddAction(SetSharpness)
        self.AddAction(GetSharpness)
        self.AddAction(SetColorTemperature)
        self.AddAction(GetColorTemperature)
        self.AddAction(SetMute)
        self.AddAction(GetMute)
        self.AddAction(GetPower)
        self.AddAction(GetChannel)
        self.AddAction(GetChannels)
        self.AddAction(RunBrowser)
        self.AddAction(RunApplication)
        self.AddActionsFromList(ACTION)
        self.AddAction(SendKey)
        self.discover_thread = DiscoveryThread(self)
        self.state_thread = StateThread(self, self.tvs)
        for device_id, tv_data in SamsungConfig.tv_data.items():
            if 'model' not in tv_data:
                del SamsungConfig.tv_data[device_id]

    def __start__(self):
        self.discover_thread.start()
        self.state_thread.start()

    def __stop__(self):
        self.discover_thread.stop()
        self.state_thread.stop()

        for tv in self.tvs.values()[:]:
            tv.close()

        self.tvs.clear()

    def Configure(self):
        config_backup = {}
        for key, value in SamsungConfig.tv_data.items():
            backup_data = dict()

            for k, v in value.items():
                backup_data[k] = v

            config_backup[key] = backup_data

        if self.discover_thread.thread is not None:
            self.discover_thread.stop()
            start_discover = True
        else:
            start_discover = False

        if self.state_thread.thread is not None:
            self.state_thread.stop()
            start_state = True
        else:
            start_state = False

        panel = eg.ConfigPanel()
        ctrl = PickerCtrl(panel)
        panel.sizer.Add(ctrl, 1, wx.EXPAND | wx.ALL, 5)

        while panel.Affirmed():
            panel.SetResult()

        last_event = panel.dialog.__dict__['_TaskletDialog__lastEventId']
        ctrl.GetValues()

        if last_event == wx.ID_CANCEL:
            backup_keys = sorted(list(config_backup.keys()))

            for key in backup_keys:
                if key not in SamsungConfig.tv_data:
                    SamsungConfig.tv_data[key] = config_backup[key]

            current_keys = sorted(list(SamsungConfig.tv_data.keys()))
            for key in current_keys:
                if key not in backup_keys:
                    del(SamsungConfig.tv_data[key])

        if start_discover:
            self.discover_thread.start()

        if start_state:
            self.state_thread.start()

    def add_tv(self, tv):
        device_id = tv.device_id

        if device_id in SamsungConfig.tv_data:
            tv_data = SamsungConfig.tv_data[device_id]
            model = tv_data.pop('model')
            tv.name = tv_data['name']

            config = dict(tv.config)
            config['name'] = tv.name
            config['model'] = model
            SamsungConfig.tv_data[tv.device_id] = dict(
                (key, value) for key, value in config.items()
            )
            self.tvs[tv.device_id] = tv
            tv.open()
            eg.PrintNotice('Samsung TV {0} connected.'.format(tv.name))

    def DoCommand(self, cmd, device_id):
        for dev_id, tv in self.tvs.items():
            if device_id in (tv.name, dev_id):
                break
        else:
            eg.PrintNotice('TV {0} not found.'.format(device_id))
            return

        try:
            tv.send(cmd)
        except:
            eg.PrintNotice('TV {0} is not powered on.'.format(tv.name))


class DiscoveryThread(object):

    def __init__(self, plugin):

        self.thread = None
        self.event = threading.Event()
        self.plugin = plugin

    def run(self):
        found_tvs = []

        for device_id, tv_data in SamsungConfig.tv_data.items():
            model = tv_data.pop('model')
            config = Config(**tv_data)
            tv_data['model'] = model
            tvs = list(discover(config))

            if tvs:
                tv = tvs[0]
                self.plugin.add_tv(tv)
                tv.power = True
                found_tvs += [tv.device_id]

        while not self.event.isSet():

            for tv in discover():

                if self.event.isSet():
                    break

                if tv.device_id in found_tvs:
                    continue

                found_tvs += [tv.device_id]
                tv.power = True
                if tv.device_id not in self.plugin.tvs:
                    self.plugin.add_tv(tv)

            for device_id, tv in list(self.plugin.tvs.items())[:]:
                if device_id not in found_tvs:
                    tv.power = False

            del found_tvs[:]

        self.thread = None

    def start(self):
        if self.thread is None:
            self.event.clear()
            self.thread = threading.Thread(target=self.run)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        if self.thread is not None:
            self.event.set()


class StateThread(object):

    def __init__(self, plugin, tvs):
        self.plugin = plugin
        self.tvs = tvs
        self.states = {}
        self.thread = None
        self.event = threading.Event()

    def start(self):
        if self.thread is None:
            self.event.clear()
            self.thread = threading.Thread(target=self.run)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        if self.thread is not None:
            self.event.set()

    def run(self):
        import requests
        from lxml import etree
        while not self.event.isSet():
            for device_id, tv in list(self.tvs.items())[:]:

                if device_id not in self.states:
                    states = dict(
                        brightness=tv.brightness,
                        contrast=tv.contrast,
                        sharpness=tv.sharpness,
                        color_temperature=tv.color_temperature,
                        channel=tv.channel,
                        source=tv.source,
                        power=tv.power,
                        media_info=tv.media_info,
                        track_number=tv.position_info[0],
                        transport_state=tv.transport_info[0],
                        transport_status=tv.transport_info[1],
                        volume=tv.volume,
                        mute=tv.mute
                    )
                    self.states[device_id] = states

                else:
                    states = self.states[device_id]

                    def check_state(attr):
                        new_state = getattr(tv, attr)
                        if states[attr] != new_state:
                            states[attr] = new_state
                            if isinstance(new_state, bool):
                                new_state = 'On' if new_state else 'Off'
                            elif isinstance(new_state, int):
                                new_state = str(new_state)
                            elif not isinstance(new_state, (basestring, dict)):
                                new_state = new_state.label

                            event = attr.replace('_', ' ').title()
                            event = event.replace(' ', '')

                            if not isinstance(new_state, dict):
                                event += '.' + new_state

                            self.plugin.TriggerEvent(
                                tv.name + '.' + event,
                                new_state
                                if isinstance(new_state, dict)
                                else None
                            )
                        return new_state

                    try:

                        if check_state('power'):
                            check_state('brightness')
                            check_state('contrast')
                            check_state('sharpness')
                            check_state('color_temperature')
                            check_state('channel')
                            check_state('source')
                            check_state('media_info')
                            check_state('volume')
                            check_state('mute')

                            transport_state = (
                                tv.transport_info[0]
                            )
                            transport_status = (
                                tv.transport_info[1]
                            )
                            track_number = tv.position_info[0]

                            if states['transport_state'] != transport_state:
                                states['transport_state'] = transport_state
                                self.plugin.TriggerEvent(
                                    tv.name + 'TransportState.' +
                                    transport_state
                                )
                            if states['transport_status'] != transport_status:
                                states['transport_status'] = transport_status
                                self.plugin.TriggerEvent(
                                    tv.name + 'TransportStatus.' +
                                    transport_status
                                )
                            if states['track_number'] != track_number:
                                states['track_number'] = track_number
                                self.plugin.TriggerEvent(
                                    tv.name + 'Track.' + track_number
                                )
                    except (requests.ConnectionError, etree.XMLSyntaxError):
                        tv.power = False

            self.event.wait(0.2)

        self.thread = None


text_widgets = []


def equalize_widths():
    eg.EqualizeWidths(tuple(text_widgets))
    del text_widgets[:]


def h_sizer(s, c):
    t_sizer = wx.BoxSizer(wx.HORIZONTAL)
    t_sizer.Add(s, 0, wx.EXPAND | wx.ALL, 5)
    t_sizer.Add(c, 0, wx.EXPAND | wx.ALL, 5)
    text_widgets.append(s)
    return t_sizer


class TVChoiceCtrl(wx.Panel):

    def __init__(self, parent, value, tvs):
        self.tvs = tvs
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_NONE)
        choices = sorted(list(tv.name for tv in self.tvs.values()))

        choice_st = wx.StaticText(self, -1, Text.tv_label)
        choice_ctrl = wx.Choice(self, -1, choices=choices)

        def set_tv():
            val = choice_ctrl.GetStringSelection()

            for device_id, tv in self.tvs.items():
                if tv.name == val:
                    break
            else:
                return None
            return device_id

        if value in self.tvs:
            tv = self.tvs[value]
            choice_ctrl.SetStringSelection(tv.name)
        else:
            choice_ctrl.SetSelection(0)

        set_tv()

        sizer = wx.BoxSizer(wx.VERTICAL)

        def add(s, c):
            sizer.Add(h_sizer(s, c), 0, wx.EXPAND)

        add(choice_st, choice_ctrl)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)

        def get_string_selection():
            dev_name = choice_ctrl.GetStringSelection()
            for dev_id, tv in self.tvs.items():
                if tv.name == dev_name:
                    return dev_id

        del text_widgets[:]

        self.GetStringSelection = get_string_selection
        self.SetSizer(sizer)


class SetBase(eg.ActionBase):
    _attribute_name = ''

    def __call__(self, value, device_id=None):
        if device_id is None:
            if len(self.plugin.tvs.keys()) > 1:
                self.plugin.PrintError('You need to select a TV first')
                return
            device_id = self.plugin.tvs.keys()[0]

        for dev_id, tv in self.plugin.tvs.items():
            if device_id in (dev_id, tv.name):
                break
        else:
            self.plugin.PrintError('Unable to locate the TV')
            return

        setattr(tv, self._attribute_name, value)

    def Configure(self, value=0, device_id=None):
        panel = eg.ConfigPanel()

        tv_ctrl = TVChoiceCtrl(panel, device_id, self.plugin.tvs)
        label = getattr(Text, self._attribute_name + '_label')

        value_st = panel.StaticText(label + ':')
        value_ctrl = panel.SpinIntCtrl(
            value=value,
            min=0, max=100,
            increment=1
        )

        panel.sizer.Add(tv_ctrl, 0, wx.EXPAND)
        panel.sizer.Add(h_sizer(value_st, value_ctrl), 0, wx.EXPAND)

        del text_widgets[:]

        while panel.Affirmed():
            panel.SetResult(
                value_ctrl.GetValue(),
                tv_ctrl.GetStringSelection()
            )


class GetBase(eg.ActionBase):
    _attribute_name = ''

    def __call__(self, device_id=None):
        if device_id is None:
            if len(self.plugin.tvs.keys()) > 1:
                self.plugin.PrintError('You need to select a TV first')
                return
            device_id = self.plugin.tvs.keys()[0]

        for dev_id, tv in self.plugin.tvs.items():
            if device_id in (dev_id, tv.name):
                break
        else:
            self.plugin.PrintError('Unable to locate the TV')
            return

        return getattr(tv, self._attribute_name)

    def Configure(self, device_id=None):
        panel = eg.ConfigPanel()

        tv_ctrl = TVChoiceCtrl(panel, device_id, self.plugin.tvs)
        panel.sizer.Add(tv_ctrl, 0, wx.EXPAND)

        del text_widgets[:]

        if tv_ctrl.GetStringSelection():
            wx.CallAfter(panel.EnableButtons, True)

        while panel.Affirmed():
            panel.SetResult(
                tv_ctrl.GetStringSelection()
            )


class SetSource(eg.ActionBase):

    def __call__(self, source, device_id=None):
        if device_id is None:
            if len(self.plugin.tvs.keys()) > 1:
                self.plugin.PrintError('You need to select a TV first')
                return
            device_id = self.plugin.tvs.keys()[0]

        for dev_id, tv in self.plugin.tvs.items():
            if device_id in (dev_id, tv.name):
                break
        else:
            self.plugin.PrintError('Unable to locate the TV')
            return

        for src in tv.sources:
            if source in (src.name, src.label, src.device_name):
                if src.is_connected:
                    src.activate()
                else:
                    self.plugin.PrintError(
                        'Source {0} on tv {1} is marked as '
                        'not being connected.'.format(source, tv.name)
                    )

                break
        else:
            self.plugin.PrintError(
                'Unable to locate the source {0} '
                'on tv {1}'.format(source, tv.name)
            )

    def Configure(self, source=None, device_id=None):
        panel = eg.ConfigPanel()

        tv_ctrl = TVChoiceCtrl(panel, device_id, self.plugin.tvs)
        source_st = panel.StaticText(Text.source_label)
        source_ctrl = wx.Choice(panel, -1, choices=[])

        if device_id is None:
            device_id = tv_ctrl.GetStringSelection()

        if device_id is not None and device_id in self.plugin.tvs:
            choices = sorted(
                list(s.label for s in self.plugin.tvs[device_id].sources)
            )
            source_ctrl.AppendItems(choices)
            if source in choices:
                source_ctrl.SetStringSelection(source)
            else:
                source_ctrl.SetSelection(0)

        panel.sizer.Add(tv_ctrl, 0, wx.EXPAND)
        panel.sizer.Add(h_sizer(source_st, source_ctrl), 0, wx.EXPAND)

        def on_choice(evt):
            value = tv_ctrl.GetStringSelection()
            tv = self.plugin.tvs[value]
            source_ctrl.Clear()
            source_ctrl.AppendItems(sorted(list(s.label for s in tv.sources)))
            source_ctrl.SetSelection(0)
            evt.Skip()

        tv_ctrl.Bind(wx.EVT_CHOICE, on_choice)

        del text_widgets[:]

        while panel.Affirmed():
            panel.SetResult(
                source_ctrl.GetStringSelection(),
                tv_ctrl.GetStringSelection()
            )


class GetSource(GetBase):
    _attribute_name = 'source'


class GetSources(GetBase):
    _attribute_name = 'sources'


class SetVolume(SetBase):
    _attribute_name = 'volume'


class GetVolume(GetBase):
    _attribute_name = 'volume'


class SetBrightness(SetBase):
    _attribute_name = 'brightness'


class GetBrightness(GetBase):
    _attribute_name = 'brightness'


class SetContrast(SetBase):
    _attribute_name = 'contrast'


class GetContrast(GetBase):
    _attribute_name = 'contrast'


class SetSharpness(SetBase):
    _attribute_name = 'sharpness'


class GetSharpness(GetBase):
    _attribute_name = 'sharpness'


class SetColorTemperature(SetBase):
    _attribute_name = 'color_temperature'


class GetColorTemperature(GetBase):
    _attribute_name = 'color_temperature'


class SetMute(eg.ActionBase):
    def __call__(self, mute, device_id=None):
        if device_id is None:
            if len(self.plugin.tvs.keys()) > 1:
                self.plugin.PrintError('You need to select a TV first')
                return
            device_id = self.plugin.tvs.keys()[0]

        for dev_id, tv in self.plugin.tvs.items():
            if device_id in (dev_id, tv.name):
                break
        else:
            self.plugin.PrintError('Unable to locate the TV')
            return

        tv.mute = mute

    def Configure(self, mute=False, device_id=None):
        panel = eg.ConfigPanel()

        tv_ctrl = TVChoiceCtrl(panel, device_id, self.plugin.tvs)

        mute_st = panel.StaticText(Text.mute_label)
        mute_ctrl = wx.Choice(panel, -1, choices=['Off', 'On'])

        mute_ctrl.SetSelection(int(mute))

        panel.sizer.Add(tv_ctrl, 0, wx.EXPAND)
        panel.sizer.Add(h_sizer(mute_st, mute_ctrl), 0, wx.EXPAND)

        del text_widgets[:]

        while panel.Affirmed():
            panel.SetResult(
                bool(mute_ctrl.GetSelection()),
                tv_ctrl.GetStringSelection()
            )


class GetMute(GetBase):
    _attribute_name = 'mute'


class GetPower(GetBase):
    _attribute_name = 'power'


class GetChannel(GetBase):
    _attribute_name = 'channel'


class GetChannels(GetBase):
    _attribute_name = 'channels'


class RunBrowser(eg.ActionBase):
    def __call__(self, url, device_id=None):
        if device_id is None:
            if len(self.plugin.tvs.keys()) > 1:
                self.plugin.PrintError('You need to select a TV first')
                return
            device_id = self.plugin.tvs.keys()[0]

        for dev_id, tv in self.plugin.tvs.items():
            if device_id in (dev_id, tv.name):
                break
        else:
            self.plugin.PrintError('Unable to locate the TV')
            return

        tv.run_browser(url)

    def Configure(self, url='', device_id=None):
        panel = eg.ConfigPanel()

        tv_ctrl = TVChoiceCtrl(panel, device_id, self.plugin.tvs)
        url_st = panel.StaticText(Text.url_label)
        url_ctrl = panel.TextCtrl(url)

        panel.sizer.Add(tv_ctrl, 0, wx.EXPAND)
        panel.sizer.Add(h_sizer(url_st, url_ctrl), 0, wx.EXPAND)

        del text_widgets[:]

        while panel.Affirmed():
            panel.SetResult(
                url_ctrl.GetValue(),
                tv_ctrl.GetStringSelection()
            )


class RunApplication(eg.ActionBase):
    def __call__(self, app, device_id=None):
        if device_id is None:
            if len(self.plugin.tvs.keys()) > 1:
                self.plugin.PrintError('You need to select a TV first')
                return
            device_id = self.plugin.tvs.keys()[0]

        for dev_id, tv in self.plugin.tvs.items():
            if device_id in (dev_id, tv.name):
                break
        else:
            self.plugin.PrintError('Unable to locate the TV')
            return

        tv.run_application(app)

    def Configure(self, app='', device_id=None):
        panel = eg.ConfigPanel()

        tv_ctrl = TVChoiceCtrl(panel, device_id, self.plugin.tvs)
        app_st = panel.StaticText(Text.app_label)
        app_ctrl = panel.TextCtrl(app)

        panel.sizer.Add(tv_ctrl, 0, wx.EXPAND)
        panel.sizer.Add(h_sizer(app_st, app_ctrl), 0, wx.EXPAND)

        del text_widgets[:]

        while panel.Affirmed():
            panel.SetResult(
                app_ctrl.GetValue(),
                tv_ctrl.GetStringSelection()
            )


class SendKey(eg.ActionBase):

    def __call__(self, cmd=None, device_id=None):
        if device_id is None:
            if len(self.plugin.tvs.keys()) > 1:
                self.plugin.PrintError('You need to select a TV first')
                return False
            device_id = self.plugin.tvs.keys()[0]

        if cmd is None:
            if not hasattr(self, 'value'):
                self.plugin.PrintError('You need to select a key to send')
                return False
            cmd = self.value

        self.plugin.DoCommand(cmd, device_id)

    def Configure(self, cmd='', device_id=''):
        panel = eg.ConfigPanel()

        tv_ctrl = TVChoiceCtrl(panel, device_id, self.plugin.tvs)
        panel.sizer.Add(tv_ctrl, 0, wx.EXPAND)

        commands = []
        for group in ACTION:
            for key in group[4]:
                commands += [key[-2:]]

        if hasattr(self, 'value'):
            class CommandCtrl(object):
                def __init__(self, value):
                    self.value = value

                def GetStringSelection(self):
                    return self.value


            for com, value in commands:
                if value == self.value:
                    break
            else:
                com = ''

            cmd_ctrl = CommandCtrl(com)

        else:
            cmd_st = panel.StaticText(Text.key_label)
            cmd_ctrl = wx.Choice(
                panel,
                -1,
                choices=list(c[0] for c in commands)
            )

            for cmd_name, cmd_value in commands:
                if cmd_value == cmd:
                    cmd_ctrl.SetStringSelection(cmd_name)
                    break
            else:
                cmd_ctrl.SetSelection(0)

            panel.sizer.Add(h_sizer(cmd_st, cmd_ctrl), 0, wx.EXPAND)

        wx.CallAfter(panel.EnableButtons, True)

        del text_widgets[:]

        while panel.Affirmed():
            v = cmd_ctrl.GetStringSelection()
            for cmd_name, cmd in commands:
                if cmd_name == v:
                    break
            else:
                cmd = None

            panel.SetResult(cmd, tv_ctrl.GetStringSelection())

ACTION = (
    (
        eg.ActionGroup, 'Power', 'Power Keys', 'Power Keys ', (
            (SendKey, 'fnKEY_POWEROFF', 'Power OFF', 'Power OFF', 'KEY_POWEROFF'),
            (SendKey, 'fnKEY_POWERON', 'Power On', 'Power On', 'KEY_POWERON'),
            (SendKey, 'fnKEY_POWER', 'Alternate Power', 'Power Toggle', 'KEY_POWER')
        )
    ),
    (
        eg.ActionGroup, 'Input', 'Input Keys', 'Input Keys ', (
            (SendKey, 'fnKEY_SOURCE', 'Source', 'Source', 'KEY_SOURCE'),
            (SendKey, 'fnKEY_COMPONENT1', 'Component 1', 'Component 1', 'KEY_COMPONENT1'),
            (SendKey, 'fnKEY_COMPONENT2', 'Component 2', 'Component 2', 'KEY_COMPONENT2'),
            (SendKey, 'fnKEY_AV1', 'AV 1', 'AV 1', 'KEY_AV1'),
            (SendKey, 'fnKEY_AV2', 'AV 2', 'AV 2', 'KEY_AV2'),
            (SendKey, 'fnKEY_AV3', 'AV 3', 'AV 3', 'KEY_AV3'),
            (SendKey, 'fnKEY_SVIDEO1', 'S Video 1', 'S Video 1', 'KEY_SVIDEO1'),
            (SendKey, 'fnKEY_SVIDEO2', 'S Video 2', 'S Video 2', 'KEY_SVIDEO2'),
            (SendKey, 'fnKEY_SVIDEO3', 'S Video 3', 'S Video 3', 'KEY_SVIDEO3'),
            (SendKey, 'fnKEY_HDMI', 'HDMI', 'HDMI', 'KEY_HDMI'),
            (SendKey, 'fnKEY_HDMI1', 'HDMI 1', 'HDMI 1', 'KEY_HDMI1'),
            (SendKey, 'fnKEY_HDMI2', 'HDMI 2', 'HDMI 2', 'KEY_HDMI2'),
            (SendKey, 'fnKEY_HDMI3', 'HDMI 3', 'HDMI 3', 'KEY_HDMI3'),
            (SendKey, 'fnKEY_HDMI4', 'HDMI 4', 'HDMI 4', 'KEY_HDMI4'),
            (SendKey, 'fnKEY_FM_RADIO', 'FM Radio', 'FM Radio', 'KEY_FM_RADIO'),
            (SendKey, 'fnKEY_DVI', 'DVI', 'DVI', 'KEY_DVI'),
            (SendKey, 'fnKEY_DVR', 'DVR', 'DVR', 'KEY_DVR'),
            (SendKey, 'fnKEY_TV', 'TV', 'TV', 'KEY_TV'),
            (SendKey, 'fnKEY_ANTENA', 'Analog TV', 'Analog TV', 'KEY_ANTENA'),
            (SendKey, 'fnKEY_DTV', 'Digital TV', 'Digital TV', 'KEY_DTV')
        )
    ),
    (
        eg.ActionGroup, 'Numbers', 'Number Keys', 'Number Keys ', (
            (SendKey, 'fnKEY_1', 'Key1', 'Key1', 'KEY_1'),
            (SendKey, 'fnKEY_2', 'Key2', 'Key2', 'KEY_2'),
            (SendKey, 'fnKEY_3', 'Key3', 'Key3', 'KEY_3'),
            (SendKey, 'fnKEY_4', 'Key4', 'Key4', 'KEY_4'),
            (SendKey, 'fnKEY_5', 'Key5', 'Key5', 'KEY_5'),
            (SendKey, 'fnKEY_6', 'Key6', 'Key6', 'KEY_6'),
            (SendKey, 'fnKEY_7', 'Key7', 'Key7', 'KEY_7'),
            (SendKey, 'fnKEY_8', 'Key8', 'Key8', 'KEY_8'),
            (SendKey, 'fnKEY_9', 'Key9', 'Key9', 'KEY_9'),
            (SendKey, 'fnKEY_0', 'Key0', 'Key0', 'KEY_0')
        )
    ),
    (
        eg.ActionGroup, 'Misc', 'Misc Keys', 'Misc Keys ', (
            (SendKey, 'fnKEY_PANNEL_CHDOWN', '3D', '3D', 'KEY_PANNEL_CHDOWN'),
            (SendKey, 'fnKEY_ANYNET', 'AnyNet+', 'AnyNet+', 'KEY_ANYNET'),
            (SendKey, 'fnKEY_ESAVING', 'Energy Saving', 'Energy Saving', 'KEY_ESAVING'),
            (SendKey, 'fnKEY_SLEEP', 'Sleep Timer', 'Sleep Timer', 'KEY_SLEEP'),
            (SendKey, 'fnKEY_DTV_SIGNAL', 'DTV Signal', 'DTV Signal', 'KEY_DTV_SIGNAL')

        )
    ),
    (
        eg.ActionGroup, 'Channel', 'Channel Keys', 'Channel Keys ', (
            (SendKey, 'fnKEY_CHUP', 'ChannelUp', 'ChannelUp', 'KEY_CHUP'),
            (SendKey, 'fnKEY_CHDOWN', 'ChannelDown', 'ChannelDown', 'KEY_CHDOWN'),
            (SendKey, 'fnKEY_PRECH', 'Previous Channel', 'Previous Channel', 'KEY_PRECH'),
            (SendKey, 'fnKEY_FAVCH', 'Favorite Channels', 'Favorite Channels', 'KEY_FAVCH'),
            (SendKey, 'fnKEY_CH_LIST', 'Channel List', 'Channel List', 'KEY_CH_LIST'),
            (SendKey, 'fnKEY_AUTO_PROGRAM', 'Auto Program', 'Auto Program', 'KEY_AUTO_PROGRAM'),
            (SendKey, 'fnKEY_MAGIC_CHANNEL', 'Magic Channel', 'Magic Channel', 'KEY_MAGIC_CHANNEL'),
        )
    ),
    (
        eg.ActionGroup, 'Volume', 'Volume Keys', 'Volume Keys ', (
            (SendKey, 'fnKEY_VOLUP', 'VolUp', 'VolUp', 'KEY_VOLUP'),
            (SendKey, 'fnKEY_VOLDOWN', 'VolDown', 'VolDown', 'KEY_VOLDOWN'),
            (SendKey, 'fnKEY_MUTE', 'Mute', 'Mute', 'KEY_MUTE')
        )
    ),
    (
        eg.ActionGroup, 'Direction', 'Direction Keys', 'Direction Keys ', (
            (SendKey, 'fnKEY_UP', 'Up', 'Up', 'KEY_UP'),
            (SendKey, 'fnKEY_DOWN', 'Down', 'Down', 'KEY_DOWN'),
            (SendKey, 'fnKEY_LEFT', 'Left', 'Left', 'KEY_LEFT'),
            (SendKey, 'fnKEY_RIGHT', 'Right', 'Right', 'KEY_RIGHT'),
            (SendKey, 'fnKEY_RETURN', 'Return', 'Return', 'KEY_RETURN'),
            (SendKey, 'fnKEY_ENTER', 'Enter', 'Enter', 'KEY_ENTER')
        )
    ),
    (
        eg.ActionGroup, 'Media', 'Media Keys', 'Media Keys ', (
            (SendKey, 'fnKEY_REWIND', 'Rewind', 'Rewind', 'KEY_REWIND'),
            (SendKey, 'fnKEY_STOP', 'Stop', 'Stop', 'KEY_STOP'),
            (SendKey, 'fnKEY_PLAY', 'Play', 'Play', 'KEY_PLAY'),
            (SendKey, 'fnKEY_FF', 'FastForward', 'FastForward', 'KEY_FF'),
            (SendKey, 'fnKEY_REC', 'Record', 'Record', 'KEY_REC'),
            (SendKey, 'fnKEY_PAUSE', 'Pause', 'Pause', 'KEY_PAUSE'),
            (SendKey, 'fnKEY_LIVE', 'Live', 'Live', 'KEY_LIVE'),
            (SendKey, 'fnKEY_QUICK_REPLAY', 'Quick Replay', 'Quick Replay', 'KEY_QUICK_REPLAY'),
            (SendKey, 'fnKEY_STILL_PICTURE', 'Still Picture', 'Still Picture', 'KEY_STILL_PICTURE'),
            (SendKey, 'fnKEY_INSTANT_REPLAY', 'Instant Replay', 'Instant Replay', 'KEY_INSTANT_REPLAY')
        )
    ),
    (
        eg.ActionGroup, 'PIP', 'Picture in Picture', 'Picture in Picture ', (
            (SendKey, 'fnKEY_PIP_ONOFF', 'PIP On/Off', 'PIP On/Off', 'KEY_PIP_ONOFF'),
            (SendKey, 'fnKEY_PIP_SWAP', 'PIP Swap', 'PIP Swap', 'KEY_PIP_SWAP'),
            (SendKey, 'fnKEY_PIP_SIZE', 'PIP Size', 'PIP Size', 'KEY_PIP_SIZE'),
            (SendKey, 'fnKEY_PIP_CHUP', 'PIP Channel Up', 'PIP Channel Up', 'KEY_PIP_CHUP'),
            (SendKey, 'fnKEY_PIP_CHDOWN', 'PIP Channel Down', 'PIP Channel Down', 'KEY_PIP_CHDOWN'),
            (SendKey, 'fnKEY_AUTO_ARC_PIP_SMALL', 'PIP Small', 'PIP Small', 'KEY_AUTO_ARC_PIP_SMALL'),
            (SendKey, 'fnKEY_AUTO_ARC_PIP_WIDE', 'PIP Wide', 'PIP Wide', 'KEY_AUTO_ARC_PIP_WIDE'),
            (SendKey, 'fnKEY_AUTO_ARC_PIP_RIGHT_BOTTOM', 'PIP Bottom Right', 'PIP Bottom Right', 'KEY_AUTO_ARC_PIP_RIGHT_BOTTOM'),
            (SendKey, 'fnKEY_AUTO_ARC_PIP_SOURCE_CHANGE', 'PIP Source Change', 'PIP Source Change', 'KEY_AUTO_ARC_PIP_SOURCE_CHANGE'),
            (SendKey, 'fnKEY_PIP_SCAN', 'PIP Scan', 'PIP Scan', 'KEY_PIP_SCAN')
        )
    ),
    (
        eg.ActionGroup, 'Modes', 'Modes', 'Modes ', (
            (SendKey, 'fnKEY_VCR_MODE', 'VCR Mode', 'VCR Mode', 'KEY_VCR_MODE'),
            (SendKey, 'fnKEY_CATV_MODE', 'CATV Mode', 'CATV Mode', 'KEY_CATV_MODE'),
            (SendKey, 'fnKEY_DSS_MODE', 'DSS Mode', 'DSS Mode', 'KEY_DSS_MODE'),
            (SendKey, 'fnKEY_TV_MODE', 'TV Mode', 'TV Mode', 'KEY_TV_MODE'),
            (SendKey, 'fnKEY_DVD_MODE', 'DVD Mode', 'DVD Mode', 'KEY_DVD_MODE'),
            (SendKey, 'fnKEY_STB_MODE', 'STB Mode', 'STB Mode', 'KEY_STB_MODE'),
            (SendKey, 'fnKEY_PCMODE', 'PC Mode', 'PC Mode', 'KEY_PCMODE')
        )
    ),
    (
        eg.ActionGroup, 'Colors', 'Color Keys', 'Color Keys ', (
            (SendKey, 'fnKEY_GREEN', 'Green', 'Green', 'KEY_GREEN'),
            (SendKey, 'fnKEY_YELLOW', 'Yellow', 'Yellow', 'KEY_YELLOW'),
            (SendKey, 'fnKEY_CYAN', 'Cyan', 'Cyan', 'KEY_CYAN'),
            (SendKey, 'fnKEY_RED', 'Red', 'Red', 'KEY_RED')
        )
    ),
    (
        eg.ActionGroup, 'Teletext', 'Teletext', 'Teletext ', (
            (SendKey, 'fnKEY_TTX_MIX', 'Teletext Mix', 'Teletext Mix', 'KEY_TTX_MIX'),
            (SendKey, 'fnKEY_TTX_SUBFACE', 'Teletext Subface', 'Teletext Subface', 'KEY_TTX_SUBFACE')
        )
    ),
    (
        eg.ActionGroup, 'AspectRatio', 'Aspect Ratio', 'Aspect Ratio ', (
            (SendKey, 'fnKEY_ASPECT', 'Aspect Ratio', 'Aspect Ratio', 'KEY_ASPECT'),
            (SendKey, 'fnKEY_PICTURE_SIZE', 'Picture Size', 'Picture Size', 'KEY_PICTURE_SIZE'),
            (SendKey, 'fnKEY_4_3', 'Aspect Ratio 4:3', 'Aspect Ratio 4:3', 'KEY_4_3'),
            (SendKey, 'fnKEY_16_9', 'Aspect Ratio 16:9', 'Aspect Ratio 16:9', 'KEY_16_9'),
            (SendKey, 'fnKEY_EXT14', 'Aspect Ratio 3:4 (Alternate)', 'Aspect Ratio 3:4 (Alternate)', 'KEY_EXT14'),
            (SendKey, 'fnKEY_EXT15', 'Aspect Ratio 16:9 (Alternate)', 'Aspect Ratio 16:9 (Alternate)', 'KEY_EXT15')

        )
    ),
    (
        eg.ActionGroup, 'PictureMode', 'Picture Mode', 'Picture Mode ', (
            (SendKey, 'fnKEY_PMODE', 'Picture Mode', 'Picture Mode', 'KEY_PMODE'),
            (SendKey, 'fnKEY_PANORAMA', 'Picture Mode Panorama', 'Picture Mode Panorama', 'KEY_PANORAMA'),
            (SendKey, 'fnKEY_DYNAMIC', 'Picture Mode Dynamic', 'Picture Mode Dynamic', 'KEY_DYNAMIC'),
            (SendKey, 'fnKEY_STANDARD', 'Picture Mode Standard', 'Picture Mode Standard', 'KEY_STANDARD'),
            (SendKey, 'fnKEY_MOVIE1', 'Picture Mode Movie', 'Picture Mode Movie', 'KEY_MOVIE1'),
            (SendKey, 'fnKEY_GAME', 'Picture Mode Game', 'Picture Mode Game', 'KEY_GAME'),
            (SendKey, 'fnKEY_CUSTOM', 'Picture Mode Custom', 'Picture Mode Custom', 'KEY_CUSTOM'),
            (SendKey, 'fnKEY_EXT9', 'Picture Mode Movie (Alternate)', 'Picture Mode Movie (Alternate)', 'KEY_EXT9'),
            (SendKey, 'fnKEY_EXT10', 'Picture Mode Standard (Alternate)', 'Picture Mode Standard (Alternate)', 'KEY_EXT10')
        )
    ),
    (
        eg.ActionGroup, 'Menus', 'Menus', 'Menus ', (
            (SendKey, 'fnKEY_MENU', 'Menu', 'Menu', 'KEY_MENU'),
            (SendKey, 'fnKEY_TOPMENU', 'Top Menu', 'Top Menu', 'KEY_TOPMENU'),
            (SendKey, 'fnKEY_TOOLS', 'Tools', 'Tools', 'KEY_TOOLS'),
            (SendKey, 'fnKEY_HOME', 'Home', 'Home', 'KEY_HOME'),
            (SendKey, 'fnKEY_CONTENTS', 'Contents', 'Contents', 'KEY_CONTENTS'),
            (SendKey, 'fnKEY_GUIDE', 'Guide', 'Guide', 'KEY_GUIDE'),
            (SendKey, 'fnKEY_DISC_MENU', 'Disc Menu', 'Disc Menu', 'KEY_DISC_MENU'),
            (SendKey, 'fnKEY_DVR_MENU', 'DVR Menu', 'DVR Menu', 'KEY_DVR_MENU'),
            (SendKey, 'fnKEY_HELP', 'Help', 'Help', 'KEY_HELP')
        )
    ),
    (
        eg.ActionGroup, 'OSD', 'OSD', 'OSD ', (
            (SendKey, 'fnKEY_INFO', 'Info', 'Info', 'KEY_INFO'),
            (SendKey, 'fnKEY_CAPTION', 'Caption', 'Caption', 'KEY_CAPTION'),
            (SendKey, 'fnKEY_CLOCK_DISPLAY', 'ClockDisplay', 'ClockDisplay', 'KEY_CLOCK_DISPLAY'),
            (SendKey, 'fnKEY_SETUP_CLOCK_TIMER', 'Setup Clock', 'Setup Clock', 'KEY_SETUP_CLOCK_TIMER'),
            (SendKey, 'fnKEY_SUB_TITLE', 'Subtitle', 'Subtitle', 'KEY_SUB_TITLE'),
        )
    ),
    (
        eg.ActionGroup, 'Zoom', 'Zoom', 'Zoom ', (
            (SendKey, 'fnKEY_ZOOM_MOVE', 'Zoom Move', 'Zoom Move', 'KEY_ZOOM_MOVE'),
            (SendKey, 'fnKEY_ZOOM_IN', 'Zoom In', 'Zoom In', 'KEY_ZOOM_IN'),
            (SendKey, 'fnKEY_ZOOM_OUT', 'Zoom Out', 'Zoom Out', 'KEY_ZOOM_OUT'),
            (SendKey, 'fnKEY_ZOOM1', 'Zoom 1', 'Zoom 1', 'KEY_ZOOM1'),
            (SendKey, 'fnKEY_ZOOM2', 'Zoom 2', 'Zoom 2', 'KEY_ZOOM2')
        )
    ),
    (
        eg.ActionGroup, 'Other', 'Other Keys', 'Other Keys ', (
            (SendKey, 'fnKEY_WHEEL_LEFT', 'Wheel Left', 'Wheel Left', 'KEY_WHEEL_LEFT'),
            (SendKey, 'fnKEY_WHEEL_RIGHT', 'Wheel Right', 'Wheel Right', 'KEY_WHEEL_RIGHT'),
            (SendKey, 'fnKEY_ADDDEL', 'Add/Del', 'Add/Del', 'KEY_ADDDEL'),
            (SendKey, 'fnKEY_PLUS100', 'Plus 100', 'Plus 100', 'KEY_PLUS100'),
            (SendKey, 'fnKEY_AD', 'AD', 'AD', 'KEY_AD'),
            (SendKey, 'fnKEY_LINK', 'Link', 'Link', 'KEY_LINK'),
            (SendKey, 'fnKEY_TURBO', 'Turbo', 'Turbo', 'KEY_TURBO'),
            (SendKey, 'fnKEY_CONVERGENCE', 'Convergence', 'Convergence', 'KEY_CONVERGENCE'),
            (SendKey, 'fnKEY_DEVICE_CONNECT', 'Device Connect', 'Device Connect', 'KEY_DEVICE_CONNECT'),
            (SendKey, 'fnKEY_11', 'Key 11', 'Key 11', 'KEY_11'),
            (SendKey, 'fnKEY_12', 'Key 12', 'Key 12', 'KEY_12'),
            (SendKey, 'fnKEY_FACTORY', 'Key Factory', 'Key Factory', 'KEY_FACTORY'),
            (SendKey, 'fnKEY_3SPEED', 'Key 3SPEED', 'Key 3SPEED', 'KEY_3SPEED'),
            (SendKey, 'fnKEY_RSURF', 'Key RSURF', 'Key RSURF', 'KEY_RSURF'),
            (SendKey, 'fnKEY_FF_', 'FF_', 'FF_', 'KEY_FF_'),
            (SendKey, 'fnKEY_REWIND_', 'REWIND_', 'REWIND_', 'KEY_REWIND_'),
            (SendKey, 'fnKEY_ANGLE', 'Angle', 'Angle', 'KEY_ANGLE'),
            (SendKey, 'fnKEY_RESERVED1', 'Reserved 1', 'Reserved 1', 'KEY_RESERVED1'),
            (SendKey, 'fnKEY_PROGRAM', 'Program', 'Program', 'KEY_PROGRAM'),
            (SendKey, 'fnKEY_BOOKMARK', 'Bookmark', 'Bookmark', 'KEY_BOOKMARK'),
            (SendKey, 'fnKEY_PRINT', 'Print', 'Print', 'KEY_PRINT'),
            (SendKey, 'fnKEY_CLEAR', 'Clear', 'Clear', 'KEY_CLEAR'),
            (SendKey, 'fnKEY_VCHIP', 'V Chip', 'V Chip', 'KEY_VCHIP'),
            (SendKey, 'fnKEY_REPEAT', 'Repeat', 'Repeat', 'KEY_REPEAT'),
            (SendKey, 'fnKEY_DOOR', 'Door', 'Door', 'KEY_DOOR'),
            (SendKey, 'fnKEY_OPEN', 'Open', 'Open', 'KEY_OPEN'),
            (SendKey, 'fnKEY_DMA', 'DMA', 'DMA', 'KEY_DMA'),
            (SendKey, 'fnKEY_MTS', 'MTS', 'MTS', 'KEY_MTS'),
            (SendKey, 'fnKEY_DNIe', 'DNIe', 'DNIe', 'KEY_DNIe'),
            (SendKey, 'fnKEY_SRS', 'SRS', 'SRS', 'KEY_SRS'),
            (SendKey, 'fnKEY_CONVERT_AUDIO_MAINSUB', 'Convert Audio Main/Sub', 'Convert Audio Main/Sub', 'KEY_CONVERT_AUDIO_MAINSUB'),
            (SendKey, 'fnKEY_MDC', 'MDC', 'MDC', 'KEY_MDC'),
            (SendKey, 'fnKEY_SEFFECT', 'Sound Effect', 'Sound Effect', 'KEY_SEFFECT'),
            (SendKey, 'fnKEY_PERPECT_FOCUS', 'PERPECT Focus','PERPECT Focus', 'KEY_PERPECT_FOCUS'),
            (SendKey, 'fnKEY_CALLER_ID', 'Caller ID', 'Caller ID', 'KEY_CALLER_ID'),
            (SendKey, 'fnKEY_SCALE', 'Scale', 'Scale', 'KEY_SCALE'),
            (SendKey, 'fnKEY_MAGIC_BRIGHT', 'Magic Bright', 'Magic Bright', 'KEY_MAGIC_BRIGHT'),
            (SendKey, 'fnKEY_W_LINK', 'W Link', 'W Link', 'KEY_W_LINK'),
            (SendKey, 'fnKEY_DTV_LINK', 'DTV Link', 'DTV Link', 'KEY_DTV_LINK'),
            (SendKey, 'fnKEY_APP_LIST', 'Application List', 'Application List', 'KEY_APP_LIST'),
            (SendKey, 'fnKEY_BACK_MHP', 'Back MHP', 'Back MHP', 'KEY_BACK_MHP'),
            (SendKey, 'fnKEY_ALT_MHP', 'Alternate MHP', 'Alternate MHP', 'KEY_ALT_MHP'),
            (SendKey, 'fnKEY_DNSe', 'DNSe', 'DNSe', 'KEY_DNSe'),
            (SendKey, 'fnKEY_RSS', 'RSS', 'RSS', 'KEY_RSS'),
            (SendKey, 'fnKEY_ENTERTAINMENT', 'Entertainment', 'Entertainment', 'KEY_ENTERTAINMENT'),
            (SendKey, 'fnKEY_ID_INPUT', 'ID Input', 'ID Input', 'KEY_ID_INPUT'),
            (SendKey, 'fnKEY_ID_SETUP', 'ID Setup', 'ID Setup', 'KEY_ID_SETUP'),
            (SendKey, 'fnKEY_ANYVIEW', 'Any View', 'Any View', 'KEY_ANYVIEW'),
            (SendKey, 'fnKEY_MS', 'MS', 'MS', 'KEY_MS'),
            (SendKey, 'fnKEY_MORE', 'KEY_MORE', 'KEY_MORE', 'KEY_MORE'),
            (SendKey, 'fnKEY_MIC', 'KEY_MIC', 'KEY_MIC', 'KEY_MIC'),
            (SendKey, 'fnKEY_NINE_SEPERATE', 'KEY_NINE_SEPERATE', 'KEY_NINE_SEPERATE', 'KEY_NINE_SEPERATE'),
            (SendKey, 'fnKEY_AUTO_FORMAT', 'Auto Format', 'Auto Format', 'KEY_AUTO_FORMAT'),
            (SendKey, 'fnKEY_DNET', 'DNET', 'DNET', 'KEY_DNET')
        )
    ),
    (
        eg.ActionGroup, 'AutoArcKeys', 'Auto Arc Keys', 'Auto Arc Keys ', (
            (SendKey, 'fnKEY_AUTO_ARC_C_FORCE_AGING', 'KEY_AUTO_ARC_C_FORCE_AGING', 'KEY_AUTO_ARC_C_FORCE_AGING', 'KEY_AUTO_ARC_C_FORCE_AGING'),
            (SendKey, 'fnKEY_AUTO_ARC_CAPTION_ENG', 'KEY_AUTO_ARC_CAPTION_ENG', 'KEY_AUTO_ARC_CAPTION_ENG', 'KEY_AUTO_ARC_CAPTION_ENG'),
            (SendKey, 'fnKEY_AUTO_ARC_USBJACK_INSPECT', 'KEY_AUTO_ARC_USBJACK_INSPECT', 'KEY_AUTO_ARC_USBJACK_INSPECT', 'KEY_AUTO_ARC_USBJACK_INSPECT'),
            (SendKey, 'fnKEY_AUTO_ARC_RESET', 'KEY_AUTO_ARC_RESET', 'KEY_AUTO_ARC_RESET', 'KEY_AUTO_ARC_RESET'),
            (SendKey, 'fnKEY_AUTO_ARC_LNA_ON', 'KEY_AUTO_ARC_LNA_ON', 'KEY_AUTO_ARC_LNA_ON', 'KEY_AUTO_ARC_LNA_ON'),
            (SendKey, 'fnKEY_AUTO_ARC_LNA_OFF', 'KEY_AUTO_ARC_LNA_OFF', 'KEY_AUTO_ARC_LNA_OFF', 'KEY_AUTO_ARC_LNA_OFF'),
            (SendKey, 'fnKEY_AUTO_ARC_ANYNET_MODE_OK', 'KEY_AUTO_ARC_ANYNET_MODE_OK', 'KEY_AUTO_ARC_ANYNET_MODE_OK', 'KEY_AUTO_ARC_ANYNET_MODE_OK'),
            (SendKey, 'fnKEY_AUTO_ARC_ANYNET_AUTO_START', 'KEY_AUTO_ARC_ANYNET_AUTO_START', 'KEY_AUTO_ARC_ANYNET_AUTO_START', 'KEY_AUTO_ARC_ANYNET_AUTO_START'),
            (SendKey, 'fnKEY_AUTO_ARC_CAPTION_ON', 'KEY_AUTO_ARC_CAPTION_ON', 'KEY_AUTO_ARC_CAPTION_ON', 'KEY_AUTO_ARC_CAPTION_ON'),
            (SendKey, 'fnKEY_AUTO_ARC_CAPTION_OFF', 'KEY_AUTO_ARC_CAPTION_OFF', 'KEY_AUTO_ARC_CAPTION_OFF', 'KEY_AUTO_ARC_CAPTION_OFF'),
            (SendKey, 'fnKEY_AUTO_ARC_PIP_DOUBLE', 'KEY_AUTO_ARC_PIP_DOUBLE', 'KEY_AUTO_ARC_PIP_DOUBLE', 'KEY_AUTO_ARC_PIP_DOUBLE'),
            (SendKey, 'fnKEY_AUTO_ARC_PIP_LARGE', 'KEY_AUTO_ARC_PIP_LARGE', 'KEY_AUTO_ARC_PIP_LARGE', 'KEY_AUTO_ARC_PIP_LARGE'),
            (SendKey, 'fnKEY_AUTO_ARC_PIP_LEFT_TOP', 'KEY_AUTO_ARC_PIP_LEFT_TOP', 'KEY_AUTO_ARC_PIP_LEFT_TOP', 'KEY_AUTO_ARC_PIP_LEFT_TOP'),
            (SendKey, 'fnKEY_AUTO_ARC_PIP_RIGHT_TOP', 'KEY_AUTO_ARC_PIP_RIGHT_TOP', 'KEY_AUTO_ARC_PIP_RIGHT_TOP', 'KEY_AUTO_ARC_PIP_RIGHT_TOP'),
            (SendKey, 'fnKEY_AUTO_ARC_PIP_LEFT_BOTTOM', 'KEY_AUTO_ARC_PIP_LEFT_BOTTOM', 'KEY_AUTO_ARC_PIP_LEFT_BOTTOM', 'KEY_AUTO_ARC_PIP_LEFT_BOTTOM'),
            (SendKey, 'fnKEY_AUTO_ARC_PIP_CH_CHANGE', 'KEY_AUTO_ARC_PIP_CH_CHANGE', 'KEY_AUTO_ARC_PIP_CH_CHANGE', 'KEY_AUTO_ARC_PIP_CH_CHANGE'),
            (SendKey, 'fnKEY_AUTO_ARC_AUTOCOLOR_SUCCESS', 'KEY_AUTO_ARC_AUTOCOLOR_SUCCESS', 'KEY_AUTO_ARC_AUTOCOLOR_SUCCESS', 'KEY_AUTO_ARC_AUTOCOLOR_SUCCESS'),
            (SendKey, 'fnKEY_AUTO_ARC_AUTOCOLOR_FAIL', 'KEY_AUTO_ARC_AUTOCOLOR_FAIL', 'KEY_AUTO_ARC_AUTOCOLOR_FAIL', 'KEY_AUTO_ARC_AUTOCOLOR_FAIL'),
            (SendKey, 'fnKEY_AUTO_ARC_JACK_IDENT', 'KEY_AUTO_ARC_JACK_IDENT', 'KEY_AUTO_ARC_JACK_IDENT', 'KEY_AUTO_ARC_JACK_IDENT'),
            (SendKey, 'fnKEY_AUTO_ARC_CAPTION_KOR', 'KEY_AUTO_ARC_CAPTION_KOR', 'KEY_AUTO_ARC_CAPTION_KOR', 'KEY_AUTO_ARC_CAPTION_KOR'),
            (SendKey, 'fnKEY_AUTO_ARC_ANTENNA_AIR', 'KEY_AUTO_ARC_ANTENNA_AIR', 'KEY_AUTO_ARC_ANTENNA_AIR', 'KEY_AUTO_ARC_ANTENNA_AIR'),
            (SendKey, 'fnKEY_AUTO_ARC_ANTENNA_CABLE', 'KEY_AUTO_ARC_ANTENNA_CABLE', 'KEY_AUTO_ARC_ANTENNA_CABLE', 'KEY_AUTO_ARC_ANTENNA_CABLE'),
            (SendKey, 'fnKEY_AUTO_ARC_ANTENNA_SATELLITE', 'KEY_AUTO_ARC_ANTENNA_SATELLITE', 'KEY_AUTO_ARC_ANTENNA_SATELLITE', 'KEY_AUTO_ARC_ANTENNA_SATELLITE'),
        )
    ),
    (
        eg.ActionGroup, 'PanelKeys', 'Panel Keys', 'Panel Keys ', (
            (SendKey, 'fnKEY_PANNEL_POWER', 'KEY_PANNEL_POWER', 'KEY_PANNEL_POWER', 'KEY_PANNEL_POWER'),
            (SendKey, 'fnKEY_PANNEL_CHUP', 'KEY_PANNEL_CHUP', 'KEY_PANNEL_CHUP', 'KEY_PANNEL_CHUP'),
            (SendKey, 'fnKEY_PANNEL_VOLUP', 'KEY_PANNEL_VOLUP', 'KEY_PANNEL_VOLUP', 'KEY_PANNEL_VOLUP'),
            (SendKey, 'fnKEY_PANNEL_VOLDOW', 'KEY_PANNEL_VOLDOW', 'KEY_PANNEL_VOLDOW', 'KEY_PANNEL_VOLDOW'),
            (SendKey, 'fnKEY_PANNEL_ENTER', 'KEY_PANNEL_ENTER', 'KEY_PANNEL_ENTER', 'KEY_PANNEL_ENTER'),
            (SendKey, 'fnKEY_PANNEL_MENU', 'KEY_PANNEL_MENU', 'KEY_PANNEL_MENU', 'KEY_PANNEL_MENU'),
            (SendKey, 'fnKEY_PANNEL_SOURCE', 'KEY_PANNEL_SOURCE', 'KEY_PANNEL_SOURCE', 'KEY_PANNEL_SOURCE'),
            (SendKey, 'fnKEY_PANNEL_ENTER', 'KEY_PANNEL_ENTER', 'KEY_PANNEL_ENTER', 'KEY_PANNEL_ENTER')
        )
    ),
    (
        eg.ActionGroup, 'ExtendedKeys', 'Extended Keys', 'Extended Keys ', (
            (SendKey, 'fnKEY_EXT1', 'KEY_EXT1', 'KEY_EXT1', 'KEY_EXT1'),
            (SendKey, 'fnKEY_EXT2', 'KEY_EXT2', 'KEY_EXT2', 'KEY_EXT2'),
            (SendKey, 'fnKEY_EXT3', 'KEY_EXT3', 'KEY_EXT3', 'KEY_EXT3'),
            (SendKey, 'fnKEY_EXT4', 'KEY_EXT4', 'KEY_EXT4', 'KEY_EXT4'),
            (SendKey, 'fnKEY_EXT5', 'KEY_EXT5', 'KEY_EXT5', 'KEY_EXT5'),
            (SendKey, 'fnKEY_EXT6', 'KEY_EXT6', 'KEY_EXT6', 'KEY_EXT6'),
            (SendKey, 'fnKEY_EXT7', 'KEY_EXT7', 'KEY_EXT7', 'KEY_EXT7'),
            (SendKey, 'fnKEY_EXT8', 'KEY_EXT8', 'KEY_EXT8', 'KEY_EXT8'),
            (SendKey, 'fnKEY_EXT11', 'KEY_EXT11', 'KEY_EXT11', 'KEY_EXT11'),
            (SendKey, 'fnKEY_EXT12', 'KEY_EXT12', 'KEY_EXT12', 'KEY_EXT12'),
            (SendKey, 'fnKEY_EXT13', 'KEY_EXT13', 'KEY_EXT13', 'KEY_EXT13'),
            (SendKey, 'fnKEY_EXT16', 'KEY_EXT16', 'KEY_EXT16', 'KEY_EXT16'),
            (SendKey, 'fnKEY_EXT17', 'KEY_EXT17', 'KEY_EXT17', 'KEY_EXT17'),
            (SendKey, 'fnKEY_EXT18', 'KEY_EXT18', 'KEY_EXT18', 'KEY_EXT18'),
            (SendKey, 'fnKEY_EXT19', 'KEY_EXT19', 'KEY_EXT19', 'KEY_EXT19'),
            (SendKey, 'fnKEY_EXT20', 'KEY_EXT20', 'KEY_EXT20', 'KEY_EXT20'),
            (SendKey, 'fnKEY_EXT21', 'KEY_EXT21', 'KEY_EXT21', 'KEY_EXT21'),
            (SendKey, 'fnKEY_EXT22', 'KEY_EXT22', 'KEY_EXT22', 'KEY_EXT22'),
            (SendKey, 'fnKEY_EXT23', 'KEY_EXT23', 'KEY_EXT23', 'KEY_EXT23'),
            (SendKey, 'fnKEY_EXT24', 'KEY_EXT24', 'KEY_EXT24', 'KEY_EXT24'),
            (SendKey, 'fnKEY_EXT25', 'KEY_EXT25', 'KEY_EXT25', 'KEY_EXT25'),
            (SendKey, 'fnKEY_EXT26', 'KEY_EXT26', 'KEY_EXT26', 'KEY_EXT26'),
            (SendKey, 'fnKEY_EXT27', 'KEY_EXT27', 'KEY_EXT27', 'KEY_EXT27'),
            (SendKey, 'fnKEY_EXT28', 'KEY_EXT28', 'KEY_EXT28', 'KEY_EXT28'),
            (SendKey, 'fnKEY_EXT29', 'KEY_EXT29', 'KEY_EXT29', 'KEY_EXT29'),
            (SendKey, 'fnKEY_EXT30', 'KEY_EXT30', 'KEY_EXT30', 'KEY_EXT30'),
            (SendKey, 'fnKEY_EXT31', 'KEY_EXT31', 'KEY_EXT31', 'KEY_EXT31'),
            (SendKey, 'fnKEY_EXT32', 'KEY_EXT32', 'KEY_EXT32', 'KEY_EXT32'),
            (SendKey, 'fnKEY_EXT33', 'KEY_EXT33', 'KEY_EXT33', 'KEY_EXT33'),
            (SendKey, 'fnKEY_EXT34', 'KEY_EXT34', 'KEY_EXT34', 'KEY_EXT34'),
            (SendKey, 'fnKEY_EXT35', 'KEY_EXT35', 'KEY_EXT35', 'KEY_EXT35'),
            (SendKey, 'fnKEY_EXT36', 'KEY_EXT36', 'KEY_EXT36', 'KEY_EXT36'),
            (SendKey, 'fnKEY_EXT37', 'KEY_EXT37', 'KEY_EXT37', 'KEY_EXT37'),
            (SendKey, 'fnKEY_EXT38', 'KEY_EXT38', 'KEY_EXT38', 'KEY_EXT38'),
            (SendKey, 'fnKEY_EXT39', 'KEY_EXT39', 'KEY_EXT39', 'KEY_EXT39'),
            (SendKey, 'fnKEY_EXT40', 'KEY_EXT40', 'KEY_EXT40', 'KEY_EXT40'),
            (SendKey, 'fnKEY_EXT41', 'KEY_EXT41', 'KEY_EXT41', 'KEY_EXT41')
        )
    )
)
