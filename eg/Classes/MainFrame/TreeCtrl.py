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
from cStringIO import StringIO
from time import clock, sleep

import xml.etree.cElementTree as ElementTree
    
import ctypes
SendMessageTimeout = ctypes.windll.user32.SendMessageTimeoutA
SendMessage = ctypes.windll.user32.SendMessageA

ContainerItem = eg.ContainerItem
EventItem = eg.EventItem



class EventDropSource(wx.DropSource):
    
    def __init__(self, win, text):
        wx.DropSource.__init__(self, win)
        # create our own data format and use it in a
        # custom data object
        customData = wx.CustomDataObject("DragItem")
        customData.SetData(text)
    
        # Now make a data object for the text and also a composite
        # data object holding both of the others.
        textData = wx.TextDataObject(text)
        
        data = wx.DataObjectComposite()
        data.Add(textData)
        data.Add(customData)
        
        # We need to hold a reference to our data object, instead it could
        # be garbage collected
        self.data = data
    
        # And finally, create the drop source and begin the drag
        # and drop opperation
        self.SetData(data)   
        


from eg.Classes.TreeItem import (
    HINT_NO_DROP, HINT_MOVE_INSIDE, HINT_MOVE_BEFORE, HINT_MOVE_AFTER,
    HINT_MOVE_BEFORE_OR_AFTER, HINT_MOVE_EVERYWHERE
)

HITTEST_FLAGS = (
    wx.TREE_HITTEST_ONITEMLABEL |
    wx.TREE_HITTEST_ONITEMICON |
    wx.TREE_HITTEST_ONITEMRIGHT
)


