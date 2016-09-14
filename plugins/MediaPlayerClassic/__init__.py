# -*- coding: utf-8 -*-
#
# plugins/MediaPlayerClassic/__init__.py
#
# Copyright (C) 2006 MonsterMagnet
#
# This file is a plugin for EventGhost.
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

# Changelog (in reverse chronological order):
# -------------------------------------------
# 2.12 by Pako 2016-04-17 18:59 UTC+1
#     - added option: "NowPlaying" event is only trigerred when the payload is changed
#     - added action "Get play-state"
# 2.11 by Pako 2016-04-17 07:31 UTC+1
#     - bugfix - program crashes when you try to open the OSD menu in fullscreen
# 2.10 by Pako 2016-03-19 09:12 UTC+1
#     - bugfix - GetWindowState() - when fullscreen is set in a maximized state
# 2.9 by Pako 2015-01-12 19:23 UTC+1
#     - bugfix - Find_MPC() function now works also in 64-bit system
# 2.8 by Pako 2014-12-26 10:38 UTC+1
#     - bugfix - the function GetMpcHcPath() improved
# 2.7 by Pako 2014-12-18 08:09 UTC+1
#     - bugfix (Show menu - Test button)
# 2.6 by Pako 2013-02-10 10:56 UTC+1
#     - the function GetMpcHcPath() improved - now works also in x64 environment
# 2.5 by Pako 2013-02-08 19:05 UTC+1
#     - we must wait with the connection, if MPC-HC is "Not responding"
# 2.4 by Pako 2012-12-02 16:01 UTC+1
#     - added "Stop processing event" feature (Menu and GoTo frames)
# 2.3 by Pako 2012-09-10 08:15 UTC+1
#     - the function GetMpcHcPath() changed,
#       due to HKEY_LOCAL_MACHINE -> HKEY_CURRENT_USER change
# 2.2 by Pako 2012-08-19 12:21 UTC+1
#     - Added the event "MPC-HC.Connected"
#     - eg.scheduler.CancelTask added, when plugin is stopped
# 2.1 by Pako 2012-08-19 12:21 UTC+1
#     - bugfixes
# 2.0 by Pako 2012-08-17 12:23 UTC+1
#     - Corrected ID at many actions
#     - Added many new actions
#     - Plugin now automatically triggers events
# 1.7 by Pako 2012-01-06 15:18 UTC+1
#     - Added actions GetWindowState and GetNowPlaying
# 1.6 by Pako 2011-06-05 18:57 UTC+1
#     - Used eg.EVT_VALUE_CHANGED instead of EVT_BUTTON_AFTER
# 1.5 by Pako
#     - bugfix (On Screen GoTo is always on primary monitor)
# 1.4 by Pako
#     - bugfix (ShowMenu when fullscreen is on second monitor)
# 1.3 by Pako
#     - added actions:
#                      Get Times
#                      Show Menu
#                      On Screen GoTo
#     - deleted action:
#                      Get recent files (replaced Show Menu)
# 1.2 by Pako
#     - added actions: Toggle OSD Elapsed Time
#                      Open Directory
#                      Send user message
#                      Get recent files
# 1.1 by bitmonster
#     - changed code to use new AddActionsFromList
# 1.0 by MonsterMagnet
#     - initial version

eg.RegisterPlugin(
    name = "Media Player Classic",
    author = "MonsterMagnet",
    version = "2.12",
    kind = "program",
    guid = "{DD75104D-D586-438A-B63D-3AD01A4D4BD3}",
    createMacrosOnAdd = True,
    description = (
        'Adds actions to control '
        '<br><a href="http://mpc-hc.sourceforge.net/">'
        'Media Player Classic - Home Cinema</a>.'
    ),
    help = """
        For proper functioning of this plugin should be used
        <br><a href="http://mpc-hc.sourceforge.net/">
        Media Player Classic - Home Cinema (x86/x64)</a>
        <br>version 1.6.3.5818 or later.
        <br><br>There must be selected the option
        <br><b> Use the same player for each media file</b>
        <br>in dialogue <i>View/Options.../Player/Open options.</i>""",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAhElEQVR42rWRgQqAIAwF"
        "fV+++eWr1V6kiM6gQaTVHYehJEdV7bUG18hCInIDQMNhA+L7cQHBETQrBWERDXANjcxm"
        "Ee6CyFxd6ArkynZT5l7KK9gFbs3CrGgEPLzM1FonAn9kz59stqhnhdhEwK/j3m0Tgj8K"
        "OPmCr4eYpmMaASt3JS44ADcFoxFdcIMPAAAAAElFTkSuQmCC"
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=694"
)
#===============================================================================

import eg
import wx
import _winreg
from os import environ
from os.path import join, exists, isfile, split, isabs
from subprocess import Popen
from eg.WinApi import SendMessageTimeout, WM_COMMAND
from eg.WinApi.Utils import GetMonitorDimensions
from win32api import EnumDisplayMonitors
from eg.WinApi.Dynamic import PostMessage
from eg.WinApi.Dynamic import CreateEvent, SetEvent, GetWindowLong
from threading import Timer
from win32gui import GetMenu, GetSubMenu, GetMenuItemCount, GetWindowPlacement
from win32gui import GetClassName, GetWindowText, IsWindowVisible, GetWindowRect
from win32gui import GetDlgItem, SendMessage, FindWindow, IsWindow
from copy import deepcopy as cpy
from time import sleep, strftime, gmtime
from winsound import PlaySound, SND_ASYNC
from ctypes import create_unicode_buffer, addressof, windll, c_int, c_buffer, sizeof
import wx.grid as gridlib
from eg.WinApi.Dynamic import COPYDATASTRUCT, PCOPYDATASTRUCT, WM_COPYDATA
from ctypes import Structure, cast, wstring_at, c_wchar, c_void_p
from sys import getfilesystemencoding
FSE = getfilesystemencoding()
from eg.Classes.MainFrame.TreeCtrl import DropTarget as EventDropTarget

GWL_EXSTYLE      = -20
WS_EX_WINDOWEDGE = 0x00000100
WM_INITMENUPOPUP = 0x0117
MF_GRAYED        = 1
MF_DISABLED      = 2
MF_CHECKED       = 8
MF_BYPOSITION    = 1024
SYS_VSCROLL_X    = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
SYS_HSCROLL_Y    = wx.SystemSettings.GetMetric(wx.SYS_HSCROLL_Y)
arialInfoString  = "0;-35;0;0;0;700;0;0;0;0;3;2;1;34;Arial"
WM_CLOSE         = 16
#===============================================================================

def Find_MPC():
    mpchc = eg.WindowMatcher(
        u'mpc-hc{*}.exe',
        None,
        u'MediaPlayerClassicW',
        None,
        None,
        None,
        True,
        0.0,
        2
    )
    return mpchc()
#===============================================================================

class MPC_OSDDATA(Structure):
    _fields_ = [
        ("nMsgPos", c_int),       #// screen position constant (see OSD_MESSAGEPOS constants)
        ("nDurationMS", c_int),   #// duration in milliseconds
        ("strMsg", c_wchar * 128) #// message to display thought OSD
    ]
OSDDATA = MPC_OSDDATA()
#===============================================================================

MPC_LOADSTATE = ("Closed", "Loading", "Loaded", "Closing")

MPC_PLAYSTATE = ("Play", "Pause", "Stop", "Unused")

CMD_CONNECT            = 0x50000000 #Par 1 : MPC window handle (command should be send to this HWnd)

CMD_STATE              = 0x50000001 #Par 1 : current state /see MPC_LOADSTATE enum

CMD_PLAYMODE           = 0x50000002 #Par 1 : current play mode (see MPC_PLAYSTATE enum)

CMD_NOWPLAYING         = 0x50000003 #;   // Send after opening a new file
                                    #   // Par 1 : title
                                    #   // Par 2 : author
                                    #   // Par 3 : description
                                    #   // Par 4 : complete filename (path included)
                                    #   // Par 5 : duration in seconds

