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
    CmdNewEvent, 
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
        
        # We need to hold a reference to our data object, instead it would
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
                    eg.actionThread.Call(
                        CmdNewEvent().Do, 
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


        
class TreeCtrl(wx.TreeCtrl):
    
    def __init__(self, parent, id=-1, document=None):
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
            )
        )
        self.root = None
        self.rootname = eg.text.General.configTree
        self.SetImageList(eg.imageList)
        self.hasFocus = False
        
        Bind = self.Bind
        Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnItemExpanding)
        Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnItemCollapsing)
        Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginLabelEdit)
        Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndLabelEdit)
        Bind(wx.EVT_SET_FOCUS, self.OnGetFocus)
        Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self.OnToolTip)
        Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivate)
        Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnBeginDrag)
        
        def OnSelectionChanged(event):
            id = event.GetItem()
            item = self.GetPyData(id)
            document.selection = item
            document.selectionEvent.Fire(item)
            event.Skip()
        Bind(wx.EVT_TREE_SEL_CHANGED, OnSelectionChanged)
        
        if eg._debug:
            Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self.OnTooTip)
        #Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnCollapsed)
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
        

    def OnExpanded(self, event):
        if self.OnItemExpandingItem == event.GetItem() and self.OnItemExpandingNum:
            self.ScrollTo(self.OnItemExpandingPos)
            self.Thaw()
            self.OnItemExpandingNum = False
        
        
    def OnCollapsed(self, event):
        id = event.GetItem()
        item = self.GetPyData(id)
        item.isExpanded = False
        
        
    def OnItemExpanding(self, event):
        eg.whoami()
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
    
    def OnItemCollapsing(self, event):
        eg.whoami()
        id = event.GetItem()
        if id == self.root.id:
            event.Veto()
            return
        self.Freeze()
        item = self.GetPyData(id)
        item.isExpanded = False
        self.Collapse(id)
        self.SetItemHasChildren(id)
        for child in item.childs:
            child.DeleteTreeItem(self)
        self.Thaw()
        

    def OnTooTip(self, event):
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
        event.Skip(True)
        
        
    def OnKillFocus(self, event):
        self.hasFocus = False
        event.Skip(True)
        
        
    def OnBeginLabelEdit(self, event):
        eg.whoami()
        obj = self.GetPyData(event.GetItem())
        if (not obj.IsEditable()) or (not self.hasFocus):
            event.Veto()
            return
        self.isInEditLabel = True
        eg.mainFrame.focusEvent.Fire("Edit")
        eg.mainFrame.UpdateViewOptions()

        
    def OnEndLabelEdit(self, event):
        self.isInEditLabel = False
        eg.mainFrame.UpdateViewOptions()
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
        
        
    def ToggleEnable(self):
        CmdToggleEnable(self.document, self.document.selection)
        
        
    def GetExpandState(self):
        eg.whoami()
        vector = []
        append = vector.append
        def _Traverse(item, i):
            if isinstance(item, ContainerItem):
                i += 1
                if item.isExpanded:
                    append(i)
                for child in item.childs:
                    i = _Traverse(child, i)
            return i
        _Traverse(self.root, -1)
        return vector
    
    
    def SetExpandState(self, vector):
        eg.whoami()
        def _Traverse(item, i):
            if isinstance(item, ContainerItem):
                i += 1
                if len(vector) and vector[0] == i:
                    item.isExpanded = True  
                    vector.pop(0)
                else:
                    item.isExpanded = False
                for child in item.childs:
                    i = _Traverse(child, i)
            return i
        
        try:
            if vector is None:
                return
            self.Freeze()
            _Traverse(self.root, -1)
        finally:
            self.Thaw()
        
        