class EventDropTarget(wx.PyDropTarget):
    
    def __init__(self, window):
        wx.PyDropTarget.__init__(self)
        self.treeCtrl = window
        self.dragCls = EventItem
        self.dragObject = None
        # specify the type of data we will accept
        self.tdata = wx.TextDataObject()
        self.ldata = wx.CustomDataObject(wx.CustomDataFormat("DragItem"))
        self.ldata.SetData("")
        self.data = wx.DataObjectComposite()
        self.data.Add(self.tdata)
        self.data.Add(self.ldata)
        self.SetDataObject(self.data)
        self.hwnd = window.GetHandle()
        self.lastExpanded = None
        self.lastHighlighted = None
        self.isExternalDrag = True
        self.position = None
        self.lastDropTime = clock()
        
        
    def OnDragOver(self, x, y, d):
        tree = self.treeCtrl
        dragCls = self.dragCls
        if self.lastHighlighted is not None:
            tree.SetItemDropHighlight(self.lastHighlighted, False)
            self.lastHighlighted = None
        # The value returned here tells the source what kind of visual
        # feedback to give.  For example, if wxDragCopy is returned then
        # only the copy cursor will be shown, even if the source allows
        # moves.  You can use the passed in (x,y) to determine what kind
        # of feedback to give.
        point = tree.ScreenToClient(wx.GetMousePosition())
        targetItem, flags = tree.HitTest(point)
        if flags & HITTEST_FLAGS:
            obj = tree.GetPyData(targetItem)
            dragObject = self.dragObject
            tmpObj = obj
            while tmpObj is not None:
                if tmpObj == dragObject:
                    self.position = None
                    return wx.DragNone
                tmpObj = tmpObj.parent

            insertionHint = obj.DropTest(dragCls)
            if targetItem == tree.lastDropTarget:
                if self.lastDropTime + 0.6 < clock():
                    if (obj.__class__ == tree.document.FolderItem 
                        or insertionHint == HINT_MOVE_INSIDE
                        or insertionHint == HINT_MOVE_EVERYWHERE) and not tree.IsExpanded(targetItem):
                        tree.Expand(targetItem)
            else:
                self.lastDropTime = clock()
                tree.lastDropTarget = targetItem
                
            if insertionHint == HINT_MOVE_BEFORE_OR_AFTER:
                x2, y2, w2, h2 = tree.GetBoundingRect(targetItem)
                if y > y2 + h2 / 2:
                    insertionHint = HINT_MOVE_AFTER
                else:
                    insertionHint = HINT_MOVE_BEFORE
            elif insertionHint == HINT_MOVE_EVERYWHERE:
                x2, y2, w2, h2 = tree.GetBoundingRect(targetItem)
                if y < y2 + h2 / 4:
                    insertionHint = HINT_MOVE_BEFORE
                elif y > y2 + (h2 / 4) * 3:
                    insertionHint = HINT_MOVE_AFTER
                else: 
                    insertionHint = HINT_MOVE_INSIDE
                
            if insertionHint == HINT_NO_DROP:
                tree.ClearInsertMark()
                self.position = None
                result = wx.DragNone
            elif insertionHint == HINT_MOVE_INSIDE:
                tree.SetItemDropHighlight(targetItem, True)
                self.lastHighlighted = targetItem
                self.position = (obj, 0)
                for i in xrange(len(obj.childs)-1, -1, -1):
                    next = obj.childs[i]
                    insertionHint = next.DropTest(dragCls)
                    if insertionHint in (HINT_MOVE_AFTER, HINT_MOVE_BEFORE_OR_AFTER, HINT_MOVE_EVERYWHERE):
                        tree.SetInsertMark(next.id, 1)
                        self.position = (obj, i+1)
                        break
                else:
                    tree.ClearInsertMark()
                result = wx.DragMove
            elif insertionHint == HINT_MOVE_BEFORE:
                parent = obj.parent
                pos = parent.GetChildIndex(obj)
                for i in xrange(pos-1, -1, -1):
                    next = parent.childs[i]
                    insertionHint = next.DropTest(dragCls)
                    if insertionHint == HINT_MOVE_BEFORE:
                        targetItem = next.id
                        pos -= 1
                tree.SetInsertMark(targetItem, 0)
                self.position = (parent, pos)
                result = wx.DragMove
            elif insertionHint == HINT_MOVE_AFTER:
                parent = obj.parent
                pos = parent.GetChildIndex(obj)
                for i in xrange(pos+1, len(parent.childs)):
                    next = parent.childs[i]
                    insertionHint = next.DropTest(dragCls)
                    if insertionHint == HINT_MOVE_AFTER:
                        targetItem = next.id
                        pos += 1
                tree.SetInsertMark(targetItem, 1)
                self.position = (parent, pos+1)
                result = wx.DragMove
            return result
        if tree.GetSelection().IsOk():
            tree.SelectItem(tree.GetSelection(), False)
            #tree.SetItemDropHighlight(tree.GetSelection(), False)
        return wx.DragNone


    @eg.LogIt
    def OnData(self, x, y, d):
        # Called when OnDrop returns True.  
        tree = self.treeCtrl
        tree.ClearInsertMark()
        if self.isExternalDrag and self.position is not None:
            # We need to get the data and do something with it.
            if self.GetData():
                # copy the data from the drag source to our data object
                if tree.GetSelection().IsOk():
                    tree.SelectItem(tree.GetSelection(), False)
                if self.lastHighlighted is not None:
                    tree.SetItemDropHighlight(self.lastHighlighted, False)
                if self.ldata.GetDataSize() > 0:
                    label = self.ldata.GetData()
                    self.ldata.SetData("")
                    parent, pos = self.position
                    eg.UndoHandler.NewEvent().Do(
                        tree.document, 
                        label, 
                        parent, 
                        pos
                    )
        # what is returned signals the source what to do
        # with the original data (move, copy, etc.)  In this
        # case we just return the suggested value given to us.
        return d  
        
        
    def OnLeave(self):
        self.treeCtrl.ClearInsertMark()


    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass


        
