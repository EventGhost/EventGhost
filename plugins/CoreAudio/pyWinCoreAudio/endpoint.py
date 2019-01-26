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


import comtypes
import ctypes
from ctypes.wintypes import (
DWORD,
BYTE,
)
from singleton import Singleton
from utils import get_icon
from __core_audio.audioclient import (
    PIAudioClient,
    PIAudioClient2,
    PIAudioClient3
)

from session import AudioSessionManager
from speaker import AudioSpeakers
from volume import AudioVolume
from jack import (
    AudioJackDescription,
    AudioJackSinkInformation
)
from parts import (
    AudioDeviceConnection,
    AudioDeviceSubunit,
)

from __core_audio.enum import (
    EDataFlow,
    ERole,
    EndpointFormFactor,
    EndpointConnectorType
)
from __core_audio.policyconfig import IPolicyConfigVista

from __core_audio.mmdeviceapi import (
    IMMDeviceEnumerator,
    IMMEndpoint,
)
from __core_audio.devicetopologyapi import (
    PIDeviceTopology,
    PIAudioBass,
    PIKsJackDescription,
    PIKsJackDescription2,
    PIKsJackSinkInformation,
    PIAudioOutputSelector,
    PIAudioInputSelector,
    PIAudioChannelConfig,
    PIAudioAutoGainControl,
    PIAudioPeakMeter,
    PIAudioMidrange,
    PIAudioLoudness,
    PIAudioTreble,
)
from __core_audio.iid import (
    IID_IAudioAutoGainControl,
    IID_IAudioBass,
    IID_IAudioChannelConfig,
    IID_IAudioInputSelector,
    IID_IAudioLoudness,
    IID_IAudioMidrange,
    IID_IAudioOutputSelector,
    IID_IAudioPeakMeter,
    IID_IAudioTreble,
    IID_IAudioClient,
    IID_IAudioClient2,
    IID_IAudioClient3,
    IID_IDeviceTopology,
    IID_IKsJackDescription,
    IID_IKsJackDescription2,
    IID_IKsJackSinkInformation,
    CLSID_MMDeviceEnumerator,
    CLSID_PolicyConfigVistaClient
)

from __core_audio.constant import (
    PKEY_Device_FriendlyName,
    DEVPKEY_DeviceClass_IconPath,
    PKEY_Device_DeviceDesc,
    PKEY_AudioEndpoint_Disable_SysFx,
    PKEY_AudioEndpoint_PhysicalSpeakers,
    PKEY_AudioEndpoint_GUID,
    PKEY_AudioEndpoint_FullRangeSpeakers,
    PKEY_AudioEndpoint_FormFactor,
    PKEY_AudioEndpoint_JackSubType,
    STGM_READ
)

CLSCTX_INPROC_SERVER = comtypes.CLSCTX_INPROC_SERVER

E_DATA_FLOW = {
    EDataFlow.eRender:              'Render',
    EDataFlow.eCapture:             'Capture',
    EDataFlow.eAll:                 'All',
    EDataFlow.EDataFlow_enum_count: 'EDataFlow_enum_count'
}


ENDPOINT_CONNECTOR_TYPE = {
    EndpointConnectorType.eHostProcessConnector:     'Host Process Connector',
    EndpointConnectorType.eOffloadConnector:         'Offload Connector',
    EndpointConnectorType.eLoopbackConnector:        'Loopback Connector',
    EndpointConnectorType.eConnectorCount:           'Connector Count',
    EndpointConnectorType.eKeywordDetectorConnector: (
        'Keyword Detector Connector'
    ),
}

ENDPOINT_FORM_FACTOR = {
    EndpointFormFactor.RemoteNetworkDevice:           'Remote Network Device',
    EndpointFormFactor.Speakers:                      'Speakers',
    EndpointFormFactor.LineLevel:                     'Line Level',
    EndpointFormFactor.Headphones:                    'Headphones',
    EndpointFormFactor.Microphone:                    'Microphone',
    EndpointFormFactor.Headset:                       'Headset',
    EndpointFormFactor.Handset:                       'Handset',
    EndpointFormFactor.SPDIF:                         'SPDIF',
    EndpointFormFactor.UnknownFormFactor:             'Unknown Form Factor',
    EndpointFormFactor.DigitalAudioDisplayDevice:     (
        'Digital Audio Display Device'
    ),
    EndpointFormFactor.UnknownDigitalPassthrough:     (
        'Unknown Digital Passthrough'
    ),
    EndpointFormFactor.EndpointFormFactor_enum_count: (
        'EndpointFormFactor_enum_count'
    )
}


