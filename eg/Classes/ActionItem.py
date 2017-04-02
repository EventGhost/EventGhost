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

import wx

# Local imports
import eg
from TreeItem import (
    HINT_MOVE_BEFORE, HINT_MOVE_BEFORE_OR_AFTER, HINT_NO_DROP, TreeItem
)
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
    url = None

    @eg.AssertInActionThread
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

    def Configure(self, *args):
        return self.executable.Configure(*args)

    @eg.AssertInActionThread
    def Delete(self):
        TreeItem.Delete(self)
        for arg in self.GetArguments():
            if isinstance(arg, TreeLink):
                if arg.target:
                    arg.target.dependants.remove(arg)
                arg.owner = None
                arg.target = None
                del arg

    def DropTest(self, dropNode):
        if self.parent == self.document.autostartMacro:
            if dropNode.xmlTag == "Plugin":
                return HINT_MOVE_BEFORE_OR_AFTER
        elif dropNode.xmlTag == "Event":
            return HINT_MOVE_BEFORE
        if dropNode.xmlTag == "Action":
            return HINT_MOVE_BEFORE_OR_AFTER
        return HINT_NO_DROP

    @eg.AssertInActionThread
    def Execute(self):
        if not self.isEnabled:
            return
        if eg.config.logActions:
            self.Print(self.GetLabel())
        if self.shouldSelectOnExecute:
            self.Select()
        eg.currentItem = self
        action = self.executable
        if not action:
            return
        eg.indent += 1
        try:
            if not action.plugin.info.isStarted:
                self.PrintError(
                    eg.text.Error.pluginNotActivated % action.plugin.name
                )
                return
            try:
                eg.result = self.compiled()
            except eg.Exception, exc:
                self.PrintError(unicode(exc))
            except:
                label = self.GetLabel()
                eg.PrintTraceback(
                    eg.text.Error.InAction % label, 1, source=self
                )
        finally:
            eg.indent -= 1

    # The Find function calls this from MainThread, so we can't restrict this
    # to the ActionThread
    #@eg.AssertInActionThread
    def GetArguments(self):
        return self.args

    @eg.AssertInActionThread
    def GetArgumentString(self):
        return ", ".join([repr(arg) for arg in self.GetArguments()])

    def GetBasePath(self):
        """
        Returns the filesystem path, where additional files (like pictures)
        should be found.
        """
        return self.executable.plugin.info.path

    def GetData(self):
        attr, text = TreeItem.GetData(self)
        action = self.executable
        text = "%s.%s(%s)" % (
            action.plugin.info.evalName,
            action.__class__.__name__,
            ", ".join([repr(arg) for arg in self.args])
        )
        return attr, text

    def GetDescription(self):
        return self.executable.description

    def GetLabel(self):
        if self.name:
            return self.name

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

    def GetTypeName(self):
        return "%s: %s" % (
            self.executable.plugin.info.label,
            self.executable.name
        )

    def NeedsStartupConfiguration(self):
        """
        Returns True if the item wants to be configured after creation.
        """
        # if the Configure method of the executable is overriden, we assume
        # the item wants to be configured after creation
        return (
            self.executable.Configure.im_func !=
            eg.ActionBase.Configure.im_func
        )

    @eg.AssertInActionThread
    def SetArguments(self, args):
        eg.currentItem = self
        if self.args != args:
            self.args = args
            try:
                self.compiled = self.executable.Compile(*args)
            except:
                eg.PrintTraceback(source=self)
                self.compiled = None

    @eg.AssertInActionThread
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
        self.SetArguments(args)

    def SetAttributes(self, tree, treeId):
        if self.name:
            tree.SetItemTextColour(treeId, RENAMED_COLOUR)
            tree.SetItemFont(treeId, tree.italicfont)
        else:
            tree.SetItemTextColour(treeId, None)
            tree.SetItemFont(treeId, tree.normalfont)

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
            self.GetBasePath()
        )

        def OnClose(dummyEvent):
            self.helpDialog.Destroy()
            del self.helpDialog

        self.helpDialog.Bind(wx.EVT_CLOSE, OnClose)
        self.helpDialog.buttonRow.okButton.Bind(wx.EVT_BUTTON, OnClose)
        self.helpDialog.Show()
