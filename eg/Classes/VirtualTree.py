# This file is part of EventGhost.
# Copyright (C) 2008 Lars-Peter Voss <bitmonster@eventghost.org>
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
# $LastChangedDate: 2008-11-26 16:07:19 +0100 (Mi, 26 Nov 2008) $
# $LastChangedRevision: 589 $
# $LastChangedBy: bitmonster $

from time import clock

import wx
import eg
from eg.WinApi.Dynamic import SendMessageTimeout
from eg.Classes.TreeItem import (
    HINT_NO_DROP, 
    HINT_MOVE_INSIDE, 
    HINT_MOVE_BEFORE, 
    HINT_MOVE_AFTER,
    HINT_MOVE_BEFORE_OR_AFTER, 
    HINT_MOVE_EVERYWHERE
)

HITTEST_FLAGS = (
    wx.TREE_HITTEST_ONITEMLABEL |
    wx.TREE_HITTEST_ONITEMICON |
    wx.TREE_HITTEST_ONITEMRIGHT
)


class DropSource(wx.DropSource):

    @eg.AssertNotMainThread
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



class DropTarget(wx.PyDropTarget):

    @eg.AssertNotMainThread
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


    @eg.AssertNotMainThread
    def OnDragOver(self, dummyX, y, dragResult):
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
            targetNode = tree.GetPyData(targetItemId)
            dragObject = self.dragObject
            tmpObj = targetNode
            while tmpObj is not None:
                if tmpObj == dragObject:
                    self.position = None
                    return wx.DragNone
                tmpObj = tmpObj.parent

            insertionHint = targetNode.DropTest(dragCls)
            if targetItemId == self.lastTargetItem:
                if self.lastDropTime + 0.6 < clock():
                    if (
                        targetNode.__class__ == targetNode.document.FolderItem
                        or insertionHint & HINT_MOVE_INSIDE
                    ):
                        if not tree.IsExpanded(targetItemId):
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
                self.position = (targetNode, 0)
                for i in xrange(len(targetNode.childs)-1, -1, -1):
                    child = targetNode.childs[i]
                    insertionHint = child.DropTest(dragCls)
                    if (
                        insertionHint in (
                            HINT_MOVE_AFTER,
                            HINT_MOVE_BEFORE_OR_AFTER,
                            HINT_MOVE_EVERYWHERE
                        )
                    ):
                        tree.SetInsertMark(tree.visibleNodes.get(child, 0), 1)
                        self.position = (targetNode, i+1)
                        break
                else:
                    tree.ClearInsertMark()
                dragResult = wx.DragMove
            elif insertionHint == HINT_MOVE_BEFORE:
                parent = targetNode.parent
                pos = parent.GetChildIndex(targetNode)
                for i in xrange(pos-1, -1, -1):
                    child = parent.childs[i]
                    insertionHint = child.DropTest(dragCls)
                    if insertionHint == HINT_MOVE_BEFORE:
                        targetItemId = tree.visibleNodes[child]
                        pos -= 1
                tree.SetInsertMark(targetItemId, 0)
                self.position = (parent, pos)
                dragResult = wx.DragMove
            elif insertionHint == HINT_MOVE_AFTER:
                parent = targetNode.parent
                pos = parent.GetChildIndex(targetNode)
                for i in xrange(pos+1, len(parent.childs)):
                    child = parent.childs[i]
                    insertionHint = child.DropTest(dragCls)
                    if insertionHint == HINT_MOVE_AFTER:
                        targetItemId = tree.visibleNodes[child]
                        pos += 1
                tree.SetInsertMark(targetItemId, 1)
                self.position = (parent, pos+1)
                dragResult = wx.DragMove
            return dragResult
        #if tree.GetSelection().IsOk():
            #tree.SelectItem(tree.GetSelection(), False)
            #tree.SetItemDropHighlight(tree.GetSelection(), False)
        return wx.DragNone


    @eg.AssertNotMainThread
    def OnData(self, dummyX, dummyY, dragResult):
        print "on data"
        self.OnLeave()
        # Called when OnDrop returns True.
        tree = self.treeCtrl
        #tree.ClearInsertMark()
        if self.isExternalDrag and self.position is not None:
            # We need to get the data and do something with it.
            if self.GetData():
                # copy the data from the drag source to our data object
                #if tree.GetSelection().IsOk():
                #    tree.SelectItem(tree.GetSelection(), False)
                if self.lastHighlighted is not None:
                    tree.SetItemDropHighlight(self.lastHighlighted, False)
                if self.customData.GetDataSize() > 0:
                    label = self.customData.GetData()
                    self.customData.SetData("")
                    parent, pos = self.position
                    eg.UndoHandler.NewEvent().Do(
                        tree.document,
                        parent,
                        pos,
                        label
                    )
        # what is returned signals the source what to do
        # with the original data (move, copy, etc.)  In this
        # case we just return the suggested value given to us.
        return dragResult


    def OnEnter(self, x, y, dragResult):
        print "on enter"
        self.dragTimerId = wx.NewId()
        self.dragTimer = wx.Timer(self.treeCtrl, self.dragTimerId)
        self.treeCtrl.Bind(wx.EVT_TIMER, self.OnDragTimerEvent, id=self.dragTimerId)
        self.dragTimer.Start(50)
        return dragResult


    @eg.AssertNotMainThread
    def OnLeave(self):
        print "on leave"
        self.treeCtrl.ClearInsertMark()
        self.dragTimer.Stop()
        self.treeCtrl.Unbind(wx.EVT_TIMER, id=self.dragTimerId)


    @eg.AssertNotMainThread
    def OnDragTimerEvent(self, dummyEvent):
        """
        Handles wx.EVT_TIMER, while a drag operation is in progress
        """
        tree = self.treeCtrl
        x, y = wx.GetMousePosition()
        treeRect = tree.GetScreenRect()
        if treeRect.x <= x <= treeRect.GetRight():
            if y < treeRect.y + 20:
                tree.ScrollLines(-1)
            elif y > treeRect.GetBottom() - 20:
                tree.ScrollLines(1)



