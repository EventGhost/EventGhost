# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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

import ctypes
import comtypes
import threading
from utils import run_in_thread
from singleton import Singleton
from __core_audio.constant import (
    S_OK,
    ENDPOINT_HARDWARE_SUPPORT_VOLUME,
    ENDPOINT_HARDWARE_SUPPORT_MUTE
)
from __core_audio.iid import (
    IID_IAudioEndpointVolumeEx,
    IID_IAudioMeterInformation
)
from __core_audio.endpointvolumeapi import (
    PIAudioEndpointVolumeEx,
    PIAudioMeterInformation,
    IAudioEndpointVolumeCallback
)


class AudioEndpointVolumeCallback(comtypes.COMObject):
    _com_interfaces_ = [IAudioEndpointVolumeCallback]

    def __init__(self, endpoint, callback):
        self.__volume_lock = threading.Lock()
        self.__endpoint = endpoint
        self.__callback = callback
        comtypes.COMObject.__init__(self)

    def OnNotify(self, pNotify):
        mute = bool(pNotify.contents.bMuted)
        master_volume = pNotify.contents.fMasterVolume
        num_channels = pNotify.contents.nChannels
        pfChannelVolumes = ctypes.cast(
            pNotify.contents.afChannelVolumes,
            ctypes.POINTER(ctypes.c_float)
        )
        channel_volumes = tuple(
            pfChannelVolumes[i] for i in range(num_channels)
        )

        def do():
            with self.__volume_lock:
                self.__callback.endpoint_volume_change(
                    self.__endpoint,
                    master_volume,
                    channel_volumes,
                    mute
                )

        run_in_thread(do)

        return S_OK


class AudioVolumeChannels(object):

    def __init__(self, endpoint, volume):
        self.__endpoint = endpoint
        self.__volume = volume

    @property
    def count(self):
        return self.__volume.GetChannelCount()

    def __getitem__(self, item):
        if isinstance(item, (int, slice)):
            res = []
            for i in range(self.count):
                res += [AudioVolumeChannel(self.__endpoint, self.__volume, i)]
            return res[item]

        raise IndexError


class AudioVolumeChannel(object):

    def __init__(self, endpoint, volume, index):
        self.__endpoint = endpoint
        self.__volume = volume
        self.__index = index

    @property
    def level(self):
        return self.__volume.GetChannelVolumeLevel(self.__index)

    @level.setter
    def level(self, level):
        self.__volume.SetChannelVolumeLevel(self.__index, level)

    @property
    def level_scalar(self):
        return self.__volume.GetChannelVolumeLevelScalar(self.__index)

    @level_scalar.setter
    def level_scalar(self, level):
        self.__volume.SetChannelVolumeLevelScalar(self.__index, level)

    @property
    def min(self):
        return self.__volume.GetVolumeRangeChannel(self.__index)[0]

    @property
    def max(self):
        return self.__volume.GetVolumeRangeChannel(self.__index)[1]

    @property
    def step(self):
        return self.__volume.GetVolumeRangeChannel(self.__index)[2]


class AudioVolume(object):
    __metaclass__ = Singleton

    def __init__(self, endpoint):
        self.__endpoint = endpoint
        self.__volume = endpoint.activate(
            IID_IAudioEndpointVolumeEx,
            PIAudioEndpointVolumeEx
        )
        support = self.__volume.QueryHardwareSupport()
        if support | ENDPOINT_HARDWARE_SUPPORT_VOLUME != support:
            raise NotImplementedError

    @property
    def endpoint(self):
        return self.__endpoint

    @property
    def channels(self):
        return AudioVolumeChannels(self.__endpoint, self.__volume)

    @property
    def master(self):
        return self.__volume.GetMasterVolumeLevel()

    @master.setter
    def master(self, level):
        self.__volume.SetMasterVolumeLevel(level)

    @property
    def master_scalar(self):
        return self.__volume.GetMasterVolumeLevelScalar()

    @master_scalar.setter
    def master_scalar(self, level):
        self.__volume.SetMasterVolumeLevelScalar(level)

    @property
    def mute(self):
        support = self.__volume.QueryHardwareSupport()

        if support | ENDPOINT_HARDWARE_SUPPORT_MUTE == support:
            return bool(self.__volume.GetMute())
        raise AttributeError

    @mute.setter
    def mute(self, mute):
        support = self.__volume.QueryHardwareSupport()

        if support | ENDPOINT_HARDWARE_SUPPORT_MUTE == support:
            self.__volume.SetMute(mute)
        else:
            raise AttributeError

    @property
    def min(self):
        return self.__range[0]

    @property
    def max(self):
        return self.__range[1]

    @property
    def step(self):
        return self.__range[2]

    @property
    def __range(self):
        return self.__volume.GetVolumeRange()

    def register_notification_callback(self, callback):
        volume_callback = AudioEndpointVolumeCallback(
            self.__endpoint,
            callback
        )
        self.__volume.RegisterControlChangeNotify(volume_callback)
        return volume_callback

    def unregister_notification_callback(self, callback):
        self.__volume.UnregisterControlChangeNotify(callback)

    def up(self):
        self.__volume.VolumeStepUp()

    def down(self):
        self.__volume.VolumeStepDown()

    @property
    def peak_meter(self):
        return AudioPeakMeter(self.__endpoint)


class AudioPeakMeter(object):

    def __init__(self, endpoint):
        self.__peak_meter = endpoint.activate(
            IID_IAudioMeterInformation,
            PIAudioMeterInformation
        )

    @property
    def channel_peak_values(self):

        # support = self.__peak_meter.QueryHardwareSupport()
        # if support | ENDPOINT_HARDWARE_SUPPORT_METER != support:
            # raise NotImplementedError
        channels = self.__peak_meter.GetChannelsPeakValues(self.channel_count)

        channel_peaks = ctypes.cast(
            channels,
            ctypes.POINTER(ctypes.c_float)
        )
        return list(
            channel_peaks[i] for i in range(self.channel_count)
        )

    @property
    def channel_count(self):
        return self.__peak_meter.GetMeteringChannelCount()

    @property
    def peak_value(self):
        return self.__peak_meter.GetPeakValue()
