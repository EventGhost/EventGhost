# Plugins/MediaPlayerClassic/__init__.py
#
# Copyright (C) 2006 MonsterMagnet
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


eg.RegisterPlugin(
    name = "Media Player Classic",
    author = "MonsterMagnet",
    version = "1.5." + "$LastChangedRevision$".split()[1],
    kind = "program",
    guid = "{DD75104D-D586-438A-B63D-3AD01A4D4BD3}",
    createMacrosOnAdd = True,
    description = (
        'Adds actions to control '
        '<a href="http://sourceforge.net/projects/guliverkli/">'
        'Media Player Classic</a>.'
    ),
    help = """
        Only for version <b>6.4.8.9</b> or above.
        The plugin will not work with older versions of MPC!
        
        <a href=http://www.eventghost.org/forum/viewtopic.php?t=17>
        Bugreports</a>
        
        <p><a href="http://sourceforge.net/projects/guliverkli/">
        Media Player Classic SourceForge Project</a>
    """,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAhElEQVR42rWRgQqAIAwF"
        "fV+++eWr1V6kiM6gQaTVHYehJEdV7bUG18hCInIDQMNhA+L7cQHBETQrBWERDXANjcxm"
        "Ee6CyFxd6ArkynZT5l7KK9gFbs3CrGgEPLzM1FonAn9kz59stqhnhdhEwK/j3m0Tgj8K"
        "OPmCr4eYpmMaASt3JS44ADcFoxFdcIMPAAAAAElFTkSuQmCC"
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=694"
)
    
# changelog:
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


ACTIONS = (
(eg.ActionGroup, 'GroupMainControls', 'Main controls', None, (
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
    ('IncreaseRate', 'Increase Rate', None, 895),
    ('DecreaseRate', 'Decrease Rate', None, 894),
    ('ResetRate', 'Reset Rate', None, 896),
    ('VolumeUp', 'Volume Up', None, 907),
    ('VolumeDown', 'Volume Down', None, 908),
    ('VolumeMute', 'Volume Mute', None, 909),
    ('BossKey', 'Boss Key', None, 943),
    ('Next', 'Next', None, 921),
    ('Previous', 'Previous', None, 920),
    ('NextPlaylistItem', 'Next Playlist Item', None, 919),
    ('PreviousPlaylistItem', 'Previous Playlist Item', None, 918),
    ('OpenFile', 'Open File', None, 800),
    ('OpenDVD', 'Open DVD', None, 801),
    ('QuickOpen', 'Quick Open File', None, 968),
    ('OpenDirectory', 'Open Directory', None, 33208),
    ('FrameStep', 'Frame Step', None, 891),
    ('FrameStepBack', 'Frame Step Back', None, 892),
    ('GoTo', 'Go To', None, 893),
    ('AudioDelayAdd10ms', 'Audio Delay +10ms', None, 905),
    ('AudioDelaySub10ms', 'Audio Delay -10ms', None, 906),
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
    ('DVDTitleMenu', 'DVD Title Menu', None, 922),
    ('DVDRootMenu', 'DVD Root Menu', None, 923),
    ('DVDSubtitleMenu', 'DVD Subtitle Menu', None, 924),
    ('DVDAudioMenu', 'DVD Audio Menu', None, 925),
    ('DVDAngleMenu', 'DVD Angle Menu', None, 926),
    ('DVDChapterMenu', 'DVD Chapter Menu', None, 927),
    ('DVDMenuLeft', 'DVD Menu Left', None, 928),
    ('DVDMenuRight', 'DVD Menu Right', None, 929),
    ('DVDMenuUp', 'DVD Menu Up', None, 930),
    ('DVDMenuDown', 'DVD Menu Down', None, 931),
    ('DVDMenuActivate', 'DVD Menu Activate', None, 932),
    ('DVDMenuBack', 'DVD Menu Back', None, 933),
    ('DVDMenuLeave', 'DVD Menu Leave', None, 934),
    ('DVDNextAngle', 'DVD Next Angle', None, 960),
    ('DVDPrevAngle', 'DVD Previous Angle', None, 961),
    ('DVDNextAudio', 'DVD Next Audio', None, 962),
    ('DVDPrevAudio', 'DVD Prev Audio', None, 963),
    ('DVDNextSubtitle', 'DVD Next Subtitle', None, 964),
    ('DVDPrevSubtitle', 'DVD Prev Subtitle', None, 965),
    ('DVDOnOffSubtitle', 'DVD On/Off Subtitle', None, 966),
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
    ('PlayerMenuShort', 'Player Menu Short', None, 948),
    ('PlayerMenuLong', 'Player Menu Long', None, 949),
    ('FiltersMenu', 'Filters Menu', None, 950),
    ('Options', 'Options', None, 886),
    ('NextAudio', 'Next Audio', None, 951),
    ('PrevAudio', 'Previous Audio', None, 952),
    ('NextSubtitle', 'Next Subtitle', None, 953),
    ('PrevSubtitle', 'Prev Subtitle', None, 954),
    ('OnOffSubtitle', 'On/Off Subtitle', None, 955),
    ('ReloadSubtitles', 'Reload Subtitles', None, 2302),
    ('NextAudioOGM', 'Next Audio OGM', None, 956),
    ('PrevAudioOGM', 'Previous Audio OGM', None, 957),
    ('NextSubtitleOGM', 'Next Subtitle OGM', None, 958),
    ('PrevSubtitleOGM', 'Previous Subtitle OGM', None, 959),
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
    ('ToggleShaderEditorBar', 'Toggle Shader Editor Bar', None, 826),
    ('ToggleElapsedTime', 'Toggle OSD Elapsed Time', None, 32778),
)),
)
#===============================================================================

