version="0.2"
# plugins/Impress/__init__.py
#
# Copyright (C)  2008-2013 Pako  (lubos.ruckl@quick.cz)
#
# This file is a plugin for EventGhost.
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

# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.2 by Pako 2013-12-15 11:30 UTC+1
#     - many changes and improvements
# 0.1 by Pako 2009-01-01 17:00
#===============================================================================

eg.RegisterPlugin(
    name = "Impress",
    author = "Pako",
    guid = "{D8767FB1-CCC0-402D-AF65-D961D2D7C20F}",
    version = version,
    kind = "program",
    description = ur'''<rst>
Adds actions to control ...

| `Appache OpenOffice Impress`__
| or
| `LibreOffice Impress`__.

__ http://www.openoffice.org/product/impress.html
__ https://www.libreoffice.org/features/impress/
''',
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=1052",
    icon = (
        "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"
        "TkSuQmCC"
    )
)
#===============================================================================

import os
import wx.grid as gridlib
from os.path import join, exists
from copy import deepcopy as cpy
from time import sleep
from threading import Thread, Event, Timer
from win32com.client.dynamic import Dispatch
from win32api import GetSystemMetrics
from win32gui import SetFocus, SetForegroundWindow, SetActiveWindow, IsWindow
from eg.WinApi import SendMessageTimeout
from eg.WinApi.Dynamic import PostMessage, CreateEvent, SetEvent
from eg.WinApi.Utils import GetMonitorDimensions
from eg.Classes.MainFrame.TreeCtrl import DropTarget as EventDropTarget

SYS_VSCROLL_X    = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
WM_CLOSE      = 16
WM_SYSCOMMAND = 274
SC_MINIMIZE   = 61472

findPresentation = eg.WindowMatcher(
    None,
    None,
    u'SALTMPSUBFRAME',
    None,
    None,
    None,
    False,
    0.0,
    0
)
#===============================================================================
class Text:
    err1 ='''Couldn't open file "%s" !'''
    err2 =  "Couldn't find window with presentation!"
    err3 = '''Couldn't find file "%s" !'''
    opened = "Opened"
    closed = "Closed"
    endless = "Endlessly:"
    endlessToolTip = "If True, the presentation repeats endlessly"
    pause = "Pause:"
    pauseToolTip = "Duration of black screen [seconds] after last slide"
    startLbl = 'Start slide number:'



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

class NumDialog(wx.Frame):

    def __init__(self, plugin):
        self.plugin = plugin
        wx.Frame.__init__(
            self,
            None,
            -1,
            'SlideNumber',
            style=wx.STAY_ON_TOP | wx.SIMPLE_BORDER
        )
        plugin.numDialog = self


    def CloseDialog(self):
        self.plugin.TriggerEvent("GoToFrame.%s" % self.plugin.text.closed)
        self.plugin.numDialog = None
        wx.CallAfter(self.Close, True)
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
        event,
        monitor,
        data,
        evtList,
        ):
        wx.Frame.__init__(
            self,
            None,
            -1,
            'Impress_menu',
            style = wx.STAY_ON_TOP|wx.SIMPLE_BORDER
        )
        self.data = data
        self.data.sort()
        tmpLst = [i[0] for i in self.data]
        self.actFileIx = 0
        if ">>ActiveFile<<" in tmpLst:
            ix = tmpLst.index(">>ActiveFile<<")
            actFile = self.data[ix][1]
            self.data.pop(ix)
            tmpLst = [i[1] for i in self.data]
            if actFile in tmpLst:
                self.actFileIx = tmpLst.index(actFile)
        self.fore     = fore
        self.back     = back
        self.foreSel  = foreSel
        self.backSel  = backSel
        self.fontInfo = fontInfo
        self.flag     = flag
        self.plugin   = plugin
        self.monitor  = monitor
        self.evtList  = evtList
        self.plugin.TriggerEvent("OnScreenMenu.%s" % self.plugin.text.opened)
        for evt in self.evtList[0]:
            eg.Bind(evt, self.onUp)
        for evt in self.evtList[1]:
            eg.Bind(evt, self.onDown)
        for evt in self.evtList[2]:
            eg.Bind(evt, self.onRight)
        for evt in self.evtList[3]:
            eg.Bind(evt, self.onEscape)
        self.menuGridCtrl = MenuGrid(self, len(self.data), wx.DefaultSize)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        mainSizer.Add(self.menuGridCtrl, 0, wx.EXPAND)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(gridlib.EVT_GRID_CMD_CELL_LEFT_DCLICK, self.onDoubleClick, self.menuGridCtrl)
        self.Bind(wx.EVT_CHAR_HOOK, self.onFrameCharHook)
        font = wx.FontFromNativeInfoString(fontInfo)
        self.menuGridCtrl.SetFont(font)
        self.SetFont(font)
        self.SetBackgroundColour((0, 0, 0))
        self.menuGridCtrl.SetBackgroundColour(self.back)
        self.menuGridCtrl.SetForegroundColour(self.fore)
        self.menuGridCtrl.SetSelectionBackground(self.backSel)
        self.menuGridCtrl.SetSelectionForeground(self.foreSel)
        if self.flag:
            self.timer = MyTimer(t = 5.0, plugin = self.plugin)
        self.menuGridCtrl.Set(self.data)
        self.DrawMenu()
        self.plugin.menuDlg = self
        wx.Yield()
        SetEvent(event)


    def DrawMenu(self):
        self.Show(False)
        self.menuGridCtrl.SetGridCursor(-1, 0)
        monDim = GetMonitorDimensions()
        try:
            x,y,ws,hs = monDim[self.monitor]
        except IndexError:
            x,y,ws,hs = monDim[0]
        # menu height calculation:
        h=self.GetCharHeight()+4
        for i in range(len(self.data)):
            self.menuGridCtrl.SetRowSize(i,h)
            self.menuGridCtrl.SetCellValue(i,0," "+self.data[i][0])
        height0 = len(self.data)*h
        height1 = h*((hs-20)/h)
        height = min(height0, height1)+6
        # menu width calculation:
        width_lst=[]
        for item in self.data:
            width_lst.append(self.GetTextExtent(item[0]+' ')[0])
        width = max(width_lst)+8
        self.menuGridCtrl.SetColSize(0,width)
        self.menuGridCtrl.ForceRefresh()
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
        self.menuGridCtrl.SelectRow(self.actFileIx)
        self.menuGridCtrl.MakeCellVisible(self.actFileIx, 0)
        self.Show(True)
        self.Raise()


    def MoveCursor(self, step):
        max=len(self.data)
        if max > 0:
            self.menuGridCtrl.MoveCursor(step)


    def onUp(self, event):
        wx.CallAfter(self.menuGridCtrl.MoveCursor, -1)
        return True #stop processing this event !!!


    def onDown(self, event):
        wx.CallAfter(self.menuGridCtrl.MoveCursor, 1)
        return True #stop processing this event !!!


    def onRight(self, event):
        wx.CallAfter(self.DefaultAction)
        return True #stop processing this event !!!


    def onEscape(self, event):
        wx.CallAfter(self.destroyMenu)
        return True #stop processing this event !!!


    def DefaultAction(self):
        item = self.data[self.menuGridCtrl.GetSelection()]
        self.destroyMenu()
        self.plugin.TriggerEvent(
            "Menu.DefaultAction",
            payload = item[1:]
        )


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
            self.destroyMenu()
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
            eg.Unbind(evt, self.onRight)
        for evt in self.evtList[3]:
            eg.Unbind(evt, self.onEscape)
        if self.flag:
            self.timer.Cancel()
        self.plugin.TriggerEvent("OnScreenMenu.%s" % self.plugin.text.closed)
        self.Close()
