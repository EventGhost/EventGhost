# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright Â© 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

import eg


eg.RegisterPlugin(
    name=u'FullScreen',
    author=u'K',
    version=u'0.0.1a',
    description=u'Makes a window fullscreen.',
    kind=u'other',
    canMultiLoad=False,
    createMacrosOnAdd=True,
    guid=u'{590AA160-5C6E-48B7-BD8F-FC7AF542C330}',
)

import wx  # NOQA
import os  # NOQA
import ctypes  # NOQA
from ctypes.wintypes import (
    BOOL,
    LONG,
    UINT,
    POINT,
    RECT,
    HWND,
    LPARAM,
    DWORD
) # NOQA
from eg.WinApi import (
    GetWindowText,
    GetTopLevelWindowList,
    GetProcessName
) # NOQA
from eg.WinApi.Utils import GetMonitorDimensions, BringHwndToFront  # NOQA


user32 = ctypes.windll.User32

PID = DWORD

WINDOWS_PATH = eg.folderPath.Windows
SYSTEM32_PATH = eg.folderPath.System

# Retrieves the extended window styles.
GWL_EXSTYLE = -20

# Retrieves a handle to the application instance.
GWL_HINSTANCE = -6

# Retrieves a handle to the parent window, if any.
GWL_HWNDPARENT = -8

# Retrieves the identifier of the window.
GWL_ID = -12

# Retrieves the window styles.
GWL_STYLE = -16

# Retrieves the user data associated with the window. This data is intended
# for use by the application that created the window. Its value is initially
# zero.
GWL_USERDATA = -21

# Retrieves the address of the window procedure, or a handle representing the
# address of the window procedure. You must use the CallWindowProc function to
# call the window procedure.
GWL_WNDPROC = -4

#     ********** ShowWindow
#
# Minimizes a window, even if the thread that owns the window is not
# responding. This flag should only be used when minimizing windows from a
# different thread.
SW_FORCEMINIMIZE = 11

# Hides the window and activates another window.
SW_HIDE = 0

# Maximizes the specified window.
SW_MAXIMIZE = 3

# Minimizes the specified window and activates the next top-level window in
# the Z order.
SW_MINIMIZE = 6

# Activates and displays the window. If the window is minimized or maximized,
# the system restores it to its original size and position. An application
# should specify this flag when restoring a minimized window.
SW_RESTORE = 9

# Activates the window and displays it in its current size and position.
SW_SHOW = 5

# Sets the show state based on the SW_ value specified in the STARTUPINFO
# structure passed to the CreateProcess function by the program that started
# the application.
SW_SHOWDEFAULT = 10

# Activates the window and displays it as a maximized window.
SW_SHOWMAXIMIZED = 3

# Activates the window and displays it as a minimized window.
SW_SHOWMINIMIZED = 2

# Displays the window as a minimized window. This value is similar to
# SW_SHOWMINIMIZED, except the window is not activated.
SW_SHOWMINNOACTIVE = 7

# Displays the window in its current size and position. This value is similar
# to SW_SHOW, except that the window is not activated.
SW_SHOWNA = 8

# Displays a window in its most recent size and position. This value is
# similar to SW_SHOWNORMAL, except that the window is not activated.
SW_SHOWNOACTIVATE = 4

# Activates and displays a window. If the window is minimized or maximized,
# the system restores it to its original size and position. An application
# should specify this flag when displaying the window for the first time.
SW_SHOWNORMAL = 1

# ***** Wnidow Styles

# The window has a thin-line border.
WS_BORDER = 0x00800000

# The window has a title bar (includes the WS_BORDER style).
WS_CAPTION = 0x00C00000

# The window is a child window. A window with this style cannot have a menu
# bar. This style cannot be used with the WS_POPUP style.
WS_CHILD = 0x40000000

# Same as the WS_CHILD style.
WS_CHILDWINDOW = 0x40000000

# Excludes the area occupied by child windows when drawing occurs within the
# parent window. This style is used when creating the parent window.
WS_CLIPCHILDREN = 0x02000000

