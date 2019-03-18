# -*- coding: utf-8 -*-
#
# plugins/PotPlayer/__init__.py
#
# Copyright (C) 2013 Pako
#
# This file is a plugin for EventGhost.
# Copyright (C) 2005-2013 Lars-Peter Voss <bitmonster@eventghost.org>
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
    
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.3 by Pako 2013-12-09 08:31 UTC+1
#     - bugfix (speed control) wrong command ID
# 0.2 by Pako 2013-11-09 12:31 UTC+1
#     - bugfix (action add/play) when filename contains non-ascii characters too
# 0.1 by Pako 2013-11-02 13:43 UTC+1
#     - support URL (EventGhost forum) added
#     - add/play file renamed to add/play file/folder
# 0.0 by Pako 2013-10-22 13:12 UTC+1
#     - initial version

eg.RegisterPlugin(
    name = "PotPlayer",
    author = "Pako",
    version = "0.3",
    kind = "program",
    guid = "{F711529C-FE41-4DC7-906D-8D44FF3D62C1}",
    createMacrosOnAdd = True,
    description = (
        'Adds actions to control '
        '<a href="http://tvpot.daum.net/application/PotPlayer.do">PotPlayer</a>.'
    ),
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAByElEQVR42mN0Svz8nwE/"
        "eADEB4B44b75vAfQJRlBBvBwMTIoyzGhSDx99ZPh2etfDCxM7AxMjMwwYZABgUCDPqAY"
        "oK/BzNBXxonV+hsPvjHsPPqbYf3ufwzMTKwgoQtA7AgzhKAByAa1z/rG8OQFB9gQoAGG"
        "JBnw6fNnhuu3HjPUzxJl+P0brDYRaMgCrAZMWPSTwcaIhcFEB+L3Hz9+MDx8/ISBhZmZ"
        "4ehlFoaFGwXhrsBqQMecH2BaXJiJwc4Y6My/zxhYWFgY2NjZGH7/YWGIrWIEhwfQAEas"
        "BpT3fUdxvqz4b4Yoz79gA9jZ2BhiKr8yvHnHgtsA56QvcDY3UDglmJHB3YaVgRXoCiYm"
        "JgavzLcMP3+yYxrw5etXhnfv3jMk1guANUd6AiPdhYVBgJ8N6GRIOvn89S+Db/YnVC/o"
        "qjIyVCR9Zfj16xcDG9CJk5ZzMaSFMDPISLCC/Y4Mthz6wtC/AJKogAY4gg3QUPjDUJP2"
        "A6iZnYEd6k+QRkZGRhTNINvDSz6AnY8SjdrK/xla8hiAGtkZWFkh/sSWkLrmAqPzKRtm"
        "QtJTY2LoKeVgYGbGrpFgUiYhM22AOh01MzHgBw8Y8GRnALMj2BGuN2wjAAAAAElFTkSu"
        "QmCC"
    ),
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=5738"
)
#===============================================================================

import eg
import wx
import _winreg
from os import environ
from os.path import join, exists, isfile, isdir, split
from subprocess import Popen
from eg.WinApi import SendMessageTimeout, WM_COMMAND
from eg.WinApi.Utils import GetMonitorDimensions
from eg.WinApi.Dynamic import PostMessage
from eg.WinApi.Dynamic import CreateEvent, SetEvent
from threading import Timer
from win32gui import GetSubMenu, GetMenuItemCount, GetDlgCtrlID 
from win32gui import GetClassName, GetWindowText
from win32gui import SendMessage, FindWindow, IsWindow, GetWindow
from copy import deepcopy as cpy
from time import sleep
from winsound import PlaySound, SND_ASYNC
from ctypes import addressof, c_int, c_buffer
from ctypes import create_string_buffer
from ctypes import byref, sizeof, c_long, c_ulong, Structure
from ctypes.wintypes import WinDLL
_user32 = WinDLL("user32")
import wx.grid as gridlib
from sys import getfilesystemencoding
FSE = getfilesystemencoding()
from eg.Classes.MainFrame.TreeCtrl import DropTarget as EventDropTarget

ARIAL_INFO  = "0;-35;0;0;0;700;0;0;0;0;3;2;1;34;Arial"

WM_INITMENUPOPUP = 0x0117
MF_GRAYED        = 1
MF_DISABLED      = 2
MF_CHECKED       = 8
MF_BYPOSITION    = 1024
MF_SEPARATOR     = 2048
SYS_VSCROLL_X    = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
SYS_HSCROLL_Y    = wx.SystemSettings.GetMetric(wx.SYS_HSCROLL_Y)
arialInfoString  = "0;-35;0;0;0;700;0;0;0;0;3;2;1;34;Arial"
GW_CHILD         = 5
GW_HWNDNEXT      = 2
BN_CLICKED       = 0
WM_SETTEXT       = 12
WM_CLOSE         = 16
EM_GETLINE       = 196
WM_CONTEXTMENU   = 0x007B
OBJID_CLIENT     = 0xFFFFFFFC
MENUsubst = {
    10059:"5 Sec.",
    10060:"5 Sec.",
    10061:"30 Sec.",
    10062:"30 Sec.",
    10063:"1 Min.",
    10064:"1 Min.",
    10065:"5 Min.",
    10066:"5 Min.",
    10579:"X Sec.",
    10580:"X Sec.",
    10140:"X Sec.",
    10141:"X Sec.",
    10291:"X Sec.",
    10292:"X Sec.",
    10479:"<Time X>",
    10784:"X Min.",
    10022:"Custom ratio",
}
#===============================================================================

def getEditText(hwnd):
    buf = create_string_buffer(32 * "0")
    valLngth = SendMessage(hwnd, EM_GETLINE, 0, addressof(buf))
    return buf.value[:valLngth].decode(eg.systemEncoding)
#===============================================================================

class FixedWidth(wx.FontEnumerator):

    def __init__(self):
        wx.FontEnumerator.__init__(self)
        self.fontList = []

    def OnFacename(self, fontname):
        if not fontname.startswith("@"): 
            self.fontList.append(fontname)
        return True

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
            txt = self.customData.GetData().tobytes()
            ix, evtList = self.object.GetEvtList()
            flag = True
            for lst in evtList:
                if txt in lst:
                    flag = False
                    break
            if flag:
                self.object.InsertItem(len(evtList[ix]), txt, 0)
                self.object.UpdateEvtList(ix, txt)
                return wx.DragCopy
            else:
                PlaySound('SystemExclamation', SND_ASYNC)
                return wx.DragError
        return wx.DragNone


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
        self.il.Add(wx.Bitmap(wx.Image(
            join(eg.imagesDir, "event.png"), wx.BITMAP_TYPE_PNG)))
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.InsertColumn(0, '')
        self.SetColumnWidth(0, width - 5 - SYS_VSCROLL_X)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        self.Bind(wx.EVT_SET_FOCUS, self.OnChange) 
        self.Bind(wx.EVT_LIST_INSERT_ITEM, self.OnChange) 
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnChange) 
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClick)
        self.SetToolTip(self.plugin.text.toolTip)


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
            self.popupID1 = wx.NewIdRef()
            self.popupID2 = wx.NewIdRef()
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
            self.InsertItem(i, evtList[i], 0)
