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

from os.path import exists, join

import sys
import types

from Utils import SetClass



class PluginProxy(object):
    
    def __init__(self, plugin):
        self.plugin = plugin
        self.actions = plugin.info.actions
        
    
    def __getattr__(self, name):
        return self.actions[name]
        

def ImportPlugin(pluginDir):
    moduleName = "pluginImport." + pluginDir
    if moduleName in sys.modules:
        return sys.modules[moduleName]
    modulePath = join(eg.PLUGIN_DIR, pluginDir)
    sys.path.insert(0, modulePath)
    try:
        module = __import__(moduleName, None, None, [''])
    finally:
        del sys.path[0]
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
    originalText = None
    isStarted = False
    label = None
    treeItem = None
    canMultiLoad = False
    createMacrosOnAdd = False
    
    eventList = None
    lastException = None
    instance = None
    url = None
        
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
    def CreatePluginInstance(pluginInfoCls, evalName, treeItem):
        info = pluginInfoCls()
        info.treeItem = treeItem
        info.actions = {}
        pluginCls = pluginInfoCls.pluginCls
        try:
            plugin = pluginCls.__new__(pluginCls)
        except:
            eg.PrintTraceback()
            return None
        plugin.info = info
        
        # create an unique exception for every plugin instance
        class _Exception(eg.PluginClass.Exception):
            obj = plugin
        plugin.Exception = _Exception
        plugin.Exceptions = eg.ExceptionsProvider(plugin)
        
        if evalName is None:
            evalName = pluginCls.__name__
            i = 1
            while hasattr(eg.plugins, evalName):
                i += 1
                evalName = pluginCls.__name__ + str(i)
        assert not hasattr(eg.plugins, evalName)
        info.evalName = evalName
        setattr(eg.plugins, evalName, PluginProxy(plugin))
        eg.pluginList.append(plugin)
        
        if evalName != pluginCls.__name__:
            numStr = evalName[len(pluginCls.__name__):]
            plugin.name = pluginInfoCls.name + " #" + numStr
        else:
            plugin.name = pluginInfoCls.name
        plugin.description = pluginInfoCls.description
        info.eventPrefix = evalName
        if pluginInfoCls.instances is None:
            pluginInfoCls.instances = [info]
        else:
            pluginInfoCls.instances.append(plugin.info)
        try:
            plugin.__init__()
            info.initFailed = False
            info.instance = plugin
        except eg.Exception, e:
            eg.PrintError(e.message)
        except:
            eg.PrintTraceback()
        pluginInfoCls.label = plugin
        return info
             
             
    def Start(self, args=(), kwargs={}):
        if self.isStarted:
            return
        try:
            self.instance.__start__(*args, **kwargs)
            self.isStarted = True
            self.lastException = None
            self.treeItem.ClearErrorState()
        except eg.Exception, exc:
            self.lastException = exc
            msg = eg.text.Error.pluginStartError % self.name
            msg += "\n" + unicode(exc)
            eg.log.PrintItem(msg, eg.Icons.ERROR_ICON, self.treeItem)
            self.treeItem.SetErrorState()
        except Exception, exc:
            self.lastException = exc
            eg.PrintError(eg.text.Error.pluginStartError % self.name)
            eg.PrintTraceback()
            self.treeItem.SetErrorState()
            
            
    def Stop(self):
        """
        This is a wrapper for the __stop__ member of a eg.PluginClass.
        
        It should only be called from the ActionThread.
        """
        if self.lastException:
            return
        if not self.isStarted:
            return
        self.isStarted = False
        try:
            self.instance.__stop__()
        except eg.Exception, exc:
            self.lastException = exc
            msg = eg.text.Error.pluginStartError % self.name
            msg += "\n" + unicode(exc)
            eg.log.PrintItem(msg, eg.Icons.ERROR_ICON, self.treeItem)
            self.treeItem.SetErrorState()
        except Exception, exc:
            self.lastException = exc
            eg.PrintError(eg.text.Error.pluginStartError % self.name)
            eg.PrintTraceback()
            self.treeItem.SetErrorState()
            
            
            
def GetPluginInfo(pluginName):
    # first look, if we already have cached this plugin class
    info = eg.pluginClassInfo.get(pluginName, None)
    if info is not None:
        return info
    
    if pluginName not in eg.pluginManager.database:
        eg.PrintError(eg.text.Error.pluginNotFound % pluginName)
        return None
    
    infoDict = eg.pluginManager.GetPluginInfo(pluginName).__dict__
    pluginPath = join("plugins", pluginName)
        
    # create a new sublclass of PluginInfo for this plugin class
    class info(PluginInfoBase):
        name = infoDict.get("name", PluginInfoBase.name)
        description = infoDict.get("description", PluginInfoBase.description)
        author = infoDict.get("author", PluginInfoBase.author)
        version = infoDict.get("version", PluginInfoBase.version)
        kind = infoDict.get("kind", PluginInfoBase.kind)
        url = infoDict.get("url", PluginInfoBase.url)
        canMultiLoad = infoDict.get("canMultiLoad", PluginInfoBase.canMultiLoad)
        createMacrosOnAdd = infoDict.get("createMacrosOnAdd", PluginInfoBase.createMacrosOnAdd)
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
    pluginInfoCls = GetPluginInfo(pluginName)
    if pluginInfoCls is None:
        return None
    if pluginInfoCls.pluginCls is None:
        if not pluginInfoCls.LoadModule():
            return None
    info = pluginInfoCls.CreatePluginInstance(evalName, treeItem)
    plugin = info.instance
    plugin.SetArguments(*args)
    if hasattr(plugin, "Compile"):
        plugin.Compile(*args)
    try:
        info.label = plugin.GetLabel(*args)
    except:
        info.label = plugin.info.name
    return info

        
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


