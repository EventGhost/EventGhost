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
from iid import (
    IID_IActivateAudioInterfaceAsyncOperation,
    IID_IActivateAudioInterfaceCompletionHandler,
    IID_IAudioCaptureClient,
    IID_IAudioClient,
    IID_IAudioClient2,
    IID_IAudioClient3,
    IID_IAudioClock,
    IID_IAudioClock2,
    IID_IAudioClockAdjustment,
    IID_IAudioRenderClient,
    IID_IAudioStreamVolume,
    IID_IChannelAudioVolume,
    IID_ISimpleAudioVolume,
)
from enum import (
    AUDIO_STREAM_CATEGORY,
    AUDCLNT_STREAMOPTIONS
)

from ctypes.wintypes import (
    FLOAT,
    DWORD,
    BOOL,
    WORD,
    HANDLE,
    BYTE
)


COMMETHOD = comtypes.COMMETHOD
UINT32 = ctypes.c_uint32
UINT64 = ctypes.c_uint64
LONGLONG = ctypes.c_longlong
REFERENCE_TIME = ctypes.c_longlong
HRESULT = ctypes.HRESULT
POINTER = ctypes.POINTER
LPCGUID = POINTER(comtypes.GUID)
LPFLOAT = POINTER(FLOAT)
LPDWORD = POINTER(DWORD)
LPBOOL = POINTER(BOOL)
LPUINT32 = POINTER(UINT32)
LPBYTE = POINTER(BYTE)
LPUINT64 = POINTER(UINT64)
LPREFERENCE_TIME = POINTER(REFERENCE_TIME)
LPHRESULT = POINTER(HRESULT)
PIUnknown = POINTER(comtypes.IUnknown)


class WAVEFORMATEX(ctypes.Structure):
    _fields_ = [
        ('wFormatTag', WORD),
        ('nChannels', WORD),
        ('nSamplesPerSec', WORD),
        ('nAvgBytesPerSec', WORD),
        ('nBlockAlign', WORD),
        ('wBitsPerSample', WORD),
        ('cbSize', WORD),
    ]


PWAVEFORMATEX = POINTER(WAVEFORMATEX)


class AudioClientProperties(ctypes.Structure):
    _fields_ = [
        ('cbSize', UINT32),
        ('bIsOffload', BOOL),
        ('eCategory', AUDIO_STREAM_CATEGORY),
        ('Options', AUDCLNT_STREAMOPTIONS),
    ]


PAudioClientProperties = POINTER(AudioClientProperties)


class IActivateAudioInterfaceAsyncOperation(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IActivateAudioInterfaceAsyncOperation
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetActivateResult',
            (['out'], LPHRESULT, 'activateOperation'),
            (['out'], POINTER(PIUnknown), 'activatedInterface')
        ),
    )


PIActivateAudioInterfaceAsyncOperation = POINTER(
    IActivateAudioInterfaceAsyncOperation
)


class IActivateAudioInterfaceCompletionHandler(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IActivateAudioInterfaceCompletionHandler
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'ActivateCompleted',
            (
                ['in'],
                PIActivateAudioInterfaceAsyncOperation,
                'activateOperation'
            )
        ),
    )


PIActivateAudioInterfaceCompletionHandler = POINTER(
    IActivateAudioInterfaceCompletionHandler
)


class IAudioCaptureClient(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioCaptureClient
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetBuffer',
            (['out'], POINTER(LPBYTE), 'ppData'),
            (['out'], LPUINT32, 'pNumFramesToRead'),
            (['out'], LPDWORD, 'pdwFlags'),
            (['out'], LPUINT64, 'pu64DevicePosition'),
            (['out'], LPUINT64, 'pu64QPCPosition')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'ReleaseBuffer',
            (['in'], UINT32, 'NumFramesWritten'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetNextPacketSize',
            (['out'], LPUINT32, 'pNumFramesInNextPacket'),
        )
    )


PIAudioCaptureClient = POINTER(IAudioCaptureClient)


class IAudioClient(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioClient
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'Initialize',
            (['in'], DWORD, 'ShareMode'),
            (['in'], DWORD, 'StreamFlags'),
            (['in'], LONGLONG, 'hnsBufferDuration'),
            (['in'], LONGLONG, 'hnsPeriodicity'),
            (['in'], PWAVEFORMATEX, 'pFormat'),
            (['in'], LPCGUID, 'AudioSessionGuid')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetBufferSize',
            (['out', 'retval'], LPUINT32, 'pNumBufferFrames')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetStreamLatency',
            (['out', 'retval'], POINTER(LONGLONG), 'phnsLatency')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetCurrentPadding',
            (['out', 'retval'], LPUINT32, 'pNumPaddingFrames')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'IsFormatSupported',
            (['in'], DWORD, 'ShareMode'),
            (['in'], PWAVEFORMATEX, 'pFormat'),
            (['out', 'unique'], POINTER(PWAVEFORMATEX), 'ppClosestMatch')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetMixFormat',
            (['out', 'retval'], POINTER(PWAVEFORMATEX), 'ppDeviceFormat')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetDevicePeriod',
            (['out', 'retval'], POINTER(LONGLONG), 'phnsDefaultDevicePeriod'),
            (['out', 'retval'], POINTER(LONGLONG), 'phnsMinimumDevicePeriod')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetEventHandle',
            (['in'], HANDLE, 'eventHandle'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetService',
            (['in'], LPCGUID, 'iid'),
            (['out'], POINTER(PIUnknown), 'ppv')
        ),
        COMMETHOD([], HRESULT, 'Start'),
        COMMETHOD([], HRESULT, 'Stop'),
        COMMETHOD([], HRESULT, 'Reset'),

    )