# Clips child windows relative to each other; that is, when a particular child
# window receives a WM_PAINT message, the WS_CLIPSIBLINGS style clips all
# other overlapping child windows out of the region of the child window to be
# updated. If WS_CLIPSIBLINGS is not specified and child windows overlap,
# it is possible, when drawing within the client area of a child window, to
# draw within the client area of a neighboring child window.
WS_CLIPSIBLINGS = 0x04000000

# The window is initially disabled. A disabled window cannot receive input
# from the user. To change this after a window has been created, use the
# EnableWindow function.
WS_DISABLED = 0x08000000

# The window has a border of a style typically used with dialog boxes. A
# window with this style cannot have a title bar.
WS_DLGFRAME = 0x00400000

# The window is the first control of a group of controls. The group consists
# of this first control and all controls defined after it, up to the next
# control with the WS_GROUP style. The first control in each group usually
# has the WS_TABSTOP style so that the user can move from group to group.
# The user can subsequently change the keyboard focus from one control in
# the group to the next control in the group by using the direction keys.
# You can turn this style on and off to change dialog box navigation. To
# change this style after a window has been created, use the SetWindowLong
# function.
WS_GROUP = 0x00020000

# The window has a horizontal scroll bar.
WS_HSCROLL = 0x00100000

# The window is initially minimized. Same as the WS_MINIMIZE style.
WS_ICONIC = 0x20000000

# The window is initially maximized.
WS_MAXIMIZE = 0x01000000

# The window has a maximize button. Cannot be combined with the
# WS_EX_CONTEXTHELP style. The WS_SYSMENU style must also be specified.
WS_MAXIMIZEBOX = 0x00010000

# The window is initially minimized. Same as the WS_ICONIC style.
WS_MINIMIZE = 0x20000000

# The window has a minimize button. Cannot be combined with the
# WS_EX_CONTEXTHELP style. The WS_SYSMENU style must also be specified.
WS_MINIMIZEBOX = 0x00020000

# The window is an overlapped window. An overlapped window has a title bar
# and a border. Same as the WS_TILED style.
WS_OVERLAPPED = 0x00000000

# The windows is a pop-up window. This style cannot be used with the
# WS_CHILD style.
WS_POPUP = 0x80000000

# The window has a sizing border. Same as the WS_THICKFRAME style.
WS_SIZEBOX = 0x00040000

# The window has a window menu on its title bar. The WS_CAPTION style must
# also be specified.
WS_SYSMENU = 0x00080000

# The window is a control that can receive the keyboard focus when the user
# presses the TAB key. Pressing the TAB key changes the keyboard focus to
# the next control with the WS_TABSTOP style. You can turn this style on
# and off to change dialog box navigation. To change this style after a
# window has been created, use the SetWindowLong function. For user-created
# windows and modeless dialogs to work with tab stops, alter the message
# loop to call the IsDialogMessage function.
WS_TABSTOP = 0x00010000

# The window has a sizing border. Same as the WS_SIZEBOX style.
WS_THICKFRAME = 0x00040000

# The window is an overlapped window. An overlapped window has a title bar
# and a border. Same as the WS_OVERLAPPED style.
WS_TILED = 0x00000000

# The window is an overlapped window. Same as the WS_OVERLAPPEDWINDOW style.
WS_TILEDWINDOW = (
    WS_OVERLAPPED |
    WS_CAPTION |
    WS_SYSMENU |
    WS_THICKFRAME |
    WS_MINIMIZEBOX |
    WS_MAXIMIZEBOX
)

# The window is an overlapped window. Same as the WS_TILEDWINDOW style.
WS_OVERLAPPEDWINDOW = (
    WS_OVERLAPPED |
    WS_CAPTION |
    WS_SYSMENU |
    WS_THICKFRAME |
    WS_MINIMIZEBOX |
    WS_MAXIMIZEBOX
)

# The window is a pop-up window. The WS_CAPTION and WS_POPUPWINDOW styles
# must be combined to make the window menu visible.
WS_POPUPWINDOW = (
    WS_POPUP |
    WS_BORDER |
    WS_SYSMENU
)