CMD_LISTSUBTITLETRACKS = 0x50000004 #   // List of subtitle tracks
                                    #   // Par 1 : Subtitle track name 0
                                    #   // Par 2 : Subtitle track name 1
                                    #   // ...
                                    #   // Par n : Active subtitle track, -1 if subtitles disabled
                                    #   //
                                    #   // if no subtitle track present, returns -1
                                    #   // if no file loaded, returns -2

CMD_LISTAUDIOTRACKS    = 0x50000005 #   // List of audio tracks
                                    #   // Par 1 : Audio track name 0
                                    #   // Par 2 : Audio track name 1
                                    #   // ...
                                    #   // Par n : Active audio track
                                    #   //
                                    #   // if no audio track present, returns -1
                                    #   // if no file loaded, returns -2

CMD_PLAYLIST           = 0x50000006 #   // List of files in the playlist
                                    #   // Par 1 : file path 0
                                    #   // Par 2 : file path 1
                                    #   // ...
                                    #   // Par n : active file, -1 if no active file

CMD_CURRENTPOSITION     = 0x50000007
     #Send current playback position in responce
     #of CMD_GETCURRENTPOSITION.
     #Par 1 : current position in seconds


CMD_NOTIFYSEEK          = 0x50000008
     #Send the current playback position after a jump.
     #(Automatically sent after a seek event).
     #Par 1 : new playback position (in seconds).

CMD_NOTIFYENDOFSTREAM   = 0x50000009
     #Notify the end of current playback
     #(Automatically sent).
     #Par 1 : none.

# ==== Commands from host to MPC

# Open new file
# Par 1 : file path
CMD_OPENFILE            = 0xA0000000

# Stop playback but keep file / playlist
CMD_STOP                = 0xA0000001

# Stop playback and close file / playlist
CMD_CLOSEFILE           = 0xA0000002

# Pause or restart playback
CMD_PLAYPAUSE           = 0xA0000003

# Add a new file to playlist (did not start playing)
# Par 1 : file path
CMD_ADDTOPLAYLIST       = 0xA0001000

# Remove all files from playlist
CMD_CLEARPLAYLIST       = 0xA0001001

# Start playing playlist
CMD_STARTPLAYLIST       = 0xA0001002

CMD_REMOVEFROMPLAYLIST  = 0xA0001003    # TODO

# Cue current file to specific position
# Par 1 : new position in seconds
CMD_SETPOSITION         = 0xA0002000

# Set the audio delay
# Par 1 : new audio delay in ms
CMD_SETAUDIODELAY       = 0xA0002001

# Set the subtitle delay
# Par 1 : new subtitle delay in ms
CMD_SETSUBTITLEDELAY    = 0xA0002002

# Set the active file in the playlist
# Par 1 : index of the active file -1 for no file selected
# DOESN'T WORK
CMD_SETINDEXPLAYLIST    = 0xA0002003

# Set the audio track
# Par 1 : index of the audio track
CMD_SETAUDIOTRACK       = 0xA0002004

# Set the subtitle track
# Par 1 : index of the subtitle track -1 for disabling subtitles
CMD_SETSUBTITLETRACK    = 0xA0002005

# Ask for a list of the subtitles tracks of the file
# return a CMD_LISTSUBTITLETRACKS
CMD_GETSUBTITLETRACKS   = 0xA0003000

# Ask for the current playback position
# see CMD_CURRENTPOSITION.
# Par 1 : current position in seconds
CMD_GETCURRENTPOSITION  = 0xA0003004

# Jump forward/backward of N seconds
# Par 1 : seconds (negative values for backward)
CMD_JUMPOFNSECONDS      = 0xA0003005

# Ask for a list of the audio tracks of the file
# return a CMD_LISTAUDIOTRACKS
CMD_GETAUDIOTRACKS      = 0xA0003001

# Ask for the properties of the current loaded file
# return a CMD_NOWPLAYING
CMD_GETNOWPLAYING       = 0xA0003002

# Ask for the current playlist
# return a CMD_PLAYLIST
CMD_GETPLAYLIST         = 0xA0003003

# Toggle FullScreen
CMD_TOGGLEFULLSCREEN    = 0xA0004000

# Jump forward(medium)
CMD_JUMPFORWARDMED      = 0xA0004001

# Jump backward(medium)
CMD_JUMPBACKWARDMED     = 0xA0004002

# Increase Volume
CMD_INCREASEVOLUME      = 0xA0004003

# Decrease volume
CMD_DECREASEVOLUME      = 0xA0004004

# Shader toggle
CMD_SHADER_TOGGLE       = 0xA0004005

# Close App
CMD_CLOSEAPP            = 0xA0004006

# show host defined OSD message string
CMD_OSDSHOWMESSAGE      = 0xA0005000
#===============================================================================

class FixedWidth(wx.FontEnumerator):

    def __init__(self):
        wx.FontEnumerator.__init__(self)
        self.fontList = []

    def OnFacename(self, fontname):
        if not fontname.startswith("@"):
            self.fontList.append(fontname)
#===============================================================================

def GetSec(timeStr):
    sec = int(timeStr[-2:])
    min = timeStr[-5:-3]
    hr = timeStr[-8:-6]
    if min:
        sec += 60*int(min)
    if hr:
        sec += 3600*int(hr)
    return sec
#===============================================================================

def GetItemList(menu, hWnd):
    SendMessage(hWnd, WM_INITMENUPOPUP, menu, 0) #REFRESH MENU STATE !!!
    itemList = []
    itemName = c_buffer("\000" * 128)
    count = GetMenuItemCount(menu)
    for i in range(count):
        windll.user32.GetMenuStringA(c_int(menu),
                                     c_int(i),
                                     itemName,
                                     c_int(len(itemName)),
                                     MF_BYPOSITION)
        menuState = windll.user32.GetMenuState(c_int(menu),
                                               c_int(i),
                                               MF_BYPOSITION)
        id = windll.user32.GetMenuItemID(c_int(menu), c_int(i))
        if menuState & (MF_GRAYED|MF_DISABLED):
            continue
        item = itemName.value.replace("&","").split("\t")[0]
        if item == "" and id == 0:
            continue
        checked = bool(menuState & MF_CHECKED)
        if isabs(item):
            if not isfile(item):
                continue
            else:
                item = split(item)[1]
        itemList.append((item, i, checked, id))
    return itemList
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
        self.il.Add(wx.BitmapFromImage(wx.Image(join(eg.imagesDir, "event.png"), wx.BITMAP_TYPE_PNG)))
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

class GoToFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(
            self,
            None,
            -1,
            'MPCgotoFrame',
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
            pos = self.pos
            self.GoToCtrl.SetStyle(0, pos, wx.TextAttr(self.fore, self.back, self.fnt))
            self.GoToCtrl.SetStyle(pos, pos+1, wx.TextAttr(self.foreSel, self.backSel, self.fnt))
            self.GoToCtrl.SetStyle(pos+1, 8, wx.TextAttr(self.fore, self.back, self.fnt))
            f = self.fore
            b = self.back
        else:
            self.GoToCtrl.SetStyle(0, 8, wx.TextAttr(self.fore, self.back, self.fnt))
            f = self.foreSel
            b = self.backSel
        self.gotoLbl.SetBackgroundColour(b)
        self.gotoLbl.SetForegroundColour(f)
        self.Refresh()


    def MoveCursor(self, step):
        max = len(self.posList)-1
        ix = self.posList.index(self.pos)
        ix += step
        if ix > max:
            ix = 0
        elif ix == -1:
            ix = max
        self.pos = self.posList[ix]
        wx.CallAfter(self.UpdateOSD)


    def Turn(self, step):
        min = 0
        max = 9
        if self.pos == -1:
            self.GoTo()
            return
        pos = self.pos
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
        newTime =''.join(data)
        if newTime<self.total:
            wx.CallAfter(self.UpdateOSD, newTime)


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
        eg.TriggerEvent("OSD.%s" % self.plugin.text.opened, prefix = "MPC")
        self.flag = False
        self.Bind(wx.EVT_CLOSE, self.onClose)
        child = GetDlgItem(hWnd, 10021)
        self.total = "99:99:99"
        if GetClassName(child) ==  "#32770":
            statText = GetDlgItem(child, 12027)
            if GetClassName(statText) ==  "Static":
                try:
                    elaps, total = GetWindowText(statText).split(" / ")
                except:
                    self.plugin.menuDlg = None
                    return
                totalSec = GetSec(total)
                self.total = strftime('%H:%M:%S', gmtime(totalSec))
                if totalSec < 600:                # < 10 min   (skip 3 digits)
                    self.posList = (-1,4,6,7)
                elif totalSec < 3600:             # < 1 hour   (skip 2 digits)
                    self.posList = (-1,3,4,6,7)
                elif totalSec < 360000:           # < 10 hour  (skip 1 digit)
                    self.posList = (-1,1,3,4,6,7)
                else:
                    self.posList = (-1,0,1,3,4,6,7)  # >= 10 hour  (no skip)
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
        label = self.plugin.text.gotoLabel
        self.gotoLbl=wx.StaticText(self, -1, label, pos = (5,5))
        self.gotoLbl.SetBackgroundColour(self.back)
        self.gotoLbl.SetForegroundColour(self.fore)
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
        data = "%s%s" % ("00:00:00"[:8-len(elaps)],elaps)
        gotoSize = self.GoToCtrl.GetTextExtent(data)
        wx.CallAfter(self.UpdateOSD, data)
        if sizeFlag:
            gotoSize = (1.4 * gotoSize[0],gotoSize[1])
        self.GoToCtrl.SetSize(gotoSize)
        self.GoToCtrl.SetPosition((border, 1.5*border+labelSize[1]))
        self.SetSize((4+gotoSize[0]+2*border,2+labelSize[1]+gotoSize[1]+2.5*border))
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
        self.gotoLbl.SetFocus()
        if self.flag:
            self.timer=MyTimer(t = 5.0, plugin = self.plugin)
        wx.Yield()
        SetEvent(event)


    def onUp(self, event):
        wx.CallAfter(self.Turn, 1)
        return True #stop processing this event !!!


    def onDown(self, event):
        wx.CallAfter(self.Turn, -1)
        return True #stop processing this event !!!


    def onLeft(self, event):
        wx.CallAfter(self.MoveCursor, -1)
        return True #stop processing this event !!!


    def onRight(self, event):
        wx.CallAfter(self.MoveCursor, 1)
        return True #stop processing this event !!!


    def onEscape(self, event):
        wx.CallAfter(self.destroyMenu)
        return True #stop processing this event !!!


    def GoTo(
        self,
    ):
        data = self.GoToCtrl.GetValue()
        if data >= self.total:
            return
        wx.CallAfter(
            self.plugin.SendCopydata,
            CMD_SETPOSITION,
            str(GetSec(data))
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
        eg.TriggerEvent("OSD.%s" % self.plugin.text.closed, prefix = "MPC")
        self.Close()
#===============================================================================

class MenuEventsDialog(wx.MiniFrame):

    def __init__(self, parent, plugin):
        wx.MiniFrame.__init__(
            self,
            parent,
            -1,
            style=wx.CAPTION,
            name="MenuEventsDialog"
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

class Menu(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(
            self,
            None,
            -1,
            'MPC_menu',
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
        eg.TriggerEvent("OSD.%s" % self.plugin.text.opened, prefix = "MPC")
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
        if self.plugin.GetWindowState() == 4: # Fullscreen !
            SendMessageTimeout(self.hWnd, WM_COMMAND, 830, 0)
            self.messStack.append(830)
            sleep(0.1)
        self.menu = GetMenu(hWnd)
        while not self.menu:
            SendMessageTimeout(self.hWnd, WM_COMMAND, 817, 0)
            self.messStack.append(817)
            sleep(0.1)
            self.menu = GetMenu(hWnd)
        self.items = GetItemList(self.menu, self.hWnd)
        self.choices = [item[0] for item in self.items]
        self.menuGridCtrl = MenuGrid(self,len(self.choices))
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        mainSizer.Add(self.menuGridCtrl, 0, wx.EXPAND)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(gridlib.EVT_GRID_CMD_CELL_LEFT_DCLICK, self.onDoubleClick, self.menuGridCtrl)
        self.Bind(wx.EVT_CHAR_HOOK, self.onFrameCharHook)
        font = wx.FontFromNativeInfoString(fontInfo)
        self.menuGridCtrl.SetFont(font)
        arial = wx.FontFromNativeInfoString(arialInfoString)
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
        self.DrawMenu(ix)
        wx.Yield()
        SetEvent(event)


    def UpdateMenu(self, ix=0):
        self.items = GetItemList(self.menu, self.hWnd)
        if len(self.items)==0:
            PlaySound('SystemExclamation', SND_ASYNC)
            self.menu,ix = self.oldMenu.pop()
            self.items = GetItemList(self.menu, self.hWnd)
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
            self.menu, ix = self.oldMenu.pop()
            wx.CallAfter(self.UpdateMenu, ix)
        else:
            wx.CallAfter(self.destroyMenu)
        return True #stop processing this event !!!


    def onRight(self, event):
        wx.CallAfter(self.DefaultAction)
        return True #stop processing this event !!!


    def onEscape(self, event):
        wx.CallAfter(self.destroyMenu)
        return True #stop processing this event !!!


    def DefaultAction(self):
        sel = self.menuGridCtrl.GetSelection()
        item = self.items[sel]
        id = item[3]
        if id != -1:
            self.destroyMenu()
            SendMessage(self.hWnd, WM_COMMAND, id, 0)
        else:
            self.oldMenu.append((self.menu,sel))
            self.menu = GetSubMenu(self.menu, item[1])
            self.UpdateMenu()


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
                self.menu, ix = self.oldMenu.pop()
                wx.CallAfter(self.UpdateMenu,ix)
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
        cnt = self.messStack.count(817)
        if cnt:
            for i in range(4 - cnt):
                SendMessageTimeout(self.hWnd, WM_COMMAND, 817, 0)
        if self.messStack.count(830):
            SendMessageTimeout(self.hWnd, WM_COMMAND, 830, 0)
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
        if self.flag:
            self.timer.Cancel()
        eg.TriggerEvent("OSD.%s" % self.plugin.text.closed, prefix = "MPC")
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

class AfterPlaybackOnce(eg.ActionClass):

    class text:
        label = "Select action after playback:"
        choices = (
            "Exit",
            "Stand By",
            "Hibernate",
            "Shutdown",
            "Log Off",
            "Lock"
        )


    def __call__(self, action = -1):
        if action > -1:
            if self.plugin.runFlg and self.plugin.mpcHwnd:
                return SendMessage(self.plugin.mpcHwnd, WM_COMMAND, action + 912, 0)
            else:
                raise self.Exceptions.ProgramNotRunning


    def GetLabel(self, action):
        return "%s: %s" % (self.name, self.text.choices[action])


    def Configure(self, action = -1):
        panel = eg.ConfigPanel()
        label = wx.StaticText(panel, -1, self.text.label)
        ctrl = wx.Choice(panel, -1, choices = self.text.choices)
        eg.EqualizeWidths((label, ctrl))
        ctrl.SetSelection(action)
        panel.sizer.Add(label, 0, wx.TOP, 20)
        panel.sizer.Add(ctrl, 0, wx.TOP, 3)
        while panel.Affirmed():
            panel.SetResult(ctrl.GetSelection())
#===============================================================================

class AfterPlayback(eg.ActionClass):

    class text:
        label = "Select action after playback (every time):"
        choices = (
            "Exit",
            "Do Nothing",
            "Play next in the folder",
        )


    def __call__(self, action = -1):
        if action > -1:
            if self.plugin.runFlg and self.plugin.mpcHwnd:
                ids = (33411, 918, 33412)
                return SendMessageTimeout(
                    self.plugin.mpcHwnd,
                    WM_COMMAND,
                    ids[action],
                    0
                )
            else:
                raise self.Exceptions.ProgramNotRunning


    def GetLabel(self, action):
        return "%s: %s" % (self.name, self.text.choices[action])


    def Configure(self, action = -1):
        panel = eg.ConfigPanel()
        label = wx.StaticText(panel, -1, self.text.label)
        ctrl = wx.Choice(panel, -1, choices = self.text.choices)
        eg.EqualizeWidths((label, ctrl))
        ctrl.SetSelection(action)
        panel.sizer.Add(label, 0, wx.TOP, 20)
        panel.sizer.Add(ctrl, 0, wx.TOP, 3)
        while panel.Affirmed():
            panel.SetResult(ctrl.GetSelection())
#===============================================================================

class UserMessage(eg.ActionClass):

    name = "Send user's message"
    description = u"""<rst>**Sends user's message.**

If you can not find in the menu of features some of the functions you can get it (maybe) add yourself.
Go to the menu "**View - Options... - Player - Hotkeys**".
If you find there a function, what you need, then write the number that is in the column "**ID**".
Type this number into the edit box "**User message ID:**".
You can of course also use an expression such as **{eg.result}** or **{eg.event.payload}**."""


    class text:
        label = "User message ID:"
        error = "ValueError: invalid literal for int() with base 10: '%s'"



    def __call__(self, val=""):
        if self.plugin.runFlg and self.plugin.mpcHwnd:
            try:
                val = eg.ParseString(val)
                val = int(val)
            except:
                raise self.Exception(self.text.error % val)
                return
            return SendMessage(self.plugin.mpcHwnd, WM_COMMAND, val, 0)
        else:
            raise self.Exceptions.ProgramNotRunning


    def Configure(self, val=""):
        panel = eg.ConfigPanel()
        textLabel = wx.StaticText(panel, -1, self.text.label)
        textControl = wx.TextCtrl(panel, -1, val, size = (200,-1))
        panel.sizer.Add(textLabel, 0, wx.TOP, 20)
        panel.sizer.Add(textControl, 0, wx.TOP, 3)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())
#===============================================================================

class ActionPrototype(eg.ActionBase):

    def __call__(self):
        if self.plugin.runFlg and self.plugin.mpcHwnd:
            wx.CallAfter(SendMessage,self.plugin.mpcHwnd, WM_COMMAND, self.value, 0)
#===============================================================================

class GetWindowState(eg.ActionBase):

    class text:
        rbLabel = "Result type choice"
        numVal = "Return a numeric value"
        strVal = "Return a string value"
        boolVal = "Return True when window is "
        triggEvent = "Trigger an event"
        evtPrefix = "Event prefix (or prefix and first suffix):"
        states = (
            "Not running",
            "Tray icon",
            "Normal",
            "Minimized",
            "Maximized",
            "Full screen",
        )

    def __call__(self, mode = 0, state = 5, evnt = False, prefix = "MPCHC.Window"):
        stt = self.plugin.GetWindowState()
        if evnt:
            eg.TriggerEvent(
                "".join([word.capitalize() for word in self.text.states[stt+1].split()]),
                prefix = prefix
            )
        if mode == 0:
            return stt
        elif mode == 1:
            return self.text.states[stt+1]
        else:
            return stt == state-1


    def Configure(self, mode = 0, state = 5, evnt = False, prefix = "MPCHC.Window"):
        self.stt = state
        panel=eg.ConfigPanel(self)
        topSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, self.text.rbLabel),
            wx.VERTICAL
        )
        boolSizer = wx.BoxSizer(wx.HORIZONTAL)
        rb0 = panel.RadioButton(mode==0, self.text.numVal, style=wx.RB_GROUP)
        rb1 = panel.RadioButton(mode==1, self.text.strVal)
        rb2 = panel.RadioButton(mode==2, self.text.boolVal)
        statChoice = wx.Choice(panel, -1, choices = self.text.states)
        statChoice.Select(state)
        triggCtrl = wx.CheckBox(panel, -1, self.text.triggEvent)
        triggCtrl.SetValue(evnt)
        prefixLabel = wx.StaticText(panel, -1, self.text.evtPrefix)
        prefixCtrl = wx.TextCtrl(panel, -1, prefix)
        prefixSizer = wx.BoxSizer(wx.HORIZONTAL)
        prefixSizer.Add(prefixLabel,0,wx.TOP,3)
        prefixSizer.Add(prefixCtrl,0,wx.LEFT,6)
        boolSizer.Add(rb2,0,wx.TOP,3)
        boolSizer.Add(statChoice)
        topSizer.Add(rb0,0,wx.TOP,3)
        topSizer.Add(rb1,0,wx.TOP,7)
        topSizer.Add(boolSizer,0,wx.TOP,5)
        panel.sizer.Add(topSizer)
        panel.sizer.Add(triggCtrl, 0, wx.TOP, 10)
        panel.sizer.Add(prefixSizer, 0, wx.TOP, 10)

        def onTriggCtrl(evt = None):
            flg = triggCtrl.GetValue()
            prefixLabel.Show(flg)
            prefixCtrl.Show(flg)
            if evt:
                evt.Skip()
        triggCtrl.Bind(wx.EVT_CHECKBOX, onTriggCtrl)
        onTriggCtrl()

        def onState(evt):
            self.stt = evt.GetSelection()
            evt.Skip()
        statChoice.Bind(wx.EVT_CHOICE, onState)

        def onRadio(evt = None):
            flg = rb2.GetValue()
            statChoice.Enable(flg)
            sel = self.stt if flg else -1
            statChoice.SetSelection(sel)
            if evt:
                evt.Skip()
        rb0.Bind(wx.EVT_RADIOBUTTON, onRadio)
        rb1.Bind(wx.EVT_RADIOBUTTON, onRadio)
        rb2.Bind(wx.EVT_RADIOBUTTON, onRadio)
        onRadio()

        while panel.Affirmed():
            state = state if self.stt == -1 else self.stt
            panel.SetResult(
                (rb0.GetValue(),rb1.GetValue(),rb2.GetValue()).index(True),
                state,
                triggCtrl.GetValue(),
                prefixCtrl.GetValue()
            )
#===============================================================================

class GetPlayState(eg.ActionBase):

    class text:
        rbLabel = "Result type choice"
        numVal = "Return a numeric value"
        strVal = "Return a string value"
        boolVal = "Return True when play state is "
        states = ("Playing", "Paused", "Stopped", "Unknown")

    def __call__(self, mode = 0, state = 0):
        stt = self.plugin.playstate
        if mode == 0:
            return stt
        elif mode == 1:
            return self.text.states[stt]
        else:
            return stt == state


    def Configure(self, mode = 0, state = 0):
        self.stt = state
        panel=eg.ConfigPanel(self)
        topSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, self.text.rbLabel),
            wx.VERTICAL
        )
        boolSizer = wx.BoxSizer(wx.HORIZONTAL)
        rb0 = panel.RadioButton(mode==0, self.text.numVal, style=wx.RB_GROUP)
        rb1 = panel.RadioButton(mode==1, self.text.strVal)
        rb2 = panel.RadioButton(mode==2, self.text.boolVal)
        statChoice = wx.Choice(panel, -1, choices = self.text.states)
        statChoice.Select(state)
        boolSizer.Add(rb2,0,wx.TOP,3)
        boolSizer.Add(statChoice)
        topSizer.Add(rb0,0,wx.TOP,3)
        topSizer.Add(rb1,0,wx.TOP,7)
        topSizer.Add(boolSizer,0,wx.TOP,5)
        panel.sizer.Add(topSizer)


        def onState(evt):
            self.stt = evt.GetSelection()
            evt.Skip()
        statChoice.Bind(wx.EVT_CHOICE, onState)

        def onRadio(evt = None):
            flg = rb2.GetValue()
            statChoice.Enable(flg)
            sel = self.stt if flg else -1
            statChoice.SetSelection(sel)
            if evt:
                evt.Skip()
        rb0.Bind(wx.EVT_RADIOBUTTON, onRadio)
        rb1.Bind(wx.EVT_RADIOBUTTON, onRadio)
        rb2.Bind(wx.EVT_RADIOBUTTON, onRadio)
        onRadio()

        while panel.Affirmed():
            state = state if self.stt == -1 else self.stt
            panel.SetResult(
                (rb0.GetValue(),rb1.GetValue(),rb2.GetValue()).index(True),
                state,
            )