class AudioDefaultEndpoint(object):

    def __init__(self, device_enum, data_flow):
        self.__device_enum = device_enum
        for key, value in E_DATA_FLOW.items():
            if data_flow in (key, value):
                data_flow = key
                break
        else:
            raise AttributeError

        self.__data_flow = data_flow

    @property
    def data_flow(self):
        return self.__data_flow

    @property
    def __default_endpoint(self):
        from device import AudioDevice

        endpoint = self.__device_enum.default_endpoint(self.__data_flow)

        device_topology = comtypes.cast(
            endpoint.Activate(
                IID_IDeviceTopology,
                CLSCTX_INPROC_SERVER
            ),
            PIDeviceTopology
        )

        device = AudioDevice(
            device_topology.GetDeviceId(),
            self.__device_enum
        )

        endpoint_id = endpoint.GetId()

        for endpoint in device:
            if endpoint.id == endpoint_id:
                return endpoint

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        endpoint = self.__default_endpoint
        if endpoint is not None:
            return getattr(endpoint, item)

        raise AttributeError


class AudioEndpoint(object):
    __metaclass__ = Singleton

    def __init__(
        self,
        parent,
        endpoint_id,
        device_enum
    ):
        self.__parent = parent
        self.__endpoint_id = endpoint_id
        self.__device_enum = device_enum
        self.__endpoint = self.__device_enum.get_device(endpoint_id)
        self.activate = self.__activate

    @property
    def __device_topology(self):
        return comtypes.cast(
            self.__endpoint.Activate(
                IID_IDeviceTopology,
                CLSCTX_INPROC_SERVER
            ),
            PIDeviceTopology
        )

    @property
    def __connector(self):
        device_topology = self.__device_topology
        return AudioDeviceConnection(device_topology.GetConnector(0))

    @property
    def __subunits(self):
        device_topology = self.__device_topology
        for i in range(device_topology.GetSubunitCount()):
            subunit = device_topology.GetSubunit(i)

            yield AudioDeviceSubunit(
                subunit
            )

    @property
    def icon(self):
        pStore = self.__endpoint.OpenPropertyStore(STGM_READ)
        # try:
        return get_icon(pStore.GetValue(DEVPKEY_DeviceClass_IconPath))
        # except comtypes.COMError:
        #     pass

    def __activate(self, iid, pointer):
        try:
            return comtypes.cast(
                self.__endpoint.Activate(
                    iid,
                    CLSCTX_INPROC_SERVER
                ),
                pointer
            )
        except comtypes.COMError:
            raise AttributeError

    def __property(self, key):
        pStore = self.__endpoint.OpenPropertyStore(STGM_READ)
        try:
            return pStore.GetValue(key)
        except comtypes.COMError:
            raise AttributeError

    def __get_interface(self, iid, pointer):

        conn_from = self.__connector

        while True:
            try:
                conn_from = conn_from.connected_to
            except comtypes.COMError:
                return

            part = conn_from.part
            device_topology = part.device_topology

            for i in range(device_topology.GetSubunitCount()):
                subunit = AudioDeviceSubunit(device_topology.GetSubunit(i))
                part = subunit.part
                try:
                    interface = part.activate(iid, pointer)
                    print interface
                    return interface
                except comtypes.COMError:
                    continue

            if conn_from.type == 'Software IO':
                raise AttributeError

            if not conn_from.is_connected:
                raise AttributeError

    def set_default(self):
        policy_config = comtypes.CoCreateInstance(
            CLSID_PolicyConfigVistaClient,
            IPolicyConfigVista,
            comtypes.CLSCTX_ALL
        )

        policy_config.SetDefaultEndpoint(self.id, ERole.eMultimedia)

    @property
    def device(self):
        return self.__parent

    @property
    def id(self):
        return self.__endpoint_id

    def play_audio_stream(self, audio_data):
        hnsRequestedDuration = REFERENCE_TIME(REFTIMES_PER_SEC)
        hnsActualDuration = REFERENCE_TIME
        pwfx = PWAVEFORMATEX
        bufferFrameCount = UINT32
        numFramesAvailable = UINT32
        numFramesPadding = UINT32
        pData = LPBYTE
        flags = DWORD(0)
        pAudioClient = self.audio_client
        pAudioClient.GetMixFormat(pwfx)


    @property
    def audio_client(self):
        try:
            return self.__activate(
                IID_IAudioClient3,
                PIAudioClient3
            )
        except comtypes.COMError:
            pass

        try:
            return self.__activate(
                IID_IAudioClient2,
                PIAudioClient2
            )
        except comtypes.COMError:
            pass

        try:
            return self.__activate(
                IID_IAudioClient,
                PIAudioClient
            )
        except comtypes.COMError:
            pass


    @property
    def session_manager(self):
        try:
            return AudioSessionManager(self)
        except NotImplementedError:
            raise AttributeError

    def __iter__(self):
        try:
            for session in self.session_manager:
                yield session
        except AttributeError:
            pass

    @property
    def data_flow(self):
        try:
            endpoint = self.__endpoint.QueryInterface(IMMEndpoint)
            return E_DATA_FLOW[endpoint.GetDataFlow().value]
        except comtypes.COMError:
            raise AttributeError

    @property
    def name(self):
        """Return an endpoint devices FriendlyName."""
        return self.__property(PKEY_Device_FriendlyName)

    @property
    def description(self):
        return self.__property(PKEY_Device_DeviceDesc)

    @property
    def form_factor(self):
        form_factor = self.__property(PKEY_AudioEndpoint_FormFactor)
        return ENDPOINT_FORM_FACTOR[form_factor]

    @property
    def type(self):
        return self.__property(PKEY_AudioEndpoint_JackSubType)

    @property
    def full_range_speakers(self):
        return AudioSpeakers(
            self.__property(PKEY_AudioEndpoint_FullRangeSpeakers)
        )

    @property
    def guid(self):
        return self.__property(PKEY_AudioEndpoint_GUID)

    @property
    def physical_speakers(self):
        return AudioSpeakers(
            self.__property(PKEY_AudioEndpoint_PhysicalSpeakers)
        )

    @property
    def system_effects(self):
        return bool(
            self.__property(PKEY_AudioEndpoint_Disable_SysFx)
        )

    @property
    def jack_descriptions(self):
        conn_from = self.__connector
        try:
            conn_to = conn_from.connected_to
        except comtypes.COMError:
            raise AttributeError
        part = conn_to.part

        try:
            jack_description = part.activate(
                IID_IKsJackDescription,
                PIKsJackDescription
            )
        except comtypes.COMError:
            raise AttributeError

        try:
            jack_description2 = part.activate(
                IID_IKsJackDescription2,
                PIKsJackDescription2
            )
        except comtypes.COMError:
            jack_description2 = None

        for i in range(jack_description.GetJackCount()):
            jd = jack_description.GetJackDescription(i)
            if jack_description2 is None:
                jd2 = None
            else:
                jd2 = jack_description2.GetJackDescription2(i)
            yield AudioJackDescription(jd, jd2)

    @property
    def jack_information(self):
        conn_from = self.__connector
        try:
            conn_to = conn_from.connected_to
        except comtypes.COMError:
            raise AttributeError

        part = conn_to.part

        try:
            return AudioJackSinkInformation(
                part.activate(
                    IID_IKsJackSinkInformation,
                    PIKsJackSinkInformation
                )
            )
        except comtypes.COMError:
            raise AttributeError

    @property
    def auto_gain_control(self):
        return self.__get_interface(
            IID_IAudioAutoGainControl,
            PIAudioAutoGainControl
        )

    @property
    def bass(self):
        return self.__get_interface(
            IID_IAudioBass,
            PIAudioBass
        )

    @property
    def channel_config(self):
        return self.__get_interface(
            IID_IAudioChannelConfig,
            PIAudioChannelConfig
        )

    @property
    def input(self):
        return self.__get_interface(
            IID_IAudioInputSelector,
            PIAudioInputSelector
        )

    @property
    def loudness(self):
        return self.__get_interface(
            IID_IAudioLoudness,
            PIAudioLoudness
        )

    @property
    def midrange(self):
        return self.__get_interface(
            IID_IAudioMidrange,
            PIAudioMidrange
        )

    @property
    def output(self):
        return self.__get_interface(
            IID_IAudioOutputSelector,
            PIAudioOutputSelector
        )

    @property
    def peak_meter(self):
        return self.__get_interface(
            IID_IAudioPeakMeter,
            PIAudioPeakMeter
        )

    @property
    def treble(self):
        return self.__get_interface(
            IID_IAudioTreble,
            PIAudioTreble
        )

    @property
    def volume(self):
        try:
            return AudioVolume(self)
        except NotImplementedError:
            raise AttributeError

    @property
    def format_support(self):
        raise NotImplementedError
        # if str(IID_IKsFormatSupport) == str(interface.GetIID()):
        #     part = self.__connector.QueryInterface(IPart)
        #
        #     control = comtypes.cast(
        #         part.Activate(
        #             comtypes.CLSCTX_INPROC_SERVER,
        #             IID_IKsFormatSupport
        #         ),
        #         PIKsFormatSupport
        #     )
        #     print 'IKsFormatSupport:', control
        #
        #     return None

    @property
    def is_default(self):
        endpoint = self.__endpoint.QueryInterface(IMMEndpoint)

        default = self.__device_enum.default_endpoint(
            endpoint.GetDataFlow().value
        )
        return default.GetId() == self.id
