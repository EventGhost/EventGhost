# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
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

import wx
from math import cos, pi, radians, sin
from Queue import Queue
from sys import maxint
from threading import Thread
from time import clock, sleep
from win32api import EnumDisplayMonitors, GetSystemMetrics, mouse_event as mouse_event2
from win32con import MOUSEEVENTF_ABSOLUTE, MOUSEEVENTF_MOVE

# Local imports
import eg
from eg import HasActiveHandler
from eg.cFunctions import SetMouseCallback
from eg.WinApi.Dynamic import GetCursorPos, mouse_event, POINT, SetCursorPos
from eg.WinApi.Utils import GetMonitorDimensions

ICON = """iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeT
AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1QQIDRgEM71mAAAAADV0RVh0Q29tbWVudAAoYy
kgMjAwNCBKYWt1YiBTdGVpbmVyCgpDcmVhdGVkIHdpdGggVGhlIEdJTVCQ2YtvAAACHElEQVQ4y42Q
zUtUURjGf/fcyatz73Wiklwo2R/QplXQ/AURlLYJcrJNQrvQahYFI0wQ7lu0azNtYlAj2rUJRFciUf
kRgUwOM6Y5jePXfNzznhZ+NOpIvpvD+5zn/M7DY3Fo0ul0JzBQLpdvG2M8wHi++6r7Zs+Tet/Yu9Hr
W5tb/Yqjc2m7vB3zfPd7LBbzPd/tK/5Zu5ZKpZZSb1LZ0bGRG7u+F2E3PG0dfp1MJl+2tvq9xeLaJv
AxkUj01aW7UKtV3xvYam525nq6b92znieHEkqpIWwLpRSV7YBoNEoun2VhIUOTY6ODAAmkqJT68PRZ
orf+w1AoFBq63//A2LZthcNhhoeH0VrjNLVgYTHw8DGlUonC6u/IyEj6DnAAoAAq1ar1c3FxX8zlcl
QqlX97Po/XGrEa9MWREuPxOPl8nmw2Szwe538Tql9WVlZoa2tjcHDwgHZiwGqhwGqhgO/7dHZ0MDM7
e7IEG6V1zp05uy/WghrLv5YPaBul9eMBnufuRLXAwsIYQYsgRhCt0SK0n2/nuBKnxBi00YhotA7Qoh
ERRAsiBiOy559qBJjVWmMrmyAQtNboYBcmgojQdMrZ8083Anyan5/D8zxaWpqxlEKLoPVOfNd1iZyO
MDPzDeBHow7efv3yuc9xnGhX10U8z8MAGMPOYchkFlhaygG8bgSoVavVu5MT448mJ8YvA1cadJUBrg
Jrhy/+AqGrAMOnH86mAAAAAElFTkSuQmCC"""

eg.RegisterPlugin(
    name = "Mouse",
    author = (
        "Bitmonster",
        "Sem;colon",
    ),
    version = "1.1.1",
    description = (
        "Actions to control the mouse cursor and emulation of mouse events."
    ),
    kind = "core",
    guid = "{6B1751BF-F94E-4260-AB7E-64C0693FD959}",
    icon = ICON,
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=5481",
)

class Mouse(eg.PluginBase):
    def __init__(self):
        self.AddEvents()
        self.AddAction(LeftButton)
        self.AddAction(LeftDoubleClick)
        self.AddAction(ToggleLeftButton)
        self.AddAction(MiddleButton)
        self.AddAction(MoveAbsolute)
        self.AddAction(MoveRelative)
        self.AddAction(RightButton)
        self.AddAction(RightDoubleClick)
        self.AddAction(GoDirection)
        self.AddAction(MouseWheel)

    @eg.LogIt
    def __close__(self):
        pass

    def __start__(self):
        self.thread = MouseThread()
        self.leftMouseButtonDown = False
        self.lastMouseEvent = None
        self.mouseButtonWasBlocked = [False, False, False, False, False]
        SetMouseCallback(self.MouseCallBack)

    @eg.LogIt
    def __stop__(self):
        SetMouseCallback(None)
        self.thread.receiveQueue.put([-1])

    def MouseCallBack(self, buttonName, buttonNum, param):
        if param:
            if self.lastMouseEvent:
                self.lastMouseEvent.SetShouldEnd()
            shouldBlock = HasActiveHandler("Mouse." + buttonName)
            self.mouseButtonWasBlocked[buttonNum] = shouldBlock
            self.lastMouseEvent = self.TriggerEnduringEvent(buttonName)
            return shouldBlock
        else:
            if self.lastMouseEvent:
                self.lastMouseEvent.SetShouldEnd()
            return self.mouseButtonWasBlocked[buttonNum]
        return False


