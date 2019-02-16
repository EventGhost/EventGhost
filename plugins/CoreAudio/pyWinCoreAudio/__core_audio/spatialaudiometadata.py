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
    IID_ISpatialAudioMetadataItems,
    IID_ISpatialAudioMetadataWriter,
    IID_ISpatialAudioMetadataReader,
    IID_ISpatialAudioMetadataCopier,
    IID_ISpatialAudioMetadataItemsBuffer,
    IID_ISpatialAudioMetadataClient,
    IID_ISpatialAudioObjectForMetadataCommands,
    IID_ISpatialAudioObjectForMetadataItems,
    IID_ISpatialAudioObjectRenderStreamForMetadata
)
from audioclient import PWAVEFORMATEX
from enum import (
    AUDIO_STREAM_CATEGORY,
    AudioObjectType,
    SpatialAudioMetadataCopyMode,
    SpatialAudioMetadataWriterOverflowMode
)
from mmdeviceapi import PPROPVARIANT
from spatialaudioclient import (
    ISpatialAudioObjectBase,
    PISpatialAudioObjectRenderStreamNotify,
    ISpatialAudioObjectRenderStreamBase
)
from ctypes.wintypes import (
    FLOAT,
    UINT,
    HANDLE,
    BYTE,
)

GUID = comtypes.GUID
COMMETHOD = comtypes.COMMETHOD
HRESULT = ctypes.HRESULT
HNSTIME = ctypes.c_longlong
UINT8 = ctypes.c_uint8
UINT16 = ctypes.c_uint16
UINT32 = ctypes.c_uint32
UINT64 = ctypes.c_uint64
LONGLONG = ctypes.c_longlong
FLOAT32 = FLOAT
POINTER = ctypes.POINTER
LPUINT16 = POINTER(UINT16)
LPUINT32 = POINTER(UINT32)
UINT_PTR = POINTER(UINT)
LPVOID = POINTER(ctypes.c_void_p)
LPBYTE = POINTER(BYTE)
LPUINT8 = POINTER(UINT8)


class SpatialAudioMetadataItemsInfo(ctypes.Structure):
    _fields_ = [
        ('FrameCount', UINT16),
        ('ItemCount', UINT16),
        ('MaxItemCount', UINT16),
        ('MaxValueBufferLength', UINT32)
    ]


PSpatialAudioMetadataItemsInfo = POINTER(SpatialAudioMetadataItemsInfo)


class SpatialAudioObjectRenderStreamForMetadataActivationParams(
    ctypes.Structure
):
    _fields_ = [
        ('ObjectFormat', PWAVEFORMATEX),
        ('StaticObjectTypeMask', AudioObjectType),
        ('MinDynamicObjectCount', UINT32),
        ('MaxDynamicObjectCount', UINT32),
        ('Category', AUDIO_STREAM_CATEGORY),
        ('EventHandle', HANDLE),
        ('MetadataFormatId', GUID),
        ('MaxMetadataItemCount', UINT16),
        ('MetadataActivationParams', PPROPVARIANT),
        ('NotifyObject', PISpatialAudioObjectRenderStreamNotify),
    ]


PSpatialAudioObjectRenderStreamForMetadataActivationParams = POINTER(
    SpatialAudioObjectRenderStreamForMetadataActivationParams
)


