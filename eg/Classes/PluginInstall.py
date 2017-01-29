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
import re
from zipfile import ZIP_DEFLATED, ZipFile
from comtypes import GUID

# Local imports
import eg
from eg.Classes.Dialog import Dialog
from eg.Utils import DecodeMarkdown, DecodeReST

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
    'name',
    'author',
    'version',
    'url',
    'guid',
    'description',
    'icon'
]

Text = eg.text.PluginInstall


def InfoField(attrName, attrValue):
    def Replace(s):
        return s.replace("'", "\\'").replace('\n', '\\n')

    types = (unicode, str)

    line = '%s = ' % attrName
    multiLine = len(line + repr(attrValue)) > 75

    if type(attrValue) in types and multiLine:
        newAttrValue = ()
        while attrValue:
            jump = min([len(repr(attrValue)) + attrValue.count("'"), 72])
            jump -= attrValue[:jump].count("'")

            value = attrValue[:jump]

            if '\n' in value:
                jump = value.find('\n') + 1

            elif len(attrValue[jump:]) > 72:
                if ' ' in value and value[-1:] != '.':
                    jump = value.rfind(' ') + 1

            newAttrValue += (Replace(attrValue[:jump]),)
            attrValue = attrValue[jump:]

        line += '(\n'
        for item in newAttrValue:
            line += "    u'%s'\n" % item
        line += ')\n'

    elif type(attrValue) in types:
        line += "u'%s'\n" % Replace(attrValue)
    else:
        line += '%r\n' % attrValue
    return line


class PluginInstall(object):
    def CreatePluginPackage(self, sourcePath, targetPath, pluginData):

        zipfile = ZipFile(targetPath, "w", ZIP_DEFLATED)
        sourceCode = ''

        if pluginData['icon'] is not None:
            pluginData['icon'] = unicode(pluginData['icon'])

        for fieldName in INFO_FIELDS:
            sourceCode += InfoField(fieldName, pluginData[fieldName])

        zipfile.writestr("info.py", sourceCode)
        baseName = os.path.basename(sourcePath)
        for dirpath, dirnames, filenames in os.walk(sourcePath):
            for dirname in dirnames[:]:
                if dirname.startswith("."):
                    dirnames.remove(dirname)
            for filename in filenames:
                ext = os.path.splitext(filename)[1]
                if (
                    ext.lower() in (".pyc", ".pyo") and
                    filename[:-1] in filenames
                ):
                    continue
                src = os.path.join(dirpath, filename)
                dst = os.path.join(baseName, src[len(sourcePath) + 1:])
                zipfile.write(src, dst)
        zipfile.close()

    @eg.LogItWithReturn
    def Export(self, pluginInfo):
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

        if pluginInfo.guid == pluginInfo.englishName:
            guid = unicode(GUID.create_new()).upper()
            dialog = wx.TextEntryDialog(
                None,
                message=Text.guidMessage,
                caption=Text.guidTitle,
                defaultValue='guid = ' + repr(guid),
                style=(
                    wx.OK |
                    wx.ICON_ERROR |
                    wx.STAY_ON_TOP
                )
            )
            textCtrl = list(
                item for item in dialog.Children
                if isinstance(item, wx.TextCtrl)
            )[0]
            textCtrl.SetEditable(False)
            dialog.ShowModal()
            dialog.Destroy()
            return
        pluginData = self.GetPluginData(pluginInfo)

        fileName = (
            '%s-%s.egplugin' % (pluginInfo.englishName, pluginInfo.version)
        )
        filePath = os.path.basename(pluginInfo.path)
        title = eg.text.MainFrame.Menu.Export.replace("&", "").replace(".", "")
        dialog = wx.FileDialog(
            eg.document.frame,
            defaultFile=os.path.join(filePath, fileName),
            message=title,
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

    def BackupPlugin(self, pluginInfo):
        backupName = (
            '%s-%s.egplugin' % (pluginInfo.englishName, pluginInfo.version)
        )

        backupPath = os.path.join(
            eg.folderPath.ProgramData,
            'EventGhost',
            'PluginBackups'
        )
        if not os.path.exists(backupPath):
            os.makedirs(backupPath)

        eg.Print('Creating backup of plugin.')
        eg.Print('Writing ' + os.path.join(backupPath, backupName))

        self.CreatePluginPackage(
            pluginInfo.path,
            os.path.join(backupPath, backupName),
            self.GetPluginData(pluginInfo)
        )

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

            guid = pluginData['guid']
            if guid in eg.pluginManager.database:
                # a plugin with same GUID already exists
                info = eg.pluginManager.database[guid]
                name = info.englishName
                mData = (name, pluginData['name'])
                if info.englishName != pluginData['name']:
                    title = Text.replaceTitle % info.englishName
                    message = Text.replaceMessage % mData

                elif info.version != pluginData['version']:
                    mData = (name, info.version, pluginData['version'])
                    if info.version < pluginData['version']:
                        title = Text.upgradeTitle % name
                        message = Text.upgradeMessage % mData
                    else:
                        title = Text.downgradeTitle % name
                        message = Text.downgradeMessage % messageData
                else:
                    title = Text.overwriteTitle % name
                    message = Text.overwriteMessage % mData

                dialog = PluginOverviewDialog(
                    title=title,
                    message=message,
                    pluginData=pluginData,
                    basePath=basePath,
                )

                result = dialog.ShowModal()
                dialog.Destroy()
                if result == wx.ID_CANCEL:
                    return

                self.BackupPlugin(info)
                try:
                    shutil.rmtree(info.path, False)
                except WindowsError:
                    if info.path.startswith(eg.corePluginDir):
                        eg.PrintNotice(Text.pluginRemoveError + info.path)
                    else:
                        raise
            else:
                dialog = PluginOverviewDialog(
                    title= Text.installTitle % pluginData['name'],
                    pluginData=pluginData,
                    basePath=basePath,
                    message=Text.installMessage
                )

                result = dialog.ShowModal()
                dialog.Destroy()
                if result == wx.ID_CANCEL:
                    return

            dstDir = os.path.join(
                eg.localPluginDir,
                os.path.basename(basePath)
            )

            if os.path.exists(dstDir):
                dstDir += '-' + pluginData['version']
                if os.path.exists(dstDir):
                    for i in range(1, 200):
                        searchDir = dstDir + '-' + str(i)
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
        message=""
    ):
        Dialog.__init__(
            self,
            None,  #eg.document.frame,
            -1,
            title,
            size=(400, 300),
            style=(
                wx.DEFAULT_DIALOG_STYLE |
                wx.RESIZE_BORDER |
                wx.STAY_ON_TOP
            )
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
