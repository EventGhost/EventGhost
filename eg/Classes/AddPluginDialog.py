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

import eg
import wx

  
KIND_TAGS = ["remote", "program", "external", "other"]

class Config(eg.PersistentData):
    position = None
    size = (640, 450)
    splitPosition = 240
    lastSelection = None
    collapsed = set()



class Text(eg.TranslatableStrings):
    title = "Choose a plugin to add..."
    noInfo = "No information available."
    noMultiloadTitle = "No multiload possible"
    noMultiload = (
        "This plugin doesn't support multiload and you already have one " 
        "instance of this plugin in your configuration."
    )
    remotePlugins = "Remote Receiver"
    programPlugins = "Program Control"
    externalPlugins = "External Equipment"
    otherPlugins = "Other"
    author = "Author:"
    version = "Version:"
    descriptionBox = "Description"
    


class AddPluginDialog(eg.Dialog):

    @eg.LogItWithReturn
    def Process(self, parent):
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

        self.treeCtrl = treeCtrl = wx.TreeCtrl(
            splitterWindow,
            style=wx.TR_SINGLE
                |wx.TR_HAS_BUTTONS
                |wx.TR_HIDE_ROOT
                |wx.TR_LINES_AT_ROOT
        )
        
        treeCtrl.SetMinSize((170, 200))

        imageList = wx.ImageList(16, 16)
        imageList.Add(eg.Icons.PLUGIN_ICON.GetBitmap())
        imageList.Add(eg.Icons.FOLDER_ICON.GetBitmap())
        treeCtrl.SetImageList(imageList)
        
        root = treeCtrl.AddRoot("")
        typeIds = {
            KIND_TAGS[0]: treeCtrl.AppendItem(root, Text.remotePlugins, 1),
            KIND_TAGS[1]: treeCtrl.AppendItem(root, Text.programPlugins, 1),
            KIND_TAGS[2]: treeCtrl.AppendItem(root, Text.externalPlugins, 1),
            KIND_TAGS[3]: treeCtrl.AppendItem(root, Text.otherPlugins, 1),
        }
        self.typeIds = typeIds
        itemToSelect = typeIds["remote"]
        
        for info in eg.pluginManager.GetPluginInfoList():
            if info.kind in ("hidden", "core"):
                continue
            if info.icon and info.icon != eg.Icons.PLUGIN_ICON:
                idx = imageList.Add(
                    eg.Icons.PluginSubIcon(info.icon).GetBitmap()
                )
            else:
                idx = 0

            treeId = treeCtrl.AppendItem(typeIds[info.kind], info.name, idx)
            treeCtrl.SetPyData(treeId, info)
            if info.path == Config.lastSelection:
                itemToSelect = treeId
                
        
        for kind, treeId in typeIds.iteritems():
            if kind in Config.collapsed:
                treeCtrl.Collapse(treeId)
            else:
                treeCtrl.Expand(treeId)
        
        treeCtrl.ScrollTo(itemToSelect)
        
        rightPanel = wx.Panel(splitterWindow)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightPanel.SetSizer(rightSizer)
        
        self.nameText = nameText = wx.StaticText(rightPanel)
        nameText.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD))
        rightSizer.Add(nameText, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM, 5)
        
        subSizer = wx.FlexGridSizer(2, 2)
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

        self.buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL), True)
        self.okButton = self.buttonRow.okButton
        self.okButton.Enable(False)
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(splitterWindow, 1, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(self.buttonRow.sizer, 0, wx.EXPAND)
        
        self.SetSizerAndFit(mainSizer)
        #minSize = mainSizer.GetMinSize()
        #self.SetMinSize(minSize)
        self.SetSize(Config.size)
        splitterWindow.SetSashPosition(Config.splitPosition)
        if Config.position:
            self.SetPosition(Config.position)
        treeCtrl.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
        treeCtrl.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivated)
        treeCtrl.SelectItem(itemToSelect)
        while self.Affirmed():
            if self.CheckMultiload():
                self.SetResult(self.resultData)
        Config.size = self.GetSizeTuple()
        Config.position = self.GetPositionTuple()
        Config.splitPosition = splitterWindow.GetSashPosition()
        Config.collapsed = set(
            kind for kind, treeId in typeIds.iteritems() 
                if not treeCtrl.IsExpanded(treeId)
        )


    def OnSelectionChanged(self, event):
        """
        Handle the wx.EVT_TREE_SEL_CHANGED events.
        """
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
            self.authorText.SetLabel(info.author.replace("&", "&&"))
            self.versionLabel.SetLabel(Text.version)
            self.versionText.SetLabel(info.version)
            self.okButton.Enable(True)
        self.nameText.SetLabel(name)
        self.descrBox.SetPage(description)


    def CheckMultiload(self):
        info = self.resultData
        if (
            info
            and info.pluginCls 
            and not info.canMultiLoad 
            and info.instances
        ):
            eg.MessageBox(
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
            self.OnOK()
            return
        event.Skip()
        
        