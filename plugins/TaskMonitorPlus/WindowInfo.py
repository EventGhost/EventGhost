# -*- coding: utf-8 -*-
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

from os.path import splitext
import win32gui
import win32con
from wx import GetProcessId

import eg
from eg.WinApi import GetClassName, GetWindowText
from eg.WinApi.Utils import GetProcessName
from eg.WinApi.Dynamic import (
    byref, DWORD, GetWindowThreadProcessId, IsWindowVisible,
)

# used for getting our own window name, since some people experience a freeze
# otherwise:
# http://www.eventghost.net/forum/viewtopic.php?f=9&t=9804&p=48065#p48062
ourName = '['+eg.APP_NAME+']'

class WindowInfo(object):
    """
    Class representing an individual window. Interesting attributes:
    - hwnd: window ID
    - pid: PID of process that owns this window
    - name: executable name of process that owns this window
    - title: window's title (updated dynamically if possible)
    - window_class: window's class name (updated dynamically if possible)
    """

    class DeadWindow(AssertionError): pass
    class NoParent(ValueError): pass

    def __init__(self, hwnd):
        if not hwnd:
            raise ValueError("Invalid hwnd")
        self.hwnd = hwnd
        dwProcessId = DWORD()
        GetWindowThreadProcessId(hwnd, byref(dwProcessId))
        self.pid = dwProcessId.value
        self.name = splitext(GetProcessName(self.pid))[0]
        # The following may change during a window's lifetime
        self.cached_title = ourName if self.pid == GetProcessId() else GetWindowText(hwnd)
        self.cached_class = GetClassName(hwnd)

    # If the window is closed, GetWindowText() and GetClassName() will return
    # the empty string. Return the cached values we have instead.
    @property
    def title(self):
        if self.IsAlive():
            self.cached_title = ourName if self.pid == GetProcessId() else GetWindowText(self.hwnd)
        return self.cached_title

    @property
    def window_class(self):
        if self.IsAlive():
            self.cached_class = GetClassName(self.hwnd)
        return self.cached_class

    def __repr__(self):
        """EventGhost uses this to show the event's payload in the log."""
        return "<title={}, window_class={},...>".format(repr(self.title), repr(self.window_class))

    def __getitem__(self, item):
        return getattr(self, item)

    def AssertAlive(self):
        """
        Called internally by functions that require their target window to
        still be open.
        """
        if not self.IsAlive():
            raise WindowInfo.DeadWindow("window no longer exists")

    # Methods for querying and modifying details about this window
    # (size, etc.)

    def IsAlive(self):
        """
        Checks to make sure the window is still open
        :return: True if window is still open else False
        :rtype: bool
        """
        return bool(win32gui.IsWindow(self.hwnd))

    def IsActive(self):
        """
        Checks to see if the window is the active window
        :return: True if window is active else False
        :rtype: bool
        """
        return self.hwnd == win32gui.GetActiveWindow()

    def Animate(
        self,
        slide=False,
        blend=False,
        direction='',
        show=False,
        hide=False,
        duration=150
    ):
        """
        Animates the hiding and showing of the window
        :param slide: Use the slide effect
        :type slide: bool
        :param blend: Use the blend effect
        :type blend: bool
        :param direction: the direction of the effect. choose from,
            'UP', 'DOWN', 'LEFT', 'RIGHT', ''
        :type direction: str
        :param show: Use effect when showing the window
        :type show: bool
        :param hide: Use the effect when hiding the window
        :type hide: bool
        :param duration: How long the total effect should run for in
            milliseconds
        :type duration: int
        :return: None
        :rtype: None
        """
        self.AssertAlive()
        if slide and blend:
            eg.PrintNotice(
                'You are only allowed to select one type of effect, '
                'or set both to False for roll effect.'
            )
            return

        style = 0

        if direction.upper() == 'UP':
            style |= win32con.AW_HOR_NEGATIVE
        elif direction.upper() == 'DOWN':
            style |= win32con.AW_HOR_POSITIVE
        elif direction.upper() == 'LEFT':
            style |= win32con.AW_VER_NEGATIVE
        elif direction.upper() == 'RIGHT':
            style |= win32con.AW_VER_POSITIVE
        else:
            style |= win32con.AW_CENTER

        if hide:
            style |= win32con.AW_HIDE
        if show:
            style |= win32con.AW_ACTIVATE

        if slide:
            style |= win32con.AW_SLIDE

        elif blend:
            style |= win32con.AW_BLEND

        win32gui.AnimateWindow(self.hwnd, duration, style)

    def SendKeystrokes(self, text, useAlternateMethod=False, mode=2):
        """
        Send keystrokes to the window

        :param text: Keystrokes you want to send. Same format as the
            Send Keys Action
        :type text: str
        :param useAlternateMethod: see eg.SendKeys()
        :type useAlternateMethod: bool
        :param mode: see eg.SendKeys()
        :type mode: int
        :return: None
        :rtype: None
        """
        self.AssertAlive()
        import time
        time.sleep(0.1)
        eg.SendKeys(win32gui.GetWindow(self.hwnd, win32con.GW_CHILD), text,
            useAlternateMethod, mode)

    def Flash(
        self,
        caption=True,
        tray=False,
        until_active=False,
        continuous=False,
        times=10,
        speed=250
    ):
        """
        Flashes the caption or tray button for a duration.
        :param caption: Flash the caption
        :type caption: bool
        :param tray: Flash the tray
        :type tray: bool
        :param until_active: Flash until window is activated
        :type until_active: bool
        :param continuous: Keep flashing until stopped. To stop the
            flashing you need to call this method with caption and tray
            set to False
        :type continuous: bool
        :param times: The number of time to flash (not used if until_active
            or continuous is set)
        :type times: int
        :param speed: The duration of time between flashes in milliseconds
        :type speed: int
        :return: None
        :rtype: None
        """
        self.AssertAlive()
        flag = 0

        if until_active:
            flag |= win32con.FLASHW_TIMERNOFG
        elif continuous:
            flag |= win32con.FLASHW_TIMER

        if tray and caption:
            flag |= win32con.FLASHW_ALL
        elif tray:
            flag |= win32con.FLASHW_TRAY
        elif caption:
            flag |= win32con.FLASHW_CAPTION
        else:
            flag = win32con.FLASHW_STOP

        win32gui.FlashWindowEx(self.hwnd, flag, times, speed)

    def BringToTop(self):
        """
        Brings the window to the front.
        :return: None
        :rtype: None
        """
        self.AssertAlive()
        win32gui.BringWindowToTop(self.hwnd)

    def IsVisible(self):
        """
        Checks if the window is visible or not.
        :return: True if visible else False
        :rtype: bool
        """
        return bool(win32gui.IsWindowVisible(self.hwnd))

    def EnableKeyboardMouse(self, enable=True):
        """
        Enables mouse and keyboard input for the window.
        :param enable: True to enable False to disable
        :type enable: bool
        :return: None
        :rtype: None
        """
        self.AssertAlive()
        win32gui.EnableWindow(self.hwnd, enable)

    def IsKeyboardMouseEnabled(self):
        """
        Checks if keyboard and mouse are enabled.
        :return: True if enabled else False
        :rtype: bool
        """
        return bool(win32gui.IsWindowEnabled(self.hwnd))

    def Restore(self, default=False):
        """
        Restores the window to it's previous state.
        :param default: Use startup position and size
        :type default: bool
        :return: None
        :rtype: None
        """
        self.AssertAlive()
        if self.IsVisible():
            if default:
                activate = win32con.SW_SHOWNORMAL
            else:
                activate = win32con.SW_RESTORE
        else:
            activate = win32con.SW_SHOWNORMAL

        win32gui.ShowWindow(self.hwnd, activate)

    def Minimize(self, activate=True, force=False):
        """
        Minimize the window.
        :param activate: Activate the window after minimizing it
        :type activate: bool
        :param force: Force the window to minimize, even if it is frozen
        :type force: bool
        :return: None
        :rtype: bool
        """
        self.AssertAlive()
        if self.IsVisible():
            if activate:
                activate = win32con.SW_MINIMIZE
            else:
                activate = win32con.SW_SHOWMINNOACTIVE
        else:
            if activate:
                activate = win32con.SW_SHOWMINIMIZED
            else:
                activate = win32con.SW_SHOWMINNOACTIVE

        if force:
            activate = win32con.SW_FORCEMINIMIZE

        win32gui.ShowWindow(self.hwnd, activate)

    def Maximize(self):
        """
        Maximize the window.
        :return: None
        :rtype: None
        """
        self.AssertAlive()
        if self.IsVisible():
            activate = win32con.SW_MAXIMIZE
        else:
            activate = win32con.SW_SHOWMAXIMIZED
        win32gui.ShowWindow(self.hwnd, activate)

    def SetPosition(self, *args):
        """
        Sets the position of the window.
        :param args: This can be any of the following,
            wx.Point(x, y)
            wx.Rect(x, y, width, height)
            (x, y)
            x, y
        :type args: tuple, wx.Point, wx.Rect, int
        :return: None
        :rtype: None
        """
        self.AssertAlive()
        if len(args) == 1:
            args = args[0]

        if isinstance(args, wx.Point):
            args = args.Get()
        elif isinstance(args, wx.Rect):
            args = args.Get()[:2]

        win32gui.SetWindowPos(
            self.hwnd,
            self.hwnd,
            args[0],
            args[1],
            0,
            0,
            (
                win32con.SWP_NOSIZE |
                win32con.SWP_NOZORDER |
                win32con.SWP_NOOWNERZORDER
            )
        )

    def SetSize(self, *args):
        """
        Sets the size of the window.
        :param args: Can be any one of the following,
            wx.Size(width, height)
            wx.Rect(x, y, width height)
            (width, height)
            width, height
        :type args: tuple, wx.Size, wx.Rect, int
        :return: None
        :rtype: None
        """
        self.AssertAlive()
        if len(args) == 1:
            args = args[0]

        if isinstance(args, wx.Size):
            args = args.Get()
        elif isinstance(args, wx.Rect):
            args = args.Get()[2:]

        win32gui.SetWindowPos(
            self.hwnd,
            self.hwnd,
            0,
            0,
            args[0],
            args[1],
            (
                win32con.SWP_NOMOVE |
                win32con.SWP_NOZORDER |
                win32con.SWP_NOOWNERZORDER
            )
        )

    def SetRect(self, *args):
        """
        Sets the position and size.
        :param args: Can be any of the following,
            wx.Rect(x, y, width, height)
            x, y, width, height
            (x, y, width, height)
            ((x, y), (width, height))
        :type args: tuple, wx.Rect, int
        :return: None
        :rtype: None
        """
        self.AssertAlive()
        if len(args) == 1:
            args = args[0]

        elif len(args) == 2:
            size = args[0]
            pos = args[1]
            if isinstance(size, wx.Size):
                size = size.Get()
            if isinstance(pos, wx.Point):
                pos = pos.Get()

            args = size + pos

        if isinstance(args, wx.Rect):
            args = args.Get()

        self.SetSize(args[2:])
        self.SetPosition(args[:2])

    def GetRect(self):
        """
        Gets the current window rect.
        :return: a `wx.Rect <https://wxpython.org/Phoenix/docs/html/wx.Rect.html/>`_ object
        :rtype: wx.Rect
        """
        self.AssertAlive()
        return wx.Rect(*self.GetRectTuple())

    def GetRectTuple(self):
        """
        Gets the current window rect.
        :return: (x, y, width, height)
        :rtype: tuple
        """
        self.AssertAlive()
        x, y, b_x, b_y = win32gui.GetWindowRect(self.hwnd)
        return x, y, x + b_x, y + b_y

    def GetSize(self):
        """
        Gets the current window size.
        :return: a `wx.Size <https://wxpython.org/Phoenix/docs/html/wx.Size.html/>`_ object
        :rtype: wx.Size
        """
        self.AssertAlive()
        return wx.Size(*self.GetSizeTuple())

    def GetSizeTuple(self):
        """
        Gets the current window size.
        :return: (width, height)
        :rtype: tuple
        """
        self.AssertAlive()
        rect = self.GetRect()
        return rect.Width, rect.Height

    def GetPosition(self):
        """
        Gets the current window position.
        :return: a `wx.Point <https://wxpython.org/Phoenix/docs/html/wx.Point.html/>`_ object
        :rtype: wx.Point
        """
        self.AssertAlive()
        return wx.Point(*self.GetPositionTuple())

    def GetPositionTuple(self):
        """
        Gets the current window position.
        :return: (x, y)
        :rtype: tuple
        """
        self.AssertAlive()
        rect = self.GetRect()
        return rect.X, rect.Y

    def Show(self, flag=True, activate=True, default=False):
        """
        Show the window.
        :param flag: True to show False to hide
        :type flag: bool
        :param activate: True to activate window False to not
        :type activate: bool
        :param default: Use window default size and position
        :type default: bool
        :return: None
        :rtype: None
        """
        self.AssertAlive()
        if activate:
            if default:
                activate = win32con.SW_SHOWDEFAULT
            else:
                activate = win32con.SW_SHOW
        else:
            if default:
                activate = win32con.SW_SHOWNA

            else:
                activate = win32con.SW_SHOWNOACTIVATE

        if not flag:
            activate = win32con.SW_HIDE

        win32gui.ShowWindow(self.hwnd, activate)

    def Hide(self):
        """
        Hides the window.
        :return: None
        :rtype: None
        """
        self.AssertAlive()
        self.Show(False)

    def Destroy(self):
        """
        Destroys the window.
        :return: None
        :rtype: None
        """
        self.AssertAlive()
        self.PostMessage(win32con.WM_DESTROY, 0, 0)

    def Close(self):
        """
        Closes the window.
        :return: None
        :rtype: None
        """
        self.AssertAlive()
        self.PostMessage(win32con.WM_CLOSE, 0, 0)

    def SendMessage(self, message, wparam=None, lparam=None):
        """
        Sends a message to the window.
        For additional help please see the
        `Microsoft KnowledgeBase <https://msdn.microsoft.com/en-us/library/windows/desktop/ms644950(v=vs.85).aspx/>`_
        """
        self.AssertAlive()
        win32gui.SendMessage(self.hwnd, message, wparam, lparam)

    def PostMessage(self, message, wparam=0, lparam=0):
        """
        Posts a message to the window.
        For additional help please see the
        `Microsoft KnowledgeBase <https://msdn.microsoft.com/en-us/library/windows/desktop/ms644944(v=vs.85).aspx/>`_
        """
        self.AssertAlive()
        win32gui.PostMessage(self.hwnd, message, wparam, lparam)

    def GetParent(self):
        """
        Gets the parent window
        :return: A task.WindowInfo object that represents the parent window
        :rtype: task.WindowInfo
        """
        self.AssertAlive()
        parent_hwnd = win32gui.GetParent(self.hwnd)
        if not parent_hwnd:
            raise WindowInfo.NoParent("current window has no parent")
        return WindowInfo(parent_hwnd)

    def Focus(self):
        """
        Makes the window in focus.
        :return: None
        :rtype: None
        """
        self.AssertAlive()
        win32gui.SetFocus(self.hwnd)

    def HasFocus(self):
        """
        Get the current window focus state.
        :return: True if in focus else False
        :rtype: bool
        """
        return self.hwnd == win32gui.GetFocus()

#
# Editor modelines  -  https://www.wireshark.org/tools/modelines.html
#
# Local variables:
# c-basic-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# coding: utf-8
# End:
#
# vi: set shiftwidth=4 tabstop=4 expandtab fileencoding=utf-8:
# :indentSize=4:tabSize=4:noTabs=true:coding=utf-8:
#