from eg.WinApi import FindWindow, SendMessageTimeout, WM_COMMAND
from eg.WinApi.Utils import GetMonitorDimensions
from win32api import EnumDisplayMonitors
from eg.WinApi.Dynamic import SendMessage, PostMessage
from eg.WinApi.Dynamic import CreateEvent, SetEvent
from os import path
from threading import Timer
from win32gui import GetMenu, GetSubMenu, GetMenuItemCount, GetDlgCtrlID, IsWindow
from win32gui import GetWindowRect, GetClassName, GetWindow, GetWindowText, GetDlgItem
from copy import deepcopy as cpy
from time import sleep, strftime, gmtime
from winsound import PlaySound, SND_ASYNC
from win32process import GetWindowThreadProcessId
from ctypes import create_unicode_buffer, addressof, windll, c_int, c_ulong, c_buffer, byref, sizeof
import wx.grid as gridlib
#===============================================================================

_psapi = windll.psapi
_kernel = windll.kernel32
modBasName = c_buffer(32)
hModule = c_ulong()
length = c_ulong()
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010

def GetModuleFrom_hWnd(hWnd):
    threadId, processId = GetWindowThreadProcessId(hWnd)
    hProc = _kernel.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, processId)
    _psapi.EnumProcessModules(hProc, byref(hModule), sizeof(hModule), byref(length))
    _psapi.GetModuleBaseNameA(hProc, hModule.value, modBasName, sizeof(modBasName))
    _kernel.CloseHandle(hProc)
    return modBasName.value


if eg.Version.base >= "0.4.0":
    from eg.Classes.MainFrame.TreeCtrl import DropTarget as EventDropTarget
    IMAGES_DIR = eg.imagesDir 
else:
    from eg.Classes.MainFrame.TreeCtrl import EventDropTarget
    IMAGES_DIR = eg.IMAGES_DIR 

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
WM_GETTEXT       = 13
WM_GETTEXTLENGTH = 14
WM_CLOSE         = 16
#===============================================================================

class FixedWidth(wx.FontEnumerator):

    def __init__(self):
        wx.FontEnumerator.__init__(self)
        self.fontList = []

    def OnFacename(self, fontname):
        if not fontname.startswith("@"): 
            self.fontList.append(fontname)
#===============================================================================

_psapi = windll.psapi
_kernel = windll.kernel32
modBasName = c_buffer(32)
hModule = c_ulong()
length = c_ulong()
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010

