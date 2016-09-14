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
from time import sleep

# Local imports
import eg
from eg.Icons import GetInternalBitmap
from eg.WinApi import (
    EnumProcesses,
    GetClassName,
    GetProcessName,
    GetTopLevelWindowList,
    GetWindowText,
    GetWindowThreadProcessId,
)
from eg.WinApi.Dynamic import (
    GA_PARENT,
    GA_ROOT,
    GetAncestor,
)
from eg.WinApi.Utils import (
    GetHwndChildren,
    GetHwndIcon,
    HighlightWindow,
    HwndHasChildren,
)

class WindowTree(wx.TreeCtrl):
    def __init__(self, parent, includeInvisible=False):
        self.includeInvisible = includeInvisible
        self.pids = {}
        wx.TreeCtrl.__init__(
            self,
            parent,
            -1,
            style=(
                wx.TR_DEFAULT_STYLE |
                wx.TR_HIDE_ROOT |
                wx.TR_FULL_ROW_HIGHLIGHT
            ),
            size=(-1, 150)
        )
        self.imageList = imageList = wx.ImageList(16, 16)
        imageList.Add(GetInternalBitmap("cwindow"))
        imageList.Add(GetInternalBitmap("cedit"))
        imageList.Add(GetInternalBitmap("cstatic"))
        imageList.Add(GetInternalBitmap("cbutton"))
        self.SetImageList(imageList)
        self.root = self.AddRoot("")

        # tree context menu
        def OnCmdHighlight(dummyEvent=None):
            hwnd = self.GetPyData(self.GetSelection())
            for _ in range(10):
                HighlightWindow(hwnd)
                sleep(0.1)
        menu = wx.Menu()
        menuId = wx.NewId()
        menu.Append(menuId, "Highlight")
        self.Bind(wx.EVT_MENU, OnCmdHighlight, id=menuId)
        self.contextMenu = menu

        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnItemRightClick)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnItemExpanding)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
        self.AppendPrograms()

    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass

    def AppendChildWindows(self, parentHwnd, item):
        for hwnd in GetHwndChildren(parentHwnd, self.includeInvisible):
            name = GetWindowText(hwnd)
            className = GetClassName(hwnd)
            if name != "":
                name = "\"" + name + "\" "
            index = self.AppendItem(item, name + className, 0)
            self.SetPyData(index, hwnd)
            if className == "Edit" or className == "TEdit":
                self.SetItemImage(index, 1, which=wx.TreeItemIcon_Normal)
            elif className == "Static" or className == "TStaticText":
                self.SetItemImage(index, 2, which=wx.TreeItemIcon_Normal)
            elif className == "Button" or className == "TButton":
                self.SetItemImage(index, 3, which=wx.TreeItemIcon_Normal)
            elif GetClassName(parentHwnd) == "MDIClient":
                icon = GetHwndIcon(hwnd)
                if icon:
                    iconIndex = self.imageList.AddIcon(icon)
                    self.SetItemImage(
                        index,
                        iconIndex,
                        which=wx.TreeItemIcon_Normal
                    )

            if HwndHasChildren(hwnd, self.includeInvisible):
                self.SetItemHasChildren(index, True)

    def AppendPrograms(self):
        self.pids.clear()
        processes = EnumProcesses()    # get PID list
        for pid in processes:
            self.pids[pid] = []

        hwnds = GetTopLevelWindowList(self.includeInvisible)

        for hwnd in hwnds:
            pid = GetWindowThreadProcessId(hwnd)[1]
            if pid == eg.processId:
                continue
            self.pids[pid].append(hwnd)

        for pid in processes:
            if len(self.pids[pid]) == 0:
                continue
            iconIndex = 0
            for hwnd in self.pids[pid]:
                icon = GetHwndIcon(hwnd)
                if icon:
                    iconIndex = self.imageList.AddIcon(icon)
                    break
            exe = GetProcessName(pid)
            item = self.AppendItem(self.root, exe)
            self.SetItemHasChildren(item, True)
            self.SetPyData(item, pid)
            self.SetItemImage(item, iconIndex, which=wx.TreeItemIcon_Normal)

    def AppendToplevelWindows(self, pid, item):
        hwnds = self.pids[pid]
        for hwnd in hwnds:
            try:
                name = GetWindowText(hwnd)
                className = GetClassName(hwnd)
                icon = GetHwndIcon(hwnd)
            except:
                continue
            if name != '':
                name = '"%s"' % name
            iconIndex = 0
            if icon:
                iconIndex = self.imageList.AddIcon(icon)
            newItem = self.AppendItem(item, name)
            self.SetPyData(newItem, hwnd)
            self.SetItemText(newItem, name + className)
            self.SetItemImage(
                newItem,
                iconIndex,
                which=wx.TreeItemIcon_Normal
            )
            if HwndHasChildren(hwnd, self.includeInvisible):
                self.SetItemHasChildren(newItem, True)

    @eg.LogIt
    def Destroy(self):
        self.Unselect()
        self.imageList.Destroy()
        return wx.TreeCtrl.Destroy(self)

    def OnItemCollapsed(self, event):
        """
        Handles wx.EVT_TREE_ITEM_COLLAPSED events.
        """
        # We need to remove all children here, otherwise we'll see all
        # that old rubbish again after the next expansion.
        self.DeleteChildren(event.GetItem())

    def OnItemExpanding(self, event):
        """
        Handles wx.EVT_TREE_ITEM_EXPANDING events.
        """
        item = event.GetItem()
        if self.IsExpanded(item):
            # This event can happen twice in the self.Expand call
            return

        res = self.GetItemParent(item)
        if res == self.root:
            pid = self.GetPyData(item)
            self.AppendToplevelWindows(pid, item)
        else:
            hwnd = self.GetPyData(item)
            self.AppendChildWindows(hwnd, item)

    def OnItemRightClick(self, dummyEvent):
        """
        Handles wx.EVT_TREE_ITEM_RIGHT_CLICK events.
        """
        self.PopupMenu(self.contextMenu)

    @eg.LogIt
    def Refresh(self):
        self.Freeze()
        self.DeleteChildren(self.root)
        self.AppendPrograms()
        self.Thaw()

    @eg.LogIt
    def SelectHwnd(self, hwnd):
        if hwnd is None:
            self.Unselect()
            return
        _, pid = GetWindowThreadProcessId(hwnd)
        item, cookie = self.GetFirstChild(self.root)
        while self.GetPyData(item) != pid:
            item, cookie = self.GetNextChild(self.root, cookie)
            if not item.IsOk():
                return

        chain = [hwnd]
        rootHwnd = GetAncestor(hwnd, GA_ROOT)
        tmp = hwnd
        while tmp != rootHwnd:
            tmp = GetAncestor(tmp, GA_PARENT)
            chain.append(tmp)

        lastItem = item
        for child in chain[::-1]:
            self.Expand(item)
            item, cookie = self.GetFirstChild(lastItem)
            while self.GetPyData(item) != child:
                item, cookie = self.GetNextChild(lastItem, cookie)
                if not item.IsOk():
                    return
            lastItem = item
        self.SelectItem(lastItem)
