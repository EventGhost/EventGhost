import threading
import pythoncom
import types
import wx

import eg
from ThreadWorker import ThreadWorker
from time import clock

EVENT_ICON_INDEX = eg.EventItem.iconIndex

CORE_PLUGINS = (
    "EventGhost",
    "System",
    "Window",
    "Mouse",
)


class ActionThread(ThreadWorker):
    
    @eg.logit(print_return=True) 
    def StartSession(self, filename):
        eg.eventTable.clear()
        eg.corePlugins.clear()
        from InternalActionMixin import ActionClass, ActionWithStringParameter
        eg.SetAttr("ActionClass", ActionClass)
        eg.SetAttr("ActionWithStringParameter", ActionWithStringParameter)
        for pluginIdent in CORE_PLUGINS:
            plugin = eg.OpenPlugin(pluginIdent)
            plugin.__start__()
            plugin.info.isStarted = True
            plugin.info.label = plugin.info.name
            eg.corePlugins[plugin] = 1
        from ActionClass import ActionClass, ActionWithStringParameter        
        eg.SetAttr("ActionClass", ActionClass)
        eg.SetAttr("ActionWithStringParameter", ActionWithStringParameter)
        start = clock()
        eg.document.Load(filename)
        eg.notice("XML loaded in %f seconds." % (clock() - start))
        eg.SetProgramCounter((eg.document.autostartMacro, None))
        eg.RunProgram()
        
            
    def ExecuteTreeItem(self, obj, event):
        eg.SetProcessingState(2, event)
        eg.event = event
        if isinstance(obj, eg.MacroItem):
            eg.SetProgramCounter((obj, 0))
            eg.RunProgram()
        elif isinstance(obj, eg.ActionItem):
            obj.Execute()
        eg.SetProcessingState(1, event)
        
        
    @eg.logit()
    def StopSession(self):
        eg.document.autostartMacro.UnloadPlugins()
        eg.notice("closing default plugins")
        for pluginIdent in CORE_PLUGINS:
            plugin = getattr(eg.plugins, pluginIdent)
            plugin.__stop__()
            eg.ClosePlugin(plugin)
        eg.notice("StopSession done")
        
