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
from mmdeviceapi import PIMMDeviceCollection
from propertystore import PIPropertyStore
from audiomediatype import PIAudioMediaType
from audioapotypes import PAPO_CONNECTION_PROPERTY
from enum import (
    APO_CONNECTION_BUFFER_TYPE,
    APO_FLAG
)
from ctypes.wintypes import (
    UINT,
    LPARAM,
    BOOL,
    HANDLE,
    LPWSTR,
    WCHAR,
    BYTE,
    LPCVOID
)
from _iid import (
    IID_IAudioProcessingObjectRT,
    IID_IAudioProcessingObjectVBR,
    IID_IAudioProcessingObjectConfiguration,
    IID_IAudioProcessingObject,
    IID_IAudioSystemEffects,
    IID_IAudioSystemEffects2,
    IID_IAudioSystemEffectsCustomFormats,
    IID
)


POINTER = ctypes.POINTER
COMMETHOD = comtypes.COMMETHOD
CLSID = comtypes.GUID
GUID = comtypes.GUID
HNSTIME = ctypes.c_longlong
VOID = ctypes.c_void_p
UINT32 = ctypes.c_uint32
HRESULT = ctypes.HRESULT
LPUINT = POINTER(UINT)
LPUINT32 = POINTER(UINT32)
UINT_PTR = POINTER(UINT)
LPBYTE = POINTER(BYTE)
LPHNSTIME = POINTER(HNSTIME)
LPGUID = POINTER(comtypes.GUID)


class APO_CONNECTION_DESCRIPTOR(ctypes.Structure):
    _fields_ = [
        ('Type', APO_CONNECTION_BUFFER_TYPE),
        ('pBuffer', UINT_PTR),
        ('u32MaxFrameCount', UINT32),
        ('pFormat', PIAudioMediaType),
        ('u32Signature', UINT32)
    ]


PAPO_CONNECTION_DESCRIPTOR = POINTER(APO_CONNECTION_DESCRIPTOR)


class APO_REG_PROPERTIES(ctypes.Structure):
    _fields_ = [
        ('clsid', CLSID),
        ('Flags', APO_FLAG),
        ('szFriendlyName[256]', WCHAR),
        ('szCopyrightInfo[256]', WCHAR),
        ('u32MajorVersion', UINT32),
        ('u32MinorVersion', UINT32),
        ('u32MinInputConnections', UINT32),
        ('u32MaxInputConnections', UINT32),
        ('u32MinOutputConnections', UINT32),
        ('u32MaxOutputConnections', UINT32),
        ('u32MaxInstances', UINT32),
        ('u32NumAPOInterfaces', UINT32),
        ('iidAPOInterfaceList[]', IID)
    ]


PAPO_REG_PROPERTIES = POINTER(APO_REG_PROPERTIES)


class APOInitBaseStruct(ctypes.Structure):
    _fields_ = [
        ('cbSize', UINT32),
        ('clsid', CLSID)
    ]


PAPOInitBaseStruct = POINTER(APOInitBaseStruct)


class IAudioProcessingObjectRT(comtypes.IUnknown):
    _iid_ = IID_IAudioProcessingObjectRT
    _methods_ = (
        COMMETHOD(
            [],
            VOID,
            'APOProcess',
            (['in'], UINT32, 'u32NumInputConnections'),
            (['in'], POINTER(PAPO_CONNECTION_PROPERTY), 'ppInputConnections'),
            (['in'], UINT32, 'u32NumOutputConnections'),
            (
                ['in', 'out'],
                POINTER(PAPO_CONNECTION_PROPERTY),
                'ppOutputConnections'
            ),
        ),
        COMMETHOD(
            [],
            UINT32,
            'CalcInputFrames',
            (['in'], UINT32, 'u32OutputFrameCount')
        ),
        COMMETHOD(
            [],
            UINT32,
            'CalcOutputFrames',
            (['in'], UINT32, 'u32InputFrameCount')
        ),
    )


PIAudioProcessingObjectRT = POINTER(IAudioProcessingObjectRT)


class IAudioProcessingObjectVBR(comtypes.IUnknown):
    _iid_ = IID_IAudioProcessingObjectVBR
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'CalcMaxInputFrames',
            (['in'], UINT32, 'u32MaxOutputFrameCount'),
            (['out'], LPUINT32, 'pu32InputFrameCount'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'CalcMaxOutputFrames',
            (['in'], UINT32, 'u32MaxInputFrameCount'),
            (['out'], LPUINT32, 'pu32OutputFrameCount'),
        ),
    )


PIAudioProcessingObjectVBR = POINTER(IAudioProcessingObjectVBR)


