# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import eg
import wx
import collections
from time import strftime, localtime
import wx.lib.mixins.listctrl as listmix


EVENT_ICON = eg.EventItem.icon
ERROR_ICON = eg.Icons.ERROR_ICON


class LogCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    """Implementation of a ListCtrl with a circular buffer."""

    def __init__(self, parent):
        self.maxlength = 2000
        self.removeOnMax = 200
        self.indent = ""
        self.OnGetItemText = self.OnGetItemTextWithTime
        wx.ListCtrl.__init__(
            self,
            parent,
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

        sysColour = eg.colour.windowBackground
        sysTextColour = eg.colour.windowText
        oddColour = eg.colour.GetOddLogColour()

        self.attr1 = wx.ListItemAttr()
        self.attr1.BackgroundColour = oddColour
        self.attr1.TextColour = sysTextColour

        self.attr2 = wx.ListItemAttr()
        self.attr2.BackgroundColour = sysColour
        self.attr2.TextColour = sysTextColour

        self.attr3 = wx.ListItemAttr()
        self.attr3.BackgroundColour = oddColour
        self.attr3.TextColour = (255, 0, 0)

        self.attr4 = wx.ListItemAttr()
        self.attr4.BackgroundColour = sysColour
        self.attr4.TextColour = (255, 0, 0)

        self.InsertColumn(0, "")

        # logger popup menu
        menu = wx.Menu()
        menu.Append(wx.ID_COPY, eg.text.MainFrame.Menu.Copy)
        self.Bind(wx.EVT_MENU, self.OnCmdCopy, id=wx.ID_COPY)
        menu.AppendSeparator()
        menuId = wx.NewId()
        menu.Append(menuId, eg.text.MainFrame.Menu.ClearLog)
        self.Bind(wx.EVT_MENU, self.OnCmdClearLog, id=menuId)
        self.contextMenu = menu

        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightUp)
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.OnStartDrag)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)

        self.logTimes = True
        self.__inSelection = False
        self.isOdd = False
        self.data = collections.deque()
        eg.log.SetCtrl(self)
        self.SetData(eg.log.GetData())


    @eg.LogIt
    def Destroy(self):
        eg.log.SetCtrl(None)


    def OnSetFocus(self, event):
        eg.Notify("FocusChange", self)
        event.Skip()


    def OnKillFocus(self, event):
        eg.Notify("FocusChange", None)
        event.Skip()


    @eg.AssertInMainThread
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


    def SetIndent(self, shouldIndent):
        if shouldIndent:
            self.indent = "   "
        else:
            self.indent = ""
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
        # and drop operation
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


    def OnCmdCopy(self, dummyEvent=None):
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
                eventstring, icon = self.GetItemData(firstItem)[:2]
                if icon == EVENT_ICON:
                    customDataObject = wx.CustomDataObject("DragEventItem")
                    customDataObject.SetData(eventstring.encode("UTF-8"))
                    dataObjectComposite.Add(customDataObject)

            wx.TheClipboard.SetData(dataObjectComposite)
            wx.TheClipboard.Close()
            wx.TheClipboard.Flush()


    def OnCmdClearLog(self, dummyEvent=None):
        self.SetItemCount(0)
        self.DeleteAllItems()
        self.data.clear()
        eg.log.data.clear()
        self.ScrollList(0, 1000000)
        self.Refresh()


    def OnRightUp(self, dummyEvent):
        self.PopupMenu(self.contextMenu)


    def OnDoubleClick(self, event):
        item, flags = self.HitTest(event.GetPosition())
        if flags & wx.LIST_HITTEST_ONITEM:
            icon, wref = self.GetItemData(item)[1:3]
            if icon != eg.EventItem.icon and wref is not None:
                node = wref()
                if node is not None and not node.isDeleted:
                    node.Select()


    def GetItemData(self, item):
        return self.data[item]


    def OnGetItemText(self, item, column):
        return ""


    def OnGetItemTextNormal(self, item, dummyColumn):
        line, _, _, _, indent = self.data[item]
        return " " + indent * self.indent + line


    def OnGetItemTextWithTime(self, item, dummyColumn):
        line, _, _, when, indent = self.data[item]
        return (
            strftime(" %X   ", localtime(when))
            + indent * self.indent
            + line
        )


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


    @eg.AssertInMainThread
    def WriteLine(self, line, icon, wRef, when, indent):
        data = self.data
        if len(data) >= self.maxlength:
            self.Freeze()
            for _ in range(self.removeOnMax):
                self.DeleteItem(0)
                data.popleft()
            self.Thaw()
        data.append((line, icon, wRef, when, indent))
        self.SetItemCount(len(data))
        self.ScrollList(0, 1000000)
        self.Update()


    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass

