# -*- coding: utf-8 -*-
version = "0.1.1"
#
# plugins/HTTPMenu/__init__.py
# Copyright (C)  2010 Pako  (lubos.ruckl@quick.cz)
#
# This file is a plugin for EventGhost.
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
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.1.1  by Pako 2012-11-07 10:28 UTC+1
#      - bugfix: reversed colors for submenus and commands
# 0.1.0  by Pako 2012-11-05 11:33 UTC+1
#      - extensive reworking for increased stability
#      - added option to return to any higher level (without event triggering)
# 0.0.1  by Pako 2012-10-11 13:30 UTC+1
#      - initial version 
#===============================================================================

eg.RegisterPlugin(
    name = "HTTP menu",
    author = "Pako",
    version = version,
    kind = "other",
    guid = "{C1E4A17B-F2AA-468F-BC22-FE7CCD9E90B9}",
    description = u"""<rst>HTTP menu.""",
    createMacrosOnAdd = True,
    canMultiLoad = False,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=4082",
    icon = (
        "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"
    ),
)

import pythoncom
import _winreg
import cPickle
import wx
from time import clock
from eg.WinApi.Dynamic import SendMessageTimeout
from os.path import abspath, join, dirname
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from zlib import decompress
from sys import getfilesystemencoding
FSE = getfilesystemencoding()

FILE_ATTRIBUTE_HIDDEN = 2
FILE_ATTRIBUTE_SYSTEM = 4
HITTEST_FLAG = (
    wx.TREE_HITTEST_ONITEMLABEL |
    wx.TREE_HITTEST_ONITEMICON |
    wx.TREE_HITTEST_ONITEMRIGHT
) 
SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
ICON = decompress(
    'x\x9c\x95\x94[H\x14Q\x18\xc7G2J4]AM$3\xb3p/\xba3\xbb\xdeJJ\xb1\xa2\x8b'
    '\x82a\x11\x04=I\x08\x15ToIA\x1bT/A\x0fBE\x0f\x11\xb5f\xc2\x8a\x99Y\x96YyI'
    '\xc5\x94"\xd9,-\x8d\xb4l5/y\xd9U\xbbh\xbf\xce\xaa\x84\xb8Z\xdb\x19~\x03'
    '\xf3}\xf3\xff\xce\xff\x9c\xf3\xcdH\x92\x87\xb8T*I\xdcWI\x07<%)H\x92$\xb5@'
    '\x84Dd:>5<%\x97\x01\xfc!+\xbb\x89\x13\xe7+\xb9U\xf6\x8a\xce\xae!\xd3\xec'
    '\x9c;\xc8\xdb+\xf0W,\xa4\xec\xcb\xe3\xcc\xc5G\xbc\xb0vU\xdaG\xbf\'\xbb'
    '\xab7\xa6>\xc5\'\xb2\x11o\xcd\x03"Rn\xb0\xffx!\x85\xf7\xad|\xee\x19q\xcb'
    '\x8bS\xef\xab{O`T7\xde\xea\x06\x02c,l\xcb\xcc%\xe7Z\r/_\xdb*\xff\xa57\xec'
    '\xa8%X\xf7\x91\x95\xf2(\x01\xf2\x00>\x9af\xc1]4[\xafs\xe4\xf4\x1d\xee=ia'
    '\xd8\xfem\xc1\xf5\xc4\xa4\xd6\x12\xaa\xeb&\\\xfe\xc9\ne\x8c e\x18\x9f\xa8'
    '\x0e\xbc"\xab\x08I\xb8\xc9\xce\x83\xf9\\\xce\xab\xa7\xb5\xbdw^/N\xffa\xda~'
    '\xd4\xca$k\x94\x89\xa9\x1a\xc1\xca\x08\xbez\x1bK\xd5\xcfY\xa6+!.\xc3\xcc'
    '\xd9K\x15X[\xba]j8\xe7\x0f\xd7\x0c \xeb\'\x89R~M\xf9\x08\x95\xc7\xa7|\xa8'
    '\xe4^Q\xc3\xca\xe2\x88b\xe2w\x99\xb9bi\xa4\xff\xeb\xb8i\xae~m\xf4\x10q\x06'
    '\x88Q@+O\x101\xb3\x16U\xb4\r/\xf53\x02\x8c\x85\xec9l\xa1\xb8\xbc\x99\xb9'
    '\xf3\xc7\xa6\xd6\xa15\x0e\x92\x18\x0f\xebb\xc0 <h\xf4?\xc5\x9ev\xe1\xa7'
    '\xad <\xc9Lfv\x11\xb7\x1fZ\xb1;\\\xfb\xc2\xa9\xd7\xc7\xd9\xd9$2\x1b'
    '\x12 ZhC\xd4\xed\xc2\x7f\t\t\xbb\xcd\x9c\xcc)\xe3qm\x1b\xa3c?\xe6=\x83'
    '\xd8\xb4z\x8c\x89\xc3l\xd9,\xb4F\x07\x01\xdaFV\'\xe5\xb3\xf7h\x01W\x0b'
    '\x1a\xc4\xbe\xf7\xfd\xb5\x07b\xd3\xea\x88\xddhG\x1d\xdf\xcdr\xb9\x1cCz.'
    '\xc7\xce\x95RV\xfd\x16w\xfa\xd8y~\xfe\xba*\xc2\x12\x8bH\xcb\xca\xe7\x82'
    '\xb9\x06k\xab\xeb9-\xc4\xfa\x8cj\x8c\xe9y\x1c2\x15c)m\xc2\xf6\xc5\xfe_\xdf'
    '\xe0\x9b6\x87\xe9\xdd\x87ASO\x9f\xc3m\xdd\'$\xa9\xc3\xc9)A\x98\xc0O\xb0H'
    '\xe01\x0b\xe7\xf3\x92\x99\\\xf2\xf4\xbb\x9d8\xff\x1d\x92\xf4\x1b&S\xc8\xba'
)

#global variable:
LOG = False
#===============================================================================

class Text:
    startMess= u'HTTP menu: Server "%s" started on host %s'
    stopMess = u'HTTP menu: Server "%s" on %s stopped'
    listhl = u"Currently enabled servers:"
    colLabels = (
        u"Server name",
        u"Host/Interface",
        u"Port",
        u"Server state",
    )
    stop = u"Stop"
    stopAll = u"Stop all"
    start = u"Start/Restart"
    startAll = u"Start/Restart all"
    refresh = u"Refresh"
    running = u"Running"
    stopped = u"Stopped"
    txtAllIfaces = u'All available interfaces'    
#===============================================================================

def convertColor(color):
    return "#%02x%02x%02x" % (color[0], color[1], color[2])
#===============================================================================

def GetInterfaces(txtAllIfaces):    
    cards = [txtAllIfaces, 'localhost']
    try:
        y = _winreg.OpenKey(
            _winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkCards"
        )
        for i in range(_winreg.QueryInfoKey(y)[0]):
            yy = _winreg.OpenKey(y,_winreg.EnumKey(y,i))
            cards.append(_winreg.QueryValueEx(yy, "Description")[0])
            _winreg.CloseKey(yy)
    except:
        raise #ToDo
    _winreg.CloseKey(y)
    return cards


def GetIPAddress(card, txtAllIfaces):
    if card == 'localhost':
        return "127.0.0.1"
    if card == txtAllIfaces:
        return "0.0.0.0"
    cards=[]
    try:
        y = _winreg.OpenKey(
            _winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkCards"
        )
        for i in range(_winreg.QueryInfoKey(y)[0]):
            yy = _winreg.OpenKey(y,_winreg.EnumKey(y,i))
            desc = _winreg.QueryValueEx(yy, "Description")[0]
            name = _winreg.QueryValueEx(yy, "ServiceName")[0]
            cards.append([desc, name])
            _winreg.CloseKey(yy)
    except:
        raise #ToDo
    _winreg.CloseKey(y)

    guid = cards[[item[0] for item in cards].index(card)][1]
    yy = None
    try: 
        y = _winreg.OpenKey(
            _winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\%s" % guid
        )
        try:
            yy = _winreg.QueryValueEx(y, "DhcpIPAddress")[0]
        except:
            try:
                yy = _winreg.QueryValueEx(y, "IPAddress")[0][0]
            except:
                pass
        _winreg.CloseKey(y)
    except:
        pass # Key Interface not found
    return yy
