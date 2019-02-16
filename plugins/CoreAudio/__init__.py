# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright Â© 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

pyWinCoreAudio = __import__('pyWinCoreAudio')

eg.RegisterPlugin(
    name=u'Core Audio',
    author=u'K',
    version=u'0.1a',
    description=u'',
    kind=u'other',
    canMultiLoad=False,
    createMacrosOnAdd=False,
    guid=u'{0FA5977B-8C04-408C-AC2D-947FE2BD7666}',
    icon=None
)

import wx # NOQA
import threading # NOQA
from eg.WinApi import SoundMixer # NOQA


class Text(eg.TranslatableStrings):
    # add variables with string that you want to be able to have translated
    # using the language editor in here

    class GetMasterVolume:
        name = 'Get Master Volume'
        description = 'Gets the master volume level.'

    class SetMasterVolume:
        name = 'Set Master Volume'
        description = 'Sets the master volume level.'

    class GetEndpointVolume:
        name = 'Get Endpoint Volume'
        description = 'Gets the volume level for a given endpoint.'

    class SetEndpointVolumeAbsolute:
        name = 'Set Endpoint Volume Absolute'
        description = 'Sets the volume level for a given endpoint.'

    class SetEndpointVolumeRelative:
        name = 'Set Endpoint Volume Relative'
        description = 'Sets the volume level +- the supplied amount.'

    class GetChannelVolume:
        name = 'Get Channel Volume'
        description = (
            'Gets the volume for a single channel on a given endpoint.'
        )

    class SetChannelVolumeAbsolute:
        name = 'Set Channel Volume Absolute'
        description = (
            'Sets the volume for a single channel on a given endpoint.'
        )

    class SetChannelVolumeRelative:
        name = 'Set Channel Volume Relative'
        description = (
            'Sets the volume for a single channel level +- the supplied amount.'
        )

    class IsPlaying:
        name = 'IsPlaying'
        description = 'Checks is there is audio output on a given endpoint.'


class Callbacks:

    def __init__(self, plugin):
        self.plugin = plugin
        self.__sessions = dict()
        self.__endpoints = dict()
        self.__default_endpoints = dict()
        self.__registered_endpoints = dict()
        self.__volume_lock = threading.Lock()

        pyWinCoreAudio.AudioDevices.register_notification_callback(self)

        for device in pyWinCoreAudio.AudioDevices:
            self.__map_device(device)

    def __map_device(self, device):
        self.__registered_endpoints[device] = []
        for endpoint in device:
            if endpoint.is_default:
                if endpoint.data_flow not in self.__default_endpoints:
                    self.__default_endpoints[endpoint.data_flow] = None

                old_default = self.__default_endpoints[endpoint.data_flow]

                if old_default is None or old_default.id != endpoint.id:
                    self.__default_endpoints[endpoint.data_flow] = endpoint
                    self.plugin.TriggerEvent(
                        u'{0}.{1}.Default.{2}'.format(
                            device.name,
                            self.__format_endpoint_name(endpoint),
                            endpoint.data_flow
                        ),
                        endpoint
                    )
            try:
                volume = endpoint.volume
                channels = volume.channels
                volume.register_notification_callback(self)
                self.__endpoints[endpoint] = dict(
                    vol=volume.master_scalar,
                    mute=volume.mute,
                    channels={
                        i: channels[i].level_scalar
                        for i in range(channels.count)
                    }
                )

            except AttributeError:
                pass
            self.__registered_endpoints[device] += [endpoint]
            for session in endpoint:
                session.register_notification_callback(self)
                # self.__sessions[session] = dict(vol=session.volume.master_scalar, mute=session.volume.mute)
            try:
                endpoint.session_manager.register_notification_callback(
                    self
                )
            except AttributeError:
                pass

    @staticmethod
    def __format_endpoint_name(endpoint):
        return endpoint.name.replace(
            '(' + endpoint.device.name + ')',
            ''
        ).strip()

    def session_created(self, session):
        endpoint = session.session_manager.endpoint
        device = endpoint.device
        self.plugin.TriggerEvent(
            u'{0}.{1}.Session.{2}.Created'.format(
                device.name,
                self.__format_endpoint_name(endpoint),
                session.name
            ),
            session
        )
        session.register_notification_callback(self)
        # self.__sessions[session] = dict(vol=session.volume.master_scalar, mute=session.volume.mute)

    def session_name_changed(self, session, _):
        endpoint = session.session_manager.endpoint
        device = endpoint.device

        self.plugin.TriggerEvent(
            u'{0}.{1}.{2}.NameChanged'.format(
                device.name,
                self.__format_endpoint_name(endpoint),
                session.name
            ),
            session
        )

    def session_grouping_changed(self, session, _):
        endpoint = session.session_manager.endpoint
        device = endpoint.device

        self.plugin.TriggerEvent(
            u'{0}.{1}.{2}.GroupChanged'.format(
                device.name,
                self.__format_endpoint_name(endpoint),
                session.name
            ),
            session
        )

    def session_icon_path_changed(self, session, _):
        endpoint = session.session_manager.endpoint
        device = endpoint.device

        self.plugin.TriggerEvent(
            u'{0}.{1}.{2}.IconChanged'.format(
                device.name,
                self.__format_endpoint_name(endpoint),
                session.name
            ),
            session
        )

    def session_disconnect(
        self,
        endpoint,
        name,
        id,
        disconnect_reason
    ):
        device = endpoint.device

        self.plugin.TriggerEvent(
            u'{0}.{1}.{2}.Disconnected'.format(
                device.name,
                self.__format_endpoint_name(endpoint),
                name
            ),
            disconnect_reason
        )

    def session_volume_changed(self, session, new_vol, new_mute):
        endpoint = session.session_manager.endpoint
        device = endpoint.device

        if session not in self.__sessions:
            self.__sessions[session] = dict(vol=None, mute=None)

        old_vol = self.__sessions[session]['vol']
        old_mute = self.__sessions[session]['mute']

        if old_vol != new_vol:
            self.__sessions[session]['vol'] = new_vol
            self.plugin.TriggerEvent(
                u'{0}.{1}.{2}.Volume.{3:.4f}'.format(
                    device.name,
                    self.__format_endpoint_name(endpoint),
                    session.name,
                    new_vol * 100.0
                ),
                session
            )
        if old_mute != new_mute:
            self.__sessions[session]['mute'] = new_mute
            if new_mute:
                self.plugin.TriggerEvent(
                    u'{0}.{1}.{2}.MuteOn'.format(
                        device.name,
                        self.__format_endpoint_name(endpoint),
                        session.name
                    ),
                    session
                )
            else:
                self.plugin.TriggerEvent(
                    u'{0}.{1}.{2}.MuteOff'.format(
                        device.name,
                        self.__format_endpoint_name(endpoint),
                        session.name
                    ),
                    session
                )

    def session_state_changed(self, session, state):
        endpoint = session.session_manager.endpoint
        device = endpoint.device

        if state == 'Active':
            state = 'AudioPlayback.Started'

        elif state == 'Inactive':
            state = 'AudioPlayback.Stopped'

        else:
            state = 'State.' + state

        self.plugin.TriggerEvent(
            u'{0}.{1}.{2}.{3}'.format(
                device.name,
                self.__format_endpoint_name(endpoint),
                session.name,
                state
            ),
            session
        )

    def endpoint_volume_change(
        self,
        endpoint,
        new_vol,
        new_channels,
        new_mute
    ):

        if endpoint not in self.__endpoints:
            self.__endpoints[endpoint] = dict(
                vol=None,
                mute=None,
                channels=[None] * 8
            )

        old_endpoint = self.__endpoints[endpoint]
        old_mute = old_endpoint['mute']
        old_vol = old_endpoint['vol']
        old_channels = old_endpoint['channels']

        if new_vol > old_vol:
            vol_diff = new_vol - old_vol
        else:
            vol_diff = old_vol

        if old_mute != new_mute:
            old_endpoint['mute'] = new_mute
            if new_mute:
                self.plugin.TriggerEvent(
                    u'{0}.{1}.MuteOn'.format(
                        endpoint.device.name,
                        self.__format_endpoint_name(endpoint),
                    ),
                    endpoint
                )
            else:
                self.plugin.TriggerEvent(
                    u'{0}.{1}.MuteOff'.format(
                        endpoint.device.name,
                        self.__format_endpoint_name(endpoint),
                    ),
                    endpoint
                )

        equal_channels = []
        unequal_channels = []

        for channel_num, channel_vol in enumerate(new_channels):
            if channel_num not in old_channels:
                old_channels[channel_num] = 0

            if (
                round(channel_vol, 4) ==
                round(old_channels[channel_num], 4)
            ):
                continue

            if round(new_vol, 4) - round(channel_vol, 4) == 0:
                equal_channels += [channel_num]

            elif (
                round(new_vol, 4) - round(vol_diff, 4) ==
                round(channel_vol, 4)
            ):
                equal_channels += [channel_num]

            else:
                unequal_channels += [channel_num]

            old_channels[channel_num] = channel_vol

        if old_vol != new_vol:
            old_endpoint['vol'] = new_vol
            if len(equal_channels) == 1:
                channel_num = equal_channels[0]
                channel_vol = new_channels[channel_num]

                self.plugin.TriggerEvent(
                    u'{0}.{1}.Channel.{2}.Volume.{3:.4f}'.format(
                        endpoint.device.name,
                        self.__format_endpoint_name(endpoint),
                        channel_num,
                        channel_vol * 100.0
                    ),
                    endpoint
                )

            self.plugin.TriggerEvent(
                u'{0}.{1}.Volume.{2:.4f}'.format(
                    endpoint.device.name,
                    self.__format_endpoint_name(endpoint),
                    new_vol * 100.0
                ),
                endpoint
            )

        elif len(unequal_channels) == 1:
            channel_num = unequal_channels[0]
            channel_vol = new_channels[channel_num]

            self.plugin.TriggerEvent(
                u'{0}.{1}.Channel.{2}.Volume.{3:.4f}'.format(
                    endpoint.device.name,
                    self.__format_endpoint_name(endpoint),
                    channel_num,
                    channel_vol * 100.0
                ),
                endpoint
            )

    def device_state_change(self, device, state):
        self.plugin.TriggerEvent(
            u'{0}.State.{1}'.format(
                device.name,
                state
            ),
            device
        )

    def device_added(self, device):
        self.__map_device(device)

        self.plugin.TriggerEvent(
            u'Device.{0}.Added'.format(device.name),
            device
        )

    def device_removed(self, device):
        for endpoint in self.__registered_endpoints[device]:
            del(self.__endpoints[endpoint])

        del(self.__registered_endpoints[device])
        self.plugin.TriggerEvent(u'Device.{0}.Removed'.format(device.name))

    def default_endpoint_changed(self, device):
        for endpoint in device:
            if endpoint.is_default:
                old_default = self.__default_endpoints[endpoint.data_flow]
                if old_default is None or old_default.id != endpoint.id:
                    self.__default_endpoints[endpoint.data_flow] = endpoint
                    self.plugin.TriggerEvent(
                        u'{0}.{1}.Default.{2}'.format(
                            device.name,
                            self.__format_endpoint_name(endpoint),
                            endpoint.data_flow
                        ),
                        endpoint
                    )

    def device_property_changed(self, device, key):
        # print 'device property changed'
        # print '    device name:', device.name
        # print '    key:', key.fmtid, key.pid
        # print
        # print
        pass


