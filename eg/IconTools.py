import wx
import Image
import zipfile
import StringIO


gPluginIconDict = {}


def pilToBitmap(pil):
    colour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
    pil2 = Image.new(
        "RGBA", 
        (16,16), 
        (colour.Red(), colour.Green(), colour.Blue())
    )
    pil2.paste(pil, None, pil)
    image = wx.EmptyImage(pil2.size[0], pil2.size[1], 32)
    image.SetData(pil2.convert('RGB').tostring())
    image.SetAlphaData(pil.convert("RGBA").tostring()[3::4]) 
    image.ConvertAlphaToMask(10)
    #image.SetMaskColour(255,255,255)
    bmp = wx.BitmapFromImage(image, 24)
    return bmp


def GetIcon(filename):
    #return wx.BitmapFromImage(wx.Image(filename, wx.BITMAP_TYPE_PNG))
    pil = Image.open(filename).convert("RGBA")
    pil2 = Image.new("RGBA", (16,16), gColourTuple)
    try:
        pil2.paste(pil, None, pil)
    except:
        eg.PrintError("Can't convert %s" % filename)
    image = wx.EmptyImage(pil2.size[0], pil2.size[1], 32)
    image.SetData(pil2.convert('RGB').tostring())
    image.SetAlphaData(pil.convert("RGBA").tostring()[3::4]) 
    image.SetMaskColour(255,255,255)
    image.ConvertAlphaToMask(128)
    bmp = wx.BitmapFromImage(image, 24)
    return bmp


def GetWxIconFromFile(filename):
    icon = wx.EmptyIcon()
    icon.CopyFromBitmap(
        wx.BitmapFromImage(wx.Image(filename, wx.BITMAP_TYPE_PNG))
    )
    return icon


    
def SetupIcons(name):
    image1 = Image.open("images/" + name + ".png").convert("RGBA")
    return SetupIcons2(image1)
    
    

def SetupIcons2(image1):
    if not image1:
        return 0
    image2 = image1.copy()
    image2.paste(gDisabledImage, None, gDisabledImage)
    bmp1 = pilToBitmap(image1)
    bmp2 = pilToBitmap(image2)
    idx = gImageList.Add(bmp1)
    gImageList.Add(bmp2)
    gImageList2.append(bmp1)
    gImageList2.append(bmp2)
    return idx


def SetupPluginIcons(image1):
    if not image1:
        return 0
    image2 = image1.copy()
    image2.paste(gDisabledImage, None, gDisabledImage)
    bmp1 = pilToBitmap(image1)
    bmp2 = pilToBitmap(image2)
    
    small = image1.resize((11,11), Image.BICUBIC)
    image3 = FOLDER_ICON.copy()
    image3.paste(small, (5, 5), small)
    bmp3 = pilToBitmap(image3)
    
    idx = gImageList.Add(bmp1)
    gImageList.Add(bmp2)
    gImageList.Add(bmp3)
    gImageList2.append(bmp1)
    gImageList2.append(bmp2)
    gImageList2.append(bmp3)
    return idx
    
    
def CreateActionGroupIcon(plugin, iconFile):
    image1 = Image.open(plugin.info.path + iconFile + ".png").convert("RGBA")
    small = image1.resize((11,11), Image.BICUBIC)
    image3 = FOLDER_ICON.copy()
    image3.paste(small, (5, 5), small)
    bmp = pilToBitmap(image3)
    idx = gImageList.Add(bmp)
    return idx

    
def GetPluginIcon(name):
    pathname = "Plugins\\" + name + "\\icon.png"
    try:
        image = Image.open(pathname).convert("RGBA")
#        image = wx.EmptyImage(pil.size[0], pil.size[1])
#        image.SetData(pil.convert('RGB').tostring())
#        image.SetAlphaData(pil.convert('RGBA').split()[3].tostring())
#        if not image.Ok():
#            image = None
        return image
    except:
        try:
            pathname = "Plugins\\" + name + ".egp"
            importer = zipfile.ZipFile(pathname, 'r')
            data = importer.read('icon.png')
            importer.close()
            image = Image.open(StringIO.StringIO(data)).convert("RGBA")
#            image = wx.EmptyImage(pil.size[0], pil.size[1])
#            image.SetData(pil.convert('RGB').tostring())
#            image.SetAlphaData(pil.convert('RGBA').split()[3].tostring())
#            if not image.Ok():
#                image = None
        except:
            image = None
    return image


def GetIconWithIndex(idx):
    return gImageList2[idx]
    

def AddPluginIcon(pluginName):
    global gPluginIconDict
    if gPluginIconDict.has_key(pluginName):
        return gPluginIconDict[pluginName]
    index = SetupIcons2(GetPluginIcon(pluginName))
    gPluginIconDict[pluginName] = index
    return index

def Init():
    global gColour, gColourTuple
    gColour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
    gColourTuple = (gColour.Red(), gColour.Green(), gColour.Blue())

    global gImageList, gImageList2
    gImageList = wx.ImageList(16, 16)
    gImageList2 = []
    icon = GetIcon("images/info.png")
    gImageList.Add(icon)
    gImageList2.append(icon)
    icon = GetIcon("images/error.png")
    gImageList.Add(icon)
    gImageList2.append(icon)
    icon = GetIcon("images/notice.png")
    gImageList.Add(icon)
    gImageList2.append(icon)
    
    global gDisabledImage
    gDisabledImage = Image.open("images/disabled.png")
    
    global FOLDER_ICON
    FOLDER_ICON = Image.open("images/folder.png").convert("RGBA")
    
    global ICON_IDX_FOLDER
    ICON_IDX_FOLDER = SetupIcons("folder")
    
    global ICON_IDX_PLUGIN
    ICON_IDX_PLUGIN = SetupPluginIcons(Image.open("images/plugin.png"))
    
