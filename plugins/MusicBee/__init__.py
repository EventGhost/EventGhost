# -*- coding: utf-8 -*-
version = "0.0.16"
#
# plugins/MusicBee/__init__.py
#
# Copyright (C) 2013 Pako
#
# This file is a plugin for EventGhost.
# Copyright (C) 2005-2015 Lars-Peter Voss <bitmonster@eventghost.org>
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
# 0.0.16 by Pako 2016-02-04 16:49 UTC+1
#       - added support for MusicBee3.exe
# 0.0.15 by Pako 2015-03-02 06:52 UTC+1
#       - added actions Get output devices and Set output device
# 0.0.14 by Pako 2014-09-28 14:03 UTC+1
#       - several new events added
# 0.0.13 by Pako 2014-05-03 10:23 UTC+1
#       - StopAfterCurrentChanged event simulated, when track ended
# 0.0.12 by Pako 2014-??-??
#       - ???
# 0.0.11 by Pako 2014-02-23 09:05 UTC+1
#       - StopAfterCurrentChanged event added
# 0.0.10 by Pako 2014-01-16 06:12 UTC+1
#       - improved routine to check the location of MusicBee.exe
# 0.0.9 by Pako 2014-01-12 14:37 UTC+1
#       - added Get "Is running" action
# 0.0.8 by Pako 2013-11-22 12:49 UTC+1
#       - bugfix
# 0.0.7 by Pako 2013-11-10 14:35 UTC+1
#       - bugfix
# 0.0.6 by Pako 2013-11-10 09:57 UTC+1
#       - added actions "Move track" and "Move track (offset)"
# 0.0.5 by Pako 2013-09-01 17:40 UTC+1
#       - cleaning
# 0.0.4 by Pako 2013-08-09 14:24 UTC+1
#       - added two actions "Add (currently playing) song to playlist"
#       - added action "Get static playlists"
#       - added actions "Toggle mute", "Toggle shuffle" and "Toggle repeat"
#       - added actions "Increase/Decrease volume" and "Get track info"
#       - added two actions "Get thumbnail" (Now playing and Library groups)
#       - added actions "Get position (�)" (Now playing group)
#       - introduced events Running and NotRunning
# 0.0.3 by Pako 2013-07-04 17:46 UTC+1
#       - added Library/NowPlayingList/NowPlaying actions "Set file tag"
# 0.0.2 by Pako 2013-05-11 12:37 UTC+1
#       - >>Set repeat mode to "One"<< removed from options (MusicBee API lack)
# 0.0.0 by Pako 2013-02-24 10:56 UTC+1
#       - initial version
#===============================================================================
        
eg.RegisterPlugin(
    name = "MusicBee",
    author = "Pako",
    version = version,
    kind = "program",
    guid = "{CF581493-5DCB-4AA6-934E-E476EF593A01}",
    createMacrosOnAdd = True,
    description = ur'''<rst>
Adds actions to control MusicBee__ - Music manager and player.

| 
| **ATTENTION:**
| For proper function of this plugin it is required the 
| *eventghost* plugin (mb_EgPlugin.dll) to be installed to MusicBee__ !

__ http://getmusicbee.com
__ http://getmusicbee.com
''',
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAADAFBMVEUB+PgC4eEF0tIC"
        "6OgDQUEAAAAGhYUEw8MFCQkFzs4AfHgCNTUANTEAa2UJAABUICuBXnGYjaGZnbGQm7CH"
        "kKM5PUUmKzB2gZWgrcSpts4uMzkAKSkDkZEiAAGmh5/JyOOrudGVn7aCjqB1gI9weolZ"
        "YW3Z7v/x///i+P/c8f/U6P8DtLSOZHjP1vWwvdiZpLqJlKl+iJpqdIJteYjI2/PG2fED"
        "UFAAEhHFr8rK0O2Nma2Di59ncH1MUV4pKzHQ5f77+/sICxABGBgAJiPPudaottCeqr9u"
        "doVja3lgZnW0xdwJCQm2lK7K0/GbqMJ6hJcdISVZKznZ2/pdZHNTWWMiJSmdrcAQERIE"
        "urrgzu+5xuJuepJzeYaMj5eGjJQ3P09ES1pJTlNBRk80OUDJ3PXs//8QExmTo777+fXz"
        "8+8mKjcDoKCXmZ5ZWV0RbW/XzO4uXWPGxsFRUVEZGRlaWlqMjIz/ywDKlwB7XAAgGQCV"
        "cAD/0wA7VF2DhqLjqgD/4gD//QCAYQD/8wABXFxLS0vMmgBsUQD/3AACYWEyS1JnbYbY"
        "owAiS0+dnp6cdQAKW1yMf5h/hYv/xABmQlJQWWvOzc1gYWPSnQAnAABiY3YwNTtwVABh"
        "S1lDR1Q7OzsaFAD/7gA8LgAE9PQdAABIQ04dIyv6vQAATUsvDBItLTRDMwAiBwwYFhuq"
        "fwAMAAAsIQAIR0cGvb0zJgAE3NwGYmIE//8GeXkDc3MEtLQAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL0xskQAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAzMJAxsoAAAEAAAAEAAAYAAL0AAL0AAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAIAAAENRcyAAAAAAAAAAAAAAAAAAAAAxs0QAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAxtIAxtIAAAcAAAAEAAAQAANwAANwxs4QAAAAAAAAAAAC2xwf+AAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAAXEQAAFxEByibzPwAAAlBJREFUeNpjYMAAjExMzAw4"
        "ARMLKxiwsTNilWdFBhycqJLMXNysaIAHSZqXj19AUEhYRBQkISYuISkiBWRIw6RlZOXk"
        "FRSVlFVUgaJSauoampoa6lpAtjZEXlpHV0/fwFDFyBgoZqSuZmIKBCaamqysZmB5cwtL"
        "BX0ra3EjG1tWVjt1e1MwMDFxcGR1Ask7u1i6ugmLiLt7eNqxsnppmppAVTh4gxXw+vgq"
        "+AmL+Kt4qKoGsLJqaplCgaYWxIrAIC8/RRFxY5vgENtQVtYwDROoE9TDWVkjGBi4I6P8"
        "omNi40LiExKTkoGO1NDQMjFN0UrVTGMF2cDMr5sel+EABJmJWcl2oFBQ1gTyvGxBTKAF"
        "2T6uOQ5QkJuGJSDz8g0d4AAtpMHxVRBV6OBQVFwCVlAKEi4rr2BlrayqBkYpSEFNLVQj"
        "3Ii6+gZW1sYmINEMViDu0AJWUAJT0FrdxMra1g4kOkAKOruA4QUCxTAF3SAFjXAFPbUZ"
        "RXATesFWlAFN72sHElwgBf0TJiLcAGZMqga6r7W9DByMwJQwecpUhyLvFpD8NLCC+vbp"
        "QK/UV4GDCZiGZ8yc1QsJBYhjWZvqZ7OyNgCdwAFJLM5z5oo5TostnQcNnfkLgHILG1qh"
        "NjAwLFq8ZNZSR0TwzV6wjJV1ehMr1AYgWL5iZUA4QkF3wyqgDQtZWVkQmWH1GqQIaAAa"
        "sLYNxHKGq+Bbh5BfBfQ/63pW1g0MG1n5sGWouk1gqh/svM1wFVvQIjoCI1Nu3YAkvQ1r"
        "vmXO7uCWlpZm2b4DRRgAhWKVHEUkH6oAAAAASUVORK5CYII="
    ),
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=5463",
)
#===============================================================================

import eg
import wx
import _winreg
import wx.grid as gridlib
from os import environ
from os.path import join, exists, isfile, split
from subprocess import Popen
from eg.WinApi import SendMessageTimeout
from eg.WinApi.Utils import GetMonitorDimensions, BringHwndToFront
from eg.WinApi.Dynamic import PostMessage
from eg.WinApi.Dynamic import CreateEvent, SetEvent
from threading import Timer
from win32gui import GetWindowText, SendMessage, GetWindow
from copy import deepcopy as cpy
from winsound import PlaySound, SND_ASYNC
from ctypes import create_string_buffer, cast, addressof
from ctypes import c_ulong, c_void_p, string_at
from eg.WinApi.Dynamic import COPYDATASTRUCT, PCOPYDATASTRUCT, WM_COPYDATA
from json import loads
from eg.Classes.MainFrame.TreeCtrl import DropTarget as EventDropTarget
from sys import getfilesystemencoding
from time import sleep
FSE = getfilesystemencoding()
MBEXE = "MusicBee3.exe"
SYS_VSCROLL_X    = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
SYS_HSCROLL_Y    = wx.SystemSettings.GetMetric(wx.SYS_HSCROLL_Y)
WM_CLOSE         = 16
WM_APP           = 0x8000
TAHOMA_INFO = "0;-27;0;0;0;400;0;0;0;0;3;2;1;34;Tahoma"
#===============================================================================