#===============================================================================

class MyFileBrowseButton(eg.FileBrowseButton):
    def GetTextCtrl(self):          #  now I can make build-in textCtrl non-editable !!!
        return self.textControl     #
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

    def __init__(self, parent, id, evtList, ix, action):
        width = 205
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT |
            wx.LC_NO_HEADER | wx.LC_SINGLE_SEL, size = (width, -1))
        self.parent = parent
        self.id = id
        self.evtList = evtList
        self.ix = ix
        self.action = action
        self.sel = -1
        self.il = wx.ImageList(16, 16)
        self.il.Add(wx.BitmapFromImage(wx.Image(join(eg.imagesDir, "event.png"), wx.BITMAP_TYPE_PNG)))
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.InsertColumn(0, '')
        self.SetColumnWidth(0, width - 5 - SYS_VSCROLL_X)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        self.Bind(wx.EVT_SET_FOCUS, self.OnChange)
        self.Bind(wx.EVT_LIST_INSERT_ITEM, self.OnChange)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnChange)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClick)
        self.SetToolTipString(self.action.text.toolTip)


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
        menu.Append(self.popupID1, self.action.text.popup[0])
        menu.Append(self.popupID2, self.action.text.popup[1])
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

    def __init__(self, parent, action):
        wx.MiniFrame.__init__(
            self,
            parent,
            -1,
            style=wx.CAPTION,
            name="Menu events dialog"
        )
        self.panel = parent
        self.action = action
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
        eventsCtrl_0 = EventListCtrl(self, id, self.evtList, 0, self.action)
        eventsCtrl_0.SetItems(self.evtList[0])
        dt0 = MyTextDropTarget(eventsCtrl_0)
        eventsCtrl_0.SetDropTarget(dt0)
        textLbl_1=wx.StaticText(self, -1, labels[1])
        id = wx.NewId()
        eventsCtrl_1 = EventListCtrl(self, id, self.evtList, 1, self.action)
        eventsCtrl_1.SetItems(self.evtList[1])
        dt1 = MyTextDropTarget(eventsCtrl_1)
        eventsCtrl_1.SetDropTarget(dt1)
        textLbl_2=wx.StaticText(self, -1, labels[2])
        id = wx.NewId()
        eventsCtrl_2 = EventListCtrl(self, id, self.evtList, 2, self.action)
        eventsCtrl_2.SetItems(self.evtList[2])
        dt2 = MyTextDropTarget(eventsCtrl_2)
        eventsCtrl_2.SetDropTarget(dt2)
        textLbl_3=wx.StaticText(self, -1, labels[3])
        id = wx.NewId()
        eventsCtrl_3 = EventListCtrl(self, id, self.evtList, 3, self.action)
        eventsCtrl_3.SetItems(self.evtList[3])
        dt3 = MyTextDropTarget(eventsCtrl_3)
        eventsCtrl_3.SetDropTarget(dt3)
        deleteSizer = wx.BoxSizer(wx.VERTICAL)
        delOneBtn = wx.Button(self, -1, self.action.text.popup[0])
        delBoxBtn = wx.Button(self, -1, self.action.text.popup[1])
        clearBtn  = wx.Button(self, -1, self.action.text.clear)
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
        topSizer.Add(deleteSizer, (5,1), flag = wx.EXPAND)

        line = wx.StaticLine(self, -1, size=(20,-1),pos = (200,0), style=wx.LI_HORIZONTAL)
        btn1 = wx.Button(self, wx.ID_OK)
        btn1.SetLabel(self.action.text.ok)
        btn1.SetDefault()
        btn2 = wx.Button(self, wx.ID_CANCEL)
        btn2.SetLabel(self.action.text.cancel)
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
                    self.ctrl.SetItemState(-1, wx.LIST_MASK_STATE, wx.LIST_STATE_SELECTED)
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
            delOneBtn.Enable(False)
            delBoxBtn.Enable(False)
            self.evtList = [[], [], [], []]
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
        btn1.Bind(wx.EVT_BUTTON, onOK)

        sizer.Layout()
        self.Raise()
        self.Show()
#===============================================================================

