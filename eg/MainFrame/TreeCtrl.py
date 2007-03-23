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

import os
import types
from cStringIO import StringIO
import win32api
from time import clock

import wx
import xml.etree.cElementTree as ElementTree
    
import eg
from eg.TreeItems import *
from UndoableCommands import (
    NewEvent, 
    CmdMoveTo, 
    CmdCut, 
    CmdPaste, 
    CmdClear, 
    CmdRename, 
    CmdToggleEnable
)

import ctypes
SendMessageTimeout = ctypes.windll.user32.SendMessageTimeoutA
SendMessage = ctypes.windll.user32.SendMessageA



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
        data.Add(customData)
        data.Add(textData)
        
        # We need to hold a reference to our data object, instead it could
        # be garbage collected
        self.data = data
    
        # And finally, create the drop source and begin the drag
        # and drop opperation
        self.SetData(data)   
        



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
        self.lastInsertLine = None
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
        id, flags = tree.HitTest(tree.ScreenToClient(wx.GetMousePosition()))
        if (
            flags & (
                wx.TREE_HITTEST_ONITEMLABEL
                |wx.TREE_HITTEST_ONITEMICON
                |wx.TREE_HITTEST_ONITEMRIGHT
            )
        ):
            obj = tree.GetPyData(id)
            dragObject = self.dragObject
            tmp_obj = obj
            while tmp_obj is not None:
                if tmp_obj == dragObject:
                    self.position = None
                    return wx.DragNone
                tmp_obj = tmp_obj.parent

            insertionHint = obj.DropTest(dragCls)
            if id == tree.lastDropTarget:
                if self.lastDropTime + 0.6 < clock():
                    if (obj.__class__ == tree.document.FolderItem 
                        or insertionHint == 1 
                        or insertionHint == 5) and not tree.IsExpanded(id):
                        tree.Expand(id)
            else:
                self.lastDropTime = clock()
                tree.lastDropTarget = id
                
            if insertionHint == 4:
                x2, y2, w2, h2 = tree.GetBoundingRect(id)
                if y > y2 + h2 / 2:
                    insertionHint = 3
                else:
                    insertionHint = 2
            elif insertionHint == 5:
                x2, y2, w2, h2 = tree.GetBoundingRect(id)
                if y < y2 + h2 / 4: # before
                    insertionHint = 2
                elif y > y2 + (h2 / 4) * 3: # after
                    insertionHint = 3
                else: #inside
                    insertionHint = 1
                
            if insertionHint is None: # cannot be dropped
                tree.ClearInsertMark()
                self.position = None
                result = wx.DragNone
            elif insertionHint == 1: # would be moved inside
                tree.SetItemDropHighlight(id, True)
                self.lastHighlighted = id
                self.position = (obj, 0)
                for i in xrange(len(obj.childs)-1, -1, -1):
                    next = obj.childs[i]
                    insertionHint = next.DropTest(dragCls)
                    if insertionHint in (3,4,5):
                        tree.SetInsertMark(next.id, 1)
                        self.position = (obj, i+1)
                        break
                else:
                    tree.ClearInsertMark()
                result = wx.DragMove
            elif insertionHint == 2: # would move before
                parent = obj.parent
                pos = parent.GetChildIndex(obj)
                for i in xrange(pos-1, -1, -1):
                    next = parent.childs[i]
                    insertionHint = next.DropTest(dragCls)
                    if insertionHint == 2:
                        id = next.id
                        pos -= 1
                tree.SetInsertMark(id, 0)
                self.position = (parent, pos)
                result = wx.DragMove
            elif insertionHint == 3: # would move after
                parent = obj.parent
                pos = parent.GetChildIndex(obj)
                for i in xrange(pos+1, len(parent.childs)):
                    next = parent.childs[i]
                    insertionHint = next.DropTest(dragCls)
                    if insertionHint == 3:
                        id = next.id
                        pos += 1
                tree.SetInsertMark(id, 1)
                self.position = (parent, pos+1)
                result = wx.DragMove
            return result
        if tree.GetSelection().IsOk():
            tree.SelectItem(tree.GetSelection(), False)
            #tree.SetItemDropHighlight(tree.GetSelection(), False)
        return wx.DragNone


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
                    NewEvent().Do(
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


    @eg.LogIt
    def __del__(self):
        pass


        
class TreeCtrl(wx.TreeCtrl):
    
    @eg.AssertNotMainThread
    def __init__(self, parent, id=-1, document=None):
        self.frame = parent
        self.document = document
        wx.TreeCtrl.__init__(
            self, 
            parent, 
            id,
            wx.DefaultPosition, 
            wx.DefaultSize,
            style=(
                wx.TR_HAS_BUTTONS
                |wx.TR_EDIT_LABELS
                |wx.TR_ROW_LINES
                |wx.CLIP_CHILDREN
                #|wx.TR_HIDE_ROOT
                #|wx.TR_LINES_AT_ROOT 
            )
        )
        self.root = None
        self.rootname = eg.text.General.configTree
        self.SetImageList(eg.imageList)
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
        @eg.LogIt
        def test(event):
            pass
        
        Bind(wx.EVT_TREE_KEY_DOWN, test)
        
        if eg.debugLevel:
            Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
        Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnExpanded)

        id = wx.NewId()
        self.dragtimer = wx.Timer(self, id)
        wx.EVT_TIMER(self, id, self.OnDragTimer)
        self.lastDropCount = 0
        self.lastDropTarget = None
        self.isInEditLabel = False
        
        self.clipboardData = u""
        self.dropTarget = EventDropTarget(self)
        self.SetDropTarget(self.dropTarget)
        self.lastInsertLine = None
        self.hwnd = self.GetHandle()
        # TVM_SETITEMHEIGHT = 4352 + 27
        #SendMessageTimeout(self.hwnd, 4379, 18, 0, 1, 100, 0)
        
        
    @eg.LogIt
    def __del__(self):
        pass
    
    
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
        document.firstVisibleItem = self.GetPyData(self.GetFirstVisibleItem())
        document.SetTree(None)
        self.Freeze()
        self.Unbind(wx.EVT_TREE_SEL_CHANGED)
        self.DeleteAllItems()
        return
        return wx.TreeCtrl.Destroy(self)

    
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
        self.frame.SetupEditMenu(self.frame.popupMenuItems)
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
        

    def OnToolTip(self, event):
        id = event.GetItem()
        item = self.GetPyData(id)
        if not item:
            return
        xmlId = item.xmlId
        s = item.GetLabel() + "\n\nxmlId: " + str(xmlId)
        if isinstance(item, ContainerItem):
            s += "\nchilds: " + str(len(item.childs)) 
            s += "\nexpanded:" + str(item.isExpanded)
            s += "\nIsExpanded:" + str(self.IsExpanded(id))
        event.SetToolTip(s)
        
        
    def SetInsertMark(self, id, after):
        # TVM_SETINSERTMARK = 4378
        if id is not None:
            SendMessageTimeout(
                self.hwnd, 
                4378, 
                after, 
                long(id.m_pItem), 
                1, 
                100, 
                0
            )
    
    
    def ClearInsertMark(self):
        SendMessageTimeout(self.hwnd, 4378, 0, long(0), 1, 100, 0)
        

    def OnItemActivate(self, event):
        item = event.GetItem()
        if item.IsOk():
            pyObj = self.GetPyData(item)
            if isinstance(pyObj, ActionItem):
                pyObj.Configure()
                return
        event.Skip()
        
        
    def OnToolTip(self, event):
        pass
        
        
    def OnGetFocus(self, event):
        self.hasFocus = True
        eg.app.focusEvent.Fire(self)
        event.Skip(True)
        
        
    def OnKillFocus(self, event):
        self.hasFocus = False
        if not self.isInEditLabel:
            eg.app.focusEvent.Fire(None)
        event.Skip(True)
        
        
    @eg.LogIt
    def OnBeginLabelEdit(self, event):
        obj = self.GetPyData(event.GetItem())
        if (not obj.isRenameable) or (not self.hasFocus):
            event.Veto()
            return
        self.isInEditLabel = True
        wx.CallAfter(self.InLabelEdit)


    def InLabelEdit(self):
        eg.app.focusEvent.Fire("Edit")
        print self.GetEditControl()
        @eg.LogIt
        def test(event): event.Skip()
        self.GetEditControl().Bind(wx.EVT_CHAR, test)
        
        
    def OnEndLabelEdit(self, event):
        self.isInEditLabel = False
        eg.app.focusEvent.Fire(self)
        id = event.GetItem()
        item = self.GetPyData(id)
        newLabel = event.GetLabel()
        if not event.IsEditCancelled() and item.GetLabel() != newLabel:
            CmdRename(self.document, item, newLabel)
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
        dropTarget.dragCls = dragObject.__class__.__bases__[0]
        dropTarget.dragObject = dragObject
        dropTarget.isExternalDrag = False
        self.dragtimer.Start(50)

        result = dropSource.DoDragDrop(wx.Drag_AllowMove)
        self.dragtimer.Stop()
        dropTarget.dragCls = EventItem
        dropTarget.dragObject = None
        dropTarget.isExternalDrag = True
        insert_mark_pos = dropTarget.position
        self.SelectItem(dragId, False)
        self.ClearInsertMark()
        if dropTarget.lastHighlighted is not None:
            self.SetItemDropHighlight(dropTarget.lastHighlighted, False)
        
        if insert_mark_pos is not None:
            parent, pos = insert_mark_pos
            CmdMoveTo(self.document, dragObject, parent, pos)


    def OnDragTimer(self, event):
        id, flags = self.HitTest(self.ScreenToClient(wx.GetMousePosition()))
        if flags & wx.TREE_HITTEST_ABOVE:
            first = self.GetFirstVisibleItem()
            self.ScrollLines(-1)
            #if first != self.GetFirstVisibleItem():
            #    self.Refresh()
        elif flags & wx.TREE_HITTEST_BELOW:
            first = self.GetFirstVisibleItem()
            self.ScrollLines(1)
            #if first != self.GetFirstVisibleItem():
            #    self.Refresh()


    def Cut(self, event=None):
        CmdCut(self.document, self.document.selection)
        
        
    def Copy(self, event=None):
        item = self.GetSelection()
        if item.IsOk():
            obj = self.GetPyData(item)
            data = self.GetItemXml(obj).decode("utf-8")
            if data != "" and wx.TheClipboard.Open():
                wx.TheClipboard.SetData(wx.TextDataObject(data))
                wx.TheClipboard.Close()
                eg.app.clipboardEvent.Fire()
            self.clipboardData = data


    def Paste(self, event=None):
        CmdPaste(self.document)
        

    def Clear(self, event=None):
        CmdClear(self.document, self.document.selection)
                

    def GetItemXml(self, obj):
        data = ""
        id = self.GetSelection()
        obj = self.GetPyData(id)
        buffer = StringIO()
        buffer.write('<?xml version="1.0" encoding="UTF-8" ?>')
        if obj == self.root:
            obj.GetXmlString(buffer.write, "\r\n", True)
        else:
            build_str = str(eg.buildNum)
            buffer.write('\r\n<EventGhost Version="%s">' % build_str)
            obj.GetXmlString(buffer.write, "\r\n    ", True)
            buffer.write('\r\n</EventGhost>')
        data = buffer.getvalue()
        buffer.close()
        return data
            
            
    def CanPaste(self, selectionObj):
        if not wx.TheClipboard.Open():
            return False
        try:
            dataObj = wx.CustomDataObject("DragEventItem")
            if wx.TheClipboard.GetData(dataObj):
                if selectionObj.DropTest(EventItem):
                    return True
                
            dataObj = wx.TextDataObject()
            if not wx.TheClipboard.GetData(dataObj):
                return False
            try:
                data = dataObj.GetText().encode("utf-8")
                xml_tree = ElementTree.fromstring(data)
                for childXmlNode in xml_tree:
                    targetObj = selectionObj
                    childCls = self.document.XMLTag2ClassDict[childXmlNode.tag].__bases__[0]
                    if targetObj.DropTest(childCls) in (1, 5):
                        continue
                    if targetObj.parent is None:
                        return False
                    else:
                        if targetObj.parent.DropTest(childCls) not in (1, 5):
                            return False
            except:
                return False
        finally:            
            wx.TheClipboard.Close()
        return True
        