#===============================================================================

class GetNowPlaying(eg.ActionBase):

    def __call__(self):
        hWnd = Find_MPC()
        if not hWnd:
            raise self.Exceptions.ProgramNotRunning
        hWnd = hWnd[0]
        title = GetWindowText(hWnd)
        if not title.startswith("Media Player Classic"):
            ix = title.rfind(".")
            if ix > -1:
                return title[:ix]
#===============================================================================

class GetTimes(eg.ActionBase):

    name = "Get Times"
    description = "Returns elapsed, remaining and total times."

    def __call__(self):
        if self.plugin.runFlg and self.plugin.mpcHwnd:
            try:
                child = GetDlgItem(self.plugin.mpcHwnd, 10021)
                if GetClassName(child) ==  "#32770":
                    statText = GetDlgItem(child, 12027)
                    if GetClassName(statText) ==  "Static":
                        elaps, total = GetWindowText(statText).split(" / ")
                        elaps = GetSec(elaps)
                        totSec = GetSec(total)
                        rem = strftime('%H:%M:%S', gmtime(totSec-elaps))
                        elaps = strftime('%H:%M:%S', gmtime(elaps))
                        total = strftime('%H:%M:%S', gmtime(totSec))
            except:
                return None, None, None
            return elaps, rem, total
        else:
            eg.programCounter = None
            raise self.Exceptions.ProgramNotRunning