class CoreAudio(eg.PluginBase):
    text = Text

    def __init__(self):
        eg.PluginBase.__init__(self)

        self.AddAction(GetEndpointVolume)
        self.AddAction(SetEndpointVolumeAbsolute)
        self.AddAction(SetEndpointVolumeRelative)
        self.AddAction(GetSessionVolume)
        self.AddAction(GetEndpointChannelVolume)
        self.AddAction(SetEndpointChannelVolumeAbsolute)
        self.AddAction(SetEndpointChannelVolumeRelative)
        self.AddAction(IsDeviceActive)
        self.AddAction(GetEndpointMute)
        self.AddAction(SetEndpointMute)
        self.AddAction(ToggleEndpointMute)
        self.AddAction(IsPlaybackEndpointActive)
        self.AddAction(IsDefaultPlaybackEndpoint)
        self.AddAction(GetDefaultPlaybackEndpoint)
        self.AddAction(SetDefaultPlaybackEndpoint)
        self.AddAction(IsDefaultRecordingEndpoint)
        self.AddAction(GetDefaultRecordingEndpoint)
        self.AddAction(SetDefaultRecordingEndpoint)

    def __start__(self):
        self.callbacks = Callbacks(self)

    def __close__(self):
        pass

    def __stop__(self):
        pass


class DevicePanel(wx.Panel):

    def __init__(self, parent, use_defaults=True):
        wx.Panel.__init__(self, parent, -1)
        self._devices = sorted(
            iter(pyWinCoreAudio.AudioDevices),
            key=lambda x: x.name
        )

        choices = (
            ['Default Playback Device', 'Default Recording Device'] +
            list(device.name for device in self._devices)
        )
        self._devices = [
            'Default Playback Device',
            'Default Recording Device'
        ] + self._devices

        if not use_defaults:
            choices = choices[2:]
            self._devices = self._devices[2:]

        self.device_ctrl = wx.Choice(
            self,
            -1,
            choices=choices
        )

        bottom_sizer = wx.BoxSizer(wx.VERTICAL)

        def create_widgets(txt):
            st = wx.StaticText(self, -1, txt)
            ctrl = wx.StaticText(self, -1, ' ' * 20)

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(st, 0, wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALL, 5)
            bottom_sizer.Add(sizer)
            return ctrl

        self.connector_ctrl = create_widgets('Connector Count:')
        self.state_ctrl = create_widgets('State:')

        self.device_ctrl.Bind(wx.EVT_CHOICE, self.on_choice)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(self.device_ctrl, 1, wx.EXPAND | wx.ALL, 15)
        main_sizer.Add(bottom_sizer)
        self.SetSizer(main_sizer)

    def set_selection(self, value):
        self.device_ctrl.SetSelection(value)
        self.on_choice()

    def set_string_selection(self, value):
        self.device_ctrl.SetStringSelection(value)
        self.on_choice()

    def get_string_selection(self):
        return self.device_ctrl.GetStringSelection()

    def on_choice(self, evt=None):
        selection = self.device_ctrl.GetSelection()
        device = self._devices[selection]

        if device in ('Default Playback Device', 'Default Recording Device'):
            self.connector_ctrl.SetLabel('')
            self.state_ctrl.SetLabel('')
        else:
            self.connector_ctrl.SetLabel(unicode(device.connector_count))
            self.state_ctrl.SetLabel(unicode(device.state))

        if evt is not None:
            evt.Skip()

    def get_device(self):
        selection = self.device_ctrl.GetSelection()
        device = self._devices[selection]
        return device


class EndpointPanel(wx.Panel):

    def __init__(self, parent):
        self._endpoints = []
        self._flow = 'All'
        wx.Panel.__init__(self, parent, -1)
        self.endpoint_ctrl = wx.Choice(self, -1, choices=[])

        bottom_sizer = wx.BoxSizer(wx.VERTICAL)

        def create_widgets(txt):
            st = wx.StaticText(self, -1, txt)
            ctrl = wx.StaticText(self, -1, ' ' * 20)

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(st, 0, wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALL, 5)
            bottom_sizer.Add(sizer)
            return ctrl

        self.description_ctrl = create_widgets('Description:')
        self.data_flow_ctrl = create_widgets('Flow:')
        self.form_factor_ctrl = create_widgets('Type:')
        self.full_speaker_ctrl = create_widgets('Full Range Speakers:')
        self.guid_ctrl = create_widgets('GUID:')
        self.physical_speaker_ctrl = create_widgets('Physical Speakers:')
        self.effects_ctrl = create_widgets('System Effects:')

        self.endpoint_ctrl.Bind(wx.EVT_CHOICE, self.on_choice)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(self.endpoint_ctrl, 1, wx.EXPAND | wx.ALL, 15)
        main_sizer.Add(bottom_sizer)
        self.SetSizer(main_sizer)

    def set_flow(self, flow):
        self._flow = flow

    def set_endpoints(self, device):

        if device in ('Default Playback Device', 'Default Recording Device'):
            self._endpoints = []
            self.endpoint_ctrl.Clear()
            self.description_ctrl.SetLabel('')
            self.data_flow_ctrl.SetLabel('')
            self.form_factor_ctrl.SetLabel('')
            self.full_speaker_ctrl.SetLabel('')
            self.guid_ctrl.SetLabel('')
            self.physical_speaker_ctrl.SetLabel('')
            self.effects_ctrl.SetLabel('')

        else:

            self._endpoints = sorted(iter(device), key=lambda x: x.name)

            if self._flow != 'All':
                self._endpoints = list(
                    endpoint for endpoint in self._endpoints
                    if endpoint.data_flow == self._flow
                )

            self.endpoint_ctrl.Clear()
            self.endpoint_ctrl.AppendItems(
                list(endpoint.name for endpoint in self._endpoints)
            )

    def set_selection(self, value):
        if value is not None:
            self.endpoint_ctrl.SetSelection(value)
            self.on_choice()

    def set_string_selection(self, value):
        if value is not None:
            self.endpoint_ctrl.SetStringSelection(value)
            self.on_choice()

    def get_string_selection(self):
        if self.endpoint_ctrl.GetItems():
            return self.endpoint_ctrl.GetStringSelection()
        else:
            return None

    def on_choice(self, evt=None):

        selection = self.endpoint_ctrl.GetSelection()
        endpoint = self._endpoints[selection]

        self.description_ctrl.SetLabel(unicode(endpoint.description))
        self.data_flow_ctrl.SetLabel(unicode(endpoint.data_flow))
        self.form_factor_ctrl.SetLabel(unicode(endpoint.form_factor))
        self.full_speaker_ctrl.SetLabel(unicode(endpoint.full_range_speakers))
        self.guid_ctrl.SetLabel(unicode(endpoint.guid))
        self.physical_speaker_ctrl.SetLabel(unicode(endpoint.physical_speakers))
        self.effects_ctrl.SetLabel(unicode(endpoint.system_effects))

        if evt is not None:
            evt.Skip()

    def get_endpoint(self):
        if self.endpoint_ctrl.GetItems():
            selection = self.endpoint_ctrl.GetSelection()
            endpoint = self._endpoints[selection]
            return endpoint


