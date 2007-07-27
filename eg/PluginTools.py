# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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

from os.path import abspath, exists, join, isdir
from base64 import b64decode
from cStringIO import StringIO

import sys
import os
import copy
import types

import Image
import wx
import eg
from Utils import SetClass
from PluginMetaClass import PluginMetaClass
from ActionMetaClass import ActionMetaClass


WX_ICON_PLUGIN = wx.EmptyIcon()
WX_ICON_PLUGIN.CopyFromBitmap(
    wx.Bitmap("images/Plugin.png", wx.BITMAP_TYPE_PNG)
)



def ImportPlugin(pluginDir):
    moduleName = "pluginImport." + pluginDir
    if moduleName in sys.modules:
        return sys.modules[moduleName]
    modulePath = join(eg.PLUGIN_DIR, pluginDir)
    ActionMetaClass.allActionClasses = []
    sys.path.insert(0, modulePath)
    try:
        module = __import__(moduleName, None, None, [''])
    finally:
        del sys.path[0]
    module.__allActionClasses__ = ActionMetaClass.allActionClasses
    return module

    
    
class PluginInfoBase(object):
    """
    This is an abstract class to hold information about a plugin.
    
    It is first subclassed dynamically for every plugin class that gets 
    defined, so the class will hold information about the plugin class. 
    Then everytime a new plugin of that class is instantiated, this 
    PluginInfo subclass gets instantiated also.
    This way attribute access will go from the PluginInfo for the plugins
    instance to the PluginInfo for the plugins class, down to the abstract 
    PluginInfo class.
    """
    # Most important is to know the class of the plugin we are looking at
    pluginCls = None
    
    # path holds the directory where the plugin files reside
    path = None
    
    # name and description will hold the fields defined through the class.
    # Keep in mind, that every plugin instance might get a modified name
    # because it is instantiated more then once.
    name = "unknown"
    description = ""
    
    # some informational fields
    author = "unknown author"
    version = "unknow version"
    
    # kind gives a hint in which group the plugin should be shown in
    # the AddPluginDialog
    kind = "other"
    
    # icon might be an instance of a PIL icon, that the plugin developer
    # has supplied
    icon = eg.Icons.PLUGIN_ICON

    
    evalName = None
    instances = None
    actionList = None
    expanded = False
    lastEvent = eg.EventGhostEvent()
    actionClassList = None
    initFailed = True
    api = 1
    originalText = None
    isStarted = False
    label = None
    treeItem = None
    canMultiLoad = False
    
        
    @classmethod
    def LoadModule(pluginInfo):
        pathname = join(pluginInfo.path, "__init__.py")
        if not exists(pathname):
            eg.PrintError("File %s does not exist" % pathname)
            return
        try:
            module = ImportPlugin(pluginInfo.pluginName)
        except:
            eg.PrintTraceback(
                "Error while loading plugin-file %s." % pluginInfo.path,
                1
            )
            return
        pluginCls = module.__pluginCls__
        pluginInfo.module = module
        pluginInfo.pluginCls = pluginCls
        if getattr(pluginCls, "canMultiLoad", False):
            pluginInfo.canMultiLoad = True
        text = pluginCls.text
        if text is None:
            class text:
                pass
        if type(text) == types.ClassType:
            translation = getattr(eg.text.Plugin, pluginCls.__name__, None)
            if translation is None:
                translation = text()
            SetClass(translation, text)
            text = translation
                
        setattr(eg.text.Plugin, pluginCls.__name__, text)
        text.__class__.name = pluginInfo.englishName
        text.__class__.description = pluginInfo.englishDescription
        pluginCls.text = text
        pluginCls.name = text.name
        pluginCls.description = text.description
        eg.pluginClassInfo[pluginInfo.pluginName] = pluginInfo
        return True
    
    
    @classmethod
    def CreatePluginInstance(pluginInfo, evalName, treeItem):
        info = pluginInfo()
        info.treeItem = treeItem
        pluginCls = pluginInfo.pluginCls
        try:
            plugin = pluginCls.__new__(pluginCls)
        except:
            eg.PrintTraceback()
            return None
        plugin.info = info
        class _Exception(eg.Exception):
            pass
        plugin.Exception = _Exception
        if evalName is None:
            evalName = pluginCls.__name__
            i = 1
            while hasattr(eg.plugins, evalName):
                i += 1
                evalName = pluginCls.__name__ + str(i)
        assert not hasattr(eg.plugins, evalName)
        info.evalName = evalName
        setattr(eg.plugins, evalName, plugin)
        
        if evalName != pluginCls.__name__:
            numStr = evalName[len(pluginCls.__name__):]
            plugin.name = pluginInfo.name + " #" + numStr
        else:
            plugin.name = pluginInfo.name
        plugin.description = pluginInfo.description
        info.eventPrefix = evalName
        if pluginInfo.instances is None:
            pluginInfo.instances = [info]
        else:
            pluginInfo.instances.append(plugin.info)
        ActionMetaClass.allActionClasses = pluginInfo.module.__allActionClasses__
        try:
            plugin.__init__()
            info.initFailed = False
        except eg.Exception, e:
            eg.PrintError(e.message)
        except:
            eg.PrintTraceback()
        pluginInfo.label = plugin
        return plugin
             

        
