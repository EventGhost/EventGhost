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
import win32api
import win32con
from zipfile import ZIP_DEFLATED, ZipFile
from wx.lib.agw import customtreectrl

# Local imports
import eg
from eg.Icons import PilToBitmap, StreamToPil
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

UNCHECKED = (
    '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D\x49\x48\x44\x52\x00\x00'
    '\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1F\xF3\xFF\x61\x00\x00\x01'
    '\x6C\x49\x44\x41\x54\x78\x9C\xA5\x92\x31\x8E\x02\x31\x0C\x45\x7F\xE2\x90'
    '\x21\x1A\x8D\x44\x47\x47\x47\xC1\xA9\xB8\x05\x17\xE0\x04\x70\x03\x4E\x41'
    '\x4B\x89\x38\x00\x07\x40\x42\x34\x14\x20\x21\x14\x0F\x93\x78\xAB\x64\x18'
    '\x46\xCB\x16\x6B\xC9\x45\x9C\xF8\xE5\x7F\x27\x4A\x44\xF0\x9F\x30\x00\xB0'
    '\x58\x2C\xE4\x7E\xBF\xC3\x39\x07\x63\x0C\x00\xE0\x13\x1C\x42\xC0\xF3\xF9'
    '\xC4\x78\x3C\xC6\x72\xB9\x54\x79\x43\x44\xB0\xDD\x6E\x85\x99\xA5\x69\x9A'
    '\xAF\xC9\xCC\xB2\xDB\xED\x64\xB5\x5A\x89\x88\x40\x44\xA0\xD7\xEB\xB5\x4C'
    '\xA7\x53\xD4\x75\x0D\xEF\x3D\x98\x19\xCC\x0C\xEF\x7D\x2F\xEB\xBA\xC6\x64'
    '\x32\x81\xF7\xBE\xB5\x70\xBB\xDD\x40\x44\x68\x9A\xE6\xAB\xD7\x64\x49\x29'
    '\x05\xE7\x5C\x0B\x18\x8D\x46\x88\x31\x22\x84\x90\x0F\x7C\x36\x6A\xAD\x91'
    '\x24\x03\x40\x8C\xB1\x05\x54\x55\xD5\x03\x28\xA5\x3A\x43\x4C\x0D\x31\x46'
    '\x30\x33\xCA\xB2\x6C\x01\x5A\x6B\x78\xEF\x3B\x12\xDF\x1B\xB5\xD6\x88\x31'
    '\xE6\x3A\x33\xA3\x28\x8A\x16\x50\x96\x25\x8A\xA2\xC0\x60\x30\xE8\x01\x94'
    '\x52\x1D\xB9\x4A\x29\x84\x10\xF2\x53\x03\x80\x71\xCE\xC1\x39\x07\x22\x82'
    '\x88\x64\x0B\x29\x92\x82\x77\x40\x47\x81\x31\x06\xD6\x5A\x18\x63\x40\x44'
    '\x79\x23\xCD\xC4\x18\x83\xD7\xEB\x05\x22\x42\x8C\x11\xCE\xB9\x2E\x80\x88'
    '\x60\xAD\xC5\x70\x38\xCC\x13\xFF\x94\x6D\xAD\xCD\x6B\x22\xEA\x02\x2E\x97'
    '\x4B\x8F\xFA\x5B\xA4\x0B\xAE\xD7\x6B\x6B\xF1\x74\x3A\xE1\x70\x38\xFC\xD9'
    '\x9C\xD4\xEC\xF7\x7B\x9C\xCF\xE7\xB6\x26\x22\x98\xCF\xE7\x72\x3C\x1E\xF1'
    '\x78\x3C\x3A\x03\x7B\xFF\x0B\x5A\x6B\x54\x55\x85\xD9\x6C\x86\xCD\x66\xA3'
    '\x3A\x80\xFF\xC4\x0F\x62\x0E\xF4\x43\x56\x07\xA1\x3A\x00\x00\x00\x00\x49'
    '\x45\x4E\x44\xAE\x42\x60\x82'
)