def GetModuleFrom_hWnd(hWnd):
    threadId, processId = GetWindowThreadProcessId(hWnd)
    hProc = _kernel.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, processId)
    _psapi.EnumProcessModules(hProc, byref(hModule), sizeof(hModule), byref(length))
    _psapi.GetModuleBaseNameA(hProc, hModule.value, modBasName, sizeof(modBasName))
    _kernel.CloseHandle(hProc)
    return modBasName.value
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
        evt = EventAfter(newEVT_BUTTON_AFTER, self.GetId())
        evt.SetValue(self.GetValue())
        self.GetEventHandler().ProcessEvent(evt)
        dialog.Destroy()
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
        evt = EventAfter(newEVT_BUTTON_AFTER, self.GetId())
        evt.SetValue(self.GetValue())
        self.GetEventHandler().ProcessEvent(evt)
        dialog.Destroy()
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
#        if menuState & (MF_GRAYED|MF_DISABLED|MF_SEPARATOR):
        if menuState & (MF_GRAYED|MF_DISABLED):
            continue
        item = itemName.value.replace("&","").split("\t")[0]
        if item == "" and id == 0:
            continue
        checked = bool(menuState & MF_CHECKED)
        if path.isabs(item):
            if not path.isfile(item):
                continue
            else:
                item = path.split(item)[1]
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
        self.il.Add(wx.BitmapFromImage(wx.Image(path.join(IMAGES_DIR, "event.png"), wx.BITMAP_TYPE_PNG)))
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
        evt = EventAfter(newEVT_BUTTON_AFTER, self.id)
        evt.SetValue(self)
        self.GetEventHandler().ProcessEvent(evt)
        event.Skip()


    def OnChange(self, event):
        evt = EventAfter(newEVT_BUTTON_AFTER, self.id)
        evt.SetValue(self)
        self.GetEventHandler().ProcessEvent(evt)
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
        evt = EventAfter(newEVT_BUTTON_AFTER, self.id)
        evt.SetValue(self)
        self.GetEventHandler().ProcessEvent(evt)        
        if event:
            event.Skip()
        

    def OnDeleteAllButton(self, event=None):
        self.DeleteAllItems()
        evt = EventAfter(newEVT_BUTTON_AFTER, self.id)
        evt.SetValue(self)
        self.GetEventHandler().ProcessEvent(evt)
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
            pos = self.posList[self.pos]
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
        eg.TriggerEvent("OSD.%s" % self.plugin.text.opened, prefix = "MPC")
        self.flag = False
        self.Bind(wx.EVT_CLOSE, self.onClose)
        PostMessage(hWnd, WM_COMMAND, 893, 0) #Open MPC GoTo dialog
        editId = 11060
        buttonId = 12024
        moduleName = GetModuleFrom_hWnd(hWnd)
        fndGoToWin = eg.WindowMatcher(moduleName, None, u'#32770', None, None, None, True, 0.0, 0)
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
                if GetDlgCtrlID(edit) == editId and GetClassName(edit) == 'Edit':
                    break
                edit = GetWindow(edit, GW_HWNDNEXT)
            if edit > 0:
                button = edit
                break
        while button > 0:
            if GetDlgCtrlID(button) == buttonId and GetClassName(button) == 'Button':
                break
            button = GetWindow(button, GW_HWNDNEXT)
        if not button:
            self.destroyMenu()
            wx.Yield()
            SetEvent(event)
            return
        self.gotowin = gotowin
        eg.WinApi.Utils.ShowWindow(gotowin, False)
        label = GetWindowText(gotowin)
        child = GetDlgItem(hWnd, 10021)
        if GetClassName(child) ==  "#32770":
            statText = GetDlgItem(child, 12027)
            if GetClassName(statText) ==  "Static":
                total = GetWindowText(statText).split(" / ")[1]
                totalSec = GetSec(total)
                self.total = strftime('%H:%M:%S', gmtime(totalSec))
                if totalSec < 600:                # < 10 min   (skip 3 digits)
                    self.posList = (4,6,7)
                elif totalSec < 3600:             # < 1 hour   (skip 2 digits)
                    self.posList = (3,4,6,7)
                elif totalSec < 360000:           # < 10 hour  (skip 1 digit)
                    self.posList = (1,3,4,6,7)
                else:
                    self.posList = (0,1,3,4,6,7)  # >= 10 hour  (no skip)
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
        buf_size = 1 + SendMessage(self.edit, WM_GETTEXTLENGTH, 0, 0)
        locBuf = create_unicode_buffer(buf_size)
        SendMessage(self.edit,WM_GETTEXT,buf_size,addressof(locBuf)) #Read data from edit box
        data = locBuf.value.split(".")[0]
        wx.CallAfter(self.UpdateOSD, data)
        gotoSize = self.GoToCtrl.GetTextExtent("00:00:00")
        if sizeFlag:
            gotoSize = (1.4*gotoSize[0],gotoSize[1])
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
        buttonId = 12024
        data = self.GoToCtrl.GetValue() + ".0"
        goto = data+"\0"
        locBuf = create_unicode_buffer(len(goto))
        locBuf.value = goto
        SendMessage(self.edit,WM_SETTEXT,0,addressof(locBuf)) #Write data to edit box
        SendMessage(self.gotowin,WM_COMMAND,buttonId+65536*BN_CLICKED, self.button)
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
        eventsCtrl_0.Bind(EVT_BUTTON_AFTER, onFocus)        
        eventsCtrl_1.Bind(EVT_BUTTON_AFTER, onFocus)        
        eventsCtrl_2.Bind(EVT_BUTTON_AFTER, onFocus)        
        eventsCtrl_3.Bind(EVT_BUTTON_AFTER, onFocus)        
        eventsCtrl_4.Bind(EVT_BUTTON_AFTER, onFocus)      
      

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
        child = GetWindow(self.hWnd, GW_CHILD)
        clsName = GetClassName(child)
        if clsName[:4] == "Afx:" and len(clsName) == 41:
            childRect = GetWindowRect(child)
            mons = EnumDisplayMonitors()
            fullscreen = False
            for mon in mons:
                if childRect == mon[2]:
                    fullscreen = True
                    break
            if fullscreen: # Fullscreen !
                SendMessageTimeout(self.hWnd, WM_COMMAND, 830, 0)
                self.messStack.append(830)
                sleep(0.1)
            childRect = GetWindowRect(child)
            parRect = GetWindowRect(self.hWnd)
            if childRect[1] - parRect[1] < 16: # Without menu !
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


    def onDown(self, event):
        wx.CallAfter(self.menuGridCtrl.MoveCursor, 1)


    def onLeft(self, event):
        if len(self.oldMenu) > 0:
            self.menu, ix = self.oldMenu.pop()
            wx.CallAfter(self.UpdateMenu, ix)
        else:
            wx.CallAfter(self.destroyMenu)


    def onRight(self, event):
        wx.CallAfter(self.DefaultAction)


    def onEscape(self, event):
        wx.CallAfter(self.destroyMenu)


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
        try:
            hWnd = FindWindow("MediaPlayerClassicW")
        except:
            raise self.Exceptions.ProgramNotRunning
            return
        try:
            val = eg.ParseString(val)
            val = int(val)
        except:
            raise self.Exception(self.text.error % val)
            return
        return SendMessageTimeout(hWnd, WM_COMMAND, val, 0)


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
        try:
            hWnd = FindWindow("MediaPlayerClassicW")
            return SendMessageTimeout(hWnd, WM_COMMAND, self.value, 0)
        except:
            raise self.Exceptions.ProgramNotRunning
