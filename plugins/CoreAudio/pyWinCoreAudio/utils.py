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

import threading
import ctypes
import comtypes
import ctypes.util
import os
from ctypes import wintypes
from io import BytesIO


RT_CURSOR = 1
RT_BITMAP = 2
RT_ICON = 3
RT_MENU = 4
RT_DIALOG = 5
RT_STRING = 6
RT_FONTDIR = 7
RT_FONT = 8
RT_ACCELERATOR = 9
RT_RCDATA = 10
RT_MESSAGETABLE = 11
DIFFERENCE = 11
RT_GROUP_CURSOR = (RT_CURSOR + DIFFERENCE)
RT_GROUP_ICON = (RT_ICON + DIFFERENCE)
RT_VERSION = 16
RT_DLGINCLUDE = 17
RT_PLUGPLAY = 19
RT_VXD = 20
RT_ANICURSOR = 21
RT_ANIICON = 22
RT_HTML = 23


def run_in_thread(func, *args, **kwargs):
    t = threading.Thread(target=func, args=args, kwargs=kwargs)
    t.daemon = True
    t.start()
    return t


def convert_triplet_to_rgb(triplet):
    if not triplet:
        return 0, 0, 0

    r, g, b = bytearray.fromhex(hex(triplet)[2:].replace('L', '').zfill(6))
    return r, g, b


icons = {}


def get_icon(icon):
    global icons

    if icon in icons:
        return icons[icon]

    libc = ctypes.CDLL(ctypes.util.find_library('c'))
    libc.memcpy.argtypes = [wintypes.LPVOID, wintypes.LPVOID, ctypes.c_size_t]
    libc.memcpy.restype = wintypes.LPCSTR

    kernel32 = ctypes.windll.kernel32

    try:
        icon_path, icon_name = icon.replace('@', '').split(',-')
        icon_name = int(icon_name)
    except ValueError:
        icon_path = icon.replace('@', '')
        icon_name = 1

    try:

        hlib = kernel32.LoadLibraryExW(
            os.path.expandvars(icon_path),
            None,
            0x00000020
        )

        # This part almost identical to C++
        hResInfo = ctypes.windll.kernel32.FindResourceW(
            hlib,
            icon_name,
            RT_ICON
        )
        size = ctypes.windll.kernel32.SizeofResource(
            hlib,
            hResInfo
        )
        rec = kernel32.LoadResource(hlib, hResInfo)
        mem_pointer = kernel32.LockResource(rec)

        # And this is some differ (copy data to Python buffer)
        binary_data = (ctypes.c_ubyte * size)()
        libc.memcpy(binary_data, mem_pointer, size)

        f = BytesIO()
        f.write(bytearray(binary_data))
        f.seek(0)
        icons[icon] = f
        return f

    except comtypes.COMError:
        import traceback
        traceback.print_exc()
