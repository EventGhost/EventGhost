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

import eg

eg.RegisterPlugin(
    name = "Window",
    author = "Bitmonster & blackwind",
    version = "1.1.2",
    description = (
        "Actions that are related to the control of windows on the desktop, "
        "like finding specific windows, moving, resizing, and sending "
        "keypresses to them."
    ),
    kind = "core",
    guid = "{E974D074-B0A3-4D0C-BBD1-992475DDD69D}",
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=3220",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAV0lEQVR42u2TsRGAAAjE"
        "YDJ+NNgMJ0OwUTo5GgvTfJUcDUxLWFVjHQAwFt2d0r0DwOwQ1eNdIALEzLnRtuQWqJOm"
        "tICIjGQz+wPfCozMB1cgd/dMG7k4AXr8XoPosfNpAAAAAElFTkSuQmCC"
    ),
)


import wx
from win32api import EnumDisplayMonitors, CloseHandle
from eg.WinApi import GetTopLevelWindowList, GetWindowText
from eg.WinApi.Utils import (
    BringHwndToFront, CloseHwnd, GetMonitorDimensions, GetHwndIcon,
    GetAlwaysOnTop, GetBestHwnd, GetContainingMonitor, GetWindowDimensions,
)
from eg.WinApi.Dynamic import (
    # functions:
    SendNotifyMessage, GetAncestor, GetWindowLong, ShowWindow, GetWindowRect,
    GetForegroundWindow, MoveWindow, IsWindow, SetWindowPos, byref,

    # types:
    RECT,

    # constants:
    GA_ROOT, SW_MAXIMIZE, SW_MINIMIZE, SW_RESTORE, WM_COMMAND, GWL_EXSTYLE,
    WS_EX_TOPMOST, SWP_NOMOVE, SWP_NOSIZE, HWND_TOPMOST, HWND_NOTOPMOST,
)
from eg.WinApi.Dynamic import SendMessage as WinApiSendMessage
from eg.WinApi.Dynamic import PostMessage as WinApiPostMessage

# imports local to plugin
from FindWindow import FindWindow
from SendKeys import SendKeys

from win32gui import GetClassName, IsChild, GetParent
from win32gui import SendMessage as win32guiSendMessage
from ctypes import create_string_buffer, addressof, sizeof, c_int
from ctypes import create_unicode_buffer, WinError, Structure
from ctypes.wintypes import UINT, INT, LPWSTR
from eg.WinApi import GetWindowThreadProcessId
from eg.WinApi.Dynamic import _kernel32

from win32con import PAGE_READWRITE, MEM_COMMIT, MEM_RESERVE, MEM_RELEASE,\
    PROCESS_ALL_ACCESS

class LVCOLUMN(Structure):
    _fields_ = [("mask", UINT),
                ("fmt", INT),
                ("cx", INT),
                ("pszText", LPWSTR),
                ("cchTextMax", INT),
                ("iSubItem", INT),
                ("iImage", INT),
                ("iOrder", INT)]

PROCESS_VM_OPERATION      = 8
PROCESS_VM_READ           = 16
#PROCESS_VM_WRITE          = 32
PROCESS_QUERY_INFORMATION = 1024

LVCF_FMT         =  1
LVCF_WIDTH       =  2
LVCF_TEXT        =  4
LVCF_SUBITEM     =  8
LVCF_IMAGE       = 16
LVCF_ORDER       = 32
LVM_GETCOLUMN    = 4121
CB_GETCOUNT      = 326
CB_GETCURSEL     = 327
CB_GETLBTEXT     = 328
LB_ERR           = -1
LB_GETCOUNT      = 395
LB_GETCURSEL     = 392
LB_GETTEXT       = 393
LB_GETSELCOUNT   = 400
LB_GETSELITEMS   = 401
SB_GETPARTS      = 1030
SB_GETTEXTW      = 1037
EM_GETLINECOUNT  = 186
EM_GETLINE       = 196
LVM_GETITEMCOUNT = 4100
LVM_GETITEMSTATE = 4140
LVM_GETITEMTEXT  = 4141
#LVM_GETSELECTIONMARK = 4162
#LVM_GETSELECTEDCOUNT = 4146
LVIS_SELECTED    = 2
#===============================================================================

