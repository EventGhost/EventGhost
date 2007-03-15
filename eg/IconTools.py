# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <lpv@eventghost.org>
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

import wx
import Image
import zipfile
import StringIO

class Icon:
    iconIndex = None
    image = None
    
    def __init__(self, filePath):
        pass
    


def PilToBitmap(pil):
    #colour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
#    pil2 = Image.new(
#        "RGBA", 
#        (16,16), 
#        #(colour.Red(), colour.Green(), colour.Blue())
#    )
    #pil2.paste(pil, None, pil)
    image = wx.EmptyImage(pil.size[0], pil.size[1], 32)
    image.SetData(pil.convert('RGB').tostring())
    image.SetAlphaData(pil.convert("RGBA").tostring()[3::4]) 
    #image.ConvertAlphaToMask(10)
    #image.SetMaskColour(255,255,255)
    bmp = wx.BitmapFromImage(image, 24)
    return bmp


def GetIcon(filename):
    pil = Image.open(filename).convert("RGBA")
#    pil2 = Image.new("RGBA", (16,16), gColourTuple)
#    try:
#        pil2.paste(pil, None, pil)
#    except:
#        eg.PrintError("Can't convert %s" % filename)
    image = wx.EmptyImage(pil.size[0], pil.size[1], 32)
    image.SetData(pil.convert('RGB').tostring())
    image.SetAlphaData(pil.convert("RGBA").tostring()[3::4]) 
    #image.SetMaskColour(255,255,255)
    #image.ConvertAlphaToMask(128)
    bmp = wx.BitmapFromImage(image, 24)
    return bmp


    
def SetupIcons(name):
    image1 = Image.open("images/" + name + ".png").convert("RGBA")
    return SetupIcons2(image1)
    
    

def SetupIcons2(image1):
    if not image1:
        return 0
    image2 = image1.copy()
    image2.paste(gDisabledImage, None, gDisabledImage)
    bmp1 = PilToBitmap(image1)
    bmp2 = PilToBitmap(image2)
    idx = gImageList.Add(bmp1)
    gImageList.Add(bmp2)
    return idx


def SetupPluginIcons(image1):
    if not image1:
        return 0
    image2 = image1.copy()
    image2.paste(gDisabledImage, None, gDisabledImage)
    bmp1 = PilToBitmap(image1)
    bmp2 = PilToBitmap(image2)
    
    small = image1.resize((11,11), Image.BICUBIC)
    image3 = FOLDER_ICON.copy()
    image3.paste(small, (5, 5), small)
    bmp3 = PilToBitmap(image3)
    
    idx = gImageList.Add(bmp1)
    gImageList.Add(bmp2)
    gImageList.Add(bmp3)
    return idx
    
    
def CreateActionGroupIcon(plugin, iconFile):
    image1 = Image.open(plugin.info.path + iconFile + ".png").convert("RGBA")
    small = image1.resize((11,11), Image.BICUBIC)
    image3 = FOLDER_ICON.copy()
    image3.paste(small, (5, 5), small)
    bmp = PilToBitmap(image3)
    idx = gImageList.Add(bmp)
    return idx

    
_gPluginIconDict = {}

def AddPluginIcon(pluginName):
    global gPluginIconDict
    if _gPluginIconDict.has_key(pluginName):
        return _gPluginIconDict[pluginName]
    pathname = "plugins\\" + pluginName + "\\icon.png"
    try:
        image = Image.open(pathname).convert("RGBA")
    except:
        image = None
    index = SetupIcons2(image)
    _gPluginIconDict[pluginName] = index
    return index


def Init():
    global gColour, gColourTuple
    gColour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
    gColourTuple = (gColour.Red(), gColour.Green(), gColour.Blue())

    global gImageList
    gImageList = wx.ImageList(16, 16)
    icon = GetIcon("images/info.png")
    gImageList.Add(icon)
    icon = GetIcon("images/error.png")
    gImageList.Add(icon)
    icon = GetIcon("images/notice.png")
    gImageList.Add(icon)
    
    global gDisabledImage
    gDisabledImage = Image.open("images/disabled.png")
    
    global FOLDER_ICON
    FOLDER_ICON = Image.open("images/folder.png").convert("RGBA")
    
    global ICON_IDX_FOLDER
    ICON_IDX_FOLDER = SetupIcons("folder")
    
    global ICON_IDX_PLUGIN
    ICON_IDX_PLUGIN = SetupPluginIcons(Image.open("images/plugin.png"))
    
