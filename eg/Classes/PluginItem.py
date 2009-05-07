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
import wx
import base64
import pickle

from ActionItem import ActionItem
from TreeItem import TreeItem



class PluginItem(ActionItem):
    xmlTag = "Plugin"
    icon = eg.Icons.PLUGIN_ICON
    isRenameable = False            
    info = None
    
    def GetData(self):
        attr, text = TreeItem.GetData(self)
        del attr[0]
        attr.append(('File', self.pluginFile))
        attr.append(('Identifier', self.executable.info.evalName))
        text = base64.b64encode(pickle.dumps(self.info.args, 2))
        return attr, text
    
    
    def __init__(self, parent, node):
        TreeItem.__init__(self, parent, node)
        if node.text:
            try:
                args = pickle.loads(base64.b64decode(node.text))
            except AttributeError:
                args = ()
        else:
            args = ()
        ident = node.attrib.get('identifier', None)
        pluginStr = node.attrib['file']
        self.pluginFile = pluginStr
        self.info = info = eg.PluginInfo.Open(pluginStr, ident, args, self)
        self.name = eg.text.General.pluginLabel % info.label
        if info.icon != self.icon:
            self.icon = eg.Icons.PluginSubIcon(info.icon)
        #self.icon = info.icon
        self.executable = info.instance


    def GetLabel(self):
        return self.name
        
    
    def GetTypeName(self):
        return self.executable.info.name
    
    
    @eg.LogIt
    def RestoreState(self):
        if self.isEnabled:
            eg.actionThread.Call(self.info.Start)
            
    
    def SetAttributes(self, tree, itemId):
        if self.info.lastException or self.info.initFailed:
            tree.SetItemTextColour(itemId, eg.colour.pluginError)
    
    
    def _SetColour(self, colour):
        if self.HasValidId():
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
        eg.indent += 1
        self.info.Start()
        eg.indent -= 1
        eg.result = self.executable
        return None, None
        
        
    def Enable(self, flag=True):
        ActionItem.Enable(self, flag)
        if flag:
            eg.actionThread.Call(self.info.Start)
        else:
            eg.actionThread.Call(self.info.Stop)


    def _Delete(self):
        info = self.info
        def DoIt():
            info.Close()
            info.instance.OnDelete()
            info.RemovePluginInstance()
        eg.actionThread.Call(DoIt)
        ActionItem._Delete(self)
        self.executable = None
        self.info = None
        
        
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
                wx.NO_DEFAULT|wx.OK|wx.ICON_EXCLAMATION
            )
            return False
        if not TreeItem.AskDelete(self):
            return False
        return True
    
    
    def AskCut(self):
        return self.AskDelete()
    
    
    def NeedsStartupConfiguration(self):
        if self.info.instance.Configure.im_func != eg.PluginBase.Configure.im_func:
            return True
        return False
    
    
    @eg.LogIt
    def ShowHelp(self, parent=None):
        if self.helpDialog:
            self.helpDialog.Raise()
            return
        plugin = self.info.instance
        self.helpDialog = eg.HtmlDialog(
            parent,
            eg.text.General.pluginLabel % plugin.name, 
            plugin.description, 
            plugin.info.icon.GetWxIcon(),
            basePath=plugin.info.GetPath()
        )
        def OnClose(dummyEvent):
            self.helpDialog.Destroy()
            del self.helpDialog
        self.helpDialog.Bind(wx.EVT_CLOSE, OnClose)
        self.helpDialog.okButton.Bind(wx.EVT_BUTTON, OnClose)
        self.helpDialog.Show()
        
                        
    def GetArgs(self):
        return self.info.args
    
    
    @eg.LogIt
    def SetArgs(self, args):
        info = self.info
        if not info.lastException and args == self.info.args:
            return
        self.info.args = args
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
            eg.actionThread.Call(self.info.Stop)
            eg.actionThread.Call(self.info.Start)


    def RefreshAllVisibleActions(self):
        """
        Calls Refresh() for all currently visible actions of this plugin.
        """
        actionItemCls = self.document.ActionItem
        plugin = self.info.instance
        def Traverse(item):
            if item.__class__ == actionItemCls:
                if item.executable.plugin == plugin:
                    item.Refresh()
            else:
                if item.childs and item.isExpanded:
                    for child in item.childs:
                        Traverse(child)
        Traverse(self.root)