def GetTargetWindows():
    hwnds = eg.lastFoundWindows
    if not hwnds:
        return [GetForegroundWindow()]
    return hwnds


def GetTopLevelOfTargetWindows():
    hwnds = eg.lastFoundWindows
    if not hwnds:
        return [GetForegroundWindow()]
    return list(set([GetAncestor(hwnd, GA_ROOT) for hwnd in hwnds]))


def pack_int(x):
    res=[]
    for i in range(4):
        res.append(chr(x&0xff))
        x >>= 8
    return ''.join(res)


def match_cls(cls, lst):
    if cls in lst:
        return True
    match = False
    for item in lst:
        if item in cls:
            match = True
            break
    return match
#===============================================================================

class Window(eg.PluginBase):

    def __init__(self):
        self.AddAction(FindWindow)
        self.AddAction(BringToFront)
        self.AddAction(SendKeys)
        self.AddAction(MoveTo)
        self.AddAction(Resize)
        self.AddAction(Maximize)
        self.AddAction(Minimize)
        self.AddAction(Restore)
        self.AddAction(Close)
        self.AddAction(SendMessage)
        self.AddAction(SetAlwaysOnTop)
        self.AddAction(GrabText)
        self.AddAction(DockWindow)
        self.AddAction(MinimizeToTray)

        self.iconDict = {}

class BringToFront(eg.ActionBase):
    name = "Bring to Front"
    description = "Bring the specified window to front."
    iconFile = "icons/BringToFront"

    def __call__(self):
        for hwnd in GetTargetWindows():
            BringHwndToFront(hwnd)
            if self.plugin.iconDict.has_key(hwnd):
                try:  
                    trayIcon = self.plugin.iconDict[hwnd] 
                    del self.plugin.iconDict[hwnd]
                    trayIcon.RemoveIcon()
                    trayIcon.Destroy()
                except:
                    pass

class MoveTo(eg.ActionBase):
    name = "Move Absolute"
    class text:
        label   = "Move window to: Monitor: %i, X: %s, Y: %s"
        text1   = "Set horizontal position X to"
        text2   = "pixels"
        text3   = "Set vertical position Y to"
        display = "Window show on monitor"


    def __call__(self, x, y, displayNumber = 0):
        monitorDimensions = GetMonitorDimensions()
        try:
            displayRect = monitorDimensions[displayNumber]
        except IndexError:
            displayRect = monitorDimensions[0]
        rect = RECT()
        mons = EnumDisplayMonitors(None, None)
        mons = [item[2] for item in mons]
        for hwnd in GetTopLevelOfTargetWindows():
            GetWindowRect(hwnd, byref(rect))
            X = rect.left
            Y = rect.top
            for mon in range(len(mons)):
                if mons[mon][0] <= X and X <= mons[mon][2] and mons[mon][1] <= Y and Y <= mons[mon][3]:
                    break
            if mon == len(mons):
                mon = 0
            if x is None:
                x = rect.left - mons[mon][0]
            if y is None:
                y = rect.top - mons[mon][1]
            x += displayRect[0]
            y += displayRect[1]
            MoveWindow(
                hwnd, x, y, rect.right - rect.left, rect.bottom - rect.top, 1
            )


    def GetLabel(self, x, y, displayNumber):
        return self.text.label % (displayNumber + 1, str(x), str(y))


    def Configure(self, x=0, y=0, displayNumber = None):
        text = self.text
        panel = eg.ConfigPanel()
#        enableDisplay = displayNumber is not None
        enableX = x is not None
        enableY = y is not None
        displayLabel = wx.StaticText(panel, -1, text.display)
#        displayCheckBox = wx.CheckBox(panel, -1, text.display)
#        displayCheckBox.SetValue(enableDisplay)
        if displayNumber is None:
            displayNumber = 0
        displayChoice = eg.DisplayChoice(panel, displayNumber)
