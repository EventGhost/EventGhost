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
from cStringIO import StringIO
from time import clock
from eg.WinApi.Dynamic import SendMessageTimeout



class EventDropSource(wx.DropSource):

    def __init__(self, win, text):
        wx.DropSource.__init__(self, win)
        # create our own data format and use it in a
        # custom data object
        customData = wx.CustomDataObject("DragItem")
        customData.SetData(text)

        # Now make a data object for the text and also a composite
        # data object holding both of the others.
        textData = wx.TextDataObject(text.decode("UTF-8"))

        data = wx.DataObjectComposite()
        data.Add(textData)
        data.Add(customData)

        # We need to hold a reference to our data object, instead it could
        # be garbage collected
        self.data = data

        # And finally, create the drop source and begin the drag
        # and drop operation
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
        self.dragCls = eg.EventItem
        self.dragObject = None
        # specify the type of data we will accept
        textData = wx.TextDataObject()
        self.customData = wx.CustomDataObject(wx.CustomDataFormat("DragItem"))
        self.customData.SetData("")
        compositeData = wx.DataObjectComposite()
        compositeData.Add(textData)
        compositeData.Add(self.customData)
        self.SetDataObject(compositeData)
        self.lastExpanded = None
        self.lastHighlighted = None
        self.isExternalDrag = True
        self.position = None
        self.lastDropTime = clock()
        self.lastTargetItem = None


    def OnDragOver(self, x, y, dragResult):
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
        mousePosition = tree.ScreenToClient(wx.GetMousePosition())
        targetItemId, flags = tree.HitTest(mousePosition)
        if flags & HITTEST_FLAGS:
            obj = tree.GetPyData(targetItemId)
            dragObject = self.dragObject
            tmpObj = obj
            while tmpObj is not None:
                if tmpObj == dragObject:
                    self.position = None
                    return wx.DragNone
                tmpObj = tmpObj.parent

            insertionHint = obj.DropTest(dragCls)
            if targetItemId == self.lastTargetItem:
                if (
                    self.lastDropTime + 0.6 < clock()
                    and (
                        obj.__class__ == tree.document.FolderItem
                        or insertionHint & HINT_MOVE_INSIDE
                    ) and not tree.IsExpanded(targetItemId)
                ):
                    tree.Expand(targetItemId)
            else:
                self.lastDropTime = clock()
                self.lastTargetItem = targetItemId

            if insertionHint == HINT_MOVE_BEFORE_OR_AFTER:
                targetRect = tree.GetBoundingRect(targetItemId)
                if y > targetRect.y + targetRect.height / 2:
                    insertionHint = HINT_MOVE_AFTER
                else:
                    insertionHint = HINT_MOVE_BEFORE
            elif insertionHint == HINT_MOVE_EVERYWHERE:
                targetRect = tree.GetBoundingRect(targetItemId)
                if y < targetRect.y + targetRect.height / 4:
                    insertionHint = HINT_MOVE_BEFORE
                elif y > targetRect.y + (targetRect.height / 4) * 3:
                    insertionHint = HINT_MOVE_AFTER
                else:
                    insertionHint = HINT_MOVE_INSIDE

            if insertionHint == HINT_NO_DROP:
                tree.ClearInsertMark()
                self.position = None
                dragResult = wx.DragNone
            elif insertionHint == HINT_MOVE_INSIDE:
                tree.SetItemDropHighlight(targetItemId, True)
                self.lastHighlighted = targetItemId
                self.position = (obj, 0)
                for i in xrange(len(obj.childs)-1, -1, -1):
                    child = obj.childs[i]
                    insertionHint = child.DropTest(dragCls)
                    if insertionHint & HINT_MOVE_AFTER:
                        tree.SetInsertMark(child.id, 1)
                        self.position = (obj, i+1)
                        break
                else:
                    tree.ClearInsertMark()
                dragResult = wx.DragMove
            elif insertionHint == HINT_MOVE_BEFORE:
                parent = obj.parent
                pos = parent.GetChildIndex(obj)
                for i in xrange(pos-1, -1, -1):
                    child = parent.childs[i]
                    insertionHint = child.DropTest(dragCls)
                    if insertionHint == HINT_MOVE_BEFORE:
                        targetItemId = child.id
                        pos -= 1
                tree.SetInsertMark(targetItemId, 0)
                self.position = (parent, pos)
                dragResult = wx.DragMove
            elif insertionHint == HINT_MOVE_AFTER:
                parent = obj.parent
                pos = parent.GetChildIndex(obj)
                for i in xrange(pos+1, len(parent.childs)):
                    child = parent.childs[i]
                    insertionHint = child.DropTest(dragCls)
                    if insertionHint == HINT_MOVE_AFTER:
                        targetItemId = child.id
                        pos += 1
                tree.SetInsertMark(targetItemId, 1)
                self.position = (parent, pos+1)
                dragResult = wx.DragMove
            return dragResult
        if tree.GetSelection().IsOk():
            tree.SelectItem(tree.GetSelection(), False)
            #tree.SetItemDropHighlight(tree.GetSelection(), False)
        return wx.DragNone


    @eg.LogIt
    def OnData(self, dummyX, dummyY, dragResult):
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
                if self.customData.GetDataSize() > 0:
                    label = self.customData.GetData()
                    self.customData.SetData("")
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
        return dragResult


    def OnLeave(self):
        self.treeCtrl.ClearInsertMark()


    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass



class TreeCtrl(wx.TreeCtrl):

    @eg.AssertNotMainThread
    def __init__(self, parent, document=None):
        self.document = document
        self.root = None
        self.hasFocus = False
        self.editLabelId = None
        self.expandingItemPos = None
        self.expandingItemId = None

        style = (
            wx.TR_HAS_BUTTONS |
            wx.TR_EDIT_LABELS |
            wx.TR_ROW_LINES |
            wx.CLIP_CHILDREN
        )
        wx.TreeCtrl.__init__(self, parent, style=style)

        self.SetImageList(eg.Icons.gImageList)

        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnItemExpanding)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnItemCollapsing)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginLabelEdit)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndLabelEdit)
        self.Bind(wx.EVT_SET_FOCUS, self.OnGetFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivate)
        self.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnBeginDrag)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
        self.Bind(wx.EVT_TREE_ITEM_MENU, self.OnContextMenu)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDoubleClick)
        if eg.debugLevel:
            self.Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnExpanded)

        self.dropTarget = EventDropTarget(self)
        self.SetDropTarget(self.dropTarget)
        self.hwnd = self.GetHandle()
        normalfont = self.GetFont()
        italicfont = wx.Font(
            normalfont.GetPointSize(), 
            normalfont.GetFamily(), 
            normalfont.GetStyle(), 
            normalfont.GetWeight(), 
            normalfont.GetUnderlined(),
            normalfont.GetFaceName(),
            normalfont.GetDefaultEncoding()
        )
        italicfont.SetStyle(wx.FONTSTYLE_ITALIC)
        self.normalfont = normalfont
        self.italicfont = italicfont


    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass


    def OnLeftDoubleClick(self, event):
        treeItem = self.HitTest(event.GetPosition())[0]
        if treeItem.IsOk():
            node = self.GetPyData(treeItem)
            if node.isConfigurable:
                # we have to wait till the mouse button is up again
                while wx.GetMouseState().LeftDown():
                    wx.GetApp().Yield()
                # and use CallLater and don't call Skip(), as otherwise the
                # click would go through to the newly opened frame.
                wx.CallLater(1, eg.UndoHandler.Configure().Try, self.document, node)
                return
        # if we don't call Skip() on all other situations, a expandable item
        # would not expand
        event.Skip()


    @eg.LogIt
    def OnItemActivate(self, event):
        item = event.GetItem()
        if item.IsOk():
            node = self.GetPyData(item)
            wx.CallAfter(eg.UndoHandler.Configure().Try, self.document, node)
        # if we don't call Skip(), a expandable item would not expand
        event.Skip()
        

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
        try:
            self.document.firstVisibleItem = self.GetPyData(
                self.GetFirstVisibleItem()
            )
        except:
            pass
        self.document.SetTree(None)
        self.Freeze()
        self.Unbind(wx.EVT_TREE_SEL_CHANGED)
        self.DeleteAllItems()


    @eg.LogIt
    def OnRightDown(self, event):
        self.EndEditLabel(self.GetSelection(), False)
        # seems like newer wxPython doesn't select the item on right-click
        # so we have to do it ourself
        pos = event.GetPosition()
        item = self.HitTest(pos)[0]
        if item.IsOk():
            self.SelectItem(item)


    @eg.LogIt
    def OnContextMenu(self, event):
        self.SetFocus()
        frame = self.document.frame
        frame.SetupEditMenu(frame.popupMenu)
        self.PopupMenu(frame.popupMenu, event.GetPoint())


    #@eg.LogIt
    def OnSelectionChanged(self, event):
        itemId = event.GetItem()
        item = self.GetPyData(itemId)
        self.document.selection = item
        event.Skip()


    #@eg.LogIt
    def OnItemExpanding(self, event):
        if self.expandingItemId is None:
            self.expandingItemId = event.GetItem()
            self.expandingItemPos = self.GetFirstVisibleItem()
            self.Freeze()
        try:
            itemId = event.GetItem()
            if not self.IsExpanded(itemId):
                item = self.GetPyData(itemId)
                item.isExpanded = True
                for child in item.childs:
                    child.CreateTreeItem(self, itemId)
        finally:
            pass


    #@eg.LogIt
    def OnExpanded(self, event):
        if self.expandingItemId == event.GetItem():
            self.expandingItemId = None
            self.ScrollTo(self.expandingItemPos)
            self.Thaw()


    #@eg.LogIt
    def OnItemCollapsing(self, event):
        itemId = event.GetItem()
        if itemId == self.root.id:
            event.Veto()
            return
        self.Freeze()
        item = self.GetPyData(itemId)
        item.isExpanded = False
        self.Collapse(itemId)
        self.DeleteChildren(itemId)
        self.SetItemHasChildren(itemId)
        newSelectedId = self.GetSelection()
        newSelectedItem = self.GetPyData(newSelectedId)
        document = self.document
        if newSelectedItem is not document.selection:
            document.selection = newSelectedItem
        self.Thaw()


    #@eg.LogIt
    def OnCollapsed(self, event):
        itemId = event.GetItem()
        item = self.GetPyData(itemId)
        item.isExpanded = False


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
            SendMessageTimeout(self.hwnd, 4378, after, lParam, 1, 100, None)


    def ClearInsertMark(self):
        SendMessageTimeout(self.hwnd, 4378, 0, long(0), 1, 100, None)


    def OnGetFocus(self, event):
        self.hasFocus = True
        eg.Notify("FocusChange", self)
        event.Skip(True)


    def OnKillFocus(self, event):
        self.hasFocus = False
        if self.editLabelId is None:
            eg.Notify("FocusChange", None)
        event.Skip(True)


    @eg.LogIt
    def OnBeginLabelEdit(self, event):
        item = self.GetPyData(event.GetItem())
        if (not item.isRenameable) or (not self.hasFocus):
            event.Veto()
            return
        self.editLabelId = event.GetItem()
        wx.CallAfter(eg.Notify, "FocusChange", "Edit")


    def OnEndLabelEdit(self, event):
        self.editLabelId = None
        eg.Notify("FocusChange", self)
        itemId = event.GetItem()
        item = self.GetPyData(itemId)
        newLabel = event.GetLabel()
        if not event.IsEditCancelled() and item.GetLabel() != newLabel:
            eg.UndoHandler.Rename(self.document, item, newLabel)
        event.Skip()


    def OnCmdExpandAll(self):
        self.Freeze()
        def Expand(item):
            if isinstance(item, eg.ContainerItem):
                if not item.isExpanded:
                    self.Expand(item.id)
                for child in item.childs:
                    Expand(child)
        Expand(self.root)
        self.EnsureVisible(self.GetSelection())
        self.Thaw()


    def OnCmdCollapseAll(self):
        self.Freeze()
        def Collapse(item):
            if isinstance(item, eg.ContainerItem):
                item.isExpanded = False
                for child in item.childs:
                    Collapse(child)
            item.id = None
        for child in self.root.childs:
            child.isExpanded = False
            for subchild in child.childs:
                Collapse(subchild)
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
        dragTimerId = wx.NewId()
        dragTimer = wx.Timer(self, dragTimerId)
        self.Bind(wx.EVT_TIMER, self.OnDragTimer, id=dragTimerId)
        dragTimer.Start(50)
        dropSource.DoDragDrop(wx.Drag_AllowMove)
        dragTimer.Stop()
        self.Unbind(wx.EVT_TIMER, id=dragTimerId)

        dropTarget.dragCls = eg.EventItem
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


    def OnDragTimer(self, dummyEvent):
        pos = wx.GetMousePosition()
        treeRect = self.GetScreenRect()
        frameRect = self.GetTopLevelWindow().GetScreenRect()
        if treeRect.x <= pos.x <= treeRect.GetRight():
            if pos.y < treeRect.y:
                if pos.y > frameRect.y:
                    self.ScrollLines(-1)
            elif pos.y > treeRect.GetBottom():
                if pos.y < frameRect.GetBottom():
                    self.ScrollLines(1)


    def Cut(self, dummyEvent=None):
        eg.UndoHandler.Cut(self.document, self.document.selection)


    def Copy(self, dummyEvent=None):
        item = self.GetSelection()
        if item.IsOk():
            obj = self.GetPyData(item)
            data = self.GetItemXml(obj).decode("utf-8")
            if data != "" and wx.TheClipboard.Open():
                wx.TheClipboard.SetData(wx.TextDataObject(data))
                wx.TheClipboard.Close()


    def Paste(self, dummyEvent=None):
        eg.UndoHandler.Paste(self.document)


    def Clear(self, dummyEvent=None):
        eg.UndoHandler.Clear(self.document, self.document.selection)


    def GetItemXml(self, obj):
        stream = StringIO()
        stream.write('<?xml version="1.0" encoding="UTF-8" ?>\r\n')
        if obj == self.root:
            obj.WriteXmlString(stream.write)
        else:
            buildStr = str(eg.revision)
            stream.write('<EventGhost Version="%s">\r\n' % buildStr)
            obj.WriteXmlString(stream.write, "    ")
            stream.write('</EventGhost>')
        data = stream.getvalue()
        stream.close()
        return data