class IAudioProcessingObjectConfiguration(comtypes.IUnknown):
    _iid_ = IID_IAudioProcessingObjectConfiguration
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'LockForProcess',
            (['in'], UINT32, 'u32NumInputConnections'),
            (
                ['in'],
                POINTER(PAPO_CONNECTION_DESCRIPTOR),
                'ppInputConnections'
            ),
            (['in'], UINT32, 'u32NumOutputConnections'),
            (
                ['in'],
                POINTER(PAPO_CONNECTION_DESCRIPTOR),
                'ppOutputConnections'
            ),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'UnlockForProcess'
        ),
    )


PIAudioProcessingObjectConfiguration = POINTER(
    IAudioProcessingObjectConfiguration
)


class IAudioProcessingObject(comtypes.IUnknown):
    _iid_ = IID_IAudioProcessingObject
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'Reset'
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetLatency',
            (['out'], LPHNSTIME, 'pTime')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetRegistrationProperties',
            (['out'], POINTER(PAPO_REG_PROPERTIES), 'ppRegProps')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Initialize',
            (['in'], UINT32, 'cbDataSize'),
            (['in'], LPBYTE, 'pbyData')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'IsInputFormatSupported',
            (['in', 'unique'], PIAudioMediaType, 'pOppositeFormat'),
            (['in'], PIAudioMediaType, 'pRequestedInputFormat'),
            (['out'], POINTER(PIAudioMediaType), 'ppSupportedInputFormat')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'IsOutputFormatSupported',
            (['in', 'unique'], PIAudioMediaType, 'pOppositeFormat'),
            (['in'], PIAudioMediaType, 'pRequestedOutputFormat'),
            (['out'], POINTER(PIAudioMediaType), 'ppSupportedOutputFormat')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetInputChannelCount',
            (['out'], LPUINT32, 'pu32ChannelCount')
        ),
    )


PIAudioProcessingObject = POINTER(IAudioProcessingObject)


class IAudioSystemEffects(comtypes.IUnknown):
    _iid_ = IID_IAudioSystemEffects


PIAudioSystemEffects = POINTER(IAudioSystemEffects)


class IAudioSystemEffects2(IAudioSystemEffects):
    _iid_ = IID_IAudioSystemEffects2
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetEffectsList',
            (['out'], POINTER(LPGUID), 'ppEffectsIds'),
            (['out'], LPUINT, 'pcEffects'),
            (['in'], HANDLE, 'Event')
        ),
    )


PIAudioSystemEffects2 = POINTER(IAudioSystemEffects2)


class IAudioSystemEffectsCustomFormats(comtypes.IUnknown):
    _iid_ = IID_IAudioSystemEffectsCustomFormats
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetFormatCount',
            (['out'], LPUINT, 'pcFormats')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetFormatCount',
            (['in'], UINT, 'nFormat'),
            (['out'], POINTER(PIAudioMediaType), 'ppFormat')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetFormatRepresentation',
            (['in'], UINT, 'nFormat'),
            (['out'], POINTER(LPWSTR), 'ppwstrFormatRep')
        )
    )


PIAudioSystemEffectsCustomFormats = POINTER(IAudioSystemEffectsCustomFormats)


class APOInitSystemEffects(ctypes.Structure):
    _fields_ = [
        ('APOInit', APOInitBaseStruct),
        ('pAPOEndpointProperties', PIPropertyStore),
        ('pAPOSystemEffectsProperties', PIPropertyStore),
        ('pReserved', LPCVOID),
        ('pDeviceCollection', PIMMDeviceCollection)
    ]


PAPOInitSystemEffects = POINTER(APOInitSystemEffects)


class APOInitSystemEffects2(ctypes.Structure):
    _fields_ = [
        ('APOInit', APOInitBaseStruct),
        ('pAPOEndpointProperties', PIPropertyStore),
        ('pAPOSystemEffectsProperties', PIPropertyStore),
        ('pReserved', LPCVOID),
        ('pDeviceCollection', PIMMDeviceCollection),
        ('nSoftwareIoDeviceInCollection', UINT),
        ('nSoftwareIoConnectorIndex', UINT),
        ('AudioProcessingMode', GUID),
        ('InitializeForDiscoveryOnly', BOOL)
    ]


PAPOInitSystemEffects2 = POINTER(APOInitSystemEffects2)


class AudioFXExtensionParams(ctypes.Structure):
    _fields_ = [
        ('AddPageParam', LPARAM),
        ('pwstrEndpointID', LPWSTR),
        ('pFxProperties', PIPropertyStore),
    ]


PAudioFXExtensionParams = POINTER(AudioFXExtensionParams)