class SessionPanel(wx.Panel):

    def __init__(self, parent):
        self._sessions = []
        wx.Panel.__init__(self, parent, -1)
        self.session_ctrl = wx.Choice(self, -1, choices=[])

        bottom_sizer = wx.BoxSizer(wx.VERTICAL)

        def create_widgets(txt):
            st = wx.StaticText(self, -1, txt)
            ctrl = wx.StaticText(self, -1, ' ' * 20)

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(st, 0, wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.ALL, 5)
            bottom_sizer.Add(sizer)
            return ctrl

        self.state_ctrl = create_widgets('State:')

        self.session_ctrl.Bind(wx.EVT_CHOICE, self.on_choice)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(self.session_ctrl, 1, wx.EXPAND | wx.ALL, 15)
        main_sizer.Add(bottom_sizer)
        self.SetSizer(main_sizer)

    def set_sessions(self, endpoint):
        self.session_ctrl.Clear()
        if endpoint is None:
            del self._sessions[:]
        else:
            self._sessions = sorted(iter(endpoint), key=lambda x: x.name)
            for session in self._sessions:
                print session.id
                print session.process_id
                print session.instance_id
            self.session_ctrl.AppendItems(
                list(session.name for session in self._sessions)
            )

    def set_selection(self, value):
        if self.session_ctrl.GetItems():
            self.session_ctrl.SetSelection(value)
            self.on_choice()

    def set_string_selection(self, value):
        if self.session_ctrl.GetItems():
            self.session_ctrl.SetStringSelection(value)
            self.on_choice()

    def get_string_selection(self):
        if self.session_ctrl.GetItems():
            return self.session_ctrl.GetStringSelection()
        else:
            return ''

    def on_choice(self, evt=None):

        selection = self.session_ctrl.GetSelection()
        session = self._sessions[selection]

        self.state_ctrl.SetLabel(unicode(session.state))
        if evt is not None:
            evt.Skip()

    def get_session(self):
        if self.session_ctrl.GetItems():
            selection = self.session_ctrl.GetSelection()
            session = self._sessions[selection]
            return session


def _re_range(val, min_value, max_value):
    return val * ((max_value - min_value) / 100.0)


class VolumeInfoCtrl(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent, -1)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        def create_widgets(txt):
            st = wx.StaticText(self, -1, txt)
            ctrl = wx.StaticText(self, -1, ' ' * 40)

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(st, 0, wx.ALL, 5)
            sizer.Add(ctrl, 1, wx.ALL, 5)
            main_sizer.Add(sizer)
            return ctrl

        self.scalar_volume_ctrl = create_widgets('Scalar Volume:')
        self.scalar_min_ctrl = create_widgets('Scalar Min:')
        self.scalar_max_ctrl = create_widgets('Scalar Max:')
        self.scalar_step_ctrl = create_widgets('Scalar Step:')
        main_sizer.AddSpacer(1)
        self.db_volume_ctrl = create_widgets('dB Volume:')
        self.db_min_ctrl = create_widgets('db Min:')
        self.db_max_ctrl = create_widgets('db Max:')
        self.db_step_ctrl = create_widgets('db Step:')

        self.SetSizer(main_sizer)

    def set_endpoint(self, endpoint):
        if endpoint:
            volume = endpoint.volume

            db_min = volume.min
            db_max = volume.max
            db_step = volume.step
            scalar_min = 0.0
            scalar_max = 100.0
            scalar_step = _re_range(db_step, db_min, db_max)

            scalar = volume.master_scalar * 100.0
            db = volume.master

            self.scalar_volume_ctrl.SetLabel(u'{0:.4f}'.format(scalar))
            self.scalar_min_ctrl.SetLabel(u'{0:.4f}'.format(scalar_min))
            self.scalar_max_ctrl.SetLabel(u'{0:.4f}'.format(scalar_max))
            self.scalar_step_ctrl.SetLabel(u'{0:.4f}'.format(scalar_step))

            self.db_volume_ctrl.SetLabel(u'{0:.4f}'.format(db))
            self.db_min_ctrl.SetLabel(u'{0:.4f}'.format(db_min))
            self.db_max_ctrl.SetLabel(u'{0:.4f}'.format(db_max))
            self.db_step_ctrl.SetLabel(u'{0:.4f}'.format(db_step))
        else:
            self.scalar_volume_ctrl.SetLabel('')
            self.scalar_min_ctrl.SetLabel('')
            self.scalar_max_ctrl.SetLabel('')
            self.scalar_step_ctrl.SetLabel('')

            self.db_volume_ctrl.SetLabel('')
            self.db_min_ctrl.SetLabel('')
            self.db_max_ctrl.SetLabel('')
            self.db_step_ctrl.SetLabel('')

    def set_channel(self, channel):
        if channel is not None:
            db_min = channel.min
            db_max = channel.max
            db_step = channel.step
            scalar_min = 0.0
            scalar_max = 100.0
            scalar_step = _re_range(db_step, db_min, db_max)

            scalar = channel.level_scalar * 100.0
            db = channel.level

            self.scalar_volume_ctrl.SetLabel(u'{0:.4f}'.format(scalar))
            self.scalar_min_ctrl.SetLabel(u'{0:.4f}'.format(scalar_min))
            self.scalar_max_ctrl.SetLabel(u'{0:.4f}'.format(scalar_max))
            self.scalar_step_ctrl.SetLabel(u'{0:.4f}'.format(scalar_step))

            self.db_volume_ctrl.SetLabel(u'{0:.4f}'.format(db))
            self.db_min_ctrl.SetLabel(u'{0:.4f}'.format(db_min))
            self.db_max_ctrl.SetLabel(u'{0:.4f}'.format(db_max))
            self.db_step_ctrl.SetLabel(u'{0:.4f}'.format(db_step))
        else:
            self.scalar_volume_ctrl.SetLabel('')
            self.scalar_min_ctrl.SetLabel('')
            self.scalar_max_ctrl.SetLabel('')
            self.scalar_step_ctrl.SetLabel('')

            self.db_volume_ctrl.SetLabel('')
            self.db_min_ctrl.SetLabel('')
            self.db_max_ctrl.SetLabel('')
            self.db_step_ctrl.SetLabel('')


class GetEndpointVolume(eg.ActionBase):

    def __call__(self, device, endpoint):
        if device == 'Default Playback Device':
            endpoint = pyWinCoreAudio.AudioDevices.default_render_endpoint
        elif device == 'Default Recording Device':
            endpoint = pyWinCoreAudio.AudioDevices.default_capture_endpoint
        else:
            for dev in pyWinCoreAudio.AudioDevices:
                if dev.name == device:
                    for endpt in dev:
                        if endpt.name == endpoint:
                            endpoint = endpt
                            break
                    else:
                        continue
                    break
            else:
                return None
        try:
            return endpoint.volume.master_scalar * 100.0
        except AttributeError:
            return None

    def Configure(
        self,
        device='Default Playback Device',
        endpoint=None
    ):
        text = self.text
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(panel)
        endpoint_ctrl = EndpointPanel(panel)
        volume_info_ctrl = VolumeInfoCtrl(panel)

        device_ctrl.set_string_selection(device)
        endpoint_ctrl.set_endpoints(device_ctrl.get_device())
        endpoint_ctrl.set_string_selection(endpoint)

        endpoint = endpoint_ctrl.get_endpoint()

        if endpoint is not None:
            try:
                _ = endpoint.volume
                volume_info_ctrl.set_endpoint(endpoint)
            except AttributeError:
                pass

        def on_device_choice(evt):
            def do():
                device = device_ctrl.get_device()
                endpoint_ctrl.set_endpoints(device)
                if device not in (
                    'Default Playback Device',
                    'Default Recording Device'
                ):
                    endpoint_ctrl.set_selection(0)
                    endpoint = endpoint_ctrl.get_endpoint()
                    try:
                        _ = endpoint.volume
                        volume_info_ctrl.set_endpoint(endpoint)
                    except AttributeError:
                        volume_info_ctrl.set_endpoint(None)
                else:
                    volume_info_ctrl.set_endpoint(None)

            wx.CallAfter(do)
            evt.Skip()

        def on_endpoint_choice(evt):
            def do():
                endpoint = endpoint_ctrl.get_endpoint()
                try:
                    _ = endpoint.volume
                    volume_info_ctrl.set_endpoint(endpoint)
                except AttributeError:
                    volume_info_ctrl.set_endpoint(None)

            wx.CallAfter(do)
            evt.Skip()

        device_ctrl.Bind(wx.EVT_CHOICE, on_device_choice)
        endpoint_ctrl.Bind(wx.EVT_CHOICE, on_endpoint_choice)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(device_ctrl, 1)
        sizer.Add(endpoint_ctrl, 1)
        sizer.Add(volume_info_ctrl)

        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.get_string_selection(),
                endpoint_ctrl.get_string_selection()
            )