class MouseThread(Thread):
    currentAngle = 0
    newAngle = 0
    acceleration = 0
    speed = 0
    maxTicks = 5
    yRemainder = 0
    xRemainder = 0
    leftButtonDown = False
    lastTime = 0
    initSpeed = 0.06
    maxSpeed = 7.0
    useAlternateMethod = False

    def __init__(self):
        Thread.__init__(self, name="MouseThread")
        self.receiveQueue = Queue(2048)
        self.start()

    @eg.LogItWithReturn
    def run(self):
        stop = False
        point = POINT()
        while True:
            self.lastTime = clock()
            if not self.receiveQueue.empty():
                data = self.receiveQueue.get()
                if data[0] == -1:
                    break
                elif data[0] == -2:
                    stop = True
                else:
                    self.newAngle = radians(data[0])
                    self.initSpeed = data[1]
                    self.maxSpeed = data[2]
                    self.acceleration = data[3]
                    self.useAlternateMethod = data[4]

            if stop:
                self.acceleration = 0
                self.speed = 0
                stop = False
                continue

            if self.acceleration == 0:
                sleep(0.05)
                continue

            ticks = 10
            if self.speed == 0:
                self.currentAngle = self.newAngle
                self.speed = self.initSpeed
            else:
                diff = self.newAngle - self.currentAngle
                if diff > pi:
                    diff = diff - 2 * pi
                elif diff < -1 * pi:
                    diff = diff + 2 * pi
                self.currentAngle = self.currentAngle + (diff / 20)

            self.speed = self.speed + (self.speed * self.acceleration * ticks)
            if self.speed > self.maxSpeed:
                self.speed = self.maxSpeed
            elif self.speed <= 0:
                self.speed = 0

            factor = self.speed * (ticks / 10)
            xCurrent = sin(self.currentAngle) * factor + self.xRemainder
            yCurrent = -1 * cos(self.currentAngle) * factor + self.yRemainder

            x = int(xCurrent)
            y = int(yCurrent)

            self.xRemainder = xCurrent - x
            self.yRemainder = yCurrent - y
            try:
                if self.useAlternateMethod:
                    mouse_event2(MOUSEEVENTF_MOVE, x, y)
                else:
                    GetCursorPos(point)
                    SetCursorPos(point.x + x, point.y + y)
            except:
                pass
            if self.speed == 0:
                self.acceleration = 0
            waitTicks = 0.01 - (clock() - self.lastTime)
            if waitTicks < 0:
                waitTicks = 0.0
            sleep(waitTicks)


class GoDirection(eg.ActionBase):
    name = "Start Movement"
    description = "Starts cursor movement in the specified direction."

    class text:
        label = u"Start cursor movement in direction %.2f\u00B0"
        text1 = "Start moving cursor in direction"
        text2 = "degrees. (0-360)"
        text3 = "Initial mouse speed:"
        text4 = "Maximum mouse speed:"
        text5 = "Acceleration factor:"
        label_AM = "Use alternate method"

    def __call__(self, direction=0, initSpeed = 60, maxSpeed = 7000, accelerationFactor = 3, useAlternateMethod=False):
        def UpFunc():
            self.plugin.thread.receiveQueue.put([-2])
        self.plugin.thread.receiveQueue.put([float(direction), float(initSpeed) / 1000, float(maxSpeed) / 1000, float(accelerationFactor) / 1000, useAlternateMethod])
        eg.event.AddUpFunc(UpFunc)

    def Configure(self, direction=0, initSpeed = 60, maxSpeed = 7000, accelerationFactor = 3, useAlternateMethod=False):
        text = self.text
        panel = eg.ConfigPanel()
        direction = float(direction)
        valueCtrl = panel.SpinNumCtrl(float(direction), min=0, max=360)
        panel.AddLine(text.text1, valueCtrl, text.text2)

        initSpeedLabel = wx.StaticText(panel, -1, text.text3)
        initSpeedSpin = eg.SpinIntCtrl(panel, -1, initSpeed, 10, 2000)
        maxSpeedLabel = wx.StaticText(panel, -1, text.text4)
        maxSpeedSpin = eg.SpinIntCtrl(panel, -1, maxSpeed, 4000, 32000)
        accelerationFactorLabel = wx.StaticText(panel, -1, text.text5)
        accelerationFactorSpin = eg.SpinIntCtrl(panel, -1, accelerationFactor, 1, 200)
        eg.EqualizeWidths((initSpeedLabel, maxSpeedLabel, accelerationFactorLabel))
        panel.AddLine(initSpeedLabel, initSpeedSpin)
        panel.AddLine(maxSpeedLabel, maxSpeedSpin)
        panel.AddLine(accelerationFactorLabel, accelerationFactorSpin)

        uAMCB = panel.CheckBox(useAlternateMethod, text.label_AM)
        panel.AddLine(uAMCB)

        while panel.Affirmed():
            panel.SetResult(
                valueCtrl.GetValue(),
                initSpeedSpin.GetValue(),
                maxSpeedSpin.GetValue(),
                accelerationFactorSpin.GetValue(),
                uAMCB.GetValue(),
            )

    def GetLabel(self, direction=0, initSpeed = 60, maxSpeed = 7000, accelerationFactor = 3, useAlternateMethod=False):
        direction = float(direction)
        return self.text.label % direction