CHECKED = (
    '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D\x49\x48\x44\x52\x00\x00'
    '\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1F\xF3\xFF\x61\x00\x00\x02'
    '\x8F\x49\x44\x41\x54\x78\x9C\x95\x93\xDB\x4B\xD4\x41\x18\x86\x9F\x99\x3D'
    '\xE9\xFE\xFC\x1D\x5C\x5D\x89\x88\x4A\x33\x42\xD0\xA2\x14\x93\x20\x88\x20'
    '\x23\x82\x0A\xAC\x94\x28\x84\xA0\x02\x05\x29\x02\x61\xC3\x8C\xA0\x9B\x22'
    '\x44\xAA\xAB\x2E\x14\xBB\x30\xFA\x03\xCA\xC8\x42\x8A\xEA\x42\x84\x4E\x22'
    '\x41\x60\x89\x16\x16\x44\xB9\xAE\xB1\xC7\xF9\xBA\x58\x4F\x5D\x36\x30\xF0'
    '\x32\xDF\xCC\xC3\x3B\xDF\xBC\x83\x88\xF0\x3F\xB3\xA2\xA2\x42\x00\xE9\xED'
    '\xED\x15\x11\xE1\xBF\x0E\xC7\x62\x31\x01\xA4\xAE\xAE\x4E\x96\xD6\x94\x88'
    '\xB0\xF7\xC0\x45\x19\x79\xF5\x03\x74\x18\xF0\x03\x06\x50\xE4\x87\x02\x04'
    '\xCC\x6F\x98\xBF\x8F\x52\x0A\x63\xCC\x52\x11\x75\xBA\xAD\x5F\xCA\xCA\xB7'
    '\x73\xE8\xE0\x7A\x1C\x2B\x08\xF9\xED\x20\x82\x52\x0A\x41\x40\xA0\xE3\x4C'
    '\x0B\x23\xC3\x0F\xD9\xB1\xAB\x99\x22\x77\x07\xCF\x1F\x75\x2A\x00\x7F\xDF'
    '\x90\xE1\xFC\x35\x8B\x8F\x3F\x53\x84\xE2\x19\x44\xC0\xA7\x15\x39\x63\x30'
    '\x92\x77\xF0\xE6\xE5\x63\x46\x86\x1F\xE2\x44\xA2\xEC\x6B\xEF\xE2\x7A\xF7'
    '\xD8\x92\x01\xFC\x54\x46\xF1\xAC\x20\x89\x64\x8E\x44\x4A\x10\x31\x68\xA5'
    '\x51\x8B\x26\xD3\xC9\x24\xF7\x7A\xBA\x00\x38\x7C\xB6\x0B\xCF\x75\xA1\xA2'
    '\x64\x19\xA0\xB1\x0B\x58\xC8\x08\xA3\xCF\x87\xB8\xDC\x52\x4B\xAC\xA9\x86'
    '\xEF\xB3\x33\x2C\x64\x20\x6D\x14\x8F\x06\x6F\xF3\x73\x76\x9A\xF2\xEA\x7A'
    '\x6A\xF6\x1C\x23\x65\x14\x14\x15\xFC\x0B\xF8\x95\x54\x94\xD7\x36\xE2\x94'
    '\xAE\xE5\x4F\xFC\x17\x83\x37\x2E\x60\x50\xCC\x4C\x7D\xE6\xE9\x83\x3B\xE0'
    '\x0F\x70\xA4\xE3\x26\x89\x14\xCC\xCC\x19\xB0\x42\xAB\xAE\x50\x18\x64\x72'
    '\x0E\x66\x13\x8A\x2D\x27\x7B\x98\xBE\xBA\x9F\xC9\xF7\xAF\x18\xEC\xBF\xCB'
    '\xF7\xF1\x67\x90\xCD\xB0\xB9\xF1\x1C\x93\x94\x93\xFD\x9A\x65\x3E\x25\x60'
    '\xAF\x02\x38\x56\x08\xB7\xC8\xC2\x0A\xF9\x50\xC5\x5B\xA9\x3F\x71\x85\xD1'
    '\x81\x18\x1F\x1E\x5C\x03\x32\x84\x23\x6B\xA9\x6D\xB9\x44\xA0\x20\x8C\x52'
    '\x9A\x40\x32\x87\x63\x15\xAE\x00\x22\xB6\x85\xEB\x7A\xD8\x21\x8D\xD6\xC2'
    '\xCE\xE6\x4E\xBE\xBD\x7B\xC2\xCC\xDB\x11\x00\xF6\xB4\xDD\x62\xCD\xBA\xF5'
    '\xE4\x72\x02\xA2\x50\xC1\x14\xA5\x4E\x78\xA5\x07\x25\x76\x21\x11\xD7\x47'
    '\xC4\x51\x44\x5C\x4D\xB4\x58\x73\xB4\xBB\x8F\x90\xE5\xB0\xA9\xBE\x91\x86'
    '\x83\x4D\x78\x61\x88\xBA\x0A\xCF\x86\xD2\x92\x10\xC5\xB6\xBD\xE2\x20\x54'
    '\x60\xE1\xDA\xE0\x58\xF9\x0C\xEA\x00\x38\xDE\x46\x8E\x77\xDF\x61\xC3\xB6'
    '\x06\x4A\x4A\x21\x9B\xCB\xA7\x4B\x2B\x98\x4F\x43\x38\xBC\x1A\xF0\xE7\x2B'
    '\x65\x65\xC5\x78\x1E\x04\x35\xE4\x04\x7C\x0A\xD6\xB5\x9F\x42\x04\xB2\x69'
    '\xF0\x05\xC8\xEB\x0C\xF8\xD2\xA0\xE3\x93\x40\x75\x1E\xE0\xC5\xC7\x98\xFA'
    '\x12\xA7\x72\xF7\xAE\xBC\x83\xC5\xF4\x9B\x45\x9D\xB5\x96\x9E\x0B\xD2\xC0'
    '\xF8\x8B\xD7\x44\x13\x9F\x96\x01\x4A\x44\x68\x6D\x6D\x95\x89\x89\x09\x12'
    '\x89\x04\xC6\x18\x44\x04\xAD\xF5\xB2\x06\xF0\xFB\xFD\xD8\xB6\x4D\x55\x55'
    '\x15\x03\x03\x03\xCB\x9F\xE9\x2F\xE2\x50\x37\xAF\x54\xCD\x47\x97\x00\x00'
    '\x00\x00\x49\x45\x4E\x44\xAE\x42\x60\x82'
)


