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

import base64
import pickle
import wx

# Local imports
import eg
from ActionItem import ActionItem
from TreeItem import TreeItem

class PluginItem(ActionItem):
    xmlTag = "Plugin"
    icon = eg.Icons.PLUGIN_ICON
    isRenameable = False
    info = None

    @eg.AssertInActionThread
    def __init__(self, parent, node):
        TreeItem.__init__(self, parent, node)
        if node.text:
            try:
                args = pickle.loads(base64.b64decode(node.text))
            except AttributeError:
                args = ()
        else:
            args = ()
        evalName = node.attrib.get('identifier', None)
        self.pluginName = node.attrib.get('file', None)
        guid = node.attrib.get('guid', self.pluginName)
        self.info = info = eg.pluginManager.OpenPlugin(
            guid,
            evalName,
            args,
            self,
        )
        self.name = eg.text.General.pluginLabel % info.label
        if info.icon != self.icon:
            self.icon = eg.Icons.PluginSubIcon(info.icon)
        #self.icon = info.icon
        self.url = info.url
        self.executable = info.instance

    def AskCut(self):
        return self.AskDelete()

    def AskDelete(self):
        actionItemCls = self.document.ActionItem

        def SearchFunc(obj):
            if obj.__class__ == actionItemCls:
                if obj.executable and obj.executable.plugin == self.executable:
                    return True
            return None

        if self.root.Traverse(SearchFunc) is not None:
            eg.MessageBox(
                eg.text.General.deletePlugin,
                eg.APP_NAME,
                wx.NO_DEFAULT | wx.OK | wx.ICON_EXCLAMATION
            )
            return False
        if not TreeItem.AskDelete(self):
            return False
        return True

    @eg.AssertInActionThread
    def Delete(self):
        info = self.info

        def DoIt():
            info.Close()
            info.instance.OnDelete()
            info.RemovePluginInstance()
        eg.actionThread.Call(DoIt)

        ActionItem.Delete(self)
        self.executable = None
        self.info = None

    @eg.AssertInActionThread
    def Execute(self):
        if not self.isEnabled:
            return None, None
        if eg.config.logActions:
            self.Print(self.name)
        if self.shouldSelectOnExecute:
            wx.CallAfter(self.Select)
        eg.indent += 1
        self.info.Start()
        eg.indent -= 1
        eg.result = self.executable
        return None, None

    # The Find function calls this from MainThread, so we can't restrict this
    # to the ActionThread
    #@eg.AssertInActionThread
    def GetArguments(self):
        return self.info.args

    def GetBasePath(self):
        """
        Returns the filesystem path, where additional files (like pictures)
        should be found.

        Overrides ActionItem.GetBasePath()
        """
        return self.info.path

    def GetData(self):
        attr, text = TreeItem.GetData(self)
        del attr[0]
        attr.append(('Identifier', self.executable.info.evalName))
        guid = self.executable.info.guid
        if guid:
            attr.append(('Guid', guid))
        attr.append(('File', self.pluginName))
        text = base64.b64encode(pickle.dumps(self.info.args, 2))
        return attr, text

    def GetLabel(self):
        return self.name

    def GetTypeName(self):
        return self.executable.info.name

    def NeedsStartupConfiguration(self):
        """
        Returns True if the item wants to be configured after creation.

        Overrides ActionItem.NeedsStartupConfiguration()
        """
        # if the Configure method of the executable is overriden, we assume
        # the item wants to be configured after creation
        return (
            self.executable.Configure.im_func !=
            eg.PluginBase.Configure.im_func
        )

    def RefreshAllVisibleActions(self):
        """
        Calls Refresh() for all currently visible actions of this plugin.
        """
        actionItemCls = self.document.ActionItem
        plugin = self.info.instance

        def Traverse(item):
            if item.__class__ == actionItemCls:
                if item.executable.plugin == plugin:
                    pass
                    #eg.Notify("NodeChanged", item)
            else:
                if item.childs and item in item.document.expandedNodes:
                    for child in item.childs:
                        Traverse(child)
        Traverse(self.root)

    @eg.LogIt
    def RestoreState(self):
        if self.isEnabled:
            eg.actionThread.Call(self.info.Start)

    @eg.LogIt
    @eg.AssertInActionThread
    def SetArguments(self, args):
        info = self.info
        if not info.lastException and args == self.info.args:
            return
        self.info.args = args
        label = info.instance.GetLabel(*args)
        if label != info.label:
            info.label = label
            self.name = eg.text.General.pluginLabel % label
            #eg.Notify("NodeChanged", self)
        self.RefreshAllVisibleActions()
        if self.isEnabled:
            eg.actionThread.Call(self.info.Stop)
            eg.actionThread.Call(self.info.Start)

    def SetAttributes(self, tree, itemId):
        if self.info.lastException or self.info.initFailed:
            tree.SetItemTextColour(itemId, eg.colour.pluginError)

    @eg.AssertInActionThread
    def SetEnable(self, flag=True):
        ActionItem.SetEnable(self, flag)
        if flag:
            self.info.Start()
        else:
            self.info.Stop()