class LeftButton(eg.ActionBase):
    name = "Left Mouse Click"
    description = "Clicks the left mouse button."

    def __call__(self):
        def UpFunc():
            mouse_event(0x0004, 0, 0, 0, 0)
            self.plugin.leftMouseButtonDown = False
        mouse_event(0x0002, 0, 0, 0, 0)
        self.plugin.leftMouseButtonDown = True
        eg.event.AddUpFunc(UpFunc)


class LeftDoubleClick(eg.ActionBase):
    name = "Left Mouse Double-Click"
    description = "Double-clicks the left mouse button."

    def __call__(self):
        def UpFunc():
            mouse_event(0x0004, 0, 0, 0, 0)
        self.plugin.leftMouseButtonDown = False
        mouse_event(0x0002, 0, 0, 0, 0)
        mouse_event(0x0004, 0, 0, 0, 0)
        mouse_event(0x0002, 0, 0, 0, 0)
        eg.event.AddUpFunc(UpFunc)


class MiddleButton(eg.ActionBase):
    name = "Middle Mouse Click"
    description = "Clicks the middle mouse button."

    def __call__(self):
        def UpFunc():
            mouse_event(0x0040, 0, 0, 0, 0)
        mouse_event(0x0020, 0, 0, 0, 0)
        eg.event.AddUpFunc(UpFunc)


class MouseWheel(eg.ActionBase):
    name = "Turn Mouse Wheel"
    description = "Turns the mouse wheel."

    class text:
        label = u"Turn mouse wheel %d clicks"
        text1 = "Turn mouse wheel by"
        text2 = "clicks. (Negative values turn down)"

    def __call__(self, direction=0):
        mouse_event(0x0800, 0, 0, direction * 120, 0)

    def Configure(self, direction=0):
        panel = eg.ConfigPanel()
        valueCtrl = panel.SpinIntCtrl(direction, min=-100, max=100)
        panel.AddLine(self.text.text1, valueCtrl, self.text.text2)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())

    def GetLabel(self, direction=0):
        return self.text.label % direction