def IsSystem(filePath):
    fileAttributes = win32api.GetFileAttributes(filePath)
    return fileAttributes | win32con.FILE_ATTRIBUTE_SYSTEM == fileAttributes


def IsHidden(filePath):
    fileAttributes = win32api.GetFileAttributes(filePath)
    return fileAttributes | win32con.FILE_ATTRIBUTE_HIDDEN == fileAttributes


def GetAttributeFlags(path, name):
    path = os.path.join(path, name)
    res = []
    if name.startswith("."):
        res.append('.')
    if IsHidden(path):
        res.append('HIDDEN')
    if IsSystem(path):
        res.append('SYSTEM')
    return res


class PluginInstall(object):

    def CreatePluginPackage(self, sourcePath, targetPath, pluginData):
        fileFolders = dict(flags=[], sourcePath=sourcePath)
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
                tmpDict[dirname] = dict(flags=dirFlags[:])

                flags = GetAttributeFlags(dirpath, dirname)
                for flag in flags:
                    if flag not in dirFlags:
                        tmpDict[dirname]['flags'].append(flag)

            for filename in filenames:
                ext = os.path.splitext(filename)[1]
                if (
                    ext.lower() in (".pyc", ".pyo") and
                    filename[:-1] in filenames
                ):
                    continue

                tmpDict[filename] = dirFlags[:]
                flags = GetAttributeFlags(dirpath, filename)
                for flag in flags:
                    if flag not in dirFlags:
                        tmpDict[filename].append(flag)

        def CheckFlags(flagDict):
            if flagDict['flags']:
                return True
            for key in flagDict.keys():
                if isinstance(flagDict[key], list) and flagDict[key]:
                    return True
                elif isinstance(flagDict[key], dict):
                    return CheckFlags(flagDict[key])

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
                    if key in ('flags', 'sourcePath'):
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
        title = eg.text.MainFrame.Menu.Export.replace("&", "").replace(".", "")
        dialog = wx.FileDialog(
            eg.document.frame,
            defaultFile=filename,
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
            title='Plugin Install - Hidden/System Files',
            size=(450, 525),
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
            name='Plugin Install',
            text=(
                'There are hidden and system files please select\n'
                'the files you wish to add to the egplugin package.'
            ),
            icon=eg.Icons.PLUGIN_ICON
        )

        self.tree = tree = customtreectrl.CustomTreeCtrl(
            self,
            -1,
            size=(-1, 325),
            style=wx.SUNKEN_BORDER,
            agwStyle=(
                customtreectrl.TR_AUTO_TOGGLE_CHILD |
                customtreectrl.TR_AUTO_CHECK_PARENT |
                customtreectrl.TR_TWIST_BUTTONS |
                customtreectrl.TR_HAS_BUTTONS |
                customtreectrl.TR_HAS_VARIABLE_ROW_HEIGHT |
                customtreectrl.TR_FULL_ROW_HIGHLIGHT
            )
        )

        buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL))

        tree.EnableSelectionGradient(True)
        tree.SetGradientStyle(False)
        tree.SetFirstGradientColour(wx.Colour(0, 0, 0))
        tree.SetSecondGradientColour(wx.Colour(0, 255, 0))
        tree.SetBackgroundColour(
            wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        )

        imageList = wx.ImageList(16, 16)
        imageList.Add(PilToBitmap(StreamToPil(CHECKED)))
        imageList.Add(PilToBitmap(StreamToPil(UNCHECKED)))
        tree.SetImageListCheck(16, 16, imageList)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(headerBox, 0, wx.EXPAND | wx.BOTTOM, 20)
        sizer.Add(tree, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 10)
        sizer.Add(buttonRow.sizer, 0, wx.EXPAND)

        self.SetSizer(sizer)
        self.Bind(wx.EVT_CLOSE, self.OnCancel)

        self.FillTree()
        tree.Bind(customtreectrl.EVT_TREE_ITEM_CHECKED, self.OnItemCheck)

    def ShowModal(self, *args, **kwargs):
        self.SendSizeEvent()
        wx.Dialog.ShowModal(self, *args, **kwargs)

    def FillTree(self):

        def ReadFileFolders(ff, parent):
            for key in sorted(ff.keys()):
                if key in ('flags', 'sourcePath'):
                    continue
                if isinstance(ff[key], dict):
                    child = self.tree.AppendItem(
                        parent,
                        key,
                        1,
                        wx.StaticText(self.tree, -1, str(ff[key]['flags']))
                    )

                    self.tree.SetPyData(child, ff[key])
                    ff[key]['flags'] = not bool(ff[key]['flags'])
                    self.tree.CheckItem(child, ff[key]['flags'])

                    ReadFileFolders(ff[key], child)
                else:
                    child = self.tree.AppendItem(
                        parent,
                        key,
                        1,
                        wx.StaticText(self.tree, -1, str(ff[key]))
                    )

                    ff[key] = not bool(ff[key])
                    self.tree.SetPyData(child, ff[key])
                    self.tree.CheckItem(child, ff[key])

        self.root = root = self.tree.AddRoot(self.fileFolders['sourcePath'])
        self.tree.SetPyData(root, self.fileFolders)
        ReadFileFolders(self.fileFolders, root)
        self.tree.Expand(root)

    def OnItemCheck(self, event):
        treeItem = event.GetItem()

        if treeItem.IsOk():
            fileFolders = self.tree.GetPyData(treeItem)
            parent = self.tree.GetItemParent(treeItem)
            flag = self.tree.IsItemChecked(treeItem)

            if isinstance(fileFolders, dict):
                fileFolders['flags'] = flag

                if (
                    not flag and
                    self.tree.ItemHasChildren(treeItem)
                ):
                    child, cookie = self.tree.GetFirstChild(treeItem)
                    while child.IsOk():
                        self.tree.CheckItem(child, False)
                        child, cookie = self.tree.GetNextChild(treeItem, cookie)

            else:
                fileFolders = self.tree.GetPyData(parent)
                key = self.tree.GetItemText(treeItem)
                fileFolders[key] = flag
                if not self.tree.IsItemChecked(parent) and flag:
                    self.tree.CheckItem(parent, True)

        event.Skip()

    def OnOK(self, event):
        self.EndModal(wx.ID_OK)
        event.Skip()

    def OnCancel(self, event):
        self.fileFolders.clear()
        self.EndModal(wx.ID_CANCEL)
        event.Skip()
