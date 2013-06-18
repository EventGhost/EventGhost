import types
import inspect
from xml.sax.saxutils import quoteattr

import wx
import eg

from TreeItem import TreeItem
from TreeLink import TreeLink


gPatches = {
    "Registry.RegistryChange": "System.RegistryChange",
    "Registry.RegistryQuery": "System.RegistryQuery",
}    


def _compileCall(action, *args):
    return action.Compile(*args)()
                    

    
class ActionItem(TreeItem):
    xmlTag = "Action"
    
    iconIndex = eg.SetupIcons("action")
    executable = None
    args = ()
    needsCompile = False
    canExecute = True
    openConfigDialog = None


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
        self.iconIndex = action.info.iconIndex
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
        if self.name:
            tree.SetItemFont(id, tree.italicfont)
            tree.SetItemTextColour(id, (64,64,64))
        else:
            tree.SetItemFont(id, tree.normalfont)
            tree.SetItemTextColour(id, None)
        tree.SetItemText(id, self.GetLabel())
            
            
    def SetAttributes(self, tree, id):
        if self.name:
            tree.SetItemTextColour(id, (64,64,64))
            tree.SetItemFont(id, tree.italicfont)
        else:
            tree.SetItemTextColour(id, None)
            tree.SetItemFont(id, tree.normalfont)
        
        
    def GetLabel(self):
        executable = self.executable
        if self.name:
            name = self.name
        else:
            # often the GetLabel() method of the executable can't handle
            # a call without arguments, because suitable default arguments
            # are missing. So we use a fallback in such cases.
            try:
                name = executable.GetLabel(*self.args)
            except:
                name = executable.plugin.info.label + ": " + executable.name
        return name


    def NeedsConfiguration(self):
        im_func = self.executable.Configure.im_func
        if im_func != eg.ActionClass.Configure.im_func:
            return True
        return False
    
    
    def IsConfigurable(self):
        return True
    
    
    def Configure(self):
        return self.ConfigureHandler().Do(self)
    
    
    def DoConfigure(self):
        eg.whoami()
        executable = self.executable
        if executable is None:
            return None
        eg.SetAttr("currentConfigureItem", self)
        
        if executable.Configure.func_code.co_flags & 0x20:
            gen = executable.Configure(*self.args)
            dialog = gen.next()
            res = dialog.AffirmedShowModal()
            if res:
                result = gen.next()
            else:
                result = None
        else:
            result = executable.Configure(*self.args)
        if self.openConfigDialog is not None:
            self.openConfigDialog.Destroy()
            self.openConfigDialog = None
        if result is None:
            return False
        self.SetParams(*result)
        self.Refresh()
        return True
        
            
    class ConfigureHandler:
        
        def Do(self, item):
            self.name = eg.text.MainFrame.Menu.Edit.replace("&", "")
            self.oldArgs = item.GetArgumentString()
            if item.DoConfigure() is False:
                return
            newArgs = item.GetArgumentString()
            if self.oldArgs != newArgs:
                self.positioner = item.GetPositioner()
                item.document.AppendUndoHandler(self)
        
        
        def Undo(self, document):
            parent, pos = self.positioner()
            item = parent.childs[pos]
            args = item.GetArgumentString()
            TreeLink.StartUndo()
            item.SetArgumentString(self.oldArgs)
            TreeLink.StopUndo()
            self.oldArgs = args
            item.Refresh()
            item.Select()

        Redo = Undo
        

    def ShowHelp(self):
        action = self.executable
        eg.HTMLDialog(
            action.name, 
            action.description, 
            action.info.GetWxIcon(),
            "plugins/%s/" % action.plugin.__module__
        ).DoModal()
        
    
    def Execute(self):
        if not self.isEnabled:
            return
        if eg.config.logActions:
            self.DoPrint(self.GetLabel())
        if self.shouldSelectOnExecute:
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
            label = self.executable.GetLabel(*self.args)
            eg.PrintTraceback(eg.text.Error.InAction % label, 1)


    def DropTest(self, cls):
        if cls == EventItem and self.parent != self.document.autostartMacro:
            return 2 # 2 = item would move before
        if cls == ActionItem:
            return 4 # 4 = item can be inserted before or after
        if cls == PluginItem and self.parent == self.document.autostartMacro:
            return 4 # 4 = item can be inserted before or after
        return None