#===============================================================================

class GoToFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(
            self,
            None,
            -1,
            'PPgotoFrame',
            style=wx.STAY_ON_TOP | wx.SIMPLE_BORDER,
        )
        self.GoToCtrl = None
        self.pos = -1
        self.posList = (0,1,3,4,6,7)
        self.gotowin = None
        self.total = None
        self.evtList = [[],[],[],[],[]]
        self.plugin = None


    def UpdateOSD(self, data=None):
        if data:
            self.GoToCtrl.SetValue(data)
        if self.pos > -1:
            pos = self.posList[self.pos]
            self.GoToCtrl.SetStyle(
                0,
                pos,
                wx.TextAttr(self.fore, self.back, self.fnt)
            )
            self.GoToCtrl.SetStyle(
                pos,
                pos+1,
                wx.TextAttr(self.foreSel, self.backSel, self.fnt)
            )
            self.GoToCtrl.SetStyle(
                pos+1,
                8,
                wx.TextAttr(self.fore, self.back, self.fnt)
            )
            f = self.fore
            b = self.back
        else:
            self.GoToCtrl.SetStyle(
                0,
                8,
                wx.TextAttr(self.fore, self.back, self.fnt)
            )
            f = self.foreSel
            b = self.backSel
        self.gotoLbl.SetBackgroundColour(b)
        self.gotoLbl.SetForegroundColour(f)
        self.Refresh()


    def MoveCursor(self, step):
        max = len(self.posList)-1
        min = 0
        value = self.pos
        value += step
        if value == -2:
            value = max
        elif value > max:
            value = -1
        self.pos = value
        self.UpdateOSD()


    def Turn(self, step):
        min = 0
        max = 9
        if self.pos == -1:
            self.GoTo()
            return
        pos = self.posList[self.pos]
        data = list(self.GoToCtrl.GetValue())
        value = int(data[pos])
        if pos == 6:
            max = 5
        elif pos == 4 and len(self.posList)==3:
            max = int(self.total[4])
        elif pos == 3:
            max = 5
            if len(self.posList)==4:
                max = int(self.total[3])
        elif pos == 1 and len(self.posList)==5:
            max = int(self.total[1])
        elif pos == 0 and len(self.posList)==6:
            max = int(self.total[0])
        value += step
        if value < min:
            value = max
        elif value > max:
            value = min
        data[pos] = str(value)
        self.UpdateOSD(''.join(data))


    def ShowGoToFrame(
        self,
        fore,
        back,
        foreSel,
        backSel,
        fontFace,
        fontSize,
        flag,
        plugin,
        event,
        monitor,
        hWnd,
        evtList,
        sizeFlag
    ):
        self.plugin = plugin
        eg.TriggerEvent("OSD.%s" % self.plugin.text.opened, prefix="PotPlayer")
        self.flag = False
        self.Bind(wx.EVT_CLOSE, self.onClose)
        PostMessage(hWnd, WM_COMMAND, 10325, 0) #Open PP GoTo dialog
        editId = 3069
        buttonId = 3021
        fndGoToWin = eg.WindowMatcher(
            split(self.plugin.ppPath)[1],
            u'',
            u'#32770',
            None,
            None,
            None,
            True,
            0.0,
            0
        )
        for i in range(1000):
            sleep(0.1)                
            GoToWin = fndGoToWin()
            if len(GoToWin) > 0:
                break
        if not GoToWin:
            self.destroyMenu()
            wx.Yield()
            SetEvent(event)
            return
        button = 0
        for gotowin in GoToWin:
            edit = GetWindow(gotowin, GW_CHILD)
            while edit > 0:
                if GetDlgCtrlID(edit) == editId and GetClassName(edit) =='Edit':
                    break
                edit = GetWindow(edit, GW_HWNDNEXT)
            if edit > 0:
                button = edit
                break
        while button > 0:
            if GetDlgCtrlID(button)==buttonId and GetClassName(button)=='Button':
                break
            button = GetWindow(button, GW_HWNDNEXT)
        if not button:
            self.destroyMenu()
            wx.Yield()
            SetEvent(event)
            return
        self.gotowin = gotowin
        eg.WinApi.Utils.ShowWindow(gotowin, False)
        label = self.plugin.text.goto
        self.edit = edit
        self.button = button
        self.back = back
        self.fore = fore
        self.foreSel = foreSel
        self.backSel = backSel
        self.flag = flag
        self.evtList = evtList
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
        self.gotoLbl=wx.StaticText(self, -1, label, pos = (5,5))
        self.gotoLbl.SetBackgroundColour(self.back)
        self.gotoLbl.SetForegroundColour(self.fore)
        gt = self.gotoLbl.GetTextExtent(label)
        fnt = self.gotoLbl.GetFont()
        border = fontSize/3
        fnt.SetPointSize(6*fontSize/10)
        fnt.SetWeight(wx.FONTWEIGHT_BOLD)
        self.gotoLbl.SetFont(fnt)
        labelSize = self.gotoLbl.GetTextExtent(label)
        self.gotoLbl.SetSize(labelSize)
        self.gotoLbl.SetPosition((border,border))
        self.GoToCtrl = wx.TextCtrl(
                    self,
                    -1,
                    style=wx.TE_RICH2|wx.NO_BORDER|wx.TE_READONLY|wx.TE_CENTER,
                )
        fnt.SetFaceName(fontFace)
        fnt.SetPointSize(fontSize)
        self.GoToCtrl.SetFont(fnt)
        self.fnt = fnt
        data = getEditText(self.edit)
        data = data.split(".")[0]
        wx.CallAfter(self.UpdateOSD, data)
        gotoSize = self.GoToCtrl.GetTextExtent("00:00:00")
        if sizeFlag:
            gotoSize = (1.4*gotoSize[0],gotoSize[1])
        self.GoToCtrl.SetSize(gotoSize)
        self.GoToCtrl.SetPosition((border, 1.5*border+labelSize[1]))
        self.SetSize(
            (4+gotoSize[0]+2*border,2+labelSize[1]+gotoSize[1]+2.5*border)
        )
        self.SetBackgroundColour(self.back)
        self.GoToCtrl.SetBackgroundColour(self.back)
        self.Bind(wx.EVT_CHAR_HOOK, self.onFrameCharHook)
        monDim = GetMonitorDimensions()
        try:
            x,y,ws,hs = monDim[monitor]
        except IndexError:
            x,y,ws,hs = monDim[0]
        width,height = self.GetSizeTuple()
        x_pos = x + (ws - width)/2
        y_pos = y + (hs - height)/2
        self.SetPosition((x_pos,y_pos) )
        self.Show(True)
