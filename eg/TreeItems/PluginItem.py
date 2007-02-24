import threading
import base64
import pickle
import copy
import types

from xml.sax.saxutils import quoteattr
import wx

import eg
from ActionItem import ActionItem
from TreeItem import TreeItem



class PluginItem(ActionItem):
    xmlTag = "Plugin"
    iconIndex = eg.SetupIcons("plugin")
    
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
        self.isStarted = False
        self.pluginFile = pluginStr
        self.executable = plugin = eg.OpenPlugin(pluginStr, ident)
        if plugin is None or plugin.info.initFailed:
            eg.PrintError("Error loading plugin: %s" % pluginStr)
            self.name = pluginStr + " not found"
            self.isInErrorState = True
            #plugin.info.label = pluginStr
        else:
            try:
                label = plugin.GetLabel(*self.args)
            except:
                label = plugin.info.name
            plugin.info.label = label
            self.name = eg.text.General.pluginLabel % label
            self.iconIndex = plugin.info.iconIndex
            self.isInErrorState = False


    def GetLabel(self):
        return self.name
        
    
    def RestoreState(self):
        eg.whoami()
        if self.isEnabled:
            eg.actionThread.Call(self.StartPlugin)
            
    
    def SetAttributes(self, tree, id):
        if self.isInErrorState:
            tree.SetItemTextColour(id, (255,0,0))
    
    
    def _SetColour(self, colour):
        if self.id is not None:
            self.tree.SetItemTextColour(self.id, colour)
        
        
    def SetErrorState(self, state):
        if state:
            if not self.isInErrorState:
                wx.CallAfter(self._SetColour, (255,0,0))
                self.isInErrorState = True
        else:
            if self.isInErrorState:
                wx.CallAfter(self._SetColour, (0,0,0))
                self.isInErrorState = False
        
        
    def Refresh(self):
        pass
    
    
    def Execute(self):
        if not self.isEnabled:
            return None, None
        if eg.config.logActions:
            self.DoPrint(self.name)
        if self.shouldSelectOnExecute:
            wx.CallAfter(self.Select)
        self.StartPlugin()
        eg.result = self.executable
        return None, None
        
        
    def StartPlugin(self):
        """
        This is a wrapper for the __start__ member of a eg.PluginClass.
        
        It should only be called from the ActionThread.
        """
        if self.isInErrorState:
            return
        if self.isStarted:
            return
        try:
            self.executable.__start__(*self.args)
            self.executable.info.isStarted = True
        except eg.Exception, e:
            eg.PrintError(eg.text.Error.pluginStartError % self.executable.name)
            eg.PrintError(e.message)
            self.SetErrorState(True)
        except:
            eg.PrintError(eg.text.Error.pluginStartError % self.executable.name)
            eg.PrintTraceback()
            self.SetErrorState(True)
        else:
            self.SetErrorState(False)
        self.isStarted = True
        
        
    def StopPlugin(self):
        """
        This is a wrapper for the __stop__ member of a eg.PluginClass.
        
        It should only be called from the ActionThread.
        """
        if self.isInErrorState:
            return
        if not self.isStarted:
            return
        try:
            self.executable.__stop__()
        except eg.Exception, e:
            eg.PrintError("Error stopping plugin: %s" % self.executable.name)
            eg.PrintError(e.message)
            #self.SetErrorState(True)
        except:
            eg.PrintError("Error stopping plugin: %s" % self.executable.name)
            eg.PrintTraceback()
            self.SetErrorState(True)
        self.isStarted = False
        self.executable.info.isStarted = False
        
        
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
    
    
    def IsEditable(self):
        return False
    
    
    def NeedsConfiguration(self):
        if self.executable.Configure.im_func != eg.PluginClass.Configure.im_func:
            return True
        return False
    
    
    def ShowHelp(self):
        plugin = self.executable
        eg.HTMLDialog(
            eg.text.General.pluginLabel % plugin.name, 
            plugin.description, 
            plugin.info.GetWxIcon(),
            basePath=plugin.info.path
        ).DoModal()
        
                        
    def SetParams(self, *args):
        if args != self.args:
            self.args = args
            label = self.executable.GetLabel(*args)
            if label != self.executable.info.label:
                self.executable.info.label = label
                if self.id:
                    self.tree.SetItemText(self.id, label)
                self.RefreshAllVisibleActions()
            if self.isEnabled:
                eg.actionThread.Call(self.StopPlugin)
                eg.actionThread.Call(self.StartPlugin)


    def RefreshAllVisibleActions(self):
        """
        Calls Refresh() for all currently visible actions of this plugin.
        """
        ActionItem = self.document.ActionItem
        plugin = self.executable
        def Traverse(item):
            if item.__class__ == ActionItem:
                if item.executable.plugin == plugin:
                    item.Refresh()
            else:
                if item.childs and item.isExpanded:
                    for child in item.childs:
                        Traverse(child)
        Traverse(self.root)
