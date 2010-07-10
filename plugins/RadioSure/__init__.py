version="0.1.5"

# Plugins/RadioSure/__init__.py
#
# Copyright (C)  2009 Pako  (lubos.ruckl@quick.cz)
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
#
# changelog:
# 0.1.5 by Pako 2010-07-10 08:21 GMT+1
#     - added Scheduler
#     - added guid attribute
# 0.1.4 by Pako 2010-03-23 11:20 GMT+1
#     - added action Random favorite
# 0.1.3 by Pako 2010-03-22 09:09 GMT+1
#     - added actions Start and Stop observation of titlebar
#===============================================================================

eg.RegisterPlugin(
    name = "RadioSure",
    author = "Pako",
    version = version,
    kind = "program",
    guid = "{1A68AA88-3C92-4B98-92A0-CB627B27D422}",
    description = ur'''<rst>
Adds actions to control the `Radio?Sure!`_

.. _Radio?Sure!: http://www.radiosure.com/ ''',
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=2359",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEUA//+Gh4ju7/Ds"
        "7e7q6+zo6evm5+nk5efi4+Xg4ePd3+Db3N7Z2tzW2Nrr7e5+g4bo6erm5+js7e3a3N7Y"
        "2dt3fYDT1dfp6uzn6Orl5uhIS03V1tjS1NbQ0tTn6Onl5ufi5OXS09XP0dPNz9HR09XP"
        "0NPMztDKzM7h4+Tf4OLd3uCVmp1OUlQZGhoYGRlLTlCHjZDMzdDJy87Hycve4OHc3t+d"
        "oqQyNDU3OjtSVlgpKywqLC2IjpHHyMvExsnc3d/Z29xWWlyBh4p2fH9pbnFfZGYsLi9L"
        "T1HExsjCxMYbHB2XnJ5MUFJKTU9yeHtVWVvBw8a/wcTW19kcHR6UmZypra9RVVeGjI9l"
        "am0aGxu/wcO9v8JcYWNeY2W5vL6xtLamqqyboKK9vsG7vcA9QEG6vL+5u76LkJPIycyy"
        "tbddYmRYXV+jqKqDiYy3ubzFx8nDxcfBw8W4ur22uLsAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADQcfgAAAAAAAXQciD0AAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAABAAgAAAAAAAAAAAAAAAAAAAAAAAAAAABGa1gAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAEAAAAAAAAAAAAPAAAAAAEAAAEAAADQckT/C08AAAAAAAAAAAAAAAMAAADf"
        "BnAAAAAAAAAAAAAAAAAAAAQAAQEAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACnZAh6AAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAKdJREFUeNpjYGBgRAVoAl9A"
        "ArwQCbDMayYgg5OTk5GBg4PhPzs7OwNIAESDARsbGwNICxtQKQeQLwSkb4EE1JEMPQfS"
        "wgMGjNwgANZix8h4UwOqYgdIxdmznGKcIPAMaBVIReARW6DcNW2QimUgAWlGe7DynTY8"
        "jPOYwNYzs/+//vqB3ANmZrAWVUeg9EsGCcafHIyTQQKGjDZAAUYOJt4/rH0M6N4HAFCJ"
        "GrcTFgV2AAAAAElFTkSuQmCC"
    ),
)
#===============================================================================

import os
import wx.grid as gridlib
import wx.lib.masked as maskedlib
import subprocess
from calendar import day_name, month_name, monthrange
from _winreg import OpenKey, HKEY_CURRENT_USER, EnumValue, CloseKey
from datetime import datetime as dt
from datetime import timedelta as td
from copy import deepcopy as cpy
from xml.dom import minidom as miniDom
from threading import Timer, Thread, Event
from eg.WinApi.Utils import GetMonitorDimensions
from eg.WinApi.Dynamic import CreateEvent, SetEvent
from time import sleep, mktime, strptime, strftime
from win32gui import GetWindowText, MessageBox, GetWindow, GetDlgCtrlID, GetDlgItem, GetClassName
from eg.WinApi.Dynamic import SendMessage
from random import randrange
from codecs import lookup
from codecs import open as openFile
from winsound import PlaySound, SND_ASYNC
from sys import getfilesystemencoding
fse = getfilesystemencoding()

WM_COMMAND    = 273
WM_SYSCOMMAND = 274
TBM_GETPOS    = 1024
TBM_SETPOS    = 1029
SC_RESTORE    = 61728
GW_CHILD      = 5
GW_HWNDNEXT   = 2
SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
#===============================================================================

class Text:
    label1 = "Radio?Sure! installation folder:"
    label2 = "RadioSure.xml and Scheduler.xml folder location:"
    filemask = "RadioSure.exe|RadioSure.exe|All-Files (*.*)|*.*"
    text1 = "Couldn't find RadioSure window !"
    browseTitle = "Selected folder:"
    toolTipFolder = "Press button and browse to select folder ..."
    boxTitle = 'Folder "%s" is incorrect'
    toolTipFile = "Press button and browse to select logfile ..."
    browseFile = 'Select the logfile'
    boxMessage1 = 'Missing file %s !'
    logLabel = "Log scheduler events to following logfile:"
    nextRun = "Next run: %s"
    none = "None"
    execut = 'Schedule "%s" - execution. Next run: %s'
    cancAndDel = 'Schedule "%s" canceled and deleted'
    cancAndDis = 'Schedule "%s" canceled (disabled)'
    newSched = 'Schedule "%s" scheduled. Next run: %s'
    re_Sched = 'Schedule "%s" re-scheduled. New next run: %s'
    start = 'RadioSure plugin started. All valid schedules will be scheduled:'
    stop = 'RadioSure plugin stoped. All scheduled schedules will be canceled:'
    canc = 'Schedule "%s" canceled'
    launched = "Schedule.Launched"
#===============================================================================

class MyDirBrowseButton(eg.DirBrowseButton):
    def GetTextCtrl(self):          #  now I can make build-in textCtrl
        return self.textControl     #  non-editable !!!
#===============================================================================

class MyFileBrowseButton(eg.FileBrowseButton):
    def GetTextCtrl(self):          #  now I can make build-in textCtrl
        return self.textControl     #  non-editable !!!
#===============================================================================

newEVT_BUTTON_AFTER = wx.NewEventType()
EVT_BUTTON_AFTER = wx.PyEventBinder(newEVT_BUTTON_AFTER, 1)

class EventAfter(wx.PyCommandEvent):

    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self.myVal = None


    def SetValue(self, val):
        self.myVal = val


    def GetValue(self):
        return self.myVal
#===============================================================================

class extColourSelectButton(eg.ColourSelectButton):

    def __init__(self,*args,**kwargs):
        eg.ColourSelectButton.__init__(self, *args)
        self.title = kwargs['title']


    def OnButton(self, event):
        colourData = wx.ColourData()
        colourData.SetChooseFull(True)
        colourData.SetColour(self.value)
        for i, colour in enumerate(eg.config.colourPickerCustomColours):
            colourData.SetCustomColour(i, colour)
        dialog = wx.ColourDialog(self.GetParent(), colourData)
        dialog.SetTitle(self.title)
        if dialog.ShowModal() == wx.ID_OK:
            colourData = dialog.GetColourData()
            self.SetValue(colourData.GetColour().Get())
            event.Skip()
        eg.config.colourPickerCustomColours = [
            colourData.GetCustomColour(i).Get() for i in range(16)
        ]
        dialog.Destroy()
        evt = EventAfter(newEVT_BUTTON_AFTER, self.GetId())
        evt.SetValue(self.GetValue())
        self.GetEventHandler().ProcessEvent(evt)
#===============================================================================

class extFontSelectButton(eg.FontSelectButton):

    def OnButton(self, event):
        fontData = wx.FontData()
        if self.value is not None:
            font = wx.FontFromNativeInfoString(self.value)
            fontData.SetInitialFont(font)
        else:
            fontData.SetInitialFont(
                wx.SystemSettings_GetFont(wx.SYS_ANSI_VAR_FONT)
            )
        dialog = wx.FontDialog(self.GetParent(), fontData)
        if dialog.ShowModal() == wx.ID_OK:
            fontData = dialog.GetFontData()
            font = fontData.GetChosenFont()
            self.value = font.GetNativeFontInfo().ToString()
            event.Skip()
        dialog.Destroy()
        evt = EventAfter(newEVT_BUTTON_AFTER, self.GetId())
        evt.SetValue(self.GetValue())
        self.GetEventHandler().ProcessEvent(evt)
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
        attr = gridlib.GridCellAttr()
        attr.SetAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
        self.SetColAttr(0,attr)
        self.CreateGrid(lngth, 1)
        self.SetSelectionMode(gridlib.Grid.wxGridSelectRows)
        self.Bind(gridlib.EVT_GRID_CMD_SELECT_CELL, self.onGridSelectCell, self)


    def SetBackgroundColour(self, colour):
        self.SetDefaultCellBackgroundColour(colour)


    def SetForegroundColour(self, colour):
        self.SetDefaultCellTextColour(colour)


    def SetFont(self, font):
        self.SetDefaultCellFont(font)


    def Set(self, choices):
        oldLen = self.GetNumberRows()
        newLen = len(choices)
        h = self.GetDefaultRowSize()
        if oldLen > newLen:
            self.DeleteRows(0, oldLen-newLen, False)
        elif oldLen < newLen:
            self.AppendRows(newLen-oldLen, False)
        for i in range(len(choices)):
            self.SetCellValue(i,0,choices[i])
            self.SetRowSize(i,h)


    def onGridSelectCell(self, event):
        row = event.GetRow()
        self.SelectRow(row)
        if not self.IsVisible(row,0):
            self.MakeCellVisible(row,0)
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

class Menu(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(
            self,
            None,
            -1,
            'RadioSure OS Menu',
            style = wx.STAY_ON_TOP|wx.SIMPLE_BORDER
        )


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
        List
    ):
        self.monitor = monitor
        self.fore    = fore
        self.back    = back
        self.foreSel    = foreSel
        self.backSel    = backSel
        self.plugin  = plugin
        self.plugin.RefreshVariables()
        self.plugin.List = List
        self.choices = self.plugin.Favorites if List else self.plugin.History
        if len(self.choices) == 0:
            return
        self.stationChoiceCtrl = MenuGrid(self, len(self.choices))
        if fontInfo is None:
            font = self.stationChoiceCtrl.GetFont()
            font.SetPointSize(36)
            fontInfo = font.GetNativeFontInfoDesc()
        else:
            font = wx.FontFromNativeInfoString(fontInfo)
        self.stationChoiceCtrl.SetFont(font)
        self.SetFont(font)
        monDim = GetMonitorDimensions()
        try:
            x,y,ws,hs = monDim[self.monitor]
        except IndexError:
            x,y,ws,hs = monDim[0]
        # menu height calculation:
        h=self.GetCharHeight()+4
        for i in range(len(self.choices)):
            self.stationChoiceCtrl.SetCellValue(i,0,self.choices[i][1])
            self.stationChoiceCtrl.SetRowSize(i,h)
        height0 = len(self.choices)*h
        height1 = h*((hs-20)/h)
        height = min(height0, height1)+6
        # menu width calculation:
        width_lst=[]
        for item in self.choices:
            width_lst.append(self.GetTextExtent(item[1]+' ')[0])
        width = max(width_lst)+8
        self.stationChoiceCtrl.SetColSize(0,width)
        if height1 < height0:
            width += SYS_VSCROLL_X
        width = min((width,ws-50))+6
        x_pos = x+(ws-width)/2
        y_pos = y + (hs-height)/2
        self.SetDimensions(x_pos,y_pos,width,height)
        self.stationChoiceCtrl.SetDimensions(2,2,width-6,height-6,wx.SIZE_AUTO)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        ix = self.plugin.FavIx if List else self.plugin.HistIx
        self.stationChoiceCtrl.SetGridCursor(ix, 0)
        self.stationChoiceCtrl.SelectRow(ix)
        self.SetBackgroundColour((0,0,0))
        self.stationChoiceCtrl.SetBackgroundColour(self.back)
        self.stationChoiceCtrl.SetForegroundColour(self.fore)
        self.stationChoiceCtrl.SetSelectionBackground(self.backSel)
        self.stationChoiceCtrl.SetSelectionForeground(self.foreSel)
        mainSizer.Add(self.stationChoiceCtrl, 0, wx.EXPAND)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(gridlib.EVT_GRID_CMD_CELL_LEFT_DCLICK, self.onDoubleClick, self.stationChoiceCtrl)
        self.Bind(wx.EVT_CHAR_HOOK, self.onFrameCharHook)
        if flag:
            self.timer = MyTimer(t = 5.0, plugin = self.plugin)
        self.Show(True)
        self.Raise()
        wx.Yield()
        SetEvent(event)


    def DefaultAction(self):
        sel=self.stationChoiceCtrl.GetSelectedRows()[0]
        self.plugin.PlayFromMenu()


    def onFrameCharHook(self, event):
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_RETURN or keyCode == wx.WXK_NUMPAD_ENTER:
            self.DefaultAction()
        elif keyCode == wx.WXK_ESCAPE:
            self.Close()
        elif keyCode == wx.WXK_UP or keyCode == wx.WXK_NUMPAD_UP:
            self.stationChoiceCtrl.MoveCursor(-1)
        elif keyCode == wx.WXK_DOWN or keyCode == wx.WXK_NUMPAD_DOWN:
            self.stationChoiceCtrl.MoveCursor(1)
        else:
            event.Skip()


    def onDoubleClick(self, event):
        self.DefaultAction()
        event.Skip()


    def onClose(self, event):
        self.plugin.menuDlg = None
        self.Show(False)
        self.Destroy()
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