# The window is initially visible. This style can be turned on and off by
# using the ShowWindow or SetWindowPos function.
WS_VISIBLE = 0x10000000

# The window has a vertical scroll bar.
WS_VSCROLL = 0x00200000

# ******* Extended Styles

# The window accepts drag-drop files.
WS_EX_ACCEPTFILES = 0x00000010

# Forces a top-level window onto the taskbar when the window is visible.
WS_EX_APPWINDOW = 0x00040000

# The window has a border with a sunken edge.
WS_EX_CLIENTEDGE = 0x00000200

# Paints all descendants of a window in bottom-to-top painting order using
# double-buffering. For more information, see Remarks. This cannot be used if
# the window has a class style of either CS_OWNDC or CS_CLASSDC.
# Windows 2000: This style is not supported.
WS_EX_COMPOSITED = 0x02000000

# The title bar of the window includes a question mark. When the user clicks
# the question mark, the cursor changes to a question mark with a pointer.
# If the user then clicks a child window, the child receives a WM_HELP
# message. The child window should pass the message to the parent window
# procedure, which should call the WinHelp function using the HELP_WM_HELP
# command. The Help application displays a pop-up window that typically
# contains help for the child window. WS_EX_CONTEXTHELP cannot be used with
# the WS_MAXIMIZEBOX or WS_MINIMIZEBOX styles.
WS_EX_CONTEXTHELP = 0x00000400

# The window itself contains child windows that should take part in dialog
# box navigation. If this style is specified, the dialog manager recurses
# into children of this window when performing navigation operations such as
# handling the TAB key, an arrow key, or a keyboard mnemonic.
WS_EX_CONTROLPARENT = 0x00010000

# The window has a double border; the window can, optionally, be created with
# a title bar by specifying the WS_CAPTION style in the dwStyle parameter.
WS_EX_DLGMODALFRAME = 0x00000001

# The window is a layered window. This style cannot be used if the window has
# a class style of either CS_OWNDC or CS_CLASSDC. Windows 8: The WS_EX_LAYERED
# style is supported for top-level windows and child windows. Previous Windows
# versions support WS_EX_LAYERED only for top-level windows.
WS_EX_LAYERED = 0x00080000

# If the shell language is Hebrew, Arabic, or another language that supports
# reading order alignment, the horizontal origin of the window is on the right
# edge. Increasing horizontal values advance to the left.
WS_EX_LAYOUTRTL = 0x00400000

# The window has generic left-aligned properties. This is the default.
WS_EX_LEFT = 0x00000000

# If the shell language is Hebrew, Arabic, or another language that supports
# reading order alignment, the vertical scroll bar (if present) is to the left
# of the client area. For other languages, the style is ignored.
WS_EX_LEFTSCROLLBAR = 0x00004000

# The window text is displayed using left-to-right reading-order properties.
# This is the default.
WS_EX_LTRREADING = 0x00000000

# The window is a MDI child window.
WS_EX_MDICHILD = 0x00000040

# A top-level window created with this style does not become the foreground
# window when the user clicks it. The system does not bring this window to the
# foreground when the user minimizes or closes the foreground window. The
# window should not be activated through programmatic access or via keyboard
# navigation by accessible technology, such as Narrator. To activate the
# window, use the SetActiveWindow or SetForegroundWindow function. The window
# does not appear on the taskbar by default. To force the window to appear on
# the taskbar, use the WS_EX_APPWINDOW style.
WS_EX_NOACTIVATE = 0x08000000

# The window does not pass its window layout to its child windows.
WS_EX_NOINHERITLAYOUT = 0x00100000

# The child window created with this style does not send the WM_PARENTNOTIFY
# message to its parent window when it is created or destroyed.
WS_EX_NOPARENTNOTIFY = 0x00000004

# The window does not render to a redirection surface. This is for windows
# that do not have visible content or that use mechanisms other than surfaces
# to provide their visual.
WS_EX_NOREDIRECTIONBITMAP = 0x00200000