class SetEndpointVolumeBase(eg.ActionBase):
    _spin_range = dict(min=0.0, max=0.0)

    def _update_volume(self, old_volume, new_volume):
        raise NotImplementedError

    def __call__(self, device, endpoint, volume):
        if device == 'Default Playback Device':
            endpoint = pyWinCoreAudio.AudioDevices.default_render_endpoint
        elif device == 'Default Recording Device':
            endpoint = pyWinCoreAudio.AudioDevices.default_capture_endpoint
        else:
            for dev in pyWinCoreAudio.AudioDevices:
                if dev.name == device:
                    for endpt in dev:
                        if endpt.name == endpoint:
                            endpoint = endpt
                            break
                    else:
                        continue
                    break
            else:
                return None
        try:
            endpoint.volume.master_scalar = self._update_volume(
                endpoint.volume.master_scalar,
                volume
            )

            return endpoint.volume.master_scalar * 100.0
        except AttributeError:
            return None

    def Configure(
        self,
        device='Default Playback Device',
        endpoint=None,
        volume=0.0
    ):
        text = self.text
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(panel)
        endpoint_ctrl = EndpointPanel(panel)
        volume_info_ctrl = VolumeInfoCtrl(panel)
        volume_ctrl = eg.SpinNumCtrl(
            panel,
            -1,
            value=volume,
            increment=1.0,
            **self._spin_range
        )

        device_ctrl.set_string_selection(device)
        endpoint_ctrl.set_endpoints(device_ctrl.get_device())
        endpoint_ctrl.set_string_selection(endpoint)
        endpoint = endpoint_ctrl.get_endpoint()

        if endpoint is not None:
            try:
                vol = endpoint.volume
                volume_info_ctrl.set_endpoint(endpoint)
                volume_ctrl.increment = _re_range(
                    vol.step,
                    vol.min,
                    vol.max
                )
            except AttributeError:
                panel.EnableButtons(False)
                volume_ctrl.Enable(False)

        def on_device_choice(evt):
            def do():
                device = device_ctrl.get_device()
                endpoint_ctrl.set_endpoints(device)
                if device not in (
                    'Default Playback Device',
                    'Default Recording Device'
                ):
                    endpoint_ctrl.set_selection(0)
                    endpoint = endpoint_ctrl.get_endpoint()
                    try:
                        vol = endpoint.volume
                        volume_info_ctrl.set_endpoint(endpoint)
                        volume_ctrl.increment = _re_range(
                            vol.step,
                            vol.min,
                            vol.max
                        )
                        panel.EnableButtons(True)
                        volume_ctrl.Enable(True)

                    except AttributeError:
                        volume_info_ctrl.set_endpoint(None)
                        volume_ctrl.Enable(False)
                        panel.EnableButtons(False)
                else:
                    volume_info_ctrl.set_endpoint(None)
                    volume_ctrl.increment = 1.0
                    panel.EnableButtons(True)
                    volume_ctrl.Enable(True)

            wx.CallAfter(do)
            evt.Skip()

        def on_endpoint_choice(evt):
            def do():
                endpoint = endpoint_ctrl.get_endpoint()
                try:
                    vol = endpoint.volume
                    volume_info_ctrl.set_endpoint(endpoint)
                    volume_ctrl.increment = _re_range(
                        vol.step,
                        vol.min,
                        vol.max
                    )
                    volume_ctrl.Enable(True)
                    panel.EnableButtons(True)
                except AttributeError:
                    volume_info_ctrl.set_endpoint(None)
                    volume_ctrl.Enable(False)
                    panel.EnableButtons(False)

            wx.CallAfter(do)
            evt.Skip()

        device_ctrl.Bind(wx.EVT_CHOICE, on_device_choice)
        endpoint_ctrl.Bind(wx.EVT_CHOICE, on_endpoint_choice)

        volume_sizer = wx.BoxSizer(wx.VERTICAL)
        volume_sizer.Add(volume_ctrl, 0, wx.ALL, 15)
        volume_sizer.Add(volume_info_ctrl, 0)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(device_ctrl, 1)
        sizer.Add(endpoint_ctrl, 1)
        sizer.Add(volume_sizer, 0)

        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.get_string_selection(),
                endpoint_ctrl.get_string_selection(),
                volume_ctrl.GetValue()
            )


class SetEndpointVolumeAbsolute(SetEndpointVolumeBase):
    _spin_range = dict(min=0.0, max=100.0)

    def _update_volume(self, _, new_volume):
        return new_volume / 100


class SetEndpointVolumeRelative(SetEndpointVolumeBase):
    _spin_range = dict(min=-100.0, max=100.0)

    def _update_volume(self, old_volume, new_volume):
        new_volume = old_volume + (new_volume / 100)

        if new_volume > 1:
            new_volume = 1.0
        elif new_volume < 0:
            new_volume = 0.0

        return new_volume


class GetEndpointChannelVolume(eg.ActionBase):

    def __call__(self, device, endpoint, channel):
        if device == 'Default Playback Device':
            endpoint = pyWinCoreAudio.AudioDevices.default_render_endpoint
        elif device == 'Default Recording Device':
            endpoint = pyWinCoreAudio.AudioDevices.default_capture_endpoint
        else:
            for dev in pyWinCoreAudio.AudioDevices:
                if dev.name == device:
                    for endpt in dev:
                        if endpt.name == endpoint:
                            endpoint = endpt
                            break
                    else:
                        continue
                    break
            else:
                return None
        try:
            return endpoint.volume.channels[channel].level_scalar * 100.0
        except (AttributeError, IndexError):
            return None

    def Configure(
        self,
        device='Default Playback Device',
        endpoint=None,
        channel=0
    ):
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(panel)
        endpoint_ctrl = EndpointPanel(panel)
        volume_info_ctrl = VolumeInfoCtrl(panel)
        channel_ctrl = eg.SpinIntCtrl(panel, -1, value=0, min=0, max=8)

        device_ctrl.set_string_selection(device)
        endpoint_ctrl.set_endpoints(device_ctrl.get_device())
        endpoint_ctrl.set_string_selection(endpoint)
        endpoint = endpoint_ctrl.get_endpoint()

        if endpoint is not None:
            try:
                vol = endpoint.volume
                channel_ctrl.numCtrl.SetMax(vol.channels.count - 1)
                volume_info_ctrl.set_channel(vol.channels[channel])

            except AttributeError:
                panel.EnableButtons(False)
                channel_ctrl.Enable(False)

        def on_device_choice(evt):
            def do():
                device = device_ctrl.get_device()
                endpoint_ctrl.set_endpoints(device)
                if device not in (
                    'Default Playback Device',
                    'Default Recording Device'
                ):
                    endpoint_ctrl.set_selection(0)
                    endpoint = endpoint_ctrl.get_endpoint()
                    try:
                        vol = endpoint.volume
                        channel_ctrl.numCtrl.SetMax(vol.channels.count - 1)
                        volume_info_ctrl.set_channel(vol.channels[0])
                        panel.EnableButtons(True)
                        channel_ctrl.Enable(True)
                        channel_ctrl.SetValue(0)

                    except AttributeError:
                        volume_info_ctrl.set_channel(None)
                        channel_ctrl.Enable(False)
                        panel.EnableButtons(False)
                else:
                    volume_info_ctrl.set_channel(None)
                    channel_ctrl.numCtrl.SetMax(8)
                    panel.EnableButtons(True)
                    channel_ctrl.Enable(True)

            wx.CallAfter(do)
            evt.Skip()

        def on_endpoint_choice(evt):
            def do():
                endpoint = endpoint_ctrl.get_endpoint()
                try:
                    vol = endpoint.volume
                    channel_ctrl.numCtrl.SetMax(vol.channels.count - 1)
                    volume_info_ctrl.set_channel(vol.channels[0])
                    panel.EnableButtons(True)
                    channel_ctrl.Enable(True)
                    channel_ctrl.SetValue(0)
                except AttributeError:
                    volume_info_ctrl.set_channel(None)
                    channel_ctrl.Enable(False)
                    panel.EnableButtons(False)

            wx.CallAfter(do)
            evt.Skip()

        device_ctrl.Bind(wx.EVT_CHOICE, on_device_choice)
        endpoint_ctrl.Bind(wx.EVT_CHOICE, on_endpoint_choice)

        channel_sizer = wx.BoxSizer(wx.VERTICAL)
        channel_sizer.Add(channel_ctrl, 0, wx.ALL, 15)
        channel_sizer.Add(volume_info_ctrl, 0)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(device_ctrl, 1)
        sizer.Add(endpoint_ctrl, 1)
        sizer.Add(channel_sizer, 0)

        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.get_string_selection(),
                endpoint_ctrl.get_string_selection(),
                channel_ctrl.GetValue()
            )


