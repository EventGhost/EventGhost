# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
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
    author = "Bitmonster",
    version = "1.0.1",
    description = (
        "Gives you actions to control the mouse pointer and emulation of "
        "mouse events."
    ),
    kind = "core",
    guid = "{6B1751BF-F94E-4260-AB7E-64C0693FD959}",
    icon = ICON,
)

import wx
from sys import maxint
from Queue import Queue
from threading import Thread
from math import sin, cos, radians, pi
from time import sleep, clock
from eg import HasActiveHandler
from eg.cFunctions import SetMouseCallback
from win32api import EnumDisplayMonitors
from eg.WinApi.Dynamic import mouse_event, GetCursorPos, SetCursorPos, POINT
from eg.WinApi.Utils import GetMonitorDimensions
#===============================================================================

# this is the real worker thread
class MouseThread(Thread):
    currentAngle = 0
    newAngle = 0
    acceleration = 0
    speed = 0
    maxSpeed = 7
    accelerationFactor = 0.003
    accelerationStopFactor = 0.1
    maxTicks = 5
    iniSpeed = 0.06
    yRemainder = 0
    xRemainder = 0
    leftButtonDown = False
    lastTime = 0

    def __init__(self):
        Thread.__init__(self, name="MouseThread")
        self.receiveQueue = Queue(2048)
        self.start()


    @eg.LogItWithReturn
    def run(self):
        upTime = 0
        point = POINT()
        while True:
            self.lastTime = clock()
            if not self.receiveQueue.empty():
                data = self.receiveQueue.get()
                if data == -1:
                    break
                elif data == -2:
                    upTime = clock()
                else:
                    self.newAngle = radians(data)
                    self.acceleration = self.accelerationFactor
                    upTime = 0

            if upTime != 0 and clock() - upTime > 0.05:
                self.acceleration = 0
                self.speed = 0


            if self.acceleration == 0:
                sleep(0.05)
                continue

            ticks = 10
            if self.speed == 0:
                self.currentAngle = self.newAngle
                self.speed = self.iniSpeed
                #self.speed = 0.06
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
            xCurrent =  sin(self.currentAngle) * factor + self.xRemainder
            yCurrent = -1 * cos(self.currentAngle) * factor + self.yRemainder

            x = int(xCurrent)
            y = int(yCurrent)

            self.xRemainder = xCurrent - x
            self.yRemainder = yCurrent - y
            try:
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
#===============================================================================

class Mouse(eg.PluginBase):

    def __init__(self):
        self.AddEvents()

        self.AddAction(GoDirection)
        self.AddAction(LeftButton)
        self.AddAction(MiddleButton)
        self.AddAction(RightButton)
        self.AddAction(LeftDoubleClick)
        self.AddAction(RightDoubleClick)
        self.AddAction(ToggleLeftButton)
        self.AddAction(MoveAbsolute)
        self.AddAction(MoveRelative)
        self.AddAction(MouseWheel)


    def __start__(self):
        self.thread = MouseThread()
        self.leftMouseButtonDown = False
        self.lastMouseEvent = None
        self.mouseButtonWasBlocked = [False, False, False, False, False]
        SetMouseCallback(self.MouseCallBack)


    @eg.LogIt
    def __stop__(self):
        SetMouseCallback(None)
        self.thread.receiveQueue.put(-1)


    @eg.LogIt
    def __close__(self):
        pass


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
#===============================================================================

class GoDirection(eg.ActionBase):
    name = "Start mouse movement in a direction"
    class text:
        label = u"Start mouse movement in direction %.2f\u00B0"
        text1 = "Start moving mouse pointer in direction"
        text2 = "degrees. (0-360)"

    def __call__(self, direction=0):
        def UpFunc():
            self.plugin.thread.receiveQueue.put(-2)
        self.plugin.thread.receiveQueue.put(float(direction))
        eg.event.AddUpFunc(UpFunc)


    def GetLabel(self, direction=0):
        direction = float(direction)
        return self.text.label % direction


    def Configure(self, direction=0):
        panel = eg.ConfigPanel()
        direction = float(direction)
        valueCtrl = panel.SpinNumCtrl(float(direction), min=0, max=360)
        panel.AddLine(self.text.text1, valueCtrl, self.text.text2)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())
#===============================================================================

