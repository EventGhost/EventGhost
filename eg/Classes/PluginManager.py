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

import os
from os.path import isdir, join, exists

import eg


class LoadErrorPlugin(eg.PluginBase):

    def __init__(self):
        raise self.Exceptions.PluginLoadError

    def __start__(self, *dummyArgs):
        raise self.Exceptions.PluginLoadError



class UnknownPlugin(eg.PluginBase):

    def __init__(self):
        raise self.Exceptions.PluginNotFound

    def __start__(self, *dummyArgs):
        raise self.Exceptions.PluginNotFound



class PluginManager:

    def __init__(self):
        self.database = {}
        self.guidDatabase = {}
        self.ScanAllPlugins()


    @eg.TimeIt
    def ScanAllPlugins(self):
        """
        Scans the plugin directories to get all needed information for all
        plugins.
        """
        self.database.clear()
        self.guidDatabase.clear()
        
        # scan through all directories in the plugin directory
        for root in (eg.PLUGIN_DIR, eg.userPluginDir):
            for dirname in os.listdir(root):
                # filter out non-plugin names
                if dirname.startswith(".") or dirname.startswith("_"):
                    continue
                pluginDir = join(root, dirname)
                if not isdir(pluginDir):
                    continue
                if not exists(join(pluginDir, "__init__.py")):
                    continue
                self.AddPlugin(pluginDir)


    def AddPlugin(self, pluginDir):
        info = eg.PluginModuleInfo(pluginDir)
        if info.guid:
            self.guidDatabase[info.guid] = info
        dirname = os.path.basename(pluginDir)
        self.database[dirname] = info
        
        
    def RemovePlugin(self, pluginInfo):
        guid = pluginInfo.guid
        if guid in self.guidDatabase:
            del self.guidDatabase[guid]
        dirname = os.path.basename(pluginInfo.path)
        if dirname in self.database:
            del self.database[dirname]
            
        
    def GetPluginInfoList(self):
        """
        Get a list of all PluginInfo for all plugins in the plugin directory
        """
        self.ScanAllPlugins()
        infoList = self.database.values()
        infoList.sort(key=lambda x: x.name.lower())
        return infoList


    def OpenPlugin(self, pluginName, evalName, args, treeItem=None, guid=None):
        if guid is not None and guid in self.guidDatabase:
            # loading by GUID is preferred
            moduleInfo = self.guidDatabase[guid]
            clsInfo = eg.PluginInstanceInfo.FromModuleInfo(moduleInfo)
        elif pluginName in self.database:
            # otherwise get it by folder name
            moduleInfo = self.database[pluginName]
            clsInfo = eg.PluginInstanceInfo.FromModuleInfo(moduleInfo)
        else:
            # we don't have such plugin
            clsInfo = eg.PluginInstanceInfo()
            clsInfo.guid = guid
            clsInfo.name = pluginName + " not found"
            clsInfo.pluginName = pluginName
            clsInfo.pluginCls = UnknownPlugin
                    
        info = clsInfo.CreateInstance(args, evalName, treeItem)
        return info