#===============================================================================
    
class MyTreeCtrl(wx.TreeCtrl):

    root = None

    def __init__(
        self,
        parent,
        id,
        style = wx.TR_DEFAULT_STYLE,
        size = wx.DefaultSize,
        data = None,
        text = None
    ):
        self.sourceNode = None
        self.data = data
        self.clipBoard = None
        self.cut = None
        self.text = text if text else self.txt
        
        wx.TreeCtrl.__init__(self, parent, id, size = size, style = style)

        #il = wx.ImageList(16, 16)
        #self.fldrix     = il.Add(wx.Bitmap(
        #    wx.Image(join(eg.imagesDir, "folder.png"), wx.BITMAP_TYPE_PNG)))
        #self.openfldrix = il.Add(wx.Bitmap(
        #    wx.Image(join(eg.imagesDir, "open.png"  ), wx.BITMAP_TYPE_PNG)))
        #self.fileix     = il.Add(wx.Bitmap(
        #    wx.Image(join(eg.imagesDir, "new.png"   ), wx.BITMAP_TYPE_PNG)))
        #self.AssignImageList(il)

        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        self.fldrix     = il.Add(
            wx.ArtProvider.GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        self.openfldrix = il.Add(wx.ArtProvider.GetBitmap(
            wx.ART_FOLDER_OPEN,   wx.ART_OTHER, isz))
        self.fileix     = il.Add(
            wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        self.backix     = il.Add(
            wx.ArtProvider.GetBitmap(wx.ART_GO_DIR_UP, wx.ART_OTHER, isz))
        self.rootix     = il.Add(
            wx.ArtProvider.GetBitmap(wx.ART_HELP_FOLDER, wx.ART_OTHER, isz))
        self.AssignImageList(il)

        if data:
            self.List2Tree(data)
        else:
            root = self.AddRoot(self.text.root)
            self.SetItemImage(root, self.rootix, wx.TreeItemIcon_Normal)
            self.SetItemData(root, None)
            self.root = root
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightClick, self)
        self.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnBeginDrag, self)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnTreeLabelEdit)        
        self.hwnd = self.GetHandle()
        self.insertionMark = None
        self.dt = self.DropTarget(self)
        self.SetDropTarget(self.dt)  


    def List2Tree(self, data, node = None, ix = 0):
        def FillTreeNode(data, node, ix):
            if not node:
                node = self.AddRoot(data[0])
                self.SetItemData(node, None)
                self.SetItemImage(node, self.rootix, wx.TreeItemIcon_Normal)
                self.root = node
            if len(data) == 3:
                if node != self.root and data[0]:
                    self.SetItemData(node, data[2])
                    self.SetItemImage(node, self.fldrix, wx.TreeItemIcon_Normal)
                    self.SetItemImage(node, self.openfldrix, wx.TreeItemIcon_Expanded)
                for item in data[1]:
                    i = self.GetChildrenCount(node) if node != self.root else 1
                    child = self.AppendItem(node, item[0])
                    FillTreeNode(item, child, i)
            else:
                if ix:
                    self.SetItemImage(node, self.fileix, wx.TreeItemIcon_Normal)
                else:
                    self.SetItemImage(node, self.backix, wx.TreeItemIcon_Normal)
                self.SetItemData(node, data[1])
        FillTreeNode(data, node, ix)


    def Tree2List(self, node):
        def Traverse(node):
            pyData = self.GetItemData(node)
            if self.ItemHasChildren(node):
                tmp = []
                child, cookie = self.GetFirstChild(node)
                while child.IsOk():
                    tmp.append(Traverse(child))
                    child, cookie = self.GetNextChild(child, cookie)
                return [self.GetItemText(node), tmp, pyData]
            else:
                return [self.GetItemText(node), pyData]
        return Traverse(node)


    def Tree2Path(self, node):
        def Traverse(nod, pth):
            if nod == self.root:
                return pth
            prnt = self.GetItemParent(nod)
            tmp = []
            child, cookie = self.GetFirstChild(prnt)
            while child.IsOk():
                tmp.append(child)
                child, cookie = self.GetNextChild(child, cookie)
            pth.append(tmp.index(nod))
            return Traverse(prnt, pth)
        return Traverse(node, [])
        

    def SetInsertMark(self, treeItem, after):
        lParam = long(treeItem.m_pItem)
        if self.insertionMark == (after, lParam):
            return
        # TVM_SETINSERTMARK = 4378
        SendMessageTimeout(self.hwnd, 4378, after, lParam, 1, 100, None)
        self.insertionMark = (after, lParam)


    def ClearInsertMark(self):
        if self.insertionMark:
            SendMessageTimeout(self.hwnd, 4378, 0, long(0), 1, 100, None)
            self.insertionMark = None
            self.Refresh()
   

    def OnBeginDrag(self, evt):
        """ Left Mouse Button initiates "Drag" for Tree Nodes """
        srcItemId = evt.GetItem()
        self.SelectItem(srcItemId)
        if srcItemId == self.root:
            return
        pth = self.Tree2Path(srcItemId)
        if not pth[0] and len(pth) > 1:
            return
        treeList = self.Tree2List(srcItemId)
        self.sourceNode = srcItemId
        cdo = wx.CustomDataObject(wx.DataFormat('DropData'))
        cdo.SetData(cPickle.dumps(treeList, 1))
        ds = wx.DropSource(self)
        ds.SetData(cdo)
        ds.DoDragDrop(wx.Drag_AllowMove)
        self.ClearInsertMark()
        evt.Skip()


    def OnRightClick(self, evt):
        node = evt.GetItem()
        root = self.root
        self.SelectItem(node)
        if not hasattr(self, "popupID0"):
            self.popupID0 = wx.NewId()
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
            self.Bind(wx.EVT_MENU, self.OnNewItem, id = self.popupID0)
            self.Bind(wx.EVT_MENU, self.OnDelete,  id = self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnCut,     id = self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnCopy,    id = self.popupID3)
            self.Bind(wx.EVT_MENU, self.OnPaste,   id = self.popupID4)
        menu = wx.Menu()
        newTxt = self.text.new if node==root or self.ItemHasChildren(node) else self.text.submenu
        item0 = menu.Append(self.popupID0, newTxt)
        item1 = menu.Append(self.popupID1, self.text.delete)
        item2 = menu.Append(self.popupID2, self.text.cut)
        item3 = menu.Append(self.popupID3, self.text.copy)
        item4 = menu.Append(self.popupID4, self.text.paste)
        pth = self.Tree2Path(node)
        if node != root and (not pth[0] and len(pth) > 1):
            item0.Enable(False)
        if node == root or (not pth[0] and len(pth) > 1):
            item1.Enable(False)
            item3.Enable(False)
            item2.Enable(False)
        if not self.clipBoard or (not pth[0] and len(pth) > 1):
            item4.Enable(False)
        elif self.cut:
            cutPath = self.Tree2Path(self.cut)
            if self.Tree2Path(node)[-len(cutPath):] == cutPath:
                item4.Enable(False)
        self.PopupMenu(menu)
        menu.Destroy()
        evt.Skip()


    def OnTreeLabelEdit(self, evt):
        """Edit tree label (some labels may not be edited)."""
        itm = evt.GetItem()
        pth = self.Tree2Path(itm)
        if itm == self.root:
            evt.Veto()
        else:
            evt.Skip()


    def CreateSubmenu(self, itm):
        if itm != self.root and not self.ItemHasChildren(itm): 
            self.SetItemImage(itm, self.fldrix, wx.TreeItemIcon_Normal)
            self.SetItemImage(itm, self.openfldrix, wx.TreeItemIcon_Expanded)
            if self.GetItemText(itm) == self.text.new:
                self.SetItemText(itm, self.text.newSubm)
            newItem = self.AppendItem(itm, self.text.parent)
            self.SetItemData(newItem, ["HTTPM","suffix",""])
            self.SetItemImage(newItem, self.backix, wx.TreeItemIcon_Normal)


    def OnNewItem(self, evt):
        itm = self.GetSelection()
        self.CreateSubmenu(itm)
        newItem = self.AppendItem(itm, self.text.new)
        self.SetItemData(newItem, ["HTTPM","suffix",""])
        self.SetItemImage(newItem, self.fileix, wx.TreeItemIcon_Normal)
        self.Expand(itm)
        self.SelectItem(newItem)
        evt.Skip()


    def DeleteItem(self, itm):
        parent = self.GetItemParent(itm)
        self.Delete(itm)
        if self.GetChildrenCount(parent) == 1:
            child, cookie = self.GetFirstChild(parent)
            self.Delete(child)
            self.SetItemImage(parent, self.fileix, wx.TreeItemIcon_Normal)         
            self.SetItemImage(parent, self.fileix, wx.TreeItemIcon_Expanded)
            if self.GetItemText(parent) == self.text.newSubm:
                self.SetItemText(parent, self.text.new)


    def OnDelete(self, evt):
        itm = self.GetSelection()
        self.DeleteItem(itm)
        evt.Skip()        


    def OnCopy(self, evt):
        itm = self.GetSelection()
        self.cut = None
        self.clipBoard = self.Tree2List(itm)
        evt.Skip()


    def OnCut(self, evt):
        itm = self.GetSelection()
        self.clipBoard = self.Tree2List(itm)
        self.cut = itm
        evt.Skip()


    def OnPaste(self, evt):
        itm = self.GetSelection()
        self.CreateSubmenu(itm)
        self.List2Tree((None, [self.clipBoard], None), itm)
        if self.cut:
            self.DeleteItem(self.cut)
            self.cut = None
        evt.Skip()


    def GetValue(self):
        return self.Tree2List(self.root)


    class DropTarget(wx.DropTarget):
        """ This is a custom DropTarget object. """
        def __init__(self, tree):
            wx.DropTarget.__init__(self)
            self.tree = tree
            self.df = wx.DataFormat('DropData')
            self.cdo = wx.CustomDataObject(self.df)
            self.SetDataObject(self.cdo)
            self.lastDropTime = clock()
            self.lastTargetItemId = None
            timerId = wx.NewId()
            self.autoScrollTimer = wx.Timer(self.tree, timerId)
            self.tree.Bind(wx.EVT_TIMER, self.OnDragTimerEvent, id = timerId)
     

        def OnEnter(self, x, y, dragResult):
            """Called when the mouse enters the drop target."""
            self.autoScrollTimer.Start(50)
            return dragResult


        def OnDragOver(self, x, y, dummyDragResult):
            """Called when the mouse is being dragged over the drop target."""
            tree = self.tree
            flg = False
            dstItemId, flags = self.tree.HitTest((x, y))     
            if not dstItemId.IsOk():
                flg = True
            else:
                if tree.GetItemParent(dstItemId) == self.tree.sourceNode:
                    flg = True
                if dstItemId == self.tree.sourceNode:
                    flg = True
                if not (flags & HITTEST_FLAG):
                    flg = True
                if dstItemId == tree.root:
                    flg = True
            if flg:
                tree.ClearInsertMark()
                return wx.DragNone
            targetRect = tree.GetBoundingRect(dstItemId)
            after = int(y > targetRect.y + targetRect.height / 2)
            # expand a container, if the mouse is hold over it for some time
            if dstItemId == self.lastTargetItemId:
                if self.lastDropTime + 0.6 < clock():
                    tree.SelectItem(dstItemId)
                    if tree.ItemHasChildren(dstItemId):
                        if not tree.IsExpanded(dstItemId):
                            tree.Expand(dstItemId)
                            if after:
                                tree.ClearInsertMark()
                                return
            else:
                self.lastDropTime = clock()
                self.lastTargetItemId = dstItemId
            if tree.ItemHasChildren(dstItemId) and tree.IsExpanded(dstItemId) and after:
                flg = True
            pth = tree.Tree2Path(dstItemId)
            if not pth[0] and len(pth) > 1 and not after:
                flg = True  
            if not flg:   
                tree.SetInsertMark(dstItemId, after)        
            return wx.DragMove


        def OnLeave(self):
            """Called when the mouse leaves the drop target."""
            self.tree.ClearInsertMark()
            self.autoScrollTimer.Stop()


        def OnData(self, x, y, dragResult):
            self.OnLeave() 
            dstItemId, flag = self.tree.HitTest((x, y))
            tree = self.tree
            if self.GetData(): #copies the data from the drop source to self.cdo
                data = cPickle.loads(self.cdo.GetData())
                pos = tree.Tree2Path(dstItemId)[0]
                targetRect = tree.GetBoundingRect(dstItemId)
                parent = tree.GetItemParent(dstItemId)
                if y > targetRect.y + targetRect.height / 2:
                    tree.SetInsertMark(dstItemId, 1)
                    if (pos + 1) < tree.GetChildrenCount(parent):
                        newItem = tree.InsertItemBefore(parent, pos+1, data[0])
                    else:
                        newItem = tree.AppendItem(parent, data[0])
                else:
                    tree.SetInsertMark(dstItemId, 0)
                    if pos:
                        newItem = tree.InsertItemBefore(parent,pos,data[0])
                    else:
                        newItem = tree.PrependItem(parent,data[0])
                tree.List2Tree(data, newItem, tree.GetChildrenCount(parent)-1)
                tree.SelectItem(newItem)
                if dragResult == wx.DragMove:
                    if self.tree.sourceNode:
                        parent = self.tree.GetItemParent(self.tree.sourceNode)
                        self.tree.DeleteItem(self.tree.sourceNode)
                        self.tree.sourceNode = None           


        def OnDragTimerEvent(self, dummyEvent):
            """
            Handles wx.EVT_TIMER, while a drag operation is in progress. It is
            responsible for the automatic scrolling if the mouse gets on the
            upper or lower bounds of the control.
            """
            tree = self.tree
            x, y = wx.GetMousePosition()
            treeRect = tree.GetScreenRect()
            if treeRect.x <= x <= treeRect.GetRight():
                if y < treeRect.y + 20:
                    tree.ScrollLines(-1)
                elif y > treeRect.GetBottom() - 20:
                    tree.ScrollLines(1)

    class txt:
        root    = "Menu root"
        new     = "New item"
        delete  = "Delete"
        cut     = "Cut"
        copy    = "Copy"
        paste   = "Paste"
        parent  = "Go back"
        submenu = "Create submenu"
        newSubm = "New submenu"
