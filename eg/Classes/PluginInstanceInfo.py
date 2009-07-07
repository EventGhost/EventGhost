# This file is part of EventGhost.
# Copyright (C) 2009 Lars-Peter Voss <bitmonster@eventghost.org>
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

from os.path import join, exists
import eg
from eg.Utils import SetDefault


class PluginProxy(object):

    def __init__(self, plugin):
        self.plugin = plugin
        self.actions = plugin.info.actions


    def __getattr__(self, name):
        return self.actions[name]()



class PluginInstanceInfo(eg.PluginModuleInfo):
    pluginCls = None
    module = None
    treeItem = None
    actions = {}
    evalName = None
    eventPrefix = None
    instance = None
    actionGroup = None
    args = ()
    label = None
    initFailed = True
    lastException = None
    isStarted = False
    lastEvent = eg.EventGhostEvent()
    eventList = None
    
    def __init__(self):
        pass
    
    @classmethod
    def FromModuleInfo(cls, moduleInfo):
        self = cls.__new__(cls)
        self.__dict__.update(moduleInfo.__dict__)
        pathname = join(self.path, "__init__.py")
        if not exists(pathname):
            eg.PrintError("File %s does not exist" % pathname)
            return False
        try:
            module = self.Import()
        except:
            eg.PrintTraceback(
                "Error while loading plugin-file %s." % self.path,
                1
            )
            return False
        pluginCls = module.__pluginCls__
        self.module = module
        self.pluginCls = pluginCls
        defaultText = pluginCls.text
        if defaultText is None:
            class defaultText:
                pass
        defaultText.name = self.englishName
        defaultText.description = self.englishDescription
        translationText = getattr(eg.text.Plugin, pluginCls.__name__, None)
        if translationText is not None:
            SetDefault(translationText, defaultText)
            text = translationText
        else:
            setattr(eg.text.Plugin, pluginCls.__name__, defaultText)
            text = defaultText

        pluginCls.text = text
        pluginCls.name = text.name
        pluginCls.description = text.description
        return self



    def CreateInstance(self, args, evalName, treeItem):
        self.args = args
        self.treeItem = treeItem
        self.actions = {}
        pluginCls = self.pluginCls
        try:
            plugin = pluginCls.__new__(pluginCls)
        except:
            eg.PrintTraceback()
            return None
        plugin.info = self
        self.instance = plugin

        # create an unique exception for every plugin instance
        class _Exception(eg.PluginBase.Exception):
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
        self.evalName = evalName
        setattr(eg.plugins, evalName, PluginProxy(plugin))
        eg.pluginList.append(plugin)

        if evalName != pluginCls.__name__:
            numStr = evalName[len(pluginCls.__name__):]
            plugin.name = self.name + " #" + numStr
        else:
            plugin.name = self.name
        plugin.description = self.description
        self.eventPrefix = evalName
        self.actionGroup = eg.ActionGroup(
            plugin, 
            plugin.name, 
            plugin.description
        )
        eg.actionGroup.items.append(self.actionGroup)
        plugin.AddAction = self.actionGroup.AddAction
        plugin.AddGroup = self.actionGroup.AddGroup
        try:
            plugin.__init__()
            self.initFailed = False
        except eg.Exceptions.PluginNotFound, exc:
            pass
        except eg.Exception, exc:
            eg.PrintError(exc.message)
        except:
            eg.PrintTraceback()

        #pluginInfoCls.label = pluginObj # ???
        if hasattr(plugin, "Compile"):
            plugin.Compile(*args)
        try:
            self.label = plugin.GetLabel(*args)
        except:
            self.label = self.name
        return self


    def Start(self):
        if self.isStarted:
            return
        try:
            self.instance.__start__(*self.args)
            self.isStarted = True
            self.lastException = None
            self.treeItem.ClearErrorState()
        except eg.Exception, exc:
            self.lastException = exc
            msg = eg.text.Error.pluginStartError % self.name
            msg += "\n" + unicode(exc)
            eg.PrintError(msg, source=self.treeItem)
            self.treeItem.SetErrorState()
        except Exception, exc:
            self.lastException = exc
            eg.PrintError(
                eg.text.Error.pluginStartError % self.name,
                source=self.treeItem
            )
            eg.PrintTraceback()
            self.treeItem.SetErrorState()


    def Stop(self):
        """
        This is a wrapper for the __stop__ member of a eg.PluginBase.

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
            self.treeItem.PrintError(msg)
            self.treeItem.SetErrorState()
        except Exception, exc:
            self.lastException = exc
            self.treeItem.PrintError(eg.text.Error.pluginStartError % self.name)
            eg.PrintTraceback()
            self.treeItem.SetErrorState()


    def Close(self):
        eg.PrintDebugNotice("closing %s" % self.path)
        if self.isStarted:
            self.Stop()
        if not self.initFailed:
            self.instance.__close__()


    def RemovePluginInstance(self):
        plugin = self.instance
        def DeleteActionListItems(items):
            if items is None:
                return
            for item in items:
                if isinstance(item, type) and issubclass(item, eg.ActionBase):
                    item.plugin = None
                else:
                    DeleteActionListItems(item.items)
                    item.plugin = None
            del items

        delattr(eg.plugins, self.evalName)
        eg.pluginList.remove(plugin)
        DeleteActionListItems(self.actionGroup.items)
        try:
            eg.actionGroup.items.remove(self.actionGroup)
        except:
            pass
        self.instance = None
        plugin.AddAction = None


        