class SchedulerTable(gridlib.PyGridTableBase):

    def __init__(self, header):
        gridlib.PyGridTableBase.__init__(self)
        self.colLabels = header
        self.dataTypes = [gridlib.GRID_VALUE_BOOL,
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_DATETIME,
                          gridlib.GRID_VALUE_DATETIME
                          ]

        self.data = [[0,""," ",""],]


    def GetNumberRows(self):
        return len(self.data)


    def GetNumberCols(self):
        return len(self.data[0])


    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True


    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''


    def SetValue(self, row, col, value):
        self.data[row][col] = value


    def GetColLabelValue(self, col):
        return self.colLabels[col]


    def GetTypeName(self, row, col):
        return self.dataTypes[col]


    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False


    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)


    def AppendRow(self):
        self.data.append([1,"", " ", ""])
        msg = gridlib.GridTableMessage(self,            # The table
                gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, # what we did to it
                1                                       # how many
                )
        self.GetView().ProcessTableMessage(msg)


    def DeleteRow(self, row):
        self.data.pop(row)
        msg = gridlib.GridTableMessage(self,           # The table
                gridlib.GRIDTABLE_NOTIFY_ROWS_DELETED, # what we did to it
                row,1                                  # which and how many
                )
        self.GetView().ProcessTableMessage(msg)
#===============================================================================

class SchedulerGrid(gridlib.Grid):

    def __init__(self, parent, text, width):
        gridlib.Grid.__init__(self, parent, -1, style = wx.BORDER_SIMPLE )
        self.back = self.GetDefaultCellBackgroundColour()
        self.fore = self.GetDefaultCellTextColour()
        self.selBack = self.GetSelectionBackground()
        self.selFore = self.GetSelectionForeground()
        self.table = SchedulerTable(text.header)
        self.SetTable(self.table, True)
        self.SetRowLabelSize(0)
        self.SetMargins(0,0)
        self.EnableDragColSize(False)
        self.EnableDragRowSize(False)
        self.EnableDragGridSize(False)
        self.AutoSizeColumns(False)
        self.SetScrollLineX(1)
        self.SetScrollLineY(self.GetRowSize(0))

        border = self.GetWindowBorderSize()[0]
        const_width = self.GetColSize(0)+2*96+SYS_VSCROLL_X+border
        self.SetColSize(1,width - const_width)
        self.SetColSize(2,96)
        self.SetColSize(3,96)

        self.SetSize((width,154))
        self.SetMinSize((width,154))
        attr = gridlib.GridCellAttr()
        attr.SetAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.SetColAttr(0,attr)
        attr = gridlib.GridCellAttr()
        attr.SetReadOnly()
        self.SetColAttr(1,attr)
        self.SetColAttr(2,attr)
        self.SetColAttr(3,attr)

        gridlib.EVT_GRID_SELECT_CELL(self, self.onGridSelectCell)


    def onGridSelectCell(self, evt):
        for row in range(self.GetNumberRows()):
            if self.GetCellTextColour(row, 0) == self.selFore:
                attr = gridlib.GridCellAttr()
                attr.SetBackgroundColour(self.back)
                attr.SetTextColour(self.fore)
                self.SetRowAttr(row, attr)
        attr = gridlib.GridCellAttr()
        attr.SetBackgroundColour(self.selBack)
        attr.SetTextColour(self.selFore)
        self.SetRowAttr(evt.GetRow(), attr)
        self.ForceRefresh()
        evt.Skip()


    def AppendRow(self):
        self.table.AppendRow()


    def DeleteRow(self, row):
        col = self.GetGridCursorCol()
        self.table.DeleteRow(row)
        lngth = self.table.GetNumberRows()


    def SelRow(self, row):
        if self.GetNumberRows()-1 >= row:
            self.SetGridCursor(row, 1)


    def SetValue(self, cell, value):
        self.table.SetValue(cell[0], cell[1], value)
        self.ForceRefresh()


    def GetValue(self, row, col):
        return self.table.GetValue(row, col)
#===============================================================================

