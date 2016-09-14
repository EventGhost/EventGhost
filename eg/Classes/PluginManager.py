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

import os
from os.path import exists, isdir, join

# Local imports
import eg

class PluginManager:
    def __init__(self):
        self.database = {}
        self.ScanAllPlugins()

    def GetPluginInfo(self, ident):
        if ident in self.database:
            return self.database[ident]
        else:
            for guid, info in self.database.iteritems():
                if info.pluginName == ident:
                    return info
        return None

    def GetPluginInfoList(self):
        """
        Get a list of all PluginInfo for all plugins in the plugin directory
        """
        self.ScanAllPlugins()
        infoList = self.database.values()
        infoList.sort(key=lambda pluginInfo: pluginInfo.name.lower())
        return infoList

    def OpenPlugin(self, ident, evalName, args, treeItem=None):
        moduleInfo = self.GetPluginInfo(ident)
        if moduleInfo is None:
            # we don't have such plugin
            clsInfo = NonexistentPluginInfo(ident, evalName)
        else:
            try:
                clsInfo = eg.PluginInstanceInfo.FromModuleInfo(moduleInfo)
            except eg.Exceptions.PluginLoadError:
                if evalName:
                    clsInfo = NonexistentPluginInfo(ident, evalName)
                else:
                    raise
        info = clsInfo.CreateInstance(args, evalName, treeItem)
        if moduleInfo is None:
            info.actions = ActionsMapping(info)
        return info

    @eg.TimeIt
    def ScanAllPlugins(self):
        """
        Scans the plugin directories to get all needed information for all
        plugins.
        """
        self.database.clear()

        # scan through all directories in the plugin directory
        for root in eg.pluginDirs:
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


class ActionsMapping(object):
    def __init__(self, info):
        self.info = info
        self.actions = {}

    def __getitem__(self, name):
        if name in self.actions:
            return self.actions[name]

        class Action(eg.ActionBase):
            pass
        Action.__name__ = name
        action = self.info.actionGroup.AddAction(Action, hidden=True)
        self.actions[name] = action
        return action

    def __setitem__(self, name, value):
        self.actions[name] = value


class LoadErrorPlugin(eg.PluginBase):
    def __init__(self):
        raise self.Exceptions.PluginLoadError

    def __start__(self, *dummyArgs):
        raise self.Exceptions.PluginLoadError


class NonexistentPlugin(eg.PluginBase):
    class text:
        pass

    def __init__(self):
        raise self.Exceptions.PluginNotFound

    def __start__(self, *dummyArgs):
        raise self.Exceptions.PluginNotFound

    def GetLabel(self, *dummyArgs):
        return '<Unknown Plugin "%s">' % self.name


class NonexistentPluginInfo(eg.PluginInstanceInfo):
    def __init__(self, guid, name):
        self.guid = guid
        self.name = name
        self.pluginName = name

        class Plugin(NonexistentPlugin):
            pass

        Plugin.__name__ = name
        self.pluginCls = Plugin
