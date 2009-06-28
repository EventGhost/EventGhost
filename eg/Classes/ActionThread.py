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

import eg
from time import clock

EVENT_ICON_INDEX = eg.EventItem.icon.index


class ActionThread(eg.ThreadWorker):

    @staticmethod
    @eg.LogItWithReturn
    def StartSession(filename):
        eg.eventTable.clear()
        for pluginIdent in eg.CORE_PLUGINS:
            # pylint: disable-msg=W0702
            try:
                pluginInfo = eg.PluginInfo.Open(pluginIdent, None, ())
                pluginInfo.instance.__start__()
                pluginInfo.isStarted = True
            except:
                eg.PrintTraceback()
        start = clock()
        eg.document.Load(filename)
        eg.PrintDebugNotice("XML loaded in %f seconds." % (clock() - start))
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


    @staticmethod
    @eg.LogIt
    def StopSession():
        eg.document.autostartMacro.UnloadPlugins()
        for pluginIdent in eg.CORE_PLUGINS:
            # pylint: disable-msg=W0702
            try:
                pluginInfo = getattr(eg.plugins, pluginIdent).plugin.info
                pluginInfo.Close()
                pluginInfo.RemovePluginInstance()
            except:
                eg.PrintTraceback()


    def HandleAction(self, action):
        try:
            action()
        except eg.PluginBase.Exception, exc:
            pluginInfo = exc.obj.info
            eg.PrintError(exc.message, source=pluginInfo.treeItem)
            pluginInfo.lastException = exc
            pluginInfo.treeItem.SetErrorState()


    @staticmethod
    def OnComputerSuspend():
        """Calls OnComputerSuspend of every enabled plugin."""
        for plugin in eg.pluginList:
            if plugin.info.isStarted:
                # pylint: disable-msg=W0702
                try:
                    plugin.OnComputerSuspend(None)
                except:
                    eg.PrintTraceback()


    @staticmethod
    def OnComputerResume():
        """Calls OnComputerResume of every enabled plugin."""
        for plugin in eg.pluginList:
            if plugin.info.isStarted:
                # pylint: disable-msg=W0702
                try:
                    plugin.OnComputerResume(None)
                except:
                    eg.PrintTraceback()

