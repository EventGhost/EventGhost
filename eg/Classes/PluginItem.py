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

import base64
import pickle

import wx

import eg
from ActionItem import ActionItem
from TreeItem import TreeItem



class PluginItem(ActionItem):
    xmlTag = "Plugin"
    icon = eg.Icons.PLUGIN_ICON
    isRenameable = False            
    
    def WriteToXML(self):
        attr, text, childs = TreeItem.WriteToXML(self)
        del attr[0]
        attr.append(('File', self.pluginFile))
        if self.executable:
            attr.append(('Identifier', self.executable.info.evalName))
        text = base64.b64encode(pickle.dumps(self.args, 2))
        return attr, text, childs
    
    
    def __init__(self, parent, node):
        TreeItem.__init__(self, parent, node)
        if node.text:
            self.args = pickle.loads(base64.b64decode(node.text))
        else:
            self.args = ()
        ident = node.attrib.get('identifier', None)
        pluginStr = node.attrib['file']
        self.pluginFile = pluginStr
        self.info = info = eg.OpenPlugin(pluginStr, ident, self.args, self)
        if info is None or info.initFailed:
            #eg.PrintError("Error loading plugin: %s" % pluginStr)
            self.name = pluginStr + " not found"
        else:
            self.name = eg.text.General.pluginLabel % info.label
            self.icon = info.icon
            self.executable = info.instance


    def GetLabel(self):
        return self.name
        
    
    @eg.LogIt
    def RestoreState(self):
        if self.isEnabled:
            eg.actionThread.Call(self.StartPlugin)
            
    
    def SetAttributes(self, tree, id):
        if self.info.lastException:
            tree.SetItemTextColour(id, eg.colour.pluginError)
    
    
    def _SetColour(self, colour):
        if self.id is not None:
            self.tree.SetItemTextColour(self.id, colour)
        
        
    def SetErrorState(self):
        wx.CallAfter(self._SetColour, eg.colour.pluginError)
        
        
    def ClearErrorState(self):
        wx.CallAfter(self._SetColour, eg.colour.treeItem)
        
        
    def Refresh(self):
        pass
    
    
    def Execute(self):
        if not self.isEnabled:
            return None, None
        if eg.config.logActions:
            self.Print(self.name)
        if self.shouldSelectOnExecute:
            #self.Select()
            wx.CallAfter(self.Select)
        self.StartPlugin()
        eg.result = self.executable
        return None, None
        
        
    def StartPlugin(self):
        """
        This is a wrapper for the __start__ member of a eg.PluginClass.
        
        It should only be called from the ActionThread.
        """
        if self.info:
            self.info.Start(self.args)
        
        
    def StopPlugin(self):
        """
        This is a wrapper for the __stop__ member of a eg.PluginClass.
        
        It should only be called from the ActionThread.
        """
        if self.info:
            self.info.Stop()
        
        
    def Enable(self, flag=True):
        ActionItem.Enable(self, flag)
        if flag:
            eg.actionThread.Call(self.StartPlugin)
        else:
            eg.actionThread.Call(self.StopPlugin)


    def _Delete(self):
        if self.executable:
            def ClosePlugin():
                self.StopPlugin()
                eg.ClosePlugin(self.executable)
                self.executable = None
                self.info = None
            eg.actionThread.Call(ClosePlugin)
            
        ActionItem._Delete(self)
        
        
    def AskDelete(self):
        ActionItem = self.document.ActionItem
        def searchFunc(obj):
            if obj.__class__ == ActionItem:
                if obj.executable and obj.executable.plugin == self.executable:
                    return True
            return None
        if self.root.Traverse(searchFunc) is not None:
            answer = wx.MessageBox(
                eg.text.General.deletePlugin,
                eg.APP_NAME, 
                wx.NO_DEFAULT|wx.OK|wx.ICON_EXCLAMATION
            )
            return False
        if not TreeItem.AskDelete(self):
            return False
        return True
    
    
    def AskCut(self):
        return self.AskDelete()
    
    
    def NeedsStartupConfiguration(self):
        if self.info.instance.Configure.im_func != eg.PluginClass.Configure.im_func:
            return True
        return False
    
    
    def ShowHelp(self):
        plugin = self.info.instance
        eg.HTMLDialog(
            eg.text.General.pluginLabel % plugin.name, 
            plugin.description, 
            plugin.info.icon.GetWxIcon(),
            basePath=plugin.info.path
        ).DoModal()
        
                        
    @eg.LogIt
    def SetParams(self, *args):
        info = self.info
        if not info.lastException and args == self.args:
            return
        self.args = args
        label = info.instance.GetLabel(*args)
        if label != info.label:
            info.label = label
            self.name = eg.text.General.pluginLabel % label
            if self.id:
                self.tree.SetItemText(
                    self.id, 
                    self.name
                )
        self.RefreshAllVisibleActions()
        if self.isEnabled:
            eg.actionThread.Call(self.StopPlugin)
            eg.actionThread.Call(self.StartPlugin)


    def RefreshAllVisibleActions(self):
        """
        Calls Refresh() for all currently visible actions of this plugin.
        """
        ActionItem = self.document.ActionItem
        plugin = self.info.instance
        def Traverse(item):
            if item.__class__ == ActionItem:
                if item.executable.plugin == plugin:
                    item.Refresh()
            else:
                if item.childs and item.isExpanded:
                    for child in item.childs:
                        Traverse(child)
        Traverse(self.root)
