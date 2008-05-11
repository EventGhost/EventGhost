# This file is part of EventGhost.
# Copyright (C) 2007 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

"""
:var gImageList: The global wx.ImageList of the module.

:undocumented: gIconCache, DISABLED_PIL, FOLDER_PIL, PLUGIN_PIL, ACTION_PIL
"""

from os.path import abspath
from base64 import b64decode
from cStringIO import StringIO
import Image


gImageList = wx.ImageList(16, 16)
DISABLED_PIL = Image.open("images/disabled.png")
FOLDER_PIL = Image.open("images/folder.png").convert("RGBA")
PLUGIN_PIL = Image.open("images/plugin.png")
ACTION_PIL = Image.open("images/action.png").convert("RGBA")


def PilToBitmap(pil):
    """ Convert a PIL image to a wx.Bitmap (with alpha channel support). """
    return wx.BitmapFromBufferRGBA(pil.size[0], pil.size[1], pil.tostring())


def GetIcon(filePath):
    """ Returns a wx.Bitmap loaded from 'filePath'.
    
    Uses PIL functions, because this way we have better alpha channel 
    handling.
    """
    return PilToBitmap(Image.open(filePath).convert("RGBA"))
    

def CreateBitmapOnTopOfIcon(foregroundIcon, backgroundIcon, size=(12, 12)):
    small = foregroundIcon.pil.resize(size, Image.BICUBIC)
    pil = backgroundIcon.pil.copy()
    pil.paste(small, (16 - size[0], 16 - size[1]), small)
    return wx.BitmapFromBufferRGBA(pil.size[0], pil.size[1], pil.tostring())
    
    
class IconBase(object):
    """ An object representing an icon with some memoization functionality.
    
    The icon is initialized by a file path (see PathIcon) or by a base64encoded
    string (see StringIcon). The object will not load/convert any data before
    an attribute is accessed. If for example the "pil" attribute is requested
    the first time, the object will load the underlying resource through the 
    method self._pil() and store the result into self.pil for further requests.
    """
    
    cache = {}
    
    def __new__(cls, key):
        """ If an instance of this data is already in the cache, returns the 
        cached instance. Otherwise creates a new instance and adds it to the 
        cache.
        """
        if cls.cache.has_key(key):
            return cls.cache[key]
        self = super(IconBase, cls).__new__(cls)
        cls.cache[key] = self
        self.key = key
        return self
    
    
    def _pil(self):
        """ Return a PIL image of the icon.
        
        Abstract method that must be implemented in a subclass.
        """
        raise NotImplementedError
    
    
    def _index(self):
        """ Return the index of this icon inside the global wx.ImageList. """
        return gImageList.Add(PilToBitmap(self.pil))
    
    
    def _disabledIndex(self):
        """ Creates a version of the icon with a "disabled" mark overlayed and
        returns its index inside the global wx.ImageList.
        """
        image = self.pil.copy()
        image.paste(DISABLED_PIL, None, DISABLED_PIL)
        return gImageList.Add(PilToBitmap(image))
    
    
    def _folderIndex(self):
        """ Creates a folder icon with a small version of the icon overlayed and
        returns its index inside the global wx.ImageList. 
        """
        small = self.pil.resize((12,12), Image.BICUBIC)
        image = FOLDER_PIL.copy()
        image.paste(small, (4, 4), small)
        return gImageList.Add(PilToBitmap(image))
    
    
    def GetBitmap(self):
        """ Return a wx.Bitmap of the icon. """
        return PilToBitmap(self.pil)


    def GetWxIcon(self):
        """ Return a wx.Icon of the icon. """
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(PilToBitmap(self.pil))
        return icon


    def __getattr__(self, name):
        """ Implements the memoization magic for the icon.
        
        Only called if an attribute 'name' does not exist. The code will look 
        if a corresponding method '_name' exists, calls this method and stores
        the result as 'self.name' (so __getattr__ gets not called again for
        this attribute) and returns the result.
        """
        if not hasattr(self, "_" + name):
            raise AttributeError
        result = getattr(self, "_" + name)()
        setattr(self, name, result)
        return result
        


class ActionSubIcon(IconBase): 
    
    def _pil(self):
        """ Return a PIL image of the icon. """
        small = self.key.pil.resize((12,12), Image.BICUBIC)
        image = ACTION_PIL.copy()
        image.paste(small, (4, 4), small)
        return image

ActionSubIcon.cache = {}               
        
        
class PluginSubIcon(IconBase): 
    
    def _pil(self):
        """ Return a PIL image of the icon. """
        small = self.key.pil.resize((12,12), Image.BICUBIC)
        image = PLUGIN_PIL.copy()
        image.paste(small, (4, 4), small)
        return image
               
PluginSubIcon.cache = {}               
        
        
class PathIcon(IconBase):
    
    def __new__(cls, path):
        """ If an instance of this path is already in the cache, returns the 
        cached instance. Otherwise creates a new instance and adds it to the 
        cache.
        """
        return super(PathIcon, cls).__new__(cls, abspath(path))
    
    
    def _pil(self):
        """ Return a PIL image of the icon. """
        return Image.open(self.key).convert("RGBA")
        
        
        
class StringIcon(IconBase):
    
    def _pil(self):
        """ Return a PIL image of the icon. """
        fd = StringIO(b64decode(self.key))
        pil = Image.open(fd).convert("RGBA")
        fd.close()
        return pil



class PilIcon(IconBase):
    
    def _pil(self):
        """ Return a PIL image of the icon. """
        return self.key
    
    
    
def ClearImageList():
    """ Delete the global wxImageList and replace it with a new empty one. """
    global gImageList
    gImageList.RemoveAll()
    gImageList = wx.ImageList(16, 16)
    # clear out all instance variables for all icons, except the key variable
    for clsType in (IconBase, ActionSubIcon, PluginSubIcon):
        for icon in clsType.cache.itervalues():
            icon.__dict__ = {"key": icon.key}
        
        
# setup some commonly used icons
INFO_ICON = PathIcon("images/info.png")
ERROR_ICON = PathIcon("images/error.png")
NOTICE_ICON = PathIcon("images/notice.png")
FOLDER_ICON = PathIcon("images/folder.png")
DISABLED_ICON = PathIcon("images/disabled.png")
PLUGIN_ICON = PathIcon("images/plugin.png")
EVENT_ICON = PathIcon("images/event.png")
ACTION_ICON = PathIcon("images/action.png")
MACRO_ICON = PathIcon("images/macro.png")