def Find_Mb_Mess():
    mb = eg.WindowMatcher(
        #u'MusicBee.exe',
        MBEXE,
        "Eg2MbMessages",
        None,
        None,
        None,
        None,
        True,
        0.0,
        2
    )
    return mb()
#===============================================================================

def Find_Mb_Main():
    mb = eg.WindowMatcher(
        #u'MusicBee.exe',
        MBEXE,
        u'{*}MusicBee',
        None,
        None,
        None,
        None,
        True,
        0.0,
        0
    )
    return mb()
#===============================================================================

PlayState = {
    0: "Undefined",
    1: "Loading",
    3: "Playing",
    6: "Paused",
    7: "Stopped"
}

RepeatMode = {
    0: "None",
    1: "All",
    2: "One"
}

RepeatMode2 = {
    0: "None",
    1: "All",
}

ReplayGainMode = {
    0:    "Off",
    1:    "Track",
    2:    "Album",
    3:    "Smart"
}

FilePropertyType =  {
    2:"Url",
    4:"Kind",
    5:"Format",
    7:"Size",
    8:"Channels",
    9:"SampleRate",
    10:"Bitrate",
    11:"DateModified",
    12:"DateAdded",
    13:"LastPlayed",
    14:"PlayCount",
    15:"SkipCount",
    16:"Duration",
    78:"NowPlayingListIndex",  # only has meaning when called from NowPlayingList_* commands
    94:"ReplayGainTrack",
    95:"ReplayGainAlbum"
}

MetaDataType = {
    65:"TrackTitle",
    30:"Album",
    31:"AlbumArtist",        # displayed album artist
    34:"AlbumArtistRaw",     # stored album artist
    32:"Artist",             # displayed artist
    33:"MultiArtist",        # individual artists, separated by a null char
    40:"Artwork",
    41:"BeatsPerMin",
    43:"Composer",           # displayed composer
    89:"MultiComposer",      # individual composers, separated by a null char
    44:"Comment",
    45:"Conductor",
    46:"Custom1",
    47:"Custom2",
    48:"Custom3",
    49:"Custom4",
    50:"Custom5",
    96:"Custom6",
    97:"Custom7",
    98:"Custom8",
    99:"Custom9",
    128:"Custom10",
    129:"Custom11",
    130:"Custom12",
    131:"Custom13",
    132:"Custom14",
    133:"Custom15",
    134:"Custom16",
    52:"DiscNo",
    54:"DiscCount",
    55:"Encoder",
    59:"Genre",
    60:"GenreCategory",
    61:"Grouping",
    84:"Keywords",
    63:"HasLyrics",
    62:"Lyricist",
    114:"Lyrics",
    64:"Mood",
    66:"Occasion",
    67:"Origin",
    73:"Publisher",
    74:"Quality",
    75:"Rating",
    76:"RatingLove",
    104:"RatingAlbum",
    85:"Tempo",
    86:"TrackNo",
    87:"TrackCount",
    109:"Virtual1",
    110:"Virtual2",
    111:"Virtual3",
    112:"Virtual4",
    113:"Virtual5",
    122:"Virtual6",
    123:"Virtual7",
    124:"Virtual8",
    125:"Virtual9",
    135:"Virtual10",
    136:"Virtual11",
    137:"Virtual12",
    138:"Virtual13",
    139:"Virtual14",
    140:"Virtual15",
    141:"Virtual16",
    88:"Year"
}
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
        self.CreateGrid(lngth, 1)
        attr = gridlib.GridCellAttr()
        attr.SetAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
        self.SetColAttr(0,attr)
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
            self.SetCellValue(i,0," "+choices[i][0]+" ")
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
        self.il.Add(wx.Bitmap(wx.Image(join(eg.imagesDir, "event.png"), wx.BITMAP_TYPE_PNG)))
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
        id = wx.NewIdRef()
        eventsCtrl_0 = EventListCtrl(self, id, self.evtList, 0, self.plugin)
        eventsCtrl_0.SetItems(self.evtList[0])
        dt0 = MyTextDropTarget(eventsCtrl_0)
        eventsCtrl_0.SetDropTarget(dt0)
        textLbl_1=wx.StaticText(self, -1, labels[1])       
        id = wx.NewIdRef()        
        eventsCtrl_1 = EventListCtrl(self, id, self.evtList, 1, self.plugin)
        eventsCtrl_1.SetItems(self.evtList[1])
        dt1 = MyTextDropTarget(eventsCtrl_1)
        eventsCtrl_1.SetDropTarget(dt1)
        textLbl_2=wx.StaticText(self, -1, labels[2])        
        id = wx.NewIdRef()
        eventsCtrl_2 = EventListCtrl(self, id, self.evtList, 2, self.plugin)
        eventsCtrl_2.SetItems(self.evtList[2])
        dt2 = MyTextDropTarget(eventsCtrl_2)
        eventsCtrl_2.SetDropTarget(dt2)
        textLbl_3=wx.StaticText(self, -1, labels[3])        
        id = wx.NewIdRef()        
        eventsCtrl_3 = EventListCtrl(self, id, self.evtList, 3, self.plugin)
        eventsCtrl_3.SetItems(self.evtList[3])
        dt3 = MyTextDropTarget(eventsCtrl_3)
        eventsCtrl_3.SetDropTarget(dt3)
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
        topSizer.Add(deleteSizer, (5,1), flag = wx.EXPAND)

        line = wx.StaticLine(self, -1, size=(20,-1),pos = (200,0), style=wx.LI_HORIZONTAL)
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
        mode,
        ):
        wx.Frame.__init__(
            self,
            None,
            -1,
            'MB_menu',
            style = wx.STAY_ON_TOP|wx.SIMPLE_BORDER
        )
        self.data = data.items()
        self.data.sort()
        self.mode = (64, 57, 58, 69, 53, 55, 56)[mode]
        tmpLst = [i[0] for i in self.data]
        self.actFileIx = 0
        if ">>ActiveFile<<" in tmpLst:
            ix = tmpLst.index(">>ActiveFile<<")
            actFile = self.data[ix][1]
            self.data.pop(ix)
            tmpLst = [i[1] for i in self.data]
            if actFile in tmpLst:
                self.actFileIx = tmpLst.index(actFile)
        self.flag = False
        self.monitor = 0
        self.oldMenu = []
        self.fore     = fore
        self.back     = back
        self.foreSel  = foreSel
        self.backSel  = backSel
        self.fontInfo = fontInfo
        self.flag     = flag
        self.plugin   = plugin
        self.monitor  = monitor
        self.evtList  = self.plugin.evtList
        eg.TriggerEvent("OnScreenMenu.%s" % self.plugin.text.opened, prefix = "MusicBee")
        for evt in self.evtList[0]:
            eg.Bind(evt, self.onUp)
        for evt in self.evtList[1]:
            eg.Bind(evt, self.onDown)
        for evt in self.evtList[2]:
            eg.Bind(evt, self.onRight)
        for evt in self.evtList[3]:
            eg.Bind(evt, self.onEscape)
        self.menuGridCtrl = MenuGrid(self, len(self.data))
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        mainSizer.Add(self.menuGridCtrl, 0, wx.EXPAND)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(gridlib.EVT_GRID_CMD_CELL_LEFT_DCLICK, self.onDoubleClick, self.menuGridCtrl)
        self.Bind(wx.EVT_CHAR_HOOK, self.onFrameCharHook)
        font = wx.Font(fontInfo)
        self.menuGridCtrl.SetFont(font)
        self.SetFont(font)                                   
        self.SetBackgroundColour((0, 0, 0))
        self.menuGridCtrl.SetBackgroundColour(self.back)
        self.menuGridCtrl.SetForegroundColour(self.fore)
        self.menuGridCtrl.SetSelectionBackground(self.backSel)
        self.menuGridCtrl.SetSelectionForeground(self.foreSel)
        if self.flag:
            self.timer=MyTimer(t = 5.0, plugin = self.plugin)
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
            width_lst.append(self.GetFullTextExtent(item[0]+' ')[0])
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
        self.SetSize(x_pos,y_pos,width,height)
        self.menuGridCtrl.SetSize(2, 2, width-6, height-6, wx.SIZE_AUTO)
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
        print "data:", self.data
        sel = self.menuGridCtrl.GetSelection()
        print "sel:", sel
        item = self.data[sel]
        print "item:", item
        self.destroyMenu()
        self.plugin.MusicBeeStringCmd(self.mode, item[1])


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
            if len(self.oldMenu) > 0:
                ix = self.oldMenu.pop()
                wx.CallAfter(self.UpdateMenu, True, ix)
            else:
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
        eg.TriggerEvent("OnScreenMenu.%s" % self.plugin.text.closed, prefix = "MusicBee")
        self.Close()
