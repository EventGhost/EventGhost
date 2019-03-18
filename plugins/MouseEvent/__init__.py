# -*- coding: utf-8 -*-

version = "1.1.4"

#
# plugins/MouseEvent/__init__.py
#
# Copyright (C) 2012 by Daniel Brugger
#
# Version history (newest on top):
# 1.1.4    Fix NameError when moving the mouse
# 1.1.3    Fix: Not being able to install the plugin in EG 0.5, OK and
#          Apply button grayed out.
#
# 1.1.2    Fix: Changed import to make sure it only imports the pyHook that is
#          included with the plugin.
#          FIX: GrabsHookManager from sys.modules so the override can be done
#          properly to get the back and forward buttons working.
#          Corrects typo in re enabeling the Mouse plugin when this plugin
#          stops and also adds exception catching in the event the Mouse plugin
#          doesn't exist
# 1.1.1    Change the way pyHook/Hookmanager is imported
#          Removed obsolete comment about pyHook installation
# 1.1.0    Added: Horizontal wheel left and right events
#          Added: Wheel up and down events
#          Added: Button 4 and button 5 support (back and forward)
# 1.0.1    Fix: StopMouseEventListener was broken in 1.0.0
#          Fix: After several suspend-resume cycles, the MouseListener stopped
#          producing mouse events.
#          Fix: MouseEventListener instantiation on __start__(), not on
#          __init__()
#          Impr: Code cleanup and maintenance
# 1.0.0    First official release
# 0.1.3    Option "Filter move events by distance" improved. The initial events
#          are now filtered until minDistance reached.
#          On some systems I got ghost events (i.e. events without moving the
#          mouse) after start and I want to suppress them.
# 0.1.2    Fix: Restore event configuration after system resume
#          Impr: new option to filter move events with a distance smaller than
#          a configurable value
# 0.1.1    Fix: trigger move events even if coalesce == False
#          Unnecessary imports removed, URL added
#          Impr: filter ghost move events, i.e. events with same position as
#          previous one
# 0.1.0    Initial version
#
# This file is part of EventGhost.
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

import eg # NOQA


eg.RegisterPlugin(
    name="Mouse Event",
    author="Daniel Brugger, K",
    version=version,
    kind="remote",
    guid="{CBF73261-23E4-452A-8B3C-4EE7DD19930F}",
    createMacrosOnAdd=True,
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=3720",
    description=(
        'Fires mouse events on mouse actions like moves, clicks and wheel.'
    ),
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAMAAABhq6zVAAAAFHRFWHRDcmVhdGlvbiBU"
        "aW1lAAfcAgcKCzhrrOQAAAAHdElNRQfcAgcMHAiviTEmAAAACXBIWXMAAArwAAAK8AFC"
        "rDSYAAADAFBMVEVaGAhrQjFzMRhzOSmEQimUKQiUUjmlKQi9MQi9Wjm9jHu9lITG/8bO"
        "SiHOUinOWjHOY0LOY0rOa0rWUinWUjHWpZTWrZzeOQjehGvelITeta3nUiHne1rnvbXv"
        "xr33OQD3Win3c0r3c1L3hGP3zsb31sb33t7359735+f/Qgj/ShD/WiH/azn/a0L/c0r/"
        "e1L/hFr/hGP/jGP/jGv/1s7/3tb/9+//9/f/////////////////////////////////"
        "////////////////////////////////////////////////////////////////////"
        "////////////////////////////////////////////////////////////////////"
        "////////////////////////////////////////////////////////////////////"
        "////////////////////////////////////////////////////////////////////"
        "////////////////////////////////////////////////////////////////////"
        "////////////////////////////////////////////////////////////////////"
        "////////////////////////////////////////////////////////////////////"
        "////////////////////////////////////////////////////////////////////"
        "////////////////////////////////////////////////////////////////////"
        "////////////////////////////////////////////////////////////////////"
        "////////////////////////////////////////////////////////////////////"
        "//////////////////+fdX+GAAAADXRSTlP///////////////8APegihgAAAHBJREFU"
        "eNpj4FEXU+OBAgYedU4+STM4R0BfgV8OxhEy1NMWlzCDcowNdLTk+VTAHEFjY31tTXkO"
        "UbAeA2NDXXYGRm4Qh19PyUhf2gSih5+XSdlQVwbCYWFWMzHQl4YYIKXOw2OkyMoF5oCs"
        "M2WTBZIAIcwNqtwIphAAAAAASUVORK5CYII="
    )
)