class EditControlProxy(object):
    
    def __init__(self, parent):
        self.parent = parent
        self.realControl = None
        
    
    def SetControl(self):
        self.realControl = self.parent.GetEditControl()
        eg.Notify("FocusChange", self)
        
    
    def ClearControl(self):
        self.realControl = None

    
    def OnCmdCut(self):
        self.realControl.Cut()
        
    
    def OnCmdCopy(self):
        self.realControl.Copy()
        
    
    def OnCmdPaste(self):
        self.realControl.Paste()


    def OnCmdClear(self):
        start, end = self.realControl.GetSelection()
        if end - start == 0:
            end += 1
        self.realControl.Remove(start, end)
        return


    def CanCut(self):
        return self.realControl.CanCut()
    
    
    def CanCopy(self):
        return self.realControl.CanCopy()


    def CanPaste(self):
        return self.realControl.CanPaste()
        
    
    def CanDelete(self):
        start, end = self.realControl.GetSelection()
        return (start != end)

        

class VirtualTree(wx.TreeCtrl):
    
    @eg.AssertNotMainThread
    def __init__(self, parent, document, size=wx.DefaultSize):
        self.document = document
        self.root = None
        self.editLabelId = None
        self.editControl = EditControlProxy(self)
        style = (
            wx.TR_HAS_BUTTONS |
            wx.TR_EDIT_LABELS |
            wx.TR_ROW_LINES |
            wx.CLIP_CHILDREN
        )
        wx.TreeCtrl.__init__(self, parent, size=size, style=style)
        self.SetImageList(eg.Icons.gImageList)
        self.hwnd = self.GetHandle()
        self.normalfont = self.GetFont()
        self.italicfont = self.GetFont()
        self.italicfont.SetStyle(wx.FONTSTYLE_ITALIC)
        self.Bind(wx.EVT_SET_FOCUS, self.OnGetFocusEvent)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocusEvent)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnItemExpandingEvent)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnItemCollapsingEvent)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginLabelEditEvent)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndLabelEditEvent)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivateEvent)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDoubleClickEvent)
        self.Bind(wx.EVT_TREE_ITEM_MENU, self.OnItemMenuEvent)
        self.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnBeginDragEvent)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChangedEvent)
        self.visibleNodes = {}
        self.expandedNodes = document.expandedNodes
        self.rootId = None
        self.dropTarget = DropTarget(self)
        self.SetDropTarget(self.dropTarget)
        eg.Bind("NodeAdded", self.OnNodeAdded)
        eg.Bind("NodeDeleted", self.OnNodeDeleted)
        eg.Bind("NodeChanged", self.OnNodeChanged)
        eg.Bind("NodeSelected", self.OnNodeSelected)
        eg.Bind("NodeMoveBegin", self.OnNodeMoveBegin)
        eg.Bind("NodeMoveEnd", self.OnNodeMoveEnd)
        root = eg.Bind("DocumentNewRoot", self.OnNewRoot)
        if root:
            self.OnNewRoot(root)


    @eg.AssertNotMainThread
    @eg.LogIt
    def Destroy(self):
        self.document.firstVisibleItem = self.GetFirstVisibleNode()
        eg.Unbind("NodeAdded", self.OnNodeAdded)
        eg.Unbind("NodeDeleted", self.OnNodeDeleted)
        eg.Unbind("NodeChanged", self.OnNodeChanged)
        eg.Unbind("NodeSelected", self.OnNodeSelected)
        eg.Unbind("NodeMoveBegin", self.OnNodeMoveBegin)
        eg.Unbind("NodeMoveEnd", self.OnNodeMoveEnd)
        eg.Unbind("DocumentNewRoot", self.OnNewRoot)
        
    
    @eg.AssertNotMainThread
    def SetInsertMark(self, treeItem, after):
        # TVM_SETINSERTMARK = 4378
        if treeItem:
            lParam = long(treeItem.m_pItem)
            SendMessageTimeout(self.hwnd, 4378, after, lParam, 1, 100, None)


    @eg.AssertNotMainThread
    def ClearInsertMark(self):
        SendMessageTimeout(self.hwnd, 4378, 0, long(0), 1, 100, None)


    @eg.AssertNotMainThread
    def CreateRoot(self, node):
        itemId = self.AddRoot(
            node.label, 
            node.imageIndex,
            node.selectedImageIndex, 
            wx.TreeItemData(node)
        )
        self.visibleNodes[node] = itemId
        self.SetItemHasChildren(itemId, True)
        self.Expand(itemId)
        return itemId
        
    
    @eg.AssertNotMainThread
    def CreateTreeItem(self, node, parentId):
        itemId = self.AppendItem(
            parentId, 
            node.label, 
            node.imageIndex,
            -1,
            wx.TreeItemData(node)
        )
        node.SetAttributes(self, itemId)
        self.visibleNodes[node] = itemId
        if node.childs:
            self.SetItemHasChildren(itemId, True)
        if node in self.expandedNodes:
            self.Expand(itemId)
        return itemId
        
        
    @eg.AssertNotMainThread
    def CreateTreeItemAt(self, node, parentId, parentNode, pos):
        if pos == -1 or pos >= len(parentNode.childs):
            return self.CreateTreeItem(node, parentId)
        else:
            itemId = self.InsertItemBefore(
                parentId,
                pos,
                node.label,
                node.imageIndex,
                -1,
                wx.TreeItemData(node)
            )
            node.SetAttributes(self, itemId)
            self.visibleNodes[node] = itemId
            if node.childs:
                self.SetItemHasChildren(itemId, True)
            if node in self.expandedNodes:
                self.Expand(itemId)
            return itemId

        
    @eg.AssertNotMainThread
    def TraverseDelete(self, itemId):
        childId, cookie = self.GetFirstChild(itemId)
        while childId.IsOk():
            self.TraverseDelete(childId)
            node = self.GetPyData(childId)
            del self.visibleNodes[node]
            childId, cookie = self.GetNextChild(childId, cookie)


    @eg.AssertNotMainThread
    def GetTopLevelWindow(self):
        result = self
        while True:
            parent = result.GetParent()
            if parent is None:
                return result
            result = parent


    @eg.AssertNotMainThread
    def GetSelectedNode(self):
        """
        Returns the currently selected node.
        """
        itemId = self.GetSelection()
        if not itemId.IsOk():
            return None
        return self.GetPyData(itemId)


    @eg.AssertNotMainThread
    def GetFirstVisibleNode(self):
        """
        Returns the first currently visible node.
        """
        itemId = self.GetFirstVisibleItem()
        if not itemId.IsOk():
            return None
        return self.GetPyData(itemId)


    @eg.AssertNotMainThread
    def EditNodeLabel(self, node):
        self.EditLabel(self.visibleNodes[node])


    #-------------------------------------------------------------------------
    # wx.Event Handlers
    #-------------------------------------------------------------------------

    
    @eg.AssertNotMainThread
    def OnGetFocusEvent(self, event):
        """ 
        Handles wx.EVT_SET_FOCUS 
        """
        eg.Notify("FocusChange", self)
        event.Skip(True)


    @eg.AssertNotMainThread
    def OnKillFocusEvent(self, event):
        """
        Handles wx.EVT_KILL_FOCUS
        """
        if self.editLabelId is None:
            eg.Notify("FocusChange", None)
        event.Skip(True)


    def OnSelectionChangedEvent(self, event):
        """
        Handles wx.EVT_TREE_SEL_CHANGED
        """
        node = self.GetPyData(event.GetItem())
        eg.Notify("SelectionChange", node)
        event.Skip()

    
    @eg.AssertNotMainThread
    def OnItemExpandingEvent(self, event):
        """
        Handles wx.EVT_TREE_ITEM_EXPANDING
        """
        itemId = event.GetItem()
        self.ClearInsertMark()
        if not self.IsExpanded(itemId):
            node = self.GetPyData(itemId)
            self.expandedNodes.add(node)
            for subNode in node.childs:
                self.CreateTreeItem(subNode, itemId)
    
    
    @eg.AssertNotMainThread
    @eg.LogIt
    def OnItemCollapsingEvent(self, event):
        """
        Handles wx.EVT_TREE_ITEM_COLLAPSING
        """
        itemId = event.GetItem()
        self.TraverseDelete(itemId)
        self.Collapse(itemId)
        self.DeleteChildren(itemId)
        self.SetItemHasChildren(itemId)
        node = self.GetPyData(itemId)
        self.expandedNodes.discard(node)
        

    @eg.AssertNotMainThread
    @eg.LogIt
    def OnBeginLabelEditEvent(self, event):
        """
        Handles wx.EVT_TREE_BEGIN_LABEL_EDIT
        """
        node = self.GetPyData(event.GetItem())
        if not node.isRenameable or self.FindFocus() is not self:
            event.Veto()
            return
        self.editLabelId = event.GetItem()
        # we have to delay the notification, because the listener wants to 
        # get the EditControl and it doesn't yet exist
        wx.CallAfter(self.editControl.SetControl)
        event.Skip()
        
        
    @eg.AssertNotMainThread
    @eg.LogIt
    def OnEndLabelEditEvent(self, event):
        """
        Handles wx.EVT_TREE_END_LABEL_EDIT
        """
        self.editLabelId = None
        eg.Notify("FocusChange", self)
        itemId = event.GetItem()
        node = self.GetPyData(itemId)
        newLabel = event.GetLabel()
        if not event.IsEditCancelled() and node.label != newLabel:
            eg.UndoHandler.Rename(self.document, node, newLabel)
        event.Skip()
        
        
    @eg.AssertNotMainThread
    @eg.LogIt
    def OnItemActivateEvent(self, event):
        """
        Handles wx.EVT_TREE_ITEM_ACTIVATED
        """
        itemId = event.GetItem()
        if itemId.IsOk():
            node = self.GetPyData(itemId)
            if node.isConfigurable:
                wx.CallAfter(self.document.OnCmdConfigure, node)
        event.Skip()

        
    @eg.AssertNotMainThread
    @eg.LogItWithReturn
    def OnLeftDoubleClickEvent(self, event):
        """
        Handles wx.EVT_LEFT_DCLICK
        """
        itemId = self.HitTest(event.GetPosition())[0]
        if itemId.IsOk():
            node = self.GetPyData(itemId)
            if node.isConfigurable:
                while wx.GetMouseState().LeftDown():
                    wx.GetApp().Yield()
                wx.CallLater(1, self.document.OnCmdConfigure, node)
        event.Skip()
    
    
    @eg.AssertNotMainThread
    def OnItemMenuEvent(self, event):
        """
        Handles wx.EVT_TREE_ITEM_MENU
        """
        self.SetFocus()
        frame = eg.document.frame
        frame.SetupEditMenu(frame.popupMenu)
        self.PopupMenu(frame.popupMenu, event.GetPoint())
        event.Skip()

    
    @eg.AssertNotMainThread
    @eg.LogItWithReturn
    def OnBeginDragEvent(self, event):
        """
        Handles wx.EVT_TREE_BEGIN_DRAG
        """
        dragId = event.GetItem()
        dragNode = self.GetPyData(dragId)
        if not dragNode.canMove:
            return
        self.SelectItem(dragId)
        dropSource = DropSource(self, dragNode.GetXmlString())
        dropTarget = self.dropTarget
        dropTarget.dragCls = dragNode.__class__.__bases__[1]
        dropTarget.dragObject = dragNode
        dropTarget.isExternalDrag = False
        
        dropSource.DoDragDrop(wx.Drag_AllowMove)

        dropTarget.dragCls = eg.EventItem
        dropTarget.dragObject = None
        dropTarget.isExternalDrag = True
        insertionMarkPos = dropTarget.position
        #self.SelectItem(dragId, False)
        self.ClearInsertMark()
        if dropTarget.lastHighlighted is not None:
            self.SetItemDropHighlight(dropTarget.lastHighlighted, False)

        if insertionMarkPos is not None:
            parentNode, pos = insertionMarkPos
            eg.UndoHandler.MoveTo(eg.document, dragNode, parentNode, pos)


    #-------------------------------------------------------------------------
    # eg.Notify Handlers
    #-------------------------------------------------------------------------

    
    @eg.AssertNotMainThread
    def OnNewRoot(self, root):
        self.Freeze()
        if self.root:
            self.DeleteAllItems()
            self.visibleNodes.clear()
        try:
            self.root = root
            self.rootId = self.CreateRoot(root)
            self.Expand(self.rootId)
            selectedNode = self.document.selection
            if selectedNode in self.visibleNodes:
                itemId = self.visibleNodes[selectedNode]
                self.SelectItem(itemId)
            firstVisibleItem = self.document.firstVisibleItem
            if firstVisibleItem:
                if firstVisibleItem in self.visibleNodes:
                    itemId = self.visibleNodes[firstVisibleItem]
                    self.ScrollTo(itemId)
        finally:
            self.Thaw()
    
    
    @eg.AssertNotMainThread
    def OnNodeAdded(self, (node, pos)):
        """
        Handles eg.Notify("NodeAdded")
        """
        parentNode = node.parent
        if parentNode in self.visibleNodes:
            parentId = self.visibleNodes[parentNode]
            if len(parentNode.childs):
                self.SetItemHasChildren(parentId)
            if self.IsExpanded(parentId):
                self.CreateTreeItemAt(
                    node, 
                    parentId, 
                    parentNode, 
                    pos
                )
            elif parentNode in self.expandedNodes:
                self.Expand(parentId)
        
        
    @eg.AssertNotMainThread
    def OnNodeDeleted(self, node):
        """
        Handles eg.Notify("NodeDeleted")
        """
        parent = node.parent
        if parent in self.visibleNodes:
            if node in self.visibleNodes:
                itemId = self.visibleNodes.pop(node)
                self.Delete(itemId)
            if len(parent.childs) == 0:
                self.SetItemHasChildren(self.visibleNodes[parent], False)
                self.expandedNodes.discard(parent)
        self.expandedNodes.discard(node)
        
        
    @eg.AssertNotMainThread
    def OnNodeChanged(self, node):
        """
        Handles eg.Notify("NodeChanged")
        """
        if node not in self.visibleNodes:
            return
        itemId = self.visibleNodes[node]
        self.SetItemText(itemId, node.label)
        self.SetItemImage(itemId, node.imageIndex)
        self.SetItemHasChildren(itemId, bool(node.childs))
        node.SetAttributes(self, itemId)


    @eg.AssertNotMainThread
    def OnNodeSelected(self, node):
        """
        Handles eg.Notify("NodeSelected")
        """
        if node not in self.visibleNodes:
            path = node.GetPath()
            parent = self.root
            for pos in path[:-1]:
                parent = parent.childs[pos]
                self.Expand(self.visibleNodes[parent])
        self.SelectItem(self.visibleNodes[node])

    
    def OnNodeMoveBegin(self, node):
        self.Freeze()
        
    
    def OnNodeMoveEnd(self, node):
        self.Thaw()
        
    
    #-------------------------------------------------------------------------
    # Command Handlers
    #-------------------------------------------------------------------------

    
    @eg.AssertNotMainThread
    def OnCmdCut(self):
        eg.UndoHandler.Cut(self.document, self.GetSelectedNode())


    @eg.AssertNotMainThread
    def OnCmdCopy(self):
        self.GetSelectedNode().OnCmdCopy()


    @eg.AssertNotMainThread
    def OnCmdPaste(self):
        eg.UndoHandler.Paste(self.document, self.GetSelectedNode())


    @eg.AssertNotMainThread
    def OnCmdDelete(self):
        eg.UndoHandler.Clear(self.document, self.GetSelectedNode())


    @eg.AssertNotMainThread
    def OnCmdExpandAll(self):
        self.Freeze()
        self.ExpandAll()
        self.EnsureVisible(self.GetSelection())
        self.Thaw()


    @eg.AssertNotMainThread
    def OnCmdCollapseAll(self):
        self.Freeze()
        mainNodes = {self.root: self.rootId}
        for child in self.root.childs:
            itemId = self.visibleNodes[child]
            self.CollapseAndReset(itemId)
            mainNodes[child] = itemId
        self.visibleNodes = mainNodes
        self.expandedNodes.clear()
        self.expandedNodes.add(self.root)
        self.EnsureVisible(self.GetSelection())
        self.Thaw()


    def GetEditCmdState(self):
        node = self.GetSelectedNode()
        if node is None:
            return (False, False, False, False)
        return (
            node.CanCut(), 
            node.CanCopy(), 
            node.CanPaste(), 
            node.CanDelete()
        )
        
        
    def DisplayError(self, ident):
        frame = self.GetTopLevelWindow()
        frame.DisplayError(getattr(eg.text.MainFrame.Messages, ident))
        
    
    def OnCmdRename(self):
        selection = self.GetSelectedNode()
        if not selection.isRenameable:
            self.DisplayError("cantRename")
        else:
            self.SetFocus()
            self.EditLabel(self.GetSelection())

    
    def OnCmdConfigure(self):
        selection = self.GetSelectedNode()
        if not selection.isConfigurable:
            self.DisplayError("cantConfigure")
        else:
            self.document.OnCmdConfigure(selection)


    def OnCmdExecute(self):
        selection = self.GetSelectedNode()
        if not selection.isExecutable:
            self.DisplayError("cantExecute")
        else:
            self.document.ExecuteNode(selection).SetShouldEnd()


    def OnCmdToggleEnable(self):
        selection = self.GetSelectedNode()
        if not selection.isDeactivatable:
            self.DisplayError("cantDisable")
        else:
            self.document.OnCmdToggleEnable(selection)