class MenuGrid(gridlib.Grid):

    def __init__(self, parent, lngth, size):
        gridlib.Grid.__init__(self, parent, size = size)
        self.CreateGrid(lngth, 1)
        self.SetRowLabelSize(0)
        self.SetColLabelSize(0)
        self.SetScrollLineX(1)
        self.SetScrollLineY(1)
        self.EnableEditing(False)
        self.EnableDragColSize(False)
        self.EnableDragRowSize(False)
        self.EnableDragGridSize(False)
        self.EnableGridLines(False)
        self.SetColMinimalAcceptableWidth(8)
        attr = gridlib.GridCellAttr()
        attr.SetAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
        self.SetColAttr(0, attr)
        self.SetSelectionMode(gridlib.Grid.wxGridSelectRows)
        self.Bind(gridlib.EVT_GRID_CMD_SELECT_CELL, self.onGridSelectCell, self)
        self.oldSel = -1


    def SetSelection(self, row):
        self.SelectRow(row)
        self.oldSel = row


    def SetBackgroundColour(self, colour):
        self.SetDefaultCellBackgroundColour(colour)


    def SetForegroundColour(self, colour):
        self.SetDefaultCellTextColour(colour)


    def SetFont(self, font):
        self.SetDefaultCellFont(font)


    def GetSelection(self):
        return self.oldSel


    def Set(self, choices):
        oldLen = self.GetNumberRows()
        newLen = len(choices)
        h = self.GetDefaultRowSize()
        if oldLen > newLen:
            self.DeleteRows(0, oldLen - newLen, False)
        elif oldLen < newLen:
            self.AppendRows(newLen - oldLen, False)
        for i in range(len(choices)):
            self.SetCellValue(i, 0, " " + choices[i][0] + " ")
            self.SetRowSize(i, h)
        self.oldSel = 0 if newLen else -1


    def onGridSelectCell(self, event):
        row = event.GetRow()
        self.oldSel = row
        self.SelectRow(row)
        if not self.IsVisible(row, 0):
            self.MakeCellVisible(row, 0)
        event.Skip()


    def MoveCursor(self, step):
        max = self.GetNumberRows()
        sel = self.GetSelectedRows()[0]
        new = sel + step
        if new < 0:
            new += max
        elif new > max-1:
            new -= max
        self.SetGridCursor(new, 0)
        self.SelectRow(new)
#===============================================================================

class StartPresentation(eg.ActionClass):

    class text:
        pathLabel = 'Presentation file:'
        filemask = 'Presentations (*.pps, *.ppt, *.pptx, *.odp)|*.pps; *.ppt;\
            *.pptx; *.odp|All files (*.*)|*.*'
        toolTipFile = 'Click browse button to choose file'
        title = "Choose a file"


    def __call__(self, url = None, strt = 0, endless = False, pause = 0):
        if self.plugin.menuDlg is None and url is not None and exists(url):
            strt = strt if isinstance(strt, int) else self.plugin.str2int(strt)
            self.plugin.StartPresentation(url, strt, endless, pause)


    def Configure(self, url = None, start = 1, endless = False, pause = 0):
        panel = eg.ConfigPanel(self)
        sizer = wx.FlexGridSizer(2, 2, 20, 5)
        sizer.AddGrowableCol(1)
        label = wx.StaticText(
            panel,
            -1,
            self.text.pathLabel,
        )
        label2 = wx.StaticText(
            panel,
            -1,
            self.plugin.text.startLbl,
        )
        label3 = wx.StaticText(
            panel,
            -1,
            self.plugin.text.endless,
        )
        label3.SetToolTipString(self.plugin.text.endlessToolTip)
        label4 = wx.StaticText(
            panel,
            -1,
            self.plugin.text.pause,
        )
        label4.SetToolTipString(self.plugin.text.pauseToolTip)
        filepathCtrl = MyFileBrowseButton(
            panel,
            initialValue = url if (url is not None) else '',
            startDirectory = eg.folderPath.Documents,
            fileMask = self.text.filemask,
            toolTip = self.text.toolTipFile,
            dialogTitle = self.text.title,
        )
        startCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            start,
            min = 1,
            max = 999
        )
        filepathCtrl.GetTextCtrl().SetEditable(False)
        endlessCtrl = wx.CheckBox(panel, -1, "")
        endlessCtrl.SetValue(endless)
        endlessCtrl.SetToolTipString(self.plugin.text.endlessToolTip)

        def onEndless(evt=None):
            flag = endlessCtrl.GetValue()
            label4.Enable(flag)
            pauseCtrl.Enable(flag)
            if evt:
                evt.Skip()
        endlessCtrl.Bind(wx.EVT_CHECKBOX, onEndless)

        pauseCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            pause,
            min = 0,
            max = 999
        )
        pauseCtrl.SetToolTipString(self.plugin.text.pauseToolTip)
        onEndless()

        panel.sizer.Add(sizer, 1, wx.EXPAND|wx.ALL, 10)
        sizer.Add(label, 0, wx.TOP, 3)
        sizer.Add(filepathCtrl, 0, wx.EXPAND)
        sizer.Add(label2, 0, wx.TOP, 3)
        sizer.Add(startCtrl)
        sizer.Add(label3, 0, wx.TOP, 3)
        sizer.Add(endlessCtrl, 0, wx.EXPAND)
        sizer.Add(label4, 0, wx.TOP, 3)
        sizer.Add(pauseCtrl)

        while panel.Affirmed():
            panel.SetResult(
                filepathCtrl.GetValue(),
                startCtrl.GetValue(),
                endlessCtrl.GetValue(),
                pauseCtrl.GetValue(),
            )
#===============================================================================

