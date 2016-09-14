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

import wx

# Local imports
import eg

class TreeItemBrowseCtrl(wx.TreeCtrl):
    def __init__(
        self,
        parent,
        filterFunc=None,
        searchFunc=None,
        selectItem=None,
        multiSelect=False
    ):
        if searchFunc is None:
            searchFunc = lambda obj, id: None

        self.filterFunc = filterFunc
        self.searchFunc = searchFunc
        style = (
            wx.TR_HAS_BUTTONS |
            wx.CLIP_CHILDREN |
            wx.NO_FULL_REPAINT_ON_RESIZE
        )
        if multiSelect:
            style |= wx.TR_MULTIPLE
        wx.TreeCtrl.__init__(self, parent, style=style)
        self.SetMinSize((10, 10))
        self.SetImageList(eg.Icons.gImageList)
        srcTree = eg.document.frame.treeCtrl

        srcRoot = srcTree.GetRootItem()
        text = srcTree.GetItemText(srcRoot)
        image = srcTree.GetItemImage(srcRoot)
        obj = srcTree.GetPyData(srcRoot)
        self.root = root = self.AddRoot(text, image)
        self.SetPyData(root, obj)

        self.normalfont = self.GetItemFont(self.root)
        # evil workaround to get another font
        treeId = self.AppendItem(self.root, '')
        self.italicfont = self.GetItemFont(treeId)
        self.Delete(treeId)
        self.italicfont.SetStyle(wx.FONTSTYLE_ITALIC)

        self.__collapsing = False
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnExpanding)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnCollapsing)
        self.SetItemHasChildren(root)
        self.Expand(root)
        self.ScrollTo(root)
        self.UnselectAll()
        if not selectItem:
            return
        item = selectItem
        path = []
        while item is not selectItem.root:
            path.append(item)
            item = item.parent
        treeId = root
        for item in reversed(path):
            if not self.IsExpanded(treeId):
                self.Expand(treeId)
            tmp, cookie = self.GetFirstChild(treeId)
            while self.GetPyData(tmp) is not item:
                tmp, cookie = self.GetNextChild(tmp, cookie)
            treeId = tmp
        self.EnsureVisible(root)
        self.SelectItem(treeId)

    def OnCollapsing(self, event):
        # Be prepared, self.CollapseAndReset below may cause
        # another wx.EVT_TREE_ITEM_COLLAPSING event being triggered.
        treeId = event.GetItem()
        if self.__collapsing or treeId is self.root:
            event.Veto()
        else:
            self.__collapsing = True
            self.CollapseAndReset(treeId)
            self.SetItemHasChildren(treeId)
            self.__collapsing = False

    @eg.LogIt
    def OnExpanding(self, event):
        treeId = event.GetItem()
        obj = self.GetPyData(treeId)
        for child in obj.childs:
            if not self.filterFunc(child):
                continue
            tmp = self.AppendItem(
                treeId,
                child.GetLabel(),
                (
                    child.icon.index if child.isEnabled
                    else child.icon.disabledIndex
                ),
                -1,
                wx.TreeItemData(child)
            )
            for subChild in child.childs:
                if self.filterFunc(subChild):
                    self.SetItemHasChildren(tmp, True)
            child.SetAttributes(self, tmp)
            self.searchFunc(child, tmp)