class LeftButton(eg.ActionBase):
    name = "Left mouse button"

    def __call__(self):
        def UpFunc():
            mouse_event(0x0004, 0, 0, 0, 0)
            self.plugin.leftMouseButtonDown = False
        mouse_event(0x0002, 0, 0, 0, 0)
        self.plugin.leftMouseButtonDown = True
        eg.event.AddUpFunc(UpFunc)
#===============================================================================

class MiddleButton(eg.ActionBase):
    name = "Middle mouse button"

    def __call__(self):
        def UpFunc():
            mouse_event(0x0040, 0, 0, 0, 0)
        mouse_event(0x0020, 0, 0, 0, 0)
        eg.event.AddUpFunc(UpFunc)
#===============================================================================

class RightButton(eg.ActionBase):
    name = "Right mouse button"

    def __call__(self):
        def UpFunc():
            mouse_event(0x0010, 0, 0, 0, 0)
        mouse_event(0x0008, 0, 0, 0, 0)
        eg.event.AddUpFunc(UpFunc)
#===============================================================================

class LeftDoubleClick(eg.ActionBase):
    name = "Left mouse button double-click"

    def __call__(self):
        def UpFunc():
            mouse_event(0x0004, 0, 0, 0, 0)
        self.plugin.leftMouseButtonDown = False
        mouse_event(0x0002, 0, 0, 0, 0)
        mouse_event(0x0004, 0, 0, 0, 0)
        mouse_event(0x0002, 0, 0, 0, 0)
        eg.event.AddUpFunc(UpFunc)
#===============================================================================

class RightDoubleClick(eg.ActionBase):
    name = "Right mouse button double-click"

    def __call__(self):
        def UpFunc():
            mouse_event(0x0010, 0, 0, 0, 0)
        mouse_event(0x0008, 0, 0, 0, 0)
        mouse_event(0x0010, 0, 0, 0, 0)
        mouse_event(0x0008, 0, 0, 0, 0)
        eg.event.AddUpFunc(UpFunc)
#===============================================================================

class ToggleLeftButton(eg.ActionBase):
    name = "Toggle left mouse button"

    def __call__(self):
        if self.plugin.leftMouseButtonDown:
            mouse_event(0x0004, 0, 0, 0, 0)
            self.plugin.leftMouseButtonDown = False
        else:
            mouse_event(0x0002, 0, 0, 0, 0)
            self.plugin.leftMouseButtonDown = True
#===============================================================================

class MoveAbsolute(eg.ActionBase):
    name = "Move Absolute"
    class text:
        display = "Move the mouse pointer to"
        label_M = "Monitor: %i,  "
        label_X = "x: %i,  "
        label_Y = "y: %i"
        text1 = "Set horizontal position X to"
        text2 = "pixels"
        text3 = "Set vertical position Y to"
        note = 'Note: The coordinates X and Y are related to the monitor \
(not to the "virtual screen")'

    def __call__(self, x = None, y = None, displayNumber = None):
        point = POINT()
        GetCursorPos(point)
        X = point.x
        Y = point.y
        mons = EnumDisplayMonitors(None, None)
        mons = [item[2] for item in mons]
        for mon in range(len(mons)): # on what monitor (= mon) is the pointer ?
            m = mons[mon]
            if m[0] <= X and X <= m[2] and m[1] <= Y and Y <= m[3]:
                break
        if displayNumber is None:
            displayNumber = mon
        monitorDimensions = GetMonitorDimensions()
        try:
            displayRect = monitorDimensions[displayNumber]
        except IndexError:
            displayRect = monitorDimensions[0]

        if x is None:
            x = X - m[0]
        if y is None:
            y = Y - m[1]

        x += displayRect[0]
        y += displayRect[1]
        SetCursorPos(x, y)


    def GetLabel(self, x, y, displayNumber):
        return self.text.display + ":  %s%s%s" % (
            self.text.label_M % (displayNumber+1) if displayNumber is not None else "",
            self.text.label_X % x if x is not None else "",
            self.text.label_Y % y if y is not None else "",
        )        


    def Configure(self, x = None, y = None, displayNumber = None):
        panel = eg.ConfigPanel()
        text = self.text

        xCB = panel.CheckBox(x is not None, text.text1)
        yCB = panel.CheckBox(y is not None, text.text3)
        displayCB = panel.CheckBox(displayNumber is not None, text.display)

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


        #xCtrl = panel.SpinIntCtrl(x or 0, min = -maxint - 1, max = maxint)
        xCtrl = panel.SpinIntCtrl(x or 0, min = 0, max = maxint) # since 1.0.1
        xCtrl.Enable(x is not None)

        #yCtrl = panel.SpinIntCtrl(y or 0, min = -maxint - 1, max = maxint)
        yCtrl = panel.SpinIntCtrl(y or 0, min = 0, max = maxint) # since 1.0.1
        yCtrl.Enable(y is not None)

        display = -1 if displayNumber is None else displayNumber
        displayChoice = eg.DisplayChoice(panel, display)
        displayChoice.Enable(displayNumber is not None)


        monsCtrl = eg.MonitorsCtrl(panel, background = (224, 238, 238))
        note = wx.StaticText(panel, -1, text.note)
        note.SetForegroundColour(wx.RED)
        sizer = wx.GridBagSizer(vgap = 6, hgap = 5)
        sizer.Add(xCB, (0, 0), (1, 1))
        sizer.Add(xCtrl, (0, 1), (1, 1))
        sizer.Add(wx.StaticText(panel,- 1, text.text2), (0, 2), (1, 1))
        sizer.Add(yCB, (1, 0), (1, 1))
        sizer.Add(yCtrl, (1, 1), (1, 1))
        sizer.Add(wx.StaticText(panel, -1, text.text2), (1, 2), (1, 1))
        sizer.Add(note, (2, 0), (1, 3))
        sizer.Add(displayCB, (3, 0), (1, 1), flag = wx.TOP, border = 14)
        sizer.Add(displayChoice, (3, 1), (1, 2), flag = wx.TOP, border = 13)
        panel.sizer.Add(sizer, 1, wx.EXPAND)
        panel.sizer.Add(monsCtrl)

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

            panel.SetResult(x, y, displayNumber,)