class SetEndpointChannelVolumeBase(eg.ActionBase):
    _spin_range = dict(min=0.0, max=0.0)

    def _update_volume(self, old_volume, new_volume):
        raise NotImplementedError

    def __call__(self, device, endpoint, channel, volume):
        if device == 'Default Playback Device':
            endpoint = pyWinCoreAudio.AudioDevices.default_render_endpoint
        elif device == 'Default Recording Device':
            endpoint = pyWinCoreAudio.AudioDevices.default_capture_endpoint
        else:
            for dev in pyWinCoreAudio.AudioDevices:
                if dev.name == device:
                    for endpt in dev:
                        if endpt.name == endpoint:
                            endpoint = endpt
                            break
                    else:
                        continue
                    break
            else:
                return None
        try:
            endpoint.volume.channels[channel].level_scalar = (
                self._update_volume(
                    endpoint.volume.channels[channel].level_scalar,
                    volume
                )
            )
            return endpoint.volume.channels[channel].level_scalar * 100
        except (AttributeError, IndexError):
            return None

    def Configure(
        self,
        device='Default Playback Device',
        endpoint=None,
        channel=0,
        volume=0.0
    ):
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(panel)
        endpoint_ctrl = EndpointPanel(panel)
        volume_info_ctrl = VolumeInfoCtrl(panel)
        channel_ctrl = eg.SpinIntCtrl(panel, -1, value=0, min=0, max=8)
        volume_ctrl = eg.SpinNumCtrl(
            panel,
            -1,
            value=volume,
            increment=1.0,
            **self._spin_range
        )

        device_ctrl.set_string_selection(device)
        endpoint_ctrl.set_endpoints(device_ctrl.get_device())
        endpoint_ctrl.set_string_selection(endpoint)
        endpoint = endpoint_ctrl.get_endpoint()

        if endpoint is not None:
            try:
                vol = endpoint.volume
                channel_ctrl.numCtrl.SetMax(vol.channels.count - 1)
                channel = vol.channels[channel]
                volume_info_ctrl.set_channel(channel)
                volume_ctrl.increment = _re_range(
                    channel.step,
                    channel.min,
                    channel.max
                )

            except AttributeError:
                panel.EnableButtons(False)
                channel_ctrl.Enable(False)
                volume_ctrl.Enable(False)

        def on_device_choice(evt):
            def do():
                device = device_ctrl.get_device()
                endpoint_ctrl.set_endpoints(device)
                if device not in (
                    'Default Playback Device',
                    'Default Recording Device'
                ):
                    endpoint_ctrl.set_selection(0)
                    endpoint = endpoint_ctrl.get_endpoint()
                    try:
                        vol = endpoint.volume
                        channel_ctrl.numCtrl.SetMax(vol.channels.count - 1)
                        channel = vol.channels[0]
                        volume_info_ctrl.set_channel(channel)
                        volume_ctrl.increment = _re_range(
                            channel.step,
                            channel.min,
                            channel.max
                        )
                        panel.EnableButtons(True)
                        channel_ctrl.Enable(True)
                        volume_ctrl.Enable(True)
                        channel_ctrl.SetValue(0)

                    except AttributeError:
                        volume_info_ctrl.set_channel(None)
                        channel_ctrl.Enable(False)
                        volume_ctrl.Enable(False)
                        panel.EnableButtons(False)
                else:
                    volume_info_ctrl.set_channel(None)
                    channel_ctrl.numCtrl.SetMax(8)
                    panel.EnableButtons(True)
                    channel_ctrl.Enable(True)
                    volume_ctrl.Enable(True)
                    volume_ctrl.increment = 1.0

            wx.CallAfter(do)
            evt.Skip()

        def on_endpoint_choice(evt):
            def do():
                endpoint = endpoint_ctrl.get_endpoint()
                try:
                    vol = endpoint.volume
                    channel_ctrl.numCtrl.SetMax(vol.channels.count - 1)
                    channel = vol.channels[0]
                    volume_info_ctrl.set_channel(channel)
                    volume_ctrl.increment = _re_range(
                        channel.step,
                        channel.min,
                        channel.max
                    )
                    panel.EnableButtons(True)
                    channel_ctrl.Enable(True)
                    volume_ctrl.Enable(True)
                    channel_ctrl.SetValue(0)
                except AttributeError:
                    volume_info_ctrl.set_channel(None)
                    channel_ctrl.Enable(False)
                    volume_ctrl.Enable(False)
                    panel.EnableButtons(False)

            wx.CallAfter(do)
            evt.Skip()

        device_ctrl.Bind(wx.EVT_CHOICE, on_device_choice)
        endpoint_ctrl.Bind(wx.EVT_CHOICE, on_endpoint_choice)

        channel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        channel_sizer.Add(channel_ctrl, 0, wx.ALL, 15)
        channel_sizer.Add(volume_ctrl, 0, wx.ALL, 15)

        volume_info_sizer = wx.BoxSizer(wx.VERTICAL)
        volume_info_sizer.Add(channel_sizer, 0)
        volume_info_sizer.Add(volume_info_ctrl, 0)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(device_ctrl, 1)
        sizer.Add(endpoint_ctrl, 1)
        sizer.Add(volume_info_sizer, 0)

        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.get_string_selection(),
                endpoint_ctrl.get_string_selection(),
                channel_ctrl.GetValue(),
                volume_ctrl.GetValue()
            )


class SetEndpointChannelVolumeAbsolute(SetEndpointChannelVolumeBase):
    _spin_range = dict(min=0.0, max=100.0)

    def _update_volume(self, _, new_volume):
        return new_volume / 100


class SetEndpointChannelVolumeRelative(SetEndpointChannelVolumeBase):
    _spin_range = dict(min=-100.0, max=100.0)

    def _update_volume(self, old_volume, new_volume):
        new_volume = old_volume + (new_volume / 100)

        if new_volume > 1:
            new_volume = 1.0
        elif new_volume < 0:
            new_volume = 0.0

        return new_volume



class IsDeviceActive(eg.ActionBase):

    def __call__(self, device):
        if device == 'Default Playback Device':
            endpoint = pyWinCoreAudio.AudioDevices.default_render_endpoint
            device = endpoint.device
        elif device == 'Default Recording Device':
            endpoint = pyWinCoreAudio.AudioDevices.default_capture_endpoint
            device = endpoint.device
        else:
            for dev in pyWinCoreAudio.AudioDevices:
                if dev.name == device:
                    device = dev
                    break
            else:
                return False

        return device.state == 'Active'

    def Configure(
        self,
        device='Default Playback Device',
        endpoint=None,
    ):
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(panel)
        device_ctrl.set_string_selection(device)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(device_ctrl, 1)

        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.get_string_selection(),
            )