#===============================================================================
class TreeMenuCtrl(wx.Window):

    def __init__(
        self,
        parent,
        id=-1,
        data=[],
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.BORDER_NONE,
        validator=wx.DefaultValidator,
        name="TreeMenuCtrl",
        text = None
    ):
        wx.Window.__init__(self, parent, id, pos, size, style, name)
        self.SetThemeEnabled(True)
        treeCtrl = MyTreeCtrl(
            self,
            -1,
            data = data,
            style = wx.TR_DEFAULT_STYLE|wx.TR_EDIT_LABELS,
         )
        self.last_sel = None
        self.treeCtrl = treeCtrl
        self.text = text if text else self.txt
        height = treeCtrl.GetSize()[1]    
        sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, -1, self.text.menuTree),
            wx.VERTICAL
        )        
        sizer.Add(treeCtrl, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL, 5)
        eventSizer = wx.FlexGridSizer(2, 3, 2, 10)
        eventSizer.AddGrowableCol(0)
        eventSizer.AddGrowableCol(1)
        eventSizer.AddGrowableCol(2)
        prefLabel = wx.StaticText(self, -1, self.text.evtPrefix)
        suffLabel = wx.StaticText(self, -1, self.text.evtSuffix)
        paylLabel = wx.StaticText(self, -1, self.text.evtPayload)
        self.prefId = wx.NewId()
        self.suffId = wx.NewId()
        self.paylId = wx.NewId()
        prefCtrl = wx.TextCtrl(self, self.prefId, "")
        suffCtrl = wx.TextCtrl(self, self.suffId, "")
        paylCtrl = wx.TextCtrl(self, self.paylId, "")
        eventSizer.Add(prefLabel)
        eventSizer.Add(suffLabel)
        eventSizer.Add(paylLabel)
        eventSizer.Add(prefCtrl,1,wx.EXPAND)
        eventSizer.Add(suffCtrl,1,wx.EXPAND)
        eventSizer.Add(paylCtrl,1,wx.EXPAND)
        sizer.Add(eventSizer,0,wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND,5)
        self.SetSizerAndFit(sizer)
        self.Layout()
        self.SetSize(size)
        self.SetMinSize(self.GetSize())
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_TEXT, self.OnTextChange)

        def OnTreeSel(evt):
            tree = self.treeCtrl
            node = evt.GetItem()
            self.last_sel = node
            flg = node != tree.root
            prefLabel.Enable(flg)
            suffLabel.Enable(flg)
            paylLabel.Enable(flg)       
            prefCtrl.Enable(flg)
            suffCtrl.Enable(flg)
            paylCtrl.Enable(flg)       
            if flg:
                pyData = tree.GetItemData(node)
                if pyData:
                    prefCtrl.ChangeValue(pyData[0])
                    suffCtrl.ChangeValue(pyData[1])
                    paylCtrl.ChangeValue(pyData[2])
            else:
                prefCtrl.ChangeValue("")
                suffCtrl.ChangeValue("")
                paylCtrl.ChangeValue("")
            evt.Skip()
        self.treeCtrl.Bind(wx.EVT_TREE_SEL_CHANGED, OnTreeSel) 


    def OnSize(self, dummyEvent):
        if self.GetAutoLayout():
            self.Layout()


    def OnTextChange(self, evt):
        tree = self.treeCtrl
        node = self.last_sel
        pyData = tree.GetItemData(node)
        id = evt.GetId()
        strng = evt.GetString()
        if id == self.prefId:
            pyData[0] = strng
        if id == self.suffId:
            pyData[1] = strng
        if id == self.paylId:
            pyData[2] = strng
        tree.SetItemData(node, pyData)
        evt.Skip()


    def OnSetFocus(self, dummyEvent):
        self.treeCtrl.SetFocus()


    def GetValue(self):
        return self.treeCtrl.GetValue()

    class txt:
        menuTree   = "Menu tree"
        evtPrefix  = "Event prefix:"
        evtSuffix  = "Event suffix:"
        evtPayload = "Event payload:"    
