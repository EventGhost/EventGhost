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
from ks import PKSMETHOD
from iid import (
    IID_IKsControl,
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
    BYTE,
    LPVOID,
    ULONG
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


LPULONG = POINTER(ULONG)
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


class IKsControl(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IKsControl
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'KsEvent',
            (['in'], ULONG, 'EventLength'),
            (['in', 'out'], LPVOID, 'EventData'),
            (['in'], ULONG, 'DataLength'),
            (['in', 'out'], LPULONG, 'BytesReturned')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'KsMethod',
            (['in'], PKSMETHOD, 'Method'),
            (['in'], ULONG, 'MethodLength'),
            (['in', 'out'], LPVOID, 'MethodData'),
            (['in'], ULONG, 'DataLength'),
            (['in', 'out'], LPULONG, 'BytesReturned')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'KsProperty',
            (['out'], LPHRESULT, 'activateOperation'),
            (['out'], POINTER(PIUnknown), 'activatedInterface')
        ),
    )


PIActivateAudioInterfaceAsyncOperation = POINTER(
    IActivateAudioInterfaceAsyncOperation
)