class MoveAbsolute(eg.ActionBase):
    name = "Move Absolute"
    description = "Moves the cursor to an absolute position."

    class text:
        display = "Move cursor to"
        label_M = "Monitor: %i,  "
        label_X = "x: %i,  "
        label_Y = "y: %i"
        label_C = "Set position to screen center"
        label_AM = "Use alternate method"
        center = "center"
        text1 = "Set horizontal position X to"
        text2 = "pixels"
        text3 = "Set vertical position Y to"
        note = (
            "Note: The coordinates X and Y are related to the monitor "
            '(not to the "virtual screen")'
        )

    def __call__(self, x = None, y = None, displayNumber = None, center = False, useAlternateMethod=False):
        point = POINT()
        GetCursorPos(point)
        X = point.x
        Y = point.y
        mons = EnumDisplayMonitors(None, None)
        mons = [item[2] for item in mons]
        for mon in range(len(mons)):  # on what monitor (= mon) is the cursor?
            m = mons[mon]
            if m[0] <= X and X <= m[2] and m[1] <= Y and Y <= m[3]:
                break
        if displayNumber is None:
            displayNumber = mon

        monitorDimensions = GetMonitorDimensions()
        try:
            displayRect = monitorDimensions[displayNumber]
        except IndexError:
            displayNumber = 0
            displayRect = monitorDimensions[displayNumber]
        if center:
            x = displayRect[2] / 2
            y = displayRect[3] / 2

        if x is None:
            x = X - mons[displayNumber][0]
        if y is None:
            y = Y - mons[displayNumber][1]

        x += displayRect[0]
        y += displayRect[1]
        if useAlternateMethod:
            x = x * 65535 / GetSystemMetrics(0)
            y = y * 65535 / GetSystemMetrics(1)
            mouse_event2(MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_MOVE, x, y)
        else:
            SetCursorPos(x, y)

    def Configure(self, x = None, y = None, displayNumber = None, center = False, useAlternateMethod=False):
        panel = eg.ConfigPanel()
        text = self.text

        uAMCB = panel.CheckBox(useAlternateMethod, text.label_AM)
        cCB = panel.CheckBox(center, text.label_C)
        xCB = panel.CheckBox(x is not None, text.text1)
        yCB = panel.CheckBox(y is not None, text.text3)
        displayCB = panel.CheckBox(displayNumber is not None, text.display)

        #xCtrl = panel.SpinIntCtrl(x or 0, min = -maxint - 1, max = maxint)
        xCtrl = panel.SpinIntCtrl(x or 0, min = 0, max = maxint)  # since 1.0.1
        xCtrl.Enable(x is not None)

        #yCtrl = panel.SpinIntCtrl(y or 0, min = -maxint - 1, max = maxint)
        yCtrl = panel.SpinIntCtrl(y or 0, min = 0, max = maxint)  # since 1.0.1
        yCtrl.Enable(y is not None)

        display = -1 if displayNumber is None else displayNumber
        displayChoice = eg.DisplayChoice(panel, display)
        displayChoice.Enable(displayNumber is not None)

        xPixels = wx.StaticText(panel, -1, text.text2)
        yPixels = wx.StaticText(panel, -1, text.text2)
        monsCtrl = eg.MonitorsCtrl(panel, background = (224, 238, 238))
        note = wx.StaticText(panel, -1, text.note)
        note.SetForegroundColour(wx.RED)
        sizer = wx.GridBagSizer(vgap = 6, hgap = 5)
        sizer.Add(cCB, (0, 0), (1, 3), flag = wx.BOTTOM, border = 8)
        sizer.Add(xCB, (1, 0), (1, 1))
        sizer.Add(xCtrl, (1, 1), (1, 1))
        sizer.Add(xPixels, (1, 2), (1, 1))
        sizer.Add(yCB, (2, 0), (1, 1))
        sizer.Add(yCtrl, (2, 1), (1, 1))
        sizer.Add(yPixels, (2, 2), (1, 1))
        sizer.Add(note, (3, 0), (1, 3))
        sizer.Add(displayCB, (4, 0), (1, 1), flag = wx.TOP, border = 14)
        sizer.Add(displayChoice, (4, 1), (1, 2), flag = wx.TOP, border = 13)
        sizer.Add(uAMCB, (5, 0), (1, 3))
        panel.sizer.Add(sizer, 1, wx.EXPAND)
        panel.sizer.Add(monsCtrl, 0, wx.TOP, 8)

        def HandleCenterCheckBox(event = None):
            val = not cCB.GetValue()
            xCB.Enable(val)
            xCtrl.Enable(val)
            xPixels.Enable(val)
            yCB.Enable(val)
            yCtrl.Enable(val)
            yPixels.Enable(val)
            if not val:
                xCB.SetValue(False)
                yCB.SetValue(False)
                xCtrl.SetValue(0)
                yCtrl.SetValue(0)
            if event:
                event.Skip()
        cCB.Bind(wx.EVT_CHECKBOX, HandleCenterCheckBox)
        HandleCenterCheckBox()

        def HandleXCheckBox(event):
            xCtrl.Enable(event.IsChecked())
            event.Skip()
        xCB.Bind(wx.EVT_CHECKBOX, HandleXCheckBox)

        def HandleYCheckBox(event):
            yCtrl.Enable(event.IsChecked())
            event.Skip()
        yCB.Bind(wx.EVT_CHECKBOX, HandleYCheckBox)

        def HandleDisplayCB(event):
            flag = event.IsChecked()
            displayChoice.Enable(flag)
            if flag:
                display = 0 if displayNumber is None else displayNumber
            else:
                display = -1
            displayChoice.SetValue(display)
            event.Skip()
        displayCB.Bind(wx.EVT_CHECKBOX, HandleDisplayCB)

        while panel.Affirmed():
            if xCtrl.IsEnabled():
                x = xCtrl.GetValue()
            else:
                x = None

            if yCtrl.IsEnabled():
                y = yCtrl.GetValue()
            else:
                y = None

            if displayChoice.IsEnabled():
                displayNumber = displayChoice.GetValue()
            else:
                displayNumber = None

            panel.SetResult(x, y, displayNumber, cCB.GetValue(), uAMCB.GetValue())

    def GetLabel(self, x, y, displayNumber, center, useAlternateMethod=False):
        if center:
            res = self.text.display + " " + self.text.center
            if displayNumber is not None:
                res += ": %s" % (self.text.label_M % (displayNumber + 1))
            return res
        else:
            return self.text.display + ":  %s%s%s" % (
                self.text.label_M % (displayNumber + 1) if displayNumber is not None else "",
                self.text.label_X % x if x is not None else "",
                self.text.label_Y % y if y is not None else "",
            )