# The window has generic "right-aligned" properties. This depends on the
# window class. This style has an effect only if the shell language is Hebrew,
# Arabic, or another language that supports reading-order alignment;
# otherwise, the style is ignored. Using the WS_EX_RIGHT style for static or
# edit controls has the same effect as using the SS_RIGHT or ES_RIGHT style,
# respectively. Using this style with button controls has the same effect as
# using BS_RIGHT and BS_RIGHTBUTTON styles.
WS_EX_RIGHT = 0x00001000

# The vertical scroll bar (if present) is to the right of the client area.
# This is the default.
WS_EX_RIGHTSCROLLBAR = 0x00000000

# If the shell language is Hebrew, Arabic, or another language that supports
# reading-order alignment, the window text is displayed using right-to-left
# reading-order properties. For other languages, the style is ignored.
WS_EX_RTLREADING = 0x00002000

# The window has a three-dimensional border style intended to be used for
# items that do not accept user input.
WS_EX_STATICEDGE = 0x00020000

# The window is intended to be used as a floating toolbar. A tool window has
# a title bar that is shorter than a normal title bar, and the window title is
# drawn using a smaller font. A tool window does not appear in the taskbar or
# in the dialog that appears when the user presses ALT+TAB. If a tool window
# has a system menu, its icon is not displayed on the title bar. However, you
# can display the system menu by right-clicking or by typing ALT+SPACE.
WS_EX_TOOLWINDOW = 0x00000080

# The window should be placed above all non-topmost windows and should stay
# above them, even when the window is deactivated. To add or remove this
# style, use the SetWindowPos function.
WS_EX_TOPMOST = 0x00000008

# The window should not be painted until siblings beneath the window (that
# were created by the same thread) have been painted. The window appears
# transparent because the bits of underlying sibling windows have already
# been painted. To achieve transparency without these restrictions, use the
# SetWindowRgn function.
WS_EX_TRANSPARENT = 0x00000020

# The window has a border with a raised edge.
WS_EX_WINDOWEDGE = 0x00000100L

# The window is an overlapped window.
WS_EX_OVERLAPPEDWINDOW = (
    WS_EX_WINDOWEDGE |
    WS_EX_CLIENTEDGE
)

# The window is palette window, which is a modeless dialog box that presents
# an array of commands.
WS_EX_PALETTEWINDOW = (
    WS_EX_WINDOWEDGE |
    WS_EX_TOOLWINDOW |
    WS_EX_TOPMOST
)


class tagWINDOWPLACEMENT(ctypes.Structure):
    _fields_ = [
        ('length', UINT),
        ('flags', UINT),
        ('showCmd', UINT),
        ('ptMinPosition', POINT),
        ('ptMaxPosition', POINT),
        ('rcNormalPosition', RECT),
        ('rcDevice', RECT)
    ]


WINDOWPLACEMENT = tagWINDOWPLACEMENT

# BOOL GetWindowPlacement(
#   HWND            hWnd,
#   WINDOWPLACEMENT *lpwndpl
# );
_GetWindowPlacement = user32.GetWindowPlacement
_GetWindowPlacement.restype = BOOL

# LONG GetWindowLongW(
#   HWND hWnd,
#   int  nIndex
# );

_GetWindowLong = user32.GetWindowLongW
_GetWindowLong.restype = LONG

# LONG SetWindowLongW(
#   HWND hWnd,
#   int  nIndex,
#   LONG dwNewLong
# );
_SetWindowLong = user32.SetWindowLongW
_SetWindowLong.restype = LONG

# BOOL ShowWindow(
#   HWND hWnd,
#   int  nCmdShow
# );
_ShowWindow = user32.ShowWindow
_ShowWindow.restype = BOOL

# BOOL SetWindowPlacement(
#   HWND                  hWnd,
#   const WINDOWPLACEMENT *lpwndpl
# );
_SetWindowPlacement = user32.SetWindowPlacement
_SetWindowPlacement.restype = BOOL

