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


gLastSelected = None


class DefaultConfig:
    position = None
    size = (550, 400)
    splitPosition = 210

config = eg.GetConfig("AddEventDialog", DefaultConfig)


class Text(eg.TranslatableStrings):
    title = "Select an event to add..."
    descriptionLabel = "Description"



class EventInfo:
    icon = eg.Icons.EVENT_ICON
    
    def __init__(self, name, description, info):
        self.name = name
        self.description = description
        self.info = info
        
        
        
class AddEventDialog(eg.Dialog):
    
    def __init__(self, parent):
        self.resultData = None
        eg.Dialog.__init__(
            self, 
            parent, 
            -1,
            Text.title, 
            style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME
        )
        splitterWindow = wx.SplitterWindow(
            self, 
            -1,
            style=wx.SP_LIVE_UPDATE
                |wx.CLIP_CHILDREN
                |wx.NO_FULL_REPAINT_ON_RESIZE
        )
        self.splitterWindow = splitterWindow

        style = wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT|wx.TR_FULL_ROW_HIGHLIGHT
        tree = wx.TreeCtrl(splitterWindow, -1, style=style)
        tree.SetMinSize((100,100))
        tree.SetImageList(eg.Icons.gImageList)
        self.tree = tree
        
        tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
        tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated)
        tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnCollapsed)
        tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnExpanded)
       
        self.htmlTemplate = (
            '<html><body bgcolor="#%02X%02X%02X">%%s</body></html>' 
                % self.GetBackgroundColour().Get()
        )

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


    def FillTree(self):
        tree = self.tree
        for plugin in eg.pluginList:
            eventList = plugin.info.eventList
            if eventList is None:
                continue
            item = tree.AppendItem(self.root, plugin.name)
            tree.SetPyData(item, plugin.info)
            tree.SetItemImage(item, plugin.info.icon.folderIndex)
            
            for eventName, description in eventList:
                data = EventInfo(eventName, description, plugin.info)
                tmp = tree.AppendItem(item, eventName)
                tree.SetPyData(tmp, data)
                tree.SetItemImage(tmp, data.icon.index)
                
                
    def ReloadTree(self):
        tree = self.tree
        tree.DeleteAllItems()
        self.root = tree.AddRoot("Functions")
        self.lastSelectedTreeItem = None
        self.FillTree()
        
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
#        if isinstance(data, eg.ActionClass):
#            self.resultData = data
#            self.buttonRow.okButton.Enable(True)
#            info = data.plugin.info
#        else:
#            self.resultData = None
#            self.buttonRow.okButton.Enable(False)
#            if isinstance(data, eg.ActionGroup):
#                info = data.plugin.info
#            else:
#                info = data
        self.nameText.SetLabel(data.name)
        #self.docText.SetBasePath(data.info.path)
        self.docText.SetPage(self.htmlTemplate % data.description)
        
        
    def OnCollapsed(self, event):
        self.tree.GetPyData(event.GetItem()).expanded = False
        
        
    def OnExpanded(self, event):
        self.tree.GetPyData(event.GetItem()).expanded = True
        
        
    def OnActivated(self, event):
        item = self.tree.GetSelection()
        data = self.tree.GetPyData(item)
        if isinstance(data, eg.ActionClass):
            self.EndModal(wx.ID_OK)
        else:
            event.Skip()


    @eg.LogItWithReturn
    def Destroy(self):
        global gLastSelected
        item = self.tree.GetSelection()
        gLastSelected = self.tree.GetPyData(item)        
        config.size = self.GetSizeTuple()
        config.position = self.GetPositionTuple()
        config.splitPosition = self.splitterWindow.GetSashPosition()
        eg.Dialog.Destroy(self)
        
        