#===============================================================================

class GetTimes(eg.ActionBase):

    name = "Get Times"
    description = "Returns elapsed, remaining and total times."

    def __call__(self):
        try:
            hWnd = FindWindow("MediaPlayerClassicW")
        except:
            eg.programCounter = None
            raise self.Exceptions.ProgramNotRunning
        else:
            try:
                child = GetDlgItem(hWnd, 10021)
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
        try:
            hWnd = FindWindow("MediaPlayerClassicW")
        except:
            eg.programCounter = None
            raise self.Exceptions.ProgramNotRunning
        else:
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
                    hWnd,
                    evtList,
                    sizeFlag
                )
                eg.actionThread.WaitOnEvent(self.event)


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
        foreColourButton = extColourSelectButton(panel,fore, title = self.text.txtColour)
        #Button Background Colour
        backLbl=wx.StaticText(panel, -1, self.text.background+':')
        backColourButton = extColourSelectButton(panel,back, title = self.text.background)
        #Button Selected Text Colour
        foreSelLbl=wx.StaticText(panel, -1, self.text.txtColourSel+':')
        foreSelColourButton = extColourSelectButton(panel,foreSel, title = self.text.txtColourSel)
        #Button Selected Background Colour
        backSelLbl=wx.StaticText(panel, -1, self.text.backgroundSel+':')
        backSelColourButton = extColourSelectButton(panel,backSel, title = self.text.backgroundSel)
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
        foreColourButton.Bind(EVT_BUTTON_AFTER, OnColourBtn)
        backColourButton.Bind(EVT_BUTTON_AFTER, OnColourBtn)
        foreSelColourButton.Bind(EVT_BUTTON_AFTER, OnColourBtn)
        backSelColourButton.Bind(EVT_BUTTON_AFTER, OnColourBtn)

        def setFocus():
            pass
        panel.setFocus = setFocus

        # re-assign the test button
        def OnButton(event):
            try:
                hWnd = FindWindow("MediaPlayerClassicW")
            except:
                self.PrintError(eg.Classes.Exceptions.Text.ProgramNotRunning)
            else:
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
                        hWnd,
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
        try:
            hWnd = FindWindow("MediaPlayerClassicW")
        except:
            eg.programCounter = None
            raise self.Exceptions.ProgramNotRunning
        else:
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
                    hWnd,
                    evtList,
                )
                eg.actionThread.WaitOnEvent(self.event)


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
        fontButton = extFontSelectButton(panel, value = fontInfo)
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
        foreColourButton = extColourSelectButton(panel,fore,title = self.text.txtColour)
        #Button Background Colour
        backLbl=wx.StaticText(panel, -1, self.text.background+':')
        backColourButton = extColourSelectButton(panel,back,title = self.text.background)
        #Button Selected Text Colour
        foreSelLbl=wx.StaticText(panel, -1, self.text.txtColourSel+':')
        foreSelColourButton = extColourSelectButton(panel,foreSel,title = self.text.txtColourSel)
        #Button Selected Background Colour
        backSelLbl=wx.StaticText(panel, -1, self.text.backgroundSel+':')
        backSelColourButton = extColourSelectButton(panel,backSel,title = self.text.backgroundSel)
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
#            listBoxCtrl.SetFocus()
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
        fontButton.Bind(EVT_BUTTON_AFTER, OnFontBtn)

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
        foreColourButton.Bind(EVT_BUTTON_AFTER, OnColourBtn)
        backColourButton.Bind(EVT_BUTTON_AFTER, OnColourBtn)
        foreSelColourButton.Bind(EVT_BUTTON_AFTER, OnColourBtn)
        backSelColourButton.Bind(EVT_BUTTON_AFTER, OnColourBtn)


        def setFocus():
            listBoxCtrl.SetFocus()
        panel.setFocus = setFocus

        # re-assign the test button
        def OnButton(event):
            try:
                hWnd = FindWindow("MediaPlayerClassicW")
            except:
                self.PrintError(eg.Classes.Exceptions.Text.ProgramNotRunning)
            else:
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
                        hWnd,
                        panel.evtList
                    )
                    eg.actionThread.WaitOnEvent(self.event)
#            listBoxCtrl.SetFocus()
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

class MediaPlayerClassic(eg.PluginBase):
    menuDlg = None

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


    def __init__(self):
        self.AddActionsFromList(ACTIONS, ActionPrototype)
        self.AddAction(UserMessage)
        self.AddAction(GetTimes)
        self.AddAction(ShowMenu)
        self.AddAction(GoTo_OSD)