#===============================================================================

class Menu(object):

    def __init__(self, data, title):
        self.data = data
        self.items = self.data[1]
        self.title = title
        self.GoHome()
 

    def GetItems(self):
        if self.path:
            ix=0
            itms=self.data[:]
            while ix>-1:
                i=self.path.find("/",ix+1)
                if i>-1:
                    c=int(self.path[ix+1:i])
                    itms=itms[1][c]
                else:
                    c=int(self.path[ix+1:])
                    itms=itms[1][c]
                ix=i
            return itms
        else:
            return self.data


    def GetTitle(self):
        if self.path:
            return self.GetItems()[0]
        return self.title


    def GoHome(self):
        self.items = self.data[1]
        self.path = ""
        self.Parents = []


    def TriggerEvent(self, ix = 0):
        evtData = self.items[ix][-1]
        if evtData[1]:
            if evtData[2]:
                eg.TriggerEvent(evtData[1], evtData[2], prefix = evtData[0] or "HTTPM")
            else:
                eg.TriggerEvent(evtData[1], prefix = evtData[0] or "HTTPM")


    def Exec(self, pth):
        op = pth.find("/Exec")
        p = pth[:op]
        if p == self.path: # open file
            ix = pth[op+5:]
            if ix:
                self.TriggerEvent(int(ix))
        else:
            pList=p.split("/")
            pathList=self.path.split("/")
            if len(pList) > len(pathList):
                if pList[:-1] == pathList: # go to folder (child)
                    ix=int(pth[1+p.rfind("/"):op])
                    self.TriggerEvent(ix)
                    if not self.path or self.path and ix:
                        if len(self.items[ix]) == 3:
                            self.Parents.append(self.GetTitle())
                            self.path=p
                            self.items = self.items[ix][1]


    def Back(self, pth):
        self.TriggerEvent(0)
        self.GoToParent(pth.replace("Back","Parent"))
        

    def GoToParent(self, pth):
        oldLn=len(self.path.split("/"))
        self.path = pth[:pth.find("/Parent")]
        ln = len(self.path.split("/"))
        for i in range(oldLn-ln):
            self.Parents.pop()
        self.items = self.GetItems()[1]
#===============================================================================

class HTTP_handler(BaseHTTPRequestHandler):
    """ The user-provided request handler class.
        An instance of this class is created for each request !!! """

    server_version = "EventGhost_HTTP_menu/%s" % version
    protocol_version = "HTTP/1.1"

    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(
            self,
            request,
            client_address,
            server
        )


    def log_message(self, format, *args):
        if LOG:
            logName = "HTTPserver_%s.log" % self.server.title.replace(" ", "_")
            try:
                logfile = abspath(join(dirname(__file__), logName))
                open(logfile, "a").write("%s -- %s - %s:  %s\n" % ( 
                    self.log_date_time_string(),
                    self.client_address,
                    self.address_string(),
                    format % args
                ))
            except eg.Exception, exc:
                eg.PrintError(unicode(exc))
            except:
                eg.PrintTraceback(
                    eg.text.Error.InAction % 
                    "BaseHTTPRequestHandler.log_message", 1, source = self
                )


    def InconsistencyCheck(self, menu):
        if self.path.find("/Home")>-1:
            return False
        fndExc=self.path.find("/Exec")
        pth = self.path[:self.path.rfind("/")]
        if len(self.path)-fndExc == 5:
            if pth.split("/")[:-1] == menu.path.split("/"):
                return False
        if fndExc > -1 and len(self.path) - fndExc > 5:
            if pth == menu.path[:len(pth)]:
                return False
        if self.path=='/' and menu.path=="":
            return False
        if self.path.find("/Parent")>-1:
            if pth == menu.path[:len(pth)]:
                return False
        if self.path.find("/Back")>-1:
            if pth == menu.path[:len(pth)]:
                return False
        return True


    def WriteWfile(self, page):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header("Content-Length", str(len(page)))  
            self.end_headers()
            self.wfile.write(page)
        except:
            pass


    def Reset(self, srvr):
        self.WriteWfile(u'''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html><head>
<meta http-equiv="Content-Type"  content="text/html; charset=utf-8">
<title>%s</title>
<script type="text/javascript">
function start()
{document.location.href = "http://%s:%i";}
window.onload = start; 
</script>
</head>''' % (
            srvr.title, 
            self.request.getsockname()[0], 
            self.request.getsockname()[1]
        ))


    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(200)
            self.send_header("Content-type", 'text/html')
            self.send_header("Content-Length", len(ICON))
            self.end_headers()
            self.wfile.write(ICON)
            return   
        srvr = self.server
        hMenu = srvr.hMenu
        if self.InconsistencyCheck(hMenu):
            hMenu.GoHome()
            self.Reset(srvr)
            return
        if "/Parent" in self.path:
            hMenu.GoToParent(self.path)
        elif "/Exec" in self.path:
            hMenu.Exec(self.path)
        elif "/Back" in self.path:
            hMenu.Back(self.path)
        elif "/Home" in self.path:
            hMenu.GoHome()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        htmlPage = u'''
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>%s</title>
<style type="text/css">
body {background-color: %s;}
table {border-collapse: collapse; padding: 0px; font-family: Arial, Helvetica, sans-serif; font-size: %ipx;} 
tr {border: %ipx solid %s;}
.tran {border: 0px; background: transparent; cursor: auto; color: %s;}
.brdr {border-top: %ipx solid %s; border-bottom: %ipx solid %s; cursor: pointer}
.filN {background-color: %s; color: %s;}
.filH {background-color: %s; color: %s;} 
.folN {background-color: %s; color: %s;}
.folH {background-color: %s; color: %s;}
</style>      
<script type="text/javascript">
function start()
{
var table = document.getElementById("myTable");
var ixs = [0,1,2];
var clickAction = function(cl){
  r = cl.parentNode.rowIndex;
  pth = "%s";
  if (pth.length>0){
    arPath = pth.split("/");
    path = arPath.slice(0,1+r).join("/");
  }
  else {
    arPath = "";
    path = "";
  }
  r = (r - arPath.length).toString();
  if (cl.parentNode.className =="back") {cmd = path+"/Parent";}
  else if (arPath.length>0 && r=="0"){
  path = arPath.slice(0,arPath.length-1).join("/");
  cmd=path+"/Back";}
  else {
    if (cl.parentNode.className == 'folder'){cmd =pth+"/"+r+"/Exec";}
    else {cmd=pth+"/Exec"+r;}
  }
    document.location.href = "http://%s:%i"+cmd;
};
var mouseOut = function(cl){
 if (cl.parentNode.className == 'file'){cls = 'filN brdr';}
 else {cls = 'folN brdr';}
    row=cl.parentNode;
    for(var i = 0; i < ixs.length; i++){row.cells[ixs[i]].className = cls;} 
};   
var mouseOver = function(cl){
 if (cl.parentNode.className =='file'){cls = 'filH brdr';}
 else{cls = 'folH brdr';}
    row=cl.parentNode;
    for(var i = 0; i < ixs.length; i++){row.cells[ixs[i]].className = cls;}  
};     
 for(var r = 0; r < table.rows.length; r++){
   var row = table.rows[r];
     for(var c = 0; c < row.cells.length; c++){
       if (row.className != "tran"){
         var	cell = row.cells[c];
         cell.onmouseout  = function() {mouseOut(this);}
         cell.onmouseover = function() {mouseOver(this);}
         cell.onclick = function() {clickAction(this);}   
         cell.onmouseout();
       }
     } 
   }
}
window.onload = start; 
</script>
</head>
<body>
<table id="myTable">''' % (
    srvr.title, srvr.bckGround, srvr.fontsize, srvr.brdrwdth, srvr.border, 
    srvr.border, srvr.brdrwdth, srvr.border, srvr.brdrwdth, srvr.border, 
    srvr.filIdlBck, srvr.filIdlTxt, srvr.filActBck,srvr.filActTxt,
    srvr.folIdlBck, srvr.folIdlTxt, srvr.folActBck,srvr.folActTxt,
    hMenu.path, self.request.getsockname()[0], self.request.getsockname()[1]
)
        if hMenu.Parents:
            for par in hMenu.Parents:
                htmlPage += u'<tr class="back"><td>▲&nbsp;</td><td>%s</td><td>&nbsp;▲</td></tr>' % par
            htmlPage += '<tr class="tran"><td></td><td>%s</td><td></td></tr>' % hMenu.GetTitle() 
        for ix,item in enumerate(hMenu.items):
            if hMenu.path != "" and not ix:
                htmlPage += u'''
<tr class="folder"><td>◄&nbsp;</td><td>%s</td><td></td></tr>''' % item[0]
            elif len(item) == 3:
                htmlPage += u'''
<tr class="folder"><td></td><td>%s</td><td>&nbsp;►</td></tr>''' % item[0]
            else:
                htmlPage += u'''
<tr class="file"><td></td><td>%s</td><td></td></tr>''' % item[0]
        htmlPage += u"</table></body></html>"
        htmlPage = htmlPage.encode("UTF-8")
        self.WriteWfile(htmlPage)
    do_HEAD = do_GET
    do_POST = do_GET    
