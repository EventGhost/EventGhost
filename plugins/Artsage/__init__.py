# -*- coding: utf-8 -*-
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
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.0.1 by Pako 2012-09-29 15:38 UTC+1
#     - initial version
#===============================================================================

import eg
import wx
import wx.grid as gridlib
from ctypes import c_int, c_ulong, sizeof, c_long, byref, c_buffer, Structure
from copy import deepcopy as cpy
from subprocess import Popen
from os.path import split, exists, isfile, isdir, join
from threading import Timer
from eg.WinApi.Utils import GetMonitorDimensions
from eg.WinApi.Dynamic import PostMessage, SendMessage
from win32gui import GetMenuItemCount, GetSubMenu, GetParent
from winsound import PlaySound, SND_ASYNC
from ctypes.wintypes import WinDLL
_user32 = WinDLL("user32")
from eg.Classes.MainFrame.TreeCtrl import DropTarget as EventDropTarget
from sys import getfilesystemencoding
FSE = getfilesystemencoding()
IMAGES_DIR = eg.imagesDir

WM_CLOSE      = 0x010
VK_F1         = 0x070
WM_KEYDOWN    = 0x100
WM_KEYUP      = 0x101
WM_COMMAND    = 0x111
SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
ARIAL_INFO    = "0;-35;0;0;0;700;0;0;0;0;3;2;1;34;Arial"
TAHOMA_INFO   = "0;-27;0;0;0;400;0;0;0;0;3;2;1;34;Tahoma"
ROOT          = (0,2,3,4,6,7,8,9,10,17,18,19,20,22,23,24,26,27)
IXS           = (None,0,1,2,3,4,5,6,7,13,14,15,16,17,18,19,20,21)

HWND = eg.WindowMatcher(
    u'artsage{*}.exe',
    None,
    u'#32770',
    None,
    None,
    None,
    True,
    0.0,
    2
)

AScatalog = eg.WindowMatcher(
    u'artsage{*}.exe',
    u'{*} - ArtSage Catalog',
    u'#32770',
    u'Catalog',
    u'SysListView32',
    None,
    True,
    0.0,
    0
)
#===============================================================================

eg.RegisterPlugin(
    name="Artsage",
    author = "Pako",
    version = "0.0.1",
    guid = "{FD304FE6-C4F8-4356-BEC2-E786741DD1EB}",
    kind = "program",
    createMacrosOnAdd = True,
    description = (
        'Adds actions to control '
        '<a href="http://www.xworks.ca/artsage/index.html">'
        'ArtSage</a> - small graphics viewer.'
    ),
    help = """
        Adds actions to control
        <a href="http://www.xworks.ca/artsage/index.html">
        ArtSage</a>.""",
    icon = (
        "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"
        "RK5CYII="
    )
)
#===============================================================================

class MyDirBrowseButton(eg.DirBrowseButton):

    def GetTextCtrl(self):
        return self.textControl
#===============================================================================

class MenuGrid(gridlib.Grid):

    def __init__(self, parent, lngth):
        gridlib.Grid.__init__(self, parent)
        self.SetRowLabelSize(0)
        self.SetColLabelSize(0)
        self.SetDefaultRowSize(16)
        self.SetScrollLineX(1)
        self.SetScrollLineY(1)
        self.EnableEditing(False)
        self.EnableDragColSize(False)
        self.EnableDragRowSize(False)
        self.EnableDragGridSize(False)
        self.EnableGridLines(False)
        self.SetColMinimalAcceptableWidth(8)
        self.CreateGrid(lngth, 3)
        attr = gridlib.GridCellAttr()
        attr.SetAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
        self.SetColAttr(1,attr)
        self.SetSelectionMode(gridlib.Grid.wxGridSelectRows)
        self.Bind(gridlib.EVT_GRID_CMD_SELECT_CELL, self.onGridSelectCell, self)


    def SetBackgroundColour(self, colour):
        self.SetDefaultCellBackgroundColour(colour)


    def SetForegroundColour(self, colour):
        self.SetDefaultCellTextColour(colour)


    def SetFont(self, font):
        self.SetDefaultCellFont(font)


    def GetSelection(self):
        return self.GetSelectedRows()[0]


    def Set(self, choices):
        oldLen = self.GetNumberRows()
        newLen = len(choices)
        h = self.GetDefaultRowSize()
        if oldLen > newLen:
            self.DeleteRows(0, oldLen-newLen, False)
        elif oldLen < newLen:
            self.AppendRows(newLen-oldLen, False)
        for i in range(len(choices)):
            chr = u"\u25a0" if choices[i][2] else ""
            self.SetCellValue(i,0,chr)
            self.SetCellValue(i,1," "+choices[i][0])
            chr = u"\u25ba" if choices[i][3] == -1 else ""
            self.SetCellValue(i,2, chr)
            self.SetRowSize(i,h)


    def onGridSelectCell(self, event):
        row = event.GetRow()
        self.SelectRow(row)
        if not self.IsVisible(row,1):
            self.MakeCellVisible(row,1)
        event.Skip()


    def MoveCursor(self, step):
        max = self.GetNumberRows()
        sel = self.GetSelectedRows()[0]
        new = sel + step
        if new < 0:
            new += max
        elif new > max-1:
            new -= max
        self.SetGridCursor(new, 1)
        self.SelectRow(new)
#===============================================================================

class MyTextDropTarget(EventDropTarget):

    def __init__(self, object):
        EventDropTarget.__init__(self, object)
        self.object = object


    def OnDragOver(self, x, y, dragResult):
        return wx.DragMove


    def OnData(self, dummyX, dummyY, dragResult):
        if self.GetData() and self.customData.GetDataSize() > 0:
            txt = self.customData.GetData()
            ix, evtList = self.object.GetEvtList()
            flag = True
            for lst in evtList:
                if txt in lst:
                    flag = False
                    break
            if flag:
                self.object.InsertImageStringItem(len(evtList[ix]), txt, 0)
                self.object.UpdateEvtList(ix, txt)
            else:
                PlaySound('SystemExclamation', SND_ASYNC)


    def OnLeave(self):
        pass
#===============================================================================

class EventListCtrl(wx.ListCtrl):

    def __init__(self, parent, id, evtList, ix, plugin):
        width = 205
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | 
            wx.LC_NO_HEADER | wx.LC_SINGLE_SEL, size = (width, -1))
        self.parent = parent
        self.id = id
        self.evtList = evtList
        self.ix = ix
        self.plugin = plugin
        self.sel = -1
        self.il = wx.ImageList(16, 16)
        self.il.Add(wx.BitmapFromImage(
            wx.Image(join(IMAGES_DIR, "event.png"),
            wx.BITMAP_TYPE_PNG)
        ))
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.InsertColumn(0, '')
        self.SetColumnWidth(0, width - 5 - SYS_VSCROLL_X)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        self.Bind(wx.EVT_SET_FOCUS, self.OnChange) 
        self.Bind(wx.EVT_LIST_INSERT_ITEM, self.OnChange) 
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnChange) 
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClick)
        self.SetToolTipString(self.plugin.text.toolTip)


    def OnSelect(self, event):
        self.sel = event.GetIndex()
        evt = eg.ValueChangedEvent(self.id, value = self)
        wx.PostEvent(self, evt)
        event.Skip()


    def OnChange(self, event):
        evt = eg.ValueChangedEvent(self.id, value = self)
        wx.PostEvent(self, evt)
        event.Skip()


    def OnRightClick(self, event):
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.Bind(wx.EVT_MENU, self.OnDeleteButton, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnDeleteAllButton, id=self.popupID2)
        # make a menu
        menu = wx.Menu()
        # add some items
        menu.Append(self.popupID1, self.plugin.text.popup[0])
        menu.Append(self.popupID2, self.plugin.text.popup[1])
        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()


    def OnDeleteButton(self, event=None):
        self.DeleteItem(self.sel)
        self.evtList[self.ix].pop(self.sel)
        evt = eg.ValueChangedEvent(self.id, value = self)
        wx.PostEvent(self, evt)       
        if event:
            event.Skip()
        

    def OnDeleteAllButton(self, event=None):
        self.DeleteAllItems()
        evt = eg.ValueChangedEvent(self.id, value = self)
        wx.PostEvent(self, evt)
        self.evtList[self.ix] = []
        if event:
            event.Skip()


    def GetEvtList(self):
        return self.ix, self.evtList


    def UpdateEvtList(self, ix, txt):
        self.evtList[ix].append(txt)


    def SetItems(self, evtList):
        for i in range(len(evtList)):
            self.InsertImageStringItem(i, evtList[i], 0) 
#===============================================================================