# BOOL CALLBACK EnumWindowsProc(
#   _In_ HWND   hwnd,
#   _In_ LPARAM lParam
# );

WNDENUMPROC = ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)

# BOOL EnumWindows(
#   WNDENUMPROC lpEnumFunc,
#   LPARAM      lParam
# );

_EnumWindows = user32.EnumWindows
_EnumWindows.restype = BOOL

# DWORD GetWindowThreadProcessId(
#   HWND    hWnd,
#   LPDWORD lpdwProcessId
# );
_GetWindowThreadProcessId = user32.GetWindowThreadProcessId
_GetWindowThreadProcessId.restype = DWORD


class Text:
    class Fullscreen:
        name = u'Fullscreen'
        description = 'Action Fullscreen'


    class Restore:
        name = u'Restore'
        description = 'Action Restore'


class FullScreenPlugin(eg.PluginBase):
    text = Text

    def __init__(self):
        super(FullScreenPlugin, self).__init__()
        self.styles = {}
        self.AddAction(FullScreen)
        self.AddAction(Restore)

    @property
    def handles(self):
        handles = GetTopLevelWindowList(False)

        found = {}
        for handle in handles:
            pid = PID()
            _GetWindowThreadProcessId(HWND(handle), ctypes.byref(pid))

            window_text = GetWindowText(handle)
            process_name = GetProcessName(pid.value)
            program_name = os.path.splitext(process_name)[0]
            if not window_text:
                continue

            if os.path.exists(os.path.join(WINDOWS_PATH, process_name)):
                continue

            if os.path.exists(os.path.join(SYSTEM32_PATH, process_name)):
                continue

            if program_name in window_text:
                found[process_name] = (program_name, handle)
                continue
            elif process_name in found:
                continue

            window_text = window_text.split('-')

            if len(window_text) == 1:
                window_text = window_text[0]

                if '\\' in window_text:
                    if os.path.exists(window_text):
                        found[process_name] = (program_name, handle)
                    else:
                        found[process_name] = (window_text, handle)
                else:
                    found[process_name] = (window_text, handle)

            else:
                saved_first = window_text[0]
                saved_last = window_text[-1]

                first = window_text[0].lower()
                last = window_text[-1].lower()

                window_text = '-'.join(window_text)

                prog_name = program_name.lower()

                if (
                    prog_name.startswith(first) or
                    prog_name.startswith(first.replace(' ', '')) or
                    first.replace(' ', '').startswith(prog_name) or
                    first.endswith(prog_name)
                ):
                    found[process_name] = (saved_first.strip(), handle)
                    continue
                if (
                    prog_name.startswith(last) or
                    last.startswith(prog_name) or
                    prog_name.startswith(last.replace(' ', '')) or
                    last.replace(' ', '').startswith(prog_name) or
                    last.endswith(prog_name)
                ):
                    found[process_name] = (saved_last.strip(), handle)
                    continue

                if (
                    prog_name.startswith(first.split(' ')[0]) or
                    first.split(' ')[0].startswith(prog_name) or
                    prog_name.startswith(first.split(' ')[-1]) or
                    first.split(' ')[-1].startswith(prog_name)
                ):
                    found[process_name] = (saved_first.strip(), handle)
                    continue
                if (
                    prog_name.startswith(last.split(' ')[0]) or
                    last.split(' ')[0].startswith(prog_name) or
                    prog_name.startswith(last.split(' ')[-1]) or
                    last.split(' ')[-1].startswith(prog_name)
                ):
                    found[process_name] = (saved_last.strip(), handle)

                found[process_name] = (window_text, handle)

        return sorted(list(found.values()))

    @property
    def choices(self):
        return list(label for label, _ in self.handles)


