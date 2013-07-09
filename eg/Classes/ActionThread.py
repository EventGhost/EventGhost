# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import eg
from time import clock

EVENT_ICON_INDEX = eg.EventItem.icon.index


class ActionThread(eg.ThreadWorker):
    corePluginInfos = None

    @eg.LogItWithReturn
    def StartSession(self, filename):
        eg.eventTable.clear()
        self.corePluginInfos = []
        for guid in eg.CORE_PLUGIN_GUIDS:
            try:
                pluginInfo = eg.pluginManager.OpenPlugin(guid, None, ())
                pluginInfo.instance.__start__()
                pluginInfo.isStarted = True
                self.corePluginInfos.append(pluginInfo)
            except: # pylint: disable-msg=W0702
                eg.PrintTraceback()
        start = clock()
        eg.document.Load(filename)
        eg.PrintDebugNotice("XML loaded in %f seconds." % (clock() - start))

        missingIds = (
            set(eg.WinUsb.ListDevices().iterkeys())
            - set(
                item.executable.info.hardwareId
                    for item in eg.document.autostartMacro.childs
                        if item.xmlTag == "Plugin"
            )
        )
        missingPlugins = [
            pluginInfo for pluginInfo in eg.pluginManager.database.itervalues()
                if pluginInfo.hardwareId in missingIds
        ]
        if missingPlugins:
            print "EventGhost has found devices on your system, that can be "
            print "handled by the following plugins and are not loaded by your"
            print "current configuration:"
            for pluginInfo in missingPlugins:
                print "   -", pluginInfo.name
            print "If you want to use them, please add the missing plugins."

        eg.programCounter = (eg.document.autostartMacro, None)
        eg.RunProgram()


    @staticmethod
    def ExecuteTreeItem(obj, event):
        eg.SetProcessingState(2, event)
        eg.event = event
        if isinstance(obj, eg.MacroItem):
            eg.programCounter = (obj, 0)
            eg.RunProgram()
        elif isinstance(obj, eg.ActionItem):
            obj.Execute()
        eg.SetProcessingState(1, event)


    @eg.LogIt
    def StopSession(self):
        eg.document.autostartMacro.UnloadPlugins()
        for pluginInfo in self.corePluginInfos:
            try:
                pluginInfo.Close()
                pluginInfo.RemovePluginInstance()
            except: # pylint: disable-msg=W0702
                eg.PrintTraceback()


    def HandleAction(self, action):
        try:
            action()
        except eg.PluginBase.Exception, exc:
            pluginInfo = exc.obj.info
            eg.PrintError(exc.message, source=pluginInfo.treeItem)
            pluginInfo.lastException = exc
            pluginInfo.treeItem.Refresh()


    @staticmethod
    def OnComputerSuspend():
        """Calls OnComputerSuspend of every enabled plugin."""
        for plugin in eg.pluginList:
            if plugin.info.isStarted:
                try:
                    plugin.OnComputerSuspend(None)
                except: # pylint: disable-msg=W0702
                    eg.PrintTraceback()


    @staticmethod
    def OnComputerResume():
        """Calls OnComputerResume of every enabled plugin."""
        for plugin in eg.pluginList:
            if plugin.info.isStarted:
                try:
                    plugin.OnComputerResume(None)
                except: # pylint: disable-msg=W0702
                    eg.PrintTraceback()

