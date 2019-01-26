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
from mmdeviceapi import IMMDevice
from audioclient import PWAVEFORMATEX, WAVEFORMATEX
from audioapotypes import (
    APO_CONNECTION_PROPERTY,
    PAPO_CONNECTION_PROPERTY
)
from enum import (
    AE_POSITION_FLAGS,
    EndpointConnectorType,
    AUDIO_CURVE_TYPE
)
from ctypes.wintypes import (
    FLOAT,
    UINT,
    DWORD,
    BOOL,
    HANDLE,
    LPWSTR
)
from _iid import (
    IID_IAudioEndpointLastBufferControl,
    IID_IHardwareAudioEngineBase,
    IID_IAudioLfxControl,
    IID_IAudioEndpointOffloadStreamVolume,
    IID_IAudioEndpointOffloadStreamMute,
    IID_IAudioEndpointOffloadStreamMeter,
    IID_IAudioEndpoint,
    IID_IAudioDeviceEndpoint,
    IID_IAudioEndpointControl,
    IID_IAudioEndpointRT,
    IID_IAudioInputEndpointRT,
    IID_IAudioOutputEndpointRT
)

COMMETHOD = comtypes.COMMETHOD
HNSTIME = ctypes.c_longlong
VOID = ctypes.c_void_p
UINT32 = ctypes.c_uint32
UINT64 = ctypes.c_uint64
FLOAT32 = FLOAT
HRESULT = ctypes.HRESULT
POINTER = ctypes.POINTER
LPBOOL = POINTER(BOOL)
UINT_PTR = POINTER(UINT)


class AUDIO_ENDPOINT_SHARED_CREATE_PARAMS(ctypes.Structure):
    _fields_ = [
        ('u32Size', UINT32),
        ('u32TSSessionId', UINT32),
        ('targetEndpointConnectorType', EndpointConnectorType),
        ('wfxDeviceFormat', WAVEFORMATEX),
    ]


PAUDIO_ENDPOINT_SHARED_CREATE_PARAMS = POINTER(
    AUDIO_ENDPOINT_SHARED_CREATE_PARAMS
)


class AE_CURRENT_POSITION(ctypes.Structure):
    _fields_ = [
        ('u64DevicePosition', UINT64),
        ('u64StreamPosition', UINT64),
        ('u64PaddingFrames', UINT64),
        ('hnsQPCPosition', HNSTIME),
        ('f32FramesPerSecond', FLOAT32),
        ('Flag', AE_POSITION_FLAGS),
    ]


PAE_CURRENT_POSITION = POINTER(AE_CURRENT_POSITION)


class IAudioEndpoint(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioEndpoint
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetFrameFormat',
            (['out'], POINTER(PWAVEFORMATEX), 'ppFormat')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetFramesPerPacket',
            (['out'], POINTER(UINT32), 'pFramesPerPacket')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetLatency',
            (['out'], POINTER(HNSTIME), 'pLatency')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetStreamFlags',
            (['in'], DWORD, 'streamFlags')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetEventHandle',
            (['in'], HANDLE, 'eventHandle')
        )
    )


PIAudioEndpoint = POINTER(IAudioEndpoint)


class IAudioEndpointLastBufferControl(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioEndpointLastBufferControl
    _methods_ = (
        COMMETHOD(
            [],
            BOOL,
            'IsLastBufferControlSupported'
        ),
        COMMETHOD(
            [],
            VOID,
            'ReleaseOutputDataPointerForLastBuffer',
            (['in'], PAPO_CONNECTION_PROPERTY, 'pConnectionProperty'),
        ),
    )


PIAudioEndpointLastBufferControl = POINTER(
    IAudioEndpointLastBufferControl
)


class IAudioLfxControl(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioLfxControl
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'SetLocalEffectsState',
            (['in'], BOOL, 'bEnabled')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetLocalEffectsState',
            (['out'], LPBOOL, 'pbEnabled')
        )
    )


PIAudioLfxControl = POINTER(IAudioLfxControl)


class IHardwareAudioEngineBase(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IHardwareAudioEngineBase
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetAvailableOffloadConnectorCount',
            (['in'], LPWSTR, '_pwstrDeviceId'),
            (['in'], UINT32, '_uConnectorId'),
            (['out'], POINTER(UINT32), '_pAvailableConnectorInstanceCount')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetEngineFormat',
            (['in'], POINTER(IMMDevice), 'pDevice'),
            (['in'], BOOL, '_bRequestDeviceFormat'),
            (['out'], POINTER(PWAVEFORMATEX), '_ppwfxFormat')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetEngineDeviceFormat',
            (['in'], POINTER(IMMDevice), 'pDevice'),
            (['in'], POINTER(WAVEFORMATEX), '_pwfxFormat')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetGfxState',
            (['in'], POINTER(IMMDevice), 'pDevice'),
            (['in'], LPBOOL, '_bEnable')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetGfxState',
            (['in'], POINTER(IMMDevice), 'pDevice'),
            (['out'], LPBOOL, '_bEnable')
        )
    )


PIHardwareAudioEngineBase = POINTER(IHardwareAudioEngineBase)


