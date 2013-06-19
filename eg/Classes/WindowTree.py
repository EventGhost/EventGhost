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
# $LastChangedDate: 2007-12-12 21:48:49 +0100 (Mi, 12 Dez 2007) $
# $LastChangedRevision: 314 $
# $LastChangedBy: bitmonster $


from time import sleep
from win32api import GetCurrentProcessId
from win32process import EnumProcesses
from os.path import basename
from win32gui import EnumWindows, GetWindowText, GetClassName, IsWindowVisible
from win32process import GetWindowThreadProcessId

from ctypes.dynamic import GetAncestor, GA_ROOT, GA_PARENT
from eg.WinAPI.Utils import (
    GetHwndIcon, 
    GetHwndChildren, 
    HwndHasChildren,
    HighlightWindow,
    GetNameOfPID, 
)

ourProcessID = GetCurrentProcessId()


class WindowTree(wx.TreeCtrl):
    
    def __init__(self, parent, id=-1, includeInvisible=False):
        self.includeInvisible = includeInvisible
        wx.TreeCtrl.__init__(
            self, 
            parent, 
            -1, 
            style=wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT|wx.TR_FULL_ROW_HIGHLIGHT, 
            size=(-1, 150)
        )
        self.imageList = imageList = wx.ImageList(16, 16)
        imageList.Add(wx.Bitmap("images/cwindow.png"))
        imageList.Add(wx.Bitmap("images/cedit.png"))
        imageList.Add(wx.Bitmap("images/cstatic.png"))
        imageList.Add(wx.Bitmap("images/cbutton.png"))
        self.SetImageList(imageList)
        self.root = self.AddRoot("")
        
        # tree context menu
        menu = eg.Menu(self, "")
        
        def OnCmdHighlight(event):
            hwnd = self.GetPyData(self.GetSelection())
            for i in range(10):
                HighlightWindow(hwnd)
                sleep(0.1)
        menu.Append("Highlight", OnCmdHighlight)
        
        def OnPopupMenu(event):
            self.PopupMenu(menu)        
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, OnPopupMenu)
        
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnItemExpanding)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
        self.AppendPrograms()
        
        
    def OnItemExpanding(self, event):
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


    def OnItemCollapsed(self, event):
        # We need to remove all children here, otherwise we'll see all
        # that old rubbish again after the next expansion.
        self.DeleteChildren(event.GetItem())
        
        
    def AppendPrograms(self):
        self.pids = {}
        processes = EnumProcesses()    # get PID list
        for pid in processes:
            self.pids[pid] = []
            
        hwnds = []
        def EnumProc(hwnd, data):
            data.append(hwnd)
            return True
        EnumWindows(EnumProc, hwnds)
        
        for hwnd in hwnds:
            threadID, pid = GetWindowThreadProcessId(hwnd)
            if pid == ourProcessID:
                continue
            if not self.includeInvisible and not IsWindowVisible(hwnd):
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
            exe = basename(GetNameOfPID(pid))
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
            icon_index = 0
            if icon:
                icon_index = self.imageList.AddIcon(icon)
            new_item = self.AppendItem(item, name)
            self.SetPyData(new_item, hwnd)
            self.SetItemText(new_item, name + className)
            self.SetItemImage(
                new_item, 
                icon_index, 
                which=wx.TreeItemIcon_Normal
            )
            if HwndHasChildren(hwnd, self.includeInvisible):
                self.SetItemHasChildren(new_item, True)
            
            
    def AppendChildWindows(self, parentHwnd, item):
        for hwnd in GetHwndChildren(parentHwnd, self.includeInvisible):
            try:
                name = GetWindowText(hwnd)
                className = GetClassName(hwnd)
            except:
                continue
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
                
                
    @eg.LogIt
    def Refresh(self):
        self.Freeze()
        self.DeleteChildren(self.root)
        self.AppendPrograms()
        self.Thaw()
                          
                        
    @eg.LogIt
    def Destroy(self):
        self.Unselect()
        self.imageList.Destroy()
        return wx.TreeCtrl.Destroy(self)
    
    
    @eg.LogIt
    def SelectHwnd(self, hwnd):
        if hwnd is None:
            self.Unselect()
            return
        pid = GetWindowThreadProcessId(hwnd)[1]
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
        
        
    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass
        
        