#===============================================================================

class HTTP_server(HTTPServer):

    def __init__(
        self,
        plugin,
        server_address,
        RequestHandlerClass,
        hMenu,
        title,
        bckGround,
        border,
        filIdlTxt,
        filIdlBck,
        filActTxt,
        filActBck,
        folIdlTxt,
        folIdlBck,
        folActTxt,
        folActBck,
        fontsize,
        brdrwdth,
    ):
        self.hMenu     = hMenu
        self.title     = title
        self.bckGround = bckGround
        self.border    = border
        self.filIdlTxt = filIdlTxt
        self.filIdlBck = filIdlBck
        self.filActTxt = filActTxt
        self.filActBck = filActBck
        self.folIdlTxt = folIdlTxt
        self.folIdlBck = folIdlBck
        self.folActTxt = folActTxt
        self.folActBck = folActBck
        self.fontsize  = fontsize
        self.brdrwdth  = brdrwdth
        plugin.servers[title] = self      
        eg.PrintNotice(plugin.text.startMess % (title,"%s:%i" % server_address))
        self.req = None
        HTTPServer.__init__(
            self,
            server_address,
            RequestHandlerClass
        )


    def server_bind(self):
        HTTPServer.server_bind(self)
        self.socket.settimeout(1)
        self.run = True


    def get_request(self):
        while self.run:
            try:
                self.req = self.socket.accept()
                self.req[0].settimeout(None)              
                return self.req
            except socket.timeout:
                pass


    def stop(self):
        self.run = False
        if self.req:
            try:
                self.req[0].shutdown(2)
            except:
                pass
            try:
                self.req[0].close()
            except:
                pass
        self.req = None


    def serve(self):
        while self.run:
            self.handle_request()
#===============================================================================

class HTTPmenu_thread(Thread):

    def __init__ (
        self,
        plugin,
        hMenu,
        iface,
        port,
        title,
        bckGround,
        border,
        filIdlTxt,
        filIdlBck,
        filActTxt,
        filActBck,
        folIdlTxt,
        folIdlBck,
        folActTxt,
        folActBck,
        fontsize,
        brdrwdth,
        ):
        Thread.__init__(self)
        self.plugin    = plugin
        self.handler   = HTTP_handler
        self.hMenu   = hMenu
        self.iface     = iface
        self.port      = port
        self.title     = title
        self.bckGround = bckGround
        self.border    = border
        self.filIdlTxt = filIdlTxt
        self.filIdlBck = filIdlBck
        self.filActTxt = filActTxt
        self.filActBck = filActBck
        self.folIdlTxt = folIdlTxt
        self.folIdlBck = folIdlBck
        self.folActTxt = folActTxt
        self.folActBck = folActBck
        self.fontsize  = fontsize
        self.brdrwdth  = brdrwdth
        self.server    = None


    def run (self):
        self.server = HTTP_server(
            self.plugin,
            (self.iface, self.port),
            self.handler,
            self.hMenu,
            self.title,
            self.bckGround,
            self.border,
            self.filIdlTxt,
            self.filIdlBck,
            self.filActTxt,
            self.filActBck,
            self.folIdlTxt,
            self.folIdlBck,
            self.folActTxt,
            self.folActBck,
            self.fontsize,
            self.brdrwdth,
        )
        self.server.serve()
#===============================================================================
#cls types for ACTIONS list :
#===============================================================================