#        self.Raise()
        self.gotoLbl.SetFocus()
        if self.flag:
            self.timer=MyTimer(t = 5.0, plugin = self.plugin)
        wx.Yield()
        SetEvent(event)


    def onUp(self, event):
        wx.CallAfter(self.Turn, 1)


    def onDown(self, event):
        wx.CallAfter(self.Turn, -1)


    def onLeft(self, event):
        wx.CallAfter(self.MoveCursor, -1)


    def onRight(self, event):
        wx.CallAfter(self.MoveCursor, 1)


    def onEscape(self, event):
        wx.CallAfter(self.destroyMenu)


    def GoTo(
        self,
    ):
        buttonId = 3021
        data = self.GoToCtrl.GetValue()
        locBuf = create_string_buffer(data)
        SendMessage(self.edit,WM_SETTEXT,0,addressof(locBuf))
        SendMessage(
            self.gotowin,
            WM_COMMAND,
            buttonId + 65536 * BN_CLICKED,
            self.button
        )
        self.destroyMenu()


    def onFrameCharHook(self, event):
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_F4:
            if event.AltDown():
                self.destroyMenu()
        elif keyCode == wx.WXK_RETURN or keyCode == wx.WXK_NUMPAD_ENTER:
            self.GoTo()
        elif keyCode == wx.WXK_RIGHT or keyCode == wx.WXK_NUMPAD_RIGHT:
            self.MoveCursor(1)
        elif keyCode == wx.WXK_ESCAPE:
            self.destroyMenu()
        elif keyCode == wx.WXK_UP or keyCode == wx.WXK_NUMPAD_UP:
            self.Turn(1)
        elif keyCode == wx.WXK_DOWN or keyCode == wx.WXK_NUMPAD_DOWN:
            self.Turn(-1)
        elif keyCode == wx.WXK_LEFT or keyCode == wx.WXK_NUMPAD_LEFT:
            self.MoveCursor(-1)
        else:
            event.Skip()


    def onClose(self, event):
        self.Show(False)
        self.Destroy()
        if self.plugin:
            self.plugin.menuDlg = None
        if self.gotowin and IsWindow(self.gotowin):
            PostMessage(self.gotowin, WM_CLOSE, 0, 0)


    def destroyMenu(self):
        if self.flag:
            self.timer.Cancel()
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
        eg.TriggerEvent("OSD.%s" % self.plugin.text.closed, prefix ="PotPlayer")
        self.Close()
#===============================================================================

