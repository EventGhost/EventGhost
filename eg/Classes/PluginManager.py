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



class NonexistentPlugin(eg.PluginBase):

    def __init__(self):
        raise self.Exceptions.PluginNotFound

    def __start__(self, *dummyArgs):
        raise self.Exceptions.PluginNotFound



class PluginManager:

    def __init__(self):
        self.database = {}
        self.ScanAllPlugins()


    @eg.TimeIt
    def ScanAllPlugins(self):
        """
        Scans the plugin directories to get all needed information for all
        plugins.
        """
        self.database.clear()
        
        # scan through all directories in the plugin directory
        for root in (eg.corePluginDir, eg.userPluginDir):
            for dirname in os.listdir(root):
                # filter out non-plugin names
                if dirname.startswith(".") or dirname.startswith("_"):
                    continue
                pluginDir = join(root, dirname)
                if not isdir(pluginDir):
                    continue
                if not exists(join(pluginDir, "__init__.py")):
                    continue
                info = eg.PluginModuleInfo(pluginDir)
                self.database[info.guid] = info
        
        
    def GetPluginInfoList(self):
        """
        Get a list of all PluginInfo for all plugins in the plugin directory
        """
        self.ScanAllPlugins()
        infoList = self.database.values()
        infoList.sort(key=lambda pluginInfo: pluginInfo.name.lower())
        return infoList


    def GetPluginInfo(self, ident):
        if ident in self.database:
            return self.database[ident]
        else:
            for guid, info in self.database.iteritems():
                if info.pluginName == ident:
                    return info
        return None
    
    
    def OpenPlugin(self, ident, evalName, args, treeItem=None):
        moduleInfo = self.GetPluginInfo(ident)
        if moduleInfo is None:
            # we don't have such plugin
            clsInfo = eg.PluginInstanceInfo()
            clsInfo.guid = ident
            clsInfo.name = ident + " not found"
            clsInfo.pluginName = ident
            clsInfo.pluginCls = NonexistentPlugin
        else:
            clsInfo = eg.PluginInstanceInfo.FromModuleInfo(moduleInfo)
        info = clsInfo.CreateInstance(args, evalName, treeItem)
        return info