class IAudioEndpointOffloadStreamVolume(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioEndpointOffloadStreamVolume
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetVolumeChannelCount',
            (['out'], POINTER(UINT32), 'pu32ChannelCount'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetChannelVolumes',
            (['in'], UINT32, 'u32ChannelCount'),
            (['in'], POINTER(FLOAT32), 'pf32Volumes'),
            (['in'], AUDIO_CURVE_TYPE, 'u32CurveType'),
            (['in'], POINTER(HNSTIME), 'pCurveDuration'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetChannelVolumes',
            (['in'], UINT32, 'u32ChannelCount'),
            (['out'], POINTER(FLOAT32), 'pf32Volumes')
        )
    )


PIAudioEndpointOffloadStreamVolume = POINTER(IAudioEndpointOffloadStreamVolume)


class IAudioEndpointOffloadStreamMute(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioEndpointOffloadStreamMute
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'SetMute',
            (['in'], BOOL, 'bMuted')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetMute',
            (['out'], LPBOOL, 'pbMuted')
        )
    )


PIAudioEndpointOffloadStreamMute = POINTER(IAudioEndpointOffloadStreamMute)


class IAudioEndpointOffloadStreamMeter(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioEndpointOffloadStreamMeter
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetMeterChannelCount',
            (['out'], POINTER(UINT32), 'pu32ChannelCount')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetMeteringData',
            (['in'], UINT32, 'u32ChannelCount'),
            (['out'], POINTER(FLOAT32), 'pf32PeakValues')
        )
    )


PIAudioEndpointOffloadStreamMeter = POINTER(IAudioEndpointOffloadStreamMeter)


class IAudioDeviceEndpoint(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioDeviceEndpoint
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'SetBuffer',
            (['in'], HNSTIME, 'MaxPeriod'),
            (['in'], UINT32, 'u32LatencyCoefficient'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetRTCaps',
            (['out', 'retval'], LPBOOL, 'pbIsRTCapable'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetEventDrivenCapable',
            (['out', 'retval'], LPBOOL, 'pbisEventCapable'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'WriteExclusiveModeParametersToSharedMemory',
            (['in'], UINT_PTR, 'hTargetProcess'),
            (['in'], HNSTIME, 'hnsPeriod'),
            (['in'], HNSTIME, 'hnsBufferDuration'),
            (['in'], UINT32, 'u32LatencyCoefficient'),
            (['out'], POINTER(UINT32), 'pu32SharedMemorySize'),
            (['out'], POINTER(UINT_PTR), 'phSharedMemory'),
        )
    )


PIAudioDeviceEndpoint = POINTER(IAudioDeviceEndpoint)


class IAudioEndpointRT(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioEndpointRT
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetCurrentPadding',
            (['out'], POINTER(HNSTIME), 'pPadding'),
            (['out'], POINTER(AE_CURRENT_POSITION), 'pAeCurrentPosition')
        ),
        COMMETHOD(
            [],
            VOID,
            'ProcessingComplete',
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetPinInactive',
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetPinActive',
        )
    )


PIAudioEndpointRT = POINTER(IAudioEndpointRT)


class IAudioInputEndpointRT(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioInputEndpointRT
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetInputDataPointer',
            (
                ['in', 'out'],
                POINTER(APO_CONNECTION_PROPERTY),
                'pConnectionProperty'
            ),
            (['in', 'out'], POINTER(AE_CURRENT_POSITION), 'pAeTimeStamp')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'ReleaseInputDataPointer',
            (['in'], UINT32, 'u32FrameCount'),
            (['in'], UINT_PTR, 'pDataPointer')
        ),
        COMMETHOD(
            [],
            VOID,
            'PulseEndpoint'
        )
    )


PIAudioInputEndpointRT = POINTER(IAudioInputEndpointRT)


class IAudioOutputEndpointRT(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioOutputEndpointRT
    _methods_ = (
        COMMETHOD(
            [],
            UINT_PTR,
            'GetOutputDataPointer',
            (['in'], UINT32, 'u32FrameCount'),
            (['in'], PAE_CURRENT_POSITION, 'pAeTimeStamp'),
        ),
        COMMETHOD(
            [],
            VOID,
            'ReleaseOutputDataPointer',
            (['in'], POINTER(APO_CONNECTION_PROPERTY), 'pConnectionProperty'),
        ),
        COMMETHOD(
            [],
            VOID,
            'PulseEndpoint'
        )
    )


PIAudioOutputEndpointRT = POINTER(IAudioOutputEndpointRT)


class IAudioEndpointControl(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioEndpointControl
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'Start',
            (['in'], VOID)
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Reset',
            (['in'], VOID)
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Stop',
            (['in'], VOID)
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetGfxState',
            (['in'], POINTER(IMMDevice), 'pDevice'),
            (['in'], LPBOOL, '_bEnable')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetGfxState',
            (['in'], POINTER(IMMDevice), 'pDevice'),
            (['out'], LPBOOL, '_bEnable')
        )
    )


PIAudioEndpointControl = POINTER(IAudioEndpointControl)