class MenuEventsDialog(wx.MiniFrame):

    def __init__(self, parent, plugin):
        wx.MiniFrame.__init__(
            self,
            parent,
            -1,
            style=wx.CAPTION,
            name="OSD_EventsManager"
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
        
        ln = len(labels)
        evtLabels = ln * [None]
        eventsCtrls = ln * [None]
        dts = ln * [None]
        self.ids = ln * [None]
        for i in range(ln):
            s = i % 2
            if s: #odd
                lc = (i-1, 1)
                cc = (i, 1)
            else: #even
                lc = (i, 0)
                cc = (i+1, 0)
            evtLabels[i]=wx.StaticText(self, -1, labels[i])
            self.ids[i] = wx.NewIdRef()
            eventsCtrls[i] = EventListCtrl(
                self,
                self.ids[i],
                self.evtList,
                i,
                self.plugin
            )
            eventsCtrls[i].SetItems(self.evtList[i])
            dts[i] = MyTextDropTarget(eventsCtrls[i])
            eventsCtrls[i].SetDropTarget(dts[i])
            eventsCtrls[i].Bind(eg.EVT_VALUE_CHANGED, onFocus)
            b = 8 if i > 1 else 0
            topSizer.Add(evtLabels[i], lc, flag = wx.TOP, border = b)
            topSizer.Add(eventsCtrls[i], cc, flag = wx.EXPAND)

        deleteSizer = wx.BoxSizer(wx.VERTICAL)
        delOneBtn = wx.Button(self, -1, self.plugin.text.popup[0])
        delBoxBtn = wx.Button(self, -1, self.plugin.text.popup[1])
        clearBtn  = wx.Button(self, -1, self.plugin.text.clear)
        deleteSizer.Add(delOneBtn, 1, wx.EXPAND)
        deleteSizer.Add(delBoxBtn, 1, wx.EXPAND|wx.TOP,5)
        deleteSizer.Add(clearBtn, 1, wx.EXPAND|wx.TOP,5)
        i += 1
        b = 0 if i % 2 else 10       
        topSizer.Add(deleteSizer, (i, 1), flag = wx.EXPAND|wx.TOP, border = b)

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
            ln = len(self.ids)
            for i in range(ln):
                wx.FindWindowById(self.ids[i]).DeleteAllItems()
            delOneBtn.Enable(False)
            delBoxBtn.Enable(False)
            self.evtList = ln*[[]]
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

class Menu(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(
            self,
            None,
            -1,
            'pp_menu',
            style = wx.STAY_ON_TOP|wx.SIMPLE_BORDER
        )
        self.flag = False
        self.monitor = 0
        self.oldMenu = []
        self.messStack = []


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
        self.menuGridCtrl.SetDimensions(2,2,width-6,height-6,wx.SIZE_AUTO)
        self.Show(True)
        self.menuGridCtrl.MakeCellVisible(ix, 1)
        self.Raise()


    def ShowMenu(
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
        hWnd,
        evtList,
        ix = 0
    ):
        self.fore     = fore
        self.back     = back
        self.foreSel  = foreSel
        self.backSel  = backSel
        self.fontInfo = fontInfo
        self.flag     = flag
        self.plugin   = plugin
        self.monitor  = monitor
        self.hWnd     = hWnd
        self.evtList = evtList
        eg.TriggerEvent("OSD.%s" % self.plugin.text.opened, prefix="PotPlayer")
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
        for evt in self.evtList[5]:
            eg.Bind(evt, self.onPrint)
        self.menuHwnd, self.menu = self.plugin.GetPP_Menu(self.hWnd)
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
        font = wx.Font(fontInfo)
        self.menuGridCtrl.SetFont(font)
        arial = wx.Font(ARIAL_INFO)
        self.SetFont(font)            
        hght = self.GetTextExtent('X')[1]
        for n in range(1,1000):
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
        self.UpdateMenu(ix == 0, ix)
        self.plugin.menuDlg = self
        wx.Yield()
        SetEvent(event)


    def UpdateMenu(self, root = False, ix = 0):
        if root:
            self.menuHwnd, self.menu = self.plugin.GetPP_Menu(self.hWnd)
        else:
            self.menuHwnd, self.menu = self.GetSubMenuExt(self.hWnd, ix)
        self.items = self.plugin.GetItemList(self.menuHwnd, self.menu)
        if len(self.items)==0:
            PlaySound('SystemExclamation', SND_ASYNC)
            eg.PrintError("Please report: %s, %s, %s, %s" % (
                str(ix),
                str(root),
                str(self.menuHwnd),
                str(self.menu)
            ))
        self.choices = [item[0] for item in self.items]
        self.menuGridCtrl.Set(self.items)
        self.DrawMenu(ix)    


    def MoveCursor(self, step):
        max=len(self.choices)
        if max > 0:
            self.menuGridCtrl.MoveCursor(step)


    def onUp(self, event):
        wx.CallAfter(self.menuGridCtrl.MoveCursor, -1)
        return True #stop processing this event !!!


    def onDown(self, event):
        wx.CallAfter(self.menuGridCtrl.MoveCursor, 1)
        return True #stop processing this event !!!


    def onLeft(self, event):
        if len(self.oldMenu) > 0:
            ix, iy = self.oldMenu.pop()
            wx.CallAfter(self.UpdateMenu, False, ix)
        else:
            wx.CallAfter(self.destroyMenu)
        return True #stop processing this event !!!


    def onRight(self, event):
        wx.CallAfter(self.DefaultAction)
        return True #stop processing this event !!!


    def onEscape(self, event):
        wx.CallAfter(self.destroyMenu)
        return True #stop processing this event !!!


    def onPrint(self, event):
        sel = self.menuGridCtrl.GetSelection()
        item = self.items[sel]
        if item[3] > -1:
            eg.PrintNotice(self.plugin.text.printLbl % (item[0], item[3]))
        return True #stop processing this event !!!


    def GetSubMenuExt(self, hWnd, ix):  
        menu, hMenu = self.plugin.GetPP_Menu(hWnd)
        if menu:
            for item in self.oldMenu:
                hMenu = GetSubMenu(hMenu, item[1])
                SendMessage(hWnd, WM_INITMENUPOPUP, hMenu, item[1]) #It must be here!!!
            return (menu, hMenu)


    def DefaultAction(self):
        sel = self.menuGridCtrl.GetSelection()
        item = self.items[sel]
        id = item[3]
        iy = item[1]
        if id != -1:
            self.destroyMenu()
            SendMessage(self.hWnd, WM_COMMAND, id, 0)
        else:
            self.oldMenu.append((sel, iy))
            wx.CallAfter(self.UpdateMenu, False)


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
        for i in range(len(self.messStack)):
            mess = self.messStack.pop()
            SendMessageTimeout(self.hWnd, WM_COMMAND, mess, 0)
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
        for evt in self.evtList[5]:
            eg.Unbind(evt, self.onPrint)
        if self.flag:
            self.timer.Cancel()
        eg.TriggerEvent("OSD.%s" % self.plugin.text.closed, prefix="PotPlayer")
        self.Close()
#===============================================================================

class MyTimer():

    def __init__(self, t, plugin):
        self.timer = Timer(t, self.Run)
        self.plugin = plugin
        self.timer.start()


    def Run(self):
        try:
            self.plugin.menuDlg.destroyMenu()
            self.plugin.menuDlg = None
        except:
            pass


    def Cancel(self):
        self.timer.cancel()
#===============================================================================

class UserCommand(eg.ActionClass):

    description = u"""<rst>**Sends user's command.**

If you can not find in the menu of features some of the commands, you can (maybe) to add it yourself.
First, you must determine the ID of the desired command (see instructions below).
Type this number into the edit box "**User command ID:**".
You can of course also use an expression such as **{eg.result}** or **{eg.event.payload}**.

NOTE: *User command name* has only a descriptive purpose.

*How to find ID:*

1. Open PotPlayer *On screen menu* (using the action **Show PotPlayer menu**)
2. Move the cursor to the desired item
3. On the remote control, press the button that corresponds to the event **Print command ID**
"""


    class text:
        label_id = "User command ID:"
        label_fnc = "User command name:"
        error = "ValueError: invalid literal for int() with base 10: '%s'"


    def __call__(self, fnc="", val = ""):
        if self.plugin.ppHwnd:
            try:
                val = eg.ParseString(val)
                val = int(val)
            except:
                raise self.Exception(self.text.error % val)
                return
            return SendMessage(self.plugin.ppHwnd, WM_COMMAND, val, 0)
        else:
            raise self.Exceptions.ProgramNotRunning


    def Configure(self, fnc="", val = ""):
        panel = eg.ConfigPanel()
        fncLabel = wx.StaticText(panel, -1, self.text.label_fnc)
        fncControl = wx.TextCtrl(panel, -1, fnc, size = (200,-1))
        idLabel = wx.StaticText(panel, -1, self.text.label_id)
        idControl = wx.TextCtrl(panel, -1, val, size = (200,-1))
        sizer = wx.FlexGridSizer(cols = 2, vgap = 20, hgap = 10)
        sizer.Add(fncLabel, 0, wx.TOP, 3)
        sizer.Add(fncControl)
        sizer.Add(idLabel, 0, wx.TOP, 3)
        sizer.Add(idControl)
        panel.sizer.Add(sizer,1,wx.EXPAND|wx.ALL,10)
        while panel.Affirmed():
            panel.SetResult(
                fncControl.GetValue(),
                idControl.GetValue(),
            )
#===============================================================================

class SendMessage2PP(eg.ActionBase):
    
    def __call__(self):
        if self.plugin.ppHwnd:
            wx.CallAfter(SendMessage,self.plugin.ppHwnd,WM_COMMAND,self.value,0)
#===============================================================================

class GoTo_OSD(eg.ActionBase):

    panel = None

    class text:
        OSELabel = '"Go To..." show on:'
        menuPreview = '"Go To..." OSD preview:'
        txtColour = 'Text colour'
        background = 'Background colour'
        txtColourSel = 'Selected text colour'
        backgroundSel = 'Selected background colour'
        gotoLabel = 'Go To...'
        dialog = "Events ..."
        btnToolTip = '''Press this button to assign events to control the "Go To..." OSD !!!'''
        evtAssignTitle = '"Go To..." OSD control - events assignement'
        events = (
            "Digit increment:",
            "Digit decrement:",
            "Kursor left:",
            "Kursor right:",
            "Cancel (Escape):",
        )
        fontFace = "Select font face"
        fontSize = "Select font size"
        inverted = "Use inverted colours"

    def __call__(
        self,
        fore,
        back,
        faceFont,
        sizeFont,
        monitor,
        foreSel,
        backSel,
        evtList,
        sizeFlag,
        inverted
        ):

        if self.plugin.ppHwnd:
            if not self.plugin.menuDlg:
                self.plugin.menuDlg = GoToFrame()
                self.event = CreateEvent(None, 0, 0, None)
                wx.CallAfter(self.plugin.menuDlg.ShowGoToFrame,
                    fore,
                    back,
                    foreSel,
                    backSel,
                    faceFont,
                    sizeFont,
                    False,
                    self.plugin,
                    self.event,
                    monitor,
                    self.plugin.ppHwnd,
                    evtList,
                    sizeFlag
                )
                eg.actionThread.WaitOnEvent(self.event)
        else:
            eg.programCounter = None
            raise self.Exceptions.ProgramNotRunning

    def GetLabel(
        self,
        fore,
        back,
        faceFont,
        sizeFont,
        monitor,
        foreSel,
        backSel,
        evtList,
        sizeFlag,
        inverted
    ):
        return self.name


    def Configure(
        self,
        fore = (75, 75, 75),
        back = (180, 180, 180),
        faceFont = "Courier New",
        sizeFont = 40,
        monitor = 0,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75),
        evtList = [[],[],[],[],[]],
        sizeFlag = False,
        inverted = True
    ):
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
        displayChoice = eg.DisplayChoice(panel, monitor)
        w = displayChoice.GetSize()[0]
        OSElbl = wx.StaticText(panel, -1, self.text.OSELabel)
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
        dialogButton = wx.Button(panel,-1,self.text.dialog, size = (w, -1))
        dialogButton.SetToolTip(self.text.btnToolTip)
        foreSelLbl.Enable(not inverted)
        foreSelColourButton.Enable(not inverted)
        backSelLbl.Enable(not inverted)
        backSelColourButton.Enable(not inverted)
        #Use inverted colours checkbox
        useInvertedCtrl = wx.CheckBox(panel, -1, self.text.inverted)
        useInvertedCtrl.SetValue(inverted)
        #Sizers
        mainSizer = panel.sizer
        topSizer=wx.GridBagSizer(2, 30)
        mainSizer.Add(topSizer)
        topSizer.Add(previewLbl,(0, 0),flag = wx.TOP,border = 0)
        topSizer.Add((160,-1),(1, 0),(3, 1),flag = wx.EXPAND)    
        topSizer.Add(foreLbl,(0, 1),flag = wx.TOP,border = 0)
        topSizer.Add(foreColourButton,(1, 1),flag = wx.TOP)
        topSizer.Add(backLbl,(2, 1),flag = wx.TOP,border = 8)
        topSizer.Add(backColourButton,(3, 1),flag = wx.TOP)        
        topSizer.Add(foreSelLbl,(4, 1), (1, 2), flag = wx.TOP,border = 8)
        topSizer.Add(foreSelColourButton, (5, 1), flag = wx.TOP)
        topSizer.Add(backSelLbl,(6, 1), (1, 2), flag = wx.TOP,border = 8)
        topSizer.Add(backSelColourButton, (7, 1), flag = wx.TOP)
        topSizer.Add(useInvertedCtrl, (8, 1))
        topSizer.Add(OSElbl,(0, 2), flag = wx.TOP)
        topSizer.Add(displayChoice,(1, 2),flag = wx.TOP)        
        topSizer.Add(dialogButton, (3, 2), flag = wx.TOP)
        #Font face
        fw = FixedWidth()
        fw.EnumerateFacenames(wx.FONTENCODING_SYSTEM,  fixedWidthOnly = True)
        fw.fontList.sort()
        fontFaceLbl=wx.StaticText(panel, -1, self.text.fontFace+':')
        topSizer.Add(fontFaceLbl,(4, 0),(1, 1), flag = wx.TOP,border = 8)
        fontFaceCtrl = wx.Choice(panel,-1,choices=fw.fontList, size = (160,-1))
        fontFaceCtrl.SetStringSelection(faceFont)
        topSizer.Add(fontFaceCtrl,(5, 0),(1, 1), flag = wx.TOP)
        #Font size
        fontSizeLbl=wx.StaticText(panel, -1, self.text.fontSize+':')
        topSizer.Add(fontSizeLbl,(6, 0),(1, 1), flag = wx.TOP,border = 8)

        def LevelCallback(value):
            if value != sizeFont:
                panel.SetIsDirty()
            return str(value)

        fontSizeCtrl = eg.Slider(
            panel, 
            value = sizeFont, 
            min=20, 
            max=120, 
            style = wx.SL_TOP,
            size=(160,-1),
            levelCallback=LevelCallback
        )
        fontSizeCtrl.SetMinSize((160, -1))
        topSizer.Add(fontSizeCtrl,(7, 0),(1, 1), flag = wx.TOP)
        panel.sizer.Layout()
        spacer = topSizer.GetChildren()[1]
        ps = spacer.GetPosition()
        sz = spacer.GetSize()
        previewPanel = wx.Panel(
            panel,
            -1,
            pos = (ps[0], ps[1]+2),
            size = sz,
            style = wx.BORDER_SIMPLE
        )
        gotoLbl=wx.StaticText(previewPanel, -1, self.text.gotoLabel, pos=(5,5))
        gotoLbl.SetBackgroundColour(self.back)
        gotoLbl.SetForegroundColour(self.fore)
        gt = gotoLbl.GetTextExtent(self.text.gotoLabel)
        fnt = gotoLbl.GetFont()
        fnt.SetPointSize(12)
        fnt.SetWeight(wx.FONTWEIGHT_BOLD)
        gotoLbl.SetFont(fnt)
        GoToCtrl = wx.TextCtrl(
            previewPanel,
            -1,
            style=wx.TE_RICH2|wx.NO_BORDER|wx.TE_READONLY|wx.TE_CENTER,
        )
        GoToCtrl.SetValue("01:25:30")
        fnt.SetPointSize(20)
        GoToCtrl.SetFont(fnt)
        previewPanel.SetBackgroundColour(self.back)
        GoToCtrl.SetBackgroundColour(self.back)

        def OnFontFaceChoice(event = None):
            fnt.SetFaceName(fontFaceCtrl.GetStringSelection())
            GoToCtrl.SetFont(fnt)
            if GoToCtrl.GetTextExtent("01:25:30")[0] < 120:
                self.sizeFlag = True
            else:
                self.sizeFlag = False
            te = GoToCtrl.GetTextExtent("01:25:30")
            GoToCtrl.SetSize((158, te[1]))
            GoToCtrl.SetPosition((1, 5+gt[1]+(sz[1]-gt[1]-te[1])/2))
            pos = 3
            GoToCtrl.SetStyle(0, pos, wx.TextAttr(self.fore, self.back, fnt))
            GoToCtrl.SetStyle(
                pos,
                pos+1,
                wx.TextAttr(self.foreSel, self.backSel, fnt)
            )
            GoToCtrl.SetStyle(pos+1, 8, wx.TextAttr(self.fore, self.back, fnt))
            if event:
                event.Skip()
        fontFaceCtrl.Bind(wx.EVT_CHOICE, OnFontFaceChoice)
        OnFontFaceChoice()


        def OnInverted(evt):
            flag = evt.IsChecked()
            foreSelLbl.Enable(not flag)
            foreSelColourButton.Enable(not flag)
            backSelLbl.Enable(not flag)
            backSelColourButton.Enable(not flag)
            self.inverted = flag
            if flag:
                backSelColourButton.SetValue(foreColourButton.GetValue())
                foreSelColourButton.SetValue(backColourButton.GetValue())
                self.backSel = self.fore
                self.foreSel = self.back
                previewPanel.Refresh()
                OnFontFaceChoice()
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


        def OnColourBtn(evt):
            id = evt.GetId()
            value = evt.GetValue()
            if id == foreColourButton.GetId():
                self.fore = value
                gotoLbl.SetForegroundColour(value)
                if self.inverted:
                    self.backSel = value
                    backSelColourButton.SetValue(value)
            elif id == backColourButton.GetId():
                self.back = value
                GoToCtrl.SetBackgroundColour(value)
                previewPanel.SetBackgroundColour(value)
                gotoLbl.SetBackgroundColour(value)
                if self.inverted:
                    self.foreSel = value
                    foreSelColourButton.SetValue(value)
            elif id == foreSelColourButton.GetId():
                self.foreSel = value
            elif id == backSelColourButton.GetId():
                self.backSel = value
            previewPanel.Refresh()
            OnFontFaceChoice()
            evt.Skip()
        foreColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)
        backColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)
        foreSelColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)
        backSelColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)

        def setFocus():
            pass
        panel.setFocus = setFocus

        # re-assign the test button
        def OnButton(event):
            if self.plugin.ppHwnd:
                if not self.plugin.menuDlg:
                    self.plugin.menuDlg = GoToFrame()
                    self.event = CreateEvent(None, 0, 0, None)
                    wx.CallAfter(self.plugin.menuDlg.ShowGoToFrame,
                        foreColourButton.GetValue(),
                        backColourButton.GetValue(),
                        foreSelColourButton.GetValue(),
                        backSelColourButton.GetValue(),
                        fontFaceCtrl.GetStringSelection(),
                        fontSizeCtrl.GetValue(),
                        True,
                        self.plugin,
                        self.event,
                        displayChoice.GetSelection(),
                        self.plugin.ppHwnd,
                        panel.evtList,
                        self.sizeFlag
                    )
                    eg.actionThread.WaitOnEvent(self.event)
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnButton)

        while panel.Affirmed():
            panel.SetResult(
            foreColourButton.GetValue(),
            backColourButton.GetValue(),
            fontFaceCtrl.GetStringSelection(),
            fontSizeCtrl.GetValue(),
            displayChoice.GetSelection(),
            foreSelColourButton.GetValue(),
            backSelColourButton.GetValue(),
            panel.evtList,
            self.sizeFlag,
            useInvertedCtrl.GetValue()
        )
