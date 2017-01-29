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

import __builtin__
import ast
import base64
import compileall
import os
import shutil
import tempfile
import wx
from zipfile import ZIP_DEFLATED, ZipFile
from wx.lib.agw import customtreectrl

# Local imports
import eg
from eg.Icons import PilToBitmap, StreamToPil
from eg.Classes.Dialog import Dialog
from eg.Utils import (
    DecodeMarkdown,
    DecodeReST,
    HasSystemAttribute,
    HasHiddenAttribute
)

TEMPLATE = u"""
<FONT SIZE=5><b>{name}</b></FONT>
<p>
<TABLE CELLSPACING=0 CELLPADDING=0>
    <tr>
        <td><b>Author:</b>&nbsp;</td>
        <td>{author}</td>
    </tr>
    <tr>
        <td><b>Version:</b>&nbsp;</td>
        <td>{version}</td>
    </tr>
</TABLE>
<P>
<b>Description:</b>"""

INFO_FIELDS = [
    "name",
    "author",
    "version",
    "url",
    "guid",
    "description",
    "icon",
]


class Text(eg.TranslatableStrings):
    hiddenSystemTitle = 'Plugin Install - Hidden/System Files'
    hiddenSystemMessage = (
        'There are hidden and system files please select\n'
        'the files you wish to add to the egplugin package.'
    )
    fileType = 'file'
    folderType = 'folder'
    dotHiddenSystem = 'is a no include, hidden, system '
    dotHidden = 'is a no include, hidden '
    dotSystem = 'is a no include, system '
    dot = 'is a no include '
    hiddenSystem = 'is a hidden, system '
    hidden = 'is a hidden '
    system = 'is a system '
    parent = 'parent '
    exportTitle = 'Export EventGhost Plugin'
    exportFileMessage = 'Export plugin %s'
    importTitle = 'Install EventGhost Plugin'
    importMessage = (
        'Do you really want to install plugin %s\n'
        'into EventGhost?\n\n'
    )
    importError = 'Can\'t create directory for plugin'


def GetAttributeFlags(path, name, flags=''):
    path = os.path.join(path, name)
    pathType = [Text.fileType, Text.folderType][os.path.isdir(path)]

    res = ''
    if name.startswith("."):
        res += 'Dot'
    if HasHiddenAttribute(path):
        res += 'Hidden'
    if HasSystemAttribute(path):
        res += 'System'

    if res:
        res = getattr(Text, res[:1].lower() + res[1:])
        res += pathType

    elif flags:
        res = Text.parent + flags

    return res