class StartServer(eg.ActionBase):

    class text:
        bckgrnd = u'Background colour'
        border = u'Border colour'
        fontsize = u'Font size (px):'
        brdrwdth = u'Border width (px):'
        idleText = u'Idle item text'
        idleBack = u'Idle item background'
        activText = u'Active item text'
        activBack = u'Active item background'
        browseTitle = u"Selected folder:"
        port = u"TCP/IP port:"
        modeHostChoiceLabel = u'Server host address to specify as'
        modeHostChoice = (
            u'Server title (or Python expression)',
            u'Server title from eg.event.payload[0]',
            u'Interface',
            u'Server IP address (or Python expression)',
        )
        titleLabel = u"Server name (must be unique !!!):"
        design = u"Html page design"
        common = u"Common properties"
        submenu = u"Submenu colors"
        command = u"Command colors"

    def __call__(
        self,
        title = "",
        mode = 0,
        iFace = "localhost",
        port = "8080",
        bckgrnd   = (245, 215, 255),
        border    = (0, 0, 0),
        filIdlTxt = (74, 74, 74),
        filIdlBck = (183, 183, 255),
        filActTxt = (183, 183, 255),
        filActBck = (74, 74, 74),
        folIdlTxt = (128, 0, 0),
        folIdlBck = (243, 237, 109),
        folActTxt = (243, 237, 109),
        folActBck = (128, 0, 0),
        fontsize  = 32,
        brdrwdth  = 1,
        data = None
    ):
        self.plugin.StartServer(
            title,
            mode,
            iFace,
            port,
            bckgrnd,
            border,
            filIdlTxt,
            filIdlBck,
            filActTxt,
            filActBck,
            folIdlTxt,
            folIdlBck,
            folActTxt,
            folActBck,
            fontsize,
            brdrwdth,
            data
        )
 

    def GetLabel(
        self,
        title,
        mode,
        iFace,
        port,
        bckgrnd,
        border,
        filIdlTxt,
        filIdlBck,
        filActTxt,
        filActBck,
        folIdlTxt,
        folIdlBck,
        folActTxt,
        folActBck,
        fontsize,
        brdrwdth,
        data
    ):
        if title:
            self.plugin.AddServerName(title)
        return '%s: %s  (%s: %s)' % (self.name, title, iFace, port)


    def Configure(
        self,
        title = "",
        mode = 0,
        iFace = "localhost",
        port = "8080",
        bckgrnd   = (245, 215, 255),
        border    = (0, 0, 0),
        filIdlTxt = (74, 74, 74),
        filIdlBck = (183, 183, 255),
        filActTxt = (183, 183, 255),
        filActBck = (74, 74, 74),
        folIdlTxt = (128, 0, 0),
        folIdlBck = (243, 237, 109),
        folActTxt = (243, 237, 109),
        folActBck = (128, 0, 0),
        fontsize = 32,
        brdrwdth = 1,
        data = None
    ):
        panel = eg.ConfigPanel(self)
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(leftSizer,1,wx.EXPAND|wx.RIGHT,10)
        panel.sizer.Add(mainSizer,1,wx.EXPAND)
        text = self.text
        menuCtrl = TreeMenuCtrl(
            panel,
            -1,
            data = data,
            size = (150, 150),
            text = None
            )
        titleLabel = wx.StaticText(panel,-1,self.text.titleLabel)
        titleCtrl = wx.TextCtrl(panel, -1, title)
        clr = titleCtrl.GetBackgroundColour()
        topSizer = wx.FlexGridSizer(2, 2, 10, 5)
        topSizer.AddGrowableCol(1)
        topSizer.Add(titleLabel,0,wx.TOP,3)
        topSizer.Add(titleCtrl, 0, wx.EXPAND)
        statSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, ""),
            wx.VERTICAL
        )
        statSizer.Add(topSizer,1,wx.EXPAND)
        leftSizer.Add(statSizer, 0, wx.EXPAND)
        leftSizer.Add(menuCtrl,1,wx.EXPAND)
        radioBoxMode = wx.RadioBox(
            panel,
            -1,
            text.modeHostChoiceLabel,
            choices = text.modeHostChoice[2:],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxMode.SetSelection(mode)
        staticBox = wx.StaticBox(panel, -1, "")
        ifaces = GetInterfaces(self.plugin.text.txtAllIfaces)
        tmpSizer = wx.BoxSizer(wx.VERTICAL)
        ifaceCtrl = wx.Choice(panel,-1,choices = ifaces)
        tmpSizer.Add(ifaceCtrl,1,wx.EXPAND)
        middleSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        middleSizer.Add(radioBoxMode,0,wx.LEFT)
        middleSizer.Add((10,-1),0,wx.LEFT|wx.EXPAND)
        middleSizer.Add(tmpSizer,1,wx.LEFT|wx.EXPAND)
        leftSizer.Add(middleSizer, 0, wx.EXPAND|wx.TOP, 8)
        size = (tmpSizer.GetMinSize()[0]+12,-1)
        minSize = (ifaceCtrl.GetSize()[0], -1)
        id = wx.NewId()
        id2 = wx.NewId()

        def OnHostChoice(evt = None):
            middleSizer = leftSizer.GetItem(2).GetSizer()
            dynamicSizer = middleSizer.GetItem(2).GetSizer()
            dynamicSizer.Clear(True)
            middleSizer.Detach(dynamicSizer)
            dynamicSizer.Destroy()
            dynamicSizer = wx.GridBagSizer(2, 10)
            dynamicSizer.SetMinSize(size)
            middleSizer.Add(dynamicSizer,1, wx.EXPAND)
            mode = radioBoxMode.GetSelection()
            portCtrl = None
            iFaceLabel = wx.StaticText(panel,-1,text.modeHostChoice[mode+2]+":")
            if mode ==0:
                ifaces = GetInterfaces(self.plugin.text.txtAllIfaces)
                ifaceCtrl = wx.Choice(panel,id,choices = ifaces)
                if not evt:
                    ifaceCtrl.SetStringSelection(iFace)        
            elif mode == 1:
                ifaceCtrl = wx.TextCtrl(panel,id,"")
                ifaceCtrl.SetMinSize(minSize)
                if not evt:
                    ifaceCtrl.ChangeValue(iFace)
            portLabel = wx.StaticText(panel,-1,text.port)
            portCtrl = wx.TextCtrl(panel,id2,"")
            portCtrl.ChangeValue(port)
            dynamicSizer.Add(iFaceLabel,(0,0),(1,1),flag = wx.TOP, border = 10)
            dynamicSizer.Add(ifaceCtrl,(1,0),(1,1),flag = wx.EXPAND)
            if portCtrl:
                dynamicSizer.Add(portLabel,(0,1),(1,1),flag = wx.TOP, border = 10)
                dynamicSizer.Add(portCtrl,(1,1),(1,1))
            leftSizer.Layout()            
            if evt:
                evt.Skip()
        radioBoxMode.Bind(wx.EVT_RADIOBOX, OnHostChoice)
        OnHostChoice()

        bckgrndLbl   = wx.StaticText(panel, -1, text.bckgrnd+':')
        borderLbl    = wx.StaticText(panel, -1, text.border+':')
        fontsizeLbl  = wx.StaticText(panel, -1, text.fontsize)
        brdrwdthLbl  = wx.StaticText(panel, -1, text.brdrwdth)
        filIdlTxtLbl = wx.StaticText(panel, -1, text.idleText+':')
        filIdlBckLbl = wx.StaticText(panel, -1, text.idleBack+':')
        filActTxtLbl = wx.StaticText(panel, -1, text.activText+':')
        filActBckLbl = wx.StaticText(panel, -1, text.activBack+':')
        folIdlTxtLbl = wx.StaticText(panel, -1, text.idleText+':')
        folIdlBckLbl = wx.StaticText(panel, -1, text.idleBack+':')
        folActTxtLbl = wx.StaticText(panel, -1, text.activText+':')
        folActBckLbl = wx.StaticText(panel, -1, text.activBack+':')
        fontsizeCtrl = eg.SpinIntCtrl(panel, -1, fontsize, max = 999, min = 16)
        brdrwdthCtrl = eg.SpinIntCtrl(panel, -1, brdrwdth, max = 9, min = 0)
        bckgrndColourButton = eg.ColourSelectButton(
            panel,
            bckgrnd,
            title = text.bckgrnd,
            size = (40, -1)
        )
        borderColourButton = eg.ColourSelectButton(
            panel,
            border,
            title = text.border,
            size = (40, -1)
        )
        filIdlTxtColourButton = eg.ColourSelectButton(
            panel,
            filIdlTxt,
            title = text.idleText,
            size = (40, -1)
        )
        filIdlBckColourButton = eg.ColourSelectButton(
            panel,
            filIdlBck,
            title = text.idleBack,
            size = (40, -1)
        )
        filActTxtColourButton = eg.ColourSelectButton(
            panel,
            filActTxt,
            title = text.activText,
            size = (40, -1)
        )
        filActBckColourButton = eg.ColourSelectButton(
            panel,
            filActBck,
            title = text.activBack,
            size = (40, -1)
        )
        folIdlTxtColourButton = eg.ColourSelectButton(
            panel,
            folIdlTxt,
            title = text.idleText,
            size = (40, -1)
        )
        folIdlBckColourButton = eg.ColourSelectButton(
            panel,
            folIdlBck,
            title = text.idleBack,
            size = (40, -1)
        )
        folActTxtColourButton = eg.ColourSelectButton(
            panel,
            folActTxt,
            title = text.activText,
            size = (40, -1)
        )
        folActBckColourButton = eg.ColourSelectButton(
            panel,
            folActBck,
            title = text.activBack,
            size = (40, -1)
        )

        eg.EqualizeWidths((
            fontsizeCtrl,
            brdrwdthCtrl,
            bckgrndColourButton,
            borderColourButton,
            filIdlTxtColourButton,
            filIdlBckColourButton,
            filActTxtColourButton,
            filActBckColourButton,
            folIdlTxtColourButton,
            folIdlBckColourButton,
            folActTxtColourButton,
            folActBckColourButton,
            ))

        #Sizers
        statColorSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, self.text.design),
            wx.VERTICAL
        )
        commonStatSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, self.text.common),
            wx.VERTICAL
        )
        submenuStatSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, self.text.submenu),
            wx.VERTICAL
        )
        commandStatSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, self.text.command),
            wx.VERTICAL
        )
        commonSizer=wx.FlexGridSizer(4, 2, 5, 5)
        commonSizer.AddGrowableCol(0)
        submenuSizer=wx.FlexGridSizer(4, 2, 5, 5)
        submenuSizer.AddGrowableCol(0)
        commandSizer=wx.FlexGridSizer(4, 2, 5, 5)
        commandSizer.AddGrowableCol(0)
        commonStatSizer.Add(commonSizer,0,wx.TOP|wx.EXPAND,3)
        submenuStatSizer.Add(submenuSizer,0,wx.TOP|wx.EXPAND,3)
        commandStatSizer.Add(commandSizer,0,wx.TOP|wx.EXPAND,3)
        statColorSizer.Add(commonStatSizer,0,wx.TOP|wx.EXPAND,5)
        statColorSizer.Add(submenuStatSizer,0,wx.TOP|wx.EXPAND,5)
        statColorSizer.Add(commandStatSizer,0,wx.TOP|wx.EXPAND,5)
        mainSizer.Add(statColorSizer,0)
        commonSizer.Add(fontsizeLbl,0,wx.TOP|wx.EXPAND,2)
        commonSizer.Add(fontsizeCtrl)
        commonSizer.Add(brdrwdthLbl,0,wx.TOP|wx.EXPAND,2)
        commonSizer.Add(brdrwdthCtrl)
        commonSizer.Add(bckgrndLbl,0,wx.TOP|wx.EXPAND,2)
        commonSizer.Add(bckgrndColourButton)
        commonSizer.Add(borderLbl,0,wx.TOP|wx.EXPAND,2)
        commonSizer.Add(borderColourButton)
        submenuSizer.Add(folIdlTxtLbl,0,wx.TOP|wx.EXPAND,2)
        submenuSizer.Add(folIdlTxtColourButton)
        submenuSizer.Add(folIdlBckLbl,0,wx.TOP|wx.EXPAND,2)
        submenuSizer.Add(folIdlBckColourButton)
        submenuSizer.Add(folActTxtLbl,0,wx.TOP|wx.EXPAND,2)
        submenuSizer.Add(folActTxtColourButton)
        submenuSizer.Add(folActBckLbl,0,wx.TOP|wx.EXPAND,2)
        submenuSizer.Add(folActBckColourButton)
        commandSizer.Add(filIdlTxtLbl,0,wx.TOP|wx.EXPAND,2)
        commandSizer.Add(filIdlTxtColourButton)
        commandSizer.Add(filIdlBckLbl,0,wx.TOP|wx.EXPAND,2)
        commandSizer.Add(filIdlBckColourButton)
        commandSizer.Add(filActTxtLbl,0,wx.TOP|wx.EXPAND,2)
        commandSizer.Add(filActTxtColourButton)
        commandSizer.Add(filActBckLbl,0,wx.TOP|wx.EXPAND,2)
        commandSizer.Add(filActBckColourButton)


        def OnTitleChange(evt = None):
            val = titleCtrl.GetValue()
            flag = val != "" and\
                (val == title or val not in self.plugin.servers.iterkeys())
            panel.dialog.buttonRow.okButton.Enable(flag)
            colour = "yellow" if not flag else clr
            titleCtrl.SetBackgroundColour(colour)
            titleCtrl.Refresh()
            if evt:
                evt.Skip()
        titleCtrl.Bind(wx.EVT_TEXT, OnTitleChange)
        OnTitleChange()


        def OnTextChange(evt):
            folder = folderCtrl.GetValue()
            patterns = patternsCtrl.GetValue()
            if not patterns:
                patterns = "*.*"
            if folder:
                folderCtrl.startDirectory=folderCtrl.GetValue()
            evt.Skip()

        panel.dialog.buttonRow.testButton.Show(False)

        while panel.Affirmed():
            mode = radioBoxMode.GetSelection()
            if mode == 0:
                iFace = wx.FindWindowById(id).GetStringSelection()
            elif mode == 1:
                iFace = wx.FindWindowById(id).GetValue()
            port = wx.FindWindowById(id2).GetValue()
            bckgrnd = bckgrndColourButton.GetValue()
            border = borderColourButton.GetValue()
            fontsize = fontsizeCtrl.GetValue()
            brdrwdth = brdrwdthCtrl.GetValue()
            filIdlTxt = filIdlTxtColourButton.GetValue()
            filIdlBck = filIdlBckColourButton.GetValue()
            filActTxt = filActTxtColourButton.GetValue()
            filActBck = filActBckColourButton.GetValue()
            folIdlTxt = folIdlTxtColourButton.GetValue()
            folIdlBck = folIdlBckColourButton.GetValue()
            folActTxt = folActTxtColourButton.GetValue()
            folActBck = folActBckColourButton.GetValue()
            newData = menuCtrl.GetValue()
            newTitle = titleCtrl.GetValue()
            flag = self.plugin.StopServer(title, True)
            self.plugin.AddServerName(newTitle)
            if flag:
                self.plugin.StartServer(
                    newTitle,
                    mode,
                    iFace,
                    port,
                    bckgrnd,
                    border,
                    filIdlTxt,
                    filIdlBck,
                    filActTxt,
                    filActBck,
                    folIdlTxt,
                    folIdlBck,
                    folActTxt,
                    folActBck,
                    fontsize,
                    brdrwdth,
                    newData
                )
            panel.SetResult(
            newTitle,
            mode,
            iFace,
            port,
            bckgrnd,
            border,
            filIdlTxt,
            filIdlBck,
            filActTxt,
            filActBck,
            folIdlTxt,
            folIdlBck,
            folActTxt,
            folActBck,
            fontsize,
            brdrwdth,
            newData
        )