class schedulerDialog(wx.Dialog):

    lastRow = -1
    data = []

    def __init__(self, text, plugin):
        wx.Dialog.__init__(
            self,
            None,
            -1,
            text.dialogTitle,
            style=wx.CAPTION | wx. STAY_ON_TOP,
        )

        #import locale as l
        #l.setlocale(l.LC_ALL, "us") # only for testing

        bttns=[]
        self.ctrls=[]
        self.plugin = plugin
        self.text = text

        def fillDynamicSizer(type, data = None, old_type = 255):
            flag = old_type != type
            if flag:
                dynamicSizer.Clear(True)
                self.ctrls=[]
                id=wx.NewId()
                self.ctrls.append(id)
                id=wx.NewId()
                self.ctrls.append(id)
            if type == -1:
                return
            if type == 0:
                if flag:
                    topSizer = wx.StaticBoxSizer(
                        wx.StaticBox(self, -1, self.text.chooseDay),
                        wx.HORIZONTAL
                    )
                    id=wx.NewId()
                    self.ctrls.append(id)
                    dp = wx.DatePickerCtrl(self, self.ctrls[2], size=(86,-1),
                            style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
                    topSizer.Add(dp,0,wx.EXPAND)
                    id=wx.NewId()
                    self.ctrls.append(id)
                    yearlyCtrl = wx.CheckBox(self, self.ctrls[3], self.text.yearly)
                    topSizer.Add(yearlyCtrl, 0, wx.EXPAND|wx.LEFT, 30)                    
                    dynamicSizer.Add(topSizer,0,wx.EXPAND|wx.TOP,2)
                else:
                    dp = wx.FindWindowById(self.ctrls[2])
                    yearlyCtrl = wx.FindWindowById(self.ctrls[3])
                if data:
                    if not data[2]:
                        val = wx.DateTime_Now()
                        data[2] = str(dt.now())[:10]
                    wxDttm=wx.DateTime()
                    wxDttm.Set(int(data[2][8:10]),int(data[2][5:7])-1,int(data[2][:4]))
                    dp.SetValue(wxDttm)
                    yearlyCtrl.SetValue(data[3])
            elif type == 2:
                if flag:
                    choices = list(day_name)
                    id=wx.NewId()
                    self.ctrls.append(id)
                    weekdayCtrl = wx.CheckListBox(
                        self,
                        self.ctrls[2],
                        choices = choices,
                        size=((-1,110)),
                    )
                    topSizer = wx.StaticBoxSizer(
                        wx.StaticBox(self, -1, self.text.chooseDay),
                        wx.HORIZONTAL
                    )
                    topSizer.Add((40,1),0,wx.ALIGN_CENTER)
                    topSizer.Add(wx.StaticText(self,-1,self.text.theEvery),0,wx.ALIGN_CENTER|wx.RIGHT,10)
                    topSizer.Add(weekdayCtrl,0,wx.TOP)
                    dynamicSizer.Add(topSizer,0,wx.EXPAND|wx.TOP,2)
                else:
                    weekdayCtrl = wx.FindWindowById(self.ctrls[2])
                val = 127 if not data else data[2]
                for i in range(7):
                    weekdayCtrl.Check(i, bool(val&(2**i)))
            elif type == 3: # Monthly ...
                if flag:
                    dateSizer = wx.BoxSizer(wx.HORIZONTAL)
                    dateSizer.Add(wx.StaticText(self,-1,self.text.the),0,wx.ALIGN_CENTER)
                    topSizer = wx.StaticBoxSizer(
                        wx.StaticBox(self, -1, self.text.chooseDay),
                        wx.VERTICAL
                    )
                    topSizer.Add(dateSizer,0,wx.EXPAND)
                    dynamicSizer.Add(topSizer,0,wx.EXPAND|wx.TOP,2)

                    id=wx.NewId()
                    self.ctrls.append(id)
                    serialCtrl = wx.CheckListBox(
                        self,
                        self.ctrls[2],
                        choices = self.text.serial_num,
                        size=((-1,95)),
                    )
                    dateSizer.Add(serialCtrl,0,wx.ALIGN_CENTER|wx.LEFT,10)

                    choices = list(day_name)
                    id=wx.NewId()
                    self.ctrls.append(id)
                    weekdayCtrl = wx.CheckListBox(
                        self,
                        self.ctrls[3],
                        choices = choices,
                        size=((-1,110)),
                    )
                    dateSizer.Add(weekdayCtrl,0,wx.ALIGN_CENTER|wx.LEFT,10)
                    dateSizer.Add(wx.StaticText(self,-1,self.text.in_),0,wx.ALIGN_CENTER|wx.LEFT,10)
                    id=wx.NewId()
                    self.ctrls.append(id)
                    monthsCtrl_1 = wx.CheckListBox(
                        self,
                        self.ctrls[4],
                        choices = list(month_name)[1:7],
                        size=((-1,95)),
                    )
                    dateSizer.Add(monthsCtrl_1,0,wx.ALIGN_CENTER|wx.LEFT,10)
                    id=wx.NewId()
                    self.ctrls.append(id)
                    monthsCtrl_2 = wx.CheckListBox(
                        self,
                        self.ctrls[5],
                        choices = list(month_name)[7:],
                        size=((-1,95)),
                    )
                    dateSizer.Add(monthsCtrl_2,0,wx.ALIGN_CENTER|wx.LEFT,-1)
                else:
                    serialCtrl = wx.FindWindowById(self.ctrls[2])
                    weekdayCtrl = wx.FindWindowById(self.ctrls[3])
                    monthsCtrl_1 = wx.FindWindowById(self.ctrls[4])
                    monthsCtrl_2 = wx.FindWindowById(self.ctrls[5])
                val = 0 if not data else data[2]
                for i in range(6):
                    serialCtrl.Check(i, bool(val&(2**i)))
                val = 0 if not data else data[3]
                for i in range(7):
                    weekdayCtrl.Check(i, bool(val&(2**i)))
                val = 63 if not data else data[4]
                for i in range(6):
                    monthsCtrl_1.Check(i, bool(val&(2**i)))
                val = 63 if not data else data[5]
                for i in range(6):
                    monthsCtrl_2.Check(i, bool(val&(2**i)))

            #else: # type == 1 (daily):
            #    pass
            if flag:
                timeSizer = wx.GridBagSizer(0,0)
                bottomSizer = wx.StaticBoxSizer(
                    wx.StaticBox(self, -1, self.text.chooseTime),
                    wx.HORIZONTAL
                )
                dynamicSizer.Add(bottomSizer,0,wx.EXPAND|wx.TOP,5)
                bottomSizer.Add(timeSizer, 0, wx.EXPAND)
                timeSizer.Add(wx.StaticText(self,-1,self.text.start),(0,0),(1,2))
                id=wx.NewId()
                self.ctrls.append(id)
                durLabel = wx.StaticText(self, id, self.text.length)
                timeSizer.Add(durLabel, (0,3), (1,2))
                spinBtn = wx.SpinButton(self,-1, wx.DefaultPosition, (-1,22), wx.SP_VERTICAL )
                val = data[0] if data and data[0] else wx.DateTime_Now()
                timeCtrl = maskedlib.TimeCtrl(
                    self, self.ctrls[0], val, fmt24hr = True, spinButton = spinBtn)
                timeSizer.Add(timeCtrl,(1,0),(1,1))
                timeSizer.Add(spinBtn,(1,1),(1,1))
                timeSizer.Add((40,-1),(1,2), (1,1))
                spinBtn2 = wx.SpinButton(self,-1, wx.DefaultPosition, (-1,22), wx.SP_VERTICAL )
                val = data[1] if data and data[1] else "00:00"
                lenCtrl = maskedlib.TimeCtrl(
                    self, self.ctrls[1], val, fmt24hr = True, spinButton = spinBtn2, displaySeconds = False)
                timeSizer.Add(lenCtrl,(1,3),(1,1))
                timeSizer.Add(spinBtn2,(1,4),(1,1))
                bottomSizer.Add((-1,-1), 1, wx.EXPAND)
                testBttn = wx.Button(self, -1 if len(bttns) == 0 else bttns[5], self.text.testButton)
                bottomSizer.Add(testBttn, 0, wx.EXPAND|wx.RIGHT)
                dynamicSizer.Layout()
            else:
                timeCtrl = wx.FindWindowById(self.ctrls[0])
                val = data[0] if data and data[0] else wx.DateTime_Now()
                timeCtrl.SetValue(val)
                lenCtrl = wx.FindWindowById(self.ctrls[1])
                val = data[1] if data and data[1] else "00:00"
                lenCtrl.SetValue(val)
            return dynamicSizer.GetMinSize()

        dynamicSizer = wx.BoxSizer(wx.VERTICAL)
        wDynamic = fillDynamicSizer(3)[0]
        fillDynamicSizer(-1)
        self.SetSize(wx.Size(wDynamic+37, 645))
        grid = SchedulerGrid(self, text, wDynamic+20)


        def onCheckListBox(evt):
            id = evt.GetId()
            sel = evt.GetSelection()
            box = self.FindWindowById(id)
            ix = self.ctrls.index(id)
            if box.IsChecked(sel):
                self.data[self.lastRow][3][ix] |= 2**sel
            else:
                self.data[self.lastRow][3][ix] &= 255-2**sel
            next = self.plugin.NextRun(self.data[self.lastRow][2],self.data[self.lastRow][3])
            if next:
                grid.SetValue((self.lastRow, 3), next[:-3])
            else:
                grid.SetValue((self.lastRow, 3), "")
        wx.EVT_CHECKLISTBOX(self, -1, onCheckListBox)


        def OnTimeChange(evt):
            ix = self.ctrls.index(evt.GetId())
            self.data[self.lastRow][3][ix]=evt.GetValue()
            next = self.plugin.NextRun(self.data[self.lastRow][2],self.data[self.lastRow][3])
            if next:
                grid.SetValue((self.lastRow, 3), next[:-3])
            else:
                grid.SetValue((self.lastRow, 3), "")
        maskedlib.EVT_TIMEUPDATE(self, -1, OnTimeChange)


        def onDatePicker(evt):
            val = str(dt.fromtimestamp(evt.GetDate().GetTicks()))[:10]
            self.data[self.lastRow][3][2] = val
            next = self.plugin.NextRun(self.data[self.lastRow][2],self.data[self.lastRow][3])
            if next:
                grid.SetValue((self.lastRow, 3), next[:-3])
            else:
                grid.SetValue((self.lastRow, 3), "")
        wx.EVT_DATE_CHANGED(self, -1, onDatePicker)


        def onYearlyCtrl(evt):
            val = evt.IsChecked()
            self.data[self.lastRow][3][3] = int(val)
            next = self.plugin.NextRun(self.data[self.lastRow][2],self.data[self.lastRow][3])
            if next:
                grid.SetValue((self.lastRow, 3), next[:-3])
            else:
                grid.SetValue((self.lastRow, 3), "")
        wx.EVT_CHECKBOX(self, -1, onYearlyCtrl)


        def OpenSchedule():
            schedulerName.ChangeValue(self.data[self.lastRow][1])
            type = self.data[self.lastRow][2]
            fillDynamicSizer(type, self.data[self.lastRow][3], typeChoice.GetSelection())
            typeChoice.SetSelection(type)
            modes = self.data[self.lastRow][7]
            rsMode = (modes>>1)&3
            workModeCtrl.SetSelection(rsMode)
            recordCtrl.GetTextCtrl().ChangeValue(self.data[self.lastRow][5])
            sourceCtrl.SetValue(self.data[self.lastRow][4])
            if rsMode == 3:
                windOpenCtrl.SetSelection(-1)
                windOpenCtrl.Enable(False)
                windOpenLbl.Enable(False)
            else:
                windOpenCtrl.SetSelection(modes&1)
                windOpenCtrl.Enable(True)
                windOpenLbl.Enable(True)
            triggEvtCtrl.SetSelection((modes>>3)&3)


        def OnLeftClick(evt):
            self.lastRow = evt.GetRow()
            OpenSchedule()
            evt.Skip() # necessary !!!
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, OnLeftClick)


        def enableBttns(value):
            for i in range(1,3):
                bttn=self.FindWindowById(bttns[i])
                bttn.Enable(value)


        def ShowMessageBox(mess):
            PlaySound('SystemExclamation', SND_ASYNC)
            MessageBox(
                self.GetHandle(),
                mess,
                self.text.boxTitle,
                    48
                )


        def FindNewTitle(title):
            tmpLst=[]
            for item in self.data:
                if item[1].startswith(title+" ("):
                    tmpLst.append(item[1][2+len(title):])
            if len(tmpLst)==0:
                return "%s (1)" % title
            tmpLst2=[]
            for item in tmpLst:
                if item[-1]==")":
                    try:
                        tmpLst2.append(int(item[:-1]))
                    except:
                        pass
            if len(tmpLst2)==0:
                return "%s (1)" % title
            else:
                return "%s (%i)" % (title, 1+max(tmpLst2))


        def testValidity(data, test):
            mssgs = []
            if test:
                data = [data,]
            tempDict = dict([(item[1].strip(), item[2]) for item in data])
            if "" in tempDict:
                mssgs.append(self.text.boxTexts[0])
            if not test and len(tempDict) < len(data):
                mssgs.append(self.text.boxTexts[1])
            for item in data:
                val = item[7]
                if (val & 6) == 6: # = Do nothing
                    if not val & 24:
                        if not self.text.boxTexts[3] in mssgs:
                            mssgs.append(self.text.boxTexts[3])
                else:
                    if "" in [item[4].strip() for item in data]:
                        if not self.text.boxTexts[2] in mssgs:
                            mssgs.append(self.text.boxTexts[2])
                if item[2] == -1:
                    if not self.text.boxTexts[4] in mssgs:
                        mssgs.append(self.text.boxTexts[4])
            flag = len(mssgs) == 0
            if not flag:
                ShowMessageBox("\n".join(mssgs))
            return flag


        def onButton(evt):
            id = evt.GetId()
            lngth = len(self.data)
            if id == bttns[0]:   # Add new
                grid.AppendRow()
                empty = [1, "", -1, [], "", "", " ",5]
                if lngth == 0:
                    self.lastRow = 0
                    self.data=[empty,]
                    enableBttns(True)
                else:
                    self.lastRow = lngth
                    self.data.append(empty)
                    Tidy()
                grid.SelRow(self.lastRow)
                EnableCtrls(True)
            elif id == bttns[1]: # Duplicate
                item = cpy(self.data[self.lastRow])
                self.lastRow = lngth
                self.data.append(item)
                newTitle = FindNewTitle(self.data[lngth][1])
                self.data[lngth][1] = newTitle
                grid.AppendRow()
                grid.SelRow(lngth)
                grid.SetValue((lngth, 1), newTitle)
                OpenSchedule()
            elif id == bttns[2]: # Delete
                self.data.pop(self.lastRow)
                grid.DeleteRow(self.lastRow)
                if len(self.data) > 0:
                    if self.lastRow == len(self.data):
                        self.lastRow -= 1
                    OpenSchedule()
                    grid.SelRow(self.lastRow)
                else:
                    self.lastRow = -1
                    Tidy()
                    EnableCtrls(False)
                    enableBttns(False)
            elif id == bttns[3]: # OK
                if not testValidity(self.data, False):
                    return
                for i in range(len(self.data)):
                    value = int(grid.GetValue(i, 0))
                    self.data[i][0]=value
                self.plugin.dataToXml(self.data)
                self.plugin.UpdateEGscheduler()
                self.Show(False)
                self.MakeModal(False)
                self.Destroy()
            elif id == bttns[4]: # Cancel
                self.Show(False)
                self.MakeModal(False)
                self.Destroy()


        def EnableCtrls(value):
            favChoice.Enable(value)
            typeChoice.Enable(value)
            sourceCtrl.Enable(value)
            schedulerName.Enable(value)
            workModeCtrl.Enable(value)
            windOpenCtrl.Enable(value)
            triggEvtCtrl.Enable(value)
            name_label.Enable(value)
            type_label.Enable(value)
            source_label.Enable(value)
            favorite_label.Enable(value)
            workModeLbl.Enable(value)
            windOpenLbl.Enable(value)
            triggEvtLbl.Enable(value)
            filename_label.Enable(value)
            recordCtrl.Enable(value)
            if not value:
                windOpenCtrl.SetSelection(-1)
                workModeCtrl.SetSelection(-1)
                triggEvtCtrl.SetSelection(-1)
            else:
                windOpenCtrl.SetSelection(1)
                workModeCtrl.SetSelection(2)
                triggEvtCtrl.SetSelection(0)


        def Tidy():
            favChoice.SetSelection(-1)
            typeChoice.SetSelection(-1)
            windOpenCtrl.SetSelection(1)
            workModeCtrl.SetSelection(2)
            triggEvtCtrl.SetSelection(0)
            sourceCtrl.ChangeValue("")
            recordCtrl.GetTextCtrl().ChangeValue("")
            schedulerName.ChangeValue("")
            fillDynamicSizer(-1)
            filename_label.Enable(True)
            recordCtrl.Enable(True)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 0, wx.ALL, 5)
        bttnSizer=wx.BoxSizer(wx.HORIZONTAL)
        bttnSizer.Add((5, -1))
        i=0
        for bttn in self.text.buttons:
            id=wx.NewId()
            bttns.append(id)
            b = wx.Button(self, id, bttn)
            bttnSizer.Add(b,1)
            if i in (1,2):
                b.Enable(False)
            b.Bind(wx.EVT_BUTTON, onButton)
            bttnSizer.Add((5, -1))
            i+=1

        #testBttn event handling:
        id=wx.NewId()
        bttns.append(id)
        def onTestButton(evt):
            data = self.data[self.lastRow]
            if not testValidity(data, True):
                return
            next = self.plugin.Execute(data)
            next = next[:19] if next else self.plugin.text.none
            self.plugin.updateLogFile(self.text.testRun % (data[1], next))
        self.Bind(wx.EVT_BUTTON, onTestButton, id = id)

        sizer.Add(bttnSizer,0,wx.EXPAND)
        schedulerName = wx.TextCtrl(self,-1,"")
        self.favorites = self.plugin.RefreshVariables()
        favChoice = wx.Choice(self, -1, choices = [item[1] for item in self.favorites])
        typeChoice = wx.Choice(self, -1, choices = self.text.sched_type)
        sourceCtrl = wx.TextCtrl(self,-1,"")
        xmltoparse = u'%s\\RadioSure.xml' % self.plugin.xmlpath
        xmldoc = miniDom.parse(xmltoparse.encode(eg.systemEncoding))
        recordings = xmldoc.getElementsByTagName('Recordings')[0]
        folder = recordings.getElementsByTagName('Folder')[0].firstChild.data
        recordCtrl = MyFileBrowseButton(
            self,
            toolTip = self.text.toolTipFile,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse,
            startDirectory = folder
        )
        recordCtrl.GetTextCtrl().SetEditable(False)


        def onSchedulerTitle(evt):
            txt = evt.GetString()
            grid.SetValue((self.lastRow,1), txt)
            self.data[self.lastRow][1] = txt
        schedulerName.Bind(wx.EVT_TEXT, onSchedulerTitle)


        def onSource(evt):
            src = evt.GetString()
            srcs = [item[0] for item in self.favorites]
            if src in srcs:
                ix = srcs.index(src)
            else:
                ix = -1
            favChoice.SetSelection(ix)
            txt = evt.GetString()
            self.data[self.lastRow][4] = txt
            evt.Skip()
        sourceCtrl.Bind(wx.EVT_TEXT, onSource)


        def onFavChoice(evt):
            sel = evt.GetSelection()
            txt = self.favorites[sel][0]
            sourceCtrl.ChangeValue(txt)
            self.data[self.lastRow][4] = txt
            evt.Skip()
        favChoice.Bind(wx.EVT_CHOICE, onFavChoice)


        def onRecordCtrl(evt):
            txt = evt.GetString()
            self.data[self.lastRow][5] = txt
            evt.Skip()
        recordCtrl.GetTextCtrl().Bind(wx.EVT_TEXT, onRecordCtrl)


        def onTypeChoice(evt):
            type = evt.GetSelection()
            if self.data[self.lastRow][2] != type:
                empty_data=[["","",0,0],["",""],["","",127],["","",0,0,63,63]]
                self.data[self.lastRow][2] = type
                self.data[self.lastRow][3]=empty_data[self.data[self.lastRow][2]]
                data = empty_data[self.data[self.lastRow][2]]
                fillDynamicSizer(type, data)
        typeChoice.Bind(wx.EVT_CHOICE, onTypeChoice)

        nameSizer = wx.FlexGridSizer(2,0,0,20)
        nameSizer.AddGrowableCol(0,1)
        name_label = wx.StaticText(self, -1, self.text.header[1]+":")
        nameSizer.Add(name_label)
        type_label = wx.StaticText(self, -1, self.text.type_label)
        nameSizer.Add(type_label)
        nameSizer.Add(schedulerName, 0, wx.EXPAND)
        nameSizer.Add(typeChoice)
        typeSizer = wx.StaticBoxSizer(
            wx.StaticBox(self, -1, ""),
            wx.VERTICAL
        )
        dynamicSizer.SetMinSize((-1,197))
        typeSizer.Add(nameSizer, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        typeSizer.Add(dynamicSizer, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        sizer.Add(typeSizer, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        source_label = wx.StaticText(self, -1, self.text.source)
        sizer.Add(source_label, 0, wx.TOP|wx.LEFT, 5)
        sizer.Add(sourceCtrl,0,wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        sizer.Add((1,4))
        favorite_label = wx.StaticText(self, -1, self.text.favorite)
        workModeLbl = wx.StaticText(self, -1, self.text.workModeLabel)
        workModeCtrl = wx.Choice(self, -1, choices = self.text.workModes)
        triggEvtLbl = wx.StaticText(self, -1, self.text.triggEvtLabel)
        triggEvtCtrl = wx.Choice(self, -1, choices = self.text.triggEvtChoices)


        def onWorkMode(evt):
            sel = evt.GetSelection()
            if sel == 3:
                windOpenCtrl.SetSelection(-1)
                windOpenCtrl.Enable(False)
                windOpenLbl.Enable(False)
                if triggEvtCtrl.GetSelection() == 0:
                    ShowMessageBox(self.text.boxTexts[3])
            else:
                if windOpenCtrl.GetSelection() == -1:
                    windOpenCtrl.SetSelection(1)
                    windOpenCtrl.Enable(True)
                    windOpenLbl.Enable(True)
            val = self.data[self.lastRow][7]
            val &= (255-6)
            val |= (sel<<1)
            self.data[self.lastRow][7] = val
        workModeCtrl.Bind(wx.EVT_CHOICE, onWorkMode)
        windOpenLbl = wx.StaticText(self, -1, self.text.windOpenLabel)
        windOpenCtrl = wx.Choice(self, -1, choices = self.text.windOpenChoices)


        def onWindOpen(evt):
            sel = evt.GetSelection()
            val = self.data[self.lastRow][7]
            val &= (255-1)
            val |= sel
            self.data[self.lastRow][7] = val
        windOpenCtrl.Bind(wx.EVT_CHOICE, onWindOpen)


        def onTriggEvtCtrl(evt):
            sel = evt.GetSelection()
            workMode = workModeCtrl.GetSelection()
            if sel == 0 and workMode == 3:
                ShowMessageBox(self.text.boxTexts[3])
            val = self.data[self.lastRow][7]
            val &= (255-24)
            val |= (sel<<3)
            self.data[self.lastRow][7] = val
        triggEvtCtrl.Bind(wx.EVT_CHOICE, onTriggEvtCtrl)

        sizer.Add(favorite_label, 0, wx.TOP|wx.LEFT, 5)
        sizer.Add(favChoice,0,wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        sizer.Add((1,4))
        choicesSizer = wx.FlexGridSizer(2,3,0,10)
        choicesSizer.Add(windOpenLbl,0)
        choicesSizer.Add(workModeLbl,0)
        choicesSizer.Add(triggEvtLbl,0)
        choicesSizer.Add(windOpenCtrl,0,wx.EXPAND)
        choicesSizer.Add(workModeCtrl,0,wx.EXPAND)
        choicesSizer.Add(triggEvtCtrl,0,wx.EXPAND)
        sizer.Add(choicesSizer,0,wx.ALL, 5)
        filename_label = wx.StaticText(self, -1, self.text.filename)
        sizer.Add(filename_label, 0, wx.LEFT, 5)
        sizer.Add(recordCtrl,0,wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.data = self.plugin.xmlToData()
        rows = len(self.data)
        if rows > 0:
            for row in range(rows):
                grid.SetValue((row,0), self.data[row][0])
                grid.SetValue((row,1), self.data[row][1])
                grid.SetValue((row,2), self.data[row][6])
                next = self.plugin.NextRun(self.data[row][2], self.data[row][3])
                val = next[:-3] if next else ""
                grid.SetValue((row,3), val)
                if row < rows-1:
                    grid.AppendRow()
            self.lastRow = 0
            grid.SelRow(0)
            OpenSchedule()
            enableBttns(True)
        else:
            EnableCtrls(False)
            grid.DeleteRow(0)

        self.SetSizer(sizer)
        sizer.Layout()
        self.Center()
        self.MakeModal(True)
        self.Show(True)
#===============================================================================

def HandleRS():

    FindRS = eg.WindowMatcher(
                u'RadioSure.exe',
                None,
                u'#32770',
                None,
                None,
                None,
                True,
                0.0,
                0
            )
    hwnds = FindRS()
    res = None
    for hwnd in hwnds:
        curhw = GetWindow(hwnd,GW_CHILD)
        while curhw > 0:
            if GetDlgCtrlID(curhw) == 1016 and GetClassName(curhw) == 'SysListView32':
                res = hwnd
                break
            curhw = GetWindow(curhw,GW_HWNDNEXT)
        if res:
            break
    return res
#===============================================================================

class ObservationThread(Thread):

    def __init__(
        self,
        period,
        evtName,
    ):
        self.abort = False
        self.aborted = False
        self.oldData = ""
        self.threadFlag = Event()

        self.period = period
        self.evtName = evtName
        Thread.__init__(self, name = self.evtName.encode('unicode_escape')+'_Thread')


    def run(self):
        while 1:
            hwnd = HandleRS()
            if hwnd:
                data = GetWindowText(hwnd).decode(eg.systemEncoding)
                if data != self.oldData and data != "Radio? Sure!":
                    self.oldData = data
                    eg.TriggerEvent(self.evtName, payload = data, prefix = "RadioSure")
            if self.abort:
                break
            self.threadFlag.wait(self.period)
            self.threadFlag.clear()
        self.aborted = True


    def AbortObservation(self):
        self.abort = True
        self.threadFlag.set()
#===============================================================================

def GetCtrlByID(id):

    res = None
    hwnd = HandleRS()
    if hwnd:
        try:
            res = GetDlgItem(hwnd,id)
        except:
            pass
    return res
#===============================================================================

def getPathFromReg():

    try:
        rs_reg = OpenKey(
            HKEY_CURRENT_USER,
            "Software\\RadioSure"
        )
        res = unicode(EnumValue(rs_reg,0)[1])
        CloseKey(rs_reg)
    except:
        res = None
    return res
#===============================================================================

def FindMonthDay(year, month, weekday, index):
    """weekday = what day of the week looking for (numbered 0-6, 0 = monday)
    index = how many occurrence of looking for (numbered 0-4 and 5 for the last day)
    Returns the day of the month (date) or 0 (if no such date exists)"""
    first_wd, length = monthrange(year, month)
    day = 1 + weekday - first_wd
    if day < 1:
        day += 7
    if index == 5:
        index = 4 if day <= length % 7 else 3
    day += 7 * (index)
    if day > length:
        day = 0
    return day
#===============================================================================

class RadioSure(eg.PluginBase):

    text=Text
    menuDlg = None
    RadioSurePath = u''
    xmlPath = u''
    Favorites = []
    History = []
    Current = ['','']
    FavIx = -1
    HistIx = -1
    List = None

    def RefreshVariables(self):

        def getList(nodelist):
            tmp1 = []
            tmp0 = []
            for item in nodelist.childNodes:
                if item.hasChildNodes():
                    tmp0.append(item.firstChild.data)
            for i in range(0, len(tmp0), 2):
                item = [tmp0[i], tmp0[i+1]]
                tmp1.append(item)
            return tmp1

        xmltoparse = u'%s\\RadioSure.xml' % self.xmlpath
        if not os.path.exists(xmltoparse):
            return
        xmldoc = miniDom.parse(xmltoparse.encode(eg.systemEncoding))
        currURL = xmldoc.getElementsByTagName('Station_URL')[0].firstChild
        if currURL:
            self.Current[0] = currURL.data
        currTitle = xmldoc.getElementsByTagName('Station_Title')[0].firstChild
        if currTitle:
            self.Current[1] = currTitle.data
        self.History = getList(xmldoc.getElementsByTagName('History')[0])
        self.Favorites = getList(xmldoc.getElementsByTagName('Favorites')[0])
        if self.Current in self.Favorites:
            self.FavIx = self.Favorites.index(self.Current)
        else:
            self.FavIx = -1
        if self.Current in self.History:
            self.HistIx = self.History.index(self.Current)
        else:
            self.HistIx = -1
        return self.Favorites


    def NextRun(self, type, data):
        now = dt.now()
        runTime = dt.strptime(data[0], "%H:%M:%S").time()
        if type == 0: # once or yearly
            runDate = dt.strptime(data[2], '%Y-%m-%d')
            runDateTime = dt.combine(runDate, runTime)
            if now < runDateTime:
                return str(runDateTime)
            elif not data[3]:
                return None
            else:
                if runDateTime.replace(year = now.year) < now:
                    return str(runDateTime.replace(year = now.year + 1))
                else:
                    return str(runDateTime.replace(year = now.year))
        elif type == 1: # daily
            runDateTime = dt.combine(now.date(),runTime)
            if now.time() > runTime:
                runDateTime += td(days=1)
            return str(runDateTime)
        elif type == 2: # weekly
            runDateTime = dt.combine(now.date(), runTime)
            weekdays = []
            nowDay = now.weekday()
            for weekday in range(7):
                if 2**weekday & data[2]:
                    weekdays.append(weekday)
            if now.time() < runTime and nowDay in weekdays:
                return str(runDateTime)
            deltas = []
            for day in weekdays:
                deltas.append(day - nowDay if day > nowDay else 7 + day - nowDay)
            return str(runDateTime + td(days=min(deltas)))
        else: # 3 = monthly
            if data[2] == 0 or data[3] == 0 or (data[4] + data[5]) == 0:
                return None
            runList=[]
            currMonth = now.month
            currYear = now.year
            monthsInt = data[4]+(data[5]<<6)
            months = []
            for month in range(1,13):
                if 2**(month-1) & monthsInt:
                    months.append(month)
            if currMonth in months:
                for ix in range(6):
                    if 2**ix & data[2]:
                        for weekday in range(7):
                            if 2**weekday & data[3]:
                                day=FindMonthDay(currYear,currMonth,weekday,ix)
                                if day:
                                    runDateTime = dt.combine(dt(currYear,currMonth,day).date(),runTime)
                                    if now < runDateTime:
                                        runList.append(runDateTime)
            if len(runList) == 0:
                lower = []
                larger = []
                nextMonth = None
                for month in months:
                    if month>currMonth:
                        larger.append(month)
                    else: #month<=currMonth:
                        lower.append(month)
                if len(larger) > 0:
                    nextMonth = min(larger)
                    nextYear = currYear
                elif len(lower)>0:
                    nextMonth = min(lower)
                    nextYear = currYear+1
                if nextMonth:
                    for ix in range(6):
                        if 2**ix & data[2]:
                            for weekday in range(7):
                                if 2**weekday & data[3]:
                                    day=FindMonthDay(nextYear,nextMonth,weekday,ix)
                                    if day:
                                        runDateTime = dt.combine(dt(nextYear,nextMonth,day).date(),runTime)
                                        runList.append(runDateTime)
            if len(runList) > 0:
                return str(min(runList))
            else:
                return None


    def updateLogFile(self, line, blank = False):
        if not self.logfile:
            return
        f = openFile(self.logfile, encoding='utf-8', mode='a')
        if blank:
            f.write("\r\n")
        f.write("%s  %s\r\n" % (str(dt.now())[:19], line))
        f.close()


    def Execute(self, params):

        def my_list2cmdline(seq):
            """ FIXING subprocess.list2cmdline
            Workaround, because subprocess.list2cmdline does not work with arguments like: 
            filename="... ...". Ie, when we need quotes inside the string, and somewhere 
            inside is a space character. When you properly prepare all items 
            (including the quotes), it works!
            There is also done simultaneously filesystemencode encoding 
            (otherwise there UnicodeDecodeError occurs...)"""
            return ' '.join([arg.encode(fse) if isinstance(arg, unicode) else arg for arg in seq])
        subprocess.list2cmdline = my_list2cmdline

        next = self.NextRun(params[2], params[3])
        modes = params[7]
        playRec = modes & 6
        if playRec != 6:
            args = [u'%s\\RadioSure.exe' % self.RadioSurePath,]
            if playRec:
                args.append("/record")
            else:
                args.append("/play")
            if playRec == 4:
                args.append("/mute")
            if modes & 1:
                args.append("/hidden")
            args.append(u'/source="%s"' % params[4])
            duration = 60*int(params[3][1][:2])+int(params[3][1][-2:])
            if duration:
                args.append('/duration=%i' % duration)
            if params[5]:
                args.append(u'/filename="%s"' % params[5])
            elif playRec:
                args.append(u'/filename="%s"' % params[1])
            subprocess.Popen(args)
        if next: # new schedule, if valid next run time
            startTicks = mktime(strptime(next, "%Y-%m-%d %H:%M:%S"))
            eg.scheduler.AddTaskAbsolute(startTicks, self.RadioSureScheduleRun, params[1])
        triggEvt = modes & 24
        if triggEvt == 8:
            eg.TriggerEvent(self.text.launched, prefix = "RadioSure", payload = params[1])
        elif triggEvt == 16:
            eg.TriggerEvent(self.text.launched, prefix = "RadioSure", payload = params)
        return next


    def RadioSureScheduleRun(self, schedule):
        data = self.xmlToData()
        ix = [item[1] for item in data].index(schedule)
        next = self.Execute(data[ix])
        data[ix][6] = str(dt.now())[:16]
        self.dataToXml(data)
        mssg = next[:19] if next else self.text.none
        self.updateLogFile(self.text.execut % (data[ix][1], mssg))


    def UpdateEGscheduler(self):
        xmlfile = u'%s\\Scheduler.xml' % self.xmlpath
        if not os.path.exists(xmlfile):
            return
        data = self.xmlToData()
        tmpList = []
        sched_list = eg.scheduler.__dict__['heap']
        for sched in sched_list:
            if sched[1] == self.RadioSureScheduleRun:
                if sched[2][0] in [item[1] for item in data]:
                    tmpList.append(sched)
                else:
                    self.updateLogFile(self.text.cancAndDel % sched[2][0])
                    eg.scheduler.CancelTask(sched)
        sched_list = tmpList
        for schedule in data:
            startMoment = self.NextRun(schedule[2], schedule[3])
            if not startMoment:
                continue
            startTicks = mktime(strptime(startMoment,"%Y-%m-%d %H:%M:%S"))

            nameList = [item[2][0] for item in sched_list]
            if schedule[1] in nameList:
                sched = sched_list[nameList.index(schedule[1])]
                if not schedule[0]: # schedule is disabled !
                    eg.scheduler.CancelTask(sched)
                    self.updateLogFile(self.text.cancAndDis % schedule[1])
                elif sched[0] != startTicks:
                    self.updateLogFile(self.text.re_Sched % (schedule[1], startMoment))
                    eg.scheduler.CancelTask(sched)
                    eg.scheduler.AddTaskAbsolute(startTicks, self.RadioSureScheduleRun, schedule[1])
            elif schedule[0]:
                    eg.scheduler.AddTaskAbsolute(startTicks, self.RadioSureScheduleRun, schedule[1])
                    self.updateLogFile(self.text.newSched % (schedule[1], startMoment))


    def dataToXml(self, data):
        impl = miniDom.getDOMImplementation()
        dom = impl.createDocument(None, u'Document', None)
        root = dom.documentElement
        for item in data:
            schedNode = dom.createElement(u'Schedule')
            schedNode.setAttribute(u'Name', unicode(item[1]))
            schedNode.setAttribute(u'Type', unicode(item[2]))
            enableNode = dom.createElement(u'Enable')
            enableText = dom.createTextNode(unicode(item[0]))
            enableNode.appendChild(enableText)
            schedNode.appendChild(enableNode)
            sourceNode = dom.createElement(u'Source')
            sourceText = dom.createTextNode(unicode(item[4]))
            sourceNode.appendChild(sourceText)
            schedNode.appendChild(sourceNode)
            filenameNode = dom.createElement(u'Filename')
            filenameText = dom.createTextNode(unicode(item[5]))
            filenameNode.appendChild(filenameText)
            schedNode.appendChild(filenameNode)
            last_runNode = dom.createElement(u'Last_run')
            last_runText = dom.createTextNode(unicode(item[6]))
            last_runNode.appendChild(last_runText)
            schedNode.appendChild(last_runNode)
            modesNode = dom.createElement(u'Modes')
            modesText = dom.createTextNode(unicode(item[7]))
            modesNode.appendChild(modesText)
            schedNode.appendChild(modesNode)
            start_timeNode = dom.createElement(u'Start_time')
            start_timeText = dom.createTextNode(unicode(item[3][0]))
            start_timeNode.appendChild(start_timeText)
            schedNode.appendChild(start_timeNode)
            durationNode = dom.createElement(u'Duration')
            durationText = dom.createTextNode(unicode(item[3][1]))
            durationNode.appendChild(durationText)
            schedNode.appendChild(durationNode)
            if item[2] == 0:
                dateNode = dom.createElement(u'Date')
                dateText = dom.createTextNode(unicode(item[3][2]))
                dateNode.appendChild(dateText)
                schedNode.appendChild(dateNode)
                yearlyNode = dom.createElement(u'Yearly')
                yearlyText = dom.createTextNode(unicode(item[3][3]))
                yearlyNode.appendChild(yearlyText)
                schedNode.appendChild(yearlyNode)
            if item[2] == 2:
                weekdayNode = dom.createElement(u'Weekday')
                weekdayText = dom.createTextNode(unicode(item[3][2]))
                weekdayNode.appendChild(weekdayText)
                schedNode.appendChild(weekdayNode)
            if item[2] == 3:
                orderNode = dom.createElement(u'Order')
                orderText = dom.createTextNode(unicode(item[3][2]))
                orderNode.appendChild(orderText)
                schedNode.appendChild(orderNode)
                weekdayNode = dom.createElement(u'Weekday')
                weekdayText = dom.createTextNode(unicode(item[3][3]))
                weekdayNode.appendChild(weekdayText)
                schedNode.appendChild(weekdayNode)
                first_halfNode = dom.createElement(u'First_half')
                first_halfText = dom.createTextNode(unicode(item[3][4]))
                first_halfNode.appendChild(first_halfText)
                schedNode.appendChild(first_halfNode)
                second_halfNode = dom.createElement(u'Second_half')
                second_halfText = dom.createTextNode(unicode(item[3][5]))
                second_halfNode.appendChild(second_halfText)
                schedNode.appendChild(second_halfNode)
            root.appendChild(schedNode)
        f = file(u'%s\\Scheduler.xml' % self.xmlpath, 'wb')
        writer = lookup('utf-8')[3](f)
        dom.writexml(writer, encoding = 'utf-8')
        f.close()


    def xmlToData(self):
        data = []
        xmlfile = u'%s\\Scheduler.xml' % self.xmlpath
        if not os.path.exists(xmlfile):
            return data
        xmldoc = miniDom.parse(xmlfile)
        document = xmldoc.getElementsByTagName('Document')[0]
        schedules = document.getElementsByTagName('Schedule')
        for schedule in schedules:
            dataItem = []
            enable = int(schedule.getElementsByTagName('Enable')[0].firstChild.data)
            dataItem.append(enable)
            name = schedule.attributes["Name"].value
            dataItem.append(name)
            type = int(schedule.attributes["Type"].value)
            dataItem.append(type)
            params = []
            start_time = schedule.getElementsByTagName('Start_time')[0].firstChild.data
            params.append(start_time)
            duration = schedule.getElementsByTagName('Duration')[0].firstChild.data
            params.append(duration)
            if type == 0:
                date = schedule.getElementsByTagName('Date')[0].firstChild.data
                params.append(date)
                date = int(schedule.getElementsByTagName('Yearly')[0].firstChild.data)
                params.append(date)
            if type == 2:
                weekday = int(schedule.getElementsByTagName('Weekday')[0].firstChild.data)
                params.append(weekday)
            if type == 3:
                order = int(schedule.getElementsByTagName('Order')[0].firstChild.data)
                params.append(order)
                weekday = int(schedule.getElementsByTagName('Weekday')[0].firstChild.data)
                params.append(weekday)
                first_half = int(schedule.getElementsByTagName('First_half')[0].firstChild.data)
                params.append(first_half)
                second_half = int(schedule.getElementsByTagName('Second_half')[0].firstChild.data)
                params.append(second_half)
            dataItem.append(params)
            source = schedule.getElementsByTagName('Source')[0].firstChild
            source = source.data if source else ""
            dataItem.append(source)
            filename = schedule.getElementsByTagName('Filename')[0].firstChild
            filename = filename.data if filename else ""
            dataItem.append(filename)
            last_run = schedule.getElementsByTagName('Last_run')[0].firstChild
            last_run = last_run.data if last_run else " "
            dataItem.append(last_run)
            modes = schedule.getElementsByTagName('Modes')[0].firstChild.data
            dataItem.append(int(modes))
            data.append(dataItem)
        return data


    def PlayFromMenu(self):
        if self.menuDlg is not None:
            sel=self.menuDlg.stationChoiceCtrl.GetSelectedRows()[0]
            self.menuDlg.Close()
        hwnd = HandleRS()
        if hwnd:
            List = self.Favorites if self.List else self.History
            Base = 1326 if self.List else 1374
            if sel <= len(List)-1:
                SendMessage(hwnd, WM_COMMAND, Base+sel, 0)
        else:
            self.PrintError(self.text.text1)


    def __init__(self):
        self.observThread = None
        text=Text
        self.AddActionsFromList(Actions)


    def __start__(self, path = None, xmlpath = None, logfile = None):
        self.RadioSurePath = path
        self.xmlpath = xmlpath
        self.logfile = logfile
        if xmlpath:
            if logfile:
                 self.updateLogFile(self.text.start, True)
            self.UpdateEGscheduler()


    def __stop__(self):
        if self.observThread:
            ot = self.observThread
            if ot.isAlive():
                ot.AbortObservation()
            del self.observThread
        self.observThread = None
        sched_list = eg.scheduler.__dict__['heap']
        tmpLst = []
        for sched in sched_list:
            if sched[1] == self.RadioSureScheduleRun:
                tmpLst.append(sched)
        if len(tmpLst) > 0:
            self.updateLogFile(self.text.stop)
            for sched in tmpLst:
                eg.scheduler.CancelTask(sched)
                self.updateLogFile(self.text.canc % sched[2][0])


    def __close__(self):
        if self.observThread:
            ot = self.observThread
            if ot.isAlive():
                ot.AbortObservation()


    def Configure(self, path = None, xmlpath = None, logfile = None):
        self.RadioSurePath = path
        self.xmlpath = xmlpath
        self.logfile = logfile
        panel = eg.ConfigPanel(self)
        label1Text = wx.StaticText(panel, -1, self.text.label1)
        rsPathCtrl = MyDirBrowseButton(
            panel,
            size=(410,-1),
            toolTip = self.text.toolTipFolder,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse
        )
        rsPathCtrl.GetTextCtrl().SetEditable(False)
        label2Text = wx.StaticText(panel, -1, self.text.label2)
        xmlPathCtrl = MyDirBrowseButton(
            panel,
            size=(410,-1),
            toolTip = self.text.toolTipFolder,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse
        )
        xmlPathCtrl.GetTextCtrl().SetEditable(False)
        logFileCtrl = MyFileBrowseButton(
            panel,
            size=(410,-1),
            toolTip = self.text.toolTipFile,
            dialogTitle = self.text.browseFile,
            buttonText = eg.text.General.browse
        )
        logFileCtrl.GetTextCtrl().SetEditable(False)
        logCheckBox = wx.CheckBox(panel, -1, self.text.logLabel)

        if self.RadioSurePath is None:
            RSpath = getPathFromReg()
            if RSpath:
                self.RadioSurePath = RSpath
                rsPathCtrl.GetTextCtrl().ChangeValue(self.RadioSurePath)
            else:
                self.RadioSurePath = "%s\\RadioSure" % unicode(eg.folderPath.ProgramFiles)
                rsPathCtrl.GetTextCtrl().ChangeValue("")
        rsPathCtrl.GetTextCtrl().ChangeValue(self.RadioSurePath)
        if self.xmlpath is None:
            xmlPath = u"%s\\RadioSure" % unicode(eg.folderPath.LocalAppData)
            self.xmlpath = xmlPath if os.path.exists(xmlPath) else ""
        xmlPathCtrl.GetTextCtrl().ChangeValue(self.xmlpath)
        if self.logfile is None:
            logCheckBox.SetValue(True)
            self.logfile = u'%s\\SchedulerLog.txt' % self.xmlpath if self.xmlpath else ""
        else:
            val = self.logfile != ""
            logCheckBox.SetValue(val)
            logFileCtrl.Enable(val)
        logFileCtrl.GetTextCtrl().ChangeValue(self.logfile)

        rsPathCtrl.startDirectory = self.RadioSurePath
        xmlPathCtrl.startDirectory = self.xmlpath
        logFileCtrl.startDirectory = self.logfile or u"%s\\RadioSure" % unicode(eg.folderPath.LocalAppData)
        sizerAdd = panel.sizer.Add
        sizerAdd(label1Text, 0, wx.TOP,15)
        sizerAdd(rsPathCtrl,0,wx.TOP,2)
        sizerAdd(label2Text, 0, wx.TOP,15)
        sizerAdd(xmlPathCtrl,0,wx.TOP,2)
        sizerAdd(logCheckBox, 0, wx.TOP,15)
        sizerAdd(logFileCtrl, 0, wx.TOP,2)


        def Validation():
            flag1 = "%s\\RadioSure.exe" % os.path.exists(rsPathCtrl.GetValue())
            flag2 = "%s\\RadioSure.xml" % os.path.exists(xmlPathCtrl.GetValue())
            flag3 = logCheckBox.IsChecked() and logFileCtrl.GetValue() != "" or not logCheckBox.IsChecked()
            flag = flag1 and flag2 and flag3
            panel.dialog.buttonRow.okButton.Enable(flag)
            panel.isDirty = True
            panel.dialog.buttonRow.applyButton.Enable(flag)


        def OnPathChange(event):
            path = rsPathCtrl.GetValue()
            if not os.path.exists("%s\\RadioSure.exe" % path):
                MessageBox(
                    panel.GetHandle(),
                    self.text.boxMessage1 % 'RadioSure.exe',
                    self.text.boxTitle % path,
                        48
                    )
            if path != "":
                rsPathCtrl.startDirectory = path
                self.RadioSurePath = path
            Validation()
            event.Skip()
        rsPathCtrl.Bind(wx.EVT_TEXT, OnPathChange)


        def OnPath2Change(event):
            path2 = xmlPathCtrl.GetValue()
            if not os.path.exists("%s\\RadioSure.xml" % path2):
                MessageBox(
                    panel.GetHandle(),
                    self.text.boxMessage1 % 'RadioSure.xml',
                    self.text.boxTitle % path2,
                        48
                    )
            if path2 != "":
                self.xmlpath = path2
                xmlPathCtrl.startDirectory = path2
            Validation()
            event.Skip()
        xmlPathCtrl.Bind(wx.EVT_TEXT, OnPath2Change)


        def logFileChange(event):
            self.logfile = logFileCtrl.GetValue()
            tmpVal = self.logfile
            if not tmpVal:
                tmpPath = u"%s\\RadioSure" % unicode(eg.folderPath.LocalAppData)
                tmpVal = tmpPath if os.path.exists(tmpPath) else self.RadioSurePath
            logFileCtrl.startDirectory = tmpVal
            Validation()
            event.Skip()
        logFileCtrl.Bind(wx.EVT_TEXT, logFileChange)


        def onLogCheckBox(evt):
            val = evt.IsChecked()
            logFileCtrl.Enable(val)
            if not val:
                logFileCtrl.SetValue("")
            else:
                Validation()
            evt.Skip()
        logCheckBox.Bind(wx.EVT_CHECKBOX, onLogCheckBox)
        while panel.Affirmed():
            panel.SetResult(
                rsPathCtrl.GetValue(),
                xmlPathCtrl.GetValue(),
                logFileCtrl.GetValue(),
            )
#===============================================================================
#cls types for Actions list:
#===============================================================================

class Run(eg.ActionBase):

    class text:
        play = "Automatically play selected favorite after start"
        default = "Use start settings RadioSure"
        label = "Select favorite:"
        over = "Too large number (%s > %s) !"
        alt_ret = "Default start"
        alr_run = "RadioSure is already running !"
        text2 = "Couldn't find file %s !"


    def __call__(self, play = False, fav = 1):
        hwnd = HandleRS()
        if hwnd is None:
            rs = '%s\\RadioSure.exe' % self.plugin.RadioSurePath
            if os.path.isfile(rs):
#                wx.CallAfter(subprocess.Popen,[rs])
                subprocess.Popen([rs])
                if play:
                    for n in range(50):
                        sleep(.1)
                        hwnd = HandleRS()
                        if hwnd:
                            flag = True
                            break
                    if flag:
                        SendMessage(hwnd, WM_COMMAND, 1008, 0) #Stop playing
                        sleep(2.5)
                        self.plugin.RefreshVariables()
                        if fav <= len(self.plugin.Favorites):
                            SendMessage(hwnd, WM_COMMAND, 1325+fav, 0)
                            return str(fav)+": "+self.plugin.Favorites[self.plugin.FavIx][1]
                        else:
                            return self.text.over % (str(fav),\
                                str(len(self.plugin.Favorites)))
                    else:
                        self.PrintError(self.plugin.text.text1)
                        return self.plugin.text.text1
                else:
                    return self.text.alt_ret
            else:
                self.PrintError(self.text.text2 % 'RadioSure.exe')
                return self.text.text2 % 'RadioSure.exe'
        else:
            return self.text.alr_run


    def GetLabel(self, play ,fav):
        num = ':'+str(fav) if play else ''
        return self.name+num


    def Configure(self, play = False, fav = 1):
        panel=eg.ConfigPanel(self)
        sizerAdd=panel.sizer.Add
        rb1 = panel.RadioButton(play, self.text.play, style=wx.RB_GROUP)
        rb2 = panel.RadioButton(not play, self.text.default)
        sizerAdd(rb1,0,wx.TOP,15)
        sizerAdd(rb2,0,wx.TOP,6)
        favLbl=wx.StaticText(panel, -1, self.text.label)
        sizerAdd(favLbl,0,wx.TOP,25)
        favCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            fav,
            fractionWidth=0,
            min=1,
            max=30,
        )
        favCtrl.SetValue(fav)
        sizerAdd(favCtrl,0,wx.TOP,5)

        def onChangeMode(evt=None):
            enbl=rb1.GetValue()
            favLbl.Enable(enbl)
            favCtrl.Enable(enbl)
            if evt is not None:
                evt.Skip()
        rb1.Bind(wx.EVT_RADIOBUTTON, onChangeMode)
        rb2.Bind(wx.EVT_RADIOBUTTON, onChangeMode)
        onChangeMode()

        while panel.Affirmed():
            panel.SetResult(
                rb1.GetValue(),
                favCtrl.GetValue()
            )
#===============================================================================

class WindowControl(eg.ActionBase):

    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            SendMessage(hwnd, WM_SYSCOMMAND, self.value, 0)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class SendMessageActions(eg.ActionBase):

    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            SendMessage(hwnd, WM_COMMAND, self.value, 0)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class Play(eg.ActionBase):

    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            self.plugin.RefreshVariables()
            SendMessage(hwnd, WM_COMMAND, 1374+self.plugin.HistIx, 0)
            return self.plugin.History[self.plugin.HistIx][1]
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class SetVolume(eg.ActionBase):

    class text:
        label=["Set volume (0 - 100%):",
            "Set step (1 - 25%):",
            "Set step (1 - 25%):"]


    def __call__(self, step = None):
        if step is None:
            if self.value == 0:
                step = 50
            else:
                step = 5
        hwnd = GetCtrlByID(1006) #1006 = ID of ctrl "msctls_trackbar32"
        if hwnd:
            vol = SendMessage(hwnd, TBM_GETPOS, 0, 0)
            key = None
            value = None
            if self.value == 0:
                volume = step
            elif self.value == 1:
                volume = vol+step if (vol+step)<100 else 100
            else:
                volume = vol-step if (vol-step)>0 else 0
            if vol>volume:
                key='{Left}'
                if vol>volume+1:
                    value = volume+1
            elif vol<volume:
                key='{Right}'
                if vol<volume-1:
                    value = volume-1
            if value:
                SendMessage(hwnd, TBM_SETPOS,1,value)
            if key:
                eg.SendKeys(hwnd, key, False)
            return SendMessage(hwnd, TBM_GETPOS, 0, 0)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1


    def Configure(self, step = None):
        if step is None:
            if self.value == 0:
                step = 50
            else:
                step = 5
        panel=eg.ConfigPanel(self)
        panel.sizer.Add(wx.StaticText(panel, -1, self.text.label[self.value]))
        if self.value == 0:
            Min = 0
            Max = 100
        else:
            Min = 1
            Max = 25
        volumeCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            step,
            fractionWidth=0,
            increment=1,
            min=Min,
            max=Max,
        )
        volumeCtrl.SetValue(step)
        panel.sizer.Add(volumeCtrl,0,wx.TOP,10)

        while panel.Affirmed():
            panel.SetResult(volumeCtrl.GetValue())
#===============================================================================

class GetVolume(eg.ActionBase):

    def __call__(self):
        hwnd = GetCtrlByID(1006)  #1006 = ID for ctrl "msctls_trackbar32"
        if hwnd:
            return SendMessage(hwnd, TBM_GETPOS, 0, 0)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class SelectFav(eg.ActionBase):

    class text:
        label = "Select preset number (1-30):"
        txtLabel = 'Preset number:'
        over = "Too large number (%s > %s) !"
        modeLabel = 'Preset number to get as:'
        modeChoices = [
            'Event payload',
            'Python expression',
            'Number'
        ]


    def __call__(self,fav = 1, mode = 0, number = '{eg.event.payload}'):
        hwnd = HandleRS()
        if hwnd:
            if mode == 2:
                indx = fav
            else:
                indx = int(eg.ParseString(number))
            self.plugin.RefreshVariables()
            if indx <= len(self.plugin.Favorites):
                SendMessage(hwnd, WM_COMMAND, 1325+indx, 0)
                return str(indx)+": "+self.plugin.Favorites[indx-1][1]
            else:
                self.PrintError(
                    self.text.over % (str(indx),str(len(self.plugin.Favorites))))
                return self.text.over % (str(indx),str(len(self.plugin.Favorites)))
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1


    def GetLabel(self, fav,mode,number):
        if mode == 2:
            number = str(fav)
        return self.text.txtLabel+number


    def Configure(self, fav = 1, mode = 0, number = '{eg.event.payload}'):
        self.number = number
        panel = eg.ConfigPanel(self)
        radioBoxMode = wx.RadioBox(
            panel,
            -1,
            self.text.modeLabel,
            choices = self.text.modeChoices,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxMode.SetSelection(mode)
        txtBoxLabel = wx.StaticText(panel, -1, self.text.txtLabel)
        numberCtrl = wx.TextCtrl(panel,-1,self.number)
        spinLabel = wx.StaticText(panel, -1, self.text.label)
        favCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            fav,
            fractionWidth=0,
            min=1,
            max=30,
        )
        favCtrl.SetValue(fav)
        panel.sizer.Add(radioBoxMode, 0, wx.TOP,0)
        panel.sizer.Add(txtBoxLabel,0,wx.TOP,10)
        panel.sizer.Add(numberCtrl,0,wx.TOP,5)
        panel.sizer.Add(spinLabel,0,wx.TOP,10)
        panel.sizer.Add(favCtrl,0,wx.TOP,5)

        def onRadioBox(event = None):
            sel = radioBoxMode.GetSelection()
            txtBoxLabel.Enable(False)
            numberCtrl.Enable(False)
            spinLabel.Enable(False)
            favCtrl.Enable(False)
            if sel == 0:
                self.number = '{eg.event.payload}'
            elif sel == 1:
                txtBoxLabel.Enable(True)
                numberCtrl.Enable(True)
            else:
                self.number = favCtrl.GetValue()
                spinLabel.Enable(True)
                favCtrl.Enable(True)
            numberCtrl.ChangeValue(str(self.number))
            if event:
                event.Skip()
        radioBoxMode.Bind(wx.EVT_RADIOBOX, onRadioBox)
        onRadioBox()


        def onSpin(event):
            numberCtrl.ChangeValue(str(favCtrl.GetValue()))
            event.Skip()
        favCtrl.Bind(wx.EVT_TEXT, onSpin)

        while panel.Affirmed():
            panel.SetResult(
                favCtrl.GetValue(),
                radioBoxMode.GetSelection(),
                numberCtrl.GetValue())
#===============================================================================

class NextPrevFav(eg.ActionBase):

    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            self.plugin.RefreshVariables()
            ix = self.plugin.FavIx
            if self.value == 1 and ix == len(self.plugin.Favorites) - 1 :
                ix = -1
            elif self.value == -1 and ix == 0:
                ix = len(self.plugin.Favorites)
            SendMessage(hwnd, WM_COMMAND, 1326+ix+self.value, 0)
            return (str(ix+self.value+1)+": "+self.plugin.Favorites[ix+self.value][1])
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class RandomFav(eg.ActionBase):

    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            self.plugin.RefreshVariables()
            ix = self.plugin.FavIx
            lng = len(self.plugin.Favorites)
            if lng > 1:
                newIx = randrange(lng)
                while newIx == ix:
                    newIx = randrange(lng)
                SendMessage(hwnd, WM_COMMAND, 1326+newIx, 0)
                return (str(newIx+1)+": "+self.plugin.Favorites[newIx][1])
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class GetPlayingTitle(eg.ActionBase):

    def __call__(self):
        hwnd = HandleRS()
        if hwnd:
            return GetWindowText(hwnd)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
#===============================================================================

class StartTitlebarObservation(eg.ActionBase):

    class text:
        intervalLabel = "Refresh interval (s):"
        label = "Event suffix:"
        timeStamp = "Insert timestamp"


    def __call__(
        self,
        period = 1.0,
        evtName ="titlebar",
    ):
        if self.plugin.observThread:
            ot = self.plugin.observThread
            if ot.isAlive():
                ot.AbortObservation()
            del self.plugin.observThread
        ot = ObservationThread(
            period,
            evtName,
        )
        ot.start()
        self.plugin.observThread = ot


    def Configure(
        self,
        period = 1.0,
        evtName = "titlebar",
    ):
        panel = eg.ConfigPanel()
        periodNumCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            period,
            integerWidth = 5,
            fractionWidth = 1,
            allowNegative = False,
            min = 0.1,
            increment = 0.1,
        )
        intervalLbl = wx.StaticText(panel, -1, self.text.intervalLabel)
        textLabel = wx.StaticText(panel, -1, self.text.label)
        textControl = wx.TextCtrl(panel, -1, evtName, size = (200,-1))
        AddCtrl = panel.sizer.Add
        AddCtrl(intervalLbl, 0, wx.TOP, 20)
        AddCtrl(periodNumCtrl, 0, wx.TOP, 3)
        AddCtrl(textLabel, 0, wx.TOP, 20)
        AddCtrl(textControl, 0, wx.TOP, 3)
        textLabel.SetFocus()
        while panel.Affirmed():
            panel.SetResult(
            periodNumCtrl.GetValue(),
            textControl.GetValue(),
        )
#===============================================================================

class StopTitlebarObservation(eg.ActionBase):

    def __call__(self):
        if self.plugin.observThread:
            ot = self.plugin.observThread
            if ot.isAlive():
                ot.AbortObservation()
            del self.plugin.observThread
        self.plugin.observThread = None
#===============================================================================

class ShowMenu(eg.ActionBase):

    panel = None

    class text:
        osmLabel = 'OSM show on:'
        menuPreview = 'On screen menu preview:'
        menuFont = 'Menu font:'
        txtColour = 'Text colour'
        backColour = 'Background colour'
        txtSelColour = 'Selected text colour'
        backSelColour = 'Selected background colour'


    def __call__(
        self,
        fore,
        back,
        fontInfo,
        monitor=0,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75),
    ):
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
                self.value
            )
            eg.actionThread.WaitOnEvent(self.event)
#===============================================================================

    def GetLabel(
        self,
        fore,
        back,
        fontInfo,
        monitor,
        foreSel,
        backSel,
    ):
        return self.name


    def Configure(
        self,
        fore = (75, 75, 75),
        back = (180, 180, 180),
        fontInfo = None,
        monitor = 0,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75),
    ):
        self.plugin.RefreshVariables()
        self.List = self.plugin.Favorites if self.value else self.plugin.History
        choices = [item[1] for item in self.List]
        self.fore = fore
        self.back = back
        self.foreSel = foreSel
        self.backSel = backSel
        global panel
        panel = eg.ConfigPanel(self)
        mainSizer = panel.sizer
        topSizer=wx.BoxSizer(wx.HORIZONTAL)
        topRightSizer=wx.FlexGridSizer(5,2,8,10)
        previewLbl=wx.StaticText(panel, -1, self.text.menuPreview)
        mainSizer.Add(previewLbl)
        mainSizer.Add(topSizer,0,wx.TOP,5)
        #Font button
        fontLbl=wx.StaticText(panel, -1, self.text.menuFont)
        fontButton = extFontSelectButton(panel, value = fontInfo)
        #Button Text Colour
        foreLbl=wx.StaticText(panel, -1, self.text.txtColour+':')
        foreColourButton = extColourSelectButton(panel,self.fore, title = self.text.txtColour)
        #Button Background Colour
        backLbl=wx.StaticText(panel, -1, self.text.backColour+':')
        backColourButton = extColourSelectButton(panel,self.back,title = self.text.backColour)
        #Button Selected Text Colour
        foreSelLbl=wx.StaticText(panel, -1, self.text.txtSelColour+':')
        foreSelColourButton = extColourSelectButton(panel,self.foreSel,title = self.text.txtSelColour)
        #Button Selected Background Colour
        backSelLbl=wx.StaticText(panel, -1, self.text.backSelColour+':')
        backSelColourButton = extColourSelectButton(panel,self.backSel, title = self.text.backSelColour)
        ch = len(choices) if len(choices) > 0 else 1
        listBoxCtrl = MenuGrid(panel, ch)
        listBoxCtrl.SetMinSize(wx.Size(220, 177))
        listBoxCtrl.SetBackgroundColour(self.back)
        listBoxCtrl.SetForegroundColour(self.fore)
        listBoxCtrl.SetSelectionBackground(self.backSel)
        listBoxCtrl.SetSelectionForeground(self.foreSel)
        if fontInfo is None:
            font = listBoxCtrl.GetFont()
            font.SetPointSize(36)
            fontInfo = font.GetNativeFontInfoDesc()
        else:
            font = wx.FontFromNativeInfoString(fontInfo)
        for n in range(10,20):
            font.SetPointSize(n)
            fontButton.SetFont(font)
            hght = fontButton.GetTextExtent('X')[1]
            if hght > 20:
                break
        listBoxCtrl.SetDefaultCellFont(font)
        listBoxCtrl.SetDefaultRowSize(hght+4, True)
        for i in range(len(choices)):
            listBoxCtrl.SetCellFont(i,0,font)
            listBoxCtrl.SetCellValue(i,0,choices[i])
        wdth = 220
        if (hght+4)*len(choices) > 177:
            wdth -=  SYS_VSCROLL_X
        listBoxCtrl.SetColSize(0, wdth)
        topSizer.Add(listBoxCtrl)
        topSizer.Add((20,1))
        topSizer.Add(topRightSizer)
        osmLbl = wx.StaticText(panel, -1, self.text.osmLabel)
        displayChoice = eg.DisplayChoice(panel, monitor)
        topRightSizer.Add(fontLbl,0,wx.TOP,4)
        topRightSizer.Add(fontButton,0,wx.TOP,0)
        topRightSizer.Add(foreLbl,0,wx.TOP,4)
        topRightSizer.Add(foreColourButton,0,wx.TOP,0)
        topRightSizer.Add(backLbl,0,wx.TOP,4)
        topRightSizer.Add(backColourButton,0,wx.TOP,0)
        topRightSizer.Add(foreSelLbl,0,wx.TOP,4)
        topRightSizer.Add(foreSelColourButton,0,wx.TOP,0)
        topRightSizer.Add(backSelLbl,0,wx.TOP,4)
        topRightSizer.Add(backSelColourButton,0,wx.TOP,0)
        topRightSizer.Add(osmLbl, 0, wx.TOP, 4)
        topRightSizer.Add(displayChoice, 0, wx.TOP, 0)
        listBoxCtrl.SetFocus()
        listBoxCtrl.SetGridCursor(0, 0)
        listBoxCtrl.SelectRow(0)
        mainSizer.Layout()

        def onMonitor(evt):
            listBoxCtrl.SetFocus()
            evt.Skip()
        displayChoice.Bind(wx.EVT_CHOICE, onMonitor)


        def OnFontBtn(evt):
            value = evt.GetValue()
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
                listBoxCtrl.SetCellFont(i,0,font)
            listBoxCtrl.SetFocus()
            evt.Skip()
        fontButton.Bind(EVT_BUTTON_AFTER, OnFontBtn)


        def OnColourBtn(evt):
            id = evt.GetId()
            value = evt.GetValue()
            if id == foreColourButton.GetId():
                listBoxCtrl.SetForegroundColour(value)
            elif id == backColourButton.GetId():
                listBoxCtrl.SetBackgroundColour(value)
            elif id == backSelColourButton.GetId():
                listBoxCtrl.SetSelectionBackground(value)
            elif id == foreSelColourButton.GetId():
                listBoxCtrl.SetSelectionForeground(value)
            listBoxCtrl.Refresh()
            listBoxCtrl.SetFocus()
            evt.Skip()
        foreColourButton.Bind(EVT_BUTTON_AFTER, OnColourBtn)
        backColourButton.Bind(EVT_BUTTON_AFTER, OnColourBtn)
        foreSelColourButton.Bind(EVT_BUTTON_AFTER, OnColourBtn)
        backSelColourButton.Bind(EVT_BUTTON_AFTER, OnColourBtn)


        # re-assign the test button
        def OnButton(event):
            if not self.plugin.menuDlg:
                self.plugin.menuDlg = Menu()
                self.event = CreateEvent(None, 0, 0, None)
                wx.CallAfter(self.plugin.menuDlg.ShowMenu,
                    foreColourButton.GetValue(),
                    backColourButton.GetValue(),
                    foreSelColourButton.GetValue(),
                    backSelColourButton.GetValue(),
                    fontButton.GetValue(),
                    True,
                    self.plugin,
                    self.event,
                    displayChoice.GetSelection(),
                    self.value
                )
                eg.actionThread.WaitOnEvent(self.event)
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnButton)

        while panel.Affirmed():
            panel.SetResult(
            foreColourButton.GetValue(),
            backColourButton.GetValue(),
            fontButton.GetValue(),
            displayChoice.GetSelection(),
            foreSelColourButton.GetValue(),
            backSelColourButton.GetValue(),
        )
