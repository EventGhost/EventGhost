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
from enum import APO_BUFFER_FLAGS
from ctypes.wintypes import (UINT)

POINTER = ctypes.POINTER
UINT32 = ctypes.c_uint32
UINT_PTR = POINTER(UINT)


class APO_CONNECTION_PROPERTY(ctypes.Structure):
    _fields_ = [
        ('pBuffer', UINT_PTR),
        ('u32ValidFrameCount', UINT32),
        ('u32BufferFlags', APO_BUFFER_FLAGS),
        ('u32Signature', UINT32)
    ]


PAPO_CONNECTION_PROPERTY = POINTER(APO_CONNECTION_PROPERTY)