class MenuEventsDialog(wx.MiniFrame):

    def __init__(self, parent, plugin):
        wx.MiniFrame.__init__(
            self,
            parent,
            -1,
            style=wx.CAPTION,
            name="Menu events dialog"
        )
        self.panel = parent
        self.plugin = plugin
        self.evtList = cpy(self.panel.evtList)
        self.SetBackgroundColour(wx.NullColour)
        self.ctrl = None
        self.sel = -1


    def ShowMenuEventsDialog(self, title, labels):
        self.panel.Enable(False)
        self.panel.dialog.buttonRow.cancelButton.Enable(False)
        self.panel.EnableButtons(False)
        self.SetTitle(title)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.SetMinSize((450, 308))
        topSizer=wx.GridBagSizer(2, 20)
        textLbl_0=wx.StaticText(self, -1, labels[0])        
        id = wx.NewId()
        eventsCtrl_0 = EventListCtrl(self, id, self.evtList, 0, self.plugin)
        eventsCtrl_0.SetItems(self.evtList[0])
        dt0 = MyTextDropTarget(eventsCtrl_0)
        eventsCtrl_0.SetDropTarget(dt0)
        textLbl_1=wx.StaticText(self, -1, labels[1])       
        id = wx.NewId()        
        eventsCtrl_1 = EventListCtrl(self, id, self.evtList, 1, self.plugin)
        eventsCtrl_1.SetItems(self.evtList[1])
        dt1 = MyTextDropTarget(eventsCtrl_1)
        eventsCtrl_1.SetDropTarget(dt1)
        textLbl_2=wx.StaticText(self, -1, labels[2])        
        id = wx.NewId()
        eventsCtrl_2 = EventListCtrl(self, id, self.evtList, 2, self.plugin)
        eventsCtrl_2.SetItems(self.evtList[2])
        dt2 = MyTextDropTarget(eventsCtrl_2)
        eventsCtrl_2.SetDropTarget(dt2)
        textLbl_3=wx.StaticText(self, -1, labels[3])        
        id = wx.NewId()        
        eventsCtrl_3 = EventListCtrl(self, id, self.evtList, 3, self.plugin)
        eventsCtrl_3.SetItems(self.evtList[3])
        dt3 = MyTextDropTarget(eventsCtrl_3)
        eventsCtrl_3.SetDropTarget(dt3)
        textLbl_4=wx.StaticText(self, -1, labels[4])        
        id = wx.NewId()
        eventsCtrl_4 = EventListCtrl(self, id, self.evtList, 4, self.plugin)
        eventsCtrl_4.SetItems(self.evtList[4])
        dt4 = MyTextDropTarget(eventsCtrl_4)
        eventsCtrl_4.SetDropTarget(dt4)
        deleteSizer = wx.BoxSizer(wx.VERTICAL)
        delOneBtn = wx.Button(self, -1, self.plugin.text.popup[0])
        delBoxBtn = wx.Button(self, -1, self.plugin.text.popup[1])
        clearBtn  = wx.Button(self, -1, self.plugin.text.clear)
        deleteSizer.Add(delOneBtn, 1, wx.EXPAND)
        deleteSizer.Add(delBoxBtn, 1, wx.EXPAND|wx.TOP,5)
        deleteSizer.Add(clearBtn, 1, wx.EXPAND|wx.TOP,5)
        
        topSizer.Add(textLbl_0, (0,0))
        topSizer.Add(eventsCtrl_0, (1,0), flag = wx.EXPAND)
        topSizer.Add(textLbl_1, (0,1))
        topSizer.Add(eventsCtrl_1, (1,1), flag = wx.EXPAND)
        topSizer.Add(textLbl_2, (2,0),flag = wx.TOP, border = 8)
        topSizer.Add(eventsCtrl_2, (3,0), flag = wx.EXPAND)
        topSizer.Add(textLbl_3, (2,1), flag = wx.TOP, border = 8)
        topSizer.Add(eventsCtrl_3, (3,1), flag = wx.EXPAND)
        topSizer.Add(textLbl_4, (4,0), flag = wx.TOP, border = 8)
        topSizer.Add(eventsCtrl_4, (5,0), flag = wx.EXPAND)
        topSizer.Add(deleteSizer, (5,1), flag = wx.EXPAND)

        line = wx.StaticLine(
            self,
            -1,
            size=(20,-1),
            pos = (200,0),
            style=wx.LI_HORIZONTAL
        )
        btn1 = wx.Button(self, wx.ID_OK)
        btn1.SetLabel(self.plugin.text.ok)
        btn1.SetDefault()
        btn2 = wx.Button(self, wx.ID_CANCEL)
        btn2.SetLabel(self.plugin.text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add(topSizer,0,wx.ALL,10)
        sizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        sizer.Add((1,6))
        self.SetSizer(sizer)
        sizer.Fit(self)


        def onFocus(evt):
            ctrl = evt.GetValue()
            if ctrl != self.ctrl:
                if self.ctrl:
                    self.ctrl.SetItemState(
                        -1,
                        wx.LIST_MASK_STATE,
                        wx.LIST_STATE_SELECTED
                    )
                self.ctrl = ctrl
            sel = self.ctrl.sel
            if sel != -1:
                self.sel = sel
            flag = self.ctrl.GetSelectedItemCount() > 0
            delOneBtn.Enable(flag)
            delBoxBtn.Enable(flag)
            evt.Skip()
        eventsCtrl_0.Bind(eg.EVT_VALUE_CHANGED, onFocus)        
        eventsCtrl_1.Bind(eg.EVT_VALUE_CHANGED, onFocus)        
        eventsCtrl_2.Bind(eg.EVT_VALUE_CHANGED, onFocus)        
        eventsCtrl_3.Bind(eg.EVT_VALUE_CHANGED, onFocus)        
        eventsCtrl_4.Bind(eg.EVT_VALUE_CHANGED, onFocus)      
      

        def onDelOneBtn(evt):
            self.ctrl.OnDeleteButton()
            delOneBtn.Enable(False)
            delBoxBtn.Enable(False)
            evt.Skip()
        delOneBtn.Bind(wx.EVT_BUTTON, onDelOneBtn)
        

        def onDelBoxBtn(evt):
            self.ctrl.OnDeleteAllButton()
            delOneBtn.Enable(False)
            delBoxBtn.Enable(False)
            evt.Skip()
        delBoxBtn.Bind(wx.EVT_BUTTON, onDelBoxBtn)


        def onClearBtn(evt):
            eventsCtrl_0.DeleteAllItems()
            eventsCtrl_1.DeleteAllItems()
            eventsCtrl_2.DeleteAllItems()
            eventsCtrl_3.DeleteAllItems()
            eventsCtrl_4.DeleteAllItems()
            delOneBtn.Enable(False)
            delBoxBtn.Enable(False)
            self.evtList = [[],[],[],[],[]]
            evt.Skip()
        clearBtn.Bind(wx.EVT_BUTTON, onClearBtn)


        def onClose(evt):
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()
            self.panel.setFocus()
        self.Bind(wx.EVT_CLOSE, onClose)
        

        def onCancel(evt):
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.Close()
        btn2.Bind(wx.EVT_BUTTON,onCancel)
        

        def onOK(evt):
            self.panel.evtList = self.evtList
            self.Close()
        btn1.Bind(wx.EVT_BUTTON,onOK)
        
        sizer.Layout()
        self.Raise()
        self.Show()
#===============================================================================

class CatalogEventsDialog(wx.MiniFrame):

    def __init__(self, parent, plugin):
        wx.MiniFrame.__init__(
            self,
            parent,
            -1,
            style=wx.CAPTION,
            name="Catalog events dialog"
        )
        self.panel = parent
        self.plugin = plugin
        self.evtList = cpy(self.panel.evtList)
        self.SetBackgroundColour(wx.NullColour)
        self.ctrl = None
        self.sel = -1


    def ShowCatalogEventsDialog(self, title, labels):
        self.panel.Enable(False)
        self.panel.dialog.buttonRow.cancelButton.Enable(False)
        self.panel.EnableButtons(False)
        self.SetTitle(title)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.SetMinSize((450, 308))
        topSizer=wx.GridBagSizer(2, 20)
        textLbl_0=wx.StaticText(self, -1, labels[0])        
        id = wx.NewId()
        eventsCtrl_0 = EventListCtrl(self, id, self.evtList, 0, self.plugin)
        eventsCtrl_0.SetItems(self.evtList[0])
        dt0 = MyTextDropTarget(eventsCtrl_0)
        eventsCtrl_0.SetDropTarget(dt0)
        textLbl_1=wx.StaticText(self, -1, labels[1])       
        id = wx.NewId()        
        eventsCtrl_1 = EventListCtrl(self, id, self.evtList, 1, self.plugin)
        eventsCtrl_1.SetItems(self.evtList[1])
        dt1 = MyTextDropTarget(eventsCtrl_1)
        eventsCtrl_1.SetDropTarget(dt1)
        textLbl_2=wx.StaticText(self, -1, labels[2])        
        id = wx.NewId()
        eventsCtrl_2 = EventListCtrl(self, id, self.evtList, 2, self.plugin)
        eventsCtrl_2.SetItems(self.evtList[2])
        dt2 = MyTextDropTarget(eventsCtrl_2)
        eventsCtrl_2.SetDropTarget(dt2)
        textLbl_3=wx.StaticText(self, -1, labels[3])        
        id = wx.NewId()        
        eventsCtrl_3 = EventListCtrl(self, id, self.evtList, 3, self.plugin)
        eventsCtrl_3.SetItems(self.evtList[3])
        dt3 = MyTextDropTarget(eventsCtrl_3)
        eventsCtrl_3.SetDropTarget(dt3)
        textLbl_4=wx.StaticText(self, -1, labels[4])        
        id = wx.NewId()
        eventsCtrl_4 = EventListCtrl(self, id, self.evtList, 4, self.plugin)
        eventsCtrl_4.SetItems(self.evtList[4])
        dt4 = MyTextDropTarget(eventsCtrl_4)
        eventsCtrl_4.SetDropTarget(dt4)
        textLbl_5=wx.StaticText(self, -1, labels[5])        
        id = wx.NewId()
        eventsCtrl_5 = EventListCtrl(self, id, self.evtList, 5, self.plugin)
        eventsCtrl_5.SetItems(self.evtList[5])
        dt5 = MyTextDropTarget(eventsCtrl_5)
        eventsCtrl_5.SetDropTarget(dt5)
        deleteSizer = wx.BoxSizer(wx.VERTICAL)
        delOneBtn = wx.Button(self, -1, self.plugin.text.popup[0])
        delBoxBtn = wx.Button(self, -1, self.plugin.text.popup[1])
        clearBtn  = wx.Button(self, -1, self.plugin.text.clear)
        eg.EqualizeWidths((delOneBtn, delBoxBtn, clearBtn))
        deleteSizer.Add(delOneBtn, 0, wx.ALIGN_RIGHT)
        deleteSizer.Add(delBoxBtn, 0, wx.ALIGN_RIGHT|wx.TOP,5)
        deleteSizer.Add(clearBtn, 0, wx.ALIGN_RIGHT|wx.TOP,5) 
        topSizer.Add(textLbl_0, (0,0))
        topSizer.Add(eventsCtrl_0, (1,0), flag = wx.EXPAND)
        topSizer.Add(textLbl_1, (0,1))
        topSizer.Add(eventsCtrl_1, (1,1), flag = wx.EXPAND)
        topSizer.Add(textLbl_2, (2,0),flag = wx.TOP, border = 8)
        topSizer.Add(eventsCtrl_2, (3,0), flag = wx.EXPAND)
        topSizer.Add(textLbl_3, (2,1), flag = wx.TOP, border = 8)
        topSizer.Add(eventsCtrl_3, (3,1), flag = wx.EXPAND)
        topSizer.Add(textLbl_4, (4,0), flag = wx.TOP, border = 8)
        topSizer.Add(eventsCtrl_4, (5,0), flag = wx.EXPAND)
        topSizer.Add(textLbl_5, (4,1), flag = wx.TOP, border = 8)
        topSizer.Add(eventsCtrl_5, (5,1), flag = wx.EXPAND)
        topSizer.Add(deleteSizer, (6,1), flag = wx.TOP|wx.EXPAND, border = 8)

        line = wx.StaticLine(
            self,
            -1,
            size=(20,-1),
            pos = (200,0),
            style=wx.LI_HORIZONTAL
        )
        btn1 = wx.Button(self, wx.ID_OK)
        btn1.SetLabel(self.plugin.text.ok)
        btn1.SetDefault()
        btn2 = wx.Button(self, wx.ID_CANCEL)
        btn2.SetLabel(self.plugin.text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add(topSizer,0,wx.ALL,10)
        sizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        sizer.Add((1,6))
        self.SetSizer(sizer)
        sizer.Fit(self)


        def onFocus(evt):
            ctrl = evt.GetValue()
            if ctrl != self.ctrl:
                if self.ctrl:
                    self.ctrl.SetItemState(
                        -1,
                        wx.LIST_MASK_STATE,
                        wx.LIST_STATE_SELECTED
                    )
                self.ctrl = ctrl
            sel = self.ctrl.sel
            if sel != -1:
                self.sel = sel
            flag = self.ctrl.GetSelectedItemCount() > 0
            delOneBtn.Enable(flag)
            delBoxBtn.Enable(flag)
            evt.Skip()
        eventsCtrl_0.Bind(eg.EVT_VALUE_CHANGED, onFocus)        
        eventsCtrl_1.Bind(eg.EVT_VALUE_CHANGED, onFocus)        
        eventsCtrl_2.Bind(eg.EVT_VALUE_CHANGED, onFocus)        
        eventsCtrl_3.Bind(eg.EVT_VALUE_CHANGED, onFocus)        
        eventsCtrl_4.Bind(eg.EVT_VALUE_CHANGED, onFocus)   
        eventsCtrl_5.Bind(eg.EVT_VALUE_CHANGED, onFocus)   
      

        def onDelOneBtn(evt):
            self.ctrl.OnDeleteButton()
            delOneBtn.Enable(False)
            delBoxBtn.Enable(False)
            evt.Skip()
        delOneBtn.Bind(wx.EVT_BUTTON, onDelOneBtn)
        

        def onDelBoxBtn(evt):
            self.ctrl.OnDeleteAllButton()
            delOneBtn.Enable(False)
            delBoxBtn.Enable(False)
            evt.Skip()
        delBoxBtn.Bind(wx.EVT_BUTTON, onDelBoxBtn)


        def onClearBtn(evt):
            eventsCtrl_0.DeleteAllItems()
            eventsCtrl_1.DeleteAllItems()
            eventsCtrl_2.DeleteAllItems()
            eventsCtrl_3.DeleteAllItems()
            eventsCtrl_4.DeleteAllItems()
            eventsCtrl_5.DeleteAllItems()
            delOneBtn.Enable(False)
            delBoxBtn.Enable(False)
            self.evtList = [[],[],[],[],[],[]]
            evt.Skip()
        clearBtn.Bind(wx.EVT_BUTTON, onClearBtn)


        def onClose(evt):
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)
        

        def onCancel(evt):
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.Close()
        btn2.Bind(wx.EVT_BUTTON,onCancel)
        

        def onOK(evt):
            self.panel.evtList = self.evtList
            self.Close()
        btn1.Bind(wx.EVT_BUTTON,onOK)
        
        sizer.Layout()
        self.Raise()
        self.Show()
#===============================================================================

class Menu(wx.Frame):

    def __init__(
        self,
        fore,
        back,
        foreSel,
        backSel,
        fontInfo,
        flag,
        plugin,
        monitor,
        hWnd,
        evtList,
        submenu,
        ):
        wx.Frame.__init__(
            self,
            None,
            -1,
            'Artsage_menu',
            style = wx.STAY_ON_TOP|wx.SIMPLE_BORDER
        )
        self.level = 0
        self.levels = [0, 0, 0]
        self.ixs = [0, 0, 0]
        self.flag = False
        self.monitor = 0
        self.fore     = fore
        self.back     = back
        self.foreSel  = foreSel
        self.backSel  = backSel
        self.fontInfo = fontInfo
        self.flag     = flag
        self.plugin   = plugin
        self.monitor  = monitor
        self.hWnd     = hWnd
        self.evtList  = evtList
        eg.TriggerEvent(
            "OnScreenMenu.%s" % self.plugin.text.opened,
            prefix = "Artsage"
        )
        if self.plugin.asCat:
            self.plugin.unBindCatEvents()
        for evt in self.evtList[0]:
            eg.Bind(evt, self.onUp)
        for evt in self.evtList[1]:
            eg.Bind(evt, self.onDown)
        for evt in self.evtList[2]:
            eg.Bind(evt, self.onLeft)
        for evt in self.evtList[3]:
            eg.Bind(evt, self.onRight)
        for evt in self.evtList[4]:
            eg.Bind(evt, self.onEscape)
        
        if submenu > 0:
            self.ixs[0] = IXS[ROOT.index(submenu)]
            self.menuHwnd, self.menu = self.GetSubMenuExt(
                self.hWnd,
                submenu,
                True
            )
        else:
            self.menuHwnd, self.menu = self.plugin.GetAS_Menu(self.hWnd)
        self.items = self.plugin.GetItemList(self.menuHwnd, self.menu)
        self.choices = [item[0] for item in self.items]
        self.menuGridCtrl = MenuGrid(self, len(self.choices))
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        mainSizer.Add(self.menuGridCtrl, 0, wx.EXPAND)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(
            gridlib.EVT_GRID_CMD_CELL_LEFT_DCLICK,
            self.onDoubleClick,
            self.menuGridCtrl
        )
        self.Bind(wx.EVT_CHAR_HOOK, self.onFrameCharHook)
        font = wx.FontFromNativeInfoString(fontInfo)
        self.menuGridCtrl.SetFont(font)
        arial = wx.FontFromNativeInfoString(ARIAL_INFO)
        self.SetFont(font)            
        hght = self.GetTextExtent('X')[1]
        for n in range(1, 1000):
            arial.SetPointSize(n)
            self.SetFont(arial)
            h = self.GetTextExtent(u"\u25a0")[1]
            if h > hght:
                break
        arial.SetPointSize(2*n/3)
        self.SetFont(arial)            
        self.w0 = 2 * self.GetTextExtent(u"\u25a0")[0]
        attr = gridlib.GridCellAttr()
        attr.SetFont(arial)
        attr.SetAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.menuGridCtrl.SetColAttr(0,attr)
        for n in range(1,1000):
            arial.SetPointSize(n)
            self.SetFont(arial)
            h = self.GetTextExtent(u"\u25ba")[1]
            if h > hght:
                break
        arial.SetPointSize(n/2)
        self.SetFont(arial)            
        self.w2 = 2 * self.GetTextExtent(u"\u25ba")[0]
        attr = gridlib.GridCellAttr()
        attr.SetFont(arial)
        attr.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
        self.menuGridCtrl.SetColAttr(2,attr)
        self.SetFont(font)                        
        self.SetBackgroundColour((0, 0, 0))
        self.menuGridCtrl.SetBackgroundColour(self.back)
        self.menuGridCtrl.SetForegroundColour(self.fore)
        self.menuGridCtrl.SetSelectionBackground(self.backSel)
        self.menuGridCtrl.SetSelectionForeground(self.foreSel)
        if self.flag:
            self.timer=MyTimer(t = 5.0, plugin = self.plugin)
        self.menuGridCtrl.Set(self.items)

        self.DrawMenu(0) 
        self.plugin.menuDlg = self
        wx.Yield()


    def DrawMenu(self, ix):
        self.Show(False)
        self.menuGridCtrl.SetGridCursor(ix, 1)
        self.menuGridCtrl.SelectRow(ix)
        monDim = GetMonitorDimensions()
        try:
            x,y,ws,hs = monDim[self.monitor]
        except IndexError:
            x,y,ws,hs = monDim[0]
        # menu height calculation:                                
        h=self.GetCharHeight()+4
        for i in range(len(self.choices)):
            self.menuGridCtrl.SetRowSize(i,h)
            self.menuGridCtrl.SetCellValue(i,1," "+self.choices[i])
            if self.items[i][3] == -1:
                self.menuGridCtrl.SetCellValue(i,2, u"\u25ba")
        height0 = len(self.choices)*h
        height1 = h*((hs-20)/h)
        height = min(height0, height1)+6
        # menu width calculation:
        width_lst=[]
        for item in self.choices:
            width_lst.append(self.GetTextExtent(item+' ')[0])
        width = max(width_lst)+8
        self.menuGridCtrl.SetColSize(0,self.w0)
        self.menuGridCtrl.SetColSize(1,width)
        self.menuGridCtrl.SetColSize(2,self.w2)
        self.menuGridCtrl.ForceRefresh()
        width = width + self.w0 + self.w2
        if height1 < height0:
            width += SYS_VSCROLL_X
        if width > ws-50:
            if height + SYS_HSCROLL_Y < hs:
                height += SYS_HSCROLL_Y
            width = ws-50
        width += 6
        x_pos = x + (ws - width)/2
        y_pos = y + (hs - height)/2
        self.SetDimensions(x_pos,y_pos,width,height)
        self.menuGridCtrl.SetDimensions(2, 2, width-6, height-6, wx.SIZE_AUTO)
        self.Show(True)
        self.Raise()


    def UpdateMenu(self, root = False, ix = 0, up = True):
        if root or (not up and self.level == 1):
            self.menuHwnd, self.menu = self.plugin.GetAS_Menu(self.hWnd)
            self.level = 0
        else:
            self.menuHwnd, self.menu = self.GetSubMenuExt(self.hWnd, ix, up)

        
        self.items = self.plugin.GetItemList(self.menuHwnd, self.menu)
        if len(self.items)==0:
            PlaySound('SystemExclamation', SND_ASYNC)
            eg.PrintError("Please report: %i, %i, %i, %i" % (
                ix,
                int(root),
                self.menuHwnd,
                self.menu
            ))
        else:
            self.choices = [item[0] for item in self.items]
            self.menuGridCtrl.Set(self.items)
            ix = 0 if up else self.ixs[self.level]
            self.DrawMenu(ix)  


    def MoveCursor(self, step):
        max=len(self.choices)
        if max > 0:
            self.menuGridCtrl.MoveCursor(step)


    def onUp(self, event):
        wx.CallAfter(self.menuGridCtrl.MoveCursor, -1)
        

    def onDown(self, event):
        wx.CallAfter(self.menuGridCtrl.MoveCursor, 1)
        

    def onLeft(self, event):
        if self.level > 0:
            wx.CallAfter(self.UpdateMenu, False, 0, False)
        else:
            wx.CallAfter(self.destroyMenu)
        

    def onRight(self, event):
        wx.CallAfter(self.DefaultAction)
        

    def onEscape(self, event):
        wx.CallAfter(self.destroyMenu)
        

    def GetSubMenuExt(self, hWnd, ix, up):
        menu, hMenu = self.plugin.GetAS_Menu(hWnd)
        if menu:
            if up:
                if self.level > 0:
                    hMenu = _user32.GetSubMenu(hMenu, self.levels[0])
                if self.level > 1:
                    hMenu = _user32.GetSubMenu(hMenu, self.levels[1])
                self.levels[self.level] = ix
                self.level += 1
                hMenu = _user32.GetSubMenu(hMenu, ix)
                return (menu, hMenu)
            else: #down
                self.level -= 1
                hMenu = _user32.GetSubMenu(hMenu, self.levels[0])
                if self.level > 1:
                    hMenu = _user32.GetSubMenu(hMenu, self.levels[1])
                return (menu, hMenu)
                

    def DefaultAction(self):
        sel = self.menuGridCtrl.GetSelection()
        self.ixs[self.level] = sel
        item = self.items[sel]
        id = item[3]
        if id != -1:
            self.destroyMenu()
            if not self.plugin.asCat:
                hwnd = self.hWnd
            elif id > 2:
                hwnd = self.plugin.GetArtsage3() # Main window when Catalog is opened
            else:
                hwnd = GetParent(self.hWnd)      # Catalog window
            PostMessage(hwnd, WM_COMMAND, id, 0)
        else:
            wx.CallAfter(self.UpdateMenu, False, item[1], True)


    def onFrameCharHook(self, event):
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_F4:
            if event.AltDown():
                self.destroyMenu()
        elif keyCode == wx.WXK_RETURN or keyCode == wx.WXK_NUMPAD_ENTER:
            self.DefaultAction()
        elif keyCode == wx.WXK_RIGHT or keyCode == wx.WXK_NUMPAD_RIGHT:
            self.DefaultAction()
        elif keyCode == wx.WXK_ESCAPE:
            self.destroyMenu()
        elif keyCode == wx.WXK_UP or keyCode == wx.WXK_NUMPAD_UP:
            self.menuGridCtrl.MoveCursor(-1)
        elif keyCode == wx.WXK_DOWN or keyCode == wx.WXK_NUMPAD_DOWN:
            self.menuGridCtrl.MoveCursor(1)
        elif keyCode == wx.WXK_LEFT or keyCode == wx.WXK_NUMPAD_LEFT:
            self.onLeft(event)
        else:
            event.Skip()


    def onDoubleClick(self, event):
        self.DefaultAction()
        event.Skip()


    def onClose(self, event):
        self.Show(False)
        self.Destroy()
        self.plugin.menuDlg = None


    def destroyMenu(self, event = None):
        for evt in self.evtList[0]:
            eg.Unbind(evt, self.onUp)
        for evt in self.evtList[1]:
            eg.Unbind(evt, self.onDown)
        for evt in self.evtList[2]:
            eg.Unbind(evt, self.onLeft)
        for evt in self.evtList[3]:
            eg.Unbind(evt, self.onRight)
        for evt in self.evtList[4]:
            eg.Unbind(evt, self.onEscape)
        if self.plugin.asCat:
            self.plugin.bindCatEvents()
        if self.flag:
            self.timer.Cancel()
        eg.TriggerEvent(
            "OnScreenMenu.%s" % self.plugin.text.closed,
            prefix = "Artsage"
        )
        self.Close()
#===============================================================================

class MyTimer():
    def __init__(self, t, plugin):
        self.timer = Timer(t, self.Run)
        self.plugin = plugin
        self.timer.start()


    def Run(self):
        try:
            self.plugin.menuDlg.Close()
            self.plugin.menuDlg = None
        except:
            pass


    def Cancel(self):
        self.timer.cancel()
#===============================================================================

class Text:
    label1 = "Artsage folder:"
    text1 = "Couldn't find Artsage window !"
    browseTitle = "Selected folder:"
    toolTipFolder = "Press button and browse to select folder ..."
    boxTitle = "Message from EventGhost:"
    boxMessage1 = 'Folder "%s" is incorrect.\nMissing file %s !'
    toolTip = "Drag-and-drop an event from the log into the box."
    popup = (
        "Delete item",
        "Delete all items",
    )
    clear  = "Clear all"
    opened = "Opened"
    closed = "Closed"
    ok = "OK"
    cancel = "Cancel"
    dialog = "Catalog events ..."
    btnToolTip = """Press this button to assign events to control the Catalog !!!"""
    evtAssignTitle = "Catalog control - events assignement"
    events = (
        "Cursor up:",
        "Cursor down:",
        "Cursor left:",
        "Cursor right:",
        "Select (Enter):",
        "Cancel (Escape):",
    )    
#===============================================================================

class Artsage(eg.PluginBase):
    text=Text
    menuDlg = None
    submenus = None
    asCat = None


    def GetArtsage(self):
        return HWND()


    def GetArtsage2(self):
        return [self.asCat] if self.asCat else HWND()
        

    def GetArtsage3(self):
        all = HWND()
        cat = AScatalog()
        for hwnd in all:
            if hwnd not in [GetParent(item) for item in cat]:
                return hwnd        


    def GetAScatalog(self):
        return AScatalog()


    def GetAS_Menu(self, hwnd):

        WM_CONTEXTMENU   = 0x007B
        OBJID_CLIENT     = 0xFFFFFFFC

        class RECT(Structure):
            _fields_ = [
                ('left', c_long),
                ('top', c_long),
                ('right', c_long),
                ('bottom', c_long),
            ]

        class MENUBARINFO(Structure):
            _fields_ = [
                ('cbSize',  c_ulong),
                ('rcBar',  RECT),            # rect of bar, popup, item
                ('hMenu',  c_long),          # real menu handle of bar, popup
                ('hwndMenu',  c_long),       # hwnd of item submenu if one
                ('fBarFocused',  c_int, 1),  # bar, popup has the focus
                ('fFocused',  c_int, 1),     # item has the focus
            ]

        findMenu = eg.WindowMatcher(
                    u'Artsage{*}.exe',
                    None,
                    u'#32768',
                    None,
                    None,
                    None,
                    True,
                    0.0,
                    0
                )

        #PostMessage(hwnd, WM_CONTEXTMENU, hwnd, 0x00010001)
        #above method unfortunately does not work for Catalog window
        PostMessage(hwnd, WM_KEYDOWN, VK_F1, 0x003B0001) #F1 keydown
        PostMessage(hwnd,   WM_KEYUP, VK_F1, 0xC03B0001) #F1 keyup

        menu = []
        i = 0
        while len(menu) == 0:
            menu = findMenu()
            i += 1
            if i > 1000:
                break
        if menu:
            menu = menu[0]
            mbi = MENUBARINFO()
            mbi.cbSize = sizeof(mbi)
            if _user32.GetMenuBarInfo(
                menu,
                OBJID_CLIENT,
                0,
                byref(mbi)
            ):
                return (menu, mbi.hMenu)
        return (None, None)


    def GetItemList(self, hWnd, hMenu):
        WM_INITMENUPOPUP = 0x0117
        MF_BYPOSITION    = 1024
        MF_GRAYED        = 1
        MF_DISABLED      = 2
        MF_CHECKED       = 8
        MF_SEPARATOR     = 2048
        SendMessage(hWnd, WM_INITMENUPOPUP, hMenu, 0) #REFRESH MENU STATE !!!
        itemList = []
        itemName = c_buffer("\000" * 128)
        count = GetMenuItemCount(hMenu)
        for i in range(count):
            _user32.GetMenuStringA(c_int(hMenu),
                                         c_int(i),
                                         itemName,
                                         c_int(len(itemName)),
                                         MF_BYPOSITION)
            hMenuState = _user32.GetMenuState(c_int(hMenu),
                                                   c_int(i),
                                                   MF_BYPOSITION)
            id = _user32.GetMenuItemID(c_int(hMenu), c_int(i))
    #        if hMenuState & (MF_GRAYED|MF_DISABLED|MF_SEPARATOR):
            if hMenuState & (MF_GRAYED|MF_DISABLED):
                continue
            item = itemName.value.replace("&","").split("\t")[0]
            if item == "" and id == 0:
                continue
            checked = bool(hMenuState & MF_CHECKED)
            itemList.append((item, i, checked, id))
        PostMessage(hWnd, WM_CLOSE, 0, 0)
        return itemList[1:] #ignore "Pin"


    def onUp(self, event):
        eg.SendKeys(self.asCat, "{Up}", False)


    def onDown(self, event):
        eg.SendKeys(self.asCat, "{Down}", False)


    def onLeft(self, event):
        eg.SendKeys(self.asCat, "{Left}", False)


    def onRight(self, event):
        eg.SendKeys(self.asCat, "{Right}", False)
        

    def onEnter(self, event):
        eg.SendKeys(self.asCat, "{Enter}", False)
        

    def onEscape(self, event):
        eg.SendKeys(self.asCat, "{Escape}", False)
 

    def bindCatEvents(self):
        for evt in self.evtList[0]:
            eg.Bind(evt, self.onUp)
        for evt in self.evtList[1]:
            eg.Bind(evt, self.onDown)
        for evt in self.evtList[2]:
            eg.Bind(evt, self.onLeft)
        for evt in self.evtList[3]:
            eg.Bind(evt, self.onRight)
        for evt in self.evtList[4]:
            eg.Bind(evt, self.onEnter)
        for evt in self.evtList[5]:
            eg.Bind(evt, self.onEscape)


    def unBindCatEvents(self):
        for evt in self.evtList[0]:
            eg.Unbind(evt, self.onUp)
        for evt in self.evtList[1]:
            eg.Unbind(evt, self.onDown)
        for evt in self.evtList[2]:
            eg.Unbind(evt, self.onLeft)
        for evt in self.evtList[3]:
            eg.Unbind(evt, self.onRight)
        for evt in self.evtList[4]:
            eg.Unbind(evt, self.onEnter)
        for evt in self.evtList[5]:
            eg.Unbind(evt, self.onEscape)       
      

    def catIsOpened(self):
        self.ASsched=eg.scheduler.AddTask(1, self.catIsOpened) # must run continuously !
        asCat = self.GetAScatalog()
        if not asCat:
            if self.asCat:
                    self.asCat = None
                    self.unBindCatEvents()
                    eg.TriggerEvent(
                        "Catalog.%s" % self.text.closed,
                        prefix = "Artsage"
                    )                
        elif not self.asCat:
            self.asCat = asCat[0]
            self.bindCatEvents()
            eg.TriggerEvent(
                "Catalog.%s" % self.text.opened,
                prefix = "Artsage"
            )                


    def __init__(self):
        self.AddActionsFromList(ACTIONS)
        self.ASsched = None

        
    def __start__(self, ArtsagePath = None, evtList = [[],[],[],[],[],[]]):
        self.ArtsagePath = ArtsagePath
        self.evtList = evtList
        self.asCat = None
        self.ASsched=eg.scheduler.AddTask(1, self.catIsOpened)


    def Configure(self, ArtsagePath = None, evtList = [[],[],[],[],[],[]]):
        panel = eg.ConfigPanel(self)
        panel.evtList = cpy(evtList)
        labelText = wx.StaticText(panel, -1, self.text.label1)
        filepathCtrl = MyDirBrowseButton(
            panel, 
            size=(410, -1),
            toolTip = self.text.toolTipFolder,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse
        )
        filepathCtrl.GetTextCtrl().SetEditable(False)
        if ArtsagePath is None:
            ArtsagePath = eg.folderPath.ProgramFiles+'\\Artsage'
            filepathCtrl.SetValue("")
        else:
            filepathCtrl.SetValue(split(ArtsagePath)[0])
        dialogButton = wx.Button(panel,-1,self.text.dialog)
        dialogButton.SetToolTipString(self.text.btnToolTip)

        filepathCtrl.startDirectory = ArtsagePath
        sizerAdd = panel.sizer.Add
        sizerAdd(labelText, 0, wx.TOP,15)
        sizerAdd(filepathCtrl,0,wx.TOP,3)
        sizerAdd(dialogButton,0,wx.TOP,15)


        def OnDialogBtn(evt):
            dlg = CatalogEventsDialog(
                parent = panel,
                plugin = self,
            )
            dlg.Centre()
            wx.CallAfter(
                dlg.ShowCatalogEventsDialog,
                self.text.evtAssignTitle,
                self.text.events
            )
            evt.Skip()
        dialogButton.Bind(wx.EVT_BUTTON, OnDialogBtn)


        def OnPathChange(event = None):
            fPath = filepathCtrl.GetValue()
            flag = exists(fPath + "\\Artsage32.exe")
            if not flag:
                flag = exists(fPath + "\\Artsage64.exe")
            panel.dialog.buttonRow.okButton.Enable(flag)
            panel.isDirty = True
            panel.dialog.buttonRow.applyButton.Enable(flag)
            if event and not flag:
                MessageBox(
                    panel.GetHandle(),
                    self.text.boxMessage1 % (fPath,'Artsage'),
                    self.text.boxTitle,
                        0
                    )
            if fPath != "":
                filepathCtrl.startDirectory = fPath
        filepathCtrl.Bind(wx.EVT_TEXT,OnPathChange)
        OnPathChange()


        while panel.Affirmed():
            pth=filepathCtrl.GetValue()
            if exists(pth + "\\Artsage32.exe"):
                pth+="\\Artsage32.exe"
            else:
                pth+="\\Artsage64.exe"
            panel.SetResult(pth, panel.evtList)
    
    def __stop__(self):
        if self.ASsched:
            try:
                eg.scheduler.CancelTask(self.ASsched)
            except:
                pass
        self.ASsched = None
        self.asCat = None
#===============================================================================

class SendHotkey(eg.ActionBase):

    class text:
        label = "Select menu item (level %s):"

    def __call__(self, ix_0 = -1,  ix_1 = -1,  ix_2 = -1):
        hwnd = self.plugin.GetArtsage()
        if hwnd:
            if ix_0 > -1:
                x = HOTKEYS[ix_0][1]
                if ix_1 > -1:
                    x = x[ix_1][1]
                    if ix_2 > -1:
                        x = x[ix_2][1]
                eg.SendKeys(hwnd[0], x, False)
        else:
            self.PrintError(self.plugin.text.text1)


    def GetLabel(self, ix_0,  ix_1,  ix_2):
        res = self.name
        if ix_0 > -1:
            x = HOTKEYS[ix_0]
            res+= ": %s" % x[0]
            if ix_1 > -1:
                x = x[1][ix_1]
                res+= " - %s" % x[0]
                if ix_2 > -1:
                    x = x[1][ix_2]
                    res+= " - %s" % x[0]
        return res


    def Configure(self, ix_0 = -1,  ix_1 = -1,  ix_2 = -1):
        panel = eg.ConfigPanel(self)
        label0 = wx.StaticText(panel, -1, self.text.label % "1")
        label1 = wx.StaticText(panel, -1, self.text.label % "2")
        label2 = wx.StaticText(panel, -1, self.text.label % "3")
        choices = [item[0] for item in HOTKEYS]
        menu0 = wx.Choice(panel, -1, choices = choices) 
        menu1 = wx.Choice(panel, -1)
        menu2 = wx.Choice(panel, -1)  
        mainSizer = wx.FlexGridSizer(3, 2, 15, 10)
        mainSizer.AddGrowableCol(1)
        mainSizer.Add(label0,0)
        mainSizer.Add(menu0,0, wx.EXPAND)
        mainSizer.Add(label1,1)
        mainSizer.Add(menu1,0, wx.EXPAND)
        mainSizer.Add(label2,2)
        mainSizer.Add(menu2,0, wx.EXPAND)
        panel.sizer.Add(mainSizer,0, wx.ALL|wx.EXPAND,8)

        def onMenu0(evt=None):
            menu1.Clear()
            menu1.SetSelection(-1)
            label2.Enable(False)
            menu2.Enable(False)
            x = HOTKEYS[menu0.GetSelection() if evt else ix_0][1]
            enable=isinstance(x,tuple)
            if enable:
                menu1.SetItems([item[0] for item in x])
            label1.Enable(enable)
            menu1.Enable(enable)
            if evt:
                evt.Skip()
            else:
                menu0.SetSelection(ix_0)

        def onMenu1(evt=None):
            menu2.Clear()
            menu2.SetSelection(-1)
            x = HOTKEYS[menu0.GetSelection()][1]
            enable = False
            ix = menu1.GetSelection() if evt else ix_1
            if ix > -1:
                x = x[ix][1]
                enable=isinstance(x, tuple)
                if enable:
                    menu2.SetItems([item[0] for item in x])
            label2.Enable(enable)
            menu2.Enable(enable)
            if evt:
                evt.Skip()
            else:
                menu1.SetSelection(ix_1)                
        menu0.Bind(wx.EVT_CHOICE, onMenu0)
        menu1.Bind(wx.EVT_CHOICE, onMenu1)
        onMenu0()
        onMenu1()
        menu2.SetSelection(ix_2)

        while panel.Affirmed():
            panel.SetResult(
                menu0.GetSelection(),
                menu1.GetSelection(),
                menu2.GetSelection(),
            )
#===============================================================================

class OpenPicture(eg.ActionBase):

    class text:
        toolTipFile = 'Type filename or click browse to choose file'
        browseFile = 'Choose a file'


    def __call__(self, filepath = ""):
        if filepath:
            filepath = eg.ParseString(filepath)
            ap = self.plugin.ArtsagePath
            ap = ap.encode(FSE) if isinstance(ap, unicode) else ap
            if isfile(ap) and  isfile(filepath):
                args = [ap]
                args.append(filepath)
                Popen(args)


    def Configure(self, filepath = ""):
        panel = eg.ConfigPanel()    
        folder = split(filepath)[0] if filepath else eg.folderPath.Pictures
        filepathLabel = wx.StaticText(panel, -1, "%s:" % self.text.browseFile)
        filepathCtrl = eg.FileBrowseButton(
            panel,
            -1,
            toolTip = self.text.toolTipFile,
            dialogTitle = self.text.browseFile,
            buttonText = eg.text.General.browse,
            startDirectory = folder,
            initialValue = filepath
        )
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(filepathLabel,0,wx.TOP,3)
        sizer.Add(filepathCtrl,1,wx.LEFT|wx.EXPAND,5)
        panel.sizer.Add(sizer,0,wx.ALL|wx.EXPAND,20)
        while panel.Affirmed():
            panel.SetResult(
                filepathCtrl.GetValue(),
            )
#===============================================================================

class OpenFolder(eg.ActionBase):

    class text:
        toolTipFile = 'Type filename or click browse to choose folder'
        browseFile = 'Choose a folder'


    def __call__(self, filepath = ""):
        if filepath:
            filepath = eg.ParseString(filepath)
            ap = self.plugin.ArtsagePath
            ap = ap.encode(FSE) if isinstance(ap, unicode) else ap
            if isfile(ap) and isdir(filepath):
                args = [ap]
                args.append(filepath)
                Popen(args)


    def Configure(self, filepath = ""):
        panel = eg.ConfigPanel()    
        folder = filepath if filepath else eg.folderPath.Pictures
        filepathLabel = wx.StaticText(panel, -1, "%s:" % self.text.browseFile)
        filepathCtrl = eg.DirBrowseButton(
            panel,
            -1,
            toolTip = self.text.toolTipFile,
            dialogTitle = self.text.browseFile,
            buttonText = eg.text.General.browse,
            startDirectory = folder,
        )
        filepathCtrl.SetValue(folder)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(filepathLabel,0,wx.TOP,3)
        sizer.Add(filepathCtrl,1,wx.LEFT|wx.EXPAND,5)
        panel.sizer.Add(sizer,0,wx.ALL|wx.EXPAND,20)
        while panel.Affirmed():
            panel.SetResult(
                filepathCtrl.GetValue(),
            )
#===============================================================================

class ShowMenu(eg.ActionClass):

    name = "Show Artsage menu"
    description = "Shows Artsage menu."
    panel = None

    class text:
        OSELabel = 'Menu show on:'
        menuPreview = 'On Screen Menu preview:'
        menuFont = 'Font:'
        txtColour = 'Text colour'
        background = 'Background colour'
        txtColourSel = 'Selected text colour'
        backgroundSel = 'Selected background colour'
        dialog = "Events ..."
        btnToolTip = """Press this button to assign events to control the menu !!!"""
        evtAssignTitle = "Menu control - events assignement"
        events = (
            "Cursor up:",
            "Cursor down:",
            "Back from the (sub)menu:",
            "Submenu, or select an item:",
            "Cancel (Escape):",
        )
        inverted = "Use inverted colours"
        submenuLbl = "Show main menu or submenu:"
        submenus = (
            "Main (root) menu",   
            "Slideshow",
            "Sort",
            "Navigate",
            "View",
            "Exhibit",   
            "Find",
            "Favorites",
            "Catalog",
            "Zoom",
            "Rotate",   
            "Collage",
            "Transitions",
            "Window",
            "Screen",
            "Shell",   
            "Settings",
            "Info",
        )

    def __call__(
        self,
        fore,
        back,
        fontInfo = TAHOMA_INFO,
        monitor = 0,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75),
        evtList = [],
        inverted = True,
        submenu = 0
    ):
        hwnd = self.plugin.GetArtsage2()
        if hwnd:
            if not self.plugin.menuDlg:
                wx.CallAfter(
                    Menu,
                    fore,
                    back,
                    foreSel,
                    backSel,
                    fontInfo,
                    False,
                    self.plugin,
                    monitor,
                    hwnd[0],
                    evtList,
                    ROOT[submenu],
                )


    def GetLabel(
        self,
        fore,
        back,
        fontInfo,
        monitor,
        foreSel,
        backSel,
        evtList,
        inverted,
        submenu = 0
    ):
        return "%s: %s" % (self.name, self.text.submenus[submenu])


    def Configure(
        self,
        fore = (75, 75, 75),
        back = (180, 180, 180),
        fontInfo = TAHOMA_INFO,
        monitor = 0,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75),
        evtList = [[],[],[],[],[]],
        inverted = True,
        submenu = 0
    ):
        self.fontInfo = fontInfo
        self.fore = fore
        self.back = back
        self.foreSel = foreSel
        self.backSel = backSel
        self.oldSel=0
        self.inverted = inverted
        global panel
        panel = eg.ConfigPanel(self)
        panel.evtList = cpy(evtList)
        previewLbl=wx.StaticText(panel, -1, self.text.menuPreview)
        listBoxCtrl = MenuGrid(panel, 3)
        items = (("Shrink",0,True,804),
                 ("Stretch",1,False,804),
                 (self.text.submenus[9],2,False,-1),)
        listBoxCtrl.Set(items)
        listBoxCtrl.SetBackgroundColour(self.back)
        listBoxCtrl.SetForegroundColour(self.fore)
        listBoxCtrl.SetSelectionBackground(self.backSel)
        listBoxCtrl.SetSelectionForeground(self.foreSel)
        #Font button
        fontLbl=wx.StaticText(panel, -1, self.text.menuFont)
        fontButton = eg.FontSelectButton(panel, value = fontInfo)
        font = wx.FontFromNativeInfoString(fontInfo)
        for n in range(10,20):
            font.SetPointSize(n)
            fontButton.SetFont(font)
            hght = fontButton.GetTextExtent('X')[1]
            if hght > 20:
                break
        listBoxCtrl.SetDefaultCellFont(font)
        arial = wx.FontFromNativeInfoString(ARIAL_INFO)
        fontButton.SetFont(font)            
        for n in range(1,1000):
            arial.SetPointSize(n)
            fontButton.SetFont(arial)
            h = fontButton.GetTextExtent(u"\u25a0")[1]
            if h > hght:
                break
        arial.SetPointSize(2*n/3)
        fontButton.SetFont(arial)            
        w0 = 2 * fontButton.GetTextExtent(u"\u25a0")[0]
        attr = gridlib.GridCellAttr()
        attr.SetFont(arial)
        attr.SetAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        listBoxCtrl.SetColAttr(0,attr)
        for n in range(1,1000):
            arial.SetPointSize(n)
            fontButton.SetFont(arial)
            h = fontButton.GetTextExtent(u"\u25ba")[1]
            if h > hght:
                break
        arial.SetPointSize(n/2)
        fontButton.SetFont(arial)            
        w2 = 2 * fontButton.GetTextExtent(u"\u25ba")[0]
        attr = gridlib.GridCellAttr()
        attr.SetFont(arial)
        attr.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
        listBoxCtrl.SetColAttr(2,attr)
        listBoxCtrl.SetDefaultRowSize(hght+4, True)
        displayChoice = eg.DisplayChoice(panel, monitor)
        w = displayChoice.GetSize()[0]
        OSElbl = wx.StaticText(panel, -1, self.text.OSELabel)
        useInvertedCtrl = wx.CheckBox(panel, -1, self.text.inverted)
        useInvertedCtrl.SetValue(inverted)
        subMenuLbl = wx.StaticText(panel, -1, self.text.submenuLbl)
        if self.plugin.submenus:
            choices = self.plugin.submenus
        else:
            choices = self.text.submenus
        subMenuCtrl = wx.Choice(panel, -1, choices = choices)
        subMenuCtrl.SetSelection(submenu)
        #Button Text Colour
        foreLbl=wx.StaticText(panel, -1, self.text.txtColour+':')
        foreColourButton = eg.ColourSelectButton(
            panel,
            fore,
            title = self.text.txtColour
        )
        #Button Background Colour
        backLbl=wx.StaticText(panel, -1, self.text.background+':')
        backColourButton = eg.ColourSelectButton(
            panel,
            back,
            title = self.text.background
        )
        #Button Selected Text Colour
        foreSelLbl=wx.StaticText(panel, -1, self.text.txtColourSel+':')
        foreSelColourButton = eg.ColourSelectButton(
            panel,
            foreSel,
            title = self.text.txtColourSel
        )
        #Button Selected Background Colour
        backSelLbl=wx.StaticText(panel, -1, self.text.backgroundSel+':')
        backSelColourButton = eg.ColourSelectButton(
            panel,
            backSel,
            title = self.text.backgroundSel
        )
        #Button Dialog "Menu control - assignement of events"
        dialogButton = wx.Button(panel,-1,self.text.dialog)
        dialogButton.SetToolTipString(self.text.btnToolTip)
        foreSelLbl.Enable(not inverted)
        foreSelColourButton.Enable(not inverted)
        backSelLbl.Enable(not inverted)
        backSelColourButton.Enable(not inverted)
        #Sizers
        mainSizer = panel.sizer
        topSizer=wx.GridBagSizer(2, 30)
        mainSizer.Add(topSizer)
        topSizer.Add(previewLbl,(0, 0),flag = wx.TOP,border = 0)
        topSizer.Add(listBoxCtrl,(1, 0),(4, 1))        
        topSizer.Add(useInvertedCtrl,(6, 0),flag = wx.TOP, border = 8)        
        topSizer.Add(subMenuLbl,(8, 0), flag = wx.TOP,border = 8)        
        topSizer.Add(subMenuCtrl,(9, 0), flag = wx.TOP)        
        topSizer.Add(fontLbl,(0, 1),flag = wx.TOP)
        topSizer.Add(fontButton,(1, 1),flag = wx.TOP)        
        topSizer.Add(foreLbl,(2, 1),flag = wx.TOP,border = 8)
        topSizer.Add(foreColourButton,(3, 1),flag = wx.TOP)
        topSizer.Add(backLbl,(4, 1),flag = wx.TOP,border = 8)
        topSizer.Add(backColourButton,(5, 1),flag = wx.TOP)        
        topSizer.Add(OSElbl,(0, 2), flag = wx.TOP)
        topSizer.Add(displayChoice,(1, 2),flag = wx.TOP)        
        topSizer.Add(foreSelLbl,(6, 1), (1, 2), flag = wx.TOP,border = 8)
        topSizer.Add(foreSelColourButton, (7, 1), flag = wx.TOP)
        topSizer.Add(backSelLbl,(8, 1), (1, 2), flag = wx.TOP,border = 8)
        topSizer.Add(backSelColourButton, (9, 1), flag = wx.TOP)
        topSizer.Add(dialogButton, (3, 2), flag = wx.TOP|wx.EXPAND)
        panel.sizer.Layout()
        wdth = 160
        if (hght+4)*listBoxCtrl.GetNumberRows() > listBoxCtrl.GetSize()[1]: #after Layout() !!!
            wdth -=  SYS_VSCROLL_X
        listBoxCtrl.SetColSize(0, w0)
        listBoxCtrl.SetColSize(1, wdth - w0 - w2)
        listBoxCtrl.SetColSize(2, w2)
        listBoxCtrl.SetGridCursor(-1, 1)
        listBoxCtrl.SelectRow(0)


        def OnMonitor(evt):
            listBoxCtrl.SetFocus()
            evt.Skip
        displayChoice.Bind(wx.EVT_CHOICE, OnMonitor)


        def OnInverted(evt):
            flag = evt.IsChecked()
            foreSelLbl.Enable(not flag)
            foreSelColourButton.Enable(not flag)
            backSelLbl.Enable(not flag)
            backSelColourButton.Enable(not flag)
            self.inverted = flag
            if flag:
                self.foreSel = self.back
                self.backSel = self.fore
                backSelColourButton.SetValue(self.backSel)
                foreSelColourButton.SetValue(self.foreSel)
                listBoxCtrl.SetSelectionForeground(self.foreSel)
                listBoxCtrl.SetSelectionBackground(self.backSel)
            listBoxCtrl.SetFocus()
            evt.Skip
        useInvertedCtrl.Bind(wx.EVT_CHECKBOX, OnInverted)


        def OnDialogBtn(evt):
            dlg = MenuEventsDialog(
                parent = panel,
                plugin = self.plugin,
            )
            dlg.Centre()
            wx.CallAfter(
                dlg.ShowMenuEventsDialog,
                self.text.evtAssignTitle,
                self.text.events
            )
            evt.Skip()
        dialogButton.Bind(wx.EVT_BUTTON, OnDialogBtn)


        def OnFontBtn(evt):
            value = evt.GetValue()
            self.fontInfo = value
            font = wx.FontFromNativeInfoString(value)
            for n in range(10,20):
                font.SetPointSize(n)
                fontButton.SetFont(font)
                hght = fontButton.GetTextExtent('X')[1]
                if hght > 20:
                    break
            listBoxCtrl.SetDefaultCellFont(font)
            listBoxCtrl.SetDefaultRowSize(hght+4, True)
            for i in range(listBoxCtrl.GetNumberRows()):
                listBoxCtrl.SetCellFont(i,1,font)
            listBoxCtrl.SetFocus()
            if evt:
                evt.Skip()
        fontButton.Bind(eg.EVT_VALUE_CHANGED, OnFontBtn)

        def OnColourBtn(evt):
            id = evt.GetId()
            value = evt.GetValue()
            if id == foreColourButton.GetId():
                listBoxCtrl.SetForegroundColour(value)
                if self.inverted:
                    self.backSel = self.fore
                    listBoxCtrl.SetSelectionBackground(value)
                    backSelColourButton.SetValue(value)
            elif id == backColourButton.GetId():
                listBoxCtrl.SetBackgroundColour(value)
                if self.inverted:
                    self.foreSel = self.back
                    listBoxCtrl.SetSelectionForeground(value)
                    foreSelColourButton.SetValue(value)
            elif id == foreSelColourButton.GetId():
                listBoxCtrl.SetSelectionForeground(value)
            elif id == backSelColourButton.GetId():
                listBoxCtrl.SetSelectionBackground(value)
            listBoxCtrl.Refresh()
            listBoxCtrl.SetFocus()
            evt.Skip()
        foreColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)
        backColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)
        foreSelColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)
        backSelColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)


        def setFocus():
            listBoxCtrl.SetFocus()
        panel.setFocus = setFocus

        # re-assign the test button
        def OnButton(event):
            hwnds = self.plugin.GetArtsage()
            if hwnds:
                if not self.plugin.menuDlg:
                    wx.CallAfter(
                        Menu,
                        foreColourButton.GetValue(),
                        backColourButton.GetValue(),
                        foreSelColourButton.GetValue(),
                        backSelColourButton.GetValue(),
                        self.fontInfo, 
                        True,
                        self.plugin,
                        displayChoice.GetSelection(),
                        hwnds[0],
                        panel.evtList,
                        ROOT[subMenuCtrl.GetSelection()]
                    )

        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnButton)

        while panel.Affirmed():
            fontInfo = fontButton.GetValue()
            if not fontInfo:
                font = listBoxCtrl.GetFont()
                font.SetPointSize(36)
                fontInfo = font.GetNativeFontInfoDesc()
            panel.SetResult(
            foreColourButton.GetValue(),
            backColourButton.GetValue(),
            fontInfo,
            displayChoice.GetSelection(),
            foreSelColourButton.GetValue(),
            backSelColourButton.GetValue(),
            panel.evtList,
            useInvertedCtrl.GetValue(),
            subMenuCtrl.GetSelection()
        )