class ShowMenu(eg.ActionClass):
    panel = None

    class text:
        filemask = "Presentations (*.pps, *.ppt, *.pptx, *.odp)|*.pps;*.ppt;\
            *.pptx; *.odp|All files (*.*)|*.*"
        toolTipFile = 'Click browse button to choose file'
        label = 'Menu label:'
        path = 'File:'
        menuPreview = 'On screen menu preview:'
        delete = 'Delete'
        insert = 'Insert new'
        menuFont = 'Menu font:'
        txtColour = 'Text colour'
        background = 'Background colour'
        txtColourSel = 'Selected text colour'
        backgroundSel = 'Selected background colour'
        inverted = "Use inverted colours"
        title = "Choose a file"
        OSELabel = 'Menu show on:'
        eventsBtn = "Events ..."
        dialog = "Playlist menu events assignement ..."
        btnToolTip ="""Press this button to assign events to control the menu !!!"""
        evtAssignTitle = "Menu control - events assignement"
        events = (
            "Cursor up:",
            "Cursor down:",
            "Select an item:",
            "Cancel (Escape):",
        )
        popup = (
            "Delete item",
            "Delete all items",
        )
        toolTip = "Drag-and-drop an event from the log into the box."
        cancel = 'Cancel'
        ok = 'OK'
        clear  = "Clear all"

    def Move(self, index, direction):
        tmpList = self.choices[:]
        max = len(self.choices)-1
        #Last to first position, other down
        if index == max and direction == 1:
            tmpList[1:] = self.choices[:-1]
            tmpList[0] = self.choices[max]
            index2 = 0
        #First to last position, other up
        elif index == 0 and direction == -1:
            tmpList[:-1] = self.choices[1:]
            tmpList[max] = self.choices[0]
            index2 = max
        else:
            index2 = index+direction
            tmpList[index] = self.choices[index2]
            tmpList[index2] = self.choices[index]
        self.choices = tmpList
        return index2

    def __call__(
        self,
        choices,
        fore,
        back,
        fontInfo,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75),
        inverted = True,
        monitor = 0,
        evtList = [[],[],[],[]],

    ):
        if not self.plugin.menuDlg:
            event = CreateEvent(None, 0, 0, None)
            wx.CallAfter(
                Menu,
                fore,
                back,
                foreSel,
                backSel,
                fontInfo,
                False,
                self.plugin,
                event,
                monitor,
                choices,
                evtList
            )
            eg.actionThread.WaitOnEvent(event)


    def GetLabel(
        self,
        choices,
        fore,
        back,
        fontInfo,
        foreSel,
        backSel,
        inverted,
        monitor,
        evtList,
    ):
        res = self.text.showMenu+' '
        for n in range(0,min(3, len(choices))):
            res=res + choices[n][0]+', '
        res = res[:-2]
        if len(choices) > 3:
            res += ', ...'
        return res


    def Configure(
        self,
        choices = [],
        fore = (0, 0, 0),
        back = (255, 255, 255),
        fontInfo = None,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75),
        inverted = True,
        monitor = 0,
        evtList = [[],[],[],[]],
    ):
        self.choices = choices
        self.fore = fore
        self.back = back
        self.foreSel = foreSel
        self.backSel = backSel
        self.oldSel = -1
        global panel
        panel = eg.ConfigPanel(self)
        panel.evtList = cpy(evtList)
        w1 = panel.GetTextExtent(self.text.label)[0]
        w2 = panel.GetTextExtent(self.text.path)[0]
        w = max((w1,w2))
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer = wx.GridBagSizer(5, 5)
        topMiddleSizer = wx.BoxSizer(wx.VERTICAL)
        previewLbl = wx.StaticText(panel, -1, self.text.menuPreview)
        previewLblSizer = wx.BoxSizer(wx.HORIZONTAL)
        previewLblSizer.Add(previewLbl)
        mainSizer.Add(previewLblSizer)
        mainSizer.Add(topSizer, 0, wx.TOP, 5)
        mainSizer.Add(bottomSizer, 0, flag = wx.TOP|wx.EXPAND, border = 16)
        panel.sizer.Add(mainSizer)

        wl = w + 165
        listBoxCtrl = MenuGrid(
            panel,
            len(self.choices),
            size = wx.Size(wl, -1)
        )
        listBoxCtrl.SetColSize(0, wl - SYS_VSCROLL_X)

        listBoxCtrl.SetDefaultRowSize(22)

        listBoxCtrl.SetBackgroundColour(self.back)
        listBoxCtrl.SetForegroundColour(self.fore)
        listBoxCtrl.SetSelectionBackground(self.backSel)
        listBoxCtrl.SetSelectionForeground(self.foreSel)
        oldFont = previewLbl.GetFont()
        if fontInfo is None:
            font = listBoxCtrl.GetFont()
            font.SetPointSize(36)
            fontInfo = font.GetNativeFontInfoDesc()
        else:
            font = wx.FontFromNativeInfoString(fontInfo)
        for n in range(10, 20):
            font.SetPointSize(n)
            previewLbl.SetFont(font)
            if previewLbl.GetTextExtent('X')[1] >= 28:
                font.SetPointSize(n - 4)
                previewLbl.SetFont(font)
                break
        listBoxCtrl.SetFont(font)
        previewLbl.SetFont(oldFont)


        label3 = wx.StaticText(
            panel,
            -1,
            self.plugin.text.endless,
        )
        label3.SetToolTipString(self.plugin.text.endlessToolTip)
        label4 = wx.StaticText(
            panel,
            -1,
            self.plugin.text.pause,
        )
        label4.SetToolTipString(self.plugin.text.pauseToolTip)

        endlessCtrl = wx.CheckBox(panel, -1, "")
        endlessCtrl.SetToolTipString(self.plugin.text.endlessToolTip)
        pauseCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            0,
            min = 0,
            max = 999
        )
        pauseCtrl.SetToolTipString(self.plugin.text.pauseToolTip)

        topSizer.Add(listBoxCtrl,0,wx.EXPAND)
        topSizer.Add((10,1))
        topSizer.Add(topMiddleSizer, 1, wx.EXPAND)
        topSizer.Add((20,1))
        labelLbl=wx.StaticText(panel, -1, self.text.label)
        labelCtrl=wx.TextCtrl(panel,-1,'',size=wx.Size(260,-1))
        labelCtrlSizer = wx.BoxSizer(wx.HORIZONTAL)
        labelCtrlSizer.Add(labelCtrl,0,wx.EXPAND)
        filepathLbl=wx.StaticText(panel, -1, self.text.path)
        filepathCtrl = MyFileBrowseButton(
            panel,
            startDirectory=eg.folderPath.Documents,
            fileMask = self.text.filemask,
            toolTip=self.text.toolTipFile,
            dialogTitle = self.text.title,
        )
        label2 = wx.StaticText(
            panel,
            -1,
            self.plugin.text.startLbl,
        )
        startCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            1,
            min = 1,
            max = 999
        )
        filepathCtrl.GetTextCtrl().SetEditable(False)
        bottomSizer.Add(filepathLbl,(0,0),flag = wx.TOP, border = 3)
        bottomSizer.Add(filepathCtrl,(0,1),(1,2),wx.EXPAND)
        bottomSizer.Add(labelLbl,(1,0),flag=wx.TOP,border=3)
        bottomSizer.Add(labelCtrlSizer,(1,1))
        bottomSizer.Add(label2,(2,0),flag = wx.TOP, border = 3)
        bottomSizer.Add(startCtrl,(2,1))
        bottomSizer.Add(label3,(3,0))
        bottomSizer.Add(endlessCtrl,(3,1))
        bottomSizer.Add(label4,(4,0),flag = wx.TOP, border = 3)
        bottomSizer.Add(pauseCtrl,(4,1))
        bottomSizer.AddGrowableCol(2)
        #Button UP
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
        btnUP = wx.BitmapButton(panel, -1, bmp)
        btnUP.Enable(False)
        topMiddleSizer.Add(btnUP)
        #Button DOWN
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16, 16))
        btnDOWN = wx.BitmapButton(panel, -1, bmp)
        btnDOWN.Enable(False)
        topMiddleSizer.Add(btnDOWN,0,wx.TOP,3)
        #Buttons 'Delete' and 'Insert new'
        w1 = panel.GetTextExtent(self.text.delete)[0]
        w2 = panel.GetTextExtent(self.text.insert)[0]
        if w1 > w2:
            btnDEL=wx.Button(panel,-1,self.text.delete)
            btnApp=wx.Button(panel,-1,self.text.insert,size=btnDEL.GetSize())
        else:
            btnApp=wx.Button(panel,-1,self.text.insert)
            btnDEL=wx.Button(panel,-1,self.text.delete,size=btnApp.GetSize())
        btnDEL.Enable(False)

        evtButton = wx.Button(panel, -1, self.text.eventsBtn)
        topMiddleSizer.Add(btnDEL,0,wx.TOP,5)
        topMiddleSizer.Add(btnApp,0,wx.TOP,5)
        topMiddleSizer.Add((-1, -1),1,wx.EXPAND)
        topMiddleSizer.Add(evtButton)
        #Font button
        fontLbl=wx.StaticText(panel, -1, self.text.menuFont)
        fontButton = eg.FontSelectButton(panel, value = fontInfo)
        #Button Text Colour
        foreLbl=wx.StaticText(panel, -1, self.text.txtColour + ':')
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
        foreSelLbl=wx.StaticText(panel, -1, self.text.txtColourSel+':')
        foreSelColourButton = eg.ColourSelectButton(panel,foreSel,title = self.text.txtColourSel)
        #Button Selected Background Colour
        backSelLbl=wx.StaticText(panel, -1, self.text.backgroundSel+':')
        backSelColourButton = eg.ColourSelectButton(panel,backSel,title = self.text.backgroundSel)
        useInvertedCtrl = wx.CheckBox(panel, -1, self.text.inverted)
        useInvertedCtrl.SetValue(inverted)
        OSElbl = wx.StaticText(panel, -1, self.text.OSELabel)
        displayChoice = eg.DisplayChoice(panel, monitor)
        topRightSizer = wx.GridBagSizer(2, 5)
        displaySizer = wx.BoxSizer(wx.HORIZONTAL)
        displaySizer.Add(OSElbl, 0,wx.TOP,3)
        displaySizer.Add((-1, -1), 1, wx.EXPAND)
        displaySizer.Add(displayChoice)
        topSizer.Add(topRightSizer)
        topRightSizer.Add(displaySizer, (0,0), (1,2),flag = wx.EXPAND)
        topRightSizer.Add(fontLbl, (1, 0), flag = wx.TOP, border = 5)
        topRightSizer.Add(fontButton, (1, 1), flag = wx.TOP, border = 2)
        topRightSizer.Add(foreLbl, (2, 0), flag = wx.TOP, border = 3)
        topRightSizer.Add(foreColourButton, (2, 1))
        topRightSizer.Add(backLbl, (3, 0), flag = wx.TOP, border = 3)
        topRightSizer.Add(backColourButton, (3, 1))
        topRightSizer.Add(foreSelLbl, (4, 0), flag = wx.TOP, border = 3)
        topRightSizer.Add(foreSelColourButton, (4, 1))
        topRightSizer.Add(backSelLbl, (5, 0), flag = wx.TOP, border = 3)
        topRightSizer.Add(backSelColourButton, (5, 1))
        topRightSizer.Add(useInvertedCtrl,(6,0),(1,2),flag = wx.TOP,border = 3)

        def OnEvtBtn(evt):
            dlg = MenuEventsDialog(
                parent = panel,
                action = self,
            )
            dlg.Centre()
            wx.CallAfter(
                dlg.ShowMenuEventsDialog,
                self.text.evtAssignTitle,
                self.text.events
            )
            evt.Skip()
        evtButton.Bind(wx.EVT_BUTTON, OnEvtBtn)

        def OnMonitor(evt):
            listBoxCtrl.SetFocus()
            evt.Skip
        displayChoice.Bind(wx.EVT_CHOICE, OnMonitor)


        def OnInverted(evt = None):
            flag = useInvertedCtrl.IsChecked()
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
            if evt:
                evt.Skip
        useInvertedCtrl.Bind(wx.EVT_CHECKBOX, OnInverted)
        OnInverted()


        def onStart(evt):
            sel = listBoxCtrl.GetSelection()
            val = startCtrl.GetValue()
            self.choices[sel][2]=val
            evt.Skip()
        startCtrl.Bind(wx.EVT_TEXT, onStart)


        def onEndless(evt=None):
            if self.choices:
                sel = listBoxCtrl.GetSelection()
                val = endlessCtrl.GetValue()
                label4.Enable(val)
                pauseCtrl.Enable(val)
                if not val:
                    pauseCtrl.numCtrl.ChangeValue(0)
                    self.choices[sel][4]=0
                self.choices[sel][3]=val
            if evt:
                evt.Skip()
        endlessCtrl.Bind(wx.EVT_CHECKBOX, onEndless)

        def onPause(evt):
            sel = listBoxCtrl.GetSelection()
            val = pauseCtrl.GetValue()
            self.choices[sel][4]=val
            evt.Skip()
        pauseCtrl.Bind(wx.EVT_TEXT, onPause)


        def FillData(item):
            labelCtrl.ChangeValue(item[0])
            filepathCtrl.GetTextCtrl().ChangeValue(item[1])
            startCtrl.SetValue(item[2])
            endlessCtrl.SetValue(item[3])
            pauseCtrl.SetValue(item[4])
            onEndless()

        def OnClickAfter():
            sel = listBoxCtrl.GetSelection()
            label = labelCtrl.GetValue()
            filepath = filepathCtrl.GetValue()
            if label.strip()<>"":
                if os.path.isfile(filepath):
                    if [item[0] for item in self.choices].count(label)==1:
                        if [item[1] for item in self.choices].count(filepath)==1:
                            self.oldSel=sel
                            item = self.choices[sel]
                            FillData(item)
            listBoxCtrl.SetSelection(self.oldSel)
            listBoxCtrl.SetFocus()


        def OnClick(evt):
            wx.CallAfter(OnClickAfter)
            evt.Skip()
        listBoxCtrl.Bind(gridlib.EVT_GRID_CMD_SELECT_CELL, OnClick)


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


        def OnFontBtn(evt):
            value = evt.GetValue()
            self.fontInfo = value
            oldFont = previewLbl.GetFont()
            font = wx.FontFromNativeInfoString(value)
            for n in range(10, 20):
                font.SetPointSize(n)
                previewLbl.SetFont(font)
                if previewLbl.GetTextExtent('X')[1] >= 28:
                    font.SetPointSize(n - 4)
                    previewLbl.SetFont(font)
                    break
            listBoxCtrl.SetFont(font)
            previewLbl.SetFont(oldFont)
            listBoxCtrl.SetFocus()
            if evt:
                evt.Skip()
        fontButton.Bind(eg.EVT_VALUE_CHANGED, OnFontBtn)


        def OnButtonUp(evt):
            newSel = self.Move(listBoxCtrl.GetSelection(), -1)
            listBoxCtrl.Set(self.choices)
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            listBoxCtrl.SetFocus()
            evt.Skip()
        btnUP.Bind(wx.EVT_BUTTON, OnButtonUp)


        def OnButtonDown(evt):
            newSel = self.Move(listBoxCtrl.GetSelection(), 1)
            listBoxCtrl.Set(self.choices)
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            listBoxCtrl.SetFocus()
            evt.Skip()
        btnDOWN.Bind(wx.EVT_BUTTON, OnButtonDown)


        def EnableCtrls(flag):
            labelCtrl.Enable(flag)
            labelLbl.Enable(flag)
            filepathCtrl.Enable(flag)
            filepathLbl.Enable(flag)
            startCtrl.Enable(flag)
            label2.Enable(flag)
            endlessCtrl.Enable(flag)
            label3.Enable(flag)
            pauseCtrl.Enable(flag)
            label4.Enable(flag)


        def OnButtonDelete(evt):
            lngth = len(self.choices)
            if lngth == 2:
                btnUP.Enable(False)
                btnDOWN.Enable(False)
            sel = oldSel = listBoxCtrl.GetSelection()
            if lngth == 1:
                self.choices = []
                labelCtrl.ChangeValue('')
                filepathCtrl.GetTextCtrl().ChangeValue('')
                EnableCtrls(False)
                panel.EnableButtons(False)
                btnDEL.Enable(False)
                btnApp.Enable(True)
                listBoxCtrl.Set(self.choices)
                listBoxCtrl.SetFocus()
                self.oldSel = -1
                evt.Skip()
                return
            self.choices.pop(oldSel)
            if sel == lngth - 1:
                sel = 0
                self.oldSel = sel
            listBoxCtrl.Set(self.choices)
            listBoxCtrl.SetSelection(sel)
            item = self.choices[sel]
            labelCtrl.ChangeValue(item[0])
            filepathCtrl.GetTextCtrl().ChangeValue(item[1])
            startCtrl.SetValue(item[2])
            endlessCtrl.SetValue(item[3])
            pauseCtrl.SetValue(item[4])
            listBoxCtrl.SetFocus()
            onEndless()
            evt.Skip()
        btnDEL.Bind(wx.EVT_BUTTON, OnButtonDelete)

        def OnTextChange(evt):
            if self.choices <> []:
                flag = False
                sel = self.oldSel
                label = labelCtrl.GetValue()
                filepath = filepathCtrl.GetValue()
                self.choices[sel][0] = label
                self.choices[sel][1] = filepath
                listBoxCtrl.Set(self.choices)
                listBoxCtrl.SetSelection(sel)
                if label.strip()<>"":
                    if os.path.isfile(filepath):
                        if [item[0] for item in self.choices].count(label)==1:
                            if [item[1] for item in self.choices].count(filepath)==1:
                                flag = True
                panel.EnableButtons(flag)
                btnApp.Enable(flag)
            evt.Skip()
        labelCtrl.Bind(wx.EVT_TEXT, OnTextChange)
        filepathCtrl.Bind(wx.EVT_TEXT, OnTextChange)


        def OnButtonAppend(evt):
            if len(self.choices) == 1:
                btnUP.Enable(True)
                btnDOWN.Enable(True)
            EnableCtrls(True)
            sel = listBoxCtrl.GetSelection() + 1
            self.oldSel = sel
            item = ['', '', 1, False, 0]
            self.choices.insert(sel, item)
            listBoxCtrl.Set(self.choices)
            listBoxCtrl.SetSelection(sel)
            FillData(item)
            evt.Skip()
        btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)

        # re-assign the test button
        def OnButton(event):
            self.plugin.choices = self.choices

            if not self.plugin.menuDlg:
                wx.CallAfter(
                    Menu,
                    foreColourButton.GetValue(),
                    backColourButton.GetValue(),
                    foreSelColourButton.GetValue(),
                    backSelColourButton.GetValue(),
                    fontButton.GetValue(),#self.fontInfo,
                    True,
                    self.plugin,
                    CreateEvent(None, 0, 0, None),
                    displayChoice.GetSelection(),
                    self.choices,
                    panel.evtList,
                )
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnButton)

        if len(self.choices) > 0:
            listBoxCtrl.Set(self.choices)
            listBoxCtrl.SetSelection(0)
            item = self.choices[0]
            labelCtrl.ChangeValue(item[0])
            filepathCtrl.GetTextCtrl().ChangeValue(item[1])
            startCtrl.SetValue(item[2])
            endlessCtrl.SetValue(item[3])
            pauseCtrl.SetValue(item[4])
            self.oldSel=0
            btnUP.Enable(True)
            btnDOWN.Enable(True)
            btnDEL.Enable(True)
        else:
            EnableCtrls(False)
            panel.EnableButtons(False)
        onEndless()
        panel.sizer.Layout()

        while panel.Affirmed():
            panel.SetResult(
            self.choices,
            foreColourButton.GetValue(),
            backColourButton.GetValue(),
            fontButton.GetValue(),
            foreSelColourButton.GetValue(),
            backSelColourButton.GetValue(),
            useInvertedCtrl.GetValue(),
            displayChoice.GetSelection(),
            panel.evtList,
        )
