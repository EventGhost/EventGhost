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

from types import ClassType

gLastSelected = None


class DefaultConfig:
    position = None
    size = (550, 400)
    splitPosition = 210

config = eg.GetConfig("AddActionDialog", DefaultConfig)


class Text(eg.TranslatableStrings):
    title = "Select an action to add..."
    descriptionLabel = "Description"



class AddActionDialog(eg.Dialog):
    
    def Process(self, parent):
        global gLastSelected
        self.resultData = None
        eg.Dialog.__init__(
            self, 
            parent, 
            -1,
            Text.title, 
            style=wx.DEFAULT_DIALOG_STYLE
                |wx.RESIZE_BORDER
                |wx.THICK_FRAME
        )
        splitterWindow = wx.SplitterWindow(
            self, 
            -1,
            style=wx.SP_LIVE_UPDATE
                |wx.CLIP_CHILDREN
                |wx.NO_FULL_REPAINT_ON_RESIZE
        )

        style = wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT|wx.TR_FULL_ROW_HIGHLIGHT
        tree = wx.TreeCtrl(splitterWindow, -1, style=style)
        tree.SetMinSize((100,100))
        tree.SetImageList(eg.Icons.gImageList)
        self.tree = tree
        
        tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
        tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated)
        tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnCollapsed)
        tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnExpanded)
       
        rightPanel = self.rightPanel = wx.Panel(splitterWindow)
        rightSizer = self.rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightPanel.SetSizer(rightSizer)
        rightPanel.SetAutoLayout(True)
        
        self.nameText = nameText = wx.StaticText(rightPanel)
        nameText.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD))
        rightSizer.Add(nameText, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM, 5)
        
        staticBoxSizer = wx.StaticBoxSizer(
            wx.StaticBox(rightPanel, label=Text.descriptionLabel),
            wx.VERTICAL
        )
        self.docText = eg.HtmlWindow(rightPanel)
        self.docText.SetBorders(2)
        
        staticBoxSizer.Add(self.docText, 1, wx.EXPAND)
        rightSizer.Add(staticBoxSizer, 1, wx.EXPAND, 5)
        
        splitterWindow.SplitVertically(self.tree, rightPanel)
        splitterWindow.SetMinimumPaneSize(60)
        splitterWindow.UpdateSize()

        self.buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL), True)
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(splitterWindow, 1, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(self.buttonRow.sizer, 0, wx.EXPAND)
        
        self.SetSizerAndFit(mainSizer)
        minSize = mainSizer.GetMinSize()
        self.SetMinSize(minSize)
        self.SetSize(config.size)
        splitterWindow.SetSashPosition(config.splitPosition)
        if config.position is not None:
            self.SetPosition(config.position)
        self.ReloadTree()
        while self.Affirmed():
            self.SetResult(self.resultData)
        
        item = self.tree.GetSelection()
        gLastSelected = tree.GetPyData(item)        
        config.size = self.GetSizeTuple()
        config.position = self.GetPositionTuple()
        config.splitPosition = splitterWindow.GetSashPosition()
        


    def FillTree(self, item, data):
        tree = self.tree
        for i in data:
            if isinstance(i, type) and issubclass(i, eg.ActionClass):
                iconIndex = i.info.icon.index
                actionList = None
                name = i.name
            elif isinstance(i, eg.PluginClass):
                i = i.info
                actionList = i.actionList
                if not len(actionList):
                    continue
                iconIndex = i.icon.folderIndex
                name = i.label
            elif isinstance(i, eg.ActionGroup):
                iconIndex = i.icon.folderIndex
                actionList = i.actionList
                name = i.name
            else:
                raise Exception("unknown type in FillTree", i)
            tmp = tree.AppendItem(item, name)
            tree.SetPyData(tmp, i)
            tree.SetItemImage(tmp, iconIndex)
            if actionList:
                self.FillTree(tmp, actionList)
                if i.expanded:
                    tree.Expand(tmp)
            if i == gLastSelected:
                self.lastSelectedTreeItem = tmp
    
    
    def ReloadTree(self):
        tree = self.tree
        tree.DeleteAllItems()
        self.root = tree.AddRoot("Functions")
        self.lastSelectedTreeItem = None
        self.FillTree(self.root, eg.actionList)
        
        if self.lastSelectedTreeItem:
            item = self.lastSelectedTreeItem
            while True:
                item = tree.GetItemParent(item)
                if item == self.root:
                    break
                tree.EnsureVisible(item)
            tree.SelectItem(self.lastSelectedTreeItem)
        
        
    def OnSelectionChanged(self, event):
        item = event.GetItem()
        if not item.IsOk():
            return
        data = self.tree.GetPyData(item)
        if isinstance(data, type) and issubclass(data, eg.ActionClass):
            self.resultData = data
            self.buttonRow.okButton.Enable(True)
            info = data.plugin.info
        else:
            self.resultData = None
            self.buttonRow.okButton.Enable(False)
            if isinstance(data, eg.ActionGroup):
                info = data.plugin.info
            else:
                info = data
        self.nameText.SetLabel(data.name)
        self.docText.SetBasePath(info.path)
        self.docText.SetPage(data.description)
        
        
    def OnCollapsed(self, event):
        self.tree.GetPyData(event.GetItem()).expanded = False
        
        
    def OnExpanded(self, event):
        self.tree.GetPyData(event.GetItem()).expanded = True
        
        
    def OnActivated(self, event):
        item = self.tree.GetSelection()
        data = self.tree.GetPyData(item)
        if isinstance(data, type) and issubclass(data, eg.ActionClass):
            self.OnOK()
        else:
            event.Skip()

        
        


