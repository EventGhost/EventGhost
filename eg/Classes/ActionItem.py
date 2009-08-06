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
import wx

from TreeItem import TreeItem
from TreeItem import HINT_NO_DROP, HINT_MOVE_BEFORE, HINT_MOVE_BEFORE_OR_AFTER
from TreeLink import TreeLink


PATCHES = {
    "Registry.RegistryChange": "System.RegistryChange",
    "Registry.RegistryQuery": "System.RegistryQuery",
}

RENAMED_COLOUR = eg.colour.GetRenamedColor()


class ActionItem(TreeItem):
    xmlTag = "Action"

    icon = eg.Icons.ACTION_ICON
    executable = None
    compiled = None
    args = None
    isExecutable = True
    isConfigurable = True
    openConfigDialog = None
    helpDialog = None
    shouldSelectOnExecute = False


    def GetData(self):
        attr, text = TreeItem.GetData(self)
        action = self.executable
        text = "%s.%s(%s)" % (
            action.plugin.info.evalName,
            action.__class__.__name__,
            ", ".join([repr(arg) for arg in self.args])
        )
        return attr, text


    def __init__(self, parent, node):
        TreeItem.__init__(self, parent, node)
        text = node.text
        if not text:
            # this should never happen
            return
        text = text.strip()
        objStr, remainder = text.split('(', 1)
        objStr = PATCHES.get(objStr, objStr)
        argString, _ = remainder.rsplit(')', 1)
        pluginStr, actionStr = objStr.split(".", 1)
        plugin = getattr(eg.plugins, pluginStr).plugin
        try:
            action = plugin.info.actions[actionStr]
        except KeyError:
            eg.PrintError("Can't find action: " + text)
            action = None
        if action is None or not issubclass(action, eg.ActionBase):
            action = eg.plugins.EventGhost.plugin.info.actions["PythonCommand"]
            argString = repr(text)
        try:
            self.executable = action()
        except:
            eg.PrintTraceback(msg="Error in action: " + repr(text))
            self.executable = eg.plugins.EventGhost.PythonCommand
            argString = repr(text)

        self.icon = action.info.icon
        self.SetArgumentString(argString)


    def GetTypeName(self):
        return "%s: %s" % (
            self.executable.plugin.info.label,
            self.executable.name
        )


    def GetDescription(self):
        return self.executable.description


    def Configure(self, *args):
        return self.executable.Configure(*args)


    def GetArgumentString(self):
        return ", ".join([repr(arg) for arg in self.GetArgs()])


    def SetArgumentString(self, argString):
        try:
            args = eval(
                'returnArgs(%s)' % argString,
                eg.globals.__dict__,
                dict(
                    returnArgs=lambda *x: x,
                    XmlIdLink=lambda id: TreeLink.CreateFromArgument(self, id),
                )
            )
        except:
            eg.PrintTraceback()
            args = ()
        self.SetArgs(args)


    def Delete(self):
        TreeItem.Delete(self)
        for arg in self.GetArgs():
            if isinstance(arg, TreeLink):
                if arg.target:
                    arg.target.dependants.remove(arg)
                arg.owner = None
                arg.target = None
                del arg


    def GetArgs(self):
        return self.args


    def SetArgs(self, args):
        if self.args != args:
            self.args = args
            try:
                self.compiled = self.executable.Compile(*args)
            except:
                eg.PrintTraceback(source=self)
                self.compiled = None
            #self.Refresh()


    def SetAttributes(self, tree, treeId):
        if self.name:
            tree.SetItemTextColour(treeId, RENAMED_COLOUR)
            tree.SetItemFont(treeId, tree.italicfont)
        else:
            tree.SetItemTextColour(treeId, None)
            tree.SetItemFont(treeId, tree.normalfont)


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
        # the item wants to be configured after creation
        imFunc = self.executable.Configure.im_func
        return imFunc != eg.ActionBase.Configure.im_func


    @eg.LogIt
    def ShowHelp(self, parent=None):
        if self.helpDialog:
            self.helpDialog.Raise()
            return
        action = self.executable
        self.helpDialog = eg.HtmlDialog(
            parent,
            action.name,
            action.description,
            action.info.icon.GetWxIcon(),
            action.plugin.info.path
        )
        def OnClose(dummyEvent):
            self.helpDialog.Destroy()
            del self.helpDialog
        self.helpDialog.Bind(wx.EVT_CLOSE, OnClose)
        self.helpDialog.buttonRow.okButton.Bind(wx.EVT_BUTTON, OnClose)
        self.helpDialog.Show()


    def Execute(self):
        if not self.isEnabled:
            return
        if eg.config.logActions:
            self.Print(self.GetLabel())
        if self.shouldSelectOnExecute:
            wx.CallAfter(self.Select)
        eg.currentItem = self
        action = self.executable
        if not action:
            return
        eg.indent += 1
        if not action.plugin.info.isStarted:
            self.PrintError(
                eg.text.Error.pluginNotActivated % action.plugin.name
            )
            return
        try:
            eg.result = self.compiled()
        except eg.Exception, exc:
            #eg.PrintError(e.message)
            self.PrintError(unicode(exc))
        except:
            label = self.GetLabel()
            eg.PrintTraceback(eg.text.Error.InAction % label, 1, source=self)
        finally:
            pass
        eg.indent -= 1


    def DropTest(self, cls):
        if self.parent == self.document.autostartMacro:
            if cls == eg.PluginItem:
                return HINT_MOVE_BEFORE_OR_AFTER
        else:
            if cls == eg.EventItem:
                return HINT_MOVE_BEFORE
        if cls == eg.ActionItem:
            return HINT_MOVE_BEFORE_OR_AFTER
        return HINT_NO_DROP