#======================================================================

#Group GoTo slide ...:
class DigitAction(eg.ActionClass):

    def __call__(self):
        cntrllr = self.plugin.controller
        if cntrllr and cntrllr.isRunning():
            self.plugin.number += self.value
            self.plugin.ShowNumLabel()
            eg.event.skipEvent = True
#======================================================================

class Enter(eg.ActionClass):

    def __call__(self):
        cntrllr = self.plugin.controller
        if cntrllr and cntrllr.isRunning():
            if (self.plugin.numDialog is not None) and (len(self.plugin.number)>0):
                last = cntrllr.getSlideCount()
                dest = min(last, self.plugin.str2int(self.plugin.number))
                self.plugin.numDialog.CloseDialog()
                cntrllr.gotoSlideIndex(dest - 1)
                self.plugin.number = ''
                eg.event.skipEvent = True
#======================================================================

class Backspace(eg.ActionClass):

    def __call__(self):
        if (self.plugin.numDialog is not None) and (len(self.plugin.number)>0):
                self.plugin.number = self.plugin.number[:-1]
                if len(self.plugin.number) == 0:
                    self.plugin.numDialog.CloseDialog()
                else:
                    self.plugin.ShowNumLabel()
                eg.event.skipEvent = True
#======================================================================

class Cancel(eg.ActionClass):

    def __call__(self):
        if self.plugin.numDialog is not None:
            self.plugin.number = ''
            self.plugin.numDialog.CloseDialog()
            eg.event.skipEvent = True
