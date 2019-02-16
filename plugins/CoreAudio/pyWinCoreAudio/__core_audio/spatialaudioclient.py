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
from audioclient import PWAVEFORMATEX
from mmdeviceapi import PPROPVARIANT
from enum import (
    AUDIO_STREAM_CATEGORY,
    AudioObjectType,
    PAudioObjectType
)
from ctypes.wintypes import (
    FLOAT,
    INT,
    BOOL,
    HANDLE,
    LPVOID,
    BYTE
)
from iid import (
    IID_IAudioFormatEnumerator,
    IID_ISpatialAudioObjectBase,
    IID_ISpatialAudioObject,
    IID_ISpatialAudioObjectRenderStreamBase,
    IID_ISpatialAudioObjectRenderStream,
    IID_ISpatialAudioObjectRenderStreamNotify,
    IID_ISpatialAudioClient
)

GUID = comtypes.GUID
COMMETHOD = comtypes.COMMETHOD
UINT32 = ctypes.c_uint32
LONGLONG = ctypes.c_longlong
HRESULT = ctypes.HRESULT
POINTER = ctypes.POINTER
REFIID = POINTER(GUID)
LPFLOAT = POINTER(FLOAT)
LPBOOL = POINTER(BOOL)
LPUINT32 = POINTER(UINT32)
LPBYTE = POINTER(BYTE)


class ISpatialAudioObjectRenderStreamNotify(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_ISpatialAudioObjectRenderStreamNotify


PISpatialAudioObjectRenderStreamNotify = POINTER(
    ISpatialAudioObjectRenderStreamNotify
)


class SpatialAudioObjectRenderStreamActivationParams(ctypes.Structure):
    _fields_ = [
        ('ObjectFormat', PWAVEFORMATEX),
        ('StaticObjectTypeMask', AudioObjectType),
        ('MinDynamicObjectCount', UINT32),
        ('MaxDynamicObjectCount', UINT32),
        ('Category', AUDIO_STREAM_CATEGORY),
        ('EventHandle', HANDLE),
        ('NotifyObject', PISpatialAudioObjectRenderStreamNotify),
    ]


PSpatialAudioObjectRenderStreamActivationParams = POINTER(
    SpatialAudioObjectRenderStreamActivationParams
)


class IAudioFormatEnumerator(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioFormatEnumerator
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetCount',
            (['out'], LPUINT32, 'count')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetFormat',
            (['in'], UINT32, 'index'),
            (['out'], POINTER(PWAVEFORMATEX), 'format')
        )
    )


PIAudioFormatEnumerator = POINTER(IAudioFormatEnumerator)


class ISpatialAudioObjectBase(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_ISpatialAudioObjectBase
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetBuffer',
            (['out'], POINTER(LPBYTE), 'buffer'),
            (['out'], LPUINT32, 'bufferLength'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetEndOfStream',
            (['in'], UINT32, 'frameCount')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'IsActive',
            (['out'], LPBOOL, 'isActive')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetAudioObjectType',
            (['out'], PAudioObjectType, 'audioObjectType')
        )
    )


PISpatialAudioObjectBase = POINTER(ISpatialAudioObjectBase)


class ISpatialAudioObject(ISpatialAudioObjectBase):
    _case_insensitive_ = True
    _iid_ = IID_ISpatialAudioObject
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'SetPosition',
            (['in'], FLOAT, 'x'),
            (['in'], FLOAT, 'y'),
            (['in'], FLOAT, 'z'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetVolume',
            (['in'], FLOAT, 'volume')
        )
    )


PISpatialAudioObject = POINTER(ISpatialAudioObject)


class ISpatialAudioObjectRenderStreamBase(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_ISpatialAudioObjectRenderStreamBase
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetAvailableDynamicObjectCount',
            (['out'], LPUINT32, 'value')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetService',
            (['in'], REFIID, 'riid'),
            (['out'], POINTER(LPVOID), 'service')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Start'
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Stop'
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Reset'
        ),
        COMMETHOD(
            [],
            HRESULT,
            'BeginUpdatingAudioObjects',
            (['out'], LPUINT32, 'availableDynamicObjectCount'),
            (['out'], LPUINT32, 'frameCountPerBuffer')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'EndUpdatingAudioObjects'
        )
    )


PISpatialAudioObjectRenderStreamBase = POINTER(
    ISpatialAudioObjectRenderStreamBase
)


class ISpatialAudioObjectRenderStream(ISpatialAudioObjectRenderStreamBase):
    _case_insensitive_ = True
    _iid_ = IID_ISpatialAudioObjectRenderStream
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'ActivateSpatialAudioObject',
            (['in'], AudioObjectType, 'type'),
            (['out'], POINTER(PISpatialAudioObject), 'audioObject'),
        ),
    )


PISpatialAudioObjectRenderStream = POINTER(ISpatialAudioObjectRenderStream)


ISpatialAudioObjectRenderStreamNotify._methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'OnAvailableDynamicObjectCountChange',
            (['in'], PISpatialAudioObjectRenderStreamBase, 'pwstrDeviceId'),
            (['in'], LONGLONG, 'hnsComplianceDeadlineTime'),
            (['in'], UINT32, 'availableDynamicObjectCountChange'),
        ),
    )


class ISpatialAudioClient(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_ISpatialAudioClient
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetStaticObjectPosition',
            (['in'], AudioObjectType, 'type'),
            (['out'], LPFLOAT, 'x'),
            (['out'], LPFLOAT, 'y'),
            (['out'], LPFLOAT, 'z'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetNativeStaticObjectTypeMask',
            (['out'], PAudioObjectType, 'mask')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetMaxDynamicObjectCount',
            (['out'], LPUINT32, 'value')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetSupportedAudioObjectFormatEnumerator',
            (['out'], POINTER(PIAudioFormatEnumerator), 'enumerator')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetMaxFrameCount',
            (['in'], PWAVEFORMATEX, 'objectFormat'),
            (['out'], LPUINT32, 'frameCountPerBuffer')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'IsAudioObjectFormatSupported',
            (['in'], PWAVEFORMATEX, 'objectFormat')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'IsSpatialAudioStreamAvailable',
            (['in'], REFIID, 'streamUuid'),
            (['in'], PPROPVARIANT, 'auxiliaryInfo')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'ActivateSpatialAudioStream',
            (['in'], PPROPVARIANT, 'activationParams'),
            (['in'], REFIID, 'streamUuid'),
            (['out'], POINTER(LPVOID), 'stream'),
        )
    )


PISpatialAudioClient = POINTER(ISpatialAudioClient)


class SpatialAudioClientActivationParams(ctypes.Structure):
    _fields_ = [
        ('tracingContextId', GUID),
        ('appId', GUID),
        ('majorVersion', INT),
        ('minorVersion1', INT),
        ('minorVersion2', INT),
        ('minorVersion3', INT),
    ]


PSpatialAudioClientActivationParams = POINTER(
    SpatialAudioClientActivationParams
)
