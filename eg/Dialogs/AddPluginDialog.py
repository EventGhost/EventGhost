# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

import os
import wx

import eg
from eg.IconTools import GetIcon, PilToBitmap
from ActionThread import CORE_PLUGINS
        
kindTags = ["remote", "program", "external", "other"]

class DefaultConfig:
    position = None
    size = (552, 382)
    splitPosition = 216
    expandDict = {}
    lastSelection = None

config = eg.GetConfig("AddPluginDialog", DefaultConfig)


class Text:
    title = "Choose a plugin to add..."
    noInfo = "No information available."
    noMultiloadTitle = "No multiload possible"
    noMultiload = \
        "This plugin doesn't support multiload and you already have one " \
        "instance of this plugin in your configuration."
    remotePlugins = "Remote Receiver"
    programPlugins = "Program Control"
    externalPlugins = "External Equipment"
    otherPlugins = "Other"
    author = "Author:"
    version = "Version:"
    descriptionBox = "Description"
    
Text = eg.GetTranslation(Text)


class AddPluginDialog(eg.Dialog):

    def __init__(self, parent):
        self.resultData = None

        eg.Dialog.__init__(
            self, 
            parent, 
            -1, 
            Text.title,
            style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER
        )

        splitterWindow = wx.SplitterWindow(
            self,
            style = wx.SP_LIVE_UPDATE
                |wx.CLIP_CHILDREN
                |wx.NO_FULL_REPAINT_ON_RESIZE
        )
        self.splitterWindow = splitterWindow

        self.treeCtrl = treeCtrl = wx.TreeCtrl(
            splitterWindow,
            style=wx.TR_SINGLE
                |wx.TR_HAS_BUTTONS
                |wx.TR_HIDE_ROOT
                |wx.TR_LINES_AT_ROOT
        )
        
        treeCtrl.SetMinSize((170, 200))

        imageList = self.imageList = wx.ImageList(16, 16)
        imageList.Add(GetIcon("images/plugin.png"))
        imageList.Add(GetIcon("images/folder.png"))
        treeCtrl.SetImageList(imageList)
        
        root = treeCtrl.AddRoot("")
        typeIds = {
            kindTags[0]: treeCtrl.AppendItem(root, Text.remotePlugins, 1),
            kindTags[1]: treeCtrl.AppendItem(root, Text.programPlugins, 1),
            kindTags[2]: treeCtrl.AppendItem(root, Text.externalPlugins, 1),
            kindTags[3]: treeCtrl.AppendItem(root, Text.otherPlugins, 1),
        }
        self.typeIds = typeIds
        itemToSelect = typeIds["remote"]
        
        pluginList = []
        for item in os.listdir("Plugins"):
            if item.startswith(".") or item.startswith("_"):
                continue
            if os.path.isdir("Plugins/" + item):
                pluginList.append(item)
        defaultTarget = typeIds["other"]
        for filename in pluginList:
            info = eg.GetPluginInfo(filename)
            idx = 0
            name = filename
            target = defaultTarget
            if info:
                if info.kind in ("hidden", "core"):
                    continue
                name = info.name
                if info.icon:
                    idx = imageList.Add(PilToBitmap(info.icon))
                target = typeIds.get(info.kind, target)
            id = treeCtrl.AppendItem(target, name, idx)
            treeCtrl.SetPyData(id, info)
            if filename == config.lastSelection:
                itemToSelect = id
                
        
        for kind, treeId in typeIds.iteritems():
            if config.expandDict.get(kind, True):
                treeCtrl.Expand(typeIds[kind])
            else:
                treeCtrl.Collapse(typeIds[kind])
        
        treeCtrl.ScrollTo(itemToSelect)
        
        self.htmlTemplate = (
            '<html><body bgcolor="#%02X%02X%02X">%%s</body></html>' 
                % self.GetBackgroundColour().Get()
        )

        rightPanel = wx.Panel(splitterWindow)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightPanel.SetSizer(rightSizer)
        
        self.nameText = nameText = wx.StaticText(rightPanel)
        nameText.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD))
        rightSizer.Add(nameText, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM, 5)
        
        subSizer = wx.FlexGridSizer(2,2)
        self.authorLabel = wx.StaticText(rightPanel, label=Text.author)
        subSizer.Add(self.authorLabel)
        self.authorText = wx.StaticText(rightPanel)
        subSizer.Add(self.authorText, 0, wx.EXPAND|wx.LEFT, 5)
        self.versionLabel = wx.StaticText(rightPanel, label=Text.version)
        subSizer.Add(self.versionLabel)
        self.versionText = wx.StaticText(rightPanel)
        subSizer.Add(self.versionText, 0, wx.EXPAND|wx.LEFT, 5)
        rightSizer.Add(subSizer, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM, 5)
        
        staticBoxSizer = wx.StaticBoxSizer(
            wx.StaticBox(rightPanel, label=Text.descriptionBox)
        )
        
        descrBox = eg.HtmlWindow(rightPanel)
        descrBox.SetBasePath("/plugins/")
        self.descrBox = descrBox
        staticBoxSizer.Add(descrBox, 1, wx.EXPAND)
        
        rightSizer.Add(staticBoxSizer, 1, wx.EXPAND|wx.LEFT, 5)
        
        splitterWindow.SplitVertically(self.treeCtrl, rightPanel)
        splitterWindow.SetMinimumPaneSize(60)
        splitterWindow.SetSashGravity(0.0)
        splitterWindow.UpdateSize()

        self.buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL))
        self.okButton = self.buttonRow.okButton
        self.okButton.Enable(False)
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(splitterWindow, 1, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(self.buttonRow.sizer, 0, wx.EXPAND)
        
        self.SetSizerAndFit(mainSizer)
        #minSize = mainSizer.GetMinSize()
        #self.SetMinSize(minSize)
        self.SetSize(config.size)
        splitterWindow.SetSashPosition(config.splitPosition)
        if config.position:
            self.SetPosition(config.position)
        treeCtrl.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelect)
        treeCtrl.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivated)
        treeCtrl.SelectItem(itemToSelect)
        if eg.debugLevel:
            exportListButton = wx.Button(self, -1, "Export list to clipboard")
            exportListButton.Bind(wx.EVT_BUTTON, self.OnExportList)
            self.buttonRow.Add(exportListButton)
            
            
    def OnExportList(self, event):
        import re
        import cStringIO
        text = cStringIO.StringIO()
        tree = self.treeCtrl
        text.write("This is the list of plugins currently distributed with EventGhost:\n\n")
        pluginList = []
        for item in os.listdir("Plugins"):
            if item.startswith(".") or item.startswith("_"):
                continue
            if os.path.isdir("Plugins/" + item):
                pluginList.append(item)
        kindList = ["core"] + kindTags
        groups = {}
        for filename in pluginList:
            info = eg.GetPluginInfo(filename)
            if info.kind in groups:
                groups[info.kind].append(info)
            else:
                groups[info.kind] = [info]
        for kind in kindList:
            text.write("\n\n== %s ==\n\n" % kind)
            groups[kind].sort()
            for info in groups[kind]:
                text.write("====%s====\n" % info.name)
                try:
                    description = info.description.splitlines()[0]
                except:
                    description = info.description
                s = re.sub(
                    r'<a\s+href="http://(.*?)">\s*((\n|.)+?)\s*</a>',
                    r'[http://\1 \2]',
                    description
                )
                text.write(":%s\n\n" % s)
        print text.getvalue()

        if wx.TheClipboard.Open():
            tdata = wx.TextDataObject(text.getvalue())
            wx.TheClipboard.SetData(tdata)
            wx.TheClipboard.Close()
            wx.TheClipboard.Flush()
        text.close()
        
            
    def OnSelect(self, event):
        item = event.GetItem()
        self.resultData = info = self.treeCtrl.GetPyData(item)       
        if info is None:
            name = self.treeCtrl.GetItemText(item)
            description = Text.noInfo
            self.authorLabel.SetLabel("")
            self.authorText.SetLabel("")
            self.versionLabel.SetLabel("")
            self.versionText.SetLabel("")
            self.okButton.Enable(False)
            event.Skip()
        else:
            name = info.name
            description = info.description
            self.descrBox.SetBasePath(info.path)
            self.authorLabel.SetLabel(Text.author)
            self.authorText.SetLabel(info.author)
            self.versionLabel.SetLabel(Text.version)
            self.versionText.SetLabel(info.version)
            self.okButton.Enable(True)
        self.nameText.SetLabel(name)
        self.descrBox.SetPage(self.htmlTemplate % description)


    def CheckMultiload(self):
        info = self.resultData
        if (
            info
            and info.pluginCls 
            and not info.pluginCls.canMultiLoad 
            and info.instances
        ):
            wx.MessageBox(
                Text.noMultiload,
                Text.noMultiloadTitle, 
                style=wx.ICON_EXCLAMATION
            )
            return False
        else:
            return True
        
        
    def OnItemActivated(self, event):
        item = self.treeCtrl.GetSelection()
        info = self.treeCtrl.GetPyData(item)
        if info is not None:
            if self.CheckMultiload():
                self.EndModal(wx.ID_OK)
            else:
                event.Skip()
        else:
            event.Skip()
        
        
    @eg.LogIt
    def OnOK(self, event):
        if self.CheckMultiload():
            event.Skip()
        
        
    def OnCancel(self, event):
        self.Close()


    def Destroy(self):
        config.size = self.GetSizeTuple()
        config.position = self.GetPositionTuple()
        config.splitPosition = self.splitterWindow.GetSashPosition()
        expandDict = {}
        for kind, treeId in self.typeIds.iteritems():
            expandDict[kind] = self.treeCtrl.IsExpanded(treeId)
        config.expandDict = expandDict        
        wx.Dialog.Destroy(self)
