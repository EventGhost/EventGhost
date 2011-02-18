version="0.2.10"

# plugins/RadioSure/__init__.py
#
# Copyright (C)  2009, 2010, 2011   Pako (lubos.ruckl@quick.cz)
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
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.2.10 by Pako 2011-02-12 09:53 UTC+1
#     - FixedTimeCtrl replaced by eg.TimeCtrl
# 0.2.9 by Pako 2011-01-15 11:50 UTC+1
#     - different shape of the cursor on the table of schedules indicate that there is context menu available
# 0.2.8 by Pako 2011-01-11 14:25 UTC+1
#     - if you turn on logging then into the log file is written whole command line
# 0.2.7 by Pako 2011-01-07 18:39 UTC+1
#     - fixed bug - the Scheduler window opens although in Scheduler.xml there not the attribute "Position"
#       (this can happen when you upgrade from version 0.2.0 and lower)
# 0.2.6 by Pako 2011-01-07 11:39 UTC+1
#     - fixed bug - incorrect reading favorites, when applied a new structure of RadioSure.xml file
# 0.2.5 by Pako 2010-12-28 16:02 UTC+1
#     - added popup menu and features "Move schedule up/down"
# 0.2.4 by Pako 2010-12-24 12:08 UTC+1
#     - there is no need to reinstall this plugin, when changing the way the installation (especially the paths) of Radio?Sure!
# 0.2.3 by Pako 2010-12-24 08:30 UTC+1
#     - scheduler dialog opens, even though there is no node "Favorites" in RadioSure.xml
# 0.2.2 by Pako 2010-12-19 15:54 UTC+1
#     - changed the way of paths settings to the RadioSure.exe and RadioSure.xml
# 0.2.1 by Pako 2010-12-19 08:19 UTC+1
#     - scheduler dialog remembers its position even after closing EventGhost
#     - bugfix - "Add schedule" enable buttons, when schedule list is empty
# 0.2.0 by Pako 2010-12-14 11:13 UTC+1
#     - a comprehensive rework according to the plugin SchedulGhost:
#     - addded new types of schedule
#     - changed format of "Scheduler.xml" file 
#     - added ability to affect certain types of schedules according to public holidays
#     - added option to select the first day of the week (Sunday or Monday)
#     - scheduler dialog remembers its position
#     - scheduler dialog is not modal and can be minimized
#     - added Apply button (scheduler dialog)
#     - added new actions - "Run schedule immediately"
# 0.1.9 by Pako 2010-12-09 13:52 UTC+1
#     - correction of previous versions (moreover redefine one pseudo-private method)
# 0.1.8 by Pako 2010-12-06 20:10 UTC+1
#     - wx.lib.masked.TimeCtrl workaround (see http://trac.wxwidgets.org/ticket/11171)
# 0.1.7 by Pako 2010-07-22 20:27 GMT+1
#     - bugfix
# 0.1.6 by Pako 2010-07-22 10:30 GMT+1
#     - added wx.ComboBox for Scheduler actions
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
import wx.calendar as wxCal
from calendar import day_name, month_name, monthrange
from wx.lib.mixins.listctrl import CheckListCtrlMixin
from _winreg import OpenKey, HKEY_CURRENT_USER, EnumValue, QueryValueEx, CloseKey
from time import sleep, mktime, strptime, strftime, localtime
from datetime import datetime as dt
from datetime import timedelta as td
from copy import deepcopy as cpy
from xml.dom import minidom as miniDom
from threading import Timer, Thread, Event
from eg.WinApi.Utils import GetMonitorDimensions
from eg.WinApi.Dynamic import CreateEvent, SetEvent
from eg.WinApi.Dynamic import SendMessage, ShowWindow
from win32gui import GetWindowText, MessageBox, GetWindow, GetDlgCtrlID
from win32gui import GetWindowPlacement, GetDlgItem, GetClassName
from win32file import GetFileAttributes
from random import randrange
from codecs import lookup
from codecs import open as openFile
from winsound import PlaySound, SND_ASYNC
from sys import getfilesystemencoding
fse = getfilesystemencoding()

