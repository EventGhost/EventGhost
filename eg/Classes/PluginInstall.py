# This file is part of EventGhost.
# Copyright (C) 2007 Lars-Peter Voss <bitmonster@eventghost.org>
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

import os
import pickle
import tempfile
import shutil
import compileall
from zipfile import ZipFile, ZIP_DEFLATED
import wx
import eg
from eg.Utils import DecodeReST

TEMPLATE = """\
<b>Name:</b> {name}<br>
<b>Author:</b> {author}<br>
<b>Version:</b> {version}<br>
<p>
<b>Description:</b> {description}
"""

class PluginInstall(object):
    
    def Export(self):
        result = eg.AddPluginDialog.GetModalResult(
            eg.document.frame,
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
            "name": pluginInfo.englishName,
            "author": pluginInfo.author,
            "version": pluginInfo.version,
            "description": description,
            "guid": pluginInfo.guid,
        }
        dialog = eg.HtmlDialog(
            eg.document.frame, 
            "Plugin Information", 
            TEMPLATE.format(**pluginData),
            basePath = pluginInfo.path,
            style=wx.OK|wx.CANCEL
        )
        result = dialog.ShowModal()
        dialog.Destroy()
        if result == wx.ID_CANCEL:
            return
        filename = pluginInfo.englishName.replace("/", "-")
        dialog = wx.FileDialog(
            eg.document.frame,
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
                if ext.lower() in (".pyc", ".pyo") and filename[:-1] in filenames:
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
            dialog = eg.HtmlDialog(
                eg.document.frame, 
                "Plugin Information", 
                TEMPLATE.format(**pluginData),
                basePath = basePath,
                style=wx.OK|wx.CANCEL
            )
            result = dialog.ShowModal()
            dialog.Destroy()
            if result == wx.ID_CANCEL:
                return
            guid = pluginData['guid']
            dstDir = os.path.join(eg.userPluginDir, os.path.basename(basePath))
            if guid in eg.pluginManager.guidDatabase:
                info = eg.pluginManager.guidDatabase[guid]
                if info.path.lower().startswith(eg.userPluginDir.lower()):
                    print "plugin with same name and GUID exists in user dir"
                    shutil.rmtree(info.path, True)
                else:
                    print "base plugin with same GUID exists"
                eg.pluginManager.RemovePlugin(info)
            if os.path.exists(dstDir):
                print "wanted dir %s already used" % dstDir
                for i in range(2, 100):
                    searchDir = dstDir + str(i)
                    if not os.path.exists(searchDir):
                        dstDir = searchDir
                        print "now using %s" % dstDir
                        break
                else:
                    raise Exception("Can't create directory for plugin")
            shutil.copytree(basePath, dstDir)
            compileall.compile_dir(dstDir, ddir="UserPlugin", quiet=True)
            eg.pluginManager.AddPlugin(dstDir)
        finally:
            shutil.rmtree(tmpDir, True)
        
        
PluginInstall = PluginInstall()

