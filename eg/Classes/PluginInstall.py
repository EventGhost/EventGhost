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

import os
import tempfile
import shutil
import compileall
import base64
import __builtin__
import ast
from zipfile import ZipFile, ZIP_DEFLATED
import wx
import eg
from eg.Utils import DecodeReST
from eg.Classes.Dialog import Dialog


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
    <tr>
        <td><b>Support:</b>&nbsp;</td>
        <td>
            <a href="http://www.eventghost.org/forum/viewforum.php?f=9">
                Forum Thread
            </a>
        </td>
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


class SafeExecParser(object):

    def Visit(self, node, *args):
        meth = getattr(self, 'Visit' + node.__class__.__name__)
        return meth(node, *args)


    def VisitModule(self, node):
        mod = {}
        for child in node.body:
            self.Visit(child, mod)
        return mod


    def VisitAssign(self, node, parent):
        value = self.Visit(node.value)
        for target in node.targets:
            parent[self.Visit(target)] = value


    def VisitName(self, node):
        if isinstance(node.ctx, ast.Load):
            if node.id in ("True", "False", "None"):
                return getattr(__builtin__, node.id)
        return node.id


    def VisitStr(self, node):
        return node.s


    @classmethod
    def Parse(cls, source):
        return cls().Visit(ast.parse(source))



class PluginInstall(object):

    @eg.LogItWithReturn
    def Export(self, mainFrame=None):
        result = eg.AddPluginDialog.GetModalResult(
            mainFrame,
            checkMultiLoad = False,
            title="Please select the plugin to export",
        )
        if not result:
            return
        pluginInfo = result[0]
        pluginData = self.GetPluginData(pluginInfo)
        dialog = PluginOverviewDialog(
            mainFrame,
            "Plugin Information",
            pluginData=pluginData,
            basePath=pluginInfo.path,
            message="Do you want to save this plugin as a plugin file?"
        )
        result = dialog.ShowModal()
        dialog.Destroy()
        if result == wx.ID_CANCEL:
            return
        filename = pluginInfo.englishName.replace("/", "-")
        dialog = wx.FileDialog(
            mainFrame,
            defaultFile=filename,
            wildcard="EventGhost Plugin (*.egplugin)|*.egplugin",
            style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT
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
        pos = description.find("<rst>")
        if pos != -1:
            description = DecodeReST(description[pos+5:])
        iconData = base64.b64encode(pluginInfo.icon.pil.tostring())
        return {
            "name": pluginInfo.englishName,
            "author": pluginInfo.author,
            "version": pluginInfo.version,
            "url": pluginInfo.url,
            "guid": pluginInfo.guid,
            "description": description,
            "icon": iconData,
        }


    def CreatePluginPackage(self, sourcePath, targetPath, pluginData):
        zipfile = ZipFile(targetPath, "w", ZIP_DEFLATED)
        sourceCode = "\n".join(
            "%s = %r" % (fieldName, pluginData[fieldName])
                for fieldName in INFO_FIELDS
        )
        zipfile.writestr("info.py", sourceCode)
        baseName = os.path.basename(sourcePath)
        for dirpath, dirnames, filenames in os.walk(sourcePath):
            for dirname in dirnames[:]:
                if dirname.startswith("."):
                    dirnames.remove(dirname)
            for filename in filenames:
                ext = os.path.splitext(filename)[1]
                if (
                    ext.lower() in (".pyc", ".pyo")
                    and filename[:-1] in filenames
                ):
                    continue
                src = os.path.join(dirpath, filename)
                dst = os.path.join(baseName, src[len(sourcePath)+1:])
                zipfile.write(src, dst)
        zipfile.close()


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
                title="Install EventGhost Plugin",
                pluginData=pluginData,
                basePath=basePath,
                message=(
                    "Do you really want to install this plugin into "
                    "EventGhost?"
                )
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
                    raise Exception("Can't create directory for plugin")
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
            eg.document.frame,
            -1,
            title,
            size=(400, 300),
            style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER
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
            (headerCtrl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5),
            (wx.StaticLine(self), 0, wx.EXPAND, 0),
            (descriptionCtrl, 1, wx.EXPAND|wx.ALL, 5),
            (wx.StaticLine(self), 0, wx.EXPAND, 0),
            (questionCtrl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5),
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
        self.headerCtrl.SetMinSize((-1, height+4))
        self.Layout()

