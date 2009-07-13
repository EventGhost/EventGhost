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
from functools import partial
from xml.sax.saxutils import quoteattr, escape
from cStringIO import StringIO
import xml.etree.cElementTree as ElementTree

from TreeLink import TreeLink

HINT_NO_DROP = 0              # item cannot be dropped on it
HINT_MOVE_INSIDE = 1          # item would be dropped inside
HINT_MOVE_BEFORE = 2          # item would move before
HINT_MOVE_AFTER = 4           # item would move after
HINT_MOVE_BEFORE_OR_AFTER = 6 # item can be inserted before or after
HINT_MOVE_EVERYWHERE = 7      # item can be inserted before or after or dropped
                              # inside



class TreeItem(object):
    # name
    # parent
    # isEnabled
    # xmlId

    xmlTag = "Item"
    dependants = None
    childs = ()
    isDeactivatable = True
    isConfigurable = False
    isRenameable = True
    isExecutable = False
    # we need this so weakrefs can find out if the item actually lives
    isDeleted = False

    document = None
    root = None
    icon = None

    @classmethod
    #@eg.AssertNotMainThread
    def Create(cls, parent, pos=-1, text="", **kwargs):
        node = ElementTree.Element(cls.xmlTag)
        node.text = text
        for key, value in kwargs.items():
            node.attrib[key] = value
        self = eg.actionThread.CallWait(partial(cls, parent, node))
        parent.AddChild(self, pos)
        return self


    #@eg.AssertNotActionThread
    def __init__(self, parent, node):
        self.parent = parent
        # convert all attribute names to lowercase
        node.attrib = dict([(k.lower(), v) for k, v in node.attrib.items()])
        get = node.attrib.get
        self.name = get("name", "")
        if type(self.name) == type(""):
            self.name = unicode(self.name, "utf8")
        self.isEnabled = not get('enabled') == "False"
        self.xmlId = TreeLink.NewXmlId(int(get('id', -1)), self)


    def RestoreState(self):
        pass


    def GetData(self):
        """
        This method returns the needed data to construct its XML representation.

        The return values should be:
            1. a list of (name, value) tuples of the attributes
            2. the text of the node
        """
        attr = []
        if self.name:
            attr.append(('Name', self.name))
        if self.dependants or TreeLink.inUndo:
            attr.append(('id', self.xmlId))
        if not self.isEnabled:
            attr.append(('Enabled', 'False'))
        return attr, None


    def GetTypeName(self):
        raise NotImplementedError


    def GetDescription(self):
        raise NotImplementedError


    def WriteXmlString(self, streamWriter, indent=""):
        attr, text = self.GetData()
        attribStrs = [
            ' %s=%s' % (k, quoteattr(unicode(v)).encode("UTF-8"))
            for k, v in attr
        ]
        streamWriter("%s<%s%s" % (indent, self.xmlTag, "".join(attribStrs)))
        if not text and len(self.childs) == 0:
            streamWriter(" />\r\n")
        else:
            streamWriter(">\r\n")
            newIndent = indent + "    "
            if text is not None:
                streamWriter(newIndent + escape(text).encode("UTF-8"))
                streamWriter("\r\n")
            for child in self.childs:
                child.WriteXmlString(streamWriter, newIndent)
            streamWriter(indent + "</%s>\r\n" % self.xmlTag)


    def GetFullXml(self):
        TreeLink.StartUndo()
        output = StringIO()
        self.WriteXmlString(output.write)
        data = output.getvalue()
        output.close()
        TreeLink.StopUndo()
        return data


    def GetXmlString(self):
        stream = StringIO()
        stream.write('<?xml version="1.0" encoding="UTF-8" ?>\r\n')
        if isinstance(self, eg.RootItem):
            self.WriteXmlString(stream.write)
        else:
            stream.write('<EventGhost Version="%s">\r\n' % str(eg.revision))
            self.WriteXmlString(stream.write, "    ")
            stream.write('</EventGhost>')
        data = stream.getvalue()
        stream.close()
        return data


    def Delete(self):
        self.isDeleted = True
        if self.dependants is not None:
            TreeLink.RemoveDependants(self)
        if self.xmlId in TreeLink.sessionId2target:
            del TreeLink.sessionId2target[self.xmlId]
        if self.xmlId in TreeLink.id2target:
            del TreeLink.id2target[self.xmlId]
        self.parent.RemoveChild(self)
        self.parent = None


    def GetAllItems(self):
        """
        Return a list of all nodes including self, by recursively traversing
        the child nodes.
        """
        result = []
        append = result.append
        def RecurseChilds(item):
            append(item)
            for child in item.childs:
                RecurseChilds(child)
        RecurseChilds(self)
        return result


    def GetDependantsOutside(self, allItems):
        result = []
        append = result.append
        def RecurseChilds(item):
            if item.dependants is not None:
                for link in item.dependants:
                    if link.owner and link.owner not in allItems:
                        append(link)
            for child in item.childs:
                RecurseChilds(child)
        RecurseChilds(self)
        return result


    def AskDelete(self):
        allItems = self.GetAllItems()
        if eg.config.confirmDelete:
            count = len(allItems) - 1
            if count > 0:
                mesg = eg.text.General.deleteManyQuestion % str(count)
            else:
                mesg = eg.text.General.deleteQuestion
            answer = eg.MessageBox(
                mesg,
                eg.APP_NAME,
                wx.NO_DEFAULT|wx.YES_NO|wx.ICON_EXCLAMATION
            )
            if answer == wx.ID_NO:
                return False
        dependants = self.GetDependantsOutside(allItems)
        if len(dependants) > 0:
            answer = eg.MessageBox(
                eg.text.General.deleteLinkedItems,
                eg.APP_NAME,
                wx.NO_DEFAULT|wx.YES_NO|wx.ICON_EXCLAMATION
            )
            return answer == wx.ID_YES
        return True


    def CanCut(self):
        return True


    def CanCopy(self):
        return True


    def CanPaste(self):
        if not wx.TheClipboard.Open():
            return False
        try:
            dataObj = wx.CustomDataObject("DragEventItem")
            if wx.TheClipboard.GetData(dataObj):
                if self.DropTest(eg.EventItem):
                    return True

            dataObj = wx.TextDataObject()
            if not wx.TheClipboard.GetData(dataObj):
                return False
            try:
                data = dataObj.GetText().encode("utf-8")
                tagToCls = self.document.XMLTag2ClassDict
                for childXmlNode in ElementTree.fromstring(data):
                    childCls = tagToCls[childXmlNode.tag.lower()].__bases__[1]
                    if self.DropTest(childCls) & HINT_MOVE_INSIDE:
                        continue
                    if self.parent is None:
                        return False
                    elif not self.parent.DropTest(childCls) & HINT_MOVE_INSIDE:
                        return False
            except:
                return False
        finally:
            wx.TheClipboard.Close()
        return True


    def CanDelete(self):
        return True


    def OnCmdCopy(self):
        data = self.GetXmlString()
        if data and wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(data))
            wx.TheClipboard.Close()

    
    def GetLabel(self):
        return self.name


    @eg.AssertNotMainThread
    @eg.LogIt
    def RenameTo(self, newName):
        self.name = newName
        if self.dependants:
            for link in self.dependants:
                eg.Notify("NodeChanged", link.owner)
        eg.Notify("NodeChanged", self)


    def SetAttributes(self, tree, treeId):
        pass


    @eg.AssertNotMainThread
    @eg.LogIt
    def MoveItemTo(self, newParentItem, pos):
        eg.Notify("NodeMoveBegin")
        oldPos = self.parent.RemoveChild(self)
        if newParentItem == self.parent:
            if pos > oldPos:
                pos -= 1
        #if pos >= len(newParentItem.childs):
        #    pos = -1
        self.parent = newParentItem
        newParentItem.AddChild(self, pos)
        eg.Notify("NodeMoveEnd")


    @eg.AssertNotMainThread
    def SetEnable(self, enable=True):
        self.isEnabled = enable


    def Select(self):
        eg.Notify("NodeSelected", self)


    def Execute(self):
        return None, None


    def GetChildIndex(self, child):
        try:
            return self.childs.index(child)
        except ValueError:
            return None


    def GetPath(self):
        item = self
        root = self.root
        path = []
        while item is not root:
            parent = item.parent
            path.append(parent.childs.index(item))
            item = parent
        path.reverse()
        return path


    def Traverse(self, func):
        result = func(self)
        if result is not None:
            return result
        for child in self.childs:
            result = child.Traverse(func)
            if result is not None:
                return result
        return None


    def TraverseDeepthFirst(self, func):
        for child in self.childs:
            result = child.TraverseDeepthFirst(func)
            if result is not None:
                return result
        result = func(self)
        if result is not None:
            return result
        return None


    def Print(self, *args, **kwargs):
        kwargs.setdefault("source", self)
        kwargs.setdefault("icon", self.icon)
        kwargs.setdefault("indent", 1)
        eg.Print(*args, **kwargs)


    def PrintError(self, *args, **kwargs):
        kwargs.setdefault("source", self)
        eg.PrintError(*args, **kwargs)


    def DropTest(self, cls):
        return HINT_NO_DROP


    def GetNextItem(self):
        """
        Returns the next item in the tree.

        This would be the next visible item of the tree if all items were
        expanded. So this can be used to forward traverse through the tree
        from any starting position.
        """
        if len(self.childs):
            return self.childs[0]
        while True:
            childs = self.parent.childs
            pos = childs.index(self) + 1
            if pos < len(childs):
                return childs[pos]
            self = self.parent
            if self.parent is None:
                return self


    def GetPreviousItem(self):
        """
        Returns the previous item in the tree.

        This would be the previous visible item of the tree if all items were
        expanded. So this can be used to reverse traverse through the tree
        from any starting position.
        """
        parent = self.parent
        if parent is not None:
            childs = parent.childs
            pos = childs.index(self)
            if pos > 0:
                self = childs[pos - 1]
            else:
                return parent
        while len(self.childs):
            self = self.childs[-1]
        return self

    @property
    def label(self):
        return self.GetLabel()
    @property
    def imageIndex(self):
        return self.icon.index if self.isEnabled else self.icon.disabledIndex
    @property
    def selectedImageIndex(self):
        return -1
    @property
    def canMove(self):
        return self is not self.document.autostartMacro