#===============================================================================

ACTIONS = (
    (ShowMenu,"ShowMenu","Show ArtSage menu","Shows ArtSage menu.", None),
    (SendHotkey, "SendHotkey", "Send Hotkey", "Sends hotkey.", None),
    (OpenPicture, "OpenPicture", "Open picture", "Opens a picture.", None),
    (OpenFolder, "OpenFolder", "Open folder", "Opens a folder.", None),
)         

HOTKEYS = (
    ("Slideshow",(
        ("Slideshow","{Pause}"),
        ("Timer...","{Ctrl+T}"),
        ("Windowed","{Alt+N}"),
        ("FullScreen","{F11}"),
        ("Wallpaper","{Alt+W}"),
        ("Stay On Top","{Alt+T}"),
        ("Transparency - Blend","{B}"),
    )),
    ("Sort",(
        ("Forward","{Alt+F}"),
        ("Reverse","{Alt+V}"),
        ("Random (Shuffle)","{Alt+R}"),
        ("Tree","{Ctrl+K}"),
        ("Tree (Strict)","{Alt+K}"),
    )),
    ("Navigate",(
        ("Next","{PageDown}"),
        ("Previous","{PageUp}"),
        ("Next x5","{Shift+PageDown}"),
        ("Previous x5","{Shift+PageUp}"),
        ("Next x10","{Ctrl+PageDown}"),
        ("Previous x10","{Ctrl+PageUp}"),
        ("First","{Home}"),
        ("Last","{End}"),
        ("Current","{F5}"),
        ("Next Folder","{Tab}"),
        ("Prev Folder","{Shift+Tab}"),
        ("Scroll",(
            ("Left","{Left}"),
            ("Right","{Right}"),
            ("Up","{Up}"),
            ("Down","{Down}"),
            ("Left x2","{Shift+Left}"),
            ("Right x2","{Shift+Right}"),
            ("Up x2","{Shift+Up}"),
            ("Down x2","{Shift+Down}"),
            ("Left x5","{Ctrl+Left}"),
            ("Right x5","{Ctrl+Right}"),
            ("Up x5","{Ctrl+Up}"),
            ("Down x5","{Ctrl+Down}"),
            ("Left Pixel","{Alt+Left}"),
            ("Right Pixel","{Alt+Right}"),
            ("Up Pixel","{Alt+Up}"),
            ("Down Pixel","{Alt+Down}"),
        )),
    )),
    ("View",(
        ("Exhibit","{Shift+A}"),
        ("Desktop","{Shift+D}"),
        ("Favorites","{Shift+F}"),
        ("Archive","{Shift+G}"),
        ("Image Folder","{Shift+F5}"),
        ("Link Target","{Shift+L}"),
    )),
    ("Exhibit",(
        ("Folder...","{Ins}"),
        ("Refresh","{Ctrl+R}"),
        ("Subfolders","{Shift+B}"),
        ("Auto Refresh","{Ctrl+A}"),
    )),
    ("Find",(
        ("Find/Filter...","{Ctrl+F}"),
        ("Find Next","{F3}"),
        ("Landscape","{Alt+L}"),
        ("Portrait","{Alt+P}"),
        ("Bookmark","{Ctrl+M}"),
        ("Go To Mark","{M}"),
        ("Go To...","{Ctrl+G}"),
    )),
    ("Favorites",(
        ("Send Shortcut","{F8}"),
        ("Send Copy","{Alt+F8}"),
        ("Favorites Folder...","{Ctrl+F8}"),
        ("Shortcut To Desktop","{D}"),
        ("Copy To Desktop","{Alt+D}"),
        ("Archive",(
            ("Move To Archive","{F9}"),
            ("Archive Folder...","{Ctrl+F9}"),
        )),
    )),
    ("Catalog","{C}"),
    ("Wrap","{W}"),
    ("Crop","{P}"),
    ("Squeeze","{S}"),
    ("Shrink","{Alt+S}"),
    ("Stretch","{Shift+S}"),
    ("Zoom",(
        ("Zoom In","{Add}"),
        ("Zoom Out","{Subtract}"),
        ("100%","="),
        ("Zoom +1%","{Alt+Add}"),
        ("Zoom -1%","{Alt+Subtract}"),
        ("Zoom Lock","{Shift+Z}"),
    )),
    ("Rotate",(
        ("Right","{R}"),
        ("Left","{L}"),
        ("Lock","{Shift+R}"),
        ("Aspect Filter","{Ctrl+Shift+R}"),
        ("Flip Horizontal","{H}"),
        ("Exif Orientation","{Ctrl+O}"),
    )),
    ("Collage","{G}"),
    ("Transitions","{T}"),
    ("Window",(
        ("Name In Caption","{N}"),
        ("Full Pathname","{Shift+N}"),
        ("Status Bar","{I}"),
        ("Tray Icon","{Alt+I}"),
        ("Background Colour Icon","{Alt+B}"),
        ("Center","{0}"),
        ("Presets",(
            ("Save1","{Alt+1}"),
            ("Save2","{Alt+2}"),
            ("Save3","{Alt+3}"),
            ("Save4","{Alt+4}"),
            ("Save5","{Alt+5}"),
            ("Restore1","{1}"),
            ("Restore2","{2}"),
            ("Restore3","{3}"),
            ("Restore4","{4}"),
            ("Restore5","{5}"),
        )),
        ("Layout",(
            ("Centered","{Ctrl+0}"),
            ("Top Left","{Ctrl+1}"),
            ("Top Right","{Ctrl+2}"),
            ("Bottom Left","{Ctrl+3}"),
            ("Bottom Right","{Ctrl+4}"),
            ("Roaming","{Ctrl+5}"),
        )),
    )),
    ("Screen",(
        ("Fullscreen","{F11}"),
        ("Caption","{Shift+F11}"),
        ("Cursor","{Shift+U}"),
        ("Centered Image","{Shift+0}"),
        ("Roaming Image","{Shift+5}"),
        ("Walpaper","{Alt+W}"),
        ("Center","{Ctrl+W}"),
        ("Tile","{Shift+W}"),
        ("Stretch","{Ctrl+Shift+W}"),
    )),
    ("Shell",(
        ("View","{Shift+V}"),
        ("Explore","{Shift+E}"),
        ("Open With...","{Shift+H}"),
        ("Copy File...","{Shift+C}"),
        ("Move/Rename...","{F2}"),
        ("Save As...","{Ctrl+S}"),
        ("Copy Image","{Shift+Ctrl+C}"),
        ("Copy View","{Ctrl+C}"),
        ("Paste","{Ctrl+V}"),
        ("Recycle","{Del}"),
    )),
    ("Exit","{Esc}"),
)