#===============================================================================

class StopServer(eg.ActionBase):

    class text:
        label = u"Server name:"


    def __call__(self, title = ""):
        self.plugin.StopServer(title)


    def Configure(self, title = ""):
        panel = eg.ConfigPanel()
        label = wx.StaticText(panel, -1, self.text.label)
        titleCtrl = wx.Choice(
            panel,
            -1,
            choices = tuple(self.plugin.servers.iterkeys())
        )              
        titleCtrl.SetStringSelection(title)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(label, 0, wx.TOP, 2)
        sizer.Add(titleCtrl, 0, wx.LEFT, 5)
        panel.sizer.Add(sizer, 0, wx.ALL, 20)
        while panel.Affirmed():
            panel.SetResult(titleCtrl.GetStringSelection())
#===============================================================================

class StopAllServers(eg.ActionBase):

    def __call__(self):
        self.plugin.StopAllServers()
#===============================================================================

class StartAllServers(eg.ActionBase):

    def __call__(self):
        self.plugin.StartAllServers()
#===============================================================================

class HTTPMenu(eg.PluginBase):

    servers = {}
    text = Text

    def __init__(self):
        self.AddActionsFromList(ACTIONS)


    def __start__(self):
        servActions = self.GetActions(self.text.StartServer.name)
        for title in [item.args[0] for item in servActions]:
            self.AddServerName(title)
        try:
            pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
        except pythoncom.com_error:
            pass # already initialized    


    def __stop__(self):
        for title in tuple(self.servers.iterkeys()):
            self.StopServer(title)


    def StopServer(self, title, flag = False):
        if self.servers.has_key(title) and self.servers[title]:
            address ="%s:%i" % self.servers[title].server_address
            self.servers[title].stop()
            self.servers[title] = None
            eg.PrintNotice(self.text.stopMess % (title, address))
            if flag:
                del self.servers[title]
            return True


    def StopAllServers(self):
        for title in tuple(self.servers.iterkeys()):
            self.StopServer(title)


    def StartAllServers(self):
        srvActions = self.GetActions(self.text.StartServer.name)
        for args in [itm.args for itm in srvActions if self.IsEnabled(itm)]:
            self.StartServer(*args)


    def StartServer(
        self,
        title,
        mode,
        iFace,
        port,
        bckgrnd,
        border,
        filIdlTxt,
        filIdlBck,
        filActTxt,
        filActBck,
        folIdlTxt,
        folIdlBck,
        folActTxt,
        folActBck,
        fontsize,
        brdrwdth,
        data
    ):
        iFace = eg.ParseString(iFace)
        port = int(eg.ParseString(port))
        if not mode :            
            iFace = GetIPAddress(iFace, self.text.txtAllIfaces)
        mn = Menu(data, title)
        self.StopServer(title)
        wit = HTTPmenu_thread(
            self,
            mn,
            iFace,
            port,
            title,
            convertColor(bckgrnd),
            convertColor(border),
            convertColor(filIdlTxt),
            convertColor(filIdlBck),
            convertColor(filActTxt),
            convertColor(filActBck),
            convertColor(folIdlTxt),
            convertColor(folIdlBck),
            convertColor(folActTxt),
            convertColor(folActBck),            
            fontsize,
            brdrwdth,
        )
        wit.start() 


    def AddServerName(self, title):
        if not self.servers.has_key(title):
            self.servers[title] = None


    def GetActions(self, actName):
        def Traverse(item):
            if item.__class__ == eg.document.ActionItem:
                if item.executable.name == actName and\
                item.executable.plugin.name == self.name and item.args:
                    actions.append(item)
            elif item and item.childs:
                    for child in item.childs:
                        Traverse(child)
        actions = []
        Traverse(eg.document.__dict__['root'])
        return actions


    def IsEnabled(self, item):
        def Traverse(item):
            if not item.isEnabled:
                return True
            elif item.parent:
                result = Traverse(item.parent)
                if result:
                    return result
        result = Traverse(item)
        return False if result else True


    def Configure(self, *args):
        panel = eg.ConfigPanel()
        servActions = self.GetActions(self.text.StartServer.name)
        panel.sizer.Add(
            wx.StaticText(panel, -1, self.text.listhl),
            flag = wx.ALIGN_CENTER_VERTICAL
        )
        mySizer = wx.GridBagSizer(5, 5)
       
        serverListCtrl = wx.ListCtrl(
            panel,
            -1,
            style=wx.LC_REPORT|wx.VSCROLL|wx.HSCROLL|wx.LC_HRULES|wx.LC_VRULES
        )
        for i, colLabel in enumerate(self.text.colLabels):
            serverListCtrl.InsertColumn(i, colLabel)

        def maxStr(lst):
            lngs = [len(item) for item in lst]
            return lst[lngs.index(max(lngs))]
        if servActions:
            serverListCtrl.InsertItem(0, maxStr([item.args[0] for item in servActions]))
            serverListCtrl.SetItem(0, 1, maxStr([item.args[2] for item in servActions]))
            serverListCtrl.SetItem(0, 2, "65535")
            serverListCtrl.SetItem(0, 3, maxStr((self.text.running, self.text.stopped)))
        width = SYS_VSCROLL_X + serverListCtrl.GetWindowBorderSize()[0]
        for i in range(4):
            serverListCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            width += serverListCtrl.GetColumnWidth(i)
        serverListCtrl.SetMinSize((width, -1))
        mySizer.Add(serverListCtrl, (0,0), (1, 5), flag = wx.EXPAND)

        #buttons
        abortButton = wx.Button(panel, -1, self.text.stop)
        mySizer.Add(abortButton, (1,0))
        abortAllButton = wx.Button(panel, -1, self.text.stopAll)
        mySizer.Add(abortAllButton, (1,1), flag = wx.ALIGN_CENTER_HORIZONTAL)
        restartButton = wx.Button(panel, -1, self.text.start)
        mySizer.Add(restartButton, (1,2), flag = wx.ALIGN_CENTER_HORIZONTAL)
        restartAllButton = wx.Button(panel, -1, self.text.startAll)
        mySizer.Add(restartAllButton, (1,3), flag = wx.ALIGN_CENTER_HORIZONTAL)
        refreshButton = wx.Button(panel, -1, self.text.refresh)
        mySizer.Add(refreshButton, (1,4), flag = wx.ALIGN_RIGHT)
        mySizer.AddGrowableRow(0)
        mySizer.AddGrowableCol(1)
        mySizer.AddGrowableCol(2)
        mySizer.AddGrowableCol(3)
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
       
        def PopulateList (event):
            servActions = self.GetActions(self.text.StartServer.name)
            serverListCtrl.DeleteAllItems()
            row = 0
            for args in [item.args for item in servActions if self.IsEnabled(item)]:
                serverListCtrl.InsertItem(row, args[0])
                serverListCtrl.SetItem(row, 1, args[2])
                serverListCtrl.SetItem(row, 2, args[3])
                serverListCtrl.SetItem(row,
                    3, (self.text.running, self.text.stopped)[int(self.servers[args[0]] is None)])
                row += 1
            ListSelection(wx.CommandEvent())


        def OnAbortButton(event):
            item = serverListCtrl.GetFirstSelected()
            while item != -1:
                name = serverListCtrl.GetItemText(item)
                self.StopServer(name)
                item = serverListCtrl.GetNextSelected(item)
            PopulateList(wx.CommandEvent())
            event.Skip()


        def OnAbortAllButton(event):
            self.StopAllServers()
            PopulateList(wx.CommandEvent())
            event.Skip()


        def OnRestartButton(event):
            item = serverListCtrl.GetFirstSelected()
            while item != -1:
                self.StartServer(*[i.args for i in servActions][item])
                item = serverListCtrl.GetNextSelected(item)
            PopulateList(wx.CommandEvent())
            event.Skip()


        def OnRestartAllButton(event):
            self.StartAllServers()
            PopulateList(wx.CommandEvent())
            event.Skip()


        def ListSelection(event):
            flag = serverListCtrl.GetFirstSelected() != -1
            abortButton.Enable(flag)
            restartButton.Enable(flag)
            event.Skip()
           

        def OnSize(event):
            for i in range(4):
                serverListCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            event.Skip()
        PopulateList(wx.CommandEvent())
        abortButton.Bind(wx.EVT_BUTTON, OnAbortButton)
        abortAllButton.Bind(wx.EVT_BUTTON, OnAbortAllButton)
        restartButton.Bind(wx.EVT_BUTTON, OnRestartButton)
        restartAllButton.Bind(wx.EVT_BUTTON, OnRestartAllButton)
        refreshButton.Bind(wx.EVT_BUTTON, PopulateList)
        serverListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, ListSelection)
        serverListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, ListSelection)
        panel.Bind(wx.EVT_SIZE, OnSize)
        panel.dialog.buttonRow.applyButton.Show(False)
        panel.dialog.buttonRow.cancelButton.Show(False)

        while panel.Affirmed():
            panel.SetResult(*args)
#===============================================================================

ACTIONS = (
    (
        StartServer,
        'StartServer',
        'Start HTTP server',
        'Starts HTTP server.',
        None
    ),
    (
        StartAllServers,
        'StartAllServers',
        'Start all enabled HTTP servers',
        'Starts all enabled HTTP servers.',
        None
    ),
    (
        StopServer,
        'StopServer',
        'Stop HTTP server',
        'Stops HTTP server.',
        None
    ),
    (
        StopAllServers,
        'StopAllServers',
        'Stop all HTTP servers',
        'Stops all HTTP servers.',
        None
    ),
)
#===============================================================================