#===============================================================================

class GoTo_OSD(eg.ActionBase):

    name = 'On Screen Go To ...'
    description = 'Show On Screen "Go To ...".'

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
        if self.plugin.runFlg and self.plugin.mpcHwnd:
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
                    self.plugin.mpcHwnd,
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
        foreColourButton = eg.ColourSelectButton(panel,fore, title = self.text.txtColour)
        #Button Background Colour
        backLbl=wx.StaticText(panel, -1, self.text.background+':')
        backColourButton = eg.ColourSelectButton(panel,back, title = self.text.background)
        #Button Selected Text Colour
        foreSelLbl=wx.StaticText(panel, -1, self.text.txtColourSel+':')
        foreSelColourButton = eg.ColourSelectButton(panel,foreSel, title = self.text.txtColourSel)
        #Button Selected Background Colour
        backSelLbl=wx.StaticText(panel, -1, self.text.backgroundSel+':')
        backSelColourButton = eg.ColourSelectButton(panel,backSel, title = self.text.backgroundSel)
        #Button Dialog "Menu control - assignement of events"
        dialogButton = wx.Button(panel,-1,self.text.dialog, size = (w, -1))
        dialogButton.SetToolTipString(self.text.btnToolTip)
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
        fontFaceCtrl = wx.Choice(panel, -1, choices = fw.fontList, size =(160,-1))
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
        previewPanel = wx.Panel(panel, -1, pos = (ps[0], ps[1]+2), size = sz, style = wx.BORDER_SIMPLE)
        gotoLbl=wx.StaticText(previewPanel, -1, self.text.gotoLabel, pos = (5,5))
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
            GoToCtrl.SetStyle(pos, pos+1, wx.TextAttr(self.foreSel, self.backSel, fnt))
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
            wx.CallAfter(dlg.ShowMenuEventsDialog, self.text.evtAssignTitle, self.text.events)
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
            if self.plugin.runFlg and self.plugin.mpcHwnd:
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
                        self.plugin.mpcHwnd,
                        panel.evtList,
                        self.sizeFlag
                    )
                    eg.actionThread.WaitOnEvent(self.event)
            else:
                self.PrintError(eg.Classes.Exceptions.Text.ProgramNotRunning)
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

    name = "Show MPC menu"
    description = "Show MPC menu."
    panel = None

    class text:
        OSELabel = 'Menu show on:'
        menuPreview = 'MPC On Screen Menu preview:'
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
        if self.plugin.runFlg and self.plugin.mpcHwnd:
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
                    self.plugin.mpcHwnd,
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
        evtList = [[],[],[],[],[]],
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
        font = wx.FontFromNativeInfoString(fontInfo)
        for n in range(10,20):
            font.SetPointSize(n)
            fontButton.SetFont(font)
            hght = fontButton.GetTextExtent('X')[1]
            if hght > 20:
                break
        listBoxCtrl.SetDefaultCellFont(font)
        arial = wx.FontFromNativeInfoString(arialInfoString)
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
            wx.CallAfter(dlg.ShowMenuEventsDialog, self.text.evtAssignTitle, self.text.events)
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
            if self.plugin.runFlg and self.plugin.mpcHwnd:
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
                        self.plugin.mpcHwnd,
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
        if self.plugin.mpcPath:
            self.plugin.ConnectMpcHc()
#===============================================================================