PIAudioClient = POINTER(IAudioClient)


class IAudioClient2(IAudioClient):
    _case_insensitive_ = True
    _iid_ = IID_IAudioClient2
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'IsOffloadCapable',
            (['in'], AUDIO_STREAM_CATEGORY, 'Category'),
            (['out'], LPBOOL, 'pbOffloadCapable')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetClientProperties',
            (['in'], PAudioClientProperties, 'pProperties')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetBufferSizeLimits',
            (['in'], PWAVEFORMATEX, 'pFormat'),
            (['in'], BOOL, 'bEventDriven'),
            (['out'], LPREFERENCE_TIME, 'phnsMinBufferDuration'),
            (['out'], LPREFERENCE_TIME, 'phnsMaxBufferDuration')
        )
    )


PIAudioClient2 = POINTER(IAudioClient2)


class IAudioClient3(IAudioClient):
    _case_insensitive_ = True
    _iid_ = IID_IAudioClient3
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'InitializeSharedAudioStream',
            (['in'], DWORD, 'StreamFlags'),
            (['in'], UINT32, 'PeriodInFrames'),
            (['in'], PWAVEFORMATEX, 'pFormat'),
            (['in'], LPCGUID, 'AudioSessionGuid')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetCurrentSharedModeEnginePeriod',
            (['out'], POINTER(PWAVEFORMATEX), 'ppFormat'),
            (['out'], LPUINT32, 'pCurrentPeriodInFrames'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetSharedModeEnginePeriod',
            (['in'], PWAVEFORMATEX, 'pFormat'),
            (['out'], LPUINT32, 'pDefaultPeriodInFrames'),
            (['out'], LPUINT32, 'pFundamentalPeriodInFrames'),
            (['out'], LPUINT32, 'pMinPeriodInFrames'),
            (['out'], LPUINT32, 'pMaxPeriodInFrames')
        )
    )


PIAudioClient3 = POINTER(IAudioClient3)


class IAudioClock(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioClock
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetFrequency',
            (['out'], LPUINT64, 'pu64Frequency')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetPosition',
            (['out'], LPUINT64, 'pu64Position'),
            (['out'], LPUINT64, 'pu64QPCPosition'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetCharacteristics',
            (['out'], LPDWORD, 'pdwCharacteristics'),
        )
    )


PIAudioClock = POINTER(IAudioClock)


class IAudioClock2(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioClock2
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetDevicePosition',
            (['out'], LPUINT64, 'DevicePosition'),
            (['out'], LPUINT64, 'QPCPosition'),
        ),
    )


PIAudioClock2 = POINTER(IAudioClock2)


class IAudioClockAdjustment(comtypes.IUnknown):
    _iid_ = IID_IAudioClockAdjustment
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'SetSampleRate',
            (['in'], FLOAT, 'flSampleRate')
        ),
    )


PIAudioClockAdjustment = POINTER(IAudioClockAdjustment)


class IAudioRenderClient(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioRenderClient
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetBuffer',
            (['in'], UINT32, 'NumFramesRequested'),
            (['out'], POINTER(LPBYTE), 'PeriodInFrames')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'ReleaseBuffer',
            (['in'], UINT32, 'NumFramesWritten'),
            (['in'], DWORD, 'dwFlags'),
        )
    )


PIAudioRenderClient = POINTER(IAudioRenderClient)


class ISimpleAudioVolume(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_ISimpleAudioVolume
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'SetMasterVolume',
            (['in'], FLOAT, 'fLevel'),
            (['in'], LPCGUID, 'EventContext')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetMasterVolume',
            (['out', 'retval'], LPFLOAT, 'pfLevel')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetMute',
            (['in'], BOOL, 'bMute'),
            (['in'], LPCGUID, 'EventContext')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetMute',
            (['out', 'retval'], LPBOOL, 'pbMute')
        )
    )


PISimpleAudioVolume = POINTER(ISimpleAudioVolume)


class IAudioStreamVolume(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioStreamVolume
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetChannelCount',
            (['out'], LPUINT32, 'pdwCount')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetChannelVolume',
            (['in'], UINT32, 'dwIndex'),
            (['in'], FLOAT, 'fLevel')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetChannelVolume',
            (['in'], UINT32, 'dwIndex'),
            (['out'], LPFLOAT, 'pfLevel')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetAllVolumes',
            (['in'], UINT32, 'dwCount'),
            (['in'], LPFLOAT, 'pfVolumes')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetAllVolumes',
            (['in'], UINT32, 'dwCount'),
            (['out'], LPFLOAT, 'pfVolumes')
        ),
    )


PIAudioStreamVolume = POINTER(IAudioStreamVolume)


class IChannelAudioVolume(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IChannelAudioVolume
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetChannelCount',
            (['out'], LPUINT32, 'pdwCount')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetChannelVolume',
            (['in'], UINT32, 'dwIndex'),
            (['in'], FLOAT, 'pfLevel')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetChannelVolume',
            (['in'], UINT32, 'dwIndex'),
            (['out'], LPFLOAT, 'pfLevel')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetAllVolumes',
            (['in'], UINT32, 'dwCount'),
            (['in'], LPFLOAT, 'pfVolumes')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetAllVolumes',
            (['in'], UINT32, 'dwCount'),
            (['out'], LPFLOAT, 'pfVolumes')
        ),
    )


PIChannelAudioVolume = POINTER(IChannelAudioVolume)
