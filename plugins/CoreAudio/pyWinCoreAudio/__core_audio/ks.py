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
from comtypes import GUID, POINTER
from ctypes.wintypes import ULONG, LONG

LONGLONG = ctypes.c_longlong


class KSAUDIO_CHANNEL_CONFIG(ctypes.Structure):

    _fields_ = [
        ('ActiveSpeakerPositions', LONG)
    ]


PKSAUDIO_CHANNEL_CONFIG = POINTER(KSAUDIO_CHANNEL_CONFIG)


class KSIDENTIFIER_STRUCT(ctypes.Union):
    _fields_ = [
        ('Set', GUID),
        ('Id', ULONG),
        ('Flags', ULONG)
    ]


class KSIDENTIFIER_UNION(ctypes.Union):
    _anonymous_ = 'KSIDENTIFIER_STRUCT'
    _fields_ = [
        ('KSIDENTIFIER_STRUCT', KSIDENTIFIER_STRUCT)
    ]


class KSIDENTIFIER(ctypes.Structure):
    _anonymous_ = 'KSIDENTIFIER_UNION'
    _fields_ = [
        ('KSIDENTIFIER_UNION', KSIDENTIFIER_UNION),
        ('Alignment', LONGLONG)
    ]


PKSIDENTIFIER = POINTER(KSIDENTIFIER)


class KSMETHOD(KSIDENTIFIER):
    pass


PKSMETHOD = POINTER(KSMETHOD)


class KSEVENT(KSIDENTIFIER):
    pass


PKSEVENT = POINTER(KSEVENT)


class KSPROPERTY(KSIDENTIFIER):
    pass


PKSPROPERTY = POINTER(KSPROPERTY)



class KSNODEPROPERTY(ctypes.Structure):

    _fields_ = [
        ('Property', KSPROPERTY),
        ('NodeId', ULONG),
        ('Reserved', ULONG)
    ]


PKSNODEPROPERTY = POINTER(KSNODEPROPERTY)


class KSNODEPROPERTY_AUDIO_CHANNEL(ctypes.Structure):

    _fields_ = [
        ('NodeProperty', KSNODEPROPERTY),
        ('Channel', LONG),
        ('Reserved', ULONG)
    ]


PKSNODEPROPERTY_AUDIO_CHANNEL = POINTER(KSNODEPROPERTY_AUDIO_CHANNEL)