#===============================================================================

CMD_CONNECT            = 0x00 #Par 1 : MB window handle (command should be send to this HWnd)
CMD_DEFAULT            = 0x01
CMD_TRACKCHANGED       = 0x02 #    Send after opening a new file
                              #    Par 1 : title
                              #    Par 2 : author
                              #    Par 3 : description
                              #    Par 4 : complete filename (path included)
                              #    Par 5 : duration in seconds
CMD_JSON               = 0x03
CMD_SIMPLE             = 0x04
CMD_NULLCHAR           = 0x05
CMD_DISCONNECT         = 0x06
#===============================================================================

class Text:
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
    cancel = 'Cancel'
    ok = 'OK'
    clear  = "Clear all"
    toolTip = "Drag-and-drop an event from the log into the box."
    opened = "Opened"
    closed = "Closed"
    label = "Path to MusicBee executable:"
    fileMask = "MusicBee3 executable|MusicBee3.exe|MusicBee executable\
        |MusicBee.exe|All-Files (*.*)|*.*"
    running = "Running"
    notRunning = "NotRunning"
    stopped = "Eg-MbPlugginStoped"

    commands = (
        "Play/Pause",#0
        "Stop",
        "Stop after current",
        "Play next track",
        "Play previous track",
        "Start AutoDj",#5
        "End AutoDj",
        "Show equaliser",
        'Clear "Now playing list"',
        'Get "Is any following tracks"',
        'Get "Is any prior tracks"',#10
        'Play library shuffled',
        'Get "Show time remaining"',
        "Get mute",
        "Set mute",
        "Get shuffle",#15
        "Set shuffle",
        "Get equaliser enabled",
        "Set equaliser enabled",
        "Get show rating track",
        "Get show rating love",#20
        "Get DSP enabled",
        "Set DSP enabled",
        "Get scrobble enabled",
        "Set scrobble enabled",
        "Get AutoDj enabled",#25
        'Get "Stop after current enabled"',
        "Get crossfade",
        "Set crossfade",
        "Get play state",
        "Get repeat mode",#30
        "Set repeat mode",
        "Get replay gain mode",
        "Set replay gain mode",
        "Get position (s)",
        "Set position",#35
        "Get volume",
        "Set volume",
        "Get duration",
        "Get current index",
        "Queue random tracks",#40
        "Get file URL",
        "Get file property",
        "Get file tag",
        "Get lyrics",
        "Get artwork",#45
        "Get artist picture",
        "Get downloaded artwork",
        "Get downloaded lyrics",
        "Get next index",
        "Play now",#50
        "Remove at",
        "Queue next",
        "Queue last",
        "Get lyrics",
        "Get artwork",#55
        "Get playlists",
        "Queue random",
        #"Seek",
        "Get tracks",
        "Get tracks and active",
        "Set file tag",#60
        "Toggle mute",
        "Increase volume",
        "Decrease volume",
        "Get artwork thumbnail",
        u"Get position (\u2030)", # \u2030 = Unicode Character 'PER MILLE SIGN')
        "Toggle shuffle",
        "Toggle repeat",
        "Get track info",
        "Get static playlists",
        "Move track",#70
        "Move track (offset)",
        "Get list of URL",
        "Get tracks count",
        "Get total duration",
        "Get track title/file name",#75
        "Get output devices",
        "Set output device"
    )

    labels = (
        "Volume (0 - 100) %:", #0
        "Position (0 - 65535) s:",
        "Mute ON:",
        "Shuffle ON:",
        "Crossfade ON:",
        "Equaliser enabled ON:",#5
        "DSP enabled ON:",
        "Scrobble enabled ON:",
        "Repeat mode:",
        "Replay gain mode:",
        "Number of tracks to add to queue:",#10
        "File property:",
        "Meta data:",
        "Fading percentage:",
        "Offset:",
        "Index:",#15
        "Song file path:",
        "Playlist path:",
        "Folder:",
        "Volume step (1 - 20) %:",
        "Size (32-256) px:",#20
        "New index:",
        "Output device:"
       
    )
#===============================================================================

class Group:
    Player = 0
    NowPlaying = 1
    NowPlayingList = 2
    Library = 3
    Playlist = 4
    Folder = 5
    Other = 6
#===============================================================================

Commands = (
    (Group.Player,0,0),#00
    (Group.Player,0,1),
    (Group.Player,0,2),
    (Group.Player,0,3),
    (Group.Player,0,4),
    (Group.Player,0,5),#05
    (Group.Player,0,6),
    (Group.Player,0,7),
    (Group.NowPlayingList,0,8),
    (Group.NowPlayingList,0,9),
    (Group.NowPlayingList,0,10),#10
    (Group.NowPlayingList,0,11),
    (Group.Player,0,12),
    (Group.Player,0,13),
    (Group.Player,0,14,1,2),
    (Group.Player,0,15),#15
    (Group.Player,0,16,1,3),
    (Group.Player,0,17),
    (Group.Player,0,18,1,5),
    (Group.Player,0,19),
    (Group.Player,0,20),#20
    (Group.Player,0,21),
    (Group.Player,0,22,1,6),
    (Group.Player,0,23),
    (Group.Player,0,24,1,7),
    (Group.Player,0,25),#25
    (Group.Player,0,26),
    (Group.Player,0,27),
    (Group.Player,0,28,1,4),
    (Group.Player,0,29,PlayState),
    (Group.Player,0,30,RepeatMode),#30
    (Group.Player,0,31,3,8,RepeatMode2),
    (Group.Player,0,32,ReplayGainMode),
    (Group.Player,0,33,3,9,ReplayGainMode),
    (Group.Player,0,34),
    (Group.Player,0,35,2,1,0,65535,0),#35
    (Group.Player,0,36),
    (Group.Player,0,37,2,0,0,100,0),
    (Group.NowPlaying,0,38),
    (Group.NowPlayingList,0,39),
    (Group.Player,0,40,2,10,0,65535,0),#40
    (Group.NowPlaying,1,41),
    (Group.NowPlaying,1,42,3,11,FilePropertyType),
    (Group.NowPlaying,1,43,3,12,MetaDataType),
    (Group.NowPlaying,1,44),
    (Group.NowPlaying,1,45),#45
    (Group.NowPlaying,1,46,2,13,0,100,0),
    (Group.NowPlaying,1,47),
    (Group.NowPlaying,1,48),
    (Group.NowPlayingList,0,49,2,14,0,65535,0),
    (Group.NowPlayingList,1,41,2,15,0,65535),#50
    (Group.NowPlayingList,1,42,2+16*3,15,0,65535,11,FilePropertyType),#Get file property
    (Group.NowPlayingList,1,43,2+16*3,15,0,65535,12,MetaDataType),
    (Group.NowPlayingList,2,50,4,16),
    (Group.NowPlayingList,0,51,2,15,0,65535,0),
    (Group.NowPlayingList,2,52,4,16),#55
    (Group.NowPlayingList,2,53,4,16),
    (Group.Playlist,2,52,4,17),
    (Group.Playlist,2,53,4,17),
    (Group.Library,4,42,4+16*3,16,11,FilePropertyType),
    (Group.Library,4,43,4+16*3,16,12,MetaDataType),#60
    (Group.Library,4,54,4,16),
    (Group.Library,4,55,4,16),#Get artwork
    (Group.Playlist,1,56),
    (Group.Playlist,2,50,4,17),
    (Group.Folder,2,50,5,18),#65
    (Group.Folder,2,52,5,18),
    (Group.Folder,2,53,5,18),
    (Group.Folder,2,57,5,18),
    (Group.Playlist,2,57,4,17),
    (Group.Other,),#70 Seek
    (Group.NowPlayingList,1,58),
    (Group.NowPlayingList,1,59),
    (Group.Library,3,60,4+16*3,16,12,MetaDataType),
    (Group.NowPlayingList,3,60,2+16*3,15,0,65535,12,MetaDataType),
    (Group.NowPlaying,3,60,3,12,MetaDataType),#75
    (Group.Other,), # Add currently playing song to playlist
    (Group.Other,), # Add a song to playlist
    (Group.Player,0,61), #Toggle mute
    (Group.Player,0,62,2,19,1,20,5),
    (Group.Player,0,63,2,19,1,20,5),#80
    (Group.Library,4,64,4+16*2,16,20,32,256,128),#Get thumbnail
    (Group.NowPlaying,1,64,2,20,32,256,128),
    (Group.NowPlaying,0,65),
    (Group.Player,0,66), #Toggle shuffle
    (Group.Player,0,67), #85  Toggle repeat
    (Group.NowPlaying,1,68),
    (Group.Playlist,1,69),#Get static playlists
    (Group.NowPlayingList,0,70,2+16*2,15,0,65535,21,0,65535,0),#Change track position
    (Group.NowPlayingList,0,71,2+16*2,15,0,65535,14,-4096,4096,0),#Change track position
    (Group.NowPlayingList,1,72),#90   Get list of URL (Now playing list)
    (Group.NowPlayingList,0,73),
    (Group.NowPlayingList,0,74),
    (Group.NowPlayingList,1,75,2,15,0,65535),
    (Group.NowPlaying,1,75),
    (Group.Library,4,75,4,16),#95
    (Group.Player,1,76),
    (Group.Player,3,77,3,22),
)
#===============================================================================