#======================================================================

class ComAction(eg.ActionClass):

    def __call__(self):
        cntrllr = self.plugin.controller
        if cntrllr and cntrllr.isRunning():
            return getattr(cntrllr, self.value)()
#======================================================================

class blankScreen(eg.ActionClass):

    class text:
        color = 'Choose a blank screen color'

    def __call__(self, color = (0, 0, 0)):
        cntrllr = self.plugin.controller
        if cntrllr and cntrllr.isRunning():
            color = color[2] + 256 * color[1] + 65536 * color[0]
            if self.plugin.numDialog is None and self.plugin.menuDlg is None:
                cntrllr.resume()
                return cntrllr.blankScreen(color)


    def Configure(self, color = (0, 0, 0)):
        panel = eg.ConfigPanel()
        colorLbl = wx.StaticText(panel, -1, self.text.color + ':')
        colorButton = eg.ColourSelectButton(panel, color, title=self.text.color)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(colorLbl,0,wx.TOP,3)
        sizer.Add(colorButton,0,wx.LEFT,5)
        panel.sizer.Add(sizer,0,wx.ALL,20)
        while panel.Affirmed():
            panel.SetResult(
                colorButton.GetValue(),
            )

#======================================================================

class Exit(eg.ActionClass):

    def __call__(self):
        cntrllr = self.plugin.controller
        if cntrllr and cntrllr.isRunning():
            self.plugin.StopPresentation()


