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
import colorsys
import wx
import wx.lib.mixins.listctrl as listmix

import eg

EVENT_ICON = eg.EventItem.icon
ERROR_ICON = eg.Icons.ERROR_ICON


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
        self.SetImageList(eg.Icons.gImageList, wx.IMAGE_LIST_SMALL)

        sysColour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        sysTextColour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOWTEXT)

        hue, saturation, value = colorsys.rgb_to_hsv(
            sysColour.Red() / 255.0,
            sysColour.Green() / 255.0,
            sysColour.Blue() / 255.0
        )
        if value > 0.5:
            value -= 0.05
        else:
            value += 0.2
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        self.attr1 = wx.ListItemAttr()
        self.attr1.BackgroundColour = (
            int(round(r * 255.0)), 
            int(round(g * 255.0)), 
            int(round(b * 255.0)), 
        )
        self.attr1.TextColour = sysTextColour

        self.attr2 = wx.ListItemAttr()
        self.attr2.BackgroundColour = sysColour
        self.attr2.TextColour = sysTextColour
        
        self.attr3 = wx.ListItemAttr()
        self.attr3.BackgroundColour = self.attr1.BackgroundColour
        self.attr3.TextColour = (255, 0, 0)
        
        self.attr4 = wx.ListItemAttr()
        self.attr4.BackgroundColour = sysColour
        self.attr4.TextColour = (255, 0, 0)
        
        text = self.text = eg.text.MainFrame.Logger
        self.InsertColumn(0, "")
        
        # logger popup menu
        menu = eg.Menu(self, "EditMenu", eg.text.MainFrame.Menu)
        menu.AddItem("Copy")
        menu.AddSeparator()
        menu.AddItem("ClearLog")
        self.contextMenu = menu
        
        Bind = self.Bind
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
        if itemData[1] != EVENT_ICON:
            return
        text = itemData[2]
        # create our own data format and use it in a
        # custom data object
        customData = wx.CustomDataObject(wx.CustomDataFormat("DragItem"))
        customData.SetData(text.encode("utf-8"))

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
            text = self.OnGetItemText(item, 0)[1:]
            item = self.GetNextItem(
                item, 
                wx.LIST_NEXT_ALL, 
                wx.LIST_STATE_SELECTED
            )
            while item != -1:
                lines += 1
                text += "\r\n" + self.OnGetItemText(item, 0)[1:]
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
                _, icon, eventstring, _ = self.GetItemData(firstItem)
                if icon == EVENT_ICON:
                    customDataObject = wx.CustomDataObject("DragEventItem")
                    customDataObject.SetData(eventstring.encode("UTF-8"))
                    dataObjectComposite.Add(customDataObject)
            
            wx.TheClipboard.SetData(dataObjectComposite)
            wx.TheClipboard.Close()
            wx.TheClipboard.Flush()
            eg.app.clipboardEvent.Fire()
            
            
    def OnCmdClearLog(self, event):
        self.SetItemCount(0)
        self.DeleteAllItems()
        self.data.clear()
        self.ScrollList(0, 1000000)
        self.Refresh()
    
    
    def OnRightUp(self, event):
        self.PopupMenu(self.contextMenu)


    def OnMouseMotion(self, event):
        item, flags = self.HitTest(event.GetPosition())
        if flags & wx.LIST_HITTEST_ONITEM:
            self.tooltip.SetTip(self.OnGetItemText(item, 0)[1:])
        
        
    def OnDoubleClick(self, event):
        item, flags = self.HitTest(event.GetPosition())
        if flags & wx.LIST_HITTEST_ONITEM:
            _, icon, wref, _ = self.GetItemData(item)
            if icon != eg.EventItem.icon and wref is not None:
                obj = wref()
                if obj is not None and not obj.isDeleted:
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
            if self.data[item][1] != ERROR_ICON:
                return self.attr1
            else:
                return self.attr3
        else:
            if self.data[item][1] != ERROR_ICON:
                return self.attr2
            else:
                return self.attr4


    def OnGetItemImage(self, item):
        return self.data[item][1].index
    

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


    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass
                 