class GetEndpointMute(eg.ActionBase):

    def __call__(self, device, endpoint):
        if device == 'Default Playback Device':
            endpoint = pyWinCoreAudio.AudioDevices.default_render_endpoint
        elif device == 'Default Recording Device':
            endpoint = pyWinCoreAudio.AudioDevices.default_capture_endpoint
        else:
            for dev in pyWinCoreAudio.AudioDevices:
                if dev.name == device:
                    for endpt in dev:
                        if endpt.name == endpoint:
                            endpoint = endpt
                            break
                    else:
                        continue
                    break
            else:
                return None
        try:
            return endpoint.volume.mute
        except AttributeError:
            return None

    def Configure(
        self,
        device='Default Playback Device',
        endpoint=None
    ):
        text = self.text
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(panel)
        endpoint_ctrl = EndpointPanel(panel)
        mute_info_st = panel.StaticText('Muted:')
        mute_info_ctrl = panel.StaticText('     ')

        device_ctrl.set_string_selection(device)
        endpoint_ctrl.set_endpoints(device_ctrl.get_device())
        endpoint_ctrl.set_string_selection(endpoint)

        endpoint = endpoint_ctrl.get_endpoint()

        if endpoint is not None:
            try:
                vol = endpoint.volume
                mute_info_ctrl.SetLabel(unicode(vol.mute))
            except AttributeError:
                panel.EnableButtons(False)

        def on_device_choice(evt):
            def do():
                device = device_ctrl.get_device()
                endpoint_ctrl.set_endpoints(device)
                if device not in (
                    'Default Playback Device',
                    'Default Recording Device'
                ):
                    endpoint_ctrl.set_selection(0)
                    endpoint = endpoint_ctrl.get_endpoint()
                    try:
                        vol = endpoint.volume
                        mute_info_ctrl.SetLabel(unicode(vol.mute))
                        panel.EnableButtons(True)
                    except AttributeError:
                        mute_info_ctrl.SetLabel('     ')
                        panel.EnableButtons(False)
                else:
                    mute_info_ctrl.SetLabel('     ')
                    panel.EnableButtons(True)

            wx.CallAfter(do)
            evt.Skip()

        def on_endpoint_choice(evt):
            def do():
                endpoint = endpoint_ctrl.get_endpoint()
                try:
                    vol = endpoint.volume
                    mute_info_ctrl.SetLabel(unicode(vol.mute))
                    panel.EnableButtons(True)
                except AttributeError:
                    mute_info_ctrl.SetLabel('     ')
                    panel.EnableButtons(False)

            wx.CallAfter(do)
            evt.Skip()

        device_ctrl.Bind(wx.EVT_CHOICE, on_device_choice)
        endpoint_ctrl.Bind(wx.EVT_CHOICE, on_endpoint_choice)

        mute_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mute_sizer.Add(mute_info_st, 0, wx.ALL, 5)
        mute_sizer.Add(mute_info_ctrl, 0, wx.ALL, 5)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(device_ctrl, 1)
        sizer.Add(endpoint_ctrl, 1)
        sizer.Add(mute_sizer)

        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.get_string_selection(),
                endpoint_ctrl.get_string_selection()
            )


class SetEndpointMute(eg.ActionBase):

    def __call__(self, device, endpoint, mute):
        if device == 'Default Playback Device':
            endpoint = pyWinCoreAudio.AudioDevices.default_render_endpoint
        elif device == 'Default Recording Device':
            endpoint = pyWinCoreAudio.AudioDevices.default_capture_endpoint
        else:
            for dev in pyWinCoreAudio.AudioDevices:
                if dev.name == device:
                    for endpt in dev:
                        if endpt.name == endpoint:
                            endpoint = endpt
                            break
                    else:
                        continue
                    break
            else:
                return None
        try:
            endpoint.volume.mute = mute
            return endpoint.volume.mute
        except AttributeError:
            return None

    def Configure(
        self,
        device='Default Playback Device',
        endpoint=None,
        mute=True
    ):
        text = self.text
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(panel)
        endpoint_ctrl = EndpointPanel(panel)
        mute_info_st = panel.StaticText('Muted:')
        mute_info_ctrl = panel.StaticText('     ')
        mute_st = panel.StaticText('Mute:')
        mute_ctrl = wx.CheckBox(panel, -1, '')
        mute_ctrl.SetValue(mute)

        device_ctrl.set_string_selection(device)
        endpoint_ctrl.set_endpoints(device_ctrl.get_device())
        endpoint_ctrl.set_string_selection(endpoint)
        endpoint = endpoint_ctrl.get_endpoint()

        if endpoint is not None:
            try:
                vol = endpoint.volume
                mute_info_ctrl.SetLabel(unicode(vol.mute))
            except AttributeError:
                panel.EnableButtons(False)
                mute_ctrl.Enable(False)

        def on_device_choice(evt):
            def do():
                device = device_ctrl.get_device()
                endpoint_ctrl.set_endpoints(device)
                if device not in (
                    'Default Playback Device',
                    'Default Recording Device'
                ):
                    endpoint_ctrl.set_selection(0)
                    endpoint = endpoint_ctrl.get_endpoint()
                    try:
                        vol = endpoint.volume
                        mute_info_ctrl.SetLabel(unicode(vol.mute))
                        panel.EnableButtons(True)
                        mute_ctrl.Enable(True)

                    except AttributeError:
                        mute_info_ctrl.SetLabel('     ')
                        mute_ctrl.Enable(False)
                        panel.EnableButtons(False)
                else:
                    mute_info_ctrl.SetLabel('     ')
                    mute_ctrl.increment = 1.0
                    panel.EnableButtons(True)
                    mute_ctrl.Enable(True)

            wx.CallAfter(do)
            evt.Skip()

        def on_endpoint_choice(evt):
            def do():
                endpoint = endpoint_ctrl.get_endpoint()
                try:
                    vol = endpoint.volume
                    mute_info_ctrl.SetLabel(unicode(vol.mute))
                    mute_ctrl.Enable(True)
                    panel.EnableButtons(True)
                except AttributeError:
                    mute_info_ctrl.SetLabel('     ')
                    mute_ctrl.Enable(False)
                    panel.EnableButtons(False)

            wx.CallAfter(do)
            evt.Skip()

        device_ctrl.Bind(wx.EVT_CHOICE, on_device_choice)
        endpoint_ctrl.Bind(wx.EVT_CHOICE, on_endpoint_choice)

        mute_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mute_sizer.Add(mute_st, 0, wx.ALL, 15)
        mute_sizer.Add(mute_ctrl, 0, wx.ALL, 15)

        mute_info_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mute_info_sizer.Add(mute_info_st, 0, wx.ALL, 5)
        mute_info_sizer.Add(mute_info_ctrl, 0, wx.ALL, 5)

        m_sizer = wx.BoxSizer(wx.VERTICAL)
        m_sizer.Add(mute_sizer, 0)
        m_sizer.Add(mute_info_sizer, 0)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(device_ctrl, 1)
        sizer.Add(endpoint_ctrl, 1)
        sizer.Add(m_sizer)

        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.get_string_selection(),
                endpoint_ctrl.get_string_selection(),
                mute_ctrl.GetValue()
            )


class ToggleEndpointMute(eg.ActionBase):

    def __call__(self, device, endpoint):
        if device == 'Default Playback Device':
            endpoint = pyWinCoreAudio.AudioDevices.default_render_endpoint
        elif device == 'Default Recording Device':
            endpoint = pyWinCoreAudio.AudioDevices.default_capture_endpoint
        else:
            for dev in pyWinCoreAudio.AudioDevices:
                if dev.name == device:
                    for endpt in dev:
                        if endpt.name == endpoint:
                            endpoint = endpt
                            break
                    else:
                        continue
                    break
            else:
                return None
        try:
            endpoint.volume.mute = not endpoint.volume.mute
            return endpoint.volume.mute
        except AttributeError:
            return None

    def Configure(
        self,
        device='Default Playback Device',
        endpoint=None
    ):
        text = self.text
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(panel)
        endpoint_ctrl = EndpointPanel(panel)
        mute_info_st = panel.StaticText('Muted:')
        mute_info_ctrl = panel.StaticText('     ')

        device_ctrl.set_string_selection(device)
        endpoint_ctrl.set_endpoints(device_ctrl.get_device())
        endpoint_ctrl.set_string_selection(endpoint)

        endpoint = endpoint_ctrl.get_endpoint()

        if endpoint is not None:
            try:
                vol = endpoint.volume
                mute_info_ctrl.SetLabel(unicode(vol.mute))
            except AttributeError:
                panel.EnableButtons(False)

        def on_device_choice(evt):
            def do():
                device = device_ctrl.get_device()
                endpoint_ctrl.set_endpoints(device)
                if device not in (
                    'Default Playback Device',
                    'Default Recording Device'
                ):
                    endpoint_ctrl.set_selection(0)
                    endpoint = endpoint_ctrl.get_endpoint()
                    try:
                        vol = endpoint.volume
                        mute_info_ctrl.SetLabel(unicode(vol.mute))
                        panel.EnableButtons(True)
                    except AttributeError:
                        mute_info_ctrl.SetLabel('     ')
                        panel.EnableButtons(False)
                else:
                    mute_info_ctrl.SetLabel('     ')
                    panel.EnableButtons(True)

            wx.CallAfter(do)
            evt.Skip()

        def on_endpoint_choice(evt):
            def do():
                endpoint = endpoint_ctrl.get_endpoint()
                try:
                    vol = endpoint.volume
                    mute_info_ctrl.SetLabel(unicode(vol.mute))
                    panel.EnableButtons(True)
                except AttributeError:
                    mute_info_ctrl.SetLabel('     ')
                    panel.EnableButtons(False)

            wx.CallAfter(do)
            evt.Skip()

        device_ctrl.Bind(wx.EVT_CHOICE, on_device_choice)
        endpoint_ctrl.Bind(wx.EVT_CHOICE, on_endpoint_choice)

        mute_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mute_sizer.Add(mute_info_st, 0, wx.ALL, 5)
        mute_sizer.Add(mute_info_ctrl, 0, wx.ALL, 5)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(device_ctrl, 1)
        sizer.Add(endpoint_ctrl, 1)
        sizer.Add(mute_sizer)

        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.get_string_selection(),
                endpoint_ctrl.get_string_selection()
            )