#===============================================================================

class MoveCursor(eg.ActionBase):

    def __call__(self):
        if self.plugin.menuDlg is not None:
            max=len(self.plugin.Favorites)
            if max > 0:
                stationChoiceCtrl = self.plugin.menuDlg.stationChoiceCtrl
                sel=stationChoiceCtrl.GetSelectedRows()[0]
                if sel == eval(self.value[0]):
                    sel = eval(self.value[1])
                stationChoiceCtrl.SetGridCursor(sel+self.value[2], 0)
                stationChoiceCtrl.SelectRow(sel+self.value[2])
#===============================================================================

class OK_Btn(eg.ActionBase):

    def __call__(self):
        if self.plugin.menuDlg is not None:
            self.plugin.PlayFromMenu()
#===============================================================================

class Cancel_Btn(eg.ActionBase):

    def __call__(self):
        if self.plugin.menuDlg is not None:
            self.plugin.menuDlg.Close()
#===============================================================================

class OpenScheduler(eg.ActionBase):

    class text:
        dialogTitle = "Radio?Sure! Scheduler (EventGhost plugin by Pako)"
        header = (
            "Enabled",
            "Schedule title",
            "Last run",
            "Next run",
        )
        sched_type = (
            "Only once (or yearly)",
            "Daily",
            "Weekly",
            "Monthly"
        )
        toolTipFile = """Press button and browse to select file ...
File type (as .mp3) need not be completed. Will be added automatically."""

        browseTitle = "Select a folder and enter file name (without file type):"
        serial_num = (
            "first",
            "second",
            "third",
            "fourth",
            "fifth",
            "last"
        )
        the = "The"
        in_ = "in"
        buttons = (
            "Add new",
            "Duplicate",
            "Delete",
            "OK",
            "Cancel",
        )
        type_label = "Schedule type:"
        source = "Source URL:"
        favorite = "Favorite station title:"
        filename = "Destination file name (optional):"
        chooseDay = "Choose day"
        theEvery = "The every"
        yearly = "Every year on the same day"
        chooseTime = "Choose start time (HH:MM:SS) and duration (HH:MM)"
        start = "Start time:"
        length = "Duration (00:00 = constantly):"
        boxTitle = "Your setup is wrong !"
        boxTexts = (
            "Schedule title must not be an empty string !",
            "Schedule title must be unique !",
            'Determine the source URL, or set the mode "Do nothing" !',
            'Not allowed to set "Do nothing" while also "None" event !',
            'Must be chosen Schedule type !',
        )
        workModeLabel = "Radio?Sure! working mode:"
        workModes = (
            "Playing (audibly)",
            "Recording (audibly)",
            "Recording (soundlessly)",
            "Do nothing"
        )
        windOpenLabel = "Window open:"
        windOpenChoices =(
            "Visible",
            "Hidden"
        )
        triggEvtLabel = "Trigger an event:"
        triggEvtChoices = (
            "None",
            "Schedule title",
            "All parameters"
        )
        testButton = "Test now"
        testRun = 'Schedule "%s" - TEST execution. Possible next run: %s'


    def __call__(self):
        wx.CallAfter(schedulerDialog, self.text, self.plugin)
