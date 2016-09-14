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
import xml.etree.cElementTree as ElementTree

# Local imports
import eg
from eg.Classes.TreeItem import (
    HINT_MOVE_AFTER,
    HINT_MOVE_BEFORE,
    HINT_MOVE_INSIDE,
)
from eg.Classes.UndoHandler import UndoHandlerBase

class Paste(UndoHandlerBase):
    name = eg.text.MainFrame.Menu.Paste.replace("&", "")

    @eg.AssertInMainThread
    def Do(self, selection):
        self.items = []
        if not wx.TheClipboard.Open():
            eg.PrintError("Can't open clipboard.")
            return
        try:
            dataObj = wx.CustomDataObject("DragEventItem")
            if wx.TheClipboard.GetData(dataObj):
                self.PasteEvent(selection, dataObj)
                return
            dataObj = wx.TextDataObject()
            if not wx.TheClipboard.GetData(dataObj):
                return
            result = eg.actionThread.Func(self.PasteXml)(
                selection,
                dataObj.GetText()
            )
            if result:
                self.document.AppendUndoHandler(self)
        finally:
            wx.TheClipboard.Close()

    def PasteEvent(self, selection, dataObj):
        if selection.DropTest(eg.EventItem):
            label = dataObj.GetData()
            parent = selection.parent
            #pos = parent.childs.index(selection)
            eg.UndoHandler.NewEvent(self.document).Do(parent, label=label)

    def PasteXml(self, selection, clipboardData):
        xmlTree = ElementTree.fromstring(clipboardData.encode("utf-8"))
        for childXmlNode in xmlTree:
            childCls = self.document.XMLTag2ClassDict[childXmlNode.tag.lower()]
            before = None
            insertionHint = selection.DropTest(childCls)
            if insertionHint & HINT_MOVE_INSIDE:
                # item will move inside
                for i in xrange(len(selection.childs) - 1, -1, -1):
                    next = selection.childs[i]
                    insertionHint = next.DropTest(childCls)
                    if insertionHint & HINT_MOVE_AFTER:
                        break
                    before = next
            elif insertionHint & HINT_MOVE_BEFORE:
                # item will move before selection
                before = selection
                parent = selection.parent
                pos = parent.GetChildIndex(selection)
                for i in xrange(pos - 1, -1, -1):
                    next = parent.childs[i]
                    insertionHint = next.DropTest(childCls)
                    if insertionHint != HINT_MOVE_BEFORE:
                        break
                    before = next
                selection = selection.parent
            elif insertionHint == HINT_MOVE_AFTER:
                # item will move after selection
                parent = selection.parent
                pos = parent.GetChildIndex(selection)
                for i in xrange(pos + 1, len(parent.childs)):
                    next = parent.childs[i]
                    insertionHint = next.DropTest(childCls)
                    if insertionHint != HINT_MOVE_AFTER:
                        before = next
                        break
                selection = selection.parent
            else:
                eg.PrintError("Unexpected item in paste.")
                return
            if before is None:
                pos = -1
            else:
                pos = before.parent.childs.index(before)
                if pos + 1 == len(before.parent.childs):
                    pos = -1
            newNode = childCls(selection, childXmlNode)
            newNode.RestoreState()
            selection.AddChild(newNode, pos)
            self.items.append(eg.TreePosition(newNode))
        if len(self.items):
            newNode.Select()
            self.document.TreeLink.StopLoad()
            return True

    @eg.AssertInActionThread
    def Redo(self):
        data = []
        for treePosition, xmlString in self.items:
            item = self.document.RestoreItem(treePosition, xmlString)
            data.append(treePosition)
        item.Select()
        self.items = data

    @eg.AssertInActionThread
    def Undo(self):
        data = []
        for treePosition in self.items:
            item = treePosition.GetItem()
            data.append((treePosition, item.GetFullXml()))
            item.Delete()
        self.items = data