class MusicBee(eg.PluginBase):

    text = Text
    menuDlg = None
    mbHwnd = None
    queryData = {}
    token = 0
    size = (-1, -1)
    mbPath = None


    def ParseMsg(self, msg):
        msg = msg.decode("utf-8")
        # If a string contains a |, it will be escaped with a \ so a \| is not a separator    
        msg = msg.replace(u"\\|", u"\xb0*\u2734*\xb0")
        msg = msg.split(u"|")
        for i in range(len(msg)):
            msg[i] = msg[i].replace(u"\xb0*\u2734*\xb0", u"|")
        return msg


    def GetToken(self):
        self.token += 1
        if self.token == 256:
            self.token = 1
        return self.token


    def GetPlaylists(self, stat = False):
        event = CreateEvent(None, 0, 0, None)
        token = self.GetToken()
        self.queryData[token] = event
        if self.MusicBeeCmd(87 if stat else 63, token, 0):
            eg.actionThread.WaitOnEvent(event)
            data = self.queryData[token]
            del self.queryData[token]
        else:
            del self.queryData[token] 
            data = {}
        return data


    def mbConnected(self, suff):
        eg.scheduler.AddTask(1, self.TriggerEvent, suff)


    @eg.LogIt
    def Handler(self, hwnd, mesg, wParam, lParam):
        cpyData = cast(lParam, PCOPYDATASTRUCT)
        dwData = cpyData.contents.dwData
        cmd = dwData & 0xff
        token = (dwData & 0xff00)/256
        if token:
            event = self.queryData[token]
        count = cpyData.contents.cbData
        msg = string_at(cpyData.contents.lpData, count)
        msg = self.ParseMsg(msg)
        if cmd == CMD_CONNECT:
            self.mbHwnd = int(msg[1])
            wx.CallAfter(self.mbConnected, msg[0])
        elif cmd == CMD_DISCONNECT:
            self.mbHwnd = None
            self.TriggerEvent(msg[0], payload = msg[1])
        elif cmd == CMD_DEFAULT:
            ln = len(msg)
            if token:
                if ln > 2:
                    self.queryData[token] = msg[1:]
                elif ln == 2:
                    self.queryData[token] = msg[1]
                else:
                    self.queryData[token] = None
                SetEvent(event)
            else:
                if ln > 2:
                    eg.TriggerEvent(msg[0],prefix="MusicBee", payload = msg[1:])
                elif ln == 2:
                    eg.TriggerEvent(msg[0],prefix="MusicBee", payload = msg[1])
                else:
                    eg.TriggerEvent(msg[0],prefix="MusicBee")
        elif cmd == CMD_JSON:
            if token:
                self.queryData[token] = loads(msg[1])
                SetEvent(event)
            else:
                eg.TriggerEvent(
                    msg[0],
                    prefix = "MusicBee",
                    payload=[msg[1], loads(msg[2])]
                )
        elif cmd == CMD_NULLCHAR:
            if token:
                self.queryData[token] = msg[1].split("\x00")
                SetEvent(event)
            else:
                eg.TriggerEvent(
                    msg[0],
                    prefix = "MusicBee",
                    payload = msg[1].split("\x00")
                )
        elif cmd == CMD_SIMPLE:
            if len(msg) == 1:
                eg.TriggerEvent(msg[0], prefix = "MusicBee")
            elif len(msg) == 2:
                eg.TriggerEvent(msg[0], prefix = "MusicBee", payload = msg[1])
            else:
                eg.TriggerEvent(msg[0], prefix = "MusicBee", payload = msg[1:])
        elif cmd == CMD_TRACKCHANGED:
            eg.TriggerEvent("TrackChanged", prefix="MusicBee", payload = msg)
        return True


    def isRunning(self):
        if self.mbHwnd:
            try:
                if GetWindowText(self.mbHwnd) == "Eg2MbMessages":
                    return self.mbHwnd
            except:
                pass
        hWnd = Find_Mb_Mess()
        if hWnd:
            self.mbHwnd = hWnd[0]        
            return self.mbHwnd
        raise self.Exceptions.ProgramNotRunning


    def MusicBeeStringCmd(self, cmd, msg):
        hwnd = self.isRunning()
        if hwnd:        
            cpDt = create_string_buffer(msg.encode("utf-8"))
            cds = COPYDATASTRUCT(cmd, len(cpDt), cast(cpDt, c_void_p))
            cds.dwData = cmd
            cds.lpData = cast(cpDt, c_void_p)
            cds.cbData = c_ulong(len(cpDt))
            res = SendMessageTimeout(
                hwnd,
                WM_COPYDATA,
                0,
                addressof(cds),
                timeout = 100000)
            return res if res != 0xFFFFFFFF else -1


    def MusicBeeCmd(self, cmd, token = 0, val = 0):
        hwnd = self.isRunning()
        if hwnd:        
            res = SendMessageTimeout(
                hwnd,
                WM_APP + 1,         # MESSAGE
                cmd + 256 * token,  # wParam
                val,                # lParam
                timeout = 100000
            )
            return res if res != 0xFFFFFFFF else -1


    def __init__(self):
        self.AddActionsFromList(ACTIONS)


    def __start__(self, mbPath = None, evtList = [[], [], [], []]):
        if mbPath is None or mbPath == "" or not exists(mbPath):
            mbPath = self.GetMbPath()
        if mbPath is None or mbPath == "" or not exists(mbPath):
            raise self.Exceptions.ProgramNotFound
            return
        global MBEXE
        MBEXE = split(mbPath)[1]
        self.mr = eg.MessageReceiver("MusicBee_plugin_")
        self.mr.AddHandler(WM_COPYDATA, self.Handler)
        self.mr.Start()
        self.evtList = evtList
        self.mbHwnd = None
        #if mbPath is None:
        self.mbPath = mbPath
        wx.CallAfter(self.setMbHwnd)
    

    def setMbHwnd(self):
        hWnd = Find_Mb_Mess()
        if hWnd:
            self.mbHwnd = hWnd[0]
            self.TriggerEvent(self.text.running)
        else:
            self.TriggerEvent(self.text.notRunning)


    def __stop__(self):
        self.TriggerEvent(self.text.stopped)
        self.mr.RemoveHandler(WM_COPYDATA, self.Handler)
        self.mr.Stop()
        self.mr = None
        self.mbHwnd = None
       

    def Configure(self, mbPath = None, evtList = [[], [], [], []]):
        if mbPath is None or mbPath == "" or not exists(mbPath):
            mbPath = self.GetMbPath()
        panel = eg.ConfigPanel()
        panel.evtList = cpy(evtList)
        filepathCtrl = eg.FileBrowseButton(
            panel, 
            size=(320,-1),
            initialValue=mbPath, 
            startDirectory=eg.folderPath.ProgramFiles,
            labelText="",
            fileMask = self.text.fileMask,
            buttonText=eg.text.General.browse,
        )
        dialogButton = wx.Button(panel,-1,self.text.dialog)
        dialogButton.SetToolTip(self.text.btnToolTip)  

        def OnDialogBtn(evt):
            dlg = MenuEventsDialog(
                parent = panel,
                plugin = self,
            )
            dlg.Centre()
            wx.CallAfter(
                dlg.ShowMenuEventsDialog,
                self.text.evtAssignTitle,
                self.text.events
            )
            evt.Skip()
        dialogButton.Bind(wx.EVT_BUTTON, OnDialogBtn)      
        panel.sizer.Add(wx.StaticText(panel,-1,self.text.label),0,wx.TOP,20)
        panel.sizer.Add(filepathCtrl)
        panel.sizer.Add(dialogButton,0,wx.TOP,20)
        while panel.Affirmed():
            panel.SetResult(filepathCtrl.GetValue(), panel.evtList)

    def str2int(self, s):
        s = eg.ParseString(s)
        try:
            s = int(s)
        except:
            s = 0
        return s


    def GetMbPath(self):
        """
        Get the path of MusicBee's installation directory through querying 
        the Windows registry.
        """
        try:
            args = [_winreg.HKEY_LOCAL_MACHINE,            
                "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\MusicBee3.exe"]
            if "PROCESSOR_ARCHITEW6432" in environ:
                args.extend((0, _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY))
            mb_reg = _winreg.OpenKey(*args)
            mbPath = unicode(_winreg.EnumValue(mb_reg,0)[1])
            _winreg.CloseKey(mb_reg)            
        except WindowsError:
            try:
                args = [_winreg.HKEY_LOCAL_MACHINE,            
                    "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\MusicBee.exe"]
                if "PROCESSOR_ARCHITEW6432" in environ:
                    args.extend((0, _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY))
                mb_reg = _winreg.OpenKey(*args)
                mbPath = unicode(_winreg.EnumValue(mb_reg,0)[1])
                _winreg.CloseKey(mb_reg)            
            except WindowsError:
                mbPath = None
        if mbPath is not None:
            pth, exe = split(mbPath)
            tmp = join(pth, "MusicBee3.exe")
            mbPath = tmp if exists(tmp) else mbPath
        else:
            mbPath = join(
                eg.folderPath.ProgramFiles, 
                "MusicBee", 
                "MusicBee3.exe"
            ) 
        return mbPath