#===============================================================================

ACTIONS = (
    ( eg.ActionGroup, 'GotoSlide', 'GoTo slide actions', 'GoTo slide actions', (
        (DigitAction, 'Digit0', 'Digit 0', 'Type Digit 0', '0' ),
        (DigitAction, 'Digit1', 'Digit 1', 'Type Digit 1', '1' ),
        (DigitAction, 'Digit2', 'Digit 2', 'Type Digit 2', '2' ),
        (DigitAction, 'Digit3', 'Digit 3', 'Type Digit 3', '3' ),
        (DigitAction, 'Digit4', 'Digit 4', 'Type Digit 4', '4' ),
        (DigitAction, 'Digit5', 'Digit 5', 'Type Digit 5', '5' ),
        (DigitAction, 'Digit6', 'Digit 6', 'Type Digit 6', '6' ),
        (DigitAction, 'Digit7', 'Digit 7', 'Type Digit 7', '7' ),
        (DigitAction, 'Digit8', 'Digit 8', 'Type Digit 8', '8' ),
        (DigitAction, 'Digit9', 'Digit 9', 'Type Digit 9', '9' ),
        (Enter, 'Enter', 'Enter', 'Enter - Goto slide.', None),
        (Backspace, 'Backspace', 'Backspace', 'Backspace (delete last digit).', None),
        (Cancel, 'Cancel', 'Cancel', 'Cancel - Do not goto a slide.', None),
    )),
    ( eg.ActionGroup, 'Other', 'Other actions', 'Other actions', (
        (StartPresentation, 'StartPresentation', 'Start presentation', 'Start presentation.', None),
        (Exit, 'Exit', 'End presentation', 'End presentation.', None ),
        (ComAction, 'stopSound', 'Stop all sounds', 'Stop all currently played sounds.', u'stopSound' ),
        (blankScreen, 'Blank', 'Blank screen', 'Pauses the slide show and blanks the screen in the given color.', None ),
        (ComAction, 'getCurrentSlideIndex', 'Get current slide index', 'Returns the index of the current slide.', u'getCurrentSlideIndex'),
        (ShowMenu, 'ShowMenu', 'Show menu', 'Show menu.', None),
        (ComAction, 'Pause', 'Pause presentation', 'Pause presentation.', u'pause' ),
        (ComAction, 'Resume', 'Resume presentation', 'Resume presentation.', u'resume' ),
        (ComAction, 'Next', 'Play next effect/slide', 'Play next effect (if any, else go to next slide).', u'gotoNextEffect' ),
        (ComAction,
            'Previous', 'Play previous effect/slide',
            'Play previous effect again. If no previous effect exists on this slide, show previous slide.',
            u'gotoPreviousEffect'
        ),
        (ComAction, 'NextWithout', 'Next slide without effects', 'Go to next slide without playing effects.', u'gotoNextSlide' ),
        (ComAction, 'PreviousWithout', 'Previous slide without effects', 'Go to the previous slide without playing effects.', u'gotoPreviousSlide' ),
        (ComAction, 'First', 'First slide', 'Jump to first slide in the slide show.', u'gotoFirstSlide' ),
        (ComAction, 'Last', 'Last slide', 'Jump to the last slide in the slide show.', u'gotoLastSlide' ),
        (ComAction, 'GetSlide', 'GetSlide', 'GetSlide.', u'getCurrentSlide' ),
        (ComAction, 'getNextSlideIndex', 'getNextSlideIndex', 'getNextSlideIndex.', u'getNextSlideIndex' ),
    )),
)
#====================================================================