class PluginInstall(object):

    def CreatePluginPackage(self, sourcePath, targetPath, pluginData):
        fileFolders = dict(flags='', sourcePath=sourcePath)
        for dirpath, dirnames, filenames in os.walk(sourcePath):
            pathList = []
            head, tail = os.path.split(dirpath.replace(sourcePath, ''))
            while tail:
                pathList.insert(0, tail)
                head, tail = os.path.split(head)

            tmpDict = fileFolders
            for folder in pathList:
                if folder not in tmpDict:
                    tmpDict[folder] = dict(flags=tmpDict['flags'])
                tmpDict = tmpDict[folder]

            dirFlags = tmpDict['flags']

            for dirname in dirnames:
                tmpDict[dirname] = dict(
                    flags=GetAttributeFlags(dirpath, dirname, dirFlags)
                )

            for filename in filenames:
                ext = os.path.splitext(filename)[1]
                if (
                    ext.lower() in (".pyc", ".pyo") and
                    filename[:-1] in filenames
                ):
                    continue

                tmpDict[filename] = GetAttributeFlags(
                    dirpath,
                    filename,
                    dirFlags
                )

        def CheckFlags(flagDict):

            if flagDict['flags']:
                return True
            for key in flagDict.keys():
                if isinstance(flagDict[key], dict):
                    return CheckFlags(flagDict[key])
                else:
                    return flagDict[key]

        if CheckFlags(fileFolders):
            dlg = HiddenSystemDialog(fileFolders)
            dlg.ShowModal()

        if fileFolders:
            zipfile = ZipFile(targetPath, "w", ZIP_DEFLATED)
            sourceCode = "\n".join(
                "%s = %r" % (fieldName, pluginData[fieldName])
                for fieldName in INFO_FIELDS
            )
            zipfile.writestr("info.py", sourceCode)
            baseName = os.path.basename(sourcePath)

            def WriteFiles(ff, path):
                for key in ff.keys():
                    if key in ('flags', 'sourcePath', 'st'):
                        continue
                    if isinstance(ff[key], dict) and ff[key]['flags']:
                        WriteFiles(ff[key], os.path.join(path, key))
                    elif isinstance(ff[key], bool) and ff[key]:
                        src = os.path.join(path, key)
                        dst = os.path.join(baseName, src[len(sourcePath) + 1:])
                        zipfile.write(src, dst)

            WriteFiles(fileFolders, sourcePath)
            zipfile.close()

    @eg.LogItWithReturn
    def Export(self, pluginInfo):
        pluginData = self.GetPluginData(pluginInfo)
        #dialog = PluginOverviewDialog(
        #    eg.document.frame,
        #    "Plugin Information",
        #    pluginData=pluginData,
        #    basePath=pluginInfo.path,
        #    message="Do you want to save this plugin as a plugin file?"
        #)
        #result = dialog.ShowModal()
        #dialog.Destroy()
        #if result == wx.ID_CANCEL:
        #    return
        filename = os.path.basename(pluginInfo.path)
        dialog = wx.FileDialog(
            eg.document.frame,
            defaultFile=filename,
            message=Text.exportFileMessage % pluginInfo.name,
            wildcard="EventGhost Plugin (*.egplugin)|*.egplugin",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )
        try:
            result = dialog.ShowModal()
            if result == wx.ID_CANCEL:
                return
            targetPath = dialog.GetPath()
        finally:
            dialog.Destroy()
        self.CreatePluginPackage(pluginInfo.path, targetPath, pluginData)

    def GetPluginData(self, pluginInfo):
        description = pluginInfo.englishDescription
        if description.startswith("<md>"):
            description = DecodeMarkdown(description[4:])
        elif description.startswith("<rst>"):
            description = DecodeReST(description[5:])
        iconData = base64.b64encode(str(pluginInfo.icon.pil.tobytes()))
        return {
            "name": pluginInfo.englishName,
            "author": pluginInfo.author,
            "version": pluginInfo.version,
            "url": pluginInfo.url,
            "guid": pluginInfo.guid,
            "description": description,
            "icon": iconData,
        }

    @eg.LogItWithReturn
    def Import(self, filepath):
        tmpDir = tempfile.mkdtemp()
        try:
            zipfile = ZipFile(filepath, "r", ZIP_DEFLATED)
            zipfile.extractall(tmpDir)
            zipfile.close()
            zipfile = open(os.path.join(tmpDir, "info.py"), "r")
            pluginData = SafeExecParser.Parse(zipfile.read())
            zipfile.close()
            for name in os.listdir(tmpDir):
                path = os.path.join(tmpDir, name)
                if os.path.isdir(path):
                    basePath = path
                    break

            dialog = PluginOverviewDialog(
                title=Text.importTitle,
                pluginData=pluginData,
                basePath=basePath,
                message=Text.importMessage % pluginData['name']
            )
            result = dialog.ShowModal()
            dialog.Destroy()
            if result == wx.ID_CANCEL:
                return
            guid = pluginData['guid']
            if guid in eg.pluginManager.database:
                # a plugin with same GUID already exists
                info = eg.pluginManager.database[guid]
                if info.path.lower().startswith(eg.localPluginDir.lower()):
                    # plugin with same GUID exists in user dir, so delete
                    # the folder first
                    shutil.rmtree(info.path, False)
            dstDir = os.path.join(eg.localPluginDir, os.path.basename(basePath))
            if os.path.exists(dstDir):
                # the wanted name is already used by another plugin
                # so we create a new folder name by adding an number
                for i in range(2, 100):
                    searchDir = dstDir + str(i)
                    if not os.path.exists(searchDir):
                        dstDir = searchDir
                        break
                else:
                    raise Exception(Text.importError)
            shutil.copytree(basePath, dstDir)
            compileall.compile_dir(dstDir, ddir="UserPlugin", quiet=True)
        finally:
            shutil.rmtree(tmpDir, True)
            #from eg.WinApi.Dynamic import ExitProcess
            #ExitProcess(0)

PluginInstall = PluginInstall()