class FullScreen(eg.ActionBase):

    def __call__(self, name, monitor):
        if name in self.plugin.styles:
            return False

        for label, hwnd in self.plugin.handles:
            if label == name:
                break

        else:
            return False

        x, y, w, h = GetMonitorDimensions()[monitor]

        if x < 0:
            x += w / 2
        else:
            x -= w / 2

        y += h / 2

        old_placement = WINDOWPLACEMENT()
        new_placement = WINDOWPLACEMENT()

        if not _GetWindowPlacement(HWND(hwnd), ctypes.byref(old_placement)):
            raise ctypes.WinError()

        new_placement.length = old_placement.length
        new_placement.flags = old_placement.flags
        new_placement.showCmd = old_placement.showCmd
        new_placement.ptMinPosition = old_placement.ptMinPosition
        new_placement.ptMaxPosition = old_placement.ptMaxPosition
        new_placement.rcNormalPosition = RECT(x, y)
        new_placement.rcDevice = old_placement.rcDevice

        _SetWindowPlacement(HWND(hwnd), ctypes.byref(new_placement))

        style = _GetWindowLong(HWND(hwnd), GWL_STYLE)
        style_ex = _GetWindowLong(HWND(hwnd), GWL_EXSTYLE)

        new_style = style
        new_style &= ~WS_BORDER
        new_style &= ~WS_DLGFRAME
        new_style &= ~WS_THICKFRAME

        new_style_ex = style_ex
        new_style_ex &= ~WS_EX_WINDOWEDGE

        _SetWindowLong(HWND(hwnd), GWL_STYLE, new_style | WS_POPUP)

        _SetWindowLong(HWND(hwnd), GWL_EXSTYLE, new_style_ex | WS_EX_TOPMOST)

        if not _ShowWindow(HWND(hwnd), SW_SHOWMAXIMIZED):
            raise ctypes.WinError()

        BringHwndToFront(hwnd)

        self.plugin.styles[name] = (hwnd, style, style_ex, old_placement)
        return True

    def Configure(self, name='', monitor=0):
        panel = eg.ConfigPanel()

        choices = self.plugin.choices
        name_ctrl = wx.Choice(panel, -1, choices=choices)
        name_st = panel.StaticText('Application:')

        monitor_ctrl = panel.DisplayChoice(value=monitor)
        monitor_st = panel.StaticText('Monitor:')

        if name in choices:
            name_ctrl.SetStringSelection(name)
        else:
            name_ctrl.SetSelection(0)

        sts = []
        ctrls = []

        def h_sizer(st, ctrl):
            sts.append(st)
            ctrls.append(ctrl)

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(st, 0, wx.EXPAND | wx.ALL, 5)
            sizer.Add(ctrl, 1, wx.EXPAND | wx.ALL, 5)
            return sizer

        panel.sizer.Add(h_sizer(name_st, name_ctrl))
        panel.sizer.Add(h_sizer(monitor_st, monitor_ctrl))

        eg.EqualizeWidths(tuple(sts))
        eg.EqualizeWidths(tuple(ctrls))

        while panel.Affirmed():
            panel.SetResult(
                name_ctrl.GetStringSelection(),
                monitor_ctrl.GetSelection()
            )


class Restore(eg.ActionBase):

    def __call__(self, name):
        if name in self.plugin.styles:
            hwnd, style, style_ex, placement = self.plugin.styles.pop(name)
            _SetWindowLong(HWND(hwnd), GWL_STYLE, style)
            _SetWindowLong(HWND(hwnd), GWL_EXSTYLE, style_ex)
            _ShowWindow(HWND(hwnd), SW_SHOWNORMAL)
            _SetWindowPlacement(HWND(hwnd), ctypes.byref(placement))

    def Configure(self, name=''):
        panel = eg.ConfigPanel()

        choices = self.plugin.choices
        ctrl = wx.Choice(panel, -1, choices=choices)
        st = panel.StaticText('Application:')

        if name in choices:
            ctrl.SetStringSelection(name)
        else:
            ctrl.SetSelection(0)

        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer.Add(st, 0, wx.EXPAND | wx.ALL, 5)
        h_sizer.Add(ctrl, 1, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(h_sizer)

        while panel.Affirmed():
            panel.SetResult(ctrl.GetStringSelection())