#===============================================================================

class ShowMenu(eg.ActionClass):

    panel = None

    class text:
        OSELabel = 'Menu show on:'
        menuPreview = 'PotPlayer On Screen Menu preview:'
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
            "Print command ID:",
        )
        inverted = "Use inverted colours"


    def __call__(
        self,
        fore,
        back,
        fontInfo = arialInfoString,
        monitor = 0,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75),
        evtList = [],
        inverted = True
    ):
        if self.plugin.ppHwnd:
            if not self.plugin.menuDlg:
                self.plugin.menuDlg = Menu()
                self.event = CreateEvent(None, 0, 0, None)
                wx.CallAfter(self.plugin.menuDlg.ShowMenu,
                    fore,
                    back,
                    foreSel,
                    backSel,
                    fontInfo,
                    False,
                    self.plugin,
                    self.event,
                    monitor,
                    self.plugin.ppHwnd,
                    evtList,
                )
                eg.actionThread.WaitOnEvent(self.event)
        else:
            eg.programCounter = None
            raise self.Exceptions.ProgramNotRunning


    def GetLabel(
        self,
        fore,
        back,
        fontInfo,
        monitor,
        foreSel,
        backSel,
        evtList,
        inverted
    ):
        return self.name


    def Configure(
        self,
        fore = (75, 75, 75),
        back = (180, 180, 180),
        fontInfo = arialInfoString,
        monitor = 0,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75),
        evtList = [[],[],[],[],[],[]],
        inverted = True
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
        items = (("Blabla_1",0,True,804),
                 ("Blabla_2",1,False,804),
                 ("Blabla_3",2,False,-1),)
        listBoxCtrl.Set(items)
        listBoxCtrl.SetBackgroundColour(self.back)
        listBoxCtrl.SetForegroundColour(self.fore)
        listBoxCtrl.SetSelectionBackground(self.backSel)
        listBoxCtrl.SetSelectionForeground(self.foreSel)
        #Font button
        fontLbl=wx.StaticText(panel, -1, self.text.menuFont)
        fontButton = eg.FontSelectButton(panel, value = fontInfo)
        font = wx.Font(fontInfo)
        for n in range(10,20):
            font.SetPointSize(n)
            fontButton.SetFont(font)
            hght = fontButton.GetTextExtent('X')[1]
            if hght > 20:
                break
        listBoxCtrl.SetDefaultCellFont(font)
        arial = wx.Font(arialInfoString)
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
        dialogButton.SetToolTip(self.text.btnToolTip)
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
        if (hght+4)*listBoxCtrl.GetNumberRows() > listBoxCtrl.GetSize()[1]:     #after Layout() !!!
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
            font = wx.Font(value)
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
            if self.plugin.ppHwnd:
                if not self.plugin.menuDlg:
                    self.plugin.menuDlg = Menu()
                    self.event = CreateEvent(None, 0, 0, None)
                    wx.CallAfter(self.plugin.menuDlg.ShowMenu,
                        foreColourButton.GetValue(),
                        backColourButton.GetValue(),
                        foreSelColourButton.GetValue(),
                        backSelColourButton.GetValue(),
                        self.fontInfo, 
                        True,
                        self.plugin,
                        self.event,
                        displayChoice.GetSelection(),
                        self.plugin.ppHwnd,
                        panel.evtList
                    )
                    eg.actionThread.WaitOnEvent(self.event)
            else:
                self.PrintError(eg.Classes.Exceptions.Text.ProgramNotRunning)
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
            useInvertedCtrl.GetValue()
        )