#===============================================================================

class mbCommand(eg.ActionBase):
    name = "MusicBee command"
    description = "Sent MusicBee command"

    class text:
        label = "Command:"
        toolTipFile = 'Type filename or click browse to choose file'
        browseFile = 'Choose a file'
        toolTipFolder = 'Type folder name or click browse to choose folder'
        browseFolder = 'Choose a folder'
        fMask = "Supported audio files (*.mp3;*.aac;*.m4a;*.mpc;*.ogg;*.flac;*.ape;*.Opus;*.tak;*.wv;*.wma;*.wav)|*.mp3;*.aac;*.m4a;*.mpc;*.ogg;*.flac;*.ape;*.Opus;*.tak;*.wv;*.wma;*.wav|All files (*.*)|*.*"
        pMask = "Playlists (*.xautopf; *.m3u)|*.xautopf; *.m3u|All files (*.*)|*.*"

    def __call__(self, cmd = 0, val = None, val2 = None, val3 = None):
        c = Commands[cmd]
        if c[2] == 77:
            pass
        elif len(c) > 4:
            offset = (None, 4, 6, 5, 4, 4)[c[3] & 0x0F]
            val = 0 if val is None else val
            if c[1] < 2:
                val = val if isinstance(val, int) else self.plugin.str2int(val)
                # if DICTIONARY, than value to get other way:
                if isinstance(c[offset], dict):
                    val = tuple(c[offset].iterkeys())[val]
                if c[3] & 0xF0:
                    val2 = 0 if val2 is None else val2
                    if isinstance(c[-1], dict):
                        val2 = tuple(c[-1].iterkeys())[val2]
                else:
                    val2 = 0
        else:
            val = val2 = 0
        if c[1] == 1:
            token = self.plugin.GetToken()
            event = CreateEvent(None, 0, 0, None)
            self.plugin.queryData[token] = event
            if self.plugin.MusicBeeCmd(cmd, token, val + 65536 * val2):
                eg.actionThread.WaitOnEvent(event)
                data = self.plugin.queryData[token]
                del self.plugin.queryData[token]
                return data
            del self.plugin.queryData[token]
        elif c[1] == 2:
            val = eg.ParseString(val) if val else ""
            return self.plugin.MusicBeeStringCmd(cmd, val)     
        elif c[1] == 3: #copydata/set value
            val3 = eg.ParseString(val3) if val3 else ""
            if isinstance(c[-1], dict) and val2 is not None:
                val2 = tuple(c[-1].iterkeys())[val2]
            if val2 is None:
                val2 = 0
                if isinstance(c[-1], dict) and val is not None:
                    val = tuple(c[-1].iterkeys())[val]
            strCmd = "%s|%s" % (str(val), val3)#If a problem occurs, consider switching to UTF-8
            return self.plugin.MusicBeeStringCmd(cmd+65536*val2, strCmd)     
        elif c[1] == 4: #copydata/token
            val = eg.ParseString(val) if val else ""
            if isinstance(c[-1], dict):
                val2 = tuple(c[-1].iterkeys())[val2]
            val2 = 0 if val2 is None else val2
            token = self.plugin.GetToken()
            event = CreateEvent(None, 0, 0, None)
            self.plugin.queryData[token] = event
            if self.plugin.MusicBeeStringCmd(cmd+256*token+65536*val2, val):
                eg.actionThread.WaitOnEvent(event)
                data = self.plugin.queryData[token]
                del self.plugin.queryData[token]
                return data
            del self.plugin.queryData[token]
        else:    # if c[1]== 0
            val += 65536 * (0xF000 + abs(val2)) if val2 < 0 else 65536 * val2
            res = self.plugin.MusicBeeCmd(cmd, 0, val)
            if len(c) == 4 and isinstance(c[3], dict):
                try:
                    res = c[3][res]
                except:
                    res = None
            return res


    def GetLabel(self, cmd, val = None, val2 = None, val3 = None):
        label = self.plugin.text.commands[Commands[cmd][2]]
        res = "%s: %s" % (self.name, label)
        item = Commands[cmd]
        if len(item) > 4 and isinstance(item[3], int):
            if item[3] == 1:
                val = bool(val)
            elif item[3] == 2:
                pass
            elif item[3] == 3: # int + wx.Choice
                val = tuple(item[5].itervalues())[val]
        else:
            val = None
        if val is not None:
            val2 = str(val2) if val2 is not None else ""
            val3 = str(val3) if val3 is not None else ""
            return "%s: %s %s %s" % (res, str(val), val2, val3)
        return res


    def Configure(self, cmd = -1, val = None, val2 = None, val3 = None):
        text = self.text
        self.val = val
        self.val2 = val2
        panel = eg.ConfigPanel(self)
        label = wx.StaticText(panel, -1, text.label)
        choices = []
        selection = [item for item in Commands if item[0] == self.value]
        for i in selection:
            choices.append(self.plugin.text.commands[i[2]])
        #choices.sort()
        cmdCtrl = wx.Choice(panel, -1, choices=choices)
        cmd = cmd if cmd != -1 else Commands.index(selection[0])
        cmdCtrl.SetSelection([i[2] for i in selection].index(Commands[cmd][2]))
        mainSizer = wx.GridBagSizer(10, 10)
        mainSizer.Add(label,(0,0),(1,1),wx.TOP,3)
        mainSizer.Add(cmdCtrl,(0,1))
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,10)
        id1 = wx.NewIdRef()
        id2 = wx.NewIdRef()
        id3 = wx.NewIdRef()
        id4 = wx.NewIdRef()
        id5 = wx.NewIdRef()
        id6 = wx.NewIdRef()

        def onChoice(evt = None):
            ix = cmdCtrl.GetSelection()
            item = selection[ix]
            ln = len(mainSizer.GetChildren())
            if item[1] == 3:
                id = id2 if item[0] == Group.NowPlaying else id4
                ctrl = wx.FindWindowById(id)
                i = ctrl.GetSelection()
                if i > -1:
                    label = ctrl.GetString(i) + ":"
                    if ln == 8 or item[0] == Group.NowPlaying and ln == 6:
                        lbl = wx.FindWindowById(id5)
                        lbl.SetLabel(label)
                    else:
                        row = len(mainSizer.GetChildren())/2
                        lbl = wx.StaticText(
                            panel,
                            id5,
                            label
                        )
                        mainSizer.Add(lbl, (row, 0))
                        ctrl= wx.TextCtrl(
                            panel,
                            id6,
                            val3 if val3 is not None else "",
                        )
                        mainSizer.Add(ctrl, (row, 1), flag = wx.EXPAND)
                        mainSizer.Layout()
            if evt:
                evt.Skip()

        def onCmdCtrl(evt = None):
            def detachControl(id):
                cntrl = wx.FindWindowById(id)
                mainSizer.Detach(cntrl)
                cntrl.Destroy()

            ln = len(mainSizer.GetChildren())
            sel = cmdCtrl.GetSelection()
            item = list(selection[sel])
            if ln == 8:
                ctrl = wx.FindWindowById(id4)
                ctrl.Unbind(wx.EVT_CHOICE, id = id4)
                detachControl(id6)
                detachControl(id5)
                detachControl(id4)
                detachControl(id3)
                detachControl(id2)
                detachControl(id1)
            elif ln == 6:
                if item[0] == Group.NowPlaying:
                    ctrl = wx.FindWindowById(id2)
                    ctrl.Unbind(wx.EVT_CHOICE, id = id2)
                    detachControl(id6)
                    detachControl(id5)
                else:
                    detachControl(id4)
                    detachControl(id3)
                detachControl(id2)
                detachControl(id1)
            elif ln == 4:
                detachControl(id2)
                detachControl(id1)
            
                
            if len(item) > 4:
                lbl = wx.StaticText(
                    panel,
                    id1,
                    self.plugin.text.labels[item[4]]
                )
                mainSizer.Add(lbl, (1, 0), (1, 1), wx.TOP,3)
                if item[3] & 0x0F == 1: # boolean
                    val = False
                    if evt is None:
                        val = bool(self.val) if self.val is not None else False
                    ctrl = wx.CheckBox(panel, id2, "")
                    ctrl.SetValue(val)
                    mainSizer.Add(ctrl, (1, 1), (1, 1), wx.TOP,3)
                elif item[3] & 0x0F == 2: # integer
                    val = item[-1] if not isinstance(item[-1], dict) else 0
                    if evt is None:
                        val = self.val if self.val is not None else val
                    ctrl = eg.SmartSpinIntCtrl(
                        panel,
                        id2,
                        val,
                        min = item[5],
                        max = item[6]
                    )
                    mainSizer.Add(ctrl, (1, 1))
                elif item[3] & 0x0F == 3: # integer + wx.Choice
                    val = -1
                    if item[2] == 77: #Special case: Set output device
                        data = []
                        if self.plugin.mbHwnd:
                            try:
                                if GetWindowText(self.plugin.mbHwnd) == "Eg2MbMessages":
                                    token = self.plugin.GetToken()
                                    event = CreateEvent(None, 0, 0, None)
                                    self.plugin.queryData[token] = event
                                    data = []
                                    if self.plugin.MusicBeeCmd(96, token, 0):
                                        eg.actionThread.WaitOnEvent(event)
                                        data = self.plugin.queryData[token]
                                        del self.plugin.queryData[token]
                                    else:
                                        del self.plugin.queryData[token]
                            except:
                                pass
                        if data:
                            item = list(item)
                            item.append(dict(enumerate(data[:-1])))
                            if evt is None: #not first opening
                                if isinstance(self.val, (str,unicode)):
                                    if self.val in data[:-1]:
                                        val = data[:-1].index(self.val)
                            if val == -1:
                                val = data.index(data[-1])
                        else:
                            item.append({})
                    elif evt is None:
                        val = self.val if self.val is not None else -1
                    ctrl = wx.Choice(
                        panel,
                        id2,
                        choices = tuple(item[5].itervalues()),
                    )
                    ctrl.SetSelection(val)
                    mainSizer.Add(ctrl, (1, 1))
                    if item[0] == Group.NowPlaying and item[1] == 3:
                        ctrl.Bind(wx.EVT_CHOICE, onChoice, id = id2)
                        onChoice()
                elif item[3] & 0x0F == 4: # file
                    val = ""
                    folder = ""
                    if evt is None:
                        val = self.val if self.val is not None else ""
                        folder = split(val)[0] if val else eg.folderPath.Music
                    mask = text.pMask if item[4] == 17 else text.fMask
                    ctrl = eg.FileBrowseButton(
                        panel,
                        id2,
                        toolTip = text.toolTipFile,
                        dialogTitle = text.browseFile,
                        buttonText = eg.text.General.browse,
                        startDirectory = folder,
                        initialValue = val,
                        fileMask = mask,
                    )
                    ctrl.SetValue(val)
                    mainSizer.Add(ctrl, (1, 1),(1,1),wx.EXPAND)
                elif item[3] & 0x0F == 5: # folder
                    val = ""
                    folder = ""
                    if evt is None:
                        val = self.val if self.val is not None else ""
                        folder = split(val)[0] if val else eg.folderPath.Music
                    mask = text.pMask if item[4] == 17 else text.fMask
                    ctrl = eg.DirBrowseButton(
                        panel,
                        id2,
                        toolTip = self.text.toolTipFolder,
                        dialogTitle = self.text.browseFolder,
                        buttonText = eg.text.General.browse,
                        startDirectory = folder,
                    )
                    ctrl.SetValue(val)
                    mainSizer.Add(ctrl, (1, 1),(1,1),wx.EXPAND)
                if item[3] & 0xF0:
                    offset = (0, 5, 7, 6, 5, 5)[item[3] & 0x0F]
                    lbl = wx.StaticText(
                        panel,
                        id3,
                        self.plugin.text.labels[item[offset]]
                    )
                    mainSizer.Add(lbl, (2, 0),(1, 1), wx.TOP,3)
                if item[3] & 0xF0 == 3 * 16: # integer + wx.Choice
                    ctrl = wx.Choice(
                        panel,
                        id4,
                        choices = tuple(item[offset + 1].itervalues()),
                    )
                    mainSizer.Add(ctrl, (2, 1))
                    ctrl.Bind(wx.EVT_CHOICE, onChoice, id = id4)
                    if evt is None:
                        val2 = self.val2 if self.val2 is not None else -1
                        ctrl.SetSelection(val2)
                        if item[1] == 3 and val2 != -1:
                            onChoice()
                    else:
                        ctrl.SetSelection(-1)
                elif item[3] & 0xF0 == 2 * 16: # integer
                    val2 = item[-1]
                    if evt is None:
                        val2 = self.val2 if self.val2 is not None else item[-1]
                    ctrl = eg.SmartSpinIntCtrl(
                        panel,
                        id4,
                        val2,
                        min = item[-3],
                        max = item[-2]
                    )
                    mainSizer.Add(ctrl, (2, 1))
            else:
                ctrl = None
            if not mainSizer.IsColGrowable(1):
                mainSizer.AddGrowableCol(1)
            mainSizer.Layout()
            if evt:
                evt.Skip()
        onCmdCtrl()
        cmdCtrl.Bind(wx.EVT_CHOICE, onCmdCtrl)

        while panel.Affirmed():
            ix = cmdCtrl.GetSelection()
            item = selection[ix]
            if len(item) > 4 and isinstance(item[3], int):
                ctrl = wx.FindWindowById(id2)
                if item[2] == 77: #Special case: Set output device
                    val = ctrl.GetStringSelection()
                elif item[3] & 0x0F == 1:
                    val = int(ctrl.GetValue())
                elif item[3] & 0x0F in (2, 4, 5):
                    val = ctrl.GetValue()
                elif item[3] & 0x0F == 3:
                    val = ctrl.GetSelection()
                if item[3] & 0xF0:
                    ctrl = wx.FindWindowById(id4)
                    if item[3] & 0xF0 == 3 * 16:
                        val2 = ctrl.GetSelection()
                    elif item[3] & 0xF0 == 2 * 16:
                        val2 = ctrl.GetValue()
                else:
                    val2 = None
            else:
                val = val2 = None
            ctrl = wx.FindWindowById(id6)
            panel.SetResult(
                Commands.index(item),
                val,
                val2,
                ctrl.GetValue() if ctrl else None,
            ) 
