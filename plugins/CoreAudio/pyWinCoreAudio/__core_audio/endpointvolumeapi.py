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
from mmdeviceapi import IMMDeviceEnumerator
from comtypes import (
    GUID,
    COMMETHOD,
    CLSCTX_INPROC_SERVER,
)
from iid import (
    IID_IAudioEndpointVolume,
    IID_IAudioEndpointVolumeEx,
    IID_IAudioMeterInformation,
    IID_IAudioEndpointVolumeCallback
)
from ctypes.wintypes import (
    FLOAT,
    UINT,
    DWORD,
    BOOL,
)

UINT32 = ctypes.c_uint32
HRESULT = ctypes.HRESULT
POINTER = ctypes.POINTER
LPCGUID = POINTER(GUID)
LPFLOAT = POINTER(FLOAT)
LPDWORD = POINTER(DWORD)
LPUINT = POINTER(UINT)
LPBOOL = POINTER(BOOL)


class AUDIO_VOLUME_NOTIFICATION_DATA(ctypes.Structure):
    _fields_ = [
        ('guidEventContext', GUID),
        ('bMuted', BOOL),
        ('fMasterVolume', FLOAT),
        ('nChannels', UINT),
        ('afChannelVolumes', (FLOAT * 8))
    ]


PAUDIO_VOLUME_NOTIFICATION_DATA = POINTER(AUDIO_VOLUME_NOTIFICATION_DATA)


class IAudioEndpointVolumeCallback(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioEndpointVolumeCallback
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'OnNotify',
            (['in'], PAUDIO_VOLUME_NOTIFICATION_DATA, 'pNotify')
        ),
    )


PIAudioEndpointVolumeCallback = POINTER(IAudioEndpointVolumeCallback)


class IAudioEndpointVolume(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioEndpointVolume
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'RegisterControlChangeNotify',
            (['in'], PIAudioEndpointVolumeCallback, 'pNotify')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'UnregisterControlChangeNotify',
            (['in'], PIAudioEndpointVolumeCallback, 'pNotify')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetChannelCount',
            (['out'], LPUINT, 'pnChannelCount')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetMasterVolumeLevel',
            (['in'], FLOAT, 'fLevelDB'),
            (['in'], LPCGUID, 'pguidEventContext', None)
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetMasterVolumeLevelScalar',
            (['in'], FLOAT, 'fLevel'),
            (['in'], LPCGUID, 'pguidEventContext', None)
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetMasterVolumeLevel',
            (['out'], LPFLOAT, 'pfLevelDB')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetMasterVolumeLevelScalar',
            (['out'], LPFLOAT, 'pfLevel')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetChannelVolumeLevel',
            (['in'], UINT, 'nChannel'),
            (['in'], FLOAT, 'fLevelDB'),
            (['in'], LPCGUID, 'pguidEventContext', None)
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetChannelVolumeLevelScalar',
            (['in'], UINT, 'nChannel'),
            (['in'], FLOAT, 'fLevel'),
            (['in'], LPCGUID, 'pguidEventContext', None)
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetChannelVolumeLevel',
            (['in'], UINT, 'nChannel'),
            (['out'], LPFLOAT, 'pfLevelDB')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetChannelVolumeLevelScalar',
            (['in'], UINT, 'nChannel'),
            (['out'], LPFLOAT, 'pfLevel')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetMute',
            (['in'], BOOL, 'bMute'),
            (['in'], LPCGUID, 'pguidEventContext', None)
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetMute',
            (['out', 'retval'], LPBOOL, 'pbMute')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetVolumeStepInfo',
            (['out'], LPUINT, 'pnStep'),
            (['out'], LPUINT, 'pnStepCount')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'VolumeStepUp',
            (['in'], LPCGUID, 'pguidEventContext', None)
        ),
        COMMETHOD(
            [],
            HRESULT,
            'VolumeStepDown',
            (['in'], LPCGUID, 'pguidEventContext', None)
        ),
        COMMETHOD(
            [],
            HRESULT,
            'QueryHardwareSupport',
            (['out'], LPDWORD, 'pdwHardwareSupportMask')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetVolumeRange',
            (['out'], LPFLOAT, 'pfLevelMinDB'),
            (['out'], LPFLOAT, 'pfLevelMaxDB'),
            (['out'], LPFLOAT, 'pfVolumeIncrementDB')
        )
    )

    @classmethod
    def get_default(cls):
        endpoint = IMMDeviceEnumerator.get_default(0, 1)
        # EDataFlow.eRender, ERole.eMultimedia)
        interface = endpoint.Activate(cls._iid_, CLSCTX_INPROC_SERVER)
        return ctypes.cast(interface, ctypes.POINTER(cls))


PIAudioEndpointVolume = POINTER(IAudioEndpointVolume)


class IAudioEndpointVolumeEx(IAudioEndpointVolume):
    _case_insensitive_ = True
    _iid_ = IID_IAudioEndpointVolumeEx
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetVolumeRangeChannel',
            (['in'], UINT, 'iChannel'),
            (['out'], LPFLOAT, 'pflVolumeMindB'),
            (['out'], LPFLOAT, 'pflVolumeMaxdB'),
            (['out'], LPFLOAT, 'pflVolumeIncrementdB')
        ),
    )


PIAudioEndpointVolumeEx = POINTER(IAudioEndpointVolumeEx)


class IAudioMeterInformation(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioMeterInformation
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetPeakValue',
            (['out'], LPFLOAT, 'pfPeak')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetMeteringChannelCount',
            (['out'], LPUINT, 'pnChannelCount')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetChannelsPeakValues',
            (['in'], UINT32, 'u32ChannelCount'),
            (['out'], (LPFLOAT * 8), 'afPeakValues')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'QueryHardwareSupport',
            (['out'], LPDWORD, 'pdwHardwareSupportMask')
        )
    )


PIAudioMeterInformation = POINTER(IAudioMeterInformation)
