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

from time import time, strftime, localtime
import collections

import wx
import wx.lib.mixins.listctrl as listmix

import eg

EVENT_ICON_INDEX = eg.EventItem.iconIndex



class LogCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    """Implemention of a ListCtrl with a circular buffer."""
    
    def __init__(
        self, 
        parent, 
        id=-1, 
        pos=wx.DefaultPosition, 
        size=wx.DefaultSize
    ):
        if eg.debugLevel:
            self.maxlength = 2000
            self.removeOnMax = 200
        else:
            self.maxlength = 2000
            self.removeOnMax = 200
        wx.ListCtrl.__init__(
            self, 
            parent, 
            id, 
            pos, 
            size,
            style=(
                wx.LC_REPORT
                |wx.LC_VIRTUAL
                |wx.NO_FULL_REPAINT_ON_RESIZE
                |wx.HSCROLL
                |wx.CLIP_CHILDREN
                |wx.LC_NO_HEADER
            )
        )
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.SetImageList(eg.imageList, wx.IMAGE_LIST_SMALL)

        sysColour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        r = sysColour.Red()
        g = sysColour.Green()
        b = sysColour.Blue()
        sum = r + g + (b / 2)
        if sum > 382:
            r = max(r - 15, 0)
            g = max(g - 15, 0)
        else:
            r = min(r + 60, 255)
            g = min(g + 60, 255)
            b = min(b + 60, 255)
        sysTextColour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOWTEXT)
        self.attr1 = wx.ListItemAttr()
        self.attr1.BackgroundColour = (r, g, b)
        self.attr1.TextColour = sysTextColour

        self.attr2 = wx.ListItemAttr()
        self.attr2.BackgroundColour = sysColour
        self.attr2.TextColour = sysTextColour
        
        text = self.text = eg.text.MainFrame.Logger
        self.InsertColumn(0, "")
        
        # logger popup menu
        menu = eg.Menu(self, "EditMenu", eg.text.MainFrame.Menu)
        menu.AddItem("Copy")
        menu.AddSeparator()
        menu.AddItem("ClearAll")
        self.contextMenu = menu
        
        Bind = self.Bind
        Bind(wx.EVT_RIGHT_DOWN, eg.DummyFunc)
        Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightUp)
        Bind(wx.EVT_LIST_BEGIN_DRAG, self.OnStartDrag)
        Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        
        self.logTimes = True
        self.OnGetItemText = self.OnGetItemTextWithTime
        self.__inSelection = False
        self.isOdd = False
        self.data = collections.deque()
        eg.log.SetCtrl(self)
        self.SetData(eg.log.GetData())
        
        
    @eg.LogIt
    def Destroy(self):
        eg.log.SetCtrl(None)
        return
        return wx.ListCtrl.Destroy(self)
        

    def OnSetFocus(self, event):
        eg.app.focusEvent.Fire(self)
        event.Skip()
        
        
    def OnKillFocus(self, event):
        eg.app.focusEvent.Fire(None)
        event.Skip()


    @eg.AssertNotMainThread
    def SetData(self, data):
        #self.Freeze()
        self.data = collections.deque(data)
        self.SetItemCount(len(data))
        #self.Thaw()
        self.ScrollList(0, 1000000)

        
    def SetTimeLogging(self, flag):
        self.logTimes = flag
        if flag:
            self.OnGetItemText = self.OnGetItemTextWithTime
        else:
            self.OnGetItemText = self.OnGetItemTextNormal
        self.Refresh()
        
        
    def OnStartDrag(self, event):
        idx = event.GetIndex()
        itemData = self.GetItemData(idx)
        if itemData[1] != EVENT_ICON_INDEX:
            return
        text = str(itemData[2])
        # create our own data format and use it in a
        # custom data object
        customData = wx.CustomDataObject(wx.CustomDataFormat("DragItem"))
        customData.SetData(text)

        # And finally, create the drop source and begin the drag
        # and drop opperation
        dropSource = wx.DropSource(self)
        dropSource.SetData(customData)
        result = dropSource.DoDragDrop(wx.Drag_AllowMove)
        if result == wx.DragMove:
            self.Refresh()
            
            
    def CanCut(self):
        return False
    
    
    def CanCopy(self):
        return self.GetSelectedItemCount() > 0
    
    
    def CanPaste(self):
        return False
    
    
    def OnCmdCopy(self, event):
        self.Copy()
        
    
    def Copy(self, event=None):
        text = ""
        lines = 1
        firstItem = item = self.GetNextItem(
            -1, 
            wx.LIST_NEXT_ALL, 
            wx.LIST_STATE_SELECTED
        )
        if item != -1:
            text = self.OnGetItemText(item, 0)
            item = self.GetNextItem(
                item, 
                wx.LIST_NEXT_ALL, 
                wx.LIST_STATE_SELECTED
            )
            while item != -1:
                lines += 1
                text += "\r\n" + self.OnGetItemText(item, 0)
                item = self.GetNextItem(
                    item, 
                    wx.LIST_NEXT_ALL, 
                    wx.LIST_STATE_SELECTED
                )
        if text != "" and wx.TheClipboard.Open():
            textDataObject = wx.TextDataObject(text)
            dataObjectComposite = wx.DataObjectComposite()
            dataObjectComposite.Add(textDataObject)
            if lines == 1:
                _, iconIndex, eventstring, _ = self.GetItemData(firstItem)
                if iconIndex == EVENT_ICON_INDEX:
                    customDataObject = wx.CustomDataObject("DragEventItem")
                    customDataObject.SetData(str(eventstring))
                    dataObjectComposite.Add(customDataObject)
            
            wx.TheClipboard.SetData(dataObjectComposite)
            wx.TheClipboard.Close()
            wx.TheClipboard.Flush()
            eg.app.clipboardEvent.Fire()
            
            
    def OnCmdClearAll(self, event):
        self.SetItemCount(0)
        self.DeleteAllItems()
        self.data.clear()
        self.ScrollList(0, 1000000)
        self.Refresh()
    
    
    @eg.LogIt
    def OnRightUp(self, event):
        self.PopupMenu(self.contextMenu)


    def OnMouseMotion(self, event):
        item, flags = self.HitTest(event.GetPosition())
        if flags & wx.LIST_HITTEST_ONITEM:
            self.tooltip.SetTip(self.OnGetItemText(item, 0))
        
        
    def OnDoubleClick(self, event):
        item, flags = self.HitTest(event.GetPosition())
        if flags & wx.LIST_HITTEST_ONITEM:
            _, iconIndex, wref, _ = self.GetItemData(item)
            if iconIndex != EVENT_ICON_INDEX and wref is not None:
                obj = wref()
                if obj is not None:
                    obj.Select()
        
        
    def GetItemData(self, item):
        return self.data[item]
    
    
    def OnGetItemText(self, item, column):
        raise NotImplementedError 
    
    
    def OnGetItemTextNormal(self, item, column):
        return " " + self.data[item][0]
        
        
    def OnGetItemTextWithTime(self, item, column):
        line, _, _, when = self.data[item]
        return strftime(" %X", localtime(when)) + "   " + line
        
        
    def OnGetItemAttr(self, item):
        if item % 2 == 0:
            return self.attr1
        else:
            return self.attr2


    def OnGetItemImage(self, item):
        return self.data[item][1]
    

    @eg.AssertNotMainThread
    def WriteLine(self, line, icon, wRef, when):
        data = self.data
        if len(data) >= self.maxlength:
             self.Freeze()
             for i in range(self.removeOnMax):
                 self.DeleteItem(0)
                 data.popleft()
             self.Thaw()
        data.append((line, icon, wRef, when))
        self.SetItemCount(len(data))
        self.ScrollList(0, 1000000)
        self.Update()


    @eg.LogIt
    def __del__(self):
        pass
                 