class Impress(eg.PluginClass):

    menuDlg = None
    numDialog = None
    number = ''
    choices = []
    hwnd = 0
    text = Text

    def __init__(self):
        self.AddActionsFromList(ACTIONS)


    def __start__(self):
        eg.Bind("Impress.Menu.DefaultAction", self.OnGui)
        self.controller = None
        self.presentation = None


    def __stop__(self):
        eg.Unbind("Impress.Menu.DefaultAction", self.OnGui)
        self.StopPresentation()


    def str2int(self, s):
        s = eg.ParseString(s)
        try:
            s = int(s)
        except:
            s = 0
        return s


    def OnGui(self, event):
        self.StartPresentation(*event.payload)
        return True


    def ImprIsRunning(self, hwnd):
        self.sched = eg.scheduler.AddTask(2, self.ImprIsRunning, hwnd)
        if not IsWindow(hwnd):
            self.StopPresentation()


    def StopPresentation(self):
        if hasattr(self, 'sched') and self.sched:
            eg.scheduler.CancelTask(self.sched)
        if hasattr(self.presentation, "end"):
            self.presentation.end()
        if hasattr(self, 'hWnd') and IsWindow(self.hWnd):
            PostMessage(self.hWnd, WM_CLOSE, 0, 0)
        self.controller = None
        self.presentation = None


    def StartPresentation(self, url, start, endless, pause):
        if not exists(url):
            self.PrintError(self.text.err3 % url)
            return
        objServiceManager = Dispatch('com.sun.star.ServiceManager')
        objServiceManager._FlagAsMethod("Bridge_GetStruct")

        def makePropertyValue(Name, Value):
            """Create a com.sun.star.beans.PropertyValue struct and return it.
            """
            oPropertyValue = objServiceManager.Bridge_GetStruct(
                "com.sun.star.beans.PropertyValue")
            oPropertyValue.Name = Name
            oPropertyValue.Value = Value
            return oPropertyValue

        desktop = objServiceManager.CreateInstance('com.sun.star.frame.Desktop')
        try:
            doc = desktop.loadComponentfromURL(
                "private:factory/simpress",
                "_default", #"_blank",
                0,
                []
            )
            win = doc.CurrentController.Frame.ContainerWindow
            hWnd = win.getWindowHandle([], 1) # 1 ~ for MS Windows env.
            SendMessageTimeout(hWnd, WM_SYSCOMMAND, SC_MINIMIZE, 0)
            doc = desktop.loadComponentfromURL("file:///"+url,'_default',0,[])
        except:
            self.PrintError(self.text.err1 % url)
            return
        presentation = doc.getPresentation()
        self.controller = presentation.getController()
        val0 = makePropertyValue("IsFullScreen", True)
        val1 = makePropertyValue("IsAlwaysOnTop", True)
        val2 = makePropertyValue("IsEndless", endless)
        val3 = makePropertyValue("Pause", pause)  #Duration of black screen after last slide  [integer, seconds]  // only when presentation is Endless
        presentation.startWithArguments([val0, val1, val2, val3])
        self.controller = presentation.getController()
        if start > 1:
            self.controller.gotoSlideIndex(start - 1)
        self.presentation = presentation
        hwnd = findPresentation()
        if len(hwnd) > 0:
            hwnd = hwnd[0]
            self.hWnd = hWnd
            self.ImprIsRunning(hwnd)
            SetForegroundWindow(hwnd)
            SetActiveWindow(hwnd)
        else:
            self.PrintError(self.text.err2)


    def ShowNumLabel(self):
        if self.numDialog is not None:
            statText = self.numDialog.GetSizer().GetChildren()[0].GetWindow()
            statText.SetLabel(self.number)
        else:
            self.TriggerEvent("GoToFrame.%s" % self.text.opened)
            NumDialog(self)
            statText=wx.StaticText(
                self.numDialog,
                -1,
                self.number,
                style = wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE
            )
            font = statText.GetFont()
            font.SetPointSize(100)
            font.SetWeight(wx.BOLD)
            statText.SetFont(font)
            self.numDialog.SetBackgroundColour(wx.Colour(0,255,255))
            statText.SetForegroundColour(wx.Colour(0,255,255))
            statText.SetBackgroundColour(wx.Colour(0, 0, 139))
            w,h = statText.GetTextExtent('8888')
            self.numDialog.SetSize((w+16,h+16))
            statText.SetPosition((7,7))
            statText.SetSize((w,h))
            mainSizer =wx.BoxSizer(wx.VERTICAL)
            self.numDialog.SetSizer(mainSizer)
            mainSizer.Add(statText, 0, wx.EXPAND)
            self.numDialog.Centre()
            self.numDialog.Show()
#===============================================================================