#===============================================================================

class Run(eg.ActionBase):

    def __call__(self):
        self.plugin.Run()     
#===============================================================================

class GetNowPlaying(eg.ActionBase):
    
    def __call__(self):
        if self.plugin.ppHwnd:
            title = GetWindowText(self.plugin.ppHwnd)
            tmp = title.split(" - ")[:-1]
            return " - ".join(tmp)
#===============================================================================

class AddFile(eg.ActionBase):

    class text:
        toolTipFile = 'Type filename or click browse to choose file'
        browseFile = 'Choose a file'
        err = 'File "%s" not found !'

    def __call__(self, filepath = ""):
        filepath = eg.ParseString(filepath)
        if isfile(filepath) or isdir(filepath):
            wx.CallAfter(self.plugin.AddFile, filepath, self.value)
        else:
            eg.PrintError(self.text.err % filepath)


    def Configure(self, filepath = ""):
        panel = eg.ConfigPanel()    
        folder = split(filepath)[0] if filepath else eg.folderPath.Videos
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

class PotPlayer(eg.PluginBase):

    mySched = None
    menuDlg = None
    state = None
    ppHwnd = None
    event = None
    result = None

    class text:
        popup = (
            "Delete item",
            "Delete all items",
        )
        cancel = 'Cancel'
        ok = 'OK'
        clear  = "Clear all"
        toolTip = "Drag-and-drop an event from the log into the box."
        opened = "Opened"
        closed = "Closed"
        label = "Path to PotPlayer executable:"
        fileMask = "PotPlayer executable|PotPlayerMini*.exe|All-Files (*.*)|*.*"
        goto = "Go To..."
        printLbl = 'Label, ID = "%s", %i'





    def Find_PP(self):
        hwndpp = eg.WindowMatcher(
            split(self.ppPath)[1],
            None,
            u'PotPlayer64' if split(self.ppPath)[1] == "PotPlayerMini64.exe" else u'PotPlayer',
            None,
            None,
            None,
            True,
            0.0,
            2
        )
        return hwndpp()


    def GetPP_Menu(self, hwnd):

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
                    split(self.ppPath)[1],
                    None,
                    u'#32768',
                    None,
                    None,
                    None,
                    True,
                    0.0,
                    0
                )
        PostMessage(hwnd, WM_CONTEXTMENU, hwnd, 0x00010001)
        menu = []
        i = 0
        while len(menu) == 0:
            menu = findMenu()
            i+=1
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


    @eg.LogIt
    def GetItemList(self, hWnd, hMenu):
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

            #import win32gui_struct
            #from win32gui import GetMenuItemInfo
            #item, extra = win32gui_struct.EmptyMENUITEMINFO()
            #GetMenuItemInfo(hMenu, i, True, item)
            #MenuItemInfo = win32gui_struct.UnpackMENUITEMINFO(item)
            #print "MenuItemInfo, extra =",MenuItemInfo, repr(extra)

    #        if hMenuState & (MF_GRAYED|MF_DISABLED|MF_SEPARATOR):
            if hMenuState & (MF_GRAYED|MF_DISABLED):
                continue
            item = itemName.decode(eg.systemEncoding).value.replace("&","").split("\t")[0]
            if item == "": #bookmark with thumbnail (PotPlayer specific)
                continue
            elif r"%s" in item:
                if id in MENUsubst:
                    item = item % MENUsubst[id]
                #else:
                #    print "%i missing in MENUsubst !" % id
            checked = bool(hMenuState & MF_CHECKED)
            itemList.append((item, i, checked, id))
        PostMessage(hWnd, WM_CLOSE, 0, 0)
        return itemList


    def Run(self):
        hWnd = self.Find_PP()
        if not hWnd:
            pp = self.ppPath
            pp = pp.encode(FSE) if isinstance(pp, unicode) else pp
            if isfile(pp):
                args = [pp]
                Popen(args) 


    def AddFile(self, filepath, flag):
        if not self.ppHwnd:
            sl = 2.0
            self.Run()
            for i in range(100):
                hWnd = self.Find_PP()
                try:
                    SendMessageTimeout(hWnd[0], 0, timeout = 1000) # 0 = WM_NULL
                    break
                except:
                    pass
                sleep(1.0)
            if i > 9:
                return #Print error message ???
            sleep(sl)
        else:
            sl = 0.5
        if flag:
            SendMessage(self.ppHwnd, WM_COMMAND, 10201, 0)#Clear playlist
            SendMessage(self.ppHwnd, WM_COMMAND, 10167, 0)#Close file
        pp = self.ppPath
        pp = pp.encode(FSE) if isinstance(pp, unicode) else pp
        fp = filepath.encode(FSE) if isinstance(filepath, unicode) else filepath
        if isfile(pp):
            args = [pp]
            args.append('"%s"' % fp)
            args.append('/add')
            Popen(args)
            if flag:
                sleep(sl)
                wx.CallAfter(SendMessage,self.ppHwnd, WM_COMMAND, 10067, 0)#Play/Pause



    def isRunning(self):
        try:
            return FindWindow(u'PotPlayer64' if split(self.ppPath)[1] == "PotPlayerMini64.exe" else u'PotPlayer', None)
        except:
            return False


    def ppIsRunning(self):
        self.mySched=eg.scheduler.AddTask(2, self.ppIsRunning) # must run continuously !
        if not self.isRunning(): #user closed pp ?
            if self.ppHwnd:
                    self.ppHwnd = None
                    self.TriggerEvent(self.text.closed)
        elif self.ppHwnd:
            pass
        else:
            hWnd = self.Find_PP()
            if hWnd:
                self.ppHwnd = hWnd[0]
                self.TriggerEvent(self.text.opened)


    def __init__(self):
        self.AddActionsFromList(ACTIONS, SendMessage2PP)


    def __start__(self, ppPath=None):
        self.mySched=None
        self.menuDlg = None
        self.state = None
        self.ppHwnd = None
        self.event = None
        self.result = None
        if ppPath is None:
            ppPath = self.GetPPpath()
        if not ppPath or not exists(ppPath):
            raise self.Exceptions.ProgramNotFound
            return
        self.ppPath = ppPath
        hWnd = self.Find_PP()
        if hWnd:
            self.ppHwnd = hWnd[0]
        eg.scheduler.AddTask(1, self.ppIsRunning)
    

    def __stop__(self):
        if self.mySched:
            try:
                eg.scheduler.CancelTask(self.mySched)
            except:
                pass
       

    def Configure(self, ppPath=None):
        if ppPath is None:
            ppPath = self.GetPPpath()
            if ppPath is None:
                ppPath = join(
                    eg.folderPath.ProgramFiles, 
                    "PotPlayer", 
                    "PotPlayerMini.exe"
                )
        panel = eg.ConfigPanel()
        filepathCtrl = eg.FileBrowseButton(
            panel, 
            size=(320,-1),
            initialValue=ppPath, 
            startDirectory=eg.folderPath.ProgramFiles,
            labelText="",
            fileMask = self.text.fileMask,
            buttonText=eg.text.General.browse,
        )
        panel.AddLabel(self.text.label)
        panel.AddCtrl(filepathCtrl)
        while panel.Affirmed():
            panel.SetResult(filepathCtrl.GetValue())


    def GetPPpath(self):
        """
        Get the path of PotPlayer's installation directory through querying 
        the Windows registry.
        """
        try:
            if "PROCESSOR_ARCHITEW6432" in environ:
                args = [_winreg.HKEY_CURRENT_USER,            
                    "Software\DAUM\PotPlayerMini64"]
                args.extend((0, _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY))
            else:
                args = [_winreg.HKEY_CURRENT_USER,            
                    "Software\Daum\PotPlayer"]
            pp = _winreg.OpenKey(*args)
            ppPath =_winreg.QueryValueEx(pp, "ProgramPath")[0]
            _winreg.CloseKey(pp)
        except WindowsError:
            ppPath = None
        return ppPath
