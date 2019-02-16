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
from iid import IID_IAudioMediaType
from audioclient import WAVEFORMATEX
from ctypes.wintypes import (
    BOOL,
    DWORD,
    FLOAT
)

POINTER = ctypes.POINTER
COMMETHOD = comtypes.COMMETHOD
GUID = comtypes.GUID
HRESULT = ctypes.HRESULT
LPBOOL = POINTER(BOOL)
LPDWORD = POINTER(DWORD)


class UNCOMPRESSEDAUDIOFORMAT(ctypes.Structure):
    _fields_ = [
        ('guidFormatType', GUID),
        ('dwSamplesPerFrame', DWORD),
        ('dwBytesPerSampleContainer', DWORD),
        ('dwValidBitsPerSample', DWORD),
        ('fFramesPerSecond', FLOAT),
        ('dwChannelMask', DWORD),
    ]


PUNCOMPRESSEDAUDIOFORMAT = POINTER(UNCOMPRESSEDAUDIOFORMAT)


class IAudioMediaType(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioMediaType


PIAudioMediaType = POINTER(IAudioMediaType)


IAudioMediaType._methods_ = (
    COMMETHOD(
        [],
        HRESULT,
        'IsCompressedFormat',
        (['out'], LPBOOL, 'pfCompressed')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'IsEqual',
        (['in'], PIAudioMediaType, 'pIAudioType'),
        (['out'], LPDWORD, 'pdwFlags'),
    ),
    COMMETHOD(
        [],
        WAVEFORMATEX,
        'GetAudioFormat'
    ),
    COMMETHOD(
        [],
        HRESULT,
        'GetUncompressedAudioFormat',
        (['out'], PUNCOMPRESSEDAUDIOFORMAT, 'pUncompressedAudioFormat'),
    )
)