#===============================================================================

class Run(eg.ActionBase):

    def __call__(self):
        hWnd = Find_Mb_Main()
        if  hWnd:
            BringHwndToFront(hWnd[0])
        else:
            mp = self.plugin.mbPath
            mp = mp.encode(FSE) if isinstance(mp, unicode) else mp
            if isfile(mp):
                args = [mp]
                Popen(args)    

#===============================================================================

class Exit(eg.ActionClass):

    def __call__(self, stop = False):
        hWnd = Find_Mb_Main()
        if  hWnd:
            PostMessage(hWnd[0], WM_CLOSE, 0, 0)
        else:
            raise self.Exceptions.ProgramNotRunning
#===============================================================================

class plMenu(eg.ActionClass):

    panel = None

    class text:
        OSELabel = 'Menu show on:'
        menuPreview = 'On Screen Menu preview:'
        menuFont = 'Font:'
        txtColour = 'Text colour'
        background = 'Background colour'
        txtColourSel = 'Selected text colour'
        backgroundSel = 'Selected background colour'
        mode = "Queue mode:"
        modes = (
            "Play now",
            "Queue next",
            "Queue last",
            "Queue random",
        )
        inverted = "Use inverted colours"


    def __call__(
        self,
        fore,
        back,
        fontInfo = TAHOMA_INFO,
        monitor = 0,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75),
        inverted = True,
        mode = 0
    ):
       
        hWnd = Find_Mb_Main()
        if  hWnd:
            if not self.plugin.menuDlg:
                event = CreateEvent(None, 0, 0, None)
                token = self.plugin.GetToken()
                self.plugin.queryData[token] = event
                if self.plugin.MusicBeeCmd(63, token, 0):
                    eg.actionThread.WaitOnEvent(event)
                    data = self.plugin.queryData[token]
                    del self.plugin.queryData[token]
                else:
                    del self.plugin.queryData[token] 
                    return
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
                    data,
                    mode,
                )
                eg.actionThread.WaitOnEvent(event)


    def Configure(
        self,
        fore = (75, 75, 75),
        back = (180, 180, 180),
        fontInfo = TAHOMA_INFO,
        monitor = 0,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75),
        inverted = True,
        mode = 0
    ):
        self.fontInfo = fontInfo
        self.fore = fore
        self.back = back
        self.foreSel = foreSel
        self.backSel = backSel
        self.oldSel=0
        self.inverted = inverted
        panel = eg.ConfigPanel(self)
        previewLbl=wx.StaticText(panel, -1, self.text.menuPreview)
        listBoxCtrl = MenuGrid(panel, 3)
        items = {
            "Blahblah_1": "Blahblah_1",
            "Blahblah_2": "Blahblah_2",
            "Blahblah_3": "Blahblah_3"
        }
        listBoxCtrl.Set(items.items())
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
            hght = fontButton.GetFullTextExtent('X')[1]
            if hght > 20:
                break
        listBoxCtrl.SetDefaultCellFont(font)
        fontButton.SetFont(font)            
        listBoxCtrl.SetDefaultRowSize(hght+4, True)
        displayChoice = eg.DisplayChoice(panel, monitor)
        w = displayChoice.GetSize()[0]
        OSElbl = wx.StaticText(panel, -1, self.text.OSELabel)
        useInvertedCtrl = wx.CheckBox(panel, -1, self.text.inverted)
        useInvertedCtrl.SetValue(inverted)
        #Button Text Colour
        foreLbl=wx.StaticText(panel, -1, self.text.txtColour+':')
        foreColourButton = eg.ColourSelectButton(panel,fore,title = self.text.txtColour)
        #Button Background Colour
        backLbl=wx.StaticText(panel, -1, self.text.background+':')
        backColourButton = eg.ColourSelectButton(panel,back,title = self.text.background)
        #Button Selected Text Colour
        foreSelLbl=wx.StaticText(panel, -1, self.text.txtColourSel+':')
        foreSelColourButton = eg.ColourSelectButton(panel,foreSel,title = self.text.txtColourSel)
        #Button Selected Background Colour
        backSelLbl=wx.StaticText(panel, -1, self.text.backgroundSel+':')
        backSelColourButton = eg.ColourSelectButton(panel,backSel,title = self.text.backgroundSel)
        modesLabel = wx.StaticText(panel, -1, self.text.mode)
        modesCtrl = wx.Choice(panel, -1, choices = self.text.modes)
        modesCtrl.SetSelection(mode)
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
        topSizer.Add(modesLabel, (2, 2), flag = wx.TOP,border = 8)
        topSizer.Add(modesCtrl, (3, 2), flag = wx.TOP|wx.EXPAND)
        panel.sizer.Layout()
        wdth = 160
        if (hght+4)*listBoxCtrl.GetNumberRows() > listBoxCtrl.GetSize()[1]: #after Layout() !!!
            wdth -=  SYS_VSCROLL_X
        listBoxCtrl.SetColSize(0, wdth)
        listBoxCtrl.SetGridCursor(-1, 0)
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

        def OnFontBtn(evt):
            value = evt.GetValue()
            self.fontInfo = value
            font = wx.Font(value)
            for n in range(10,20):
                font.SetPointSize(n)
                fontButton.SetFont(font)
                hght = fontButton.GetFullTextExtent('X')[1]
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


        # re-assign the test button
        def OnButton(event):
            hWnd = Find_Mb_Main()
            if  hWnd:
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
                        CreateEvent(None, 0, 0, None),
                        displayChoice.GetSelection(),
                        items,
                        modesCtrl.GetSelection(),
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
            useInvertedCtrl.GetValue(),
            modesCtrl.GetSelection()
        )