#===============================================================================

ACTIONS = (
(eg.ActionGroup, 'GroupMainControls', 'Main controls', None, (
    (Run, "Run", "Run PotPlayer", "Run PotPlayer with its default settings." ,None),
    ('Exit', 'Quit PotPlayer', None, 57665),
    ('PlayPause', 'Play/Pause', None, 10014),
    ('Stop', 'Stop', None, 20002),
    ('VolumeUp', 'Volume Up', None, 10035),
    ('VolumeDown', 'Volume Down', None, 10036),
    ('VolumeMute', 'Volume Mute', None, 10037),
    ('Next', 'Next', None, 10068),
    ('Previous', 'Previous', None, 10067),
    (AddFile, "AddFile", "Add file/folder to playlist", "Adds file or folder to playlist.", 0),
    (AddFile, "PlayFile", "Play file/folder", "Immediately plays selected file/folder.", 1),
)),
(eg.ActionGroup, 'JumpTo', 'Jump (to)', None, (
    ('JumpForward5s', 'Jump Forward 5s', None, 10060),
    ('JumpBackward5s', 'Jump Backward 5s', None, 10059),
    ('JumpForward30s', 'Jump Forward 30s', None, 10062),
    ('JumpBackward30s', 'Jump Backward 30s', None, 10061),
    ('JumpForward1min', 'Jump Forward 1 min', None, 10064),
    ('JumpBackward1min', 'Jump Backward 1 min', None, 10063),
    ('JumpForward5min', 'Jump Forward 5 min', None, 10066),
    ('JumpBackward5min', 'Jump Backward 5 min', None, 10065),
    ('SpeedNormal', 'Speed normal', None, 10246),
    ('SpeedDown', 'Speed down -', None, 10247),
    ('SpeedUp', 'Speed up +', None, 10248),
    ('PreviousFrame', 'Previous Frame', None, 10242),
    ('NextFrame', 'Next frame', None, 10241),
    ('PreviousKeyframe', 'Previous keyframe', None, 10786),
    ('NextKeyframe', 'Next keyframe', None, 10787),
    ('StartingPoint', 'Starting point', None, 10243),
    ('Middle', 'Middle', None, 10619),
    ('Sec30beforeEnding', '30 sec. before ending', None, 10620),
    ('PreviousSubtitle', 'Previous subtitle', None, 10244),
    ('NextSubtitle', 'Next subtitle', None, 10245),
    ('CurrentSubtitle', 'Current subtitle position', None, 10582),
    ('Time_Frame', 'Time/Frame', None, 10325),
    ('PreviewScenes', 'Preview scenes', None, 10416),
    ('TimeJumpSettings', 'Time jump settings', None, 10758),
)),
(eg.ActionGroup, 'GroupViewModes', 'View modes', None, (
    ('X0_5','0.5 X','0.5 X.', 10232),
    ('X1_0','1.0 X','1.0 X.', 10233),
    ('X1_5','1.5 X','1.5 X.', 10234),
    ('X2_0','2.0 X','2.0 X.', 10235),
    ('Custom','Custom','Custom.', 10664),
    ('Minimize','Minimize','Minimize.', 10230),
    ('Mini_size','Mini-size','Mini-size.', 10231),
    ('Maximize','Maximize','Maximize.', 10236),
    ('Maximize_Restore','Maximize/Restore','Maximize/Restore.', 10237),
    ('MaximizeP_Restore','Maximize +/Restore','Maximize +/Restore.', 10238),
    ('Fullscreen', 'Fullscreen', None, 10013),
    ('FullscreenStretched', 'Fullscreen stretched', None, 10308),
    ('Full Size','Full Size','Full Size.', 10309),
)),
(eg.ActionGroup, 'GroupExtendedControls', 'Extended controls', None, (
    (ShowMenu,'ShowMenu','Show PotPlayer menu','Shows PotPlayer Menu.', None),
    (GoTo_OSD,'GoTo_OSD','On Screen Go To ...','Shows On Screen "Go To ...".', None),
    ('ShowOSDTime','OSD: Show Time','Shows OSD Time.', 10442),
    ('ShowOSDShortInfo','OSD: Show Short Info','Shows OSD Short Info.', 10449),
    (GetNowPlaying,'GetNowPlaying','Get currently playing file','Gets currently playing file.', None),
    (UserCommand,'UserCommand',"User command",UserCommand.description, None),
)),
(eg.ActionGroup, 'ToggleModes', 'Toggle/Switch modes/streams ...', None, (
    ('SwitchOnTop','Switch on top','Switch on top.', 10337),
    ('SwitchRepeat','Switch repeat','Switch repeat.', 10034),
    ('SwitchShuffle','Switch shuffle play','Switch shuffle play.', 10069),
    ('ShowSubtitles','Show subtitles (On/Off)','Show subtitles (On/Off).', 10126),
    ('SwitchSubtitles','Switch subtitles','Switch subtitles.', 6899),
    ('SwitchAudioStream','Switch audio stream','Switch audio stream.', 6799),
    ('SwapChannels','Swap stereo channels','Swaps stereo channels.', 10660),
    ('Enable3DVideoMode','Enable 3D Video Mode (On/Off)','Enables 3D Video Mode (On/Off).', 10683),
    ('JumpToKeyframeOnOff', 'Jump to keyframe (On/Off)', None, 10265),
    ('EnableSkipFeature', 'Enable skip feature', None, 10239),
    ('PlayFromTheLatestPoint', 'Play from the latest point', None, 10419),
)),
)
#===============================================================================