import wx # NOQA
import math # NOQA
import sys # NOQA

from . import pyHook # NOQA
from threading import Lock # NOQA
from eg.cFunctions import SetMouseCallback # NOQA


XBUTTON1 = 0x0001
XBUTTON2 = 0x0002
WM_XBUTTONDOWN = 0x020B
WM_XBUTTONUP = 0x020C
WM_MOUSEHWHEEL = 0x020E

try:
    HookManager = (
        sys.modules['eg.UserPluginModule.MouseEvent.pyHook.HookManager']
    )
except KeyError:
    HookManager = (
        sys.modules['eg.CorePluginModule.MouseEvent.pyHook.HookManager']
    )


class _MouseEvent(HookManager.HookEvent):
    def __init__(self, msg, x, y, data, flags, time, hwnd, window_name):
        HookManager.HookEvent.__init__(self, msg, time, hwnd, window_name)

        self.Position = (x, y)
        self.Data = data
        if data > 0:
            w = 1
        elif data < 0:
            w = -1
        else:
            w = 0
        self.Wheel = w
        self.Injected = flags & 0x01


HookManager.MouseEvent = _MouseEvent


class MouseEvent(eg.PluginBase):
    class Text:
        header = (
            "Hint: Call action 'Start Mouse Event Listener'"
            " in order to start receiving mouse events."
        )
        notStarted = "Plugin is not started, event was ignored"


    @eg.LogIt
    def __init__(self):
        self.AddAction(StartMouseEventListener)
        self.AddAction(StopMouseEventListener)
        self.AddAction(GetLastMouseEvent)
        self.AddAction(GetLastMoveEvent)
        self.AddAction(GetLastLeftClickEvent)
        self.AddAction(GetLastMiddleClickEvent)
        self.AddAction(GetLastRightClickEvent)
        self.AddAction(GetLastBackClickEvent)
        self.AddAction(GetLastForwardClickEvent)
        self.AddAction(GetLastWheelEvent)
        self.AddAction(GetLastHorizontalWheelEvent)
        self.started = False

    @eg.LogIt
    def __start__(self):
        eg.PrintDebugNotice("MouseEvent " + version)
        try:
            SetMouseCallback(None)
        except:
            pass
        self.mouseListener = MouseEventListener(self)
        self.started = True

    @eg.LogItWithReturn
    def __stop__(self):
        self.started = False
        self.mouseListener.Stop()
        del self.mouseListener
        try:
            SetMouseCallback(eg.plugins.Mouse.plugin.MouseCallBack)
        except:
            pass

    def __close__(self):
        pass

    @eg.LogIt
    def __del__(self):
        if self.started:
            self.__stop__()

    @eg.LogIt
    def Configure(self):
        panel = eg.ConfigPanel()
        gridSizer = wx.GridBagSizer(10, 5)
        gridSizer.Add(wx.StaticText(panel, -1, self.Text.header), (0, 0),
            flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
        panel.sizer.Add(gridSizer)

        wx.CallAfter(panel.dialog.buttonRow.okButton.Enable, True)
        while panel.Affirmed():
            panel.SetResult()

    @eg.LogIt
    def OnComputerSuspend(self, _):
        if self.started:
            self.mouseListener.Stop()

    @eg.LogIt
    def OnComputerResume(self, _):
        if self.started:
            self.mouseListener.Restart()


class StartMouseEventListener(eg.ActionBase):
    name = "Start Mouse Event Listener"
    description = "Start listening on mouse events"


    class Text:
        header = "Fire mouse events for"
        allEvents = "All mouse actions"
        mMove = "Mouse move"
        mLeftClick = "Mouse left click"
        mMiddleClick = "Mouse middle click"
        mRightClick = "Mouse right click"
        mBackClick = "Mouse back click"
        mForwardClick = "Mouse forward click"
        mWheel = "Mouse wheel"
        mHorizontalWheel = "Mouse horizontal wheel"
        coalesce1 = "Coalesce move events: Fire not more than"
        coalesce2 = "events per second."
        filter1 = "Filter move events with a distance smaller or equal than"
        filter2 = "pixel."


    @eg.LogIt
    def __call__(self,
        mouseLeftClick=True,
        mouseMiddleClick=True,
        mouseRightClick=True,
        mouseWheel=True,
        mouseMove=True,
        coalesce=True,
        repeatRate=2.0,
        minDistFilter=True,
        minDistance=2,
        mouseBackClick=True,
        mouseForwardClick=True,
        mouseHorizontalWheel=True
    ):
        plugin = self.plugin

        if not plugin.started:
            self.PrintError(plugin.text.notStarted)
            return False

        plugin.mouseListener.Start(
            mouseLeftClick,
            mouseMiddleClick,
            mouseRightClick,
            mouseWheel,
            mouseMove,
            coalesce,
            repeatRate,
            minDistFilter,
            minDistance,
            mouseBackClick,
            mouseForwardClick,
            mouseHorizontalWheel
        )

    @eg.LogIt
    def Configure(self,
        mouseLeftClick=True,
        mouseMiddleClick=True,
        mouseRightClick=True,
        mouseWheel=True,
        mouseMove=True,
        coalesce=True,
        repeatRate=2.0,
        minDistFilter=True,
        minDistance=1,
        mouseBackClick=True,
        mouseForwardClick=True,
        mouseHorizontalWheel=True
    ):
        def onAllEventsCheckBox(evt):
            selected = allEventsCheckBoxCtrl.GetValue()
            mLeftClickCheckBoxCtrl.SetValue(selected)
            mMiddleClickCheckBoxCtrl.SetValue(selected)
            mRightClickCheckBoxCtrl.SetValue(selected)
            mBackClickCheckBoxCtrl.SetValue(selected)
            mForwardClickCheckBoxCtrl.SetValue(selected)
            mWheelCheckBoxCtrl.SetValue(selected)
            mHorizontalWheelCheckBoxCtrl.SetValue(selected)
            mMoveCheckBoxCtrl.SetValue(selected)
            onGuiChange(evt)
            evt.Skip()

        def onGuiChange(evt):
            allEventsCheckBoxCtrl.SetValue(
                mLeftClickCheckBoxCtrl.GetValue()
                and mMiddleClickCheckBoxCtrl.GetValue()
                and mRightClickCheckBoxCtrl.GetValue()
                and mBackClickCheckBoxCtrl.GetValue()
                and mForwardClickCheckBoxCtrl.GetValue()
                and mWheelCheckBoxCtrl.GetValue()
                and mMoveCheckBoxCtrl.GetValue()
                and mHorizontalWheelCheckBoxCtrl.GetValue()
            )
            enable = mMoveCheckBoxCtrl.GetValue()
            coalesceCheckBoxCtrl.Enable(enable)
            repeatRateNumCtrl.Enable(
                enable and
                coalesceCheckBoxCtrl.GetValue()
            )
            minDistCheckBoxCtrl.Enable(enable)
            minDistNumCtrl.Enable(
                enable and
                minDistCheckBoxCtrl.GetValue()
            )
            evt.Skip()

        def onCoalesceCheckBox(evt):
            repeatRateNumCtrl.Enable(coalesceCheckBoxCtrl.GetValue())
            evt.Skip()

        def onMinDistCheckBox(evt):
            minDistNumCtrl.Enable(minDistCheckBoxCtrl.GetValue())
            evt.Skip()

        panel = eg.ConfigPanel(self)
        text = self.Text

        allEventsCheckBoxCtrl = wx.CheckBox(panel, -1, text.allEvents)
        allEventsCheckBoxCtrl.SetValue(
            mouseLeftClick and
            mouseMiddleClick and
            mouseRightClick and
            mouseWheel and
            mouseMove and
            mouseBackClick and
            mouseForwardClick
        )
        allEventsCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onAllEventsCheckBox)

        mLeftClickCheckBoxCtrl = wx.CheckBox(panel, -1, text.mLeftClick)
        mLeftClickCheckBoxCtrl.SetValue(mouseLeftClick)
        mLeftClickCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onGuiChange)

        mMiddleClickCheckBoxCtrl = wx.CheckBox(panel, -1, text.mMiddleClick)
        mMiddleClickCheckBoxCtrl.SetValue(mouseMiddleClick)
        mMiddleClickCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onGuiChange)

        mRightClickCheckBoxCtrl = wx.CheckBox(panel, -1, text.mRightClick)
        mRightClickCheckBoxCtrl.SetValue(mouseRightClick)
        mRightClickCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onGuiChange)

        mBackClickCheckBoxCtrl = wx.CheckBox(panel, -1, text.mBackClick)
        mBackClickCheckBoxCtrl.SetValue(mouseBackClick)
        mBackClickCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onGuiChange)

        mForwardClickCheckBoxCtrl = wx.CheckBox(panel, -1, text.mForwardClick)
        mForwardClickCheckBoxCtrl.SetValue(mouseForwardClick)
        mForwardClickCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onGuiChange)

        mWheelCheckBoxCtrl = wx.CheckBox(panel, -1, text.mWheel)
        mWheelCheckBoxCtrl.SetValue(mouseWheel)
        mWheelCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onGuiChange)

        mHorizontalWheelCheckBoxCtrl = wx.CheckBox(panel, -1, text.mHorizontalWheel)
        mHorizontalWheelCheckBoxCtrl.SetValue(mouseHorizontalWheel)
        mHorizontalWheelCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onGuiChange)

        mMoveCheckBoxCtrl = wx.CheckBox(panel, -1, text.mMove)
        mMoveCheckBoxCtrl.SetValue(mouseMove)
        mMoveCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onGuiChange)

        coalesceCheckBoxCtrl = wx.CheckBox(panel, -1, text.coalesce1)
        coalesceCheckBoxCtrl.SetValue(coalesce)
        coalesceCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onCoalesceCheckBox)
        repeatRateNumCtrl = panel.SpinNumCtrl(
            repeatRate,
            min=0,
            max=999.999,
            fractionWidth=3,
            integerWidth=3
        )

        minDistCheckBoxCtrl = wx.CheckBox(panel, -1, text.filter1)
        minDistCheckBoxCtrl.SetValue(minDistFilter)
        minDistCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onMinDistCheckBox)
        minDistNumCtrl = panel.SpinNumCtrl(
            minDistance,
            min=1,
            max=9999,
            fractionWidth=0,
            integerWidth=4
        )

        gridSizer = wx.GridBagSizer(10, 5)

        rowCount = 0
        gridSizer.Add(
            wx.StaticText(panel, -1, text.header),
            (rowCount, 0),
            flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        rowCount += 1
        gridSizer.Add(
            allEventsCheckBoxCtrl,
            (rowCount, 0),
            flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        rowCount += 1
        gridSizer.Add(
            mLeftClickCheckBoxCtrl,
            (rowCount, 0),
            flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        rowCount += 1
        gridSizer.Add(
            mMiddleClickCheckBoxCtrl,
            (rowCount, 0),
            flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        rowCount += 1
        gridSizer.Add(
            mRightClickCheckBoxCtrl,
            (rowCount, 0),
            flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        rowCount += 1
        gridSizer.Add(
            mBackClickCheckBoxCtrl,
            (rowCount, 0),
            flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        rowCount += 1
        gridSizer.Add(
            mForwardClickCheckBoxCtrl,
            (rowCount, 0),
            flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        rowCount += 1
        gridSizer.Add(
            mWheelCheckBoxCtrl,
            (rowCount, 0),
            flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        rowCount += 1
        gridSizer.Add(
            mHorizontalWheelCheckBoxCtrl,
            (rowCount, 0),
            flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        rowCount += 1
        gridSizer.Add(
            mMoveCheckBoxCtrl,
            (rowCount, 0),
            flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        rowCount += 1
        gridSizer.Add(
            coalesceCheckBoxCtrl,
            (rowCount, 0),
            flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        gridSizer.Add(
            repeatRateNumCtrl,
            (rowCount, 1),
            flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        gridSizer.Add(
            wx.StaticText(panel, -1, text.coalesce2),
            (rowCount, 2),
            flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        rowCount += 1
        gridSizer.Add(
            minDistCheckBoxCtrl,
            (rowCount, 0),
            flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        gridSizer.Add(
            minDistNumCtrl,
            (rowCount, 1),
            flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        gridSizer.Add(
            wx.StaticText(panel, -1, text.filter2),
            (rowCount, 2),
            flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL
        )

        panel.sizer.Add(gridSizer)
        onGuiChange(wx.CommandEvent())

        while panel.Affirmed():
            if repeatRateNumCtrl.GetValue() <= 0.00001:
                repeatRate = 0.0
                coalesce = False
            else:
                repeatRate = repeatRateNumCtrl.GetValue()
                coalesce = coalesceCheckBoxCtrl.GetValue()
            panel.SetResult(
                mLeftClickCheckBoxCtrl.GetValue(),
                mMiddleClickCheckBoxCtrl.GetValue(),
                mRightClickCheckBoxCtrl.GetValue(),
                mWheelCheckBoxCtrl.GetValue(),
                mMoveCheckBoxCtrl.GetValue(),
                coalesce,
                repeatRate,
                minDistCheckBoxCtrl.GetValue(),
                minDistNumCtrl.GetValue(),
                mBackClickCheckBoxCtrl.GetValue(),
                mForwardClickCheckBoxCtrl.GetValue(),
                mHorizontalWheelCheckBoxCtrl.GetValue()
            )


class StopMouseEventListener(eg.ActionBase):
    name = "Stop Mouse Event Listener"
    description = "Stop listening on mouse events"

    @eg.LogIt
    def __call__(self):
        if not self.plugin.started:
            self.PrintError(self.plugin.text.notStarted)
            return False
        self.plugin.mouseListener.Stop()


class GetLastMouseEvent(eg.ActionBase):
    name = "Get last Mouse Event"
    description = (
        "Gets the event details of the last mouse event regardless of it's "
        "type. Provides result in 'eg.result'."
    )

    @eg.LogIt
    def __call__(self):
        if not self.plugin.started:
            self.PrintError(self.plugin.text.notStarted)
            return False
        return self.plugin.mouseListener.GetLastEvent()


class GetLastMoveEvent(eg.ActionBase):
    name = "Get last Mouse Move Event"
    description = (
        "Gets the event details of the last mouse move event. "
        "Provides result in 'eg.result'."
    )

    @eg.LogIt
    def __call__(self):
        if not self.plugin.started:
            self.PrintError(self.plugin.text.notStarted)
            return False
        return self.plugin.mouseListener.GetLastMoveEvent()


class GetLastLeftClickEvent(eg.ActionBase):
    name = "Get last Mouse Left Click Event"
    description = (
        "Gets the event details of the last mouse left click event. "
        "Provides result in 'eg.result'."
    )

    @eg.LogIt
    def __call__(self):
        if not self.plugin.started:
            self.PrintError(self.plugin.text.notStarted)
            return False
        return self.plugin.mouseListener.GetLastLeftClickEvent()


class GetLastMiddleClickEvent(eg.ActionBase):
    name = "Get last Mouse Middle Click Event"
    description = (
        "Gets the event details of the last mouse middle click event. "
        "Provides result in 'eg.result'."
    )

    @eg.LogIt
    def __call__(self):
        if not self.plugin.started:
            self.PrintError(self.plugin.text.notStarted)
            return False
        return self.plugin.mouseListener.GetLastMiddleClickEvent()


class GetLastForwardClickEvent(eg.ActionBase):
    name = "Get last Mouse Forward Click Event"
    description = (
        "Gets the event details of the last mouse forward click event. "
        "Provides result in 'eg.result'."
    )

    @eg.LogIt
    def __call__(self):
        if not self.plugin.started:
            self.PrintError(self.plugin.text.notStarted)
            return False
        return self.plugin.mouseListener.GetLastForwardClickEvent()


class GetLastBackClickEvent(eg.ActionBase):
    name = "Get last Mouse Back Click Event"
    description = (
        "Gets the event details of the last mouse back click event. "
        "Provides result in 'eg.result'."
    )

    @eg.LogIt
    def __call__(self):
        if not self.plugin.started:
            self.PrintError(self.plugin.text.notStarted)
            return False
        return self.plugin.mouseListener.GetLastBackClickEvent()


class GetLastRightClickEvent(eg.ActionBase):
    name = "Get last Mouse Right Click Event"
    description = (
        "Gets the event details of the last mouse right click event. Provides "
        "result in 'eg.result'."
    )

    @eg.LogIt
    def __call__(self):
        if not self.plugin.started:
            self.PrintError(self.plugin.text.notStarted)
            return False
        return self.plugin.mouseListener.GetLastRightClickEvent()


class GetLastWheelEvent(eg.ActionBase):
    name = "Get last Mouse Wheel Event"
    description = (
        "Gets the event details of the last mouse wheel event. Provides "
        "result in 'eg.result'."
    )

    @eg.LogIt
    def __call__(self):
        if not self.plugin.started:
            self.PrintError(self.plugin.text.notStarted)
            return False
        return self.plugin.mouseListener.GetLastWheelEvent()


class GetLastHorizontalWheelEvent(eg.ActionBase):
    name = "Get last Mouse Horizontal Wheel Event"
    description = (
        "Gets the event details of the last mouse horizontal wheel event. "
        "Provides result in 'eg.result'."
    )

    @eg.LogIt
    def __call__(self):
        if not self.plugin.started:
            self.PrintError(self.plugin.text.notStarted)
            return False
        return self.plugin.mouseListener.GetLastHorizontalWheelEvent()


class MouseEventListener(object):
    """Basic listener for all mouse events.
    """

    @eg.LogIt
    def __init__(
        self,
        plugin,
    ):
        self.plugin = plugin
        self.lock = Lock() # thread synchronization

        self.hm = None

        self.lastLeftClickEvent = None
        self.lastMiddleClickEvent = None
        self.lastRightClickEvent = None
        self.lastBackClickEvent = None
        self.lastForwardClickEvent = None
        self.lastHorizontalWheelEvent = None
        self.lastWheelEvent = None
        self.lastEvent = None
        self.lastTriggeredMoveEvent = None
        self.lastMoveEvent = None
        self.firstMoveEvent = None
        self.listenerStarted = False

        self.lastWheelHEvent = None
        self.mouseLeftClick = False
        self.mouseMiddleClick = False
        self.mouseRightClick = False
        self.mouseBackClick = False
        self.mouseForwardClick = False
        self.mouseHorizontalWheel = False
        self.mouseWheel = False
        self.mouseMove = False
        self.coalesce = None
        self.repeatRate = None
        self.minDistFilter = None
        self.minDistance = None
        self.minTimeDiff = None

    def _resetEventData(self):
        self.lastWheelHEvent = None
        self.lastLeftClickEvent = None
        self.lastMiddleClickEvent = None
        self.lastRightClickEvent = None
        self.lastBackClickEvent = None
        self.lastForwardClickEvent = None
        self.lastHorizontalWheelEvent = None
        self.lastWheelEvent = None
        self.lastEvent = None
        self.lastTriggeredMoveEvent = None
        self.lastMoveEvent = None
        self.firstMoveEvent = None

    def __getattr__(self, item):

        if item in self.__dict__:
            return self.__dict__[item]

        if item.startswith('Mouse'):
            def wrapper(evt):
                with self.lock:
                    button = item
                    press = item

                    for word in ('Mouse', 'Left', 'Middle', 'Right'):
                        press = press.replace(word, '')

                    for word in ('Mouse', 'Up', 'Down', 'Double'):
                        button = button.replace(word, '')

                    event = button + '.' + press
                    payload = evt.Position

                    setattr(self, 'last' + button + 'ClickEvent', evt)

                    self.plugin.TriggerEvent(event, payload)
                    self.lastEvent = evt

                    return True

            return wrapper

        raise AttributeError

    @eg.LogIt
    def Start(self,
        mouseLeftClick,
        mouseMiddleClick,
        mouseRightClick,
        mouseWheel,
        mouseMove,
        coalesce,
        repeatRate,
        minDistFilter,
        minDistance,
        mouseBackClick,
        mouseForwardClick,
        mouseHorizontalWheel
    ):
        if self.listenerStarted:
            self.Stop()

        with self.lock:
            self.hm = HookManager.HookManager()
            self._resetEventData()
            self.listenerStarted = True

            self.mouseLeftClick = mouseLeftClick
            self.mouseMiddleClick = mouseMiddleClick
            self.mouseRightClick = mouseRightClick
            self.mouseBackClick = mouseBackClick
            self.mouseForwardClick = mouseForwardClick
            self.mouseWheel = mouseWheel
            self.mouseHorizontalWheel = mouseHorizontalWheel
            self.mouseMove = mouseMove
            self.coalesce = coalesce
            self.repeatRate = repeatRate
            self.minDistFilter = minDistFilter
            self.minTimeDiff = 1000 / repeatRate

            if minDistFilter:
                self.minDistance = minDistance
            else:
                self.minDistance = -1

            if mouseLeftClick:
                self.hm.SubscribeMouseLeftUp(self.MouseLeftUp)
                self.hm.SubscribeMouseLeftDown(self.MouseLeftDown)
                self.hm.SubscribeMouseLeftDbl(self.MouseLeftDouble)

            if mouseMiddleClick:
                self.hm.SubscribeMouseMiddleUp(self.MouseMiddleUp)
                self.hm.SubscribeMouseMiddleDown(self.MouseMiddleDown)
                self.hm.SubscribeMouseMiddleDbl(self.MouseMiddleDouble)

            if mouseRightClick:
                self.hm.SubscribeMouseRightUp(self.MouseRightUp)
                self.hm.SubscribeMouseRightDown(self.MouseRightDown)
                self.hm.SubscribeMouseRightDbl(self.MouseRightDouble)

            if mouseBackClick or mouseForwardClick:
                self.hm.connect(
                    self.hm.mouse_funcs,
                    WM_XBUTTONUP,
                    self.MouseXUp
                )
                self.hm.connect(
                    self.hm.mouse_funcs,
                    WM_XBUTTONDOWN,
                    self.MouseXDown
                )

            if mouseWheel:
                self.hm.SubscribeMouseWheel(self.MouseWheel)
            if mouseMove:
                self.hm.SubscribeMouseMove(self.MouseMove)
            if mouseHorizontalWheel:
                self.hm.connect(
                    self.hm.mouse_funcs,
                    WM_MOUSEHWHEEL,
                    self.MouseHWheel
                )

            wx.CallAfter(self.hm.HookMouse)

    @eg.LogIt
    def Stop(self):
        if self.listenerStarted:
            with self.lock:
                wx.CallAfter(self.hm.UnhookMouse)
                del self.hm
                self.listenerStarted = False

    @eg.LogIt
    def Restart(self):
        if self.listenerStarted:
            self.Start(
                self.mouseLeftClick,
                self.mouseMiddleClick,
                self.mouseRightClick,
                self.mouseWheel,
                self.mouseMove,
                self.coalesce,
                self.repeatRate,
                self.minDistFilter,
                self.minDistance,
                self.mouseBackClick,
                self.mouseForwardClick
            )

    def MouseXUp(self, evt):
        with self.lock:
            xb = evt.Data >> 16
            if xb | XBUTTON1 == xb and self.mouseBackClick:
                self.lastBackClickEvent = evt
                self.plugin.TriggerEvent('Back.Up', evt.Position)
                self.lastEvent = evt

            elif xb | XBUTTON2 == xb and self.mouseForwardClick:
                self.lastForwardClickEvent = evt
                self.plugin.TriggerEvent('Forward.Up', evt.Position)
                self.lastEvent = evt

            return True

    def MouseXDown(self, evt):
        with self.lock:
            xb = evt.Data >> 16
            if xb | XBUTTON1 == xb and self.mouseBackClick:
                self.lastBackClickEvent = evt
                self.plugin.TriggerEvent('Back.Down', evt.Position)
                self.lastEvent = evt

            elif xb | XBUTTON2 == xb and self.mouseForwardClick:
                self.lastForwardClickEvent = evt
                self.plugin.TriggerEvent('Forward.Down', evt.Position)
                self.lastEvent = evt
            return True

    def MouseHWheel(self, evt):
        with self.lock:
            self.lastHorizontalWheelEvent = evt

            if evt.Wheel == -1:
                self.plugin.TriggerEvent('WheelHorizontal.Left', evt.Position)
            else:
                self.plugin.TriggerEvent('WheelHorizontal.Right', evt.Position)

            self.lastEvent = evt
            return True

    def MouseWheel(self, evt):
        with self.lock:
            self.lastWheelEvent = evt

            if evt.Wheel == -1:
                self.plugin.TriggerEvent('Wheel.Down', evt.Position)
            else:
                self.plugin.TriggerEvent('Wheel.Up', evt.Position)

            self.lastEvent = evt
            return True

    def MouseMove(self, evt):
        with self.lock:
            lastTriggeredEvent = self.lastTriggeredMoveEvent
            lastEvent = self.lastMoveEvent
            firstEvent = self.firstMoveEvent

            trigger = False

            # the very first move event
            if lastEvent is None:
                self.firstMoveEvent = evt
                if self.minDistance <= 0: # feature disabled
                    trigger = True

            # following events, still untriggered
            elif lastTriggeredEvent is None:
                # Filter by pixel distance (initial events)
                # The initial events are filtered until minDistance is reached.
                # The reason for that is that on some systems I got ghost
                # events, i.e. events without mouse move

                if self.minDistance > 0:
                    a = abs(evt.Position[0] - firstEvent.Position[0])
                    b = abs(evt.Position[1] - firstEvent.Position[1])
                    c = math.sqrt(a * a + b * b)
                    if c > self.minDistance:
                        trigger = True
                else:
                    trigger = True

            # following events
            else:

                # Filter by pixel distance (following events)
                if self.minDistance > 0:
                    a = abs(evt.Position[0] - lastTriggeredEvent.Position[0])
                    b = abs(evt.Position[1] - lastTriggeredEvent.Position[1])
                    c = math.sqrt(a * a + b * b)
                    if c > self.minDistance:
                        trigger = True

                # Filter by time
                if trigger and self.coalesce:
                    diff = evt.Time - lastTriggeredEvent.Time
                    if diff < self.minTimeDiff:
                        trigger = False

            if trigger:
                self.plugin.TriggerEvent("Move", evt.Position)
                self.lastTriggeredMoveEvent = evt

            self.lastEvent = evt
            self.lastMoveEvent = evt

            return True

    def _printEvent(self, event):
        print 'MessageName:', event.MessageName
        print 'Message:', event.Message
        print 'Time:', event.Time
        print 'Window:', event.Window
        print 'WindowName:', event.WindowName
        print 'Position:', event.Position
        print 'Wheel:', event.Wheel
        print 'Injected:', event.Injected
        print '---'

    def GetLastEvent(self):
        return self._fillEventData(self.lastEvent)

    def GetLastMoveEvent(self):
        return self._fillEventData(self.lastMoveEvent)

    def GetLastLeftClickEvent(self):
        return self._fillEventData(self.lastLeftClickEvent)

    def GetLastMiddleClickEvent(self):
        return self._fillEventData(self.lastMiddleClickEvent)

    def GetLastRightClickEvent(self):
        return self._fillEventData(self.lastRightClickEvent)

    def GetLastBackClickEvent(self):
        return self._fillEventData(self.lastBackClickEvent)

    def GetLastForwardClickEvent(self):
        return self._fillEventData(self.lastForwardClickEvent)

    def GetLastWheelEvent(self):
        return self._fillEventData(self.lastWheelEvent)

    def GetLastHorizontalWheelEvent(self):
        return self._fillEventData(self.lastHorizontalWheelEvent)

    def _fillEventData(self, event):
        with self.lock:
            data = {}
            if event is not None:
                data['MessageName'] = event.MessageName
                data['Message'] = event.Message
                data['Time'] = event.Time
                data['Window'] = event.Window
                data['WindowName'] = event.WindowName
                data['Position'] = event.Position
                data['Wheel'] = event.Wheel
                data['Injected'] = event.Injected

            return data