#===============================================================================

class trMenu(eg.ActionClass):

    panel = None

    class text:
        OSELabel = 'Menu show on:'
        menuPreview = 'On Screen Menu preview:'
        menuFont = 'Font:'
        txtColour = 'Text colour'
        background = 'Background colour'
        txtColourSel = 'Selected text colour'
        backgroundSel = 'Selected background colour'
        mode = "Queue mode:"
        modes = (
            "Play now",
            "Queue next",
            "Queue last",
            "Queue random",
        )
        inverted = "Use inverted colours"


    def __call__(
        self,
        fore,
        back,
        fontInfo = TAHOMA_INFO,
        monitor = 0,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75),
        inverted = True,
        mode = 0
    ):
       
        hWnd = Find_Mb_Main()
        if  hWnd:
            if not self.plugin.menuDlg:
                event = CreateEvent(None, 0, 0, None)
                token = self.plugin.GetToken()
                self.plugin.queryData[token] = event
                if self.plugin.MusicBeeCmd(72, token, 0):
                    eg.actionThread.WaitOnEvent(event)
                    data = self.plugin.queryData[token]
                    del self.plugin.queryData[token]
                else:
                    del self.plugin.queryData[token] 
                    return
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
                    data,
                    mode + 4,
                )
                eg.actionThread.WaitOnEvent(event)


    def Configure(
        self,
        fore = (75, 75, 75),
        back = (180, 180, 180),
        fontInfo = TAHOMA_INFO,
        monitor = 0,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75),
        inverted = True,
        mode = 0
    ):
        self.fontInfo = fontInfo
        self.fore = fore
        self.back = back
        self.foreSel = foreSel
        self.backSel = backSel
        self.oldSel=0
        self.inverted = inverted
        panel = eg.ConfigPanel(self)
        previewLbl=wx.StaticText(panel, -1, self.text.menuPreview)
        listBoxCtrl = MenuGrid(panel, 3)
        items = {
            "Blahblah_1": "Blahblah_1",
            "Blahblah_2": "Blahblah_2",
            "Blahblah_3": "Blahblah_3"
        }
        listBoxCtrl.Set(items.items())
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
            hght = fontButton.GetFullTextExtent('X')[1]
            if hght > 20:
                break
        listBoxCtrl.SetDefaultCellFont(font)
        fontButton.SetFont(font)            
        listBoxCtrl.SetDefaultRowSize(hght+4, True)
        displayChoice = eg.DisplayChoice(panel, monitor)
        w = displayChoice.GetSize()[0]
        OSElbl = wx.StaticText(panel, -1, self.text.OSELabel)
        useInvertedCtrl = wx.CheckBox(panel, -1, self.text.inverted)
        useInvertedCtrl.SetValue(inverted)
        #Button Text Colour
        foreLbl=wx.StaticText(panel, -1, self.text.txtColour+':')
        foreColourButton = eg.ColourSelectButton(panel,fore,title = self.text.txtColour)
        #Button Background Colour
        backLbl=wx.StaticText(panel, -1, self.text.background+':')
        backColourButton = eg.ColourSelectButton(panel,back,title = self.text.background)
        #Button Selected Text Colour
        foreSelLbl=wx.StaticText(panel, -1, self.text.txtColourSel+':')
        foreSelColourButton = eg.ColourSelectButton(panel,foreSel,title = self.text.txtColourSel)
        #Button Selected Background Colour
        backSelLbl=wx.StaticText(panel, -1, self.text.backgroundSel+':')
        backSelColourButton = eg.ColourSelectButton(panel,backSel,title = self.text.backgroundSel)
        modesLabel = wx.StaticText(panel, -1, self.text.mode)
        modesCtrl = wx.Choice(panel, -1, choices = self.text.modes[:-1])
        modesCtrl.SetSelection(mode)
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
        topSizer.Add(modesLabel, (2, 2), flag = wx.TOP,border = 8)
        topSizer.Add(modesCtrl, (3, 2), flag = wx.TOP|wx.EXPAND)
        panel.sizer.Layout()
        wdth = 160
        if (hght+4)*listBoxCtrl.GetNumberRows() > listBoxCtrl.GetSize()[1]: #after Layout() !!!
            wdth -=  SYS_VSCROLL_X
        listBoxCtrl.SetColSize(0, wdth)
        listBoxCtrl.SetGridCursor(-1, 0)
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

        def OnFontBtn(evt):
            value = evt.GetValue()
            self.fontInfo = value
            font = wx.Font(value)
            for n in range(10,20):
                font.SetPointSize(n)
                fontButton.SetFont(font)
                hght = fontButton.GetFullTextExtent('X')[1]
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

        # re-assign the test button
        def OnButton(event):
            hWnd = Find_Mb_Main()
            if  hWnd:
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
                        CreateEvent(None, 0, 0, None),
                        displayChoice.GetSelection(),
                        items,
                        4 + modesCtrl.GetSelection(),
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
            useInvertedCtrl.GetValue(),
            modesCtrl.GetSelection()
        )
#===============================================================================

