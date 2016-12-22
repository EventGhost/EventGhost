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
    "name",
    "author",
    "version",
    "url",
    "guid",
    "description",
    "icon",
]


class PluginInstall(object):
    def AddGUID(self, pluginInfo):
        from comtypes import GUID
        self.BackupPlugin(pluginInfo)

        initFile = os.path.join(pluginInfo.path, '__init__.py')
        initFile = open(initFile, 'r+')

        lines = initFile.readlines()
        initFile.seek(0)

        startPos = None
        stopPos = None
        modifiedRegister = []
        bracketCount = 0
        for i, line in enumerate(lines):
            if line.strip() == 'eg.RegisterPlugin(':
                startPos = i
                modifiedRegister.append(line)
                bracketCount = 1
                continue
            elif line.startswith('eg.RegisterPlugin('):
                modifiedRegister.append(line)
                startPos = i
                bracketCount = 1
                for char in line[18:]:
                    if char == '(':
                        bracketCount += 1
                    elif char == ')':
                        bracketCount -= 1
                if bracketCount:
                    for j, nextLine in enumerate(lines[i + 1:]):
                        modifiedRegister.append(nextLine)
                        for char2 in nextLine:
                            if char2 == '(':
                                bracketCount += 1
                            if char2 == ')':
                                bracketCount -= 1
                        if not bracketCount:
                            stopPos = j
                            break
                    break
                else:
                    stopPos = i
                    break
            if startPos is not None:
                modifiedRegister.append(line)
                if line.strip().lower.startswith('guid'):
                    continue
                for char in line:
                    if char == '(':
                        bracketCount += 1
                    elif char == ')':
                        bracketCount -= 1

                if not bracketCount:
                    stopPos = i
                    break
        if stopPos is None:
            return None

        print modifiedRegister

        spaces = 0
        tabs = 0
        for i, char in enumerate(modifiedRegister[0]):
            if char == ' ':
                spaces += 1
            elif char == '\t':
                tabs += 1
            else:
                break

        guid = unicode(GUID.create_new()).upper()

        modifiedRegister = list(line.strip() for line in modifiedRegister)
        modifiedRegister = ''.join(modifiedRegister)
        modifiedRegister = modifiedRegister.split(',')
        firstLine = modifiedRegister[0].split('(')
        if len(modifiedRegister) == 1:
            lastLine = firstLine[1][:-1]
            modifiedRegister = [
                firstLine[0] + '(',
                lastLine,
                'guid=%r' % guid,
                ')'
            ]
        else:
            lastLine = modifiedRegister[-1]
            modifiedRegister[0] = firstLine[0] + '('
            modifiedRegister.insert(1, firstLine[1])
            modifiedRegister[len(modifiedRegister) - 1] = lastLine[:-1]
            modifiedRegister.append('guid=%r' % guid)
            modifiedRegister.append(')')

        regLen = len(modifiedRegister)

        print modifiedRegister

        for i, line in enumerate(modifiedRegister):
            if spaces:
                indent = ' ' * spaces
            elif tabs:
                indent = '\t' * tabs
            else:
                indent = ''
            if not i or i >= regLen - 2:
                formatter = '%s%s\n'
            else:
                formatter = '%s%s,\n'

            if i and i + 1 != regLen:
                if tabs:
                    indent += '\t'
                else:
                    indent += ' ' * 4

            keywordList = (
                'name',
                'description',
                'kind',
                'author',
                'version',
                'icon',
                'canMultiLoad',
                'createMacrosOnAdd',
                'url',
                'help',
                'hardwareId'
            )

            for kName in keywordList:
                if line.startswith(kName):
                    line = line.replace(kName, '')
                    if line.startswith(' ='):
                        line = line[2:].strip()
                    if line.startswith('='):
                        line = line[1:].strip()

                    if line.startswith("('") or line.startswith('("'):
                        quote = line[:2][1]
                        line = line[1:]
                        if tabs:
                            dent = indent + '\t'
                        else:
                            dent = indent + ' ' * 4
                        line = line.replace(
                            quote + quote,
                            '%s\n%s%s' % (quote, dent, quote)
                        )
                        if line.endswith(quote + ')'):
                            line = line[:-2] + quote + '\n' + indent + ')'

                        line = '(\n' + dent + line
                    line = kName + '=' + line
                    break

            line = formatter % (indent, line)
            modifiedRegister[i] = line

        print modifiedRegister

        for i in range(startPos, stopPos + 1):
            lines.pop(startPos)

        for i, line in enumerate(modifiedRegister):
            lines.insert(startPos + i, line)

        initFile.writelines(lines)
        initFile.close()

        eg.pluginManager.ScanAllPlugins()

        return eg.pluginManager.database[guid]

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
            dialog = wx.MessageDialog(
                None,
                message=(
                    'Plugin %s does not have a GUID,\n'
                    'this is required for plugins.\n\n'
                    'Would you like to add one?' %
                    pluginInfo.englishName
                ),
                caption='Plugin Export - Missing GUID',
                style=(
                    wx.YES_NO |
                    wx.YES_DEFAULT |
                    wx.ICON_EXCLAMATION |
                    wx.STAY_ON_TOP
                )
            )

            result = dialog.ShowModal()
            dialog.Destroy()
            if result == wx.ID_NO:
                return
            pluginInfo = self.AddGUID(pluginInfo)

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

        eg.PrintNotice('Creating backup of plugin.')
        eg.PrintNotice('Writing ' + os.path.join(backupPath, backupName))

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

                if info.englishName != pluginData['name']:
                    title = 'Replace EventGhost Plugin %s' % info.englishName
                    message = (
                        'The new plugin has the same identifier as\n'
                        'an existing plugin.\n'
                        'Would you like to replace plugin\n'
                        '%s with plugin %s?' %
                        (info.englishName, pluginData['name'])
                    )
                elif info.version != pluginData['version']:
                    if info.version < pluginData['version']:
                        title = (
                            'Upgrade EventGhost Plugin %s' % info.englishName
                        )
                        message = (
                            'Would you like to upgrade plugin %s\n'
                            'version %s to version %s?' %
                            (
                                info.englishName,
                                info.version,
                                pluginData['version']
                            )
                        )
                    else:
                        title = (
                            'Downgrade EventGhost Plugin %s' % info.englishName
                        )
                        message = (
                            'Would you like to downgrade plugin %s\n'
                            'version %s to version %s?' %
                            (
                                info.englishName,
                                info.version,
                                pluginData['version']
                            )
                        )
                else:
                    title = 'Overwrite EventGhost Plugin %s' % info.englishName
                    message = (
                        'Plugin %s is already installed.\n'
                        'Would you like to overwrite plugin %s?\n' %
                        (info.englishName, pluginData['name'])
                    )

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
                        eg.PrintNotice(
                            'The old plugin will have to removed manually.\n' +
                            info.path
                        )
                    else:
                        raise
            else:
                dialog = PluginOverviewDialog(
                    title="Install EventGhost Plugin %s" % pluginData['name'],
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
        message="",
        upgrade=False
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
