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

import colorsys

import wx

import eg
from TreeItem import TreeItem
from TreeLink import TreeLink


gPatches = {
    "Registry.RegistryChange": "System.RegistryChange",
    "Registry.RegistryQuery": "System.RegistryQuery",
}    

def GetRenamedColor():
    r, g, b = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOWTEXT).Get()
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)        
    if v > 0.5:
        v -= 0.25
    else:
        v += 0.25
    rgb = colorsys.hsv_to_rgb(h, s, v)
    return tuple([int(round(c * 255.0)) for c in rgb])


gRenamedColour = GetRenamedColor()


def _compileCall(action, *args):
    return action.Compile(*args)()
                    

    
class ActionItem(TreeItem):
    xmlTag = "Action"
    
    icon = eg.Icons.ACTION_ICON
    executable = None
    args = ()
    needsCompile = False
    isExecutable = True
    isConfigurable = True
    openConfigDialog = None
    shouldSelectOnExecute = False
    configurationGenerator = None


    def WriteToXML(self):
        attr, text, childs = TreeItem.WriteToXML(self)
        action = self.executable
        text = "%s.%s(%s)" % (
            action.plugin.info.evalName,
            action.__class__.__name__,
            ", ".join([repr(arg) for arg in self.args])
        )
        return attr, text, None


    def __init__(self, parent, node):
        TreeItem.__init__(self, parent, node)
        text = node.text
        self.CmdData = None
        if not text:
            # this should never happen
            return
        text = text.strip()
        obj_str, remainder = text.split('(', 1)
        obj_str = gPatches.get(obj_str, obj_str)                
        argString, _ = remainder.rsplit(')', 1)
        try:
            action = eval(obj_str, eg.plugins.__dict__)
        except:
            eg.PrintError("Can't find action: " + text)
            action = None
        if not isinstance(action, eg.ActionClass):
            action = eg.plugins.EventGhost.PythonCommand
            argString = repr(text)
        self.executable = action
        self.icon = action.info.icon
        if hasattr(action, "Compile"):
            self.needsCompile = True
            action.__call__ = _compileCall
        else:
            self.needsCompile = False
        self.SetArgumentString(argString)
    
    
    def GetArgumentString(self):
        return ", ".join([repr(arg) for arg in self.args])
    
        
    def SetArgumentString(self, argString):
        try:
            args = eval(
                'returnArgs(%s)' % argString,
                eg.globals.__dict__, 
                {
                    'returnArgs': lambda *x: x,
                    'XmlIdLink': lambda id: TreeLink.CreateFromArgument(self, id),
                }
            )
        except:
            eg.PrintTraceback()
            args = ()
        self.SetParams(*args)
            

    def _Delete(self):
        TreeItem._Delete(self)
        for arg in self.args:
            if isinstance(arg, TreeLink):
                if arg.target:
                    arg.target.dependants.remove(arg)
                arg.owner = None
                arg.target = None
                del arg
        
    
    def SetParams(self, *args):
        if self.args != args:
            self.args = args
            if self.needsCompile:
                self.compiledArgs = self.executable.Compile(*args)
            #self.Refresh()
        
        
    def Refresh(self):
        tree = self.tree
        id = self.id
        if id is None:
            return
        self.SetAttributes(tree, id)
        tree.SetItemText(id, self.GetLabel())
            
            
    def SetAttributes(self, tree, id):
        if self.name:
            tree.SetItemTextColour(id, gRenamedColour)
            tree.SetItemFont(id, tree.italicfont)
        else:
            tree.SetItemTextColour(id, None)
            tree.SetItemFont(id, tree.normalfont)
        
        
    def GetLabel(self):
        if self.name:
            name = self.name
        else:
            # often the GetLabel() method of the executable can't handle
            # a call without arguments, because suitable default arguments
            # are missing. So we use a fallback in such cases.
            executable = self.executable
            try:
                name = executable.GetLabel(*self.args)
            except:
                name = executable.name
            pluginInfo = executable.plugin.info
            if pluginInfo.kind != "core":
                name = pluginInfo.label + ": " + name
        return name


    def NeedsStartupConfiguration(self):
        """
        Returns True if the item wants to be configured after creation.
        """
        # if the Configure method of the executable is overriden, we assume
        # the items wants to configured after creation
        im_func = self.executable.Configure.im_func
        return im_func != eg.ActionClass.Configure.im_func
    
    
    def IsConfigurable(self):
        return True
    
    
    def ShowHelp(self):
        action = self.executable
        eg.HTMLDialog(
            action.name, 
            action.description, 
            action.info.icon.GetWxIcon(),
            "plugins/%s/" % action.plugin.__module__
        ).DoModal()
        
    
    def Execute(self):
        if not self.isEnabled:
            return
        if eg.config.logActions:
            self.Print(self.GetLabel())
        if self.shouldSelectOnExecute:
            #self.Select()
            wx.CallAfter(self.Select)
        eg.currentItem = self
        action = self.executable
        if not action:
            return
        if not action.plugin.info.isStarted:
            eg.PrintError(
                eg.text.Error.pluginNotActivated % action.plugin.name
            )
            return
        try:
            if self.needsCompile:
                eg.result = self.compiledArgs()
            else:
                eg.result = action(*self.args)
        except eg.Exception, e:
            eg.PrintError(e.message)
        except:
            wx.CallAfter(self.Select)
            label = self.GetLabel()
            eg.PrintTraceback(eg.text.Error.InAction % label, 1)
        finally:
            pass


    def DropTest(self, cls):
        if cls == eg.EventItem and self.parent != self.document.autostartMacro:
            return 2 # 2 = item would move before
        if cls == eg.ActionItem:
            return 4 # 4 = item can be inserted before or after
        if cls == eg.PluginItem and self.parent == self.document.autostartMacro:
            return 4 # 4 = item can be inserted before or after
        return None