class MediaPlayerClassic(eg.PluginBase):

    mySched = None
    myStart = None
    menuDlg = None
    state = None
    playstate = 3
    np_payload = None
    mpcHwnd = None
    event = None
    result = None
    runFlg = False
    strtFlg = False
    connected = False

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
        label = "Path to MPC-HC executable:"
        fileMask = "MPC-HC executable|mpc-hc*.exe|All EXE files (*.exe)|*.exe"
        gotoLabel = "Go To..."
        fltr='"NowPlaying" event is only trigerred when the payload is changed'

    def ParseMsg(self, msg):
        msg = msg.replace(u"\\|", u"\xb0*\u2734*\xb0")
        msg = msg.split(u"|")
        for i in range(len(msg)):
            msg[i] = msg[i].replace(u"\xb0*\u2734*\xb0", u"|")
        return msg


    @eg.LogIt
    def Handler(self, hwnd, mesg, wParam, lParam):
        if not self.runFlg:
            return True
        cpyData = cast(lParam, PCOPYDATASTRUCT)
        cmd = cpyData.contents.dwData
        msg = wstring_at(cpyData.contents.lpData)
        if cmd == CMD_CONNECT:
            self.mpcHwnd = int(msg)
            self.connected = True
            eg.TriggerEvent("Connected",prefix="MPC-HC")
        elif cmd == CMD_STATE:
            state = int(msg)
            if self.state != state:
                self.state = state
                eg.TriggerEvent("State."+MPC_LOADSTATE[state],prefix="MPC-HC")
        elif cmd == CMD_NOWPLAYING:
            if self.playstate == 3: # if the plugin is started when the MPC-HC is already playing
                self.playstate = 0
            msg = self.ParseMsg(msg)
            if msg !=  self.np_payload:
                self.np_payload = msg
                eg.TriggerEvent("NowPlaying",prefix="MPC-HC", payload = msg)

        elif cmd == CMD_PLAYMODE:
            self.playstate = int(msg)
            eg.TriggerEvent("Playstate."+MPC_PLAYSTATE[self.playstate],prefix="MPC-HC")

        elif cmd == CMD_NOTIFYSEEK:
            eg.TriggerEvent("Seek",prefix="MPC-HC",payload = int(0.5+float(msg)))

        elif cmd in (
            CMD_CURRENTPOSITION,
            CMD_LISTSUBTITLETRACKS,
            CMD_LISTAUDIOTRACKS,
            CMD_PLAYLIST
        ):
            if self.event:
                self.result = self.ParseMsg(msg)
                SetEvent(self.event)

        elif cmd == CMD_NOTIFYENDOFSTREAM:
            eg.TriggerEvent("EndOfStream",prefix="MPC-HC")
        return True


    def ConnectMpcHc(self):
        if not self.runFlg:
            mp = self.mpcPath
            mp = mp.encode(FSE) if isinstance(mp, unicode) else mp
            if isfile(mp):
                self.runFlg = True
                self.strtFlg = False
                args = [mp]
                args.append("/slave")
                args.append(str(self.mr.hwnd))
                Popen(args)


    def isResponding(self, hwnd):
        try:
            SendMessageTimeout(hwnd, 0, timeout = 1000) # 0 = WM_NULL
            return True
        except:
            return False


    def isRunning(self):
        try:
            return FindWindow(u'MediaPlayerClassicW', None)
        except:
            return False


    def waitBeforeConnect(self):
        hwnd = self.isRunning()
        if hwnd:
            if self.isResponding(hwnd):
                eg.scheduler.AddTask(1, self.ConnectMpcHc)
            else:
                self.myStart = eg.scheduler.AddTask(2, self.waitBeforeConnect)
        else:
            self.strtFlg = False


    def mpcIsRunning(self):
        self.mySched=eg.scheduler.AddTask(2, self.mpcIsRunning) # must run continuously !
        if not self.isRunning(): #user closed MPC-HC ?
            if self.runFlg and self.connected:
                    self.runFlg = False
                    self.connected = False
                    self.strtFlg = False
                    self.myStart = None
                    self.mpcHwnd = None
        elif self.runFlg:
            pass
        elif not self.strtFlg:
            self.strtFlg = True
            self.myStart = eg.scheduler.AddTask(2, self.waitBeforeConnect)


    def SendCopydata(self, cmd, txt):
        if self.mpcHwnd is not None:
            cpyData = create_unicode_buffer(txt)
            cds = COPYDATASTRUCT()
            cds.dwData = cmd
            cds.lpData = cast(cpyData, c_void_p)
            cds.cbData = sizeof(cpyData)
            return SendMessage(self.mpcHwnd, WM_COPYDATA, 0, addressof(cds))


    def __init__(self):
        self.mr = eg.MessageReceiver("MPC-HC_plugin_")
        self.mr.AddHandler(WM_COPYDATA, self.Handler)
        self.mr.Start()
        self.AddActionsFromList(ACTIONS, ActionPrototype)


    def __start__(self, mpcPath=None, fltr=True):
        self.fltr=fltr
        self.mySched=None
        self.myStart=None
        self.menuDlg = None
        self.state = None
        self.mpcHwnd = None
        self.event = None
        self.result = None
        self.runFlg = False
        self.strtFlg = False
        self.connected = False
        self.playstate = 3
        self.np_payload = None
        if mpcPath is None:
            mpcPath = self.GetMpcHcPath()
        if not mpcPath or not exists(mpcPath):
            raise self.Exceptions.ProgramNotFound
            return
        self.mpcPath = mpcPath
        hWnd = Find_MPC()
        if hWnd:
            self.mpcHwnd = hWnd[0]
        eg.scheduler.AddTask(1, self.mpcIsRunning)


    def __stop__(self):
        if self.mySched:
            try:
                eg.scheduler.CancelTask(self.mySched)
            except:
                pass
        if self.myStart:
            try:
                eg.scheduler.CancelTask(self.myStart)
            except:
                pass


    def __close__(self):
        self.mr.RemoveHandler(WM_COPYDATA, self.Handler)
        self.mr.Stop()
        self.mr = None


    def Configure(self, mpcPath=None,fltr=True):
        if mpcPath is None:
            mpcPath = self.GetMpcHcPath()
            if mpcPath is None:
                mpcPath = join(
                    eg.folderPath.ProgramFiles,
                    "MediaPlayerClassic",
                    "mpc-hc.exe"
                )
        panel = eg.ConfigPanel()
        filepathCtrl = eg.FileBrowseButton(
            panel,
            size=(320,-1),
            initialValue=mpcPath,
            startDirectory=eg.folderPath.ProgramFiles,
            labelText="",
            fileMask = self.text.fileMask,
            buttonText=eg.text.General.browse,
        )
        fltrCtrl = wx.CheckBox(panel, -1, self.text.fltr)
        fltrCtrl.SetValue(fltr)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel,-1,self.text.label))
        sizer.Add(filepathCtrl)
        sizer.Add(fltrCtrl,0,wx.TOP,20)
        panel.sizer.Add(sizer,0,wx.ALL,10)
        while panel.Affirmed():
            panel.SetResult(
                filepathCtrl.GetValue(),
                fltrCtrl.GetValue()
            )


    def GetMpcHcPath(self):
        """
        Get the path of MPC-HC's installation directory through querying
        the Windows registry.
        """
        try:
            if "PROCESSOR_ARCHITEW6432" in environ:
                args = [_winreg.HKEY_CURRENT_USER,
                    "Software\MPC-HC\MPC-HC"]
                args.extend((0, _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY))
            else:
                args = [_winreg.HKEY_CURRENT_USER,
                    "Software\Gabest\Media Player Classic"]
            mpc = _winreg.OpenKey(*args)
            mpcPath =_winreg.QueryValueEx(mpc, "ExePath")[0]
            _winreg.CloseKey(mpc)
        except WindowsError:
            mpcPath = None
        return mpcPath


    def GetWindowState(self):
        hWnd = Find_MPC()
        if not hWnd:
            return -1
        else:
            hWnd = hWnd[0]
        if not IsWindowVisible(hWnd):
            return 0
        state = GetWindowPlacement(hWnd)[1]
        border = GetWindowLong(hWnd, GWL_EXSTYLE) & WS_EX_WINDOWEDGE
        if border:
            return state
        rect = GetWindowRect(hWnd)
        mons = EnumDisplayMonitors()
        fullscreen = False
        for mon in mons:
            if rect == mon[2]:
                fullscreen = True
                break
        if fullscreen:
            return 4
        return state
#===============================================================================

class SendCmd(eg.ActionBase):
    def __call__(self):
        self.plugin.SendCopydata(self.value, u"")
#===============================================================================

class GetInfo(eg.ActionBase):
    def __call__(self):
        self.plugin.result = None
        self.plugin.event = CreateEvent(None, 0, 0, None)
        if self.plugin.SendCopydata(self.value, u""):
            eg.actionThread.WaitOnEvent(self.plugin.event)
            self.plugin.event = None
            if self.plugin.result:
                return self.plugin.result
#===============================================================================

class OpenFile(eg.ActionBase):

    class text:
        toolTipFile = 'Type filename or click browse to choose file'
        browseFile = 'Choose a file'


    def __call__(self, filepath = ""):
        if filepath:
            filepath = eg.ParseString(filepath)
            self.plugin.SendCopydata(self.value, filepath)


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

class GetPosition(eg.ActionBase):

    def __call__(self):
        self.plugin.result = None
        self.plugin.event = CreateEvent(None, 0, 0, None)
        if self.plugin.SendCopydata(CMD_GETCURRENTPOSITION, u""):
            eg.actionThread.WaitOnEvent(self.plugin.event)
            self.plugin.event = None
            if self.plugin.result:
                return int(0.5+float(self.plugin.result[0]))
#===============================================================================

class SetInteger(eg.ActionBase):

    class text:
        labels = (
            ("Jump of", "seconds (negative values for backward)"),
            ("New position:", "seconds"),
            ("Index of the audio track:", ""),
            ("Index of the subtitle track:", "(-1 for disabling subtitles)"),
            ("Index of the active file:", "(-1 for no file selected)"),
            ("New audio delay:", "milliseconds"),
            ("New subtitle delay:", "milliseconds"),
        )


    def __call__(self, value=0):
        value = unicode(value)
        self.plugin.SendCopydata(self.value[0], value)


    def Configure(self, value=0):
        panel = eg.ConfigPanel()
        label_1 = wx.StaticText(panel,-1,self.text.labels[self.value[1]][0])
        label_2 = wx.StaticText(panel,-1,self.text.labels[self.value[1]][1])
        valueCtrl = eg.SpinIntCtrl(panel, -1, value, max=self.value[3],min=self.value[2])
        sizer = wx.FlexGridSizer(1, 3, 5, 10)
        sizer.Add(label_1,0,wx.TOP,3)
        sizer.Add(valueCtrl)
        sizer.Add(label_2,0,wx.TOP,3)
        panel.sizer.Add(sizer,0,wx.ALL|wx.EXPAND,20)
        while panel.Affirmed():
            panel.SetResult(
                valueCtrl.GetValue(),
            )