class ISpatialAudioMetadataItems(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_ISpatialAudioMetadataItems
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetFrameCount',
            (['out'], LPUINT16, 'pwstrDeviceId'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetItemCount',
            (['out'], LPUINT16, 'pwstrDeviceId')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetMaxItemCount',
            (['out'], LPUINT16, 'pwstrDeviceId')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetMaxValueBufferLength',
            (['out'], LPUINT32, 'flow'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetInfo',
            (['out'], PSpatialAudioMetadataItemsInfo, 'pwstrDeviceId'),
        )
    )


PISpatialAudioMetadataItems = POINTER(ISpatialAudioMetadataItems)


class ISpatialAudioMetadataWriter(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_ISpatialAudioMetadataWriter
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'Open',
            (['in'], PISpatialAudioMetadataItems, 'metadataItems'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'WriteNextItem',
            (['in'], UINT16, 'frameOffset')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'WriteNextItemCommand',
            (['in'], BYTE, 'commandID'),
            (['in'], LPVOID, 'valueBuffer'),
            (['in'], UINT32, 'valueBufferLength')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Close'
        ),
    )


PISpatialAudioMetadataWriter = POINTER(ISpatialAudioMetadataWriter)


class ISpatialAudioMetadataReader(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_ISpatialAudioMetadataReader
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'Open',
            (['in'], PISpatialAudioMetadataItems, 'metadataItems'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'ReadNextItem',
            (['out'], LPUINT8, 'commandCount'),
            (['out'], LPUINT16, 'frameOffset')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'ReadNextItemCommand',
            (['out'], LPBYTE, 'commandID'),
            (['out'], LPVOID, 'valueBuffer'),
            (['in'], UINT32, 'maxValueBufferLength'),
            (['out'], LPUINT32, 'valueBufferLength')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Close'
        ),
    )


PISpatialAudioMetadataReader = POINTER(ISpatialAudioMetadataReader)


class ISpatialAudioMetadataCopier(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_ISpatialAudioMetadataCopier
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'Open',
            (['in'], PISpatialAudioMetadataItems, 'metadataItems'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'CopyMetadataForFrames',
            (['in'], UINT16, 'copyFrameCount'),
            (['in'], SpatialAudioMetadataCopyMode, 'copyMode'),
            (['in'], PISpatialAudioMetadataItems, 'dstMetadataItems'),
            (['out'], LPUINT16, 'itemsCopied')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Close'
        )
    )


PISpatialAudioMetadataCopier = POINTER(ISpatialAudioMetadataCopier)


class ISpatialAudioMetadataItemsBuffer(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_ISpatialAudioMetadataItemsBuffer
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'AttachToBuffer',
            (['in'], LPBYTE, 'buffer'),
            (['in'], UINT32, 'bufferLength')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'AttachToPopulatedBuffer',
            (['in'], LPBYTE, 'buffer'),
            (['in'], UINT32, 'bufferLength')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'DetachBuffer'
        )
    )


PISpatialAudioMetadataItemsBuffer = POINTER(ISpatialAudioMetadataItemsBuffer)


class ISpatialAudioMetadataClient(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_ISpatialAudioMetadataClient
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'ActivateSpatialAudioMetadataItems',
            (['in'], UINT16, 'maxItemCount'),
            (['in'], UINT16, 'frameCount'),
            (
                ['out'],
                POINTER(PISpatialAudioMetadataItemsBuffer),
                'metadataItemsBuffer'
            ),
            (['out'], POINTER(PISpatialAudioMetadataItems), 'metadataItems')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetSpatialAudioMetadataItemsBufferLength',
            (['in'], UINT16, 'maxItemCount'),
            (['out'], LPUINT32, 'bufferLength')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'ActivateSpatialAudioMetadataWriter',
            (['in'], SpatialAudioMetadataWriterOverflowMode, 'overflowMode'),
            (['out'], POINTER(PISpatialAudioMetadataWriter), 'metadataWriter')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'ActivateSpatialAudioMetadataCopier',
            (['out'], POINTER(PISpatialAudioMetadataCopier), 'metadataCopier')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'ActivateSpatialAudioMetadataReader',
            (['out'], POINTER(PISpatialAudioMetadataReader), 'metadataReader')
        ),
    )


PISpatialAudioMetadataClient = POINTER(ISpatialAudioMetadataClient)


class ISpatialAudioObjectForMetadataCommands(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_ISpatialAudioObjectForMetadataCommands
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'WriteNextMetadataCommand',
            (['in'], BYTE, 'commandID'),
            (['in'], LPVOID, 'valueBuffer'),
            (['in'], UINT32, 'valueBufferLength'),
        ),
    )


PISpatialAudioObjectForMetadataCommands = POINTER(
    ISpatialAudioObjectForMetadataCommands
)


class ISpatialAudioObjectForMetadataItems(ISpatialAudioObjectBase):
    _case_insensitive_ = True
    _iid_ = IID_ISpatialAudioObjectForMetadataItems
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetSpatialAudioMetadataItems',
            (['out'], POINTER(PISpatialAudioMetadataItems), 'metadataItems'),
        ),
    )


PISpatialAudioObjectForMetadataItems = POINTER(
    ISpatialAudioObjectForMetadataItems
)


class ISpatialAudioObjectRenderStreamForMetadata(
    ISpatialAudioObjectRenderStreamBase
):
    _case_insensitive_ = True
    _iid_ = IID_ISpatialAudioObjectRenderStreamForMetadata
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'ActivateSpatialAudioObjectForMetadataCommands',
            (['in'], AudioObjectType, 'type'),
            (
                ['in'],
                POINTER(PISpatialAudioObjectForMetadataCommands),
                'audioObject'
            ),
            (['in'], UINT32, 'valueBufferLength'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'ActivateSpatialAudioObjectForMetadataItems',
            (['in'], AudioObjectType, 'type'),
            (
                ['in'],
                POINTER(PISpatialAudioObjectForMetadataItems),
                'audioObject'
            ),
            (['in'], UINT32, 'valueBufferLength'),
        ),
    )


PISpatialAudioObjectRenderStreamForMetadata = POINTER(
    ISpatialAudioObjectRenderStreamForMetadata
)