#===============================================================================

class EnableSchedule(eg.ActionBase):

    class text:
        scheduleTitle = "Schedule title:"
        notFound = 'Can not find schedule "%s" !'


    def __call__(self, schedule=""):
        schedule = eg.ParseString(schedule)
        xmlfile = u'%s\\Scheduler.xml' % self.plugin.xmlpath
        if not os.path.exists(xmlfile):
            return
        data = self.plugin.xmlToData()
        tmpLst = [item[1] for item in data]
        if schedule in tmpLst:
            ix = tmpLst.index(schedule)
            if self.value > -1:
                data[ix][0] = self.value
                self.plugin.dataToXml(data)
                self.plugin.UpdateEGscheduler()
            return data[tmpLst.index(schedule)]
        else:
            return self.text.notFound % schedule


    def Configure(self, schedule=""):
        panel = eg.ConfigPanel()
        textControl = wx.TextCtrl(panel, -1, schedule, size = (300,-1))
        panel.sizer.Add(wx.StaticText(panel,-1,self.text.scheduleTitle), 0,wx.LEFT|wx.TOP, 10)
        panel.sizer.Add(textControl, 0, wx.LEFT, 10)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())
#===============================================================================

class EnableAll(eg.ActionBase):

    def __call__(self):
        xmlfile = u'%s\\Scheduler.xml' % self.plugin.xmlpath
        if not os.path.exists(xmlfile):
            return
        data = self.plugin.xmlToData()
        for schedule in data:
            schedule[0] = self.value
        self.plugin.dataToXml(data)
        self.plugin.UpdateEGscheduler()