WM_COMMAND            = 273
WM_SYSCOMMAND         = 274
TBM_GETPOS            = 1024
TBM_SETPOS            = 1029
SC_RESTORE            = 61728
SW_RESTORE            = 9
GW_CHILD              = 5
GW_HWNDNEXT           = 2
FILE_ATTRIBUTE_HIDDEN = 2
FILE_ATTRIBUTE_SYSTEM = 4
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
    cmdLine = 'Commandline: %s'
    cancAndDel = 'Schedule "%s" canceled and deleted'
    cancAndDis = 'Schedule "%s" canceled (disabled)'
    newSched = 'Schedule "%s" scheduled. Next run: %s'
    re_Sched = 'Schedule "%s" re-scheduled. New next run: %s'
    start = 'RadioSure plugin started. All valid schedules will be scheduled:'
    stop = 'RadioSure plugin stoped. All scheduled schedules will be canceled:'
    canc = 'Schedule "%s" canceled'
    launched = "Schedule.Launched"
    holidButton = "Public holidays ..."
    managerButton = "Show scheduler"
    fixBoxLabel = "Fixed public holidays:"
    varBoxLabel = "Variable public holidays:"
    ok = "OK"
    cancel = "Cancel"
    add = "Add"
    delete = "Delete"
    first_day = "The first day of the week:"
    xmlComment = "Radio?Sure! scheduler configuration file. Updated at %s."


    class OpenScheduler:
        dialogTitle = "Radio?Sure! Scheduler %s  (plugin for EventGhost)"
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
            "Monthly / weekday",
            "Monthly / day",
            "Periodically",
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
            "Apply"
        )
        type_label = "Schedule type:"
        source = "Source URL:"
        favorite = "Favorite station title:"
        filename = "Destination file name (optional):"
        chooseDay = "Choose day"
        theEvery = "The every"
        yearly = "Every year on the same day"
        chooseTime = "Choose start time and duration (00:00 = constantly)"
        choosePeriod = "Choose period"
        andThenEvery = "Repeat every"
        units = (
            "hours",
            "days",
            "weeks",
            "months",
            "years",
        )
        start = "Start time (HH:MM:SS):"
        length = "Duration (HH:MM):"
        boxTitle = "Your setup is not properly configured !"
        boxTexts = (
            "Schedule title must not be an empty string !",
            "Schedule title must be unique !",
            'Determine the source URL, or set the mode "Do nothing" !',
            'Not allowed to set "Do nothing" while also "None" event !',
            'Must be chosen Schedule type !',
            "The span must be shorter than the period !",
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
        holidCheck_1 = "Do not trigger events for a chosen day if it happens to be a holiday"
        holidCheck_2 = "Do also trigger events for a non-chosen day if it happens to be a holiday"
        popup = (
            "Add schedule",
            "Duplicate schedule",
            "Delete schedule",
            "Enable all schedules",
            "Disable all schedules",
            "Move schedule up",
            "Move schedule down",
        )

#===============================================================================

class MyDirBrowseButton(eg.DirBrowseButton):
    def GetTextCtrl(self):          #  now I can make build-in textCtrl
        return self.textControl     #  non-editable !!!
#===============================================================================

class MyFileBrowseButton(eg.FileBrowseButton):
    def GetTextCtrl(self):          #  now I can make build-in textCtrl
        return self.textControl     #  non-editable !!!
#===============================================================================

class MySpinIntCtrl(eg.SpinIntCtrl):

    def SetNumCtrlId(self, id):
        self.numCtrl.SetId(id)
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

newEVT_UPDATE_DIALOG = wx.NewEventType()
EVT_UPDATE_DIALOG = wx.PyEventBinder(newEVT_UPDATE_DIALOG, 1)
#===============================================================================

newEVT_CHECKLISTCTRL = wx.NewEventType()
EVT_CHECKLISTCTRL = wx.PyEventBinder(newEVT_CHECKLISTCTRL, 1)

class Evt_ChecklistCtrl(wx.PyCommandEvent):

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
        h=self.GetCharHeight() + 4
        for i in range(len(self.choices)):
            self.stationChoiceCtrl.SetCellValue(i, 0, self.choices[i][1])
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

class HolidaysFrame(wx.Dialog):
    fixWin = None
    varWin = None
    fixHolidays = []
    varHolidays = []

    def __init__(self, parent, plugin):
        self.plugin = plugin
        wx.Dialog.__init__(
            self,
            parent,
            -1,
            style = wx.DEFAULT_DIALOG_STYLE,
            name = self.plugin.text.holidButton
        )
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.panel = parent
        self.fixHolidays, self.varHolidays = cpy(self.panel.holidays)
        self.Bind(wxCal.EVT_CALENDAR_DAY, self.OnChangeDay)


    def ShowHolidaysFrame(self):
        text = self.plugin.text
        self.SetTitle(self.plugin.text.holidButton)
        self.fixWin = CalendarPopup(self, False, self.plugin.first_day)
        self.varWin = CalendarPopup(self, True, self.plugin.first_day)
        calW, calH = self.fixWin.GetWinSize()
        fixLbl = wx.StaticText(self, -1, text.fixBoxLabel)
        variableLbl = wx.StaticText(self, -1, text.varBoxLabel)
        widthList = [self.GetTextExtent("30. %s 2000" % month)[0] +
            SYS_VSCROLL_X for month in list(month_name)]
        widthList.append(fixLbl.GetSize()[0])
        widthList.append(variableLbl.GetSize()[0])
        w = max(widthList) + 5
        self.SetMinSize((w + calW + 30, 2 * calH + 128))
        self.fixListBox = HolidaysBox(
            self,
            -1,
            size = wx.Size(w, 130),
            style = wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        self.fix_add_Btn = wx.Button(self, -1, text.add)
        self.fix_del_Btn = wx.Button(self, -1, text.delete)
        self.fix_del_Btn.Enable(False)
        self.varListBox = HolidaysBox(
            self,
            -1,
            size = wx.Size(w, 130),
            style = wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        self.var_add_Btn = wx.Button(self, -1, text.add)
        self.var_del_Btn = wx.Button(self, -1, text.delete)
        self.var_del_Btn.Enable(False)
        line = wx.StaticLine(self, -1, style = wx.LI_HORIZONTAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        fixSizer = wx.GridBagSizer(2, 8)
        fixSizer.SetMinSize((w + 8 + calW, -1))
        varSizer = wx.GridBagSizer(2, 8)
        varSizer.SetMinSize((w + 8 + calW, -1))
        fixSizer.Add(fixLbl, (0, 0))
        fixSizer.Add(self.fixListBox, (1, 0), (3, 1))
        fixSizer.Add(self.fix_add_Btn, (1, 1))
        fixSizer.Add((-1, 15), (2, 1))
        fixSizer.Add(self.fix_del_Btn, (3, 1))
        varSizer.Add(variableLbl, (0, 0))
        varSizer.Add(self.varListBox, (1, 0), (3,1))
        varSizer.Add(self.var_add_Btn, (1, 1))
        varSizer.Add((-1, 15), (2, 1))
        varSizer.Add(self.var_del_Btn, (3, 1))
        sizer.Add(fixSizer, 0, wx.EXPAND|wx.ALL, 8)
        sizer.Add((-1, 12))
        sizer.Add(varSizer, 0, wx.EXPAND|wx.ALL, 8)
        sizer.Add((1, 16))
        btn1 = wx.Button(self, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn1.SetDefault()
        btn2 = wx.Button(self, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add(line, 0, wx.EXPAND)
        sizer.Add((1,5))
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        sz = self.GetMinSize()
        self.SetSize(sz)
        self.fixListBox.Reset(self.fixHolidays)
        self.varListBox.Reset(self.varHolidays)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        btn2.Bind(wx.EVT_BUTTON, self.onCancel)
        btn1.Bind(wx.EVT_BUTTON, self.onOK)
        self.fix_add_Btn.Bind(wx.EVT_BUTTON, self.onFixAddBtn)
        self.var_add_Btn.Bind(wx.EVT_BUTTON, self.onVarAddBtn)
        self.fix_del_Btn.Bind(wx.EVT_BUTTON, self.onFixDelBtn)
        self.var_del_Btn.Bind(wx.EVT_BUTTON, self.onVarDelBtn)
        self.Bind(wx.EVT_LISTBOX, self.onHolBoxSel)
        sizer.Layout()
        self.SetSizer(sizer)
        self.MakeModal(True)
        self.Show(True)


    def onClose(self, evt):
        self.MakeModal(False)
        self.GetParent().GetParent().Raise()
        self.Destroy()


    def onCancel(self, evt):
        self.Close()


    def onOK(self, evt):
        self.panel.holidays = (self.fixHolidays, self.varHolidays)
        self.Close()


    def onHolBoxSel(self, evt):
        if  evt.GetId() == self.fixListBox.GetId():
            self.fix_del_Btn.Enable(True)
        else:
            self.var_del_Btn.Enable(True)
        evt.Skip()


    def onFixAddBtn(self, evt):
        pos = self.ClientToScreen(self.fix_add_Btn.GetPosition())
        self.fixWin.PopUp(pos, self.fixHolidays)


    def onVarAddBtn(self, evt):
        pos = self.ClientToScreen(self.var_add_Btn.GetPosition())
        self.varWin.PopUp(pos, self.varHolidays)


    def onFixDelBtn(self, evt):
        self.fixHolidays.pop(self.fixListBox.GetSelection())
        if self.fixListBox.Reset(self.fixHolidays):
            self.fix_del_Btn.Enable(False)


    def onVarDelBtn(self, evt):
        self.varHolidays.pop(self.varListBox.GetSelection())
        if self.varListBox.Reset(self.varHolidays):
            self.var_del_Btn.Enable(False)


    def OnChangeDay(self, evt):
        if evt.GetId() == self.fixWin.GetCalId():
            self.fixListBox.Reset(self.fixHolidays)
        else:
            self.varListBox.Reset(self.varHolidays)
        evt.Skip()
#===============================================================================

class HolidaysBox(wx.ListBox):

    def __init__ (self, parent, id, size, style):
        wx.ListBox.__init__(
            self,
            parent = parent,
            id = id,
            size = size,
            style = style
        )
        self.sel = -1
        self.Bind(wx.EVT_LISTBOX, self.onHolBoxSel)


    def Reset(self, list):
        tmpList = []
        for item in list:
            day = item[-1]
            day = "  %i" % day if day < 10 else "%i" % day
            if len(item) == 2:
                tmpList.append("%s. %s" % (day, month_name[item[0]]))
            else:
                tmpList.append("%s. %s %i" % (day, month_name[item[1]], item[0]))
        self.Set(tmpList)
        if self.sel > -1 and self.sel < self.GetCount():
            self.SetSelection(self.sel)
            return False
        else:
            return True


    def  onHolBoxSel(self, evt):
        self.sel = evt.GetSelection()
        evt.Skip()
#===============================================================================

class CalendarPopup(wx.PopupWindow):
    yearChange = True

    def __init__(self, parent, yearChange, first_day):
        self.yearChange = yearChange
        wx.PopupWindow.__init__(self, parent)
        startDate = wx.DateTime()
        startDate.Set(1, 0)
        self.cal = wxCal.CalendarCtrl(
            self,
            -1,
            startDate,
            style = (wxCal.CAL_MONDAY_FIRST, wxCal.CAL_SUNDAY_FIRST)[first_day]
                | wxCal.CAL_SHOW_HOLIDAYS
                | wxCal.CAL_SEQUENTIAL_MONTH_SELECTION
                | wxCal.CAL_SHOW_SURROUNDING_WEEKS 
        )
        self.cal.EnableYearChange(yearChange)
        sz = self.cal.GetBestSize()
        self.SetSize(sz)
        self.cal.Bind(wxCal.EVT_CALENDAR_DAY, self.OnChangeDay)
        self.cal.Bind(wxCal.EVT_CALENDAR_MONTH, self.OnChangeMonth)
        self.cal.Bind(wxCal.EVT_CALENDAR_YEAR, self.OnChangeMonth)
        self.cal.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)


    def OnLeaveWindow(self, evt):
        self.PopDown()
        evt.Skip()


    def GetCalId(self):
        return self.cal.GetId()


    def GetWinSize(self):
        return self.GetSize()


    def OnChangeDay(self, evt):
        date = evt.GetDate()
        day, month, year = date.GetDay(), 1 + date.GetMonth(), date.GetYear()
        newHoliday = (year, month, day) if self.yearChange else (month, day)
        if not newHoliday in self.holidays:
            self.holidays.append(newHoliday)
            self.holidays.sort()
        date = self.cal.GetDate()
        self.cal.SetHoliday(day)
        date.AddDS(wx.DateSpan.Day())
        self.cal.SetDate(date)
        self.Refresh()
        evt.Skip()


    def OnChangeMonth(self, evt = None):
        date = self.cal.GetDate()
        cur_month = date.GetMonth() + 1   # convert wx.DateTime 0-11 => 1-12
        if self.yearChange:
            cur_year = date.GetYear()
            for year, month, day in self.holidays:
                if year == cur_year and month == cur_month:
                    self.cal.SetHoliday(day)
        else:
            for month, day in self.holidays:
                if month == cur_month:
                    self.cal.SetHoliday(day)


    def PopUp(self, position, holidays):
        self.cal.EnableHolidayDisplay(False)
        self.cal.EnableHolidayDisplay(True)
        self.SetPosition(position)
        self.holidays = holidays
        self.OnChangeMonth()
        self.Show(True)


    def PopDown(self):
        self.Show(False)
        self.Close()
#===============================================================================

class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin):

    def __init__(self, parent, text, width):
        wx.ListCtrl.__init__(
            self,
            parent,
            -1,
            size = (width, 164),
            style = wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|wx.LC_SINGLE_SEL
        )
        curString = (
            "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAADAFBMVEX/AAAAAAAUFBQV"
            "FRUWFhYTExMCAgI1NTXp6ekEBAQzMzPV1dWPj4+goKCAgIAbGxsBAQHa2tq4uLi/v7/C"
            "wsLBwcG8vLy6uro5OTkNDQ0QEBAHBwcFBQXR0dFra2s9PT0oKCgGBgYXFxdsbGxLS0t0"
            "dHQyMjJhYWFOTk5SUlJWVlYqKirGxsb8/PylpaUrKyudnZ2kpKTHx8e7urp6enrX19fP"
            "z8+RkZEiJCRfX18REREtLS2EhISXl5dERERVVVVZWVkdHR1/gYE0NDSUlJQaGhoYGBgZ"
            "GRkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA5GIQAACQAAAAAAAAA"
            "AAAAAAAAAAAAADQAABNBfeQAAAAAAAA5GLg5GLgAACQAAAAAAAAAAAAAAAAAAAAAAGgA"
            "ABNBfeQAAAAAAAA5GOw5GOwAACQAAAAAAAAAAAAAABAAAAAAANAAABNBfeQAAAAAAABh"
            "FgiPH4AAJtwAAAAAAAAAAAAAAAAAAIAAAAA5ELy/IqwAAGgAAAA/6bw5AjwAAFgAAAAA"
            "AAAAAAAAAAAAAAAAAAA5EpBmS+wAADQAAAA5GYg5GYgAACQAAAAAAAAAAAAAAAAAAAAA"
            "AWwAABNBfeQAAAAAAABhFgiPH4AAJkAAAAAAAAAAAAAAAACAAAAAAABhFgiPH4AAJhwA"
            "AABhFgiPH4AAJgwAAAAAAAAAAAAAAAAAgAAAAABhFgiPH4AAJegAAAA5GiQ5GiQAASgA"
            "AAAAAAACAAAAAAAAAAAAAAA5E8g5E8gAAQQAAAA5Glg5GlgAACQAAAAAAAAAAAAAAAAA"
            "AAAAADQAABNBfeQAAAAAAAA5Gow5GowAAIwAAAAAAAAAAAAAAAAAAAAAAADJSBkDAAAA"
            "AXRSTlMAQObYZgAAAAlwSFlzAAABiQAAAYkBni4RNQAAAP1JREFUeNqF09lWwjAQBuD5"
            "KVZZBJcCUmQpICrKJiooixuW938jmLZJKZQzc9E2ydeZJCchEgMikAQkAUlAEpAEJAFJ"
            "QBKQBCQBSUAS2BNIGEkvDCN5ggMAMiN/xyzTpFPVc6ZBih9pBTLZcy9yYQbKhykuLq+u"
            "LauwjWLJCkDAbtSky7C5XVFD3H2rUwBVKteUJX0mGdSDjzQacBw0IxujF+K02i3QHTr3"
            "D4/d3Z1j8LR9237WZ1AveuQZ9D0w4FRDvQ8qRkHDppcxXt+yeJ/EXxouMf349Mfiwcyb"
            "73y/RAgWy6/vzs8v/o6X4NWujpUw/10Ow3XX64R4s4k2SJ0PWZEnDEUAAAAASUVORK5C"
            "YII="
        )

        from cStringIO import StringIO
        from base64 import b64decode
        from Image import open as openImage
        stream = StringIO(b64decode(curString))
        pil = openImage(stream).convert("RGBA")
        stream.close()
        bmp = wx.BitmapFromBufferRGBA(pil.size[0],pil.size[1],pil.tostring())
        img = bmp.ConvertToImage()
        img.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 1)
        img.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 1)
        cursor = wx.CursorFromImage(img)
        self.SetCursor(cursor)
        self.selRow = -1
        self.back = self.GetBackgroundColour()
        self.fore = self.GetForegroundColour()
        self.selBack = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.selFore = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        for i in range(len(text.header)):
            self.InsertColumn(i, text.header[i])
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        self.SetColumnWidth(
            1,
            width - self.GetColumnWidth(0) - 2 * 116 - SYS_VSCROLL_X - self.GetWindowBorderSize()[0]
        )
        self.SetColumnWidth(2, 116)
        self.SetColumnWidth(3, 116)
        CheckListCtrlMixin.__init__(self)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)

    def OnItemSelected(self, evt):
        self.SelRow(evt.m_itemIndex)
        evt.Skip()


    # this is called by the base class when an item is checked/unchecked !!!!!!!
    def OnCheckItem(self, index, flag):
        evt = Evt_ChecklistCtrl(newEVT_CHECKLISTCTRL, self.GetId())
        evt.SetValue((index, flag))
        self.GetEventHandler().ProcessEvent(evt)


    def SelRow(self, row):
        if row != self.selRow:
            if self.selRow in range(self.GetItemCount()):
                item = self.GetItem(self.selRow)
                item.SetTextColour(self.fore)
                item.SetBackgroundColour(self.back)
                self.SetItem(item)
            self.selRow = row
        if self.GetItemBackgroundColour(row) != self.selBack:
            item = self.GetItem(row)
            item.SetTextColour(self.selFore)
            item.SetBackgroundColour(self.selBack)
            self.SetItem(item)
            self.SetItemState(row, 0, wx.LIST_STATE_SELECTED)


    def AppendRow(self):
        ix = self.GetItemCount()
        self.InsertStringItem(ix, "")
        self.CheckItem(ix)
        self.EnsureVisible(ix)
        self.SelRow(ix)
#===============================================================================

class schedulerDialog(wx.Dialog):
    lastRow = -1
    applyBttn = None

    def __init__(self, text, plugin):
        wx.Dialog.__init__(
            self,
            None,
            -1,
            text.dialogTitle % version,
            style = wx.DEFAULT_DIALOG_STYLE|wx.MINIMIZE_BOX|wx.CLOSE_BOX,
        )

        #import locale as l
        #l.setlocale(l.LC_ALL, "us") # only for testing

        bttns = []
        self.ctrls=[]
        self.plugin = plugin
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.plugin.dialog = self
        self.tmpData = self.plugin.tmpData = cpy(self.plugin.data)
        self.text = text

        def fillDynamicSizer(type, data = None, old_type = 255):
            flag = old_type != type
            if flag:
                dynamicSizer.Clear(True)
                self.ctrls=[]
                self.ctrls.append(wx.NewId())
                self.ctrls.append(wx.NewId())
            if type == -1:
                return
            if type != 1 and flag:
                topSizer = wx.StaticBoxSizer(
                    wx.StaticBox(self, -1, self.text.chooseDay),
                    wx.HORIZONTAL
                )
            if type == 0:
                if flag:
                    self.ctrls.append(wx.NewId())
                    dp = wx.DatePickerCtrl(self, self.ctrls[2], size = (86, -1),
                            style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
                    topSizer.Add(dp,0,wx.EXPAND)
                    self.ctrls.append(wx.NewId())
                    yearlyCtrl = wx.CheckBox(self, self.ctrls[3], self.text.yearly)
                    topSizer.Add(yearlyCtrl, 0, wx.EXPAND|wx.LEFT, 30)
                    dynamicSizer.Add(topSizer, 0, wx.EXPAND|wx.TOP, 2)
                else:
                    dp = wx.FindWindowById(self.ctrls[2])
                    yearlyCtrl = wx.FindWindowById(self.ctrls[3])
                if data:
                    if not data[2]:
                        val = wx.DateTime_Now()
                        data[2] = str(dt.now())[:10]
                    wxDttm = wx.DateTime()
                    wxDttm.Set(
                        int(data[2][8:10]),
                        int(data[2][5:7]) - 1,
                        int(data[2][:4])
                    )
                    dp.SetValue(wxDttm)
                    yearlyCtrl.SetValue(data[3])
            elif type == 2:
                if flag:
                    if self.plugin.first_day:
                        choices = list(day_name)[:-1]
                        choices.insert(0, list(day_name)[-1])
                    else:
                        choices = list(day_name)
                    self.ctrls.append(wx.NewId())
                    weekdayCtrl = wx.CheckListBox(
                        self,
                        self.ctrls[2],
                        choices = choices,
                        size=((-1,110)),
                    )
                    self.ctrls.append(wx.NewId())
                    holidCheck_2 = wx.CheckBox(
                        self,
                        self.ctrls[3],
                        self.text.holidCheck_2
                    )
                    self.ctrls.append(wx.NewId())
                    holidCheck_1 = wx.CheckBox(
                        self,
                        self.ctrls[4],
                        self.text.holidCheck_1
                    )
                    topSizer.Add((40,1), 0, wx.ALIGN_CENTER)
                    topSizer.Add(
                        wx.StaticText(
                            self,
                            -1,
                            self.text.theEvery
                        ),
                        0,
                        wx.ALIGN_CENTER | wx.RIGHT, 10
                    )
                    topSizer.Add(weekdayCtrl, 0, wx.TOP)
                    dynamicSizer.Add(topSizer, 0, wx.EXPAND | wx.TOP,2)
                    dynamicSizer.Add(holidCheck_1, 0, wx.TOP, 2)
                    dynamicSizer.Add(holidCheck_2, 0, wx.TOP, 2)
                else:
                    weekdayCtrl = wx.FindWindowById(self.ctrls[2])
                    holidCheck_2 = wx.FindWindowById(self.ctrls[3])
                    holidCheck_1 = wx.FindWindowById(self.ctrls[4])
                val = 127 if not data else data[2]
                if self.plugin.first_day:
                    exp = [6, 0, 1, 2, 3, 4, 5]
                else:
                    exp = [0, 1, 2, 3, 4, 5, 6]
                for i in range(7):
                    weekdayCtrl.Check(i, bool(val & (2 ** exp[i])))
                enable = val & 31 and not val & 96
                holidCheck_1.Enable(enable)
                check = 0 if (not data or not enable) else data[4]
                holidCheck_1.SetValue(check)
                enable = val & 96 and not val & 31
                holidCheck_2.Enable(enable)
                check = 0 if (not data or not enable) else data[3]
                holidCheck_2.SetValue(check)
            elif type == 3: # Monthly/weekday ...
                if flag:
                    dateSizer = wx.BoxSizer(wx.HORIZONTAL)
                    dateSizer.Add(
                        wx.StaticText(
                            self,
                            -1,
                            self.text.the
                        ),
                        0,
                        wx.ALIGN_CENTER
                    )
                    topSizer.Add(dateSizer, 0, wx.EXPAND)
                    dynamicSizer.Add(topSizer, 0, wx.EXPAND | wx.TOP,2)
                    self.ctrls.append(wx.NewId())
                    serialCtrl = wx.CheckListBox(
                        self,
                        self.ctrls[2],
                        choices = self.text.serial_num,
                        size = ((-1, 95)),
                    )
                    dateSizer.Add(serialCtrl, 0, wx.ALIGN_CENTER | wx.LEFT, 10)
                    if self.plugin.first_day:
                        choices = list(day_name)[0:-1]
                        choices.insert(0, list(day_name)[-1])
                    else:
                        choices = list(day_name)
                    self.ctrls.append(wx.NewId())
                    weekdayCtrl = wx.CheckListBox(
                        self,
                        self.ctrls[3],
                        choices = choices,
                        size = ((-1, 110)),
                    )
                    dateSizer.Add(weekdayCtrl, 0, wx.ALIGN_CENTER | wx.LEFT, 10)
                    dateSizer.Add(
                        wx.StaticText(
                            self,
                            -1,
                            self.text.in_
                        ),
                        0,
                        wx.ALIGN_CENTER | wx.LEFT, 10
                    )
                    self.ctrls.append(wx.NewId())
                    monthsCtrl_1 = wx.CheckListBox(
                        self,
                        self.ctrls[4],
                        choices = list(month_name)[1:7],
                        size = ((-1, 95)),
                    )
                    dateSizer.Add(monthsCtrl_1, 0, wx.ALIGN_CENTER | wx.LEFT, 10)
                    self.ctrls.append(wx.NewId())
                    monthsCtrl_2 = wx.CheckListBox(
                        self,
                        self.ctrls[5],
                        choices = list(month_name)[7:],
                        size = ((-1, 95)),
                    )
                    dateSizer.Add(monthsCtrl_2, 0, wx.ALIGN_CENTER | wx.LEFT, -1)
                    self.ctrls.append(wx.NewId())
                    holidCheck_1 = wx.CheckBox(
                        self,
                        self.ctrls[6],
                        self.text.holidCheck_1
                    )
                    dynamicSizer.Add(holidCheck_1, 0, wx.TOP, 2)
                else:
                    serialCtrl = wx.FindWindowById(self.ctrls[2])
                    weekdayCtrl = wx.FindWindowById(self.ctrls[3])
                    monthsCtrl_1 = wx.FindWindowById(self.ctrls[4])
                    monthsCtrl_2 = wx.FindWindowById(self.ctrls[5])
                    holidCheck_1 = wx.FindWindowById(self.ctrls[6])
                val = 0 if not data else data[2]
                for i in range(6):
                    serialCtrl.Check(i, bool(val & (2 ** i)))
                val = 0 if not data else data[3]
                if self.plugin.first_day:
                    exp = [6, 0, 1, 2, 3, 4, 5]
                else:
                    exp = [0, 1, 2, 3, 4, 5, 6]
                for i in range(7):
                    weekdayCtrl.Check(i, bool(val & (2 ** exp[i])))
                enable = val & 31 and not val & 96
                holidCheck_1.Enable(enable)
                val = 63 if not data else data[4]
                for i in range(6):
                    monthsCtrl_1.Check(i, bool(val & (2 ** i)))
                val = 63 if not data else data[5]
                for i in range(6):
                    monthsCtrl_2.Check(i, bool(val & (2 ** i)))
                check = 0 if (not data or not enable) else data[6]
                holidCheck_1.SetValue(check)
            elif type == 4: # Monthly/day ...
                if flag:
                    dateSizer = wx.BoxSizer(wx.HORIZONTAL)
                    topSizer.Add(dateSizer, 0, wx.EXPAND)
                    dynamicSizer.Add(topSizer, 0, wx.EXPAND | wx.TOP, 2)
                    self.ctrls.append(wx.NewId())
                    q_1_Ctrl = wx.CheckListBox(
                        self,
                        self.ctrls[2],
                        choices = [str(i) + '.' for i in range(1, 9)],
                        size = ((40, 125)),
                    )
                    dateSizer.Add(q_1_Ctrl, 0, wx.LEFT, 5)
                    self.ctrls.append(wx.NewId())
                    q_2_Ctrl = wx.CheckListBox(
                        self,
                        self.ctrls[3],
                        choices = [str(i) + '.' for i in range(9, 17)],
                        size = ((46, 125)),
                    )
                    dateSizer.Add(q_2_Ctrl, 0, wx.LEFT, -1)
                    self.ctrls.append(wx.NewId())
                    q_3_Ctrl = wx.CheckListBox(
                        self,
                        self.ctrls[4],
                        choices = [str(i) + '.' for i in range(17, 25)],
                        size = ((46, 125)),
                    )
                    dateSizer.Add(q_3_Ctrl, 0, wx.LEFT, -1)
                    self.ctrls.append(wx.NewId())
                    q_4_Ctrl = wx.CheckListBox(
                        self,
                        self.ctrls[5],
                        choices = [str(i) + '.' for i in range(25, 32)],
                        size = ((46, 125)),
                    )
                    dateSizer.Add(q_4_Ctrl, 0, wx.LEFT, -1)
                    dateSizer.Add((-1, 1), 1, wx.EXPAND)
                    self.ctrls.append(wx.NewId())
                    monthsCtrl_1 = wx.CheckListBox(
                        self,
                        self.ctrls[6],
                        choices = list(month_name)[1:7],
                        size = ((-1, 95)),
                    )
                    dateSizer.Add(monthsCtrl_1, 0, wx.ALIGN_CENTER | wx.LEFT, 10)
                    self.ctrls.append(wx.NewId())
                    monthsCtrl_2 = wx.CheckListBox(
                        self,
                        self.ctrls[7],
                        choices = list(month_name)[7:],
                        size = ((-1, 95)),
                    )
                    dateSizer.Add(monthsCtrl_2, 0, wx.ALIGN_CENTER | wx.LEFT, -1)
                    dateSizer.Add((5, 1), 0)
                else:
                    q_1_Ctrl = wx.FindWindowById(self.ctrls[2])
                    q_2_Ctrl = wx.FindWindowById(self.ctrls[3])
                    q_3_Ctrl = wx.FindWindowById(self.ctrls[4])
                    q_4_Ctrl = wx.FindWindowById(self.ctrls[5])
                    monthsCtrl_1 = wx.FindWindowById(self.ctrls[6])
                    monthsCtrl_2 = wx.FindWindowById(self.ctrls[7])
                val = 0 if not data else data[2]
                for i in range(8):
                    q_1_Ctrl.Check(i, bool(val & (2 ** i)))
                val = 0 if not data else data[3]
                for i in range(8):
                    q_2_Ctrl.Check(i, bool(val & (2 ** i)))
                val = 0 if not data else data[4]
                for i in range(8):
                    q_3_Ctrl.Check(i, bool(val & (2 ** i)))
                val = 0 if not data else data[5]
                for i in range(7):
                    q_4_Ctrl.Check(i, bool(val & (2 ** i)))
                val = 63 if not data else data[6]
                for i in range(6):
                    monthsCtrl_1.Check(i, bool(val & (2 ** i)))
                val = 63 if not data else data[7]
                for i in range(6):
                    monthsCtrl_2.Check(i, bool(val & (2 ** i)))
            elif type == 5:
                if flag:
                    self.ctrls.append(wx.NewId())
                    dp = wx.DatePickerCtrl(self, self.ctrls[2], size = (86, -1),
                            style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
                    topSizer.Add(dp, 0, wx.EXPAND)
                    dynamicSizer.Add(topSizer, 0, wx.EXPAND | wx.TOP, 2)
                else:
                    dp = wx.FindWindowById(self.ctrls[2])
                if data:
                    if not data[2]:
                        val = wx.DateTime_Now()
                        data[2] = str(dt.now())[:10]
                    wxDttm = wx.DateTime()
                    wxDttm.Set(
                        int(data[2][8:10]),
                        int(data[2][5:7])-1,
                        int(data[2][:4])
                    )
                    dp.SetValue(wxDttm)
            #elif type == 1: # daily
            #    pass
            if flag:
                timeSizer = wx.GridBagSizer(0, 0)
                bottomSizer = wx.StaticBoxSizer(
                    wx.StaticBox(self, -1, self.text.chooseTime6 if type == 6 else self.text.chooseTime),
                    wx.HORIZONTAL
                )
                dynamicSizer.Add(bottomSizer, 0, wx.EXPAND | wx.TOP, 16 if type != 2 else 5)
                bottomSizer.Add(timeSizer, 0, wx.EXPAND)
                stEvLbl = wx.StaticText(self, -1, self.text.start)
                timeSizer.Add(stEvLbl, (0, 0), (1, 2))
                durLabel = wx.StaticText(self, -1, self.text.length)
                timeSizer.Add(durLabel, (0, 3), (1, 2))
                spinBtn = wx.SpinButton(
                    self,
                    -1,
                    wx.DefaultPosition,
                    (-1, 22),
                    wx.SP_VERTICAL
                )
                initTime = wx.DateTime_Now()
                initTime.SetSecond(0)
                initTime.AddTS(wx.TimeSpan.Minute())
                val = data[0] if data and data[0] else initTime
                timeCtrl = eg.TimeCtrl(
                    self, 
                    self.ctrls[0],
                    val,
                    fmt24hr = True,
                    spinButton = spinBtn
                )
                timeSizer.Add(timeCtrl, (1, 0), (1, 1))
                timeSizer.Add(spinBtn, (1, 1), (1, 1))
                timeSizer.Add((40, -1), (1, 2), (1, 1))
                spinBtn2 = wx.SpinButton(
                    self,
                    -1,
                    wx.DefaultPosition,
                    (-1, 22),
                    wx.SP_VERTICAL
                )
                val = data[1] if data and data[1] else "00:00"
                lenCtrl = eg.TimeCtrl_Duration(
                    self,
                    self.ctrls[1],
                    val,
                    fmt24hr = True,
                    spinButton = spinBtn2,
                    displaySeconds = False
                )
                timeSizer.Add(lenCtrl, (1, 3), (1, 1))
                timeSizer.Add(spinBtn2, (1, 4), (1, 1))
                bottomSizer.Add((-1,-1), 1, wx.EXPAND)
                testBttn = wx.Button(
                    self,
                    -1 if len(bttns) == 0 else bttns[-1],
                    self.text.testButton
                )
                bottomSizer.Add(testBttn, 0, wx.EXPAND | wx.RIGHT)
            else:
                timeCtrl = wx.FindWindowById(self.ctrls[0])
                val = data[0] if data and data[0] else wx.DateTime_Now()
                timeCtrl.SetValue(val)
                lenCtrl = wx.FindWindowById(self.ctrls[1])
                val = data[1] if data and data[1] else "00:00"
                lenCtrl.SetValue(val)
            if type == 5: #periodically
                if flag:
                    bottomSizer = wx.StaticBoxSizer(
                        wx.StaticBox(self, -1, self.text.choosePeriod),
                        wx.HORIZONTAL
                    )
                    self.ctrls.append(wx.NewId())
                    numCtrl = MySpinIntCtrl(self, -1, value = 1, min = 1)
                    numCtrl.SetNumCtrlId(self.ctrls[3])
                    bottomSizer.Add(
                        wx.StaticText(
                            self,
                            -1,
                            self.text.andThenEvery
                        ),
                        0,
                        wx.ALIGN_CENTER
                    )
                    bottomSizer.Add(numCtrl, 0, wx.LEFT, 4)
                    self.ctrls.append(wx.NewId())
                    unitCtrl = wx.Choice(
                        self,
                        self.ctrls[4],
                        choices = self.text.units
                    )
                    bottomSizer.Add(unitCtrl, 0, wx.LEFT, 8)
                    dynamicSizer.Add(bottomSizer, 0, wx.EXPAND|wx.TOP, 16)
                    dynamicSizer.Layout()
                else:
                    numCtrl = wx.FindWindowById(self.ctrls[3])
                    unitCtrl = wx.FindWindowById(self.ctrls[4])
                if data:
                    numCtrl.SetValue(str(data[3]))
                    unitCtrl.SetSelection(data[4])
            elif flag:
                dynamicSizer.Layout()
            if type == 6:
                stEvLbl.Show(False)
                timeCtrl.Show(False)
                spinBtn.Show(False)
            return dynamicSizer.GetMinSize()[0]


        def Diff():
            applyBttn = wx.FindWindowById(bttns[5])
            flg = self.tmpData != self.plugin.data
            applyBttn.Enable(flg)        


        def onCheckListBox(evt):
            id = evt.GetId()
            sel = evt.GetSelection()
            box = self.FindWindowById(id)
            ix = self.ctrls.index(id)
            type = self.tmpData[self.lastRow][2]
            cond = (type == 2 and ix == 2) or (type == 3 and ix == 3)
            if cond and self.plugin.first_day:
                exp = (6, 0, 1, 2, 3, 4, 5)[sel]
            else:
                exp = sel
            if box.IsChecked(sel):
                self.tmpData[self.lastRow][3][ix] |= 2 ** exp
            else:
                self.tmpData[self.lastRow][3][ix] &= 255 - 2 ** exp
            if cond:
                holidCheck_1 = wx.FindWindowById(self.ctrls[-1])
                val = self.tmpData[self.lastRow][3][ix]
                flg = val & 31 and not val & 96
                holidCheck_1.Enable(flg)
                if not flg:
                    holidCheck_1.SetValue(0)
                    self.tmpData[self.lastRow][3][-1] = 0
                if type == 2:
                    holidCheck_2 = wx.FindWindowById(self.ctrls[3])
                    val = self.tmpData[self.lastRow][3][2]
                    flg = val & 96 and not val & 31
                    holidCheck_2.Enable(flg)
                    if not flg:
                        holidCheck_2.SetValue(0)
                        self.tmpData[self.lastRow][3][3] = 0
            next = self.plugin.NextRun(
                self.tmpData[self.lastRow][2],
                self.tmpData[self.lastRow][3]
            )
            grid.SetStringItem(self.lastRow, 3, next)
            Diff()


        def OnTimeChange(evt):
            ix = self.ctrls.index(evt.GetId())
            self.tmpData[self.lastRow][3][ix] = evt.GetValue()
            next = self.plugin.NextRun(
                self.tmpData[self.lastRow][2],
                self.tmpData[self.lastRow][3]
            )
            grid.SetStringItem(self.lastRow, 3, next)
            Diff()


        def onPeriodUnit(evt):
            if len(self.ctrls) == 5 and evt.GetId() == self.ctrls[4]:
                self.tmpData[self.lastRow][3][4] = evt.GetSelection()
                next = self.plugin.NextRun(
                    self.tmpData[self.lastRow][2],
                    self.tmpData[self.lastRow][3]
                )
                grid.SetStringItem(self.lastRow, 3, next)
            else:
                evt.Skip()
            Diff()


        def onDatePicker(evt):
            val = str(dt.fromtimestamp(evt.GetDate().GetTicks()))[:10]
            self.tmpData[self.lastRow][3][2] = val
            next = self.plugin.NextRun(
                self.tmpData[self.lastRow][2],
                self.tmpData[self.lastRow][3]
            )
            grid.SetStringItem(self.lastRow, 3, next)
            Diff()


        def onCheckBox(evt):
            val = evt.IsChecked()
            ix = self.ctrls.index(evt.GetId())
            if self.tmpData[self.lastRow][2] == 2 and ix == 3:
                self.tmpData[self.lastRow][3][3] = int(val)
            else:
                self.tmpData[self.lastRow][3][-1] = int(val)
            next = self.plugin.NextRun(
                self.tmpData[self.lastRow][2],
                self.tmpData[self.lastRow][3]
            )
            grid.SetStringItem(self.lastRow, 3, next)
            Diff()


        def OnUpdateDialog(evt):
            if self.lastRow == evt.GetId():
                OpenSchedule()


        def OnSelectCell(evt):
            self.lastRow = evt.m_itemIndex
            OpenSchedule()
            Diff()
            evt.Skip() # necessary !!!


        def enableBttns(value):
            for i in (1, 2):
                bttn = self.FindWindowById(bttns[i])
                bttn.Enable(value)
            Diff()


        def ShowMessageBox(mess):
            PlaySound('SystemExclamation', SND_ASYNC)
            MessageBox(
                self.GetHandle(),
                mess,
                self.text.boxTitle,
                    48
                )


        def FindNewTitle(title):
            tmpLst = []
            for item in self.tmpData:
                if item[1].startswith(title + " ("):
                    tmpLst.append(item[1][2 + len(title):])
            if len(tmpLst) == 0:
                return "%s (1)" % title
            tmpLst2 = []
            for item in tmpLst:
                if item[-1] == ")":
                    try:
                        tmpLst2.append(int(item[:-1]))
                    except:
                        pass
            if len(tmpLst2) == 0:
                return "%s (1)" % title
            else:
                return "%s (%i)" % (title, 1 + max(tmpLst2))


        def testValidity(data, test = False):
            mssgs = []
            tempDict = dict([(item[1].strip(), item[2]) for item in data])
            if "" in tempDict.iterkeys():
                mssgs.append(self.text.boxTexts[0])
            if not test and len(tempDict) < len(data):
                mssgs.append(self.text.boxTexts[1])
            if -1 in tempDict.itervalues():
                mssgs.append(self.text.boxTexts[4])
            for item in data:
                val = item[7]
                if (val & 6) == 6: # = Do nothing
                    if not val & 24:
                        if not self.text.boxTexts[3] in mssgs:
                            mssgs.append(self.text.boxTexts[3])
                else: # Not "Do nothing"
                    if not item[5]:
                        if not self.text.boxTexts[2] in mssgs:
                            mssgs.append(self.text.boxTexts[2])                    
                if item[2] == 5 and item[3][4] < 2:
                    period = item[3][3] * (3600, 86400)[item[3][4]]
                    span = 60 * int(item[3][1][3:]) + 3600 * int(item[3][1][:2])
                    if period <= span:
                        if self.text.boxTexts[5] not in mssgs:
                            mssgs.append(self.text.boxTexts[5])
            flag = len(mssgs) > 0
            if flag:
                ShowMessageBox("\n".join(mssgs))
            return flag


        def addSchedule(evt = None):
            empty = [1, "", -1, [], " ", "", "", 5]
            self.lastRow = len(self.tmpData)
            self.tmpData.append(empty)
            Tidy()
            grid.AppendRow()
            grid.SelRow(self.lastRow)
            if not self.lastRow:
                enableBttns(True)
                EnableCtrls(True)
            Diff()


        def duplSchedule(evt = None):
            lngth = len(self.tmpData)
            item = cpy(self.tmpData[self.lastRow])
            nxt = grid.GetItem(self.lastRow, 3).GetText()
            item[4] = ""
            self.lastRow = lngth
            self.tmpData.append(item)
            newTitle = FindNewTitle(self.tmpData[lngth][1])
            self.tmpData[lngth][1] = newTitle
            grid.AppendRow()
            grid.SelRow(lngth)
            grid.SetStringItem(lngth, 1, newTitle)
            grid.SetStringItem(lngth, 3, nxt)
            OpenSchedule()
            Diff()


        def delSchedule(evt = None):
            self.tmpData.pop(self.lastRow)
            grid.DeleteItem(self.lastRow)
            if len(self.tmpData) > 0:
                if self.lastRow == len(self.tmpData):
                    self.lastRow -= 1
                OpenSchedule()
                grid.SelRow(self.lastRow)
            else:
                self.lastRow = -1
                Tidy()
                EnableCtrls(False)
                enableBttns(False)
            Diff()


        def Move(direction):
            lst = cpy(self.tmpData)
            index = self.lastRow
            max = len(lst)-1
            #Last to first position, other down
            if index == max and direction == 1:
                self.tmpData[1:] = lst[:-1]
                self.tmpData[0] = lst[max]
                index2 = 0
            #First to last position, other up
            elif index == 0 and direction == -1:
                self.tmpData[:-1] = lst[1:]
                self.tmpData[max] = lst[0]
                index2 = max
            else:
                index2 = index + direction
                self.tmpData[index] = lst[index2]
                self.tmpData[index2] = lst[index]
            del lst
            return index2


        def moveUp(evt = None):
            newSel = Move(-1)
            fillGrid(False)
            self.grid.SelRow(newSel)
            Diff()


        def moveDown(evt = None):
            newSel = Move(1)
            fillGrid(False)
            self.grid.SelRow(newSel)
            Diff()


        def onButton(evt):
            id = evt.GetId()
            if id == bttns[0]:   # Add new
                addSchedule()
            elif id == bttns[1]: # Duplicate
                duplSchedule()
            elif id == bttns[2]: # Delete
                delSchedule()
            elif id == bttns[3]: # OK
                if testValidity(self.tmpData):
                    evt.Skip()
                    return
                self.plugin.data = cpy(self.tmpData)
                self.tmpData = []
                self.plugin.dataToXml()
                self.plugin.UpdateEGscheduler()
                self.Close()
            elif id == bttns[4]: # Cancel
                self.tmpData = []
                self.Close()
            elif id == bttns[5]: # Apply
                applyBttn = wx.FindWindowById(bttns[5])
                applyBttn.Enable(False)
                if testValidity(self.tmpData):
                    evt.Skip()
                    return
                self.plugin.data = cpy(self.tmpData)
                self.plugin.dataToXml()
                self.plugin.UpdateEGscheduler()
            evt.Skip()


        def EnableCtrls(value):
            typeChoice.Enable(value)
            schedulerName.Enable(value)
            name_label.Enable(value)
            type_label.Enable(value)
            favorite_label.Enable(value)
            workModeLbl.Enable(value)
            triggEvtLbl.Enable(value)
            windOpenLbl.Enable(value)
            source_label.Enable(value)
            filename_label.Enable(value)
            favChoice.Enable(value)
            sourceCtrl.Enable(value)
            recordCtrl.Enable(value)
            workModeCtrl.Enable(value)
            triggEvtCtrl.Enable(value)
            windOpenCtrl.Enable(value)
            if not value:
                workModeCtrl.SetSelection(-1)
                triggEvtCtrl.SetSelection(-1)
                windOpenCtrl.SetSelection(-1)


        def OpenSchedule():
            schedulerName.ChangeValue(self.tmpData[self.lastRow][1])
            type = self.tmpData[self.lastRow][2]
            fillDynamicSizer(
                type,
                self.tmpData[self.lastRow][3],
                typeChoice.GetSelection()
            )
            typeChoice.SetSelection(type)
            modes = self.tmpData[self.lastRow][7]
            rsMode = (modes>>1)&3
            workModeCtrl.SetSelection(rsMode)
            recordCtrl.GetTextCtrl().ChangeValue(self.tmpData[self.lastRow][6])
            sourceCtrl.SetValue(self.tmpData[self.lastRow][5])
            if rsMode == 3:
                windOpenCtrl.SetSelection(-1)
                windOpenCtrl.Enable(False)
                windOpenLbl.Enable(False)
            else:
                windOpenCtrl.SetSelection(modes&1)
                windOpenCtrl.Enable(True)
                windOpenLbl.Enable(True)
            triggEvtCtrl.SetSelection((modes>>3)&3)


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


        def onCheckListCtrl(evt):
            index, flag = evt.GetValue()
            if self.tmpData[index][0] != int(flag):
                self.tmpData[index][0] = int(flag)
                Diff()


        def onSchedulerTitle(evt):
            txt = evt.GetString()
            grid.SetStringItem(self.lastRow, 1, txt)
            self.tmpData[self.lastRow][1] = txt
            Diff()


        def onPeriodNumber(evt):
            if len(self.ctrls) == 5 and evt.GetId() == self.ctrls[3]:
                self.tmpData[self.lastRow][3][3] = int(evt.GetString())
                next = self.plugin.NextRun(
                    self.tmpData[self.lastRow][2],
                    self.tmpData[self.lastRow][3]
                )
                grid.SetStringItem(self.lastRow, 3, next)
                Diff()
            else:
                evt.Skip()


        def onTestButton(evt):
            data = self.tmpData[self.lastRow]
            if testValidity([data,], True):
                return
            ticks = mktime(localtime())
            next, cmdline = self.plugin.Execute(data, True)
            next = next[:19] if next else self.plugin.text.none
            self.plugin.updateLogFile(self.text.testRun % (data[1], next))
            self.plugin.updateLogFile(self.plugin.text.cmdLine % cmdline)


        def OnRightClick(evt):
            if not hasattr(self, "popupID1"):
                self.popupID1 = wx.NewId()
                self.popupID2 = wx.NewId()
                self.popupID3 = wx.NewId()
                self.popupID4 = wx.NewId()
                self.popupID5 = wx.NewId()
                self.popupID6 = wx.NewId()
                self.popupID7 = wx.NewId()
                self.Bind(wx.EVT_MENU, addSchedule, id=self.popupID1)
                self.Bind(wx.EVT_MENU, duplSchedule, id=self.popupID2)
                self.Bind(wx.EVT_MENU, delSchedule, id=self.popupID3)
                self.Bind(wx.EVT_MENU, self.EnableAll, id=self.popupID4)
                self.Bind(wx.EVT_MENU, self.DisableAll, id=self.popupID5)
                self.Bind(wx.EVT_MENU, moveUp, id=self.popupID6)
                self.Bind(wx.EVT_MENU, moveDown, id=self.popupID7)
            # make a menu
            menu = wx.Menu()
            menu.Append(self.popupID1, self.text.popup[0])
            menu.Append(self.popupID2, self.text.popup[1])
            menu.Append(self.popupID3, self.text.popup[2])
            menu.AppendSeparator()
            menu.Append(self.popupID4, self.text.popup[3])
            menu.Append(self.popupID5, self.text.popup[4])
            menu.AppendSeparator()
            menu.Append(self.popupID6, self.text.popup[5])
            menu.Append(self.popupID7, self.text.popup[6])
            self.PopupMenu(menu)
            menu.Destroy()
            evt.Skip()


        def fillGrid(flag):
            grid.DeleteAllItems()
            rows = len(self.tmpData)
            if rows > 0:
                for row in range(rows):
                    grid.InsertStringItem(row, "")
                    if self.tmpData[row][0]:
                        grid.CheckItem(row)
                    grid.SetStringItem(row, 1, self.tmpData[row][1])
                    grid.SetStringItem(row, 2, self.tmpData[row][4])
                    next = self.plugin.NextRun(self.tmpData[row][2], self.tmpData[row][3])
                    grid.SetStringItem(row, 3, next)
                if flag:
                    self.lastRow = 0
                    grid.SelRow(0)
                    OpenSchedule()
                    enableBttns(True)
            else:
                EnableCtrls(False)
                grid.DeleteItem(0)

        dynamicSizer = wx.BoxSizer(wx.VERTICAL)
        wDynamic = fillDynamicSizer(3)
        fillDynamicSizer(-1)
        self.SetSize(wx.Size(wDynamic + 37, 684))
        grid = self.grid = CheckListCtrl(self, text, wDynamic + 20)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 0, wx.ALL, 5)
        favorite_label = wx.StaticText(self, -1, self.text.favorite)
        workModeLbl = wx.StaticText(self, -1, self.text.workModeLabel)
        workModeCtrl = wx.Choice(self, -1, choices = self.text.workModes)
        triggEvtLbl = wx.StaticText(self, -1, self.text.triggEvtLabel)
        triggEvtCtrl = wx.Choice(self, -1, choices = self.text.triggEvtChoices)
        windOpenLbl = wx.StaticText(self, -1, self.text.windOpenLabel)
        windOpenCtrl = wx.Choice(self, -1, choices = self.text.windOpenChoices)
        source_label = wx.StaticText(self, -1, self.text.source)
        self.favorites = self.plugin.RefreshVariables()
        favChoice = wx.Choice(self, -1, choices = [item[1] for item in self.favorites])
        sourceCtrl = wx.TextCtrl(self,-1,"")
        filename_label = wx.StaticText(self, -1, self.text.filename)
        schedulerName = wx.TextCtrl(self, -1, "")
        typeChoice = wx.Choice(self, -1, choices = self.text.sched_type)
        xmltoparse = u'%s\\RadioSure.xml' % self.plugin.xmlpath
        xmltoparse = xmltoparse.encode(fse) if isinstance(xmltoparse, unicode) else xmltoparse
        xmldoc = miniDom.parse(xmltoparse)
        recordings = xmldoc.getElementsByTagName('Recordings')
        if not recordings:
            folder = u'%s\\RadioSure Recordings' % self.plugin.xmlpath
        else:
            folder = recordings[0].getElementsByTagName('Folder')[0].firstChild.data
        recordCtrl = MyFileBrowseButton(
            self,
            toolTip = self.text.toolTipFile,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse,
            startDirectory = folder
        )
        self.grid.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, OnRightClick)

        def onSource(evt):
            src = evt.GetString()
            srcs = [item[0] for item in self.favorites]
            if src in srcs:
                ix = srcs.index(src)
            else:
                ix = -1
            favChoice.SetSelection(ix)
            self.tmpData[self.lastRow][5] = src
            Diff()
            evt.Skip()
        sourceCtrl.Bind(wx.EVT_TEXT, onSource)


        def onFavChoice(evt):
            sel = evt.GetSelection()
            txt = self.favorites[sel][0]
            sourceCtrl.ChangeValue(txt)
            self.tmpData[self.lastRow][5] = txt
            Diff()
            evt.Skip()
        favChoice.Bind(wx.EVT_CHOICE, onFavChoice)


        def onRecordCtrl(evt):
            txt = evt.GetString()
            self.tmpData[self.lastRow][6] = txt
            Diff()
            evt.Skip()
        recordCtrl.GetTextCtrl().Bind(wx.EVT_TEXT, onRecordCtrl)


        def onTypeChoice(evt):
            type = evt.GetSelection()
            if self.tmpData[self.lastRow][2] != type:
                empty_data = [
                    ["", "", 0, 0],
                    ["", ""],
                    ["", "", 127, 0, 0],
                    ["", "", 0, 0, 63, 63, 0],
                    ["", "", 0, 0, 0, 0, 63, 63],
                    ["", "", 0, 1, 0],
                ]
                self.tmpData[self.lastRow][2] = type
                data = empty_data[self.tmpData[self.lastRow][2]]
                self.tmpData[self.lastRow][3] = data
                fillDynamicSizer(type, data)
            Diff()


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
            val = self.tmpData[self.lastRow][7]
            val &= (255-6)
            val |= (sel<<1)
            self.tmpData[self.lastRow][7] = val
            Diff()
        workModeCtrl.Bind(wx.EVT_CHOICE, onWorkMode)


        def onWindOpen(evt):
            sel = evt.GetSelection()
            val = self.tmpData[self.lastRow][7]
            val &= (255-1)
            val |= sel
            self.tmpData[self.lastRow][7] = val
            Diff()
        windOpenCtrl.Bind(wx.EVT_CHOICE, onWindOpen)


        def onTriggEvtCtrl(evt):
            sel = evt.GetSelection()
            workMode = workModeCtrl.GetSelection()
            if sel == 0 and workMode == 3:
                ShowMessageBox(self.text.boxTexts[3])
            val = self.tmpData[self.lastRow][7]
            val &= (255-24)
            val |= (sel<<3)
            self.tmpData[self.lastRow][7] = val
            Diff()
        triggEvtCtrl.Bind(wx.EVT_CHOICE, onTriggEvtCtrl)

        bttnSizer = wx.BoxSizer(wx.HORIZONTAL)
        bttnSizer.Add((5, -1))
        i = 0
        for bttn in self.text.buttons:
            id = wx.NewId()
            bttns.append(id)
            b = wx.Button(self, id, bttn)
            bttnSizer.Add(b,1)
            if i in (1, 2, 5):
                b.Enable(False)
            if i == 3:
                b.SetDefault()
            if i == 5:
                self.applyBttn = b
            b.Bind(wx.EVT_BUTTON, onButton, id = id)
            bttnSizer.Add((5, -1))
            i += 1
        sizer.Add(bttnSizer,0,wx.EXPAND)
        id = wx.NewId() #testBttn
        bttns.append(id)
        self.Bind(wx.EVT_BUTTON, onTestButton, id = id)
        wx.EVT_CHECKLISTBOX(self, -1, onCheckListBox)
        maskedlib.EVT_TIMEUPDATE(self, -1, OnTimeChange)
        wx.EVT_TEXT(self, -1, onPeriodNumber)
        wx.EVT_CHOICE(self, -1, onPeriodUnit)
        wx.EVT_DATE_CHANGED(self, -1, onDatePicker)
        wx.EVT_CHECKBOX(self, -1, onCheckBox)
        self.Bind(EVT_UPDATE_DIALOG, OnUpdateDialog)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, OnSelectCell)
        typeChoice.Bind(wx.EVT_CHOICE, onTypeChoice)
        schedulerName.Bind(wx.EVT_TEXT, onSchedulerTitle)
        self.Bind(EVT_CHECKLISTCTRL, onCheckListCtrl)
        nameSizer = wx.FlexGridSizer(2, 0, 0, 20)
        nameSizer.AddGrowableCol(0,1)
        name_label = wx.StaticText(self, -1, self.text.header[1] + ":")
        nameSizer.Add(name_label)
        type_label = wx.StaticText(self, -1, self.text.type_label)
        nameSizer.Add(type_label)
        nameSizer.Add(schedulerName, 0, wx.EXPAND)
        nameSizer.Add(typeChoice)
        typeSizer = wx.StaticBoxSizer(
            wx.StaticBox(self, -1, ""),
            wx.VERTICAL
        )
        dynamicSizer.SetMinSize((-1, 226))
        typeSizer.Add(nameSizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        typeSizer.Add(dynamicSizer, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 5)
        sizer.Add(typeSizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        sizer.Add(source_label, 0, wx.TOP|wx.LEFT, 5)
        sizer.Add(sourceCtrl,0,wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        sizer.Add((1,4))
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
        sizer.Add(filename_label, 0, wx.LEFT, 5)
        sizer.Add(recordCtrl,0,wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        fillGrid(True)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.SetSizer(sizer)
        sizer.Layout()
        if self.plugin.pos:
            self.SetPosition(self.plugin.pos)
        else:
            self.Center()
        self.Show(True)


    def EnableAll(self, flag):
        if isinstance(flag, wx.CommandEvent):
            schedule = self.tmpData[self.lastRow][1]
            flag = 1
        for ix in range(len(self.tmpData)):
            self.tmpData[ix][0] = flag
            if self.grid.GetItem(ix, 1).GetText() == self.tmpData[ix][1]:
                if flag:
                    self.grid.CheckItem(ix)
                elif self.grid.IsChecked(ix):
                    self.grid.ToggleItem(ix)
        self.applyBttn.Enable(self.tmpData != self.plugin.data)


    def DisableAll(self, evt):
        self.EnableAll(0)


    def EnableSchedule(self, schedule, flag):
        tmpList = [item[1] for item in self.tmpData]
        if schedule in tmpList:
            ix = tmpList.index(schedule)
            self.tmpData[ix][0] = flag
            if self.grid.GetItem(ix, 1).GetText() == self.tmpData[ix][1]:
                if flag:
                    self.grid.CheckItem(ix)
                elif self.grid.IsChecked(ix):
                    self.grid.ToggleItem(ix)


    def DeleteSchedule(self, schedule):
        tmpList = [item[1] for item in self.tmpData]
        if schedule in tmpList:
            ix = tmpList.index(schedule)
            if self.grid.GetItem(ix, 1).GetText() == self.tmpData[ix][1]:
                self.grid.DeleteItem(ix)
                self.grid.Refresh()
            self.tmpData.pop(ix)


    def AddSchedule(self, schedule):
        tmpList = [item[1] for item in self.tmpData]
        if schedule[1] in tmpList:
            ix = tmpList.index(schedule[1])
            self.tmpData[ix] = schedule
            if not self.grid.GetItem(ix, 1).GetText() == self.tmpData[ix][1]:
                return
        else:
            ix = len(self.tmpData)
            self.tmpData.append(schedule)
            self.grid.InsertStringItem(ix, "")
        if schedule[0]:
            self.grid.CheckItem(ix)
        elif self.grid.IsChecked(ix):
            self.grid.ToggleItem(ix)
        self.grid.SetStringItem(ix, 1, schedule[1])
        next = self.plugin.NextRun(schedule[2], schedule[3])
        self.grid.SetStringItem(ix, 3, next)
        if self.lastRow == ix:
            evt = wx.PyCommandEvent(newEVT_UPDATE_DIALOG, ix)
            self.GetEventHandler().ProcessEvent(evt)


    def RefreshGrid(self, ix, last, next):
        if self.grid.GetItem(ix, 1).GetText() == self.tmpData[ix][1]:
            self.grid.SetStringItem(ix, 2, last)
            self.grid.SetStringItem(ix, 3, next)


    def onClose(self, evt):
        hwnd = self.GetHandle()
        wp = GetWindowPlacement(hwnd)
        self.plugin.pos = (wp[4][0], wp[4][1])
        #Note: GetPosition() return (-32000, -32000), if window is minimized !!!
        self.Show(False)
        self.plugin.dialog = None
        self.Destroy()
        evt.Skip()
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
    day += 7 * index
    if day > length:
        day = 0
    return day
#===============================================================================

class RadioSure(eg.PluginBase):

    text=Text
    menuDlg = None
    RadioSurePath = u''
    xmlPath = u''
    data = []
    tmpData = []
    dialog = None
    pos = None
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

        def getList2(nodelist):
            tmp = []
            for item in nodelist.childNodes:
                if item.nodeName[:5] == "Item-":
                    title = item.getElementsByTagName('Title')[0].firstChild.data
                    source = item.getElementsByTagName('Source')[0].firstChild.data
                    tmp.append((source, title))
            return tmp

        xmltoparse = u'%s\\RadioSure.xml' % self.xmlpath
        xmltoparse = xmltoparse.encode(fse) if isinstance(xmltoparse, unicode) else xmltoparse
        if not os.path.exists(xmltoparse):
            return
        xmldoc = miniDom.parse(xmltoparse)
        currURL = xmldoc.getElementsByTagName('Station_URL')[0].firstChild
        if currURL:
            self.Current[0] = currURL.data
        currTitle = xmldoc.getElementsByTagName('Station_Title')[0].firstChild
        if currTitle:
            self.Current[1] = currTitle.data
        histNode = xmldoc.getElementsByTagName('History')
        if histNode:
            if histNode[0].childNodes[0].nodeName == "Source_1": # Old xml format
                self.History = getList(histNode[0])
            else: # New xml format
                self.History = getList2(histNode[0])
        else:
            self.History = []
        favNode = xmldoc.getElementsByTagName('Favorites')
        if favNode:
            if favNode[0].childNodes[0].nodeName == "Source_1": # Old xml format
                self.Favorites = getList(favNode[0])
            else: # New xml format
                self.Favorites = getList2(favNode[0])
        else:
            self.Favorites = []
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

        def FindRunDateTime(runList, cond):
            runList.sort()
            runDateTime = ""
            if len(runList) > 0:
                if not cond:
                    return runList[0]
                found = False
                for item in runList:
                    if item.weekday() > 4:
                        found = True
                        break
                    else:
                        if (item.month, item.day) in self.holidays[0]:
                            pass
                        elif (item.year, item.month, item.day) in self.holidays[1]:
                            pass
                        else:
                            found = True
                            break
                if found:
                    runDateTime = item
            return runDateTime

        now = dt.now()
        now = now.replace(microsecond = 0) + td(seconds = 2)
        runTime = dt.strptime(data[0], "%H:%M:%S").time()
        if type == 0: # once or yearly
            runDate = dt.strptime(data[2], '%Y-%m-%d')
            runDateTime = dt.combine(runDate, runTime)
            if now < runDateTime:
                return str(runDateTime)
            elif not data[3]:
                return ""
            else:
                if runDateTime.replace(year = now.year) < now:
                    return str(runDateTime.replace(year = now.year + 1))
                else:
                    return str(runDateTime.replace(year = now.year))
        elif type == 1: # daily
            runDateTime = dt.combine(now.date(), runTime)
            if now.time() > runTime:
                runDateTime += td(days = 1)
            return str(runDateTime)
        elif type == 2: # weekly
            if not data[2]:
                return ""
            runDateTime = dt.combine(now.date(), runTime)
            weekdaysLower = []
            weekdaysLarger = []
            nowDay = now.weekday()
            for weekday in range(7):
                if 2**weekday & data[2]:
                    if weekday < nowDay or (weekday == nowDay and now.time() > runTime):
                        weekdaysLower.append(weekday)
                    else:
                        weekdaysLarger.append(weekday)
            if not data[4] and not data[3]: # without holiday check
                if len(weekdaysLarger) > 0:
                    delta = weekdaysLarger[0] - nowDay
                    return str(runDateTime + td(days = delta))
                delta = 7 + weekdaysLower[0] - nowDay
                return str(runDateTime + td(days = delta))
            elif data[4]: # holiday check
                found = False
                shift = 0
                while True:
                    for day in weekdaysLarger:
                        delta = day + shift - nowDay
                        tmpRunDT = runDateTime + td(days = delta)
                        if tmpRunDT.weekday() > 4: # weekend
                            found = True
                            break
                        else: # workday
                            if (tmpRunDT.month, tmpRunDT.day) in self.holidays[0]:
                                pass
                            elif (tmpRunDT.year, tmpRunDT.month, tmpRunDT.day) in self.holidays[1]:
                                pass
                            else:
                                found = True
                                break
                    if found:
                        break
                    shift += 7
                    for day in weekdaysLower:
                        delta = day + shift - nowDay
                        tmpRunDT = runDateTime + td(days = delta)
                        if tmpRunDT.weekday() > 4: # weekend
                            found = True
                            break
                        else: # workday
                            if (tmpRunDT.month, tmpRunDT.day) in self.holidays[0]:
                                pass
                            elif (tmpRunDT.year, tmpRunDT.month, tmpRunDT.day) in self.holidays[1]:
                                pass
                            else:
                                found = True
                                break
                    if found:
                        break
                return str(tmpRunDT)
            else: # holiday_2 check
                if len(weekdaysLarger) > 0:
                    Delta = weekdaysLarger[0] - nowDay
                else:
                    Delta = 7 + weekdaysLower[0] - nowDay
                start = 0 if now.time() < runTime else 1
                found = False
                for delta in range(start, Delta):
                    tmpRunDT = runDateTime + td(days = delta)
                    if tmpRunDT.weekday() < 5:
                        if (tmpRunDT.month, tmpRunDT.day) in self.holidays[0]:
                            found = True
                            break
                        elif (tmpRunDT.year, tmpRunDT.month, tmpRunDT.day) in self.holidays[1]:
                            found = True
                            break
                return str(tmpRunDT if found else runDateTime + td(days = Delta))
        elif type == 3: # monthly/weekday
            if data[2] == 0 or data[3] == 0 or (data[4] + data[5]) == 0:
                return ""
            currMonth = now.month
            currYear = now.year
            monthsInt = data[4] + (data[5] << 6)
            months = []
            for month in range(1,13):
                if 2 ** (month - 1) & monthsInt:
                    months.append(month)
            if currMonth in months:
                runList = []
                for ix in range(6):
                    if 2 ** ix & data[2]:
                        for weekday in range(7):
                            if 2 ** weekday & data[3]:
                                day = FindMonthDay(currYear, currMonth, weekday, ix)
                                if day:
                                    runDateTime = dt.combine(dt(currYear, currMonth, day).date(), runTime)
                                    if now < runDateTime:
                                        runList.append(runDateTime)
                tmpRunDT = FindRunDateTime(runList, data[6])
                if tmpRunDT:
                    return str(tmpRunDT)
            lower = []
            larger = []
            for month in months:
                if month > currMonth:
                    larger.append(month)
                else: #month <= currMonth:
                    lower.append(month)
            year = currYear
            tmpRunDT = None
            while True:
                for month in larger:
                    runList = []
                    for ix in range(6):
                        if 2 ** ix & data[2]:
                            for weekday in range(7):
                                if 2 ** weekday & data[3]:
                                    day = FindMonthDay(year, month, weekday, ix)
                                    if day:
                                        runDateTime = dt.combine(dt(year, month, day).date(), runTime)
                                        runList.append(runDateTime)
                    tmpRunDT = FindRunDateTime(runList, data[6])
                    if tmpRunDT:
                        break
                if tmpRunDT:
                    break
                year += 1
                for month in lower:
                    runList = []
                    for ix in range(6):
                        if 2 ** ix & data[2]:
                            for weekday in range(7):
                                if 2 ** weekday & data[3]:
                                    day=FindMonthDay(year, month, weekday, ix)
                                    if day:
                                        runDateTime = dt.combine(dt(year, month, day).date(), runTime)
                                        runList.append(runDateTime)
                    tmpRunDT = FindRunDateTime(runList, data[6])
                    if tmpRunDT:
                        break
                if tmpRunDT:
                    break
            return str(tmpRunDT)
        elif type == 4: #monthly/day
            if (data[2] + data[3] + data[4] + data[5]) == 0 or (data[6] + data[7]) == 0:
                return ""
            runList = []
            currMonth = now.month
            currYear = now.year
            monthsInt = data[6] + (data[7] << 6)
            daysInt = data[2] + (data[3] << 8) + (data[4] << 16) + (data[5] << 24)
            days = []
            for day in range(1, 32):
                if 2 ** (day - 1) & daysInt:
                    days.append(day)
            months = []
            for month in range(1, 13):
                if 2 ** (month - 1) & monthsInt:
                    months.append(month)
            if currMonth in months:
                for day in days:
                    if day > monthrange(currYear, currMonth)[1]:
                        break
                    runDateTime = dt.combine(dt(currYear, currMonth, day).date(), runTime)
                    if now < runDateTime:
                        runList.append(runDateTime)
            if len(runList) == 0:
                lower = []
                larger = []
                nextMonth = None
                for month in months:
                    if month > currMonth:
                        larger.append(month)
                    else: #month<=currMonth:
                        lower.append(month)
                if len(larger) > 0:
                    nextYear = currYear
                    for month in larger:
                        for day in days:
                            if day > monthrange(nextYear, month)[1]:
                                break
                            runDateTime = dt.combine(dt(nextYear, month, day).date(), runTime)
                            runList.append(runDateTime)
                if len(runList) == 0 and len(lower) > 0:
                    nextYear = currYear + 1
                    for month in lower:
                        for day in days:
                            if day > monthrange(nextYear, month)[1]:
                                break
                            runDateTime = dt.combine(dt(nextYear, month, day).date(), runTime)
                            runList.append(runDateTime)
            if len(runList) > 0:
                return str(min(runList))
            else:
                return ""
        else: #type == 5: #periodically
            runDate = dt.strptime(data[2], '%Y-%m-%d')
            runDateTime = dt.combine(runDate, runTime)
            if now < runDateTime:
                return str(runDateTime)
            elif data[4] == 0: #unit =  hour
                period = data[3] * 3600
                if period < 86400 and not 86400 % period:
                    if now.time() > runTime:
                        date = now.date()
                    else:
                        date = now.date() - td(days = 1)
                    runDateTime = dt.combine(date, runTime)
                delta = now - runDateTime
                delta = delta.seconds + 86400 * delta.days
                share = delta / period
                share += 1
                delta = td(seconds = share * period)
                return str(runDateTime + delta)
            elif data[4] == 1 or data[4] == 2: #unit = day or week
                period = data[3] if data[4] == 1 else 7 * data[3]
                delta = (now - runDateTime).days
                share = delta / period
                if not delta % period:
                    if now.time() < runTime:
                        return str(dt.combine(now.date(), runTime))
                share += 1
                delta = td(days = share * period)
                return str(runDateTime + delta)
            elif data[4] == 3: #unit = month
                period = data[3]
                month = runDateTime.month
                year = runDateTime.year
                while now > runDateTime:
                    year += period / 12
                    m = month+period % 12
                    if m > 12:
                        year += 1
                        month = m % 12
                    else:
                        month = m
                    runDateTime = runDateTime.replace(year = year).replace(month = month)
                return str(runDateTime)
            else: # data[4] == 6: #unit = year
                period = data[3]
                year = runDateTime.year
                while now > runDateTime:
                    year += period
                    runDateTime = runDateTime.replace(year = year)
                return str(runDateTime)


    def updateLogFile(self, line, blank = False):
        if not self.logfile:
            return
        f = openFile(self.logfile, encoding='utf-8', mode='a')
        if blank:
            f.write("\r\n")
        f.write("%s  %s\r\n" % (str(dt.now())[:19], line))
        f.close()


    def Execute(self, params, immed = False):

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
            args.append(u'/source="%s"' % params[5])
            duration = 60*int(params[3][1][:2])+int(params[3][1][-2:])
            if duration:
                args.append('/duration=%i' % duration)
            if params[6]:
                recfile = eg.ParseString(params[6])
                try:
                    recfile = eval(recfile)
                except:
                    pass
                args.append(u'/filename="%s"' % recfile)
            elif playRec:
                args.append(u'/filename="%s"' % params[1])
            subprocess.Popen(args)
        if not immed and next: # new schedule, if valid next run time and not TEST/IMMEDIATELY run
            startTicks = mktime(strptime(next, "%Y-%m-%d %H:%M:%S"))
            eg.scheduler.AddTaskAbsolute(startTicks, self.RadioSureScheduleRun, params[1])
        triggEvt = modes & 24
        if triggEvt == 8:
            eg.TriggerEvent(self.text.launched, prefix = "RadioSure", payload = params[1])
        elif triggEvt == 16:
            eg.TriggerEvent(self.text.launched, prefix = "RadioSure", payload = params)
        return (next, my_list2cmdline(args))


    def RadioSureScheduleRun(self, schedule):
        data = self.data
        ix = [item[1] for item in data].index(schedule)
        next, cmdline = self.Execute(data[ix])
        last = str(dt.now())[:19]
        self.data[ix][4] = last
        if self.dialog:
            tmpList = [item[1] for item in self.tmpData]
            if schedule in tmpList:
                ixTmp = tmpList.index(schedule)
                self.tmpData[ixTmp][4] = last
            self.dialog.RefreshGrid(ixTmp, last, next)
        nxt = next[:19] if next else self.text.none        
        self.updateLogFile(self.text.execut % (data[ix][1], nxt))
        self.updateLogFile(self.text.cmdLine % cmdline)


    def UpdateEGscheduler(self):
        data = self.data
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
                elif sched[0] != startTicks: #Re-schedule
                    self.updateLogFile(self.text.re_Sched % (schedule[1], startMoment))
                    eg.scheduler.CancelTask(sched)
                    eg.scheduler.AddTaskAbsolute(startTicks, self.RadioSureScheduleRun, schedule[1])
            elif schedule[0]: #New schedule
                    eg.scheduler.AddTaskAbsolute(startTicks, self.RadioSureScheduleRun, schedule[1])
                    self.updateLogFile(self.text.newSched % (schedule[1], startMoment))


    def dataToXml(self):
        impl = miniDom.getDOMImplementation()
        dom = impl.createDocument(None, u'Document', None)
        root = dom.documentElement
        if self.dialog:
            wp = GetWindowPlacement(self.dialog.GetHandle())
            pos = (wp[4][0], wp[4][1])
        else:
            pos = self.pos     
        root.setAttribute(u'Position', str(pos))
        commentNode = dom.createComment(self.text.xmlComment % str(dt.now())[:19])
        dom.insertBefore(commentNode, root)
        for item in self.data:
            schedNode = dom.createElement(u'Schedule')
            schedNode.setAttribute(u'Name', unicode(item[1]))
            schedNode.setAttribute(u'Type', unicode(item[2]))
            enableNode = dom.createElement(u'Enable')
            enableText = dom.createTextNode(unicode(item[0]))
            enableNode.appendChild(enableText)
            schedNode.appendChild(enableNode)
            last_runNode = dom.createElement(u'Last_run')
            last_runText = dom.createTextNode(unicode(item[4]))
            last_runNode.appendChild(last_runText)
            schedNode.appendChild(last_runNode)
            sourceNode = dom.createElement(u'Source')
            sourceText = dom.createTextNode(unicode(item[5]))
            sourceNode.appendChild(sourceText)
            schedNode.appendChild(sourceNode)
            filenameNode = dom.createElement(u'Filename')
            filenameText = dom.createTextNode(unicode(item[6]))
            filenameNode.appendChild(filenameText)
            schedNode.appendChild(filenameNode)
            modesNode = dom.createElement(u'Modes')
            modesText = dom.createTextNode(unicode(item[7]))
            modesNode.appendChild(modesText)
            schedNode.appendChild(modesNode)
            dateTimeNode = dom.createElement(u'Datetime')
            start_timeNode = dom.createElement(u'Start_time')
            start_timeText = dom.createTextNode(unicode(item[3][0]))
            start_timeNode.appendChild(start_timeText)
            dateTimeNode.appendChild(start_timeNode)
            durationNode = dom.createElement(u'Duration')
            durationText = dom.createTextNode(unicode(item[3][1]))
            durationNode.appendChild(durationText)
            dateTimeNode.appendChild(durationNode)
            if item[2] == 0:
                dateNode = dom.createElement(u'Date')
                dateText = dom.createTextNode(unicode(item[3][2]))
                dateNode.appendChild(dateText)
                dateTimeNode.appendChild(dateNode)
                yearlyNode = dom.createElement(u'Yearly')
                yearlyText = dom.createTextNode(unicode(item[3][3]))
                yearlyNode.appendChild(yearlyText)
                dateTimeNode.appendChild(yearlyNode)
            if item[2] == 2:
                weekdayNode = dom.createElement(u'Weekday')
                weekdayText = dom.createTextNode(unicode(item[3][2]))
                weekdayNode.appendChild(weekdayText)
                dateTimeNode.appendChild(weekdayNode)
                holidayNode = dom.createElement(u'HolidayCheck')
                holidayText = dom.createTextNode(unicode(item[3][4]))
                holidayNode.appendChild(holidayText)
                dateTimeNode.appendChild(holidayNode)
                holiday2Node = dom.createElement(u'HolidayCheck_2')
                holiday2Text = dom.createTextNode(unicode(item[3][3]))
                holiday2Node.appendChild(holiday2Text)
                dateTimeNode.appendChild(holiday2Node)
            if item[2] == 3:
                orderNode = dom.createElement(u'Order')
                orderText = dom.createTextNode(unicode(item[3][2]))
                orderNode.appendChild(orderText)
                dateTimeNode.appendChild(orderNode)
                weekdayNode = dom.createElement(u'Weekday')
                weekdayText = dom.createTextNode(unicode(item[3][3]))
                weekdayNode.appendChild(weekdayText)
                dateTimeNode.appendChild(weekdayNode)
                first_halfNode = dom.createElement(u'First_half')
                first_halfText = dom.createTextNode(unicode(item[3][4]))
                first_halfNode.appendChild(first_halfText)
                dateTimeNode.appendChild(first_halfNode)
                second_halfNode = dom.createElement(u'Second_half')
                second_halfText = dom.createTextNode(unicode(item[3][5]))
                second_halfNode.appendChild(second_halfText)
                dateTimeNode.appendChild(second_halfNode)
                holidayNode = dom.createElement(u'HolidayCheck')
                holidayText = dom.createTextNode(unicode(item[3][6]))
                holidayNode.appendChild(holidayText)
                dateTimeNode.appendChild(holidayNode)
            if item[2] == 4:
                q_1_Node = dom.createElement(u'Q_1')
                q_1_Text = dom.createTextNode(unicode(item[3][2]))
                q_1_Node.appendChild(q_1_Text)
                dateTimeNode.appendChild(q_1_Node)
                q_2_Node = dom.createElement(u'Q_2')
                q_2_Text = dom.createTextNode(unicode(item[3][3]))
                q_2_Node.appendChild(q_2_Text)
                dateTimeNode.appendChild(q_2_Node)
                q_3_Node = dom.createElement(u'Q_3')
                q_3_Text = dom.createTextNode(unicode(item[3][4]))
                q_3_Node.appendChild(q_3_Text)
                dateTimeNode.appendChild(q_3_Node)
                q_4_Node = dom.createElement(u'Q_4')
                q_4_Text = dom.createTextNode(unicode(item[3][5]))
                q_4_Node.appendChild(q_4_Text)
                dateTimeNode.appendChild(q_4_Node)
                first_halfNode = dom.createElement(u'First_half')
                first_halfText = dom.createTextNode(unicode(item[3][6]))
                first_halfNode.appendChild(first_halfText)
                dateTimeNode.appendChild(first_halfNode)
                second_halfNode = dom.createElement(u'Second_half')
                second_halfText = dom.createTextNode(unicode(item[3][7]))
                second_halfNode.appendChild(second_halfText)
                dateTimeNode.appendChild(second_halfNode)
            if item[2] == 5:
                dateNode = dom.createElement(u'Date')
                dateText = dom.createTextNode(unicode(item[3][2]))
                dateNode.appendChild(dateText)
                dateTimeNode.appendChild(dateNode)
                numberNode = dom.createElement(u'Number')
                numberText = dom.createTextNode(unicode(item[3][3]))
                numberNode.appendChild(numberText)
                dateTimeNode.appendChild(numberNode)
                unitNode = dom.createElement(u'Unit')
                unitText = dom.createTextNode(unicode(item[3][4]))
                unitNode.appendChild(unitText)
                dateTimeNode.appendChild(unitNode)
            schedNode.appendChild(dateTimeNode)
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
        if "Position" in document.attributes.keys():
            pos = document.attributes["Position"].value
            self.pos = eval(pos)
        else:
            self.pos = (0, 0)
        schedules = tuple(document.getElementsByTagName('Schedule'))
        for schedule in schedules:
            dataItem = []
            enable = int(schedule.getElementsByTagName('Enable')[0].firstChild.data)
            dataItem.append(enable)
            name = schedule.attributes["Name"].value
            dataItem.append(name)
            schedType = int(schedule.attributes["Type"].value)
            dataItem.append(schedType)
            dateTime = schedule.getElementsByTagName('Datetime')[0]
            params = []
            start_time = dateTime.getElementsByTagName('Start_time')[0].firstChild.data
            params.append(start_time)
            duration = dateTime.getElementsByTagName('Duration')[0].firstChild.data
            params.append(duration)
            if schedType == 0:
                date = dateTime.getElementsByTagName('Date')[0].firstChild.data
                params.append(date)
                date = int(dateTime.getElementsByTagName('Yearly')[0].firstChild.data)
                params.append(date)
            if schedType == 2:
                weekday = int(dateTime.getElementsByTagName('Weekday')[0].firstChild.data)
                params.append(weekday)
                holiday2 = int(dateTime.getElementsByTagName('HolidayCheck_2')[0].firstChild.data)
                params.append(holiday2)
                holiday = int(dateTime.getElementsByTagName('HolidayCheck')[0].firstChild.data)
                params.append(holiday)
            if schedType == 3:
                order = int(dateTime.getElementsByTagName('Order')[0].firstChild.data)
                params.append(order)
                weekday = int(dateTime.getElementsByTagName('Weekday')[0].firstChild.data)
                params.append(weekday)
                first_half = int(dateTime.getElementsByTagName('First_half')[0].firstChild.data)
                params.append(first_half)
                second_half = int(dateTime.getElementsByTagName('Second_half')[0].firstChild.data)
                params.append(second_half)
                holiday = int(dateTime.getElementsByTagName('HolidayCheck')[0].firstChild.data)
                params.append(holiday)
            if schedType == 4:
                q_1 = int(dateTime.getElementsByTagName('Q_1')[0].firstChild.data)
                params.append(q_1)
                q_2 = int(dateTime.getElementsByTagName('Q_2')[0].firstChild.data)
                params.append(q_2)
                q_3 = int(dateTime.getElementsByTagName('Q_3')[0].firstChild.data)
                params.append(q_3)
                q_4 = int(dateTime.getElementsByTagName('Q_4')[0].firstChild.data)
                params.append(q_4)
                first_half = int(dateTime.getElementsByTagName('First_half')[0].firstChild.data)
                params.append(first_half)
                second_half = int(dateTime.getElementsByTagName('Second_half')[0].firstChild.data)
                params.append(second_half)
            if schedType == 5:
                date = dateTime.getElementsByTagName('Date')[0].firstChild.data
                params.append(date)
                number = int(dateTime.getElementsByTagName('Number')[0].firstChild.data)
                params.append(number)
                unit = int(dateTime.getElementsByTagName('Unit')[0].firstChild.data)
                params.append(unit)
            dataItem.append(params)
            last_run = schedule.getElementsByTagName('Last_run')[0].firstChild
            last_run = last_run.data if last_run else " "
            dataItem.append(last_run)
            source = schedule.getElementsByTagName('Source')[0].firstChild
            source = source.data if source else ""
            dataItem.append(source)
            filename = schedule.getElementsByTagName('Filename')[0].firstChild
            filename = filename.data if filename else ""
            dataItem.append(filename)
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


    def __start__(
        self,
        path = None,
        xmlpath = None,
        logfile = None,
        holidays = [[], []],
        first_day = 0
        ):
        self.RadioSurePath = path
        self.xmlpath = xmlpath
        self.logfile = logfile
        self.holidays = holidays
        self.first_day = first_day
        self.data = []
        self.tmpData = []
        if self.xmlpath:
            if os.path.exists(self.xmlpath):
                self.data = self.xmlToData()
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
        if self.dialog:
            self.dialog.Close()
        self.dataToXml()



    def __close__(self):
        if self.observThread:
            ot = self.observThread
            if ot.isAlive():
                ot.AbortObservation()


    def Configure(
        self,
        path = "",
        xmlpath = "",
        logfile = None,
        holidays = [[], []],
        first_day = 0
        ):
        panel = eg.ConfigPanel(self)
        panel.holidays = cpy(holidays)
        del holidays
        managerButton = wx.Button(panel, -1, self.text.managerButton)
        if not path: #First run after plugin insert
            managerButton.Enable(False)
        self.RadioSurePath = path
        self.xmlpath = xmlpath
        self.logfile = logfile
        self.first_day = first_day
        label1Text = wx.StaticText(panel, -1, self.text.label1)
        rsPathCtrl = MyDirBrowseButton(
            panel,
            toolTip = self.text.toolTipFolder,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse
        )
        rsPathCtrl.GetTextCtrl().SetEditable(False)
        label2Text = wx.StaticText(panel, -1, self.text.label2)
        xmlPathCtrl = MyDirBrowseButton(
            panel,
            toolTip = self.text.toolTipFolder,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse
        )
        xmlPathCtrl.GetTextCtrl().SetEditable(False)
        logFileCtrl = MyFileBrowseButton(
            panel,
            toolTip = self.text.toolTipFile,
            dialogTitle = self.text.browseFile,
            buttonText = eg.text.General.browse
        )
        logFileCtrl.GetTextCtrl().SetEditable(False)
        logCheckBox = wx.CheckBox(panel, -1, self.text.logLabel)
        if not self.RadioSurePath or not os.path.exists(self.RadioSurePath):
            RSpath = getPathFromReg() #Try get path from registry
            if RSpath: #Regular installation
                if os.path.exists(RSpath):
                    self.RadioSurePath = RSpath
            else: #Portable installation
                self.RadioSurePath = u"%s\\RadioSure" % unicode(eg.folderPath.LocalAppData) 
            xmlPath = u"%s\\RadioSure" % unicode(eg.folderPath.LocalAppData)
            if os.path.exists(xmlPath):
                self.xmlpath = xmlPath
        if os.path.exists(os.path.join(self.RadioSurePath, "RadioSure.exe")):
            rsPathCtrl.GetTextCtrl().ChangeValue(self.RadioSurePath)
            rsPathCtrl.Enable(False)
            label1Text.Enable(False)
        if os.path.exists(os.path.join(self.xmlpath, "RadioSure.xml")):
            xmlPathCtrl.GetTextCtrl().ChangeValue(self.xmlpath)
            xmlPathCtrl.Enable(False)
            label2Text.Enable(False)


        def NotHidden():
            try:
                nssh = OpenKey(
                    HKEY_CURRENT_USER,
                    "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced"
                )
                res = QueryValueEx(nssh, "Hidden")[0] != 2
                CloseKey(nssh)
            except:
                res = False
            return res            


        def NotHiddenAttr(path):
            attr = GetFileAttributes(path)
            if attr & (FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM):
                return False
            else:
                p = os.path.split(path)[0]
                if len(p) > 3:
                    return NotHiddenAttr(p)
                return True

        if self.logfile is None:
            logCheckBox.SetValue(True)
            if NotHiddenAttr(self.xmlpath) or NotHidden():
                self.logfile = u'%s\\RadioSureSchedulerLog.txt' % self.xmlpath
            else:
                self.logfile = u'%s\\RadioSureSchedulerLog.txt' % unicode(eg.folderPath.Documents)
        else:
            val = self.logfile != ""
            logCheckBox.SetValue(val)
            logFileCtrl.Enable(val)
        logFileCtrl.GetTextCtrl().ChangeValue(self.logfile)

        rsPathCtrl.startDirectory = self.RadioSurePath
        xmlPathCtrl.startDirectory = self.xmlpath
        logFileCtrl.startDirectory = self.logfile or u"%s\\RadioSure" % unicode(eg.folderPath.LocalAppData)
        sizerAdd = panel.sizer.Add
        sizerAdd(label1Text, 0)
        sizerAdd(rsPathCtrl,0,wx.TOP|wx.EXPAND,2)
        sizerAdd(label2Text, 0, wx.TOP,15)
        sizerAdd(xmlPathCtrl,0,wx.TOP|wx.EXPAND,2)
        sizerAdd(logCheckBox, 0, wx.TOP,15)
        sizerAdd(logFileCtrl, 0, wx.TOP|wx.EXPAND,2)
        firstDayLabel = wx.StaticText(panel, -1, self.text.first_day)
        firstDayCtrl = wx.Choice(
            panel,
            -1,
            choices = (
                day_name[0],
                day_name[6]
            ),
            size = (firstDayLabel.GetSize()[0], -1)
        )
        firstDayCtrl.SetSelection(first_day)
        panel.holidButton = wx.Button(panel, -1, self.text.holidButton)


        def OnApplyBtn(evt):
            managerButton.Enable(True)
            evt.Skip()
        panel.dialog.buttonRow.applyButton.Bind(wx.EVT_BUTTON, OnApplyBtn)


        def onManagerButton(evt):
            if not self.dialog:
                wx.CallAfter(schedulerDialog, self.text.OpenScheduler, self)
            else:
                if self.dialog.GetPosition() == (-32000, -32000):
                    ShowWindow(self.dialog.GetHandle(), SW_RESTORE) 
                wx.CallAfter(self.dialog.Raise)
            evt.Skip()
        managerButton.Bind(wx.EVT_BUTTON, onManagerButton)


        def onHolidButton(evt):
            dlg = HolidaysFrame(
                parent = panel,
                plugin = self,
            )
            dlg.Centre()
            wx.CallAfter(dlg.ShowHolidaysFrame)
            evt.Skip()
        panel.holidButton.Bind(wx.EVT_BUTTON, onHolidButton)

        bottomSizer = wx.GridBagSizer(1, 1)
        bottomSizer.AddGrowableCol(1,1)
        bottomSizer.AddGrowableCol(3,1)
        bottomSizer.Add(firstDayLabel, (0, 0), flag = wx.LEFT)
        bottomSizer.Add(firstDayCtrl, (1, 0), flag = wx.LEFT)
        bottomSizer.Add((1, -1), (1, 1), flag = wx.EXPAND)
        bottomSizer.Add((1, -1), (1, 3), flag = wx.EXPAND)
        bottomSizer.Add(panel.holidButton, (1, 2))
        bottomSizer.Add(managerButton, (1, 4), flag = wx.RIGHT)
        sizerAdd(bottomSizer, 1, wx.TOP | wx.EXPAND, 15)


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
                panel.holidays,
                firstDayCtrl.GetSelection()
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
            rs = rs.encode(fse) if isinstance(rs, unicode) else rs
            if os.path.isfile(rs):
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
            max = len(self.plugin.Favorites)
            if max > 0:
                stationChoiceCtrl = self.plugin.menuDlg.stationChoiceCtrl
                sel = stationChoiceCtrl.GetSelectedRows()[0]
                if sel == eval(self.value[0]):
                    sel = eval(self.value[1])
                stationChoiceCtrl.SetGridCursor(sel + self.value[2], 0)
                stationChoiceCtrl.SelectRow(sel + self.value[2])
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

    def __call__(self):
        if not self.plugin.dialog:
            wx.CallAfter(schedulerDialog, self.text, self.plugin)
        else:
            if self.plugin.dialog.GetPosition() == (-32000, -32000):
                ShowWindow(self.plugin.dialog.GetHandle(), SW_RESTORE) 
            wx.CallAfter(self.plugin.dialog.Raise)
#===============================================================================

class HideScheduler(eg.ActionBase):

    def __call__(self):
        if self.plugin.dialog:
            wx.CallAfter(self.plugin.dialog.Close)
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
        data = self.plugin.data
        tmpLst = [item[1] for item in data]
        if schedule in tmpLst:
            ix = tmpLst.index(schedule)
            if self.value > -1:
                data[ix][0] = self.value
                self.plugin.dataToXml()
                self.plugin.UpdateEGscheduler()
                if self.plugin.dialog:
                    wx.CallAfter(self.plugin.dialog.EnableSchedule, schedule, self.value)
            return data[tmpLst.index(schedule)]
        else:
            return self.text.notFound % schedule


    def Configure(self, schedule=""):
        panel = eg.ConfigPanel()
        xmlfile = u'%s\\Scheduler.xml' % self.plugin.xmlpath
        if not os.path.exists(xmlfile):
            return
        data = self.plugin.xmlToData()
        choices = [item[1] for item in data]
        textControl = wx.ComboBox(panel, -1, schedule, size = (300,-1), choices = choices)
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
        data = self.plugin.data
        for schedule in data:
            schedule[0] = self.value
        self.plugin.dataToXml()
        self.plugin.UpdateEGscheduler()
        if self.plugin.dialog:
            wx.CallAfter(self.plugin.dialog.EnableAll, self.value)
#===============================================================================

class DeleteSchedule(eg.ActionBase):

    class text:
        scheduleTitle = "Schedule title:"


    def __call__(self, schedule=""):
        schedule = eg.ParseString(schedule)
        xmlfile = u'%s\\Scheduler.xml' % self.plugin.xmlpath
        if not os.path.exists(xmlfile):
            return
        data = self.plugin.data
        tmpLst = [item[1] for item in data]
        if schedule in tmpLst:
            ix = tmpLst.index(schedule)
            data.pop(ix)
            self.plugin.dataToXml()
            self.plugin.UpdateEGscheduler()
            if self.plugin.dialog:
                wx.CallAfter(self.plugin.dialog.DeleteSchedule, schedule)


    def Configure(self, schedule=""):
        panel = eg.ConfigPanel()
        xmlfile = u'%s\\Scheduler.xml' % self.plugin.xmlpath
        if not os.path.exists(xmlfile):
            return
        data = self.plugin.xmlToData()
        choices = [item[1] for item in data]
        textControl = wx.ComboBox(panel, -1, schedule, size = (300,-1), choices = choices)
        panel.sizer.Add(wx.StaticText(panel,-1,self.text.scheduleTitle), 0,wx.LEFT|wx.TOP, 10)
        panel.sizer.Add(textControl, 0, wx.LEFT, 10)

        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())
#===============================================================================

class RunScheduleImmediately(eg.ActionBase):

    class text:
        scheduleTitle = "Schedule title:"
        notFound = 'Can not find schedule "%s" !'
        immedRun = 'Schedule "%s" - IMMEDIATELY execution. Possible next time: %s'

    def __call__(self, schedule=""):
        schedule = eg.ParseString(schedule)
        data = self.plugin.data
        tmpLst = [item[1] for item in data]
        if schedule in tmpLst:
            ix = tmpLst.index(schedule)
            sched = self.plugin.data[ix]
            if sched[0]:
                for sch in eg.scheduler.__dict__['heap']:
                    if sch[1] == self.plugin.RadioSureScheduleRun:
                        if sch[2][0] == sched[1]:
                            eg.scheduler.CancelTask(sch)
                            self.plugin.updateLogFile(self.plugin.text.canc % sch[2][0])
                            break
                next, cmdline = self.plugin.Execute(sched, True)
                next = next[:19] if next else self.plugin.text.none
                self.plugin.updateLogFile(self.text.immedRun % (sched[1], next))
                self.plugin.updateLogFile(self.plugin.text.cmdLine % cmdline)
        else:
            self.PrintError(self.text.notFound % schedule)
            return self.text.notFound % schedule


    def Configure(self, schedule = ""):
        panel = eg.ConfigPanel()
        data = self.plugin.data
        choices = [item[1] for item in data]
        textControl = wx.ComboBox(panel, -1, schedule, size = (300, -1), choices = choices)
        panel.sizer.Add(wx.StaticText(panel, -1, self.text.scheduleTitle), 0, wx.LEFT | wx.TOP, 10)
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
        schedule = eg.ParseString(expr)
        schedule = eval(schedule)
        if len(schedule) == 8 and isinstance(schedule[1], unicode):
            data = self.plugin.data
            tmpLst = [item[1] for item in data]
            if schedule[1] in tmpLst:
                data[tmpLst.index(schedule[1])] = schedule
            else:
                data.append(schedule)
            self.plugin.UpdateEGscheduler()
            if self.plugin.dialog:
                wx.CallAfter(self.plugin.dialog.AddSchedule, schedule)


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
        (HideScheduler,"HideScheduler","Hide scheduler","Hide scheduler.", None),
        (EnableSchedule,"EnableSchedule","Enable schedule","Enable schedule.", 1),
        (EnableSchedule,"DisableSchedule","Disable schedule","Disable schedule.", 0),
        (EnableAll,"EnableAll","Enable all schedules","Enable all schedules.", 1),
        (EnableAll,"DisableAll","Disable all schedules","Disable all schedules.", 0),
        (EnableSchedule,"GetSchedule","Get schedule","Get schedule.", -1),
        (AddSchedule,"AddSchedule","Add schedule",AddSchedule.text.descr, None),
        (DeleteSchedule,"DeleteSchedule","Delete schedule","Delete schedule.", None),
        (RunScheduleImmediately, "RunScheduleImmediately", "Run schedule immediately", "Runs schedule immediately.", None),
    )),
)
#===============================================================================