#===============================================================================

class MoveRelative(eg.ActionBase):
    name = "Move Relative"
    class text:
        label = "Change Mouse position by x:%s, y:%s"
        text1 = "Change horizontal position X by"
        text2 = "pixels"
        text3 = "Change vertical position Y by"

    def __call__(self, x, y):
        point = POINT()
        GetCursorPos(point)
        if x is None:
            x = 0
        if y is None:
            y = 0
        SetCursorPos(point.x + x, point.y + y)


    def GetLabel(self, x, y):
        return self.text.label % (str(x), str(y))


    def Configure(self, x=0, y=0):
        panel = eg.ConfigPanel()
        text = self.text

        xCB = panel.CheckBox(x is not None, text.text1)
        def HandleXCheckBox(event):
            xCtrl.Enable(event.IsChecked())
            event.Skip()
        xCB.Bind(wx.EVT_CHECKBOX, HandleXCheckBox)

        xCtrl = panel.SpinIntCtrl(x or 0, min=-maxint-1, max=maxint)
        xCtrl.Enable(x is not None)

        yCB = panel.CheckBox(y is not None, text.text3)
        def HandleYCheckBox(event):
            yCtrl.Enable(event.IsChecked())
            event.Skip()
        yCB.Bind(wx.EVT_CHECKBOX, HandleYCheckBox)

        yCtrl = panel.SpinIntCtrl(y or 0, min=-maxint-1, max=maxint)
        yCtrl.Enable(y is not None)

        panel.AddLine(xCB, xCtrl, text.text2)
        panel.AddLine(yCB, yCtrl, text.text2)

        while panel.Affirmed():
            if xCtrl.IsEnabled():
                x = xCtrl.GetValue()
            else:
                x = None

            if yCtrl.IsEnabled():
                y = yCtrl.GetValue()
            else:
                y = None
            panel.SetResult(x, y)
#===============================================================================

class MouseWheel(eg.ActionBase):
    name = "Turn mouse wheel"
    class text:
        label = u"Turn mouse wheel %d clicks"
        text1 = "Turn mouse wheel by"
        text2 = "clicks. (Negative values turn down)"

    def __call__(self, direction=0):
        mouse_event(0x0800, 0, 0, direction * 120, 0)


    def GetLabel(self, direction=0):
        return self.text.label % direction


    def Configure(self, direction=0):
        panel = eg.ConfigPanel()
        valueCtrl = panel.SpinIntCtrl(direction, min=-100, max=100)
        panel.AddLine(self.text.text1, valueCtrl, self.text.text2)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())
#===============================================================================