class GetSessionVolume(eg.ActionBase):

    def __call__(self, device, endpoint, session):

        for dev in pyWinCoreAudio.AudioDevices:
            if dev.name == device:
                for endpt in dev:
                    if endpt.name == endpoint:
                        try:
                            for sess in endpt:
                                if sess.name == session:
                                    try:
                                        return (
                                            sess.volume.master_scalar * 100.0
                                        )
                                    except AttributeError:
                                        return None

                        except (AttributeError, TypeError):
                            pass
                        return None

                else:
                    return None
        else:
            return None

    def Configure(
        self,
        device='',
        endpoint=None,
        session=''
    ):
        text = self.text
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(panel, use_defaults=False)
        endpoint_ctrl = EndpointPanel(panel)
        session_ctrl = SessionPanel(panel)

        if device:
            device_ctrl.set_string_selection(device)
        else:
            device_ctrl.set_selection(0)

        endpoint_ctrl.set_flow('Render')
        endpoint_ctrl.set_endpoints(device_ctrl.get_device())
        endpoint_ctrl.set_string_selection(endpoint)
        endpoint = endpoint_ctrl.get_endpoint()

        session_ctrl.set_sessions(endpoint)
        session_ctrl.set_string_selection(session)

        def on_device_choice(evt):
            def do():
                device = device_ctrl.get_device()
                endpoint_ctrl.set_endpoints(device)
                endpoint_ctrl.set_selection(0)
                endpoint = endpoint_ctrl.get_endpoint()
                session_ctrl.set_sessions(endpoint)
                session_ctrl.set_selection(0)

            wx.CallAfter(do)
            evt.Skip()

        def on_endpoint_choice(evt):
            def do():
                endpoint = endpoint_ctrl.get_endpoint()
                session_ctrl.set_sessions(endpoint)
                session_ctrl.set_selection(0)

            wx.CallAfter(do)
            evt.Skip()

        device_ctrl.Bind(wx.EVT_CHOICE, on_device_choice)

        endpoint_ctrl.Bind(wx.EVT_CHOICE, on_endpoint_choice)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(device_ctrl, 1)
        sizer.Add(endpoint_ctrl, 1)
        sizer.Add(session_ctrl, 1)

        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.get_string_selection(),
                endpoint_ctrl.get_string_selection(),
                session_ctrl.get_string_selection()
            )


class IsPlaybackEndpointActive(eg.ActionBase):

    def __call__(self, device, endpoint):

        for dev in pyWinCoreAudio.AudioDevices:
            if dev.name == device:
                for endpt in dev:
                    if endpt.name == endpoint:
                        try:
                            for session in endpt:
                                if session.state == 'Active':
                                    return True
                        except (AttributeError, TypeError):
                            pass
                        return False

                else:
                    return False
        else:
            return False

    def Configure(
        self,
        device='',
        endpoint=None
    ):
        text = self.text
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(panel, use_defaults=False)
        endpoint_ctrl = EndpointPanel(panel)
        if device:
            device_ctrl.set_string_selection(device)
        else:
            device_ctrl.set_selection(0)

        endpoint_ctrl.set_flow('Render')
        endpoint_ctrl.set_endpoints(device_ctrl.get_device())
        endpoint_ctrl.set_string_selection(endpoint)

        def on_device_choice(evt):
            def do():
                device = device_ctrl.get_device()
                endpoint_ctrl.set_endpoints(device)
                endpoint_ctrl.set_selection(0)

            wx.CallAfter(do)
            evt.Skip()

        device_ctrl.Bind(wx.EVT_CHOICE, on_device_choice)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(device_ctrl, 1)
        sizer.Add(endpoint_ctrl, 1)

        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.get_string_selection(),
                endpoint_ctrl.get_string_selection()
            )


class IsDefaultPlaybackEndpoint(eg.ActionBase):
    def __call__(self, device, endpoint):

        for dev in pyWinCoreAudio.AudioDevices:
            if dev.name == device:
                for endpt in dev:
                    if endpt.name == endpoint:
                        return endpt.is_default
                else:
                    return False
        else:
            return False

    def Configure(
        self,
        device='',
        endpoint=None
    ):
        text = self.text
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(panel, use_defaults=False)
        endpoint_ctrl = EndpointPanel(panel)
        if device:
            device_ctrl.set_string_selection(device)
        else:
            device_ctrl.set_selection(0)

        endpoint_ctrl.set_flow('Render')
        endpoint_ctrl.set_endpoints(device_ctrl.get_device())
        endpoint_ctrl.set_string_selection(endpoint)

        def on_device_choice(evt):
            def do():
                device = device_ctrl.get_device()
                endpoint_ctrl.set_endpoints(device)
                endpoint_ctrl.set_selection(0)

            wx.CallAfter(do)
            evt.Skip()

        device_ctrl.Bind(wx.EVT_CHOICE, on_device_choice)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(device_ctrl, 1)
        sizer.Add(endpoint_ctrl, 1)

        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.get_string_selection(),
                endpoint_ctrl.get_string_selection()
            )


class GetDefaultPlaybackEndpoint(eg.ActionBase):

    def __call__(self):
        return pyWinCoreAudio.AudioDevices.default_render_endpoint


class SetDefaultPlaybackEndpoint(eg.ActionBase):

    def __call__(self, device, endpoint):

        for dev in pyWinCoreAudio.AudioDevices:
            if dev.name == device:
                for endpt in dev:
                    if endpt.name == endpoint:
                        endpt.set_default()
                        return endpt.is_default
                else:
                    return None
        else:
            return None

    def Configure(
        self,
        device='',
        endpoint=None
    ):
        text = self.text
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(panel, use_defaults=False)
        endpoint_ctrl = EndpointPanel(panel)
        if device:
            device_ctrl.set_string_selection(device)
        else:
            device_ctrl.set_selection(0)

        endpoint_ctrl.set_flow('Render')
        endpoint_ctrl.set_endpoints(device_ctrl.get_device())
        endpoint_ctrl.set_string_selection(endpoint)

        def on_device_choice(evt):
            def do():
                device = device_ctrl.get_device()
                endpoint_ctrl.set_endpoints(device)
                endpoint_ctrl.set_selection(0)

            wx.CallAfter(do)
            evt.Skip()

        device_ctrl.Bind(wx.EVT_CHOICE, on_device_choice)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(device_ctrl, 1)
        sizer.Add(endpoint_ctrl, 1)

        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.get_string_selection(),
                endpoint_ctrl.get_string_selection()
            )


class IsDefaultRecordingEndpoint(eg.ActionBase):

    def __call__(self, device, endpoint):

        for dev in pyWinCoreAudio.AudioDevices:
            if dev.name == device:
                for endpt in dev:
                    if endpt.name == endpoint:
                        return endpt.is_default
                else:
                    return False
        else:
            return False

    def Configure(
        self,
        device='',
        endpoint=None
    ):
        text = self.text
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(panel, use_defaults=False)
        endpoint_ctrl = EndpointPanel(panel)
        if device:
            device_ctrl.set_string_selection(device)
        else:
            device_ctrl.set_selection(0)

        endpoint_ctrl.set_flow('Capture')
        endpoint_ctrl.set_endpoints(device_ctrl.get_device())
        endpoint_ctrl.set_string_selection(endpoint)

        def on_device_choice(evt):
            def do():
                device = device_ctrl.get_device()
                endpoint_ctrl.set_endpoints(device)
                endpoint_ctrl.set_selection(0)

            wx.CallAfter(do)
            evt.Skip()

        device_ctrl.Bind(wx.EVT_CHOICE, on_device_choice)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(device_ctrl, 1)
        sizer.Add(endpoint_ctrl, 1)

        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.get_string_selection(),
                endpoint_ctrl.get_string_selection()
            )


class GetDefaultRecordingEndpoint(eg.ActionBase):

    def __call__(self):
        return pyWinCoreAudio.AudioDevices.default_capture_endpoint