#===============================================================================

class SendOSD(eg.ActionBase):

    class text:
        osdLabel = "OSD text:"
        durLabel = "Duration [s]:"
        posLabel = "Position:"
        position = (
            "None (clear)",
            "Top left",
            "Top right",
        )


    def __call__(self, osd="", dur=3, pos=1):
        if self.plugin.mpcHwnd is not None:
            osd = eg.ParseString(osd) + "\0"
            OSDDATA.nMsgPos     = pos
            OSDDATA.nDurationMS = 1000*dur
            OSDDATA.strMsg      = osd.encode(eg.systemEncoding)
            cds = COPYDATASTRUCT()
            cds.dwData = CMD_OSDSHOWMESSAGE
            cds.cbData = sizeof(OSDDATA)
            cds.lpData = cast(addressof(OSDDATA), c_void_p)
            SendMessage(self.plugin.mpcHwnd, WM_COPYDATA, 0, addressof(cds))


    def Configure(self, osd="", dur=3, pos=1):
        panel = eg.ConfigPanel()
        osdLabel = wx.StaticText(panel,-1,self.text.osdLabel)
        posLabel = wx.StaticText(panel,-1,self.text.posLabel)
        durLabel = wx.StaticText(panel,-1,self.text.durLabel)
        osdCtrl = wx.TextCtrl(panel,-1,osd, size=(200,-1))
        durCtrl = eg.SpinIntCtrl(panel, -1, dur, max=99999)
        posCtrl = wx.Choice(panel,-1,choices=self.text.position)
        posCtrl.SetSelection(pos)
        sizer = wx.FlexGridSizer(3, 2, 5, 10)
        sizer.Add(osdLabel,0,wx.TOP,3)
        sizer.Add(osdCtrl)
        sizer.Add(durLabel,0,wx.TOP,3)
        sizer.Add(durCtrl)
        sizer.Add(posLabel,0,wx.TOP,3)
        sizer.Add(posCtrl)
        panel.sizer.Add(sizer,0,wx.ALL|wx.EXPAND,20)

        while panel.Affirmed():
            panel.SetResult(
                osdCtrl.GetValue(),
                durCtrl.GetValue(),
                posCtrl.GetSelection(),
            )
#===============================================================================

