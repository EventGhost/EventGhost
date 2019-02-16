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
import threading
from singleton import Singleton
from endpoint import AudioEndpoint
from parts import AudioDeviceConnection
from utils import run_in_thread, get_icon

from __core_audio.mmdeviceapi import (
    IMMDeviceEnumerator,
    IMMNotificationClient
)
from __core_audio.devicetopologyapi import (
    PIDeviceTopology,
    IPart
)
from __core_audio.enum import (
    AudioDeviceState,
    EDataFlow,
    ERole
)
from __core_audio.iid import (
    IID_IDeviceTopology,
    CLSID_MMDeviceEnumerator
)
from __core_audio.constant import (
    S_OK,
    PKEY_DeviceInterface_FriendlyName,
    DEVPKEY_DeviceClass_IconPath,
    STGM_READ,
    DEVICE_STATE_MASK_ALL
)

CLSCTX_INPROC_SERVER = comtypes.CLSCTX_INPROC_SERVER

AUDIO_DEVICE_STATE = {
    AudioDeviceState.Active:     'Active',
    AudioDeviceState.Disabled:   'Disabled',
    AudioDeviceState.NotPresent: 'Not Present',
    AudioDeviceState.Unplugged:  'Unplugged'
}


class AudioDevice(object):
    __metaclass__ = Singleton

    def __init__(self, dev_id, device_enum):
        self.__id = dev_id
        self.__device_enum = device_enum

    @property
    def __device(self):
        return self.__device_enum.get_device(self.__id)

    @property
    def __device_topology(self):
        return comtypes.cast(
            self.__device.Activate(
                IID_IDeviceTopology,
                CLSCTX_INPROC_SERVER
            ),
            PIDeviceTopology
        )

    @property
    def __connectors(self):
        name = self.name
        for endpoint in self.__device_enum.endpoints:

            pStore = endpoint.OpenPropertyStore(STGM_READ)
            try:
                item_name = pStore.GetValue(PKEY_DeviceInterface_FriendlyName)
            except comtypes.COMError:
                continue

            if item_name == name:
                for j in range(self.__device_topology.GetConnectorCount()):
                    yield AudioDeviceConnection(
                        self.__device_topology.GetConnector(j)
                    )

    @property
    def __subunits(self):
        for i in range(self.__device_topology.GetSubunitCount()):
            subunit = self.__device_topology.GetSubunit(i)
            yield subunit.QueryInterface(IPart)

    @property
    def connectors(self):
        return self.__connectors

    @property
    def state(self):
        return AUDIO_DEVICE_STATE[self.__device.GetState()]

    @property
    def connector_count(self):
        return self.__device_topology.GetConnectorCount()

    @property
    def id(self):
        return self.__device_topology.GetDeviceId()

    @property
    def icon(self):
        pStore = self.__device.OpenPropertyStore(STGM_READ)
        try:
            return get_icon(pStore.GetValue(DEVPKEY_DeviceClass_IconPath))
        except comtypes.COMError:
            pass

    @property
    def name(self):
        pStore = self.__device.OpenPropertyStore(STGM_READ)
        try:
            return pStore.GetValue(PKEY_DeviceInterface_FriendlyName)
        except comtypes.COMError:
            pass

    @property
    def render_endpoints(self):
        return list(self.__endpoints(EDataFlow.eRender))

    @property
    def capture_endpoints(self):
        return list(self.__endpoints(EDataFlow.eCapture))

    def __endpoints(self, data_flow):
        endpoint_enum = self.__device_enum.endpoint_enum(data_flow)
        device_name = self.name

        for i in range(endpoint_enum.GetCount()):
            endpoint = endpoint_enum.Item(i)

            pStore = endpoint.OpenPropertyStore(STGM_READ)
            try:
                name = pStore.GetValue(PKEY_DeviceInterface_FriendlyName)
            except comtypes.COMError:
                continue

            if name == device_name:
                yield AudioEndpoint(
                    self,
                    endpoint.GetId(),
                    self.__device_enum
                )

    def __iter__(self):
        return iter(self.__endpoints(EDataFlow.eAll))


class AudioDeviceEnumerator(object):

    def __init__(self):
        self.__device_enum = comtypes.CoCreateInstance(
            CLSID_MMDeviceEnumerator,
            IMMDeviceEnumerator,
            comtypes.CLSCTX_INPROC_SERVER
        )

    def register_endpoint_notification_callback(self, client):
        self.__device_enum.RegisterEndpointNotificationCallback(
            client
        )

    def unregister_endpoint_notification_callback(self, client):
        self.__device_enum.UnregisterEndpointNotificationCallback(
            client
        )

    def default_endpoint(self, data_flow):
        return self.__device_enum.GetDefaultAudioEndpoint(
            data_flow,
            ERole.eMultimedia,
        )

    def get_device(self, device_id):
        return self.__device_enum.GetDevice(device_id)

    @property
    def endpoints(self):
        endpoint_enum = self.__device_enum.EnumAudioEndpoints(
            EDataFlow.eAll,
            DEVICE_STATE_MASK_ALL
        )

        for i in range(endpoint_enum.GetCount()):
            yield endpoint_enum.Item(i)

    def endpoint_enum(self, data_flow):
        return self.__device_enum.EnumAudioEndpoints(
            data_flow,
            DEVICE_STATE_MASK_ALL
        )


class AudioNotificationClient(comtypes.COMObject):
    _com_interfaces_ = [IMMNotificationClient]

    def __init__(self, device_enum, callbacks):
        self.__device_enum = device_enum
        self.__callbacks = callbacks
        self.__default_endpoint_lock = threading.Lock()
        comtypes.COMObject.__init__(self)

    def __get_device(self, device_id):
        device = self.__device_enum.get_device(device_id)
        device_topology = comtypes.cast(
            device.Activate(
                IID_IDeviceTopology,
                CLSCTX_INPROC_SERVER
            ),
            PIDeviceTopology
        )

        return AudioDevice(
            device_topology.GetDeviceId(),
            self.__device_enum
        )

    def OnDeviceStateChanged(self, pwstrDeviceId, dwNewState):
        device = self.__get_device(pwstrDeviceId)
        state = AUDIO_DEVICE_STATE[dwNewState]

        def do():
            for callback in self.__callbacks:
                try:
                    callback.device_state_change(device, state)
                except AttributeError:
                    pass

        run_in_thread(do)

        return S_OK

    def OnDeviceAdded(self, pwstrDeviceId):
        device = self.__get_device(pwstrDeviceId)

        def do():
            for callback in self.__callbacks:
                try:
                    callback.device_added(device)
                except AttributeError:
                    pass

        run_in_thread(do)

        return S_OK

    def OnDeviceRemoved(self, pwstrDeviceId):
        device = self.__get_device(pwstrDeviceId)

        def do():
            for callback in self.__callbacks:
                try:
                    callback.device_removed(device)
                except AttributeError:
                    pass

        run_in_thread(do)

        return S_OK

    def OnDefaultDeviceChanged(self, _, __, pwstrDefaultDeviceId):
        device = self.__get_device(pwstrDefaultDeviceId)

        def do():
            with self.__default_endpoint_lock:
                for callback in self.__callbacks:
                    try:
                        callback.default_endpoint_changed(device)
                    except AttributeError:
                        pass

        run_in_thread(do)

        return S_OK

    def OnPropertyValueChanged(self, pwstrDeviceId, key):
        device = self.__get_device(pwstrDeviceId)

        def do():
            for callback in self.__callbacks:
                try:
                    callback.device_property_changed(device, key)
                except AttributeError:
                    pass

        run_in_thread(do)

        return S_OK