class MoveRelative(eg.ActionBase):
    name = "Move Relative"
    description = "Moves the cursor to a relative position."

    class text:
        label = "Change cursor position by x:%s, y:%s"
        text1 = "Change horizontal position X by"
        text2 = "pixels"
        text3 = "Change vertical position Y by"
        label_AM = "Use alternate method"

    def __call__(self, x, y, useAlternateMethod=False):
        if x is None:
            x = 0
        if y is None:
            y = 0
        if useAlternateMethod:
            mouse_event2(MOUSEEVENTF_MOVE, x, y)
        else:
            point = POINT()
            GetCursorPos(point)
            SetCursorPos(point.x + x, point.y + y)

    def Configure(self, x=0, y=0, useAlternateMethod=False):
        panel = eg.ConfigPanel()
        text = self.text

        uAMCB = panel.CheckBox(useAlternateMethod, text.label_AM)

        xCB = panel.CheckBox(x is not None, text.text1)

        def HandleXCheckBox(event):
            xCtrl.Enable(event.IsChecked())
            event.Skip()
        xCB.Bind(wx.EVT_CHECKBOX, HandleXCheckBox)

        xCtrl = panel.SpinIntCtrl(x or 0, min=-maxint - 1, max=maxint)
        xCtrl.Enable(x is not None)

        yCB = panel.CheckBox(y is not None, text.text3)

        def HandleYCheckBox(event):
            yCtrl.Enable(event.IsChecked())
            event.Skip()
        yCB.Bind(wx.EVT_CHECKBOX, HandleYCheckBox)

        yCtrl = panel.SpinIntCtrl(y or 0, min=-maxint - 1, max=maxint)
        yCtrl.Enable(y is not None)

        panel.AddLine(xCB, xCtrl, text.text2)
        panel.AddLine(yCB, yCtrl, text.text2)
        panel.AddLine(uAMCB)

        while panel.Affirmed():
            if xCtrl.IsEnabled():
                x = xCtrl.GetValue()
            else:
                x = None

            if yCtrl.IsEnabled():
                y = yCtrl.GetValue()
            else:
                y = None
            panel.SetResult(x, y, uAMCB.GetValue())

    def GetLabel(self, x, y, useAlternateMethod=False):
        return self.text.label % (str(x), str(y))


class RightButton(eg.ActionBase):
    name = "Right Mouse Click"
    description = "Clicks the right mouse button."

    def __call__(self):
        def UpFunc():
            mouse_event(0x0010, 0, 0, 0, 0)
        mouse_event(0x0008, 0, 0, 0, 0)
        eg.event.AddUpFunc(UpFunc)


class RightDoubleClick(eg.ActionBase):
    name = "Right Mouse Double-Click"
    description = "Double-clicks the right mouse button."

    def __call__(self):
        def UpFunc():
            mouse_event(0x0010, 0, 0, 0, 0)
        mouse_event(0x0008, 0, 0, 0, 0)
        mouse_event(0x0010, 0, 0, 0, 0)
        mouse_event(0x0008, 0, 0, 0, 0)
        eg.event.AddUpFunc(UpFunc)


class ToggleLeftButton(eg.ActionBase):
    class text:
        name = "Left Mouse Toggle"
        description = "Changes the status of the left mouse button."
        radioBoxLabel = "Option"
        radioBoxOptions = [
            "Toggle left mouse button",
            "Set left mouse button \"Up\"",
            "Set left mouse button \"Down\""
        ]

    def __call__(self, data=0):
        if self.plugin.leftMouseButtonDown and data == 0 or data == 1:
            mouse_event(0x0004, 0, 0, 0, 0)
            self.plugin.leftMouseButtonDown = False
        else:
            mouse_event(0x0002, 0, 0, 0, 0)
            self.plugin.leftMouseButtonDown = True

    def GetLabel(self, data=0):
        return self.plugin.label + ': ' + self.text.radioBoxOptions[data]

    def Configure(self, data=0):
        panel = eg.ConfigPanel()
        radioBox = wx.RadioBox(
            panel,
            label=self.text.radioBoxLabel,
            choices=self.text.radioBoxOptions,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(data)
        panel.sizer.Add(radioBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(radioBox.GetSelection())