class PluginOverviewDialog(Dialog):
    def __init__(
        self,
        parent=None,
        title=eg.APP_NAME,
        basePath=None,
        pluginData=None,
        message="",
    ):
        Dialog.__init__(
            self,
            None,  #eg.document.frame,
            -1,
            title,
            size=(400, 300),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        self.text = TEMPLATE.format(**pluginData)
        headerCtrl = eg.HtmlWindow(self, style=wx.html.HW_SCROLLBAR_NEVER)
        headerCtrl.SetBorders(2)
        headerCtrl.SetBasePath(basePath)
        headerCtrl.SetPage(self.text)
        self.headerCtrl = headerCtrl
        #height = headerCtrl.GetInternalRepresentation().GetHeight()
        #headerCtrl.SetMinSize((-1, height + 4))
        #headerCtrl.Layout()
        descriptionCtrl = eg.HtmlWindow(self)
        descriptionCtrl.SetBorders(2)
        descriptionCtrl.SetBasePath(basePath)
        descriptionCtrl.SetPage(pluginData['description'])
        questionCtrl = self.StaticText(message)
        self.buttonRow = eg.ButtonRow(
            self, (wx.ID_OK, wx.ID_CANCEL), True, True
        )
        mainSizer = eg.VBoxSizer(
            (headerCtrl, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5),
            (wx.StaticLine(self), 0, wx.EXPAND, 0),
            (descriptionCtrl, 1, wx.EXPAND | wx.ALL, 5),
            (wx.StaticLine(self), 0, wx.EXPAND, 0),
            (questionCtrl, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5),
            (self.buttonRow.sizer, 0, wx.EXPAND),
        )
        self.SetSizer(mainSizer)
        self.SetAutoLayout(True)
        mainSizer.Fit(self)
        mainSizer.Layout()
        self.Layout()
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.SetSize((400, 500))
        self.SetMinSize(self.GetSize())
        self.Center()
#        self.SetSizerAndFit(mainSizer)
#        self.Bind(wx.EVT_SIZE, self.OnSize)
#        self.Layout()

    def OnSize(self, dummyEvent=None):
        self.Layout()
        #self.headerCtrl.SetPage(self.text)
        #print repr(self.text)
        internal = self.headerCtrl.GetInternalRepresentation()
        height = internal.GetHeight()
        #self.headerCtrl.SetSizeHints(self.headerCtrl.GetSize()[0], height)
        self.headerCtrl.SetMinSize((-1, height + 4))
        self.Layout()


class SafeExecParser(object):
    @classmethod
    def Parse(cls, source):
        return cls().Visit(ast.parse(source))

    def Visit(self, node, *args):
        meth = getattr(self, 'Visit' + node.__class__.__name__)
        return meth(node, *args)

    def VisitAssign(self, node, parent):
        value = self.Visit(node.value)
        for target in node.targets:
            parent[self.Visit(target)] = value

    def VisitModule(self, node):
        mod = {}
        for child in node.body:
            self.Visit(child, mod)
        return mod

    def VisitName(self, node):
        if isinstance(node.ctx, ast.Load):
            if node.id in ("True", "False", "None"):
                return getattr(__builtin__, node.id)
        return node.id

    def VisitStr(self, node):
        return node.s


class HiddenSystemDialog(wx.Dialog):

    def __init__(self, fileFolders):

        self.fileFolders = fileFolders
        self.root = None

        wx.Dialog.__init__(
            self,
            None,
            title=Text.hiddenSystemTitle,
            size=(600, 400),
            style=(
                wx.CAPTION |
                wx.CLOSE_BOX |
                wx.SYSTEM_MENU |
                wx.RESIZE_BORDER |
                wx.MAXIMIZE_BOX
            )
        )

        headerBox = eg.HeaderBox(
            self,
            name=Text.hiddenSystemTitle,
            text=Text.hiddenSystemMessage,
            icon=eg.Icons.PLUGIN_ICON
        )

        self.tree = tree = customtreectrl.CustomTreeCtrl(
            self,
            -1,
            size=(-1, 325),
            style=wx.SUNKEN_BORDER,
            agwStyle=(
                customtreectrl.TR_ALIGN_WINDOWS_RIGHT
                | customtreectrl.TR_TWIST_BUTTONS
                | customtreectrl.TR_HAS_BUTTONS
                | customtreectrl.TR_HAS_VARIABLE_ROW_HEIGHT
                | customtreectrl.TR_FULL_ROW_HIGHLIGHT
            )
        )

        buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL))

        tree.EnableSelectionGradient(False)
        tree.SetBackgroundColour(
            wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        )

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(headerBox, 0, wx.EXPAND | wx.BOTTOM, 20)
        sizer.Add(tree, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 10)
        sizer.Add(buttonRow.sizer, 0, wx.EXPAND)

        self.SetSizer(sizer)
        self.Bind(wx.EVT_CLOSE, self.OnCancel)

        self.FillTree()
        tree.Bind(customtreectrl.EVT_TREE_ITEM_CHECKED, self.OnItemCheck)

    def ShowModal(self, *args, **kwargs):
        self.SendSizeEvent()
        wx.Dialog.ShowModal(self, *args, **kwargs)

    def FillTree(self):

        def ReadFileFolders(ff, parent, stWidgets=None):
            for key in sorted(ff.keys()):
                if key in ('flags', 'sourcePath', 'st'):
                    continue
                if isinstance(ff[key], dict):
                    if stWidgets is None:
                        child = self.tree.AppendItem(
                            parent,
                            key,
                            1,
                            ff[key]['st']
                        )

                        self.tree.SetPyData(child, ff[key])

                        ff[key]['flags'] = not bool(ff[key]['flags'])
                        self.tree.CheckItem(child, ff[key]['flags'])

                    else:
                        child = None
                        st = wx.StaticText(self.tree, -1, ff[key]['flags'])
                        stWidgets += (st,)
                        ff[key]['st'] = st

                    stWidgets = ReadFileFolders(ff[key], child, stWidgets)
                else:
                    if stWidgets is None:
                        flag, st = ff[key]
                        ff[key] = not bool(flag)
                        child = self.tree.AppendItem(parent, key, 1, st)
                        self.tree.SetPyData(child, ff[key])
                        self.tree.CheckItem(child, ff[key])
                    else:
                        st = wx.StaticText(self.tree, -1, ff[key])
                        stWidgets += (st,)
                        ff[key] = [ff[key], st]

            return stWidgets

        self.root = root = self.tree.AddRoot(self.fileFolders['sourcePath'])
        self.tree.SetPyData(root, self.fileFolders)

        for widget in ReadFileFolders(self.fileFolders, None, ()):

            def GetSize():
                size = (widget.GetCharWidth() * 34, widget.GetSizeTuple()[1])
                return wx.Size(*size)
            setattr(widget, 'GetSize', GetSize)

        ReadFileFolders(self.fileFolders, root)

        self.tree.Expand(root)
        self.tree.ExpandAllChildren(root)

    def OnItemCheck(self, event):
        self.tree.Unbind(
            customtreectrl.EVT_TREE_ITEM_CHECKED,
            handler=self.OnItemCheck
        )

        treeItem = event.GetItem()

        if treeItem.IsOk():
            def CheckParents(parentItem):
                child, cookie = self.tree.GetFirstChild(parentItem)
                checkParent = 0
                while child and child.IsOk():
                    checkParent = max([
                        checkParent,
                        int(self.tree.IsItemChecked(child))
                    ])
                    child, cookie = self.tree.GetNextChild(parentItem, cookie)

                self.tree.CheckItem(parentItem, bool(checkParent))
                parentData = self.tree.GetPyData(parentItem)
                parentData['flags'] = bool(checkParent)

                parentItem = self.tree.GetItemParent(parentItem)

                if parentItem != self.tree.GetRootItem():
                    CheckParents(parentItem)

            def CheckChildren(parentItem):
                child, cookie = self.tree.GetFirstChild(parentItem)
                while child and child.IsOk():
                    self.tree.CheckItem(child, False)
                    childData = self.tree.GetPyData(child)

                    if isinstance(childData, dict):
                        childData['flags'] = False
                        if self.tree.ItemHasChildren(child):
                            CheckChildren(child)
                    else:
                        parentData = self.tree.GetPyData(parentItem)
                        key = self.tree.GetItemText(child)
                        parentData[key] = False

                    child, cookie = self.tree.GetNextChild(
                        parentItem,
                        cookie
                    )

            itemData = self.tree.GetPyData(treeItem)
            parent = self.tree.GetItemParent(treeItem)
            flag = self.tree.IsItemChecked(treeItem)

            if isinstance(itemData, dict):
                itemData['flags'] = flag
                if not flag and self.tree.ItemHasChildren(treeItem):
                    CheckChildren(treeItem)
            else:
                itemData = self.tree.GetPyData(parent)
                key = self.tree.GetItemText(treeItem)
                itemData[key] = flag

            if parent != self.tree.GetRootItem():
                CheckParents(parent)

            self.tree.Bind(
                customtreectrl.EVT_TREE_ITEM_CHECKED,
                self.OnItemCheck
            )

        event.Skip()

    def OnOK(self, event):
        self.EndModal(wx.ID_OK)
        event.Skip()

    def OnCancel(self, event):
        self.fileFolders.clear()
        self.EndModal(wx.ID_CANCEL)
        event.Skip()