class TreeCtrl(wx.TreeCtrl):
    
    @eg.AssertNotMainThread
    def __init__(self, parent, document=None):
        self.frame = parent
        self.document = document
        style = (
            wx.TR_HAS_BUTTONS |
            wx.TR_EDIT_LABELS |
            wx.TR_ROW_LINES |
            wx.CLIP_CHILDREN
        )
        wx.TreeCtrl.__init__(self, parent, style=style)
        self.root = None
        self.rootname = eg.text.General.configTree
        self.SetImageList(eg.Icons.gImageList)
        self.hasFocus = False
        
        Bind = self.Bind
        Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnItemExpanding)
        Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnItemCollapsing)
        Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginLabelEdit)
        Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndLabelEdit)
        Bind(wx.EVT_SET_FOCUS, self.OnGetFocus)
        Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
        Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivate)
        Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnBeginDrag)
        Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
        Bind(wx.EVT_TREE_ITEM_MENU, self.OnContextMenu)
        Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDoubleClick)
        if eg.debugLevel:
            Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
        Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnExpanded)

        id = wx.NewId()
        self.dragtimer = wx.Timer(self, id)
        wx.EVT_TIMER(self, id, self.OnDragTimer)
        self.lastDropTarget = None
        self.isInEditLabel = False
        
        self.clipboardData = u""
        self.dropTarget = EventDropTarget(self)
        self.SetDropTarget(self.dropTarget)
        self.hwnd = self.GetHandle()
        # TVM_SETITEMHEIGHT = 4352 + 27
        #SendMessageTimeout(self.hwnd, 4379, 18, 0, 1, 100, 0)
        
        
    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass
    
    
    def OnLeftUp(self, event):
        event.Skip()
        
        
    @eg.LogIt
    def OnLeftDoubleClick(self, event):
        treeItem, flags = self.HitTest(event.GetPosition())
        if treeItem.IsOk():
            if isinstance(self.document.selection, eg.ActionItem):
                while wx.GetMouseState().LeftDown():
                    wx.GetApp().Yield()
                eg.UndoHandler.Configure().Try(self.document)
                return
        event.Skip()
    
    
    @eg.LogIt
    def OnItemActivate(self, event):
        item = event.GetItem()
        if item.IsOk():
            wx.CallAfter(eg.UndoHandler.Configure().Try, self.document)
            return
        #event.Skip()
        
        
    @eg.AssertNotMainThread
    def SetData(self):
        self.Freeze()
        try:
            self.root = self.document.root
            self.root.CreateTreeItem(self, None)
            self.Expand(self.root.id)
            self.document.selection.Select()
            firstVisibleItem = self.document.firstVisibleItem
            if firstVisibleItem and firstVisibleItem.id is not None:
                self.ScrollTo(firstVisibleItem.id)
        finally:
            self.Thaw()

    
    @eg.AssertNotMainThread
    @eg.LogIt
    def Destroy(self):
        document = self.document
        try:
            document.firstVisibleItem = self.GetPyData(self.GetFirstVisibleItem())
        except:
            pass
        document.SetTree(None)
        self.Freeze()
        self.Unbind(wx.EVT_TREE_SEL_CHANGED)
        self.DeleteAllItems()
        return
        #return wx.TreeCtrl.Destroy(self)

    
    @eg.LogIt
    def OnRightDown(self, event):
        self.EndEditLabel(self.GetSelection(), False)
        # seems like newer wxPython doesn't select the item on right-click
        # so we have to do it ourself
        pos = event.GetPosition()
        id, flags = self.HitTest(pos)
        if id.IsOk():
            self.SelectItem(id)
        

    @eg.LogIt
    def OnContextMenu(self, event):
        self.SetFocus()
        self.frame.SetupEditMenu(self.frame.popupMenu)
        self.PopupMenu(self.frame.popupMenu, event.GetPoint())

    
    #@eg.LogIt
    def OnSelectionChanged(self, event):
        id = event.GetItem()
        item = self.GetPyData(id)
        self.document.selection = item
        event.Skip()

    
    def OnExpanded(self, event):
        if self.OnItemExpandingItem == event.GetItem() and self.OnItemExpandingNum:
            self.ScrollTo(self.OnItemExpandingPos)
            self.Thaw()
            self.OnItemExpandingNum = False
        
        
    def OnCollapsed(self, event):
        id = event.GetItem()
        item = self.GetPyData(id)
        item.isExpanded = False
        
        
    #@eg.LogIt
    def OnItemExpanding(self, event):
        if not self.OnItemExpandingNum:
            self.OnItemExpandingItem = event.GetItem()
            self.Freeze()
            tmp = self.OnItemExpandingPos = self.GetFirstVisibleItem()
            self.OnItemExpandingNum = True
        try:
            id = event.GetItem()
            if not self.IsExpanded(id):
                item = self.GetPyData(id)
                item.isExpanded = True
                for child in item.childs:
                    child.CreateTreeItem(self, id)
        finally:
            pass
    
    OnItemExpandingNum = False
    
    @eg.LogIt
    def OnItemCollapsing(self, event):
        id = event.GetItem()
        if id == self.root.id:
            event.Veto()
            return
        self.Freeze()
        item = self.GetPyData(id)
        item.isExpanded = False
        self.Collapse(id)
        self.DeleteChildren(id)
        self.SetItemHasChildren(id)
        newSelectedId = self.GetSelection()
        newSelectedItem = self.GetPyData(newSelectedId)
        document = self.document
        if newSelectedItem is not document.selection:
            document.selection = newSelectedItem
        self.Thaw()
        

