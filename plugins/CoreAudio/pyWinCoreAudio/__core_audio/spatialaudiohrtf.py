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
from spatialaudioclient import PISpatialAudioObjectRenderStreamNotify
from enum import (
    AUDIO_STREAM_CATEGORY,
    AudioObjectType
)
from iid import (
    IID_ISpatialAudioObjectForHrtf,
    IID_ISpatialAudioObjectRenderStreamForHrtf
)
from _spatialaudioclient import (
    ISpatialAudioObjectRenderStreamBase,
    ISpatialAudioObjectBase
)
from enum import (
    SpatialAudioHrtfEnvironmentType,
    SpatialAudioHrtfDirectivityType,
    SpatialAudioHrtfDistanceDecayType,
    PSpatialAudioHrtfEnvironmentType
)
from ctypes.wintypes import (
    FLOAT,
    HANDLE,
)

COMMETHOD = comtypes.COMMETHOD
UINT32 = ctypes.c_uint32
HRESULT = ctypes.HRESULT
POINTER = ctypes.POINTER


class SpatialAudioHrtfDirectivity(ctypes.Structure):
    _fields_ = [
        ('Type', SpatialAudioHrtfDirectivityType),
        ('Scaling', FLOAT)
    ]


PSpatialAudioHrtfDirectivity = POINTER(SpatialAudioHrtfDirectivity)


class SpatialAudioHrtfDirectivityCardioid(ctypes.Structure):
    _fields_ = [
        ('directivity', SpatialAudioHrtfDirectivity),
        ('Order', FLOAT)
    ]


PSpatialAudioHrtfDirectivityCardioid = POINTER(
    SpatialAudioHrtfDirectivityCardioid
)


class SpatialAudioHrtfDirectivityCone(ctypes.Structure):
    _fields_ = [
        ('directivity', SpatialAudioHrtfDirectivity),
        ('InnerAngle', FLOAT),
        ('OuterAngle', FLOAT)
    ]


PSpatialAudioHrtfDirectivityCone = POINTER(SpatialAudioHrtfDirectivityCone)


class SpatialAudioHrtfDirectivityUnion(ctypes.Union):
    _fields_ = [
        ('Cone', SpatialAudioHrtfDirectivityCone),
        ('Cardiod', SpatialAudioHrtfDirectivityCardioid),
        ('Omni', SpatialAudioHrtfDirectivity)
    ]


PSpatialAudioHrtfDirectivityUnion = POINTER(SpatialAudioHrtfDirectivityUnion)


class SpatialAudioHrtfDistanceDecay(ctypes.Structure):
    _fields_ = [
        ('Type', SpatialAudioHrtfDistanceDecayType),
        ('MaxGain', FLOAT),
        ('MinGain', FLOAT),
        ('UnityGainDistance', FLOAT),
        ('CutoffDistance', FLOAT)
    ]


PSpatialAudioHrtfDistanceDecay = POINTER(SpatialAudioHrtfDistanceDecay)


SpatialAudioHrtfOrientation = (FLOAT() * 9)

PSpatialAudioHrtfOrientation = POINTER(SpatialAudioHrtfOrientation)


class SpatialAudioHrtfActivationParams(ctypes.Structure):
    _fields_ = [
        ('ObjectFormat', PWAVEFORMATEX),
        ('StaticObjectTypeMask', AudioObjectType),
        ('MinDynamicObjectCount', UINT32),
        ('MaxDynamicObjectCount', UINT32),
        ('Category', AUDIO_STREAM_CATEGORY),
        ('EventHandle', HANDLE),
        ('NotifyObject', PISpatialAudioObjectRenderStreamNotify),
        ('DistanceDecay', PSpatialAudioHrtfDistanceDecay),
        ('Directivity', PSpatialAudioHrtfDirectivityUnion),
        ('Environment', PSpatialAudioHrtfEnvironmentType),
        ('Orientation', PSpatialAudioHrtfOrientation)
    ]


PSpatialAudioHrtfActivationParams = POINTER(SpatialAudioHrtfActivationParams)


class ISpatialAudioObjectForHrtf(
    ISpatialAudioObjectBase
):
    _case_insensitive_ = True
    _iid_ = IID_ISpatialAudioObjectForHrtf
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'SetPosition',
            (['in'], FLOAT, 'x'),
            (['in'], FLOAT, 'y'),
            (['in'], FLOAT, 'z')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetGain',
            (['in'], FLOAT, 'gain')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetOrientation',
            (['in'], PSpatialAudioHrtfOrientation, 'orientation')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetEnvironment',
            (['in'], SpatialAudioHrtfEnvironmentType, 'environment')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetDistanceDecay',
            (['in'], PSpatialAudioHrtfDistanceDecay, 'distanceDecay')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetDirectivity',
            (['in'], PSpatialAudioHrtfDirectivityUnion, 'directivity')
        ),
    )


PISpatialAudioObjectForHrtf = POINTER(
    ISpatialAudioObjectForHrtf
)


class ISpatialAudioObjectRenderStreamForHrtf(
    ISpatialAudioObjectRenderStreamBase
):
    _case_insensitive_ = True
    _iid_ = IID_ISpatialAudioObjectRenderStreamForHrtf
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'ActivateSpatialAudioObjectForHrtf',
            (['in'], AudioObjectType, 'type'),
            (['out'], POINTER(PISpatialAudioObjectForHrtf), 'audioObject')
        ),
    )


PISpatialAudioObjectRenderStreamForHrtf = POINTER(
    ISpatialAudioObjectRenderStreamForHrtf
)
