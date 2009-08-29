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
import xml.etree.cElementTree as ElementTree

from eg.Classes.TreeItem import (
    HINT_MOVE_INSIDE,
    HINT_MOVE_BEFORE,
    HINT_MOVE_AFTER,
)


class Paste:
    name = eg.text.MainFrame.Menu.Paste.replace("&", "")

    @eg.AssertInMainThread
    def __init__(self, document, selection):
        self.items = []
        if not wx.TheClipboard.Open():
            eg.PrintError("Can't open clipboard.")
            return
        try:
            dataObj = wx.CustomDataObject("DragEventItem")
            if wx.TheClipboard.GetData(dataObj):
                self.PasteEvent(document, selection, dataObj)
                return
            dataObj = wx.TextDataObject()
            if not wx.TheClipboard.GetData(dataObj):
                return
            result = eg.actionThread.Func(self.PasteXml)(
                document, selection, dataObj.GetText()
            )
            if result:
                document.AppendUndoHandler(self)
        finally:
            wx.TheClipboard.Close()


    def PasteEvent(self, document, selection, dataObj):
        if selection.DropTest(eg.EventItem):
            label = dataObj.GetData()
            parent = selection.parent
            pos = parent.childs.index(selection)
            eg.UndoHandler.NewEvent().Do(document, parent, label=label)


    def PasteXml(self, document, selection, clipboardData):
        xmlTree = ElementTree.fromstring(clipboardData.encode("utf-8"))
        for childXmlNode in xmlTree:
            childCls = document.XMLTag2ClassDict[childXmlNode.tag.lower()]
            before = None
            childClsBase = childCls.__bases__[1]
            insertionHint = selection.DropTest(childClsBase)
            if insertionHint & HINT_MOVE_INSIDE:
                # item will move inside
                for i in xrange(len(selection.childs)-1, -1, -1):
                    next = selection.childs[i]
                    insertionHint = next.DropTest(childClsBase)
                    if insertionHint & HINT_MOVE_AFTER:
                        break
                    before = next
            elif insertionHint & HINT_MOVE_BEFORE:
                # item will move before selection
                before = selection
                parent = selection.parent
                pos = parent.GetChildIndex(selection)
                for i in xrange(pos-1, -1, -1):
                    next = parent.childs[i]
                    insertionHint = next.DropTest(childClsBase)
                    if insertionHint != HINT_MOVE_BEFORE:
                        break
                    before = next
                selection = selection.parent
            elif insertionHint == HINT_MOVE_AFTER:
                # item will move after selection
                parent = selection.parent
                pos = parent.GetChildIndex(selection)
                for i in xrange(pos+1, len(parent.childs)):
                    next = parent.childs[i]
                    insertionHint = next.DropTest(childClsBase)
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
            document.TreeLink.StopLoad()
            return True


    @eg.AssertInActionThread
    def Undo(self, document):
        data = []
        for positionData in self.items:
            item = positionData.GetItem()
            data.append((positionData, item.GetFullXml()))
            item.Delete()
        self.items = data


    @eg.AssertInActionThread
    def Redo(self, document):
        data = []
        for positionData, xmlString in self.items:
            item = document.RestoreItem(positionData, xmlString)
            data.append(positionData)
        item.Select()
        self.items = data