#    def OnToolTip(self, event):
#        id = event.GetItem()
#        item = self.GetPyData(id)
#        if not item:
#            return
#        xmlId = item.xmlId
#        s = item.GetLabel() + "\n\nxmlId: " + str(xmlId)
#        if isinstance(item, eg.ContainerItem):
#            s += "\nchilds: " + str(len(item.childs)) 
#            s += "\nexpanded:" + str(item.isExpanded)
#            s += "\nIsExpanded:" + str(self.IsExpanded(id))
#        event.SetToolTip(s)
        
        
    def OnToolTip(self, event):
        pass
        
        
    def SetInsertMark(self, treeItem, after):
        # TVM_SETINSERTMARK = 4378
        if treeItem is not None:
            lParam = long(treeItem.m_pItem)
            SendMessageTimeout(self.hwnd, 4378, after, lParam, 1, 100, 0)
    
    
    def ClearInsertMark(self):
        SendMessageTimeout(self.hwnd, 4378, 0, long(0), 1, 100, 0)
        

    def OnGetFocus(self, event):
        self.hasFocus = True
        eg.focusEvent.Fire(self)
        event.Skip(True)
        
        
    def OnKillFocus(self, event):
        self.hasFocus = False
        if not self.isInEditLabel:
            eg.focusEvent.Fire(None)
        event.Skip(True)
        
        
    @eg.LogIt
    def OnBeginLabelEdit(self, event):
        obj = self.GetPyData(event.GetItem())
        if (not obj.isRenameable) or (not self.hasFocus):
            event.Veto()
            return
        self.isInEditLabel = True
        self.editLabelId = event.GetItem()
        wx.CallAfter(self.InLabelEdit)


    def InLabelEdit(self):
        eg.focusEvent.Fire("Edit")
        
        
    def OnEndLabelEdit(self, event):
        self.isInEditLabel = False
        self.editLabelId = None
        eg.focusEvent.Fire(self)
        id = event.GetItem()
        item = self.GetPyData(id)
        newLabel = event.GetLabel()
        if not event.IsEditCancelled() and item.GetLabel() != newLabel:
            eg.UndoHandler.Rename(self.document, item, newLabel)
        event.Skip()
        
        
    def ExpandAll(self):
        self.Freeze()
        def _Expand(item):
            if isinstance(item, ContainerItem):
                if not item.isExpanded:
                    self.Expand(item.id)
                for child in item.childs:
                    _Expand(child)
        _Expand(self.root)
        self.EnsureVisible(self.GetSelection())
        self.Thaw()


    def CollapseAll(self):
        self.Freeze()
        def _Collapse(item):
            if isinstance(item, ContainerItem):
                item.isExpanded = False
                for child in item.childs:
                    _Collapse(child)
            item.id = None
        for child in self.root.childs:
            child.isExpanded = False
            for subchild in child.childs:
                _Collapse(subchild)
            self.CollapseAndReset(child.id)
        self.Thaw()
    
    
    @eg.LogItWithReturn
    def OnBeginDrag(self, event):
        dragId = event.GetItem()
        dragObject = self.GetPyData(dragId)
        if dragObject is self.document.autostartMacro:
            return
        self.SelectItem(dragId)
        dropSource = EventDropSource(self, self.GetItemXml(dragObject))
        dropTarget = self.dropTarget
        dropTarget.dragCls = dragObject.__class__.__bases__[1]
        dropTarget.dragObject = dragObject
        dropTarget.isExternalDrag = False
        self.dragtimer.Start(50)

        result = dropSource.DoDragDrop(wx.Drag_AllowMove)
        self.dragtimer.Stop()
        dropTarget.dragCls = EventItem
        dropTarget.dragObject = None
        dropTarget.isExternalDrag = True
        insertionMarkPos = dropTarget.position
        self.SelectItem(dragId, False)
        self.ClearInsertMark()
        if dropTarget.lastHighlighted is not None:
            self.SetItemDropHighlight(dropTarget.lastHighlighted, False)
        
        if insertionMarkPos is not None:
            parent, pos = insertionMarkPos
            eg.UndoHandler.MoveTo(self.document, dragObject, parent, pos)


    def GetTopLevelWindow(self):
        result = self
        while True:
            parent = result.GetParent()
            if parent is None:
                return result
            result = parent
            
        
    def OnDragTimer(self, event):
        pos = wx.GetMousePosition()
        r = self.GetScreenRect()
        r2 = self.GetTopLevelWindow().GetScreenRect()
        if r.x <= pos.x <= r.GetRight():
            if pos.y < r.y:
                if pos.y > r2.y:
                    self.ScrollLines(-1)
            elif pos.y > r.GetBottom():
                if pos.y < r2.GetBottom():
                    self.ScrollLines(1)


    def Cut(self, event=None):
        eg.UndoHandler.Cut(self.document, self.document.selection)
        
        
    def Copy(self, event=None):
        item = self.GetSelection()
        if item.IsOk():
            obj = self.GetPyData(item)
            data = self.GetItemXml(obj).decode("utf-8")
            if data != "" and wx.TheClipboard.Open():
                wx.TheClipboard.SetData(wx.TextDataObject(data))
                wx.TheClipboard.Close()
            self.clipboardData = data


    def Paste(self, event=None):
        eg.UndoHandler.Paste(self.document)
        

    def Clear(self, event=None):
        eg.UndoHandler.Clear(self.document, self.document.selection)
                

    def GetItemXml(self, obj):
        data = ""
        id = self.GetSelection()
        obj = self.GetPyData(id)
        buffer = StringIO()
        buffer.write('<?xml version="1.0" encoding="UTF-8" ?>\r\n')
        if obj == self.root:
            obj.GetXmlString(buffer.write)
        else:
            buildStr = str(eg.buildNum)
            buffer.write('<EventGhost Version="%s">\r\n' % buildStr)
            obj.GetXmlString(buffer.write, "    ")
            buffer.write('</EventGhost>')
        data = buffer.getvalue()
        buffer.close()
        return data
            