#===============================================================================

class DeleteSchedule(eg.ActionBase):

    class text:
        scheduleTitle = "Schedule title:"


    def __call__(self, schedule=""):
        schedule = eg.ParseString(schedule)
        xmlfile = u'%s\\Scheduler.xml' % self.plugin.xmlpath
        if not os.path.exists(xmlfile):
            return
        data = self.plugin.xmlToData()
        tmpLst = [item[1] for item in data]
        if schedule in tmpLst:
            ix = tmpLst.index(schedule)
            data.pop(ix)
            self.plugin.dataToXml(data)
            self.plugin.UpdateEGscheduler()


    def Configure(self, schedule=""):
        panel = eg.ConfigPanel()
        textControl = wx.TextCtrl(panel, -1, schedule, size = (300,-1))
        panel.sizer.Add(wx.StaticText(panel,-1,self.text.scheduleTitle), 0,wx.LEFT|wx.TOP, 10)
        panel.sizer.Add(textControl, 0, wx.LEFT, 10)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())
#===============================================================================

class AddSchedule(eg.ActionBase):

    class text:
        python_expr = "Python expression:"
        descr = u'''<rst>**Add schedule**.

In the edit box, enter a python expression with the parameters of the plan.
This may be for example *eg.result*, *eg.event.payload* or the entire list
(in the same format, what you get as a result of actions **"GetSchedule"**).

This action works in two ways (depending on the title of the schedule):

1. If the schedule with the same title already exists, its parameters are overwritten by new ones.
2. If the title does not exist yet, the schedule is added to the list as new.'''

    def __call__(self, expr = ""):
        xmlfile = u'%s\\Scheduler.xml' % self.plugin.xmlpath
        if not os.path.exists(xmlfile):
            return
        schedule = eg.ParseString(expr)
        schedule = eval(schedule)
        if len(schedule) == 8 and isinstance(schedule[1], unicode):
            data = self.plugin.xmlToData()
            tmpLst = [item[1] for item in data]
            if schedule[1] in tmpLst:
                data[tmpLst.index(schedule[1])] = schedule
            else:
                data.append(schedule)
            self.plugin.dataToXml(data)
            self.plugin.UpdateEGscheduler()


    def Configure(self, expr=""):
        panel = eg.ConfigPanel(resizable=True)
        textControl = wx.TextCtrl(panel, -1, expr, size = (300,-1), style = wx.TE_MULTILINE )
        panel.sizer.Add(wx.StaticText(panel,-1,self.text.python_expr), 0,wx.LEFT|wx.TOP, 10)
        panel.sizer.Add(textControl, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 10)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())