#        displayChoice.Enable(enableDisplay)
        xCheckBox = wx.CheckBox(panel, -1, text.text1)
        xCheckBox.SetValue(enableX)
        xCtrl = eg.SpinIntCtrl(panel, -1, 0 if not enableX else x, min=-32768, max=32767)
        xCtrl.Enable(enableX)
        yCheckBox = wx.CheckBox(panel, -1, text.text3)
        yCheckBox.SetValue(enableY)
        yCtrl = eg.SpinIntCtrl(panel, -1, 0 if not enableY else y, min=-32768, max=32767)
        yCtrl.Enable(enableY)

        monsCtrl = eg.MonitorsCtrl(panel, background = (224, 238, 238))
        sizer = wx.GridBagSizer(vgap = 6, hgap = 5)
        sizer.Add(xCheckBox, (0, 0), (1, 1))
        sizer.Add(xCtrl, (0, 1), (1, 1))
        sizer.Add(wx.StaticText(panel,- 1, text.text2), (0, 2), (1, 1))
        sizer.Add(yCheckBox, (1, 0), (1, 1))
        sizer.Add(yCtrl, (1, 1), (1, 1))
        sizer.Add(wx.StaticText(panel, -1, text.text2), (1, 2), (1, 1))
        sizer.Add(displayLabel, (2, 0), (1, 1), flag = wx.TOP, border = 18)
        sizer.Add(displayChoice, (2, 1), (1, 2), flag = wx.TOP, border = 17)
        panel.sizer.Add(sizer, 1, wx.EXPAND)
        panel.sizer.Add(monsCtrl)

        def HandleXCheckBox(event):
            xCtrl.Enable(event.IsChecked())
            event.Skip()
        xCheckBox.Bind(wx.EVT_CHECKBOX, HandleXCheckBox)

        def HandleYCheckBox(event):
            yCtrl.Enable(event.IsChecked())
            event.Skip()
        yCheckBox.Bind(wx.EVT_CHECKBOX, HandleYCheckBox)

        while panel.Affirmed():
            panel.SetResult(
                xCtrl.GetValue() if xCtrl.IsEnabled() else None,
                yCtrl.GetValue() if yCtrl.IsEnabled() else None,
                displayChoice.GetValue()
            )


class Resize(eg.ActionBase):
    name = "Resize"
    description = "Resizes a window to the specified dimension."
    class text:
        label = "Resize window to %s, %s"
        text1 = "Set width to"
        text2 = "pixels"
        text3 = "Set height to"


    def __call__(self, width=None, height=None):
        rect = RECT()
        for hwnd in GetTopLevelOfTargetWindows():
            GetWindowRect(hwnd, byref(rect))
            if width is None:
                width = rect.right - rect.left - 1
            if height is None:
                height = rect.bottom - rect.top - 1
            MoveWindow(hwnd, rect.left, rect.top, width+1, height+1, 1)


    def GetLabel(self, x, y):
        return self.text.label % (str(x), str(y))


    def Configure(self, x=0, y=0):
        text = self.text
        panel = eg.ConfigPanel()
        xCheckBox = panel.CheckBox(x is not None, text.text1)
        xCtrl = panel.SpinIntCtrl(0 if x is None else x, min=-32768, max=32767)
        xCtrl.Enable(x is not None)
        yCheckBox = panel.CheckBox(y is not None, text.text3)
        yCtrl = panel.SpinIntCtrl(0 if y is None else y, min=-32768, max=32767)
        yCtrl.Enable(y is not None)

        def HandleXCheckBox(event):
            xCtrl.Enable(event.IsChecked())
            event.Skip()
        xCheckBox.Bind(wx.EVT_CHECKBOX, HandleXCheckBox)

        def HandleYCheckBox(event):
            yCtrl.Enable(event.IsChecked())
            event.Skip()
        yCheckBox.Bind(wx.EVT_CHECKBOX, HandleYCheckBox)

        panel.AddLine(xCheckBox, xCtrl, text.text2)
        panel.AddLine(yCheckBox, yCtrl, text.text2)

        while panel.Affirmed():
            panel.SetResult(
                xCtrl.GetValue() if xCtrl.IsEnabled() else None,
                yCtrl.GetValue() if yCtrl.IsEnabled() else None,
            )


class Maximize(eg.ActionBase):
    name = "Maximize"

    def __call__(self):
        for hwnd in GetTopLevelOfTargetWindows():
            ShowWindow(hwnd, SW_MAXIMIZE)