ACTIONS = (
(eg.ActionGroup, 'GroupMainControls', 'Main controls', None, (
    (Run, "Run", "Run MPC-HC", "Run MPC-HC with its default settings." ,None),
    ('Exit', 'Quit Application', None, 816),
    ('PlayPause', 'Play/Pause', None, 889),
    ('Play', 'Play', None, 887),
    ('Pause', 'Pause', None, 888),
    ('Stop', 'Stop', None, 890),
    ('JumpForwardSmall', 'Jump Forward Small', None, 900),
    ('JumpBackwardSmall', 'Jump Backward Small', None, 899),
    ('JumpForwardMedium', 'Jump Forward Medium', None, 902),
    ('JumpBackwardMedium', 'Jump Backward Medium', None, 901),
    ('JumpForwardLarge', 'Jump Forward Large', None, 904),
    ('JumpBackwardLarge', 'Jump Backward Large', None, 903),
    ('JumpForwardKeyframe', 'Jump Forward Keyframe', None, 898),
    ('JumpBackwardKeyframe', 'Jump Backward Keyframe', None, 897),
    (
        SetInteger,
        "Jump",
        "Jump forward/backward of N seconds",
        "Jumps forward/backward of N seconds.",
        (CMD_JUMPOFNSECONDS,0,-99999,99999)
    ),
    (
        SetInteger,
        "SetPosition",
        "Cue current file to specific position",
        "Cues current file to specific position.",
        (CMD_SETPOSITION,1,1,999999)
    ),    ('IncreaseRate', 'Increase Rate', None, 895),
    ('DecreaseRate', 'Decrease Rate', None, 894),
    ('ResetRate', 'Reset Rate', None, 896),
    ('VolumeUp', 'Volume Up', None, 907),
    ('VolumeDown', 'Volume Down', None, 908),
    ('VolumeMute', 'Volume Mute', None, 909),
    ('BossKey', 'Boss Key', None, 944),
    ('Next', 'Next', None, 922),
    ('Previous', 'Previous', None, 921),
    (SendCmd,"StartPlaylist","Start playing playlist","Starts playing playlist.",CMD_STARTPLAYLIST),
    (SendCmd,"ClearPlaylist","Remove all files from playlist","Removes all files from playlist.",CMD_CLEARPLAYLIST),
    ('NextPlaylistItem', 'Next Playlist Item', None, 920),
    ('PreviousPlaylistItem', 'Previous Playlist Item', None, 919),
    (OpenFile,"AddFile","Add file to playlist","Add a new file to playlist (did not start playing).",CMD_ADDTOPLAYLIST),
    #(
    #    SetInteger,
    #    "SetActiveFile",
    #    "Set the active file in the playlist",
    #    "Sets the active file in the playlist.",
    #    (CMD_SETINDEXPLAYLIST,4,-1,9)
    #),
    ('OpenDVD', 'Open DVD', None, 801),
    ('OpenFileDialog', 'Show dialog "Open file"', None, 800),
    (OpenFile,"OpenFile","Open file","Opens file.",CMD_OPENFILE),
    ('QuickOpen', 'Quick Open File', None, 969),
    ('OpenDirectory', 'Open Directory', None, 33208),
    ('FrameStep', 'Frame Step', None, 891),
    ('FrameStepBack', 'Frame Step Back', None, 892),
    ('GoTo', 'Go To', None, 893),
    ('AudioDelayAdd10ms', 'Audio Delay +10ms', None, 905),
    ('AudioDelaySub10ms', 'Audio Delay -10ms', None, 906),
    (
        SetInteger,
        "SetAudioDelay",
        "Set the audio delay",
        "Sets the audio delay.",
        (CMD_SETAUDIODELAY,5,-999999,999999)
    ),
)),
(eg.ActionGroup, 'GroupViewModes', 'View modes', None, (
    ('Fullscreen', 'Fullscreen', None, 830),
    ('FullscreenWOR', 'Fullscreen without resolution change', None, 831),
    ('PnSIncSize', 'Pan & Scan Increase Size', None, 862),
    ('PnSDecSize', 'Pan & Scan Decrease Size', None, 863),
    ('PnSTo169', 'Pan & Scan Scale to 16:9', None, 4100),
    ('PnSToWidescreen', 'Pan & Scan to Widescreen', None, 4101),
    ('PnSToUltraWidescreen', 'Pan & Scan to Ultra-Widescreen', None, 4102),
    ('ViewMinimal', 'View Minimal', None, 827),
    ('ViewCompact', 'View Compact', None, 828),
    ('ViewNormal', 'View Normal', None, 829),
    ('AlwaysOnTop', 'Always On Top', None, 884),
    ('Zoom50', 'Zoom 50%', None, 832),
    ('Zoom100', 'Zoom 100%', None, 833),
    ('Zoom200', 'Zoom 200%', None, 834),
    ('VidFrmHalf', 'Video Frame Half', None, 835),
    ('VidFrmNormal', 'Video Frame Normal', None, 836),
    ('VidFrmDouble', 'Video Frame Double', None, 837),
    ('VidFrmStretch', 'Video Frame Stretch', None, 838),
    ('VidFrmInside', 'Video Frame Inside', None, 839),
    ('VidFrmOutside', 'Video Frame Outside', None, 840),
    ('PnSReset', 'Pan & Scan Reset', None, 861),
    ('PnSIncWidth', 'Pan & Scan Increase Width', None, 864),
    ('PnSIncHeight', 'Pan & Scan Increase Height', None, 866),
    ('PnSDecWidth', 'Pan & Scan Decrease Width', None, 865),
    ('PnSDecHeight', 'Pan & Scan Decrease Height', None, 867),
    ('PnSCenter', 'Pan & Scan Center', None, 876),
    ('PnSLeft', 'Pan & Scan Left', None, 868),
    ('PnSRight', 'Pan & Scan Right', None, 869),
    ('PnSUp', 'Pan & Scan Up', None, 870),
    ('PnSDown', 'Pan & Scan Down', None, 871),
    ('PnSUpLeft', 'Pan & Scan Up/Left', None, 872),
    ('PnSUpRight', 'Pan & Scan Up/Right', None, 873),
    ('PnSDownLeft', 'Pan & Scan Down/Left', None, 874),
    ('PnSDownRight', 'Pan & Scan Down/Right', None, 875),
    ('PnSRotateAddX', 'Pan & Scan Rotate X+', None, 877),
    ('PnSRotateSubX', 'Pan & Scan Rotate X-', None, 878),
    ('PnSRotateAddY', 'Pan & Scan Rotate Y+', None, 879),
    ('PnsRotateSubY', 'Pan & Scan Rotate Y-', None, 880),
    ('PnSRotateAddZ', 'Pan & Scan Rotate Z+', None, 881),
    ('PnSRotateSubZ', 'Pan & Scan Rotate Z-', None, 882),
)),
(eg.ActionGroup, 'GroupDvdControls', 'DVD controls', None, (
    ('DVDTitleMenu', 'DVD Title Menu', None, 923),
    ('DVDRootMenu', 'DVD Root Menu', None, 924),
    ('DVDSubtitleMenu', 'DVD Subtitle Menu', None, 925),
    ('DVDAudioMenu', 'DVD Audio Menu', None, 926),
    ('DVDAngleMenu', 'DVD Angle Menu', None, 927),
    ('DVDChapterMenu', 'DVD Chapter Menu', None, 928),
    ('DVDMenuLeft', 'DVD Menu Left', None, 929),
    ('DVDMenuRight', 'DVD Menu Right', None, 930),
    ('DVDMenuUp', 'DVD Menu Up', None, 931),
    ('DVDMenuDown', 'DVD Menu Down', None, 932),
    ('DVDMenuActivate', 'DVD Menu Activate', None, 933),
    ('DVDMenuBack', 'DVD Menu Back', None, 934),
    ('DVDMenuLeave', 'DVD Menu Leave', None, 935),
    ('DVDNextAngle', 'DVD Next Angle', None, 961),
    ('DVDPrevAngle', 'DVD Previous Angle', None, 962),
    ('DVDNextAudio', 'DVD Next Audio', None, 963),
    ('DVDPrevAudio', 'DVD Prev Audio', None, 964),
    ('DVDNextSubtitle', 'DVD Next Subtitle', None, 965),
    ('DVDPrevSubtitle', 'DVD Prev Subtitle', None, 966),
    ('DVDOnOffSubtitle', 'DVD On/Off Subtitle', None, 967),
)),
(eg.ActionGroup, 'GroupExtendedControls', 'Extended controls', None, (
    ('OpenDevice', 'Open Device', None, 802),
    ('SaveAs', 'Save As', None, 805),
    ('SaveImage', 'Save Image', None, 806),
    ('SaveImageAuto', 'Save Image Auto', None, 807),
    ('LoadSubTitle', 'Load Subtitle', None, 809),
    ('SaveSubtitle', 'Save Subtitle', None, 810),
    ('Close', 'Close File', None, 804),
    ('Properties', 'Properties', None, 814),
    ('PlayerMenuShort', 'Player Menu Short', None, 949),
    ('PlayerMenuLong', 'Player Menu Long', None, 950),
    ('FiltersMenu', 'Filters Menu', None, 951),
    ('Options', 'Options', None, 815),
    ('NextAudio', 'Next Audio', None, 952),
    ('PrevAudio', 'Previous Audio', None, 953),
    (
        SetInteger,
        "SetAudioTrack",
        "Set the audio track",
        "Sets the audio track.",
        (CMD_SETAUDIOTRACK,2,0,9)
    ),
    ('NextSubtitle', 'Next Subtitle', None, 954),
    ('PrevSubtitle', 'Prev Subtitle', None, 955),
    (
        SetInteger,
        "SetSubtitlesTrack",
        "Set the subtitle track",
        "Sets the subtitle track.",
        (CMD_SETSUBTITLETRACK,3,-1,9)
    ),
    ('OnOffSubtitle', 'On/Off Subtitle', None, 956),
    ('GotoNextSubtitle', 'Goto Next Subtitle', None, 32781),
    ('GotoPrevSubtitle', 'Goto Prev Subtitle', None, 32780),
    ('SubtitleDelayMinus', 'Subtitle Delay -', None, 24000),
    ('SubtitleDelayPlus', 'Subtitle Delay +', None, 24001),
    (
        SetInteger,
        "SetSubtitleDelay",
        "Set the subtitle delay",
        "Sets the subtitle delay.",
        (CMD_SETSUBTITLEDELAY,6,-999999,999999)
    ),
    ('ReloadSubtitles', 'Reload Subtitles', None, 2302),
    ('NextAudioOGM', 'Next Audio OGM', None, 957),
    ('PrevAudioOGM', 'Previous Audio OGM', None, 958),
    ('NextSubtitleOGM', 'Next Subtitle OGM', None, 959),
    ('PrevSubtitleOGM', 'Previous Subtitle OGM', None, 960),
    (ShowMenu,'ShowMenu','Show MPC menu','Show MPC menu.', None),
    (GoTo_OSD,'GoTo_OSD','On Screen Go To ...','Show On Screen "Go To ...".', None),
    (SendOSD,"SendOSD","Show custom OSD","Shows custom OSD.",None),
    (AfterPlaybackOnce,"AfterPlaybackOnce","Action after playback (once)","The selected action will be made after playback (once).", None),
    (AfterPlayback,"AfterPlayback","Action after playback (every time)","The selected action will be made after playback (every time).", None),
    (UserMessage,'UserMessage',"Send user's message",UserMessage.description, None),
)),
(eg.ActionGroup, 'GroupToggleControls', 'Toggle player controls', None, (
    ('ToggleCaptionMenu', 'Toggle Caption Menu', None, 817),
    ('ToggleSeeker', 'Toggle Seeker', None, 818),
    ('ToggleControls', 'Toggle Controls', None, 819),
    ('ToggleInformation', 'Toggle Information', None, 820),
    ('ToggleStatistics', 'Toggle Statistics', None, 821),
    ('ToggleStatus', 'Toggle Status', None, 822),
    ('ToggleSubresyncBar', 'Toggle Subresync Bar', None, 823),
    ('TogglePlaylistBar', 'Toggle Playlist Bar', None, 824),
    ('ToggleCaptureBar', 'Toggle Capture Bar', None, 825),
    (SendCmd,"ShaderToggle","Toggle shader","Toggles shader.",CMD_SHADER_TOGGLE),
    ('ToggleShaderEditorBar', 'Toggle Shader Editor Bar', None, 826),
    ('ToggleElapsedTime', 'Toggle OSD Elapsed Time', None, 32778),
)),
(eg.ActionGroup, 'VariousInformationRetrieval',"Retrieve various information", None, (
    (GetWindowState,'GetWindowState','Get window state','Gets window state.', None),
    (GetNowPlaying,'GetNowPlaying','Get currently playing file','Gets currently playing file.', None),
    (GetTimes,'GetTimes','Get Times','Returns elapsed, remaining and total times.', None),
    (GetPosition,"GetPosition","Get current position","Returns current position.",None),
    (GetInfo,"GetSubtitles","Get subtitles tracks","Asks for a list of the subtitles tracks of the file.",CMD_GETSUBTITLETRACKS),
    (GetInfo,"GetAdiotracks","Get audio tracks","Asks for a list of the audio tracks of the file.",CMD_GETAUDIOTRACKS),
    (GetInfo,"GetPlaylist","Get playlist","Asks for the current playlist.",CMD_GETPLAYLIST),
    (GetPlayState,"GetPlaystate","Get play-state","Returns current play-state.",None),
)),
)
#===============================================================================