#===============================================================================

Actions = (
    (Run,"Run","Run RadioSure","Run RadioSure with its default settings.",None),
    (SendMessageActions,"Minimize","Minimize window","Minimize window.",2),
    (WindowControl,"Restore","Restore window","Restore window.",SC_RESTORE),
    (SendMessageActions,"MinimRest","Minimize/Restore","Minimize/Restore window.",1075),
    (SendMessageActions,"Close","Close window (exit RadioSure)","Close window (exit RadioSure).",1),
    (SendMessageActions,"Expand","Collapse/Expand window","Collapse/Expand window.",1076),
    (SendMessageActions,"OnTop","Stay on top On/Off","Stay on top On/Off.",1077),
    (SendMessageActions,"PlayStop","Play/Stop","Play/Stop.",1000),
    (SendMessageActions,"MuteOnOff","Mute On/Off","Mute On/Off.",1027),
    (SendMessageActions,"RecOnOff","Record On/Off","Record On/Off.",1051),
    (Play,"Play","Play","Play last playing station.",None),
    (SendMessageActions,"Stop","Stop","Stop.",1008),
#    (SendMessageActions,"RecOn","Rec on","Rec on.",0),
#    (SendMessageActions,"RecOff","Rec off","Rec off.",0),
#    (SendMessageActions,"MuteOn","Mute on","Mute on.",0),
#    (SendMessageActions,"MuteOff","Mute off","Mute off.",0),
    (GetVolume,"GetVolume","Get volume","Get volume.", None),
    (SetVolume,"SetVolume","Set volume","Set volume.", 0),
    (SetVolume,"VolumeUp","Volume up","Volume up.", 1),
    (SetVolume,"VolumeDown","Volume down","Volume down.", 2),
    (GetPlayingTitle,"GetPlayingTitle","Get currently playing station/title","Gets the name of currently playing station/title.", None),
    (StartTitlebarObservation,"StartTitlebarObservation","Start observation of titlebar","Starts observation of titlebar.", None),
    (StopTitlebarObservation,"StopTitlebarObservation","Stop observation of titlebar","Stops observation of titlebar.", None),
    (eg.ActionGroup, 'Equalizer', 'Equalizer', 'Equalizer',(
        (SendMessageActions,"EqualizerOff","Equalizer Off","Equalizer Off.", 2000),
        (SendMessageActions,"EqualizerJazz","Equalizer Jazz","Equalizer Jazz.", 2001),
        (SendMessageActions,"EqualizerPop","Equalizer Pop","Equalizer Pop.", 2002),
        (SendMessageActions,"EqualizerRock","Equalizer Rock","Equalizer Rock.", 2003),
        (SendMessageActions,"EqualizerClassic","Equalizer Classic","Equalizer Classic.", 2004),
    )),
    (eg.ActionGroup, 'Fav_and_Hist', 'Favorites and History', 'Favorites and History',(
        (SendMessageActions,"AddFav","Add to favorites","Add current station to favorites.",1324),
        (SendMessageActions,"RemFav","Remove from favorites","Remove current station from favorites.",1325),
        (SelectFav,"SelectFav","Select favorite (preset number)","Select favorite by preset number (order).", None),
        (NextPrevFav,"NextFav","Next favorite","Next favorite.", 1),
        (NextPrevFav,"PreviousFav","Previous favorite","Previous favorite.", -1),
        (RandomFav,"RandomFav","Random favorite","Random favorite.", None),
        (SendMessageActions,"PreviousHist","Back in history","Back in history.",1038),
        (SendMessageActions,"ForwardHist","Forward in history","Forward in history.",1039),
        (eg.ActionGroup, 'Menu', 'Menu', 'Menu',(
            (ShowMenu, 'ShowFavMenu', 'Show favorites menu', 'Show favorites on screen menu.', True),
            (ShowMenu, 'ShowHistMenu', 'Show history menu', 'Show history on screen menu.', False),
            (MoveCursor, 'MoveDown', 'Cursor down', 'Cursor down.', ('max-1', '-1', 1)),
            (MoveCursor, 'MoveUp', 'Cursor up', 'Cursor up.', ('0', 'max', -1)),
            (OK_Btn, 'OK_Btn', 'OK', 'OK button pressed.', None),
            (Cancel_Btn, 'Cancel_Btn', 'Cancel', 'Cancel button pressed.', None),
        )),
    )),
    (eg.ActionGroup, 'Scheduler', 'Scheduler', 'Scheduler',(
        (OpenScheduler,"OpenScheduler","Open scheduler","Open scheduler.", None),
        (EnableSchedule,"EnableSchedule","Enable schedule","Enable schedule.", 1),
        (EnableSchedule,"DisableSchedule","Disable schedule","Disable schedule.", 0),
        (EnableAll,"EnableAll","Enable all schedules","Enable all schedules.", 1),
        (EnableAll,"DisableAll","Disable all schedules","Disable all schedules.", 0),
        (EnableSchedule,"GetSchedule","Get schedule","Get schedule.", -1),
        (AddSchedule,"AddSchedule","Add schedule",AddSchedule.text.descr, None),
        (DeleteSchedule,"DeleteSchedule","Delete schedule","Delete schedule.", None),
    )),
)