class seek(eg.ActionBase):
    class text:
        label = "Seek value:"
        unit = "Unit"
        unitChoice = ("Second", "Percent")
        pos = "Positioning"
        posChoice = ("Relatively", "Absolutely")
        dir = "Direction"
        dirChoice = ("Forward", "Backward")


    def __call__(self, value = 5, unit = 1, pos = 0, dir = 0):
        value = value if isinstance(value, int) else self.plugin.str2int(value)
        dir = 0 if pos else dir
        return self.plugin.MusicBeeCmd(
            70 + 65536 * unit + 131072 * pos + 262144 * dir,
            0, 
            value
        )


    def GetLabel(self, value, unit, pos, dir):
        if pos:
            return "%s: %s%s, %s" % (self.name,value,("","%")[unit],self.text.posChoice[pos])
        else:
            return "%s: %s%s, %s, %s" % (self.name,value,("","%")[unit],self.text.posChoice[pos],self.text.dirChoice[dir])


    def Configure(self, value = 5, unit = 1, pos = 0, dir = 0):
        text = self.text
        panel = eg.ConfigPanel()
        mySizer = wx.BoxSizer(wx.VERTICAL)
        panel.sizer.Add(mySizer,1,wx.EXPAND|wx.LEFT,10)
        width = 120
        staticText = panel.StaticText(text.label)
        valueCtrl = eg.SmartSpinIntCtrl(
                        panel,
                        -1,
                        value,
                        min = 0,
                        max = 65535
                    )
        unitSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.unit), 
            wx.HORIZONTAL
        )
        rb1 = panel.RadioButton(not unit, text.unitChoice[0], style=wx.RB_GROUP, size = (width,-1))
        rb2 = panel.RadioButton(unit, text.unitChoice[1])                            
        unitSizer.Add(rb1, 1)
        unitSizer.Add(rb2, 1)
        posSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.pos), 
            wx.HORIZONTAL
        )
        rb3 = panel.RadioButton(not pos, text.posChoice[0], style=wx.RB_GROUP, size = (width,-1))
        rb4 = panel.RadioButton(pos, text.posChoice[1])                            
        posSizer.Add(rb3, 1)
        posSizer.Add(rb4, 1)

        dirSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.dir), 
            wx.HORIZONTAL
        )
        rb5 = panel.RadioButton(not dir, text.dirChoice[0], style=wx.RB_GROUP, size = (width,-1))
        rb6 = panel.RadioButton(dir, text.dirChoice[1])                            
        dirSizer.Add(rb5, 1)
        dirSizer.Add(rb6, 1)

        def OnRadioButton(event=None):
            flag = rb3.GetValue()
            mySizer.Show(dirSizer,flag,True)
            mySizer.Layout()
            if event:
                event.Skip()
        rb3.Bind(wx.EVT_RADIOBUTTON, OnRadioButton)
        rb4.Bind(wx.EVT_RADIOBUTTON, OnRadioButton)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(staticText, 0, wx.TOP, 3)
        topSizer.Add(valueCtrl, 0, wx.LEFT, 10)
        mySizer.Add(topSizer, 0, wx.TOP, 5)
        mySizer.Add(unitSizer, 0, wx.TOP, 12)
        mySizer.Add(posSizer, 0, wx.TOP, 12)
        mySizer.Add(dirSizer, 0, wx.TOP, 12)
        OnRadioButton()
        while panel.Affirmed():
            panel.SetResult(
                valueCtrl.GetValue(),
                rb2.GetValue(),
                rb4.GetValue(),
                rb6.GetValue(),
                )
#====================================================================

class AddSongToPlaylist(eg.ActionBase):

    def __call__(self, plString = "", skip = False, filename = ""):
        plString = eg.ParseString(plString)
        if self.value:
            filename = eg.ParseString(filename)
        hWnd = Find_Mb_Main()
        if  hWnd:
            data = self.plugin.GetPlaylists(True)
            if plString in data:
                url = data[plString]
                msg = "%s|%s" % (url, filename) if self.value else url
                cmd = 76 + self.value
                res = self.plugin.MusicBeeStringCmd(cmd, msg) if url else 0
                if skip:
                    self.plugin.MusicBeeCmd(3)
                return res
            else:
                eg.PrintError(self.text.msg2 % plString)



    def Configure(self, plString = "", skip = False, filename = ""):
        panel = eg.ConfigPanel(self)
        text = self.text
        hWnd = Find_Mb_Main()
        if hWnd:
            mainSizer = wx.GridBagSizer(18, 5)
            if self.value:
                fileLabel = wx.StaticText(panel, -1, text.filename)
                fileCtrl = wx.TextCtrl(panel, -1, filename)
                mainSizer.Add(fileLabel,(0, 0), flag = wx.TOP, border = 2)
                mainSizer.Add(fileCtrl,(0, 1), flag = wx.EXPAND)
            data = self.plugin.GetPlaylists(True)
            data = tuple(data.iteritems())
            choices = [i[0] for i in data if not i[1].endswith("xautopf")]
            choices.sort()
            pllstLabel = wx.StaticText(panel, -1, text.playlistName)
            pllstCtrl = wx.ComboBox(panel, -1, choices = choices, style = wx.CB_DROPDOWN )
            pllstCtrl.SetValue(plString)
            skipChkBoxCtrl = wx.CheckBox(panel, label = self.text.skip)
            skipChkBoxCtrl.SetValue(skip)
            mainSizer.Add(pllstLabel,(self.value, 0), flag = wx.TOP, border = 2)
            mainSizer.Add(pllstCtrl,(self.value, 1), flag = wx.EXPAND)
            mainSizer.Add(skipChkBoxCtrl, (self.value+1, 0), (1, 2))
            mainSizer.AddGrowableCol(1)
            panel.sizer.Add(mainSizer, 0, wx.ALL|wx.EXPAND, 10)

        else:
            lbl = wx.StaticText(panel, -1, text.msg1)
            font = lbl.GetFont()
            #font.SetWeight(wx.FONTWEIGHT_BOLD )
            font.SetPointSize(2 * font.GetPointSize())
            lbl.SetFont(font)
            lbl.SetForegroundColour(wx.RED)
            panel.sizer.Add(lbl, 0, wx.ALL, 10)
            panel.dialog.buttonRow.testButton.Show(False)


        while panel.Affirmed():
            if self.value:
                filename = fileCtrl.GetValue()
            if hWnd:
                plString = pllstCtrl.GetValue()
                skip = skipChkBoxCtrl.GetValue()
            panel.SetResult(plString, skip, filename)

    class text:
        filename = "Song file name:"
        playlistName = "Playlist name:"
        skip = "Skip to next track"
        msg1 = "MusicBee must be running !"
        msg2 = 'Playlist "%s" not exists in current library'
#===============================================================================

class IsRunning(eg.ActionBase):

    class text:
        stopMode = "Stop macro if"
        stopChoices = [
            "MusicBee is not running",
            "MusicBee is running",
            "Never"
        ]


    def __call__(self, stop = 0):
        flag = self.plugin.mbHwnd is not None
        if (
            (stop == 0 and not flag)
            or (stop == 1 and flag)
        ):
            eg.programCounter = None
        return flag


    def GetLabel(self, stop):
        text = self.text
        return "%s: %s %s" % (self.name, text.stopMode, text.stopChoices[stop])


    def Configure(self, stop = 0):
        text = self.text
        panel = eg.ConfigPanel()
        radioBoxStop = wx.RadioBox(
            panel,
            -1,
            text.stopMode + " ...",
            choices = text.stopChoices,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxStop.SetSelection(stop)
        panel.sizer.Add(radioBoxStop,0,wx.ALL,10)

        while panel.Affirmed():
            panel.SetResult(
                radioBoxStop.GetSelection(),
            )
#===============================================================================

ACTIONS = (
    (Run, "Run", "Run MusicBee", "Run MusicBee application." , None),
    (Exit, 'Exit', 'Exit MusicBee', 'Exit MusicBee.', None ),
    (IsRunning,
        'IsRunning',
        'Get "Is running"',
        'Returns MusicBee running status.', None
    ),
    (mbCommand,
        "PlayerCommand",
        "Player command",
        "Player command",
        Group.Player
    ),
    ( mbCommand,
        "NowPlayingCommand",
        "Now playing command",
        "Now playing command",
        Group.NowPlaying
    ),
    (mbCommand,
        "NowPlayingListCommand",
        "Now playing list command",
        "Now playing list command",
        Group.NowPlayingList
    ),
    (mbCommand,
        "LibraryCommand",
        "Library command",
        "Library command",
        Group.Library
    ),
    (mbCommand,
        "PlaylistCommand",
        "Playlist command",
        "Playlist command",
        Group.Playlist
    ),
    (mbCommand,
        "FolderCommand",
        "Folder command",
        "Folder command",
        Group.Folder
    ),
    (plMenu,
        "PlaylistMenu",
        "Playlist menu",
        "Playlist menu",
        None
    ),
    (trMenu,
        "TrackMenu",
        "Track menu",
        "Track menu",
        None
    ),
    (seek,
        "Seek",
        "Seek",
        "Seek",
        None
    ),
    (AddSongToPlaylist,
        "AddSongToPlaylist",
        "Add a song to playlist",
        "Adds a song to a specific playlist.",
        1
    ),
    (AddSongToPlaylist,
        "AddCurrentSongToPlaylist",
        "Add currently playing song to playlist",
        "Adds the currently playing song to a specific playlist.",
        0
    ),
)

#===============================================================================
