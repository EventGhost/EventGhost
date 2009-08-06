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
import pickle
import tempfile
import shutil
import compileall
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

class PluginInstall(object):

    def Export(self, mainFrame=None):
        result = eg.AddPluginDialog.GetModalResult(
            mainFrame,
            checkMultiLoad = False
        )
        if not result:
            return
        pluginInfo = result[0]
        description = pluginInfo.englishDescription
        pos = description.find("<rst>")
        if pos != -1:
            description = DecodeReST(description[pos+5:])
        pluginData = {
            "guid": pluginInfo.guid,
            "name": pluginInfo.englishName,
            "author": pluginInfo.author,
            "version": pluginInfo.version,
            "description": description,
            "url": pluginInfo.url,
            "icon": pluginInfo.icon.pil.tostring()
        }
        dialog = InstallDialog(
            mainFrame,
            "Plugin Information",
            pluginData=pluginData,
            basePath=pluginInfo.path,
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
            path = dialog.GetPath()
        finally:
            dialog.Destroy()
        outfile = ZipFile(path, "w", ZIP_DEFLATED)
        outfile.writestr("info.pickle", pickle.dumps(pluginData))
        baseDir = os.path.basename(pluginInfo.path)
        for dirpath, dirnames, filenames in os.walk(pluginInfo.path):
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
                dst = os.path.join(baseDir, src[len(pluginInfo.path)+1:])
                print src, dst
                outfile.write(src, dst)
        outfile.close()


    def Import(self, filepath):
        tmpDir = tempfile.mkdtemp()
        try:
            infile = ZipFile(filepath, "r", ZIP_DEFLATED)
            infile.extractall(tmpDir)
            infile.close()
            infile = open(os.path.join(tmpDir, "info.pickle"), "r")
            pluginData = pickle.load(infile)
            infile.close()
            for name in os.listdir(tmpDir):
                path = os.path.join(tmpDir, name)
                if os.path.isdir(path):
                    basePath = path
                    break
            dialog = InstallDialog(
                title="Install EventGhost Plugin",
                pluginData=pluginData,
                basePath=basePath,
            )
            result = dialog.ShowModal()
            dialog.Destroy()
            if result == wx.ID_CANCEL:
                return
            guid = pluginData['guid']
            if guid in eg.pluginManager.guidDatabase:
                # a plugin with same GUID already exists
                info = eg.pluginManager.guidDatabase[guid]
                if info.path.lower().startswith(eg.userPluginDir.lower()):
                    # plugin with same GUID exists in user dir, so delete
                    # the folder first
                    shutil.rmtree(info.path, False)
            dstDir = os.path.join(eg.userPluginDir, os.path.basename(basePath))
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
            from eg.WinApi.Dynamic import ExitProcess
            ExitProcess(0)

PluginInstall = PluginInstall()


class InstallDialog(Dialog):

    def __init__(
        self,
        parent=None,
        title=eg.APP_NAME,
        basePath=None,
        pluginData=None,
    ):
        Dialog.__init__(
            self,
            parent,
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
        questionCtrl = self.StaticText(
            "Do you really want to install this plugin into EventGhost?"
        )
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

