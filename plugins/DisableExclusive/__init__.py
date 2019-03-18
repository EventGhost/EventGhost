# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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

import eg



eg.RegisterPlugin(
    name="Disable Exclusive",
    author="K, borrowed Code from Enable Exclusive",
    description=(
        "Disables every sibling and child in the selected tree item."
    ),
    version="0.1",
    guid="{14DDD7CA-A295-4AD0-92ED-EF0291C361B3}",
)

import wx
from eg import FolderItem, MacroItem


class DisableExclusive(eg.PluginBase):

    def __init__(self):
        self.AddAction(Disable)


class Disable(eg.ActionBase):
    name = "Disable Item Exclusively"
    description = (
        "Disables a specified folder or macro in your configuration, but "
        "also enables all other folders and macros that are siblings on "
        "the same level in that branch of the tree."
    )

    class text:
        label = "Disable Exclusively: %s"
        text1 = "Please select the folder/macro which should be disabled:"
        cantSelect = (
            "The selected item type can't change its disable state.\n\n"
            "Please select another item."
        )

    def __call__(self, link):
        if not link:
            return
        node = link.target
        if not node:
            return

        def DoIt():
            node.SetEnable(False)
            for child in node.parent.childs:
                if child is not node and child.isDeactivatable:
                    child.SetEnable(True)
        eg.actionThread.Call(DoIt)

    def Configure(self, link=None):
        panel = eg.ConfigPanel(resizable=True)
        if link is not None:
            searchItem = link.target
        else:
            searchItem = None
        link = eg.TreeLink(panel.dialog.treeItem)

        tree = eg.TreeItemBrowseCtrl(
            panel,
            self.FilterFunc,
            # searchFunc,
            selectItem=searchItem
        )
        tree.SetFocus()
        panel.sizer.Add(panel.StaticText(self.text.text1), 0, wx.BOTTOM, 5)
        panel.sizer.Add(tree, 1, wx.EXPAND)
        while panel.Affirmed():
            treeItem = tree.GetSelection()
            if treeItem.IsOk():
                obj = tree.GetItemData(treeItem)
                if self.IsSelectableItem(obj):
                    link.SetTarget(obj)
                    panel.SetResult(link)
                    continue
            eg.MessageBox(self.text.cantSelect, parent=panel)

    def FilterFunc(self, item):
        return isinstance(item, (FolderItem, MacroItem))

    def IsSelectableItem(self, item):
        return item.isDeactivatable

    def GetLabel(self, link):
        obj = link.target
        if obj:
            return self.text.label % obj.GetLabel()
        return self.text.label % ''