def GetPluginInfo(pluginName):
    # first look, if we already have cached this plugin class
    info = eg.pluginClassInfo.get(pluginName, None)
    if info is not None:
        return info
    
    if pluginName not in eg.pluginDatabase.database:
        eg.PrintError(eg.text.Error.pluginNotFound % pluginName)
        return None
    
    infoDict = eg.pluginDatabase.GetPluginInfo(pluginName).__dict__
    pluginPath = join("plugins", pluginName)
        
    # create a new sublclass of PluginInfo for this plugin class
    class info(PluginInfoBase):
        name = infoDict.get("name", PluginInfoBase.name)
        description = infoDict.get("description", PluginInfoBase.description)
        author = infoDict.get("author", PluginInfoBase.author)
        version = infoDict.get("version", PluginInfoBase.version)
        kind = infoDict.get("kind", PluginInfoBase.kind)
        api = infoDict.get("api", PluginInfoBase.api)
        canMultiLoad = infoDict.get("canMultiLoad", PluginInfoBase.canMultiLoad)
        path = pluginPath + "/"
    info.pluginName = pluginName
    info.englishName = info.name
    info.englishDescription = info.description
    
    # try to translate name and description
    textCls = getattr(eg.text.Plugin, pluginName, None)
    if textCls is not None:
        info.name = getattr(textCls, "name", info.name)
        info.description = getattr(textCls, "description", info.description)
    info.textCls = textCls
    
    # get the icon if any
    if "icon" in infoDict and infoDict["icon"] is not None:
        info.icon = eg.Icons.StringIcon(infoDict["icon"])
    else:
        iconPath = join(pluginPath, "icon.png")
        if exists(iconPath):
            info.icon = eg.Icons.PathIcon(iconPath)
    
    info.actionClassList = []
    return info


@eg.LogIt
def OpenPlugin(pluginName, evalName, args, treeItem=None):
    info = GetPluginInfo(pluginName)
    if info is None:
        return None
    if info.pluginCls is None:
        if not info.LoadModule():
            return None
    plugin = info.CreatePluginInstance(evalName, treeItem)
    try:
        plugin.info.label = plugin.GetLabel(*args)
    except:
        plugin.info.label = plugin.info.name
    return plugin

        
@eg.LogIt
def ClosePlugin(plugin):
    def _delActionListItems(actionList):
        if actionList is not None:
            for item in actionList:
                if isinstance(item, eg.ActionClass):
                    item.plugin = None
                else:
                    _delActionListItems(item.actionList)
                    item.plugin = None
            del actionList
            
    info = plugin.info
    if not info.initFailed:
        plugin.__close__()
    delattr(eg.plugins, info.evalName)
    _delActionListItems(info.actionList)
    try:
        eg.actionList.remove(plugin)
    except:
        pass
    info.instances.remove(info)
    info.instance = None
    plugin.AddAction = None
    del info
    del plugin


gPluginInfoList = None

def GetPluginInfoList():
    """
    Get a list of all PluginInfo for all plugins in the plugin directory
    """
    global gPluginInfoList
    if gPluginInfoList is not None:
        return gPluginInfoList
    
    gPluginInfoList = []
    for filename in os.listdir("plugins"):
        if filename.startswith(".") or filename.startswith("_"):
            continue
        if not isdir(join("plugins", filename)):
            continue
        info = GetPluginInfo(filename)
        gPluginInfoList.append(info)
    return gPluginInfoList

