# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

"""
:var gImageList: The global wx.ImageList of the module.

:undocumented: gIconCache, DISABLED_PIL, FOLDER_PIL, PLUGIN_PIL, ACTION_PIL
"""

import wx
from base64 import b64decode
from cStringIO import StringIO
from os.path import abspath, join
from PIL import Image

# Local imports
import eg

IMAGES_PATH = eg.imagesDir

gImageList = wx.ImageList(16, 16)
DISABLED_PIL = Image.open(join(IMAGES_PATH, "disabled.png"))
FOLDER_PIL = Image.open(join(IMAGES_PATH, "folder.png")).convert("RGBA")
PLUGIN_PIL = Image.open(join(IMAGES_PATH, "plugin.png"))
ACTION_PIL = Image.open(join(IMAGES_PATH, "action.png")).convert("RGBA")

class IconBase(object):
    """
    An object representing an icon with some memoization functionality.

    The icon is initialized by a file path (see PathIcon) or by a base64encoded
    string (see StringIcon). The object will not load/convert any data before
    an attribute is accessed. If for example the "pil" attribute is requested
    the first time, the object will load the underlying resource through the
    method self._pil() and store the result into self.pil for further requests.
    """
    cache = {}

    def __new__(cls, key):
        """
        If an instance of this data is already in the cache, returns the
        cached instance. Otherwise creates a new instance and adds it to the
        cache.
        """
        if key in cls.cache:
            return cls.cache[key]
        self = super(IconBase, cls).__new__(cls)
        cls.cache[key] = self
        self.key = key
        return self

    def __getattr__(self, name):
        """
        Implements the memoization magic for the icon.

        Only called if an attribute 'name' does not exist. The code will look
        if a corresponding method '_name' exists, calls this method and stores
        the result as 'self.name' (so __getattr__ gets not called again for
        this attribute) and returns the result.
        """
        funcName = "_Get" + name[0].upper() + name[1:]
        if not hasattr(self, funcName):
            raise AttributeError
        result = getattr(self, funcName)()
        setattr(self, name, result)
        return result

    def __getnewargs__(self):
        return (self.key,)

    def GetBitmap(self):
        """
        Return a wx.Bitmap of the icon.
        """
        return PilToBitmap(self.pil)

    def GetWxIcon(self):
        """
        Return a wx.Icon of the icon.
        """
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(PilToBitmap(self.pil))
        return icon

    def _GetDisabledIndex(self):
        """
        Creates a version of the icon with a "disabled" mark overlayed and
        returns its index inside the global wx.ImageList.
        """
        image = self.pil.copy()
        image.paste(DISABLED_PIL, None, DISABLED_PIL)
        return gImageList.Add(PilToBitmap(image))

    def _GetFolderIndex(self):
        """
        Creates a folder icon with a small version of the icon overlayed and
        returns its index inside the global wx.ImageList.
        """
        small = self.pil.resize((12, 12), Image.BICUBIC)
        image = FOLDER_PIL.copy()
        image.paste(small, (4, 4), small)
        return gImageList.Add(PilToBitmap(image))

    def _GetIndex(self):
        """
        Return the index of this icon inside the global wx.ImageList.
        """
        return gImageList.Add(PilToBitmap(self.pil))

    def _GetPil(self):
        """
        Return a PIL image of the icon.

        Abstract method that must be implemented in a subclass.
        """
        raise NotImplementedError


class ActionSubIcon(IconBase):
    def _GetPil(self):
        """
        Return a PIL image of the icon.
        """
        small = self.key.pil.resize((12, 12), Image.BICUBIC)
        image = ACTION_PIL.copy()
        image.paste(small, (4, 4), small)
        return image

ActionSubIcon.cache = {}


class PathIcon(IconBase):
    def __new__(cls, path):
        """
        If an instance of this path is already in the cache, returns the
        cached instance. Otherwise creates a new instance and adds it to the
        cache.
        """
        return super(PathIcon, cls).__new__(cls, abspath(path))

    def _GetPil(self):
        """
        Return a PIL image of the icon.
        """
        return Image.open(self.key).convert("RGBA")


class PilIcon(IconBase):
    def _GetPil(self):
        """
        Return a PIL image of the icon.
        """
        return self.key


class PluginSubIcon(IconBase):
    def _GetPil(self):
        """
        Return a PIL image of the icon.
        """
        small = self.key.pil.resize((12, 12), Image.BICUBIC)
        image = PLUGIN_PIL.copy()
        image.paste(small, (4, 4), small)
        return image

PluginSubIcon.cache = {}


class StringIcon(IconBase):
    def _GetPil(self):
        """
        Return a PIL image of the icon.
        """
        stream = StringIO(b64decode(self.key))
        pil = Image.open(stream).convert("RGBA")
        stream.close()
        return pil


def ClearImageList():
    """
    Clear the global wxImageList.
    """
    gImageList.RemoveAll()
    # clear out all instance variables for all icons, except the key variable
    for clsType in (IconBase, ActionSubIcon, PluginSubIcon):
        for icon in clsType.cache.itervalues():
            icon.__dict__ = {"key": icon.key}

def CreateBitmapOnTopOfIcon(foregroundIcon, backgroundIcon, size=(12, 12)):
    small = foregroundIcon.pil.resize(size, Image.BICUBIC)
    pil = backgroundIcon.pil.copy()
    pil.paste(small, (16 - size[0], 16 - size[1]), small)
    return wx.BitmapFromBufferRGBA(pil.size[0], pil.size[1], str(pil.tobytes()))

def GetBitmap(filePath):
    """
    Returns a wx.Bitmap loaded from 'filePath'.

    Uses PIL functions, because this way we have better alpha channel
    handling.
    """
    return PilToBitmap(Image.open(filePath).convert("RGBA"))

def GetInternalBitmap(name):
    """
    Same as GetBitmap() but looks for the file in the programs images
    folder. Also appends the .png extension to the name.
    """
    return GetBitmap(join(IMAGES_PATH, name + ".png"))

def GetInternalImage(name):
    return wx.Image(join(eg.imagesDir, name + ".png"), wx.BITMAP_TYPE_PNG)

def PilToBitmap(pil):
    """
    Convert a PIL image to a wx.Bitmap (with alpha channel support).
    """
    return wx.BitmapFromBufferRGBA(pil.size[0], pil.size[1], str(pil.tobytes()))

# setup some commonly used icons
INFO_ICON = PathIcon(join(IMAGES_PATH, "info.png"))
ERROR_ICON = PathIcon(join(IMAGES_PATH, "error.png"))
NOTICE_ICON = PathIcon(join(IMAGES_PATH, "notice.png"))
FOLDER_ICON = PathIcon(join(IMAGES_PATH, "folder.png"))
DISABLED_ICON = PathIcon(join(IMAGES_PATH, "disabled.png"))
PLUGIN_ICON = PathIcon(join(IMAGES_PATH, "plugin.png"))
EVENT_ICON = PathIcon(join(IMAGES_PATH, "event.png"))
ACTION_ICON = PathIcon(join(IMAGES_PATH, "action.png"))
MACRO_ICON = PathIcon(join(IMAGES_PATH, "macro.png"))
ADD_ICON = PathIcon(join(IMAGES_PATH, 'add.png'))
ROOT_ICON = PathIcon(join(IMAGES_PATH, 'root.png'))
AUTOSTART_ICON = PathIcon(join(IMAGES_PATH, 'Execute.png'))
