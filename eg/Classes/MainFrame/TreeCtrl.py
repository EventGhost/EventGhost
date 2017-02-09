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
from time import clock

# Local imports
import eg
from eg.Classes.TreeItem import (
    HINT_MOVE_AFTER,
    HINT_MOVE_BEFORE,
    HINT_MOVE_BEFORE_OR_AFTER,
    HINT_MOVE_EVERYWHERE,
    HINT_MOVE_INSIDE,
    HINT_NO_DROP,
)
from eg.WinApi.Dynamic import SendMessageTimeout

HITTEST_FLAG = (
    wx.TREE_HITTEST_ONITEMLABEL |
    wx.TREE_HITTEST_ONITEMICON |
    wx.TREE_HITTEST_ONITEMRIGHT
)

class DropSource(wx.DropSource):
    """
    This class represents a source for a drag and drop operation of the
    TreeCtrl.
    """
    @eg.AssertInMainThread
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
    """
    This class represents a target for a drag and drop operation of the
    TreeCtrl.
    """
    @eg.AssertInMainThread
    def __init__(self, treeCtrl):
        wx.PyDropTarget.__init__(self)
        self.treeCtrl = treeCtrl
        self.srcNode = eg.EventItem
        # specify the type of data we will accept
        textData = wx.TextDataObject()
        self.customData = wx.CustomDataObject(wx.CustomDataFormat("DragItem"))
        self.customData.SetData("")
        compositeData = wx.DataObjectComposite()
        compositeData.Add(textData)
        compositeData.Add(self.customData)
        self.SetDataObject(compositeData)
        self.lastHighlighted = None
        self.isExternalDrag = True
        self.whereToDrop = None
        self.lastDropTime = clock()
        self.lastTargetItemId = None
        timerId = wx.NewId()
        self.autoScrollTimer = wx.Timer(self.treeCtrl, timerId)
        self.treeCtrl.Bind(wx.EVT_TIMER, self.OnDragTimerEvent, id=timerId)

    @eg.AssertInMainThread
    def OnData(self, dummyX, dummyY, dragResult):
        """
        Overrides wx.DropTarget.OnData

        Called after OnDrop returns true. By default this will usually GetData
        and will return the suggested default.
        """
        self.OnLeave()
        # Called when OnDrop returns True.
        tree = self.treeCtrl
        #tree.ClearInsertMark()
        if self.isExternalDrag and self.whereToDrop is not None:
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
                    parent, pos = self.whereToDrop
                    eg.UndoHandler.NewEvent(tree.document).Do(
                        parent,
                        pos,
                        label
                    )
        # what is returned signals the source what to do
        # with the original data (move, copy, etc.)  In this
        # case we just return the suggested value given to us.
        return dragResult

    @eg.AssertInMainThread
    def OnDragOver(self, x, y, dummyDragResult):
        """
        Called when the mouse is being dragged over the drop target.
        """
        tree = self.treeCtrl
        self.whereToDrop = None

        # remove the last drop highlight if any
        if self.lastHighlighted is not None:
            tree.SetItemDropHighlight(self.lastHighlighted, False)
            self.lastHighlighted = None

        dstItemId, flags = tree.HitTest((x, y))

        if not (flags & HITTEST_FLAG):
            return wx.DragNone

        dstNode = tree.GetPyData(dstItemId)
        srcNode = self.srcNode

        # check if dstNode would get a parent of the srcNode
        dstParentNode = dstNode
        while dstParentNode is not None:
            if dstParentNode == srcNode:
                # they would, so avoid dropping the srcNode inside itself.
                return wx.DragNone
            dstParentNode = dstParentNode.parent

        insertionHint = dstNode.DropTest(srcNode)

        # expand a container, if the mouse is hold over it for some time
        if dstItemId == self.lastTargetItemId:
            if self.lastDropTime + 0.6 < clock():
                if (
                    dstNode.__class__ == dstNode.document.FolderItem or
                    insertionHint & HINT_MOVE_INSIDE
                ):
                    if not tree.IsExpanded(dstItemId):
                        tree.Expand(dstItemId)
        else:
            self.lastDropTime = clock()
            self.lastTargetItemId = dstItemId

        if insertionHint == HINT_NO_DROP:
            tree.ClearInsertMark()
            return wx.DragNone

        if insertionHint == HINT_MOVE_BEFORE_OR_AFTER:
            targetRect = tree.GetBoundingRect(dstItemId)
            if y > targetRect.y + targetRect.height / 2:
                insertionHint = HINT_MOVE_AFTER
            else:
                insertionHint = HINT_MOVE_BEFORE
        elif insertionHint == HINT_MOVE_EVERYWHERE:
            targetRect = tree.GetBoundingRect(dstItemId)
            if y < targetRect.y + targetRect.height / 4:
                insertionHint = HINT_MOVE_BEFORE
            elif y > targetRect.y + (targetRect.height / 4) * 3:
                insertionHint = HINT_MOVE_AFTER
            else:
                insertionHint = HINT_MOVE_INSIDE

        if insertionHint == HINT_MOVE_INSIDE:
            self.whereToDrop = self.OnWouldMoveInside(tree, dstNode, dstItemId)
        elif insertionHint == HINT_MOVE_BEFORE:
            self.whereToDrop = self.OnWouldMoveBefore(tree, dstNode, dstItemId)
        elif insertionHint == HINT_MOVE_AFTER:
            self.whereToDrop = self.OnWouldMoveAfter(tree, dstNode, dstItemId)
        return wx.DragMove

    @eg.AssertInMainThread
    def OnDragTimerEvent(self, dummyEvent):
        """
        Handles wx.EVT_TIMER, while a drag operation is in progress. It is
        responsible for the automatic scrolling if the mouse gets on the
        upper or lower bounds of the control.
        """
        tree = self.treeCtrl
        x, y = wx.GetMousePosition()
        treeRect = tree.GetScreenRect()
        if treeRect.x <= x <= treeRect.GetRight():
            if y < treeRect.y + 20:
                tree.ScrollLines(-1)
            elif y > treeRect.GetBottom() - 20:
                tree.ScrollLines(1)

    def OnEnter(self, dummyX, dummyY, dragResult):
        """
        Called when the mouse enters the drop target.
        """
        self.autoScrollTimer.Start(50)
        return dragResult

    @eg.AssertInMainThread
    def OnLeave(self):
        """
        Called when the mouse leaves the drop target.
        """
        self.treeCtrl.ClearInsertMark()
        self.autoScrollTimer.Stop()

    def OnWouldMoveAfter(self, tree, dstNode, dstItemId):
        """
        Handles the situation, that the dragged item would be inserted behind
        the currently highlighted item.
        """
        parent = dstNode.parent
        pos = parent.GetChildIndex(dstNode)
        for i in xrange(pos + 1, len(parent.childs)):
            child = parent.childs[i]
            if child.DropTest(self.srcNode) == HINT_MOVE_AFTER:
                dstItemId = tree.visibleNodes[child]
                pos += 1
        tree.SetInsertMark(dstItemId, 1)
        return (parent, pos + 1)

    def OnWouldMoveBefore(self, tree, dstNode, dstItemId):
        """
        Handles the situation, that the dragged item would be inserted before
        the currently highlighted item.
        """
        parent = dstNode.parent
        pos = parent.GetChildIndex(dstNode)
        for i in xrange(pos - 1, -1, -1):
            child = parent.childs[i]
            if child.DropTest(self.srcNode) == HINT_MOVE_BEFORE:
                dstItemId = tree.visibleNodes[child]
                pos -= 1
        tree.SetInsertMark(dstItemId, 0)
        return (parent, pos)

    def OnWouldMoveInside(self, tree, dstNode, dstItemId):
        """
        Handles the situation, that the dragged item would be inserted inside
        the currently highlighted item.
        """
        tree.SetItemDropHighlight(dstItemId, True)
        self.lastHighlighted = dstItemId
        whereToDrop = (dstNode, 0)
        for i in xrange(len(dstNode.childs) - 1, -1, -1):
            child = dstNode.childs[i]
            if child.DropTest(self.srcNode) & HINT_MOVE_AFTER:
                tree.SetInsertMark(tree.visibleNodes.get(child, 0), 1)
                whereToDrop = (dstNode, i + 1)
                break
        else:
            tree.ClearInsertMark()
        return whereToDrop