class Minimize(eg.ActionBase):
    name = "Minimize"

    def __call__(self):
        for hwnd in GetTopLevelOfTargetWindows():
            ShowWindow(hwnd, SW_MINIMIZE)



class Restore(eg.ActionBase):
    name = "Restore"

    def __call__(self):
        for hwnd in GetTopLevelOfTargetWindows():
            ShowWindow(hwnd, SW_RESTORE)
            if self.plugin.iconDict.has_key(hwnd):
                try:  
                    trayIcon = self.plugin.iconDict[hwnd]
                    del self.plugin.iconDict[hwnd]
                    trayIcon.RemoveIcon()
                    trayIcon.Destroy()
                except:
                    pass



class Close(eg.ActionBase):
    name = "Close"
    description = "Closes application windows"

    def __call__(self):
        for hwnd in GetTopLevelOfTargetWindows():
            CloseHwnd(hwnd)


class SendMessage(eg.ActionBase):
    name = "Send Message"
    description = \
        "Uses the Windows-API SendMessage function to "\
        "send a window a specified message. Can also use "\
        "PostMessage if desired."
    class text:
        text1 = "Use PostMessage instead of SendMessage"

    msgConstants = (
        (273, "WM_COMMAND"),
        (274, "WM_SYSCOMMAND"),
        (793, "WM_APPCOMMAND"),
        (245, "BM_CLICK"),
    )
    msgToNameDict = dict(msgConstants)


    def __call__(self, mesg, wParam=0, lParam=0, kind=0):
        result = None
        for hwnd in GetTargetWindows():
            if kind == 0:
                result = WinApiSendMessage(hwnd, mesg, wParam, lParam)
            else:
                result = WinApiPostMessage(hwnd, mesg, wParam, lParam)
        return result


    def GetLabel(self, mesg, wParam=0, lParam=0, kind=0):
        return self.name + " %s, %d, %d" % (
            self.msgToNameDict.get(mesg, str(mesg)),
            wParam,
            lParam
        )


    def Configure(self, mesg=WM_COMMAND, wParam=0, lParam=0, kind=0):
        mesgValues, mesgNames = zip(*self.msgConstants)
        mesgValues, mesgNames = list(mesgValues), list(mesgNames)
        try:
            i = mesgValues.index(mesg)
            choice = mesgNames[i]
        except:
            choice = str(mesg)

        panel = eg.ConfigPanel()

        mesgCtrl = panel.ComboBox(
            choice,
            mesgNames,
            style=wx.CB_DROPDOWN,
            validator=eg.DigitOnlyValidator(mesgNames)
        )

        wParamCtrl = panel.SpinIntCtrl(wParam, max=65535)
        lParamCtrl = panel.SpinIntCtrl(lParam, max=4294967295)
        kindCB = panel.CheckBox(kind==1, self.text.text1)

        panel.AddLine("Message:", mesgCtrl)
        panel.AddLine("wParam:", wParamCtrl)
        panel.AddLine("lParam:", lParamCtrl)
        #panel.AddLine()
        panel.AddLine(kindCB)

        while panel.Affirmed():
            choice = mesgCtrl.GetValue()
            try:
                i = mesgNames.index(choice)
                mesg = mesgValues[i]
            except:
                mesg = int(choice)
            panel.SetResult(
                mesg,
                wParamCtrl.GetValue(),
                lParamCtrl.GetValue(),
                1 if kindCB.GetValue() else 0
            )