class SetDefaultRecordingEndpoint(eg.ActionBase):

    def __call__(self, device, endpoint):

        for dev in pyWinCoreAudio.AudioDevices:
            if dev.name == device:
                for endpt in dev:
                    if endpt.name == endpoint:
                        endpt.set_default()
                        return endpt.is_default
                else:
                    return None
        else:
            return None

    def Configure(
        self,
        device='',
        endpoint=None
    ):
        text = self.text
        panel = eg.ConfigPanel()

        device_ctrl = DevicePanel(panel, use_defaults=False)
        endpoint_ctrl = EndpointPanel(panel)
        if device:
            device_ctrl.set_string_selection(device)
        else:
            device_ctrl.set_selection(0)

        endpoint_ctrl.set_flow('Capture')
        endpoint_ctrl.set_endpoints(device_ctrl.get_device())
        endpoint_ctrl.set_string_selection(endpoint)

        def on_device_choice(evt):
            def do():
                device = device_ctrl.get_device()
                endpoint_ctrl.set_endpoints(device)
                endpoint_ctrl.set_selection(0)

            wx.CallAfter(do)
            evt.Skip()

        device_ctrl.Bind(wx.EVT_CHOICE, on_device_choice)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(device_ctrl, 1)
        sizer.Add(endpoint_ctrl, 1)

        panel.sizer.Add(sizer)

        while panel.Affirmed():
            panel.SetResult(
                device_ctrl.get_string_selection(),
                endpoint_ctrl.get_string_selection()
            )

def old_get_label(device_id):
    if eg.WindowsVersion >= 'Vista':
        if not device_id:
            device_id = 'Primary Sound Driver'

        if device_id == 'Primary Sound Driver':
            return device_id
        elif not isinstance(device_id, int):
            for device in pyWinCoreAudio.AudioDevices:
                for endpoint in device:
                    if endpoint.name.startswith(device_id):
                        return endpoint.name
            else:
                return device_id

    return SoundMixer.GetDeviceId(device_id)


class OldAudioChoiceCtrl(wx.Choice):

    def __init__(self, parent):
        if eg.WindowsVersion >= 'Vista':
            choices = ['Primary Sound Driver']
            for device in pyWinCoreAudio.AudioDevices:
                for endpoint in device:
                    choices += [endpoint.name]
        else:
            choices = SoundMixer.GetMixerDevices(True)

        wx.Choice.__init__(self, parent, -1, choices=choices)

    def SetStringSelection(self, value):
        if eg.WindowsVersion >= 'Vista':
            if not value:
                value = 'Primary Sound Driver'
            if value in self.GetItems():
                wx.Choice.SetStringSelection(self, value)
            else:
                self.SetSelection(0)
        else:
            self.SetSelection(SoundMixer.GetDeviceId(value))


class MasterVolumeBase(eg.ActionBase):
    name = ''
    description = ''
    iconFile = "icons/SoundCard"
    _min = 0
    _max = 0

    class text:
        text1 = ''
        text2 = ''

    def _set_volume(self, value, device):
        raise NotImplementedError

    def __call__(self, value, deviceId=0):
        value = (
            float(value)
            if isinstance(value, (int, float))
            else float(eg.ParseString(value))
        )

        if eg.WindowsVersion >= 'Vista':
            if not deviceId:
                deviceId = 'Primary Sound Driver'

            if deviceId == 'Primary Sound Driver':
                endpoint = pyWinCoreAudio.AudioDevices.default_render_endpoint
            else:
                for device in pyWinCoreAudio.AudioDevices:
                    for endpoint in device:
                        if endpoint.name.startswith(deviceId):
                            break
                    else:
                        continue
                    break
                else:
                    raise SoundMixer.SoundMixerException(
                        u'Device {0} not found.'.format(deviceId)
                    )

            return self._set_volume(value, endpoint.volume)

        else:
            return self._set_volume(value, deviceId)

    def Configure(self, value=0, deviceId=0):
        panel = eg.ConfigPanel()

        deviceCtrl = OldAudioChoiceCtrl(panel)
        deviceCtrl.SetStringSelection(deviceId)

        valueCtrl = panel.SmartSpinNumCtrl(value, min=self._min, max=self._max)
        sizer = eg.HBoxSizer(
            (panel.StaticText(self.text.text1), 0, wx.ALIGN_CENTER_VERTICAL),
            (valueCtrl, 0, wx.LEFT | wx.RIGHT, 5),
            (panel.StaticText(self.text.text2), 0, wx.ALIGN_CENTER_VERTICAL),
        )

        panel.AddLine(self.plugin.text.device, deviceCtrl)
        panel.AddLine(sizer)
        while panel.Affirmed():
            panel.SetResult(
                valueCtrl.GetValue(),
                deviceCtrl.GetStringSelection(),
            )

    def GetLabel(self, value, deviceId=0):
        primaryDevice = (deviceId == self.plugin.text.primaryDevice)
        deviceId = old_get_label(deviceId)
        if isinstance(value, (int, float)):
            value = float(value)
            if not primaryDevice:
                return "%s #%i: %.2f %%" % (self.name, deviceId + 1, value)
            else:
                return "%s: %.2f %%" % (self.name, value)
        else:
            if not primaryDevice:
                return "%s #%i: %s %%" % (self.name, deviceId + 1, value)
            else:
                return "%s: %s %%" % (self.name, value)


class ChangeMasterVolumeBy(MasterVolumeBase):
    name = "Change Master Volume"
    description = "Changes the master volume relative to the current value."
    _min = -100
    _max = 100

    class text:
        text1 = "Change master volume by"
        text2 = "percent."

    def _set_volume(self, value, device):
        if eg.WindowsVersion >= 'Vista':
            volume = device.master_scalar * 100.00
            volume += value
            device.master_scalar = volume / 100.00
            return device.master_scalar * 100
        else:
            return SoundMixer.ChangeMasterVolumeBy(value, device)


class SetMasterVolume(MasterVolumeBase):
    name = "Set Master Volume"
    description = "Sets the master volume to an absolute value."
    _min = 0
    _max = 100

    class text:
        text1 = "Set master volume to"
        text2 = "percent."

    def _set_volume(self, value, device):
        if eg.WindowsVersion >= 'Vista':
            device.master_scalar = value / 100.00
            return device.master_scalar * 100
        else:
            return SoundMixer.SetMasterVolume(value, device)


class MuteBase(eg.ActionBase):
    name = ''
    description = ''
    iconFile = "icons/SoundCard"
    _mute = None

    def __call__(self, deviceId=0):
        if eg.WindowsVersion >= 'Vista':
            if not deviceId:
                deviceId = 'Primary Sound Driver'

            if deviceId == 'Primary Sound Driver':
                endpoint = pyWinCoreAudio.AudioDevices.default_render_endpoint
            else:
                for device in pyWinCoreAudio.AudioDevices:
                    for endpoint in device:
                        if endpoint.name.startswith(deviceId):
                            break
                    else:
                        continue
                    break
                else:
                    raise SoundMixer.SoundMixerException(
                        u'Device {0} not found.'.format(deviceId)
                    )

            endpoint.volume.mute = self._mute
            return endpoint.volume.mute
        else:
            return SoundMixer.SetMute(self._mute, deviceId)

    def Configure(self, deviceId=0):
        panel = eg.ConfigPanel()

        deviceCtrl = OldAudioChoiceCtrl(panel)
        deviceCtrl.SetStringSelection(deviceId)

        panel.AddLine(self.plugin.text.device, deviceCtrl)
        while panel.Affirmed():
            panel.SetResult(deviceCtrl.GetStringSelection())

    def GetLabel(self, deviceId):
        return self.text.name + ': ' + old_get_label(deviceId)


class MuteOff(MuteBase):
    name = "Turn Mute Off"
    description = "Turns mute off."
    _mute = False


class MuteOn(MuteBase):
    name = "Turn Mute On"
    description = "Turns mute on."
    _mute = True


class GetMute(MuteBase):
    name = "Get Mute Status"
    description = "Gets mute status."

    def __call__(self, deviceId=0):
        if eg.WindowsVersion >= 'Vista':
            if not deviceId:
                deviceId = 'Primary Sound Driver'

            if deviceId == 'Primary Sound Driver':
                endpoint = pyWinCoreAudio.AudioDevices.default_render_endpoint
            else:
                for device in pyWinCoreAudio.AudioDevices:
                    for endpoint in device:
                        if endpoint.name.startswith(deviceId):
                            break
                    else:
                        continue
                    break
                else:
                    raise SoundMixer.SoundMixerException(
                        u'Device {0} not found.'.format(deviceId)
                    )
            return endpoint.volume.mute
        else:
            return SoundMixer.GetMute(deviceId)


class ToggleMute(MuteBase):
    name = "Toggle Mute"
    description = "Toggles mute."

    def __call__(self, deviceId=0):
        if eg.WindowsVersion >= 'Vista':
            if not deviceId:
                deviceId = 'Primary Sound Driver'

            if deviceId == 'Primary Sound Driver':
                endpoint = pyWinCoreAudio.AudioDevices.default_render_endpoint
            else:
                for device in pyWinCoreAudio.AudioDevices:
                    for endpoint in device:
                        if endpoint.name.startswith(deviceId):
                            break
                    else:
                        continue
                    break
                else:
                    raise SoundMixer.SoundMixerException(
                        u'Device {0} not found.'.format(deviceId)
                    )

            endpoint.volume.mute = not endpoint.volume.mute
            return endpoint.volume.mute
        else:
            return SoundMixer.ToggleMute(deviceId)


