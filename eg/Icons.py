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

from os.path import abspath
from base64 import b64decode
from cStringIO import StringIO
import wx
import Image


gIconCache = {}
gImageList = wx.ImageList(16, 16)
gDisabledImage = Image.open("images/disabled.png")
gFolderImage = Image.open("images/folder.png").convert("RGBA")


def PilToBitmap(pil):
    """Convert a PIL image to a wx.Bitmap (with alpha channel support)."""
    image = wx.EmptyImage(pil.size[0], pil.size[1], 32)
    image.SetData(pil.convert('RGB').tostring())
    image.SetAlphaData(pil.convert("RGBA").tostring()[3::4]) 
    return wx.BitmapFromImage(image, 24)



def GetIcon(filePath):
    """Returns a wx.Bitmap loaded from 'filePath'.
    
    Uses PIL functions, because this way we have better alpha channel 
    handling.
    """
    return PilToBitmap(Image.open(filePath).convert("RGBA"))
    
    

class Icon(object):
    """An object representing an icon with some caching functionality.
    
    The icon is initialized by a file path (see PathIcon) or by a base64encoded
    string (see StringIcon). The object will not load/convert any data before
    an attribute is accessed. If for example the "pil" attribute is requested
    the first time, the object will load the underlying resource through the 
    method self._pil() and store the result into self.pil for further requests.
    """
    
    def _pil(self):
        """Return a PIL image of the icon.
        
        Abstract method that must be implemented in a subclass.
        """
        raise NotImplementedError
    
    
    def _index(self):
        """Return the index of this icon inside the global wx.ImageList."""
        return gImageList.Add(PilToBitmap(self.pil))
    
    
    def _disabledIndex(self):
        """Creates a version of the icon with a "disabled" mark overlayed and
        returns its index inside the global wx.ImageList.
        """
        image = self.pil.copy()
        image.paste(gDisabledImage, None, gDisabledImage)
        return gImageList.Add(PilToBitmap(image))
    
    
    def _folderIndex(self):
        """Creates a folder icon with a small version of the icon overlayed and
        returns its index inside the global wx.ImageList. 
        """
        small = self.pil.resize((11,11), Image.BICUBIC)
        image = gFolderImage.copy()
        image.paste(small, (5, 5), small)
        return gImageList.Add(PilToBitmap(image))
    
    
    def GetBitmap(self):
        """Return a wx.Bitmap of the icon."""
        return PilToBitmap(self.pil)


    def GetWxIcon(self):
        """Return a wx.Icon of the icon."""
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(PilToBitmap(self.pil))
        return icon


    def __getattr__(self, name):
        """Implements the caching magic for the icon.
        
        Only called if an attribute 'name' does not exist. The code will look 
        if a corresponding method '_name' exists, calls this method and stores
        the result as 'self.name' (so __getattr__ gets not called again for
        this attribute) and returns the result.
        """
        if not hasattr(self, "_" + name):
            raise
        result = getattr(self, "_" + name)()
        setattr(self, name, result)
        return result
        
        
        
class PathIcon(Icon):
    
    def __new__(cls, path):
        """If an instance of this path is already in the cache, returns the 
        cached instance. Otherwise creates a new instance and adds it to the 
        cache.
        """
        path = abspath(path)
        if gIconCache.has_key(path):
            return gIconCache[path]
        self = super(PathIcon, cls).__new__(cls)
        gIconCache[path] = self
        self.path = path
        return self
    
    
    def _pil(self):
        """Return a PIL image of the icon."""
        return Image.open(self.path).convert("RGBA")
        
        
        
class StringIcon(Icon):
    
    def __new__(cls, data):
        """If an instance of this data is already in the cache, returns the 
        cached instance. Otherwise creates a new instance and adds it to the 
        cache.
        """
        if gIconCache.has_key(data):
            return gIconCache[data]
        self = super(StringIcon, cls).__new__(cls)
        gIconCache[data] = self
        self.data = data
        return self
    
    
    def _pil(self):
        """Return a PIL image of the icon."""
        fd = StringIO(b64decode(self.data))
        pil = Image.open(fd).convert("RGBA")
        fd.close()
        return pil

        
        
# setup some commonly used icons
        
FOLDER_ICON = PathIcon("images/folder.png")
DISABLED_ICON = PathIcon("images/disabled.png")
PLUGIN_ICON = PathIcon("images/plugin.png")
EVENT_ICON = PathIcon("images/event.png")
ACTION_ICON = PathIcon("images/action.png")
MACRO_ICON = PathIcon("images/macro.png")

gImageList.Add(GetIcon("images/info.png"))
gImageList.Add(GetIcon("images/error.png"))
gImageList.Add(GetIcon("images/notice.png"))

           