class SetAlwaysOnTop(eg.ActionBase):
    name = "Always on Top"
    class text:
        radioBox = "Choose action:"
        actions = (
            "Clear always on top",
            "Set always on top",
            "Toggle always on top"
        )

    def __call__(self, action=2):
        for hwnd in GetTargetWindows():
            if not IsWindow(hwnd):
                self.PrintError("Not a window")
                continue
            isAlwaysOnTop = GetAlwaysOnTop(hwnd)
            if action == 1 or (action == 2 and not isAlwaysOnTop):
                flag = HWND_TOPMOST
            else:
                flag = HWND_NOTOPMOST

            SetWindowPos(hwnd, flag, 0, 0, 0, 0, SWP_NOMOVE|SWP_NOSIZE)
        return GetAlwaysOnTop(hwnd)


    def GetLabel(self, action):
        return self.text.actions[action]


    def Configure(self, action=2):
        panel = eg.ConfigPanel()
        radioBox = wx.RadioBox(
            panel,
            -1,
            self.text.radioBox,
            choices=self.text.actions,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(action)
        panel.sizer.Add(radioBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(radioBox.GetSelection())


class GrabText(eg.ActionBase):
    name = "Grab Text Item(s)"
#=========================================================================================================
# Sources:
# winGuiAuto.py (Simon Brunning - simon@brunningonline.net)
# http://www.java2s.com/Open-Source/Python/Windows/Venster/venster-0.72/venster/comctl.py.htm
# http://www.java2s.com/Open-Source/Python/GUI/Python-Win32-GUI-Automation/pywinauto-0.4.0/pywinauto/controls/common_controls.py.htm
# http://www.java2s.com/Open-Source/Python/GUI/Python-Win32-GUI-Automation/pywinauto-0.4.0/pywinauto/controls/win32_controls.py.htm
# http://stackoverflow.com/questions/1872480/use-python-to-extract-listview-items-from-another-application
# Note: this only works on 32 bit Python, and only for 32 bit 'other' processes.
# Pako
#=========================================================================================================

    class text:
        onlySel = "Return only selected item(s)"
        onlySelToolTip = """Return only selected item(s).
For example: ComboBox, ListBox, ListView"""

    def Configure(self, only_sel = False):
        panel = eg.ConfigPanel(self)
        onlySelCtrl = wx.CheckBox(panel, -1, self.text.onlySel)
        onlySelCtrl.SetValue(only_sel)
        onlySelCtrl.SetToolTip(wx.ToolTip(self.text.onlySelToolTip))
        panel.AddCtrl(onlySelCtrl)

        while panel.Affirmed():
            panel.SetResult(onlySelCtrl.GetValue(),
            )

    def GetLabel(self, only_sel = False):
        return "%s: %s: %s" % (self.name, self.text.onlySel, str(only_sel))


    def __call__(self, only_sel = False):
        self.only_sel = only_sel
        from win32_ctrls import win32_ctrls
        res = []
        for hwnd in GetTargetWindows():
            if not IsWindow(hwnd):
                self.PrintError("Not a window")
                continue
            clsName = GetClassName(hwnd)
            if not IsChild(GetParent(hwnd), hwnd) or clsName in win32_ctrls['statics']:
                val = eg.WinApi.GetWindowText(hwnd)
            elif clsName in win32_ctrls['edits']:
                val = self.getEditText(hwnd)
            elif clsName in win32_ctrls['combos']:
                val = self.getComboboxItems(hwnd)
            elif clsName in win32_ctrls['listboxes']:
                val = self.getListboxItems(hwnd)
            elif clsName in win32_ctrls['listviews']:
                val = self.getListViewItems(hwnd)
            elif match_cls(clsName, win32_ctrls['statusbars']):
                val = self.getStatusBarItems(hwnd)
            else:
                val = None
            res.append(val)
        return res


    def getMultipleValues(self, hwnd, CountMessg, ValMessg, selected = None):
        buf_size = 512
        buf = create_string_buffer(pack_int(buf_size), buf_size)
        indexes = selected if selected else range(win32guiSendMessage(hwnd, CountMessg, 0, 0))
        val = []
        for ix in indexes:
            valLngth = win32guiSendMessage(hwnd, ValMessg, ix, addressof(buf))
            val.append(buf.value[:valLngth].decode(eg.systemEncoding))
        return val


    def getEditText(self, hwnd):
        return self.getMultipleValues(hwnd, EM_GETLINECOUNT, EM_GETLINE)


    def getListboxItems(self, hwnd):
        if self.only_sel:
            num_selected = win32guiSendMessage(hwnd, LB_GETSELCOUNT, 0, 0)
            if num_selected == LB_ERR: # if we got LB_ERR then it is a single selection list box
                items = (win32guiSendMessage(hwnd, LB_GETCURSEL, 0, 0), )
            else: # otherwise it is a multiselection list box
                items = (c_int * num_selected)()
                win32guiSendMessage(hwnd, LB_GETSELITEMS, num_selected, addressof(items))
                items = tuple(items) # Convert from Ctypes array to a python tuple
        else:
            items = None
        return self.getMultipleValues(hwnd, LB_GETCOUNT, LB_GETTEXT, items)


    def getComboboxItems(self, hwnd):
        if self.only_sel:
            items = (win32guiSendMessage(hwnd, CB_GETCURSEL, 0, 0), )
        else:
            items = None
        return self.getMultipleValues(hwnd, CB_GETCOUNT, CB_GETLBTEXT, items)


    def getStatusBarItems(self, hwnd, buf_len = 512):
        """If success, return statusbar texts like list of strings.
        Otherwise return either '>>> No process ! <<<' or '>>> No parts ! <<<'.
        Mandatory argument: handle of statusbar.
        Option argument: length of text buffer."""
        pid = GetWindowThreadProcessId(hwnd)[1]
        process = _kernel32.OpenProcess(PROCESS_VM_OPERATION|PROCESS_VM_READ|PROCESS_QUERY_INFORMATION, False, pid)
        res_val = ['>>> No process ! <<<',]
        if process:
            parts = win32guiSendMessage(hwnd, SB_GETPARTS, 0, 0)
            partList = []
            res_val = ['>>> No parts ! <<<',]
            if parts > 0:
                remBuf = _kernel32.VirtualAllocEx(process, None, buf_len, MEM_COMMIT, PAGE_READWRITE)
                locBuf = create_unicode_buffer(buf_len)
                for item in range(parts):
                    win32guiSendMessage(hwnd, SB_GETTEXTW, item, remBuf)
                    _kernel32.ReadProcessMemory(process, remBuf, locBuf, buf_len, None) #copy remBuf to locBuf
                    partList.append(locBuf.value)
                res_val =  partList
                _kernel32.VirtualFreeEx(process, remBuf, 0, MEM_RELEASE)
                CloseHandle(process)
        return res_val


    def getListViewItems(self, hwnd):
        col = LVCOLUMN()
        col.mask = LVCF_FMT | LVCF_IMAGE | LVCF_ORDER | LVCF_SUBITEM | LVCF_TEXT | LVCF_WIDTH
        pid = GetWindowThreadProcessId(hwnd)[1]
        hProcHnd = _kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        pLVI = _kernel32.VirtualAllocEx(hProcHnd, 0, 4096, MEM_RESERVE |MEM_COMMIT, PAGE_READWRITE)
        col.cchTextMax = 2000
        col.pszText = pLVI + sizeof(col) + 1
        ret = _kernel32.WriteProcessMemory(hProcHnd, pLVI, addressof(col), sizeof(col), 0)
        if not ret:
            raise WinError()
        retval = 1
        col_count = 0
        while retval: # Columns enumeration
            try:
                retval = win32guiSendMessage(hwnd, LVM_GETCOLUMN, col_count, pLVI)
            except:
                retval = 0
                raise
            col_count += 1
        pBuffer = _kernel32.VirtualAllocEx(hProcHnd, 0, 4096, MEM_RESERVE|MEM_COMMIT, PAGE_READWRITE)
        lvitem_str = 20 * "\x00" + pack_int(pBuffer) + pack_int(4096) + 8 * "\x00"
        lvitem_buffer = create_string_buffer(lvitem_str)
        num_items = win32guiSendMessage(hwnd, LVM_GETITEMCOUNT)
        res = []
        for column_index in range(col_count):
            lvitem_buffer.__setslice__(8, 12, pack_int(column_index)) #column index increment
            _kernel32.WriteProcessMemory(hProcHnd, pLVI, addressof(lvitem_buffer), sizeof(lvitem_buffer), 0)
            target_buff = create_string_buffer(4096)
            item_texts = []
            for item_index in range(num_items):
                if self.only_sel:
                    if not win32guiSendMessage(hwnd, LVM_GETITEMSTATE, item_index, LVIS_SELECTED):
                        continue
                win32guiSendMessage(hwnd, LVM_GETITEMTEXT, item_index, pLVI)
                _kernel32.ReadProcessMemory(hProcHnd, pBuffer, addressof(target_buff), 4096, 0)
                item_texts.append(target_buff.value)
            res.append(item_texts)
        _kernel32.VirtualFreeEx(hProcHnd, pBuffer, 0, MEM_RELEASE)
        _kernel32.VirtualFreeEx(hProcHnd, pLVI, 0, MEM_RELEASE)
        CloseHandle(hProcHnd)
        return map(list, zip(*res)) #Transposing Two-Dimensional Arrays by Steve Holden


class DockWindow(eg.ActionBase):
    name = "Dock Window"
    description = "Moves the specified window to the specified edge(s) of your screen. Respects multi-monitor configurations."

    hChoices = ["[no change]", "Left", "Center", "Right"]
    vChoices = ["[no change]", "Top", "Center", "Bottom"]

    def __call__(self, h, v, hwnd = None):
        hwnd = GetBestHwnd(hwnd)
        win = GetWindowDimensions(hwnd)
        mon, i = GetContainingMonitor(win)

        # Choose horizontal position
        if h == 1:
            x = mon.left
        elif h == 2:
            x = mon.left + (mon.width / 2) - (win.width / 2)
        elif h == 3:
            x = mon.left + mon.width - win.width
        else:
            x = win.left

        # Choose vertical position
        if v == 1:
            y = mon.top
        elif v == 2:
            y = mon.top + (mon.height / 2) - (win.height / 2)
        elif v == 3:
            y = mon.top + mon.height - win.height
        else:
            y = win.top

        # Move window to the specified location
        MoveWindow(hwnd, x, y, win.width, win.height, 1)


    def Configure(self, h = 0, v = 0):
        panel = eg.ConfigPanel()
        vCtrl = panel.ComboBox(self.vChoices[v], self.vChoices, style = wx.CB_READONLY)
        hCtrl = panel.ComboBox(self.hChoices[h], self.hChoices, style = wx.CB_READONLY)
        panel.AddLine("Vertical Position:", vCtrl)
        panel.AddLine("Horizontal Position:", hCtrl)
        while panel.Affirmed():
            panel.SetResult(self.hChoices.index(hCtrl.GetValue()),
                            self.vChoices.index(vCtrl.GetValue()))


    def GetLabel(self, h, v):
        return "Dock Window: V: " + self.vChoices[v] + ", H: " + self.hChoices[h]


class MinimizeToTray(eg.ActionBase):
    name = "Minimize to Tray"
    description = "Minimizes the specified window to the system tray."

    #def OnClick(self, *dummyArgs):
    #    # Remove our tray icon and restore the window
    #    try:
    #        BringHwndToFront(hwnd)
    #        #wx.CallAfter(BringHwndToFront, hwnd)
    #    except:
    #        pass
    #    finally:
    #        trayIcon.RemoveIcon()
    #        trayIcon.Destroy()

    def __call__(self, hwnd = None):
        # Gather info about the target window
        hwnd = GetBestHwnd(hwnd)
        icon = GetHwndIcon(hwnd)
        title = unicode(GetWindowText(hwnd))

        # If valid, minimize target to the systray
        if hwnd in eg.WinApi.GetTopLevelWindowList(False) and isinstance(icon, wx._gdi.Icon):
            trayIcon = wx.TaskBarIcon()
            trayIcon.SetIcon(icon, title)
            self.plugin.iconDict[hwnd] = trayIcon

            #def OnClick(self, *dummyArgs):
            #    # Remove our tray icon and restore the window
            #    try:
            #        BringHwndToFront(hwnd)
            #    except:
            #        pass
            #    finally:
            #        trayIcon.RemoveIcon()
            #        trayIcon.Destroy()

            def OnClick2():
                # Remove our tray icon and restore the window
                try:
                    BringHwndToFront(hwnd)
                    del self.plugin.iconDict[hwnd]
                except:
                    pass
                finally:
                    trayIcon.RemoveIcon()
                    trayIcon.Destroy()
            def OnClick(*dummyArgs):
                wx.CallAfter(OnClick2)
                

            trayIcon.Bind(wx.EVT_TASKBAR_LEFT_UP, OnClick)
            wx.CallAfter(ShowWindow, hwnd, 0)

