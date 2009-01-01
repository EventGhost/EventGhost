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
import xml.etree.cElementTree as ElementTree
from functools import partial


class Paste:
    name = eg.text.MainFrame.Menu.Paste.replace("&", "")
    
    def __init__(self, document):
        tree = document.tree
        self.items = []
        selectionObj = tree.GetPyData(tree.GetSelection())
        if not wx.TheClipboard.Open():
            return
        try:
            dataObj = wx.CustomDataObject("DragEventItem")
            if wx.TheClipboard.GetData(dataObj):
                selectedObj = tree.GetPyData(tree.GetSelection())
                if selectedObj.DropTest(eg.EventItem):
                    label = dataObj.GetData()
                    parent = selectionObj.parent
                    pos = parent.childs.index(selectionObj)
                    eg.UndoHandler.NewEvent().Do(tree.document, label)
                return
            dataObj = wx.TextDataObject()
            if not wx.TheClipboard.GetData(dataObj):
                return
            clipboardData = dataObj.GetText()
            xmlTree = ElementTree.fromstring(clipboardData.encode("utf-8"))
            for childXmlNode in xmlTree:
                targetObj = selectionObj
                childCls = document.XMLTag2ClassDict[childXmlNode.tag]
                before = None
                childClsBase = childCls.__bases__[1]
                insertionHint = targetObj.DropTest(childClsBase)
                if insertionHint in (1, 5): 
                    # item will move inside
                    for i in xrange(len(targetObj.childs)-1, -1, -1):
                        next = targetObj.childs[i]
                        insertionHint = next.DropTest(childClsBase)
                        if insertionHint in (3, 4, 5):
                            break
                        before = next
                elif insertionHint in (2, 4): 
                    # item will move before selection
                    before = targetObj
                    parent = targetObj.parent
                    pos = parent.GetChildIndex(targetObj)
                    for i in xrange(pos-1, -1, -1):
                        next = parent.childs[i]
                        insertionHint = next.DropTest(childClsBase)
                        if insertionHint != 2:
                            break
                        before = next
                    targetObj = targetObj.parent
                elif insertionHint == 3: #in (3, 4):
                    # item will move after selection
                    parent = targetObj.parent
                    pos = parent.GetChildIndex(targetObj)
                    for i in xrange(pos+1, len(parent.childs)):
                        next = parent.childs[i]
                        insertionHint = next.DropTest(childClsBase)
                        if insertionHint != 3:
                            before = next
                            break
                    targetObj = targetObj.parent
                else:
                    eg.PrintError("Unexpected item in paste.")
                    return
                if before is None:
                    pos = -1
                else:
                    pos = before.parent.childs.index(before)
                    if pos + 1 == len(before.parent.childs):
                        pos = -1
                obj = eg.actionThread.CallWait(
                    partial(childCls, targetObj, childXmlNode)
                )
                obj.RestoreState()
                targetObj.AddChild(obj, pos)
                self.items.append(obj.GetPositionData())
            if len(self.items):
                obj.Select()
                document.TreeLink.StopLoad()
                document.AppendUndoHandler(self)
        finally:
            wx.TheClipboard.Close()                        

            
    def Undo(self, document):
        data = []
        for positionData in self.items:
            item = positionData.GetItem()
            data.append((positionData, item.GetFullXml()))
            item.Delete()
        self.items = data
        
        
    def Redo(self, document):
        data = []
        for positionData, xmlString in self.items:
            item = document.RestoreItem(positionData, xmlString)
            data.append(positionData)
        item.Select()
        self.items = data
        
        