class EditControlProxy(object):
    def __init__(self, parent):
        self.parent = parent
        self.realControl = None

    def CanCut(self):
        return self.realControl.CanCut()

    def CanCopy(self):
        return self.realControl.CanCopy()

    #def CanPython(self):
    #    return self.realControl.CanPython()

    def CanPaste(self):
        return self.realControl.CanPaste()

    def CanDelete(self):
        start, end = self.realControl.GetSelection()
        return (start != end)

    def ClearControl(self):
        self.realControl = None

    def OnCmdCut(self):
        self.realControl.Cut()

    def OnCmdCopy(self):
        self.realControl.Copy()

    def OnCmdPython(self):
        eg.PrintNotice("DEBUG: TreeCtrl: OnCmdPython")
        #self.realControl.Copy()

    def OnCmdPaste(self):
        self.realControl.Paste()

    #def OnCmdClear(self):
    def OnCmdDelete(self):  # Pako
        start, end = self.realControl.GetSelection()
        if end - start == 0:
            end += 1
        self.realControl.Remove(start, end)
        return

    def SetControl(self):
        self.realControl = self.parent.GetEditControl()
        eg.Notify("FocusChange", self)


class TreeCtrl(wx.TreeCtrl):
    @eg.AssertInMainThread
    def __init__(self, parent, document, size=wx.DefaultSize):
        self.document = document
        self.root = None
        self.editLabelId = None
        self.insertionMark = None
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
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightClickEvent)
        self.Bind(wx.EVT_TREE_ITEM_MENU, self.OnItemMenuEvent)
        self.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnBeginDragEvent)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChangedEvent)
        self.visibleNodes = {}
        self.expandedNodes = document.expandedNodes
        self.dropTarget = DropTarget(self)
        self.SetDropTarget(self.dropTarget)
        eg.Bind("NodeAdded", self.OnNodeAdded)
        eg.Bind("NodeDeleted", self.OnNodeDeleted)
        eg.Bind("NodeChanged", self.OnNodeChanged)
        eg.Bind("NodeSelected", self.OnNodeSelected)
        eg.Bind("DocumentNewRoot", self.OnNewRoot)
        if document.root:
            self.OnNewRoot(document.root)

    @eg.AssertInMainThread
    def ClearInsertMark(self):
        SendMessageTimeout(self.hwnd, 4378, 0, long(0), 1, 100, None)
        self.insertionMark = None

    @eg.AssertInMainThread
    def CollapseAll(self):
        """
        Collapses all items in the tree.
        """
        self.Freeze()
        mainNodes = {self.root: self.GetRootItem()}
        for child in self.root.childs:
            itemId = self.visibleNodes[child]
            self.CollapseAndReset(itemId)
            mainNodes[child] = itemId
        self.visibleNodes = mainNodes
        self.expandedNodes.clear()
        self.expandedNodes.add(self.root)
        self.EnsureVisible(self.GetSelection())
        self.Thaw()

    @eg.AssertInMainThread
    def CreateRoot(self, node):
        itemId = self.AddRoot(
            node.GetLabel(),
            node.imageIndex,
            -1,
            wx.TreeItemData(node)
        )
        self.visibleNodes[node] = itemId
        self.SetItemHasChildren(itemId, True)
        self.Expand(itemId)
        return itemId

    @eg.AssertInMainThread
    def CreateTreeItem(self, node, parentId):
        itemId = self.AppendItem(
            parentId,
            node.GetLabel(),
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

    @eg.AssertInMainThread
    def CreateTreeItemAt(self, node, parentId, parentNode, pos):
        if pos == -1 or pos >= len(parentNode.childs):
            return self.CreateTreeItem(node, parentId)
        else:
            itemId = self.InsertItemBefore(
                parentId,
                pos,
                node.GetLabel(),
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

    @eg.AssertInMainThread
    @eg.LogIt
    def Destroy(self):
        self.document.firstVisibleItem = self.GetFirstVisibleNode()
        eg.Unbind("NodeAdded", self.OnNodeAdded)
        eg.Unbind("NodeDeleted", self.OnNodeDeleted)
        eg.Unbind("NodeChanged", self.OnNodeChanged)
        eg.Unbind("NodeSelected", self.OnNodeSelected)
        eg.Unbind("DocumentNewRoot", self.OnNewRoot)

    @eg.AssertInMainThread
    def EditNodeLabel(self, node):
        self.SetFocus()
        self.EditLabel(self.visibleNodes[node])

    @eg.AssertInMainThread
    def ExpandAll(self):
        """
        Expands all items in the tree.
        """
        self.Freeze()

        def Exp(item):
            child, cookie = self.GetFirstChild(item)
            while child.IsOk():
                if not self.IsExpanded(child):
                    self.Expand(child)
                Exp(child)
                child, cookie = self.GetNextChild(child, cookie)

        try:
            item = self.GetRootItem()
            Exp(item)
        finally:
            self.EnsureVisible(self.GetSelection())
            self.Thaw()

    @eg.AssertInMainThread
    def GetEditCmdState(self):
        node = self.GetSelectedNode()
        if node is None:
            return (False, False, False, False, False)
        return (
            node.CanCut(),
            node.CanCopy(),
            node.CanPython(),
            node.CanPaste(),
            node.CanDelete()
        )

    @eg.AssertInMainThread
    def GetFirstVisibleNode(self):
        """
        Returns the first currently visible node.
        """
        itemId = self.GetFirstVisibleItem()
        if not itemId.IsOk():
            return None
        return self.GetPyData(itemId)

    @eg.AssertInMainThread
    def GetSelectedNode(self):
        """
        Returns the currently selected node.
        """
        itemId = self.GetSelection()
        if not itemId.IsOk():
            return None
        return self.GetPyData(itemId)

    @eg.AssertInMainThread
    def SetInsertMark(self, treeItem, after):
        if treeItem:
            lParam = long(treeItem.m_pItem)
            if self.insertionMark == (lParam, after):
                return
            # TVM_SETINSERTMARK = 4378
            SendMessageTimeout(self.hwnd, 4378, after, lParam, 1, 100, None)
            self.insertionMark = (lParam, after)
        else:
            self.ClearInsertMark()

    @eg.AssertInMainThread
    def TraverseDelete(self, itemId):
        childId, cookie = self.GetFirstChild(itemId)
        while childId.IsOk():
            self.TraverseDelete(childId)
            node = self.GetPyData(childId)
            del self.visibleNodes[node]
            childId, cookie = self.GetNextChild(childId, cookie)

    #-------------------------------------------------------------------------
    # wx.Event Handlers
    #-------------------------------------------------------------------------

    @eg.AssertInMainThread
    @eg.LogItWithReturn
    def OnBeginDragEvent(self, event):
        """
        Handles wx.EVT_TREE_BEGIN_DRAG
        """
        srcItemId = event.GetItem()
        srcNode = self.GetPyData(srcItemId)
        if not srcNode.isMoveable:
            return
        self.SelectItem(srcItemId)
        dropTarget = self.dropTarget
        dropTarget.srcNode = srcNode
        dropTarget.isExternalDrag = False

        DropSource(self, srcNode.GetXmlString()).DoDragDrop(wx.Drag_AllowMove)

        dropTarget.srcNode = eg.EventItem
        dropTarget.isExternalDrag = True
        self.ClearInsertMark()
        if dropTarget.lastHighlighted is not None:
            self.SetItemDropHighlight(dropTarget.lastHighlighted, False)

        if dropTarget.whereToDrop is not None:
            parentNode, pos = dropTarget.whereToDrop
            eg.UndoHandler.MoveTo(self.document).Do(srcNode, parentNode, pos)

    @eg.AssertInMainThread
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

    @eg.AssertInMainThread
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
        if not event.IsEditCancelled() and node.GetLabel() != newLabel:
            eg.UndoHandler.Rename(self.document).Do(node, newLabel)
        event.Skip()

    @eg.AssertInMainThread
    def OnGetFocusEvent(self, event):
        """
        Handles wx.EVT_SET_FOCUS
        """
        eg.Notify("FocusChange", self)
        event.Skip(True)

    @eg.AssertInMainThread
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

    @eg.AssertInMainThread
    @eg.LogIt
    def OnItemCollapsingEvent(self, event):
        """
        Handles wx.EVT_TREE_ITEM_COLLAPSING
        """
        itemId = event.GetItem()
        if itemId == self.GetRootItem():
            event.Veto()
            return
        self.TraverseDelete(itemId)
        self.Unbind(wx.EVT_TREE_ITEM_COLLAPSING)
        self.Collapse(itemId)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnItemCollapsingEvent)
        self.DeleteChildren(itemId)
        self.SetItemHasChildren(itemId)
        node = self.GetPyData(itemId)
        self.expandedNodes.discard(node)

    @eg.AssertInMainThread
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

    @eg.AssertInMainThread
    def OnItemMenuEvent(self, event):
        """
        Handles wx.EVT_TREE_ITEM_MENU
        """
        self.SetFocus()
        frame = self.document.frame
        frame.SetupEditMenu(frame.popupMenu)
        self.PopupMenu(frame.popupMenu, event.GetPoint())
        event.Skip()

    @eg.AssertInMainThread
    def OnKillFocusEvent(self, event):
        """
        Handles wx.EVT_KILL_FOCUS
        """
        if self.editLabelId is None:
            eg.Notify("FocusChange", None)
        event.Skip(True)

    @eg.AssertInMainThread
    @eg.LogItWithReturn
    def OnLeftDoubleClickEvent(self, event):
        """
        Handles wx.EVT_LEFT_DCLICK
        """
        itemId = self.HitTest(event.GetPosition())[0]
        if itemId.IsOk():
            node = self.GetPyData(itemId)
            if node.isConfigurable:
                while wx.GetMouseState().LeftIsDown():
                    wx.GetApp().Yield()
                wx.CallLater(1, self.document.OnCmdConfigure, node)
        event.Skip()

    @eg.AssertInMainThread
    def OnRightClickEvent(self, event):
        """
        Handles wx.EVT_TREE_ITEM_RIGHT_CLICK
        """
        treeId = event.GetItem()
        self.SelectItem(treeId)

    @eg.AssertInMainThread
    def OnSelectionChangedEvent(self, event):
        """
        Handles wx.EVT_TREE_SEL_CHANGED
        """
        node = self.GetPyData(event.GetItem())
        self.document.selection = node
        eg.Notify("SelectionChange", node)
        event.Skip()

    #-------------------------------------------------------------------------
    # eg.Notify Handlers
    #-------------------------------------------------------------------------

    @eg.AssertInMainThread
    def OnNewRoot(self, root):
        """
        Handles eg.Notify("DocumentNewRoot")
        """
        self.Freeze()
        try:
            if self.root:
                self.DeleteAllItems()
                self.visibleNodes.clear()
            self.root = root
            rootId = self.CreateRoot(root)
            self.Expand(rootId)
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

    @eg.AssertInMainThread
    @eg.LogIt
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

    @eg.AssertInMainThread
    def OnNodeChanged(self, node):
        """
        Handles eg.Notify("NodeChanged")
        """
        if node not in self.visibleNodes:
            return
        itemId = self.visibleNodes[node]
        self.SetItemText(itemId, node.GetLabel())
        self.SetItemImage(itemId, node.imageIndex)
        self.SetItemHasChildren(itemId, bool(node.childs))
        node.SetAttributes(self, itemId)
        if node in self.expandedNodes:
            if not self.IsExpanded(itemId):
                self.Expand(itemId)
        else:
            if self.IsExpanded(itemId):
                self.Collapse(itemId)

    @eg.AssertInMainThread
    @eg.LogIt
    def OnNodeDeleted(self, (node, parent)):
        """
        Handles eg.Notify("NodeDeleted")
        """
        if parent in self.visibleNodes:
            if node in self.visibleNodes:
                itemId = self.visibleNodes.pop(node)
                self.Delete(itemId)
            if len(parent.childs) == 0:
                self.SetItemHasChildren(self.visibleNodes[parent], False)
                self.expandedNodes.discard(parent)
        self.expandedNodes.discard(node)
        selected = self.GetSelection()
        self.UnselectAll()
        self.SelectItem(selected)

    @eg.AssertInMainThread
    def OnNodeSelected(self, node):
        """
        Handles eg.Notify("NodeSelected")
        """
        if node not in self.visibleNodes:
            path = node.GetPath()
            if path is None:
                return
            parent = self.root
            for pos in path[:-1]:
                childNode = parent.childs[pos]
                if (
                    childNode not in self.visibleNodes and
                    parent not in self.expandedNodes
                ):
                        self.Expand(self.visibleNodes[parent])
                parent = childNode
            if parent not in self. expandedNodes:
                self.Expand(self.visibleNodes[parent])
        self.SelectItem(self.visibleNodes[node])
