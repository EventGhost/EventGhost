# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$


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
    version = "1.0." + "$LastChangedRevision$".split()[1],
    description = (
        "Gives you actions to control the mouse pointer and emulation of "
        "mouse events."
    ),
    kind = "core",
    icon = ICON,
)


from sys import maxint
from Queue import Queue
from threading import Thread
from math import sin, cos, radians, pi
from time import sleep, clock
from eg import HasActiveHandler
from eg.cFunctions import SetMouseCallback
from eg.WinApi.Dynamic import mouse_event, GetCursorPos, SetCursorPos, POINT

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
    yRemainder = 0
    xRemainder = 0
    leftButtonDown = False
    lastTime = 0

    def __init__(self):
        Thread.__init__(self, name="MouseThread")
        self.receiveQueue = Queue(2048)
        lastTime = clock()
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
                self.speed = 0.06
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
            current_x =  sin(self.currentAngle) * factor + self.xRemainder
            current_y = -1 * cos(self.currentAngle) * factor + self.yRemainder

            x = int(current_x)
            y = int(current_y)

            self.xRemainder = current_x - x
            self.yRemainder = current_y - y
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
        


class Mouse(eg.PluginClass):
    
    def __init__(self):
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
    
    
        
class GoDirection(eg.ActionClass):
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
        panel = eg.ConfigPanel(self)
        direction = float(direction)
        valueCtrl = panel.SpinNumCtrl(float(direction), min=0, max=360)
        panel.AddLine(self.text.text1, valueCtrl, self.text.text2)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())



class LeftButton(eg.ActionClass):
    name = "Left mouse button"
    
    def __call__(self):
        def UpFunc():
            mouse_event(0x0004, 0, 0, 0, 0)
            self.plugin.leftMouseButtonDown = False
        mouse_event(0x0002, 0, 0, 0, 0)
        self.plugin.leftMouseButtonDown = True
        eg.event.AddUpFunc(UpFunc)



class MiddleButton(eg.ActionClass):
    name = "Middle mouse button"
    
    def __call__(self):
        def UpFunc():
            mouse_event(0x0040, 0, 0, 0, 0)
        mouse_event(0x0020, 0, 0, 0, 0)
        eg.event.AddUpFunc(UpFunc)
        


class RightButton(eg.ActionClass):
    name = "Right mouse button"
    
    def __call__(self):
        def UpFunc():
            mouse_event(0x0010, 0, 0, 0, 0)
        mouse_event(0x0008, 0, 0, 0, 0)
        eg.event.AddUpFunc(UpFunc)
        
        
        
class LeftDoubleClick(eg.ActionClass):
    name = "Left mouse button double-click"
    
    def __call__(self):
        def UpFunc():
            mouse_event(0x0004, 0, 0, 0, 0)
        self.plugin.leftMouseButtonDown = False
        mouse_event(0x0002, 0, 0, 0, 0)
        mouse_event(0x0004, 0, 0, 0, 0)
        mouse_event(0x0002, 0, 0, 0, 0)
        eg.event.AddUpFunc(UpFunc)



class RightDoubleClick(eg.ActionClass):
    name = "Right mouse button double-click"
    
    def __call__(self):
        def UpFunc():
            mouse_event(0x0010, 0, 0, 0, 0)
        mouse_event(0x0008, 0, 0, 0, 0)
        mouse_event(0x0010, 0, 0, 0, 0)
        mouse_event(0x0008, 0, 0, 0, 0)
        eg.event.AddUpFunc(UpFunc)
        
        
        
class ToggleLeftButton(eg.ActionClass):
    name = "Toggle left mouse button"
    
    def __call__(self):
        if self.plugin.leftMouseButtonDown:
            mouse_event(0x0004, 0, 0, 0, 0)
            self.plugin.leftMouseButtonDown = False
        else:
            mouse_event(0x0002, 0, 0, 0, 0)
            self.plugin.leftMouseButtonDown = True
            
            
            
class MoveAbsolute(eg.ActionClass):
    name = "Move Absolute"
    class text:
        label = "Move Mouse to x:%s, y:%s"
        text1 = "Set horizontal position X to"
        text2 = "pixels"
        text3 = "Set vertical position Y to"
        text4 = "pixels"

    def __call__(self, x, y):
        point = POINT()
        GetCursorPos(point)
        if x is None:
            x = point.x
        if y is None:
            y = point.y
        SetCursorPos(x, y)
            
            
    def GetLabel(self, x, y):
        return self.text.label % (str(x), str(y))

    
    def Configure(self, x=0, y=0):
        panel = eg.ConfigPanel(self)
        text = self.text
            
        xCB = panel.CheckBox(x is not None, text.text1)
        def HandleXCheckBox(event):
            xCtrl.Enable(event.IsChecked())
        xCB.Bind(wx.EVT_CHECKBOX, HandleXCheckBox)    

        if x is None:
            x = 0
            xCtrl = panel.SpinIntCtrl(x, min=-maxint-1, max=maxint)
            xCtrl.Enable(False)
        else:
            xCtrl = panel.SpinIntCtrl(x, min=-maxint-1, max=maxint)

                    
        yCB = panel.CheckBox(y is not None, text.text3)
        def HandleYCheckBox(event):
            yCtrl.Enable(event.IsChecked())  
        yCB.Bind(wx.EVT_CHECKBOX, HandleYCheckBox)    

        if y is None:
            y = 0
            yCtrl = panel.SpinIntCtrl(y, min=-maxint-1, max=maxint)
            yCtrl.Enable(False)
        else:
            yCtrl = panel.SpinIntCtrl(y, min=-maxint-1, max=maxint)
        
        panel.AddLine(xCB, xCtrl, text.text2)
        panel.AddLine(yCB, yCtrl, text.text4)

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



class MoveRelative(eg.ActionClass):
    name = "Move Relative"
    class text:
        label = "Change Mouse position by x:%s, y:%s"
        text1 = "Change horizontal position X by"
        text2 = "pixels"
        text3 = "Change vertical position Y by"
        text4 = "pixels"
    
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
        panel = eg.ConfigPanel(self)
        text = self.text

        xCB = panel.CheckBox(x is not None, text.text1)
        def HandleXCheckBox(event):
            xCtrl.Enable(event.IsChecked())
        xCB.Bind(wx.EVT_CHECKBOX, HandleXCheckBox)    

        if x is None:
            x = 0
            xCtrl = panel.SpinIntCtrl(x, min=-maxint-1, max=maxint)
            xCtrl.Enable(False)
        else:
            xCtrl = panel.SpinIntCtrl(x, min=-maxint-1, max=maxint)
        	
        yCB = panel.CheckBox(y is not None, text.text3)
        def HandleYCheckBox(event):
            yCtrl.Enable(event.IsChecked())  
        yCB.Bind(wx.EVT_CHECKBOX, HandleYCheckBox)    

        if y is None:
            y = 0
            yCtrl = panel.SpinIntCtrl(y, min=-maxint-1, max=maxint)
            yCtrl.Enable(False)
        else:
            yCtrl = panel.SpinIntCtrl(y, min=-maxint-1, max=maxint)
          
        panel.AddLine(xCB, xCtrl, text.text2)
        panel.AddLine(yCB, yCtrl, text.text4)

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



class MouseWheel(eg.ActionClass):
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
        panel = eg.ConfigPanel(self)
        valueCtrl = panel.SpinIntCtrl(direction, min=-100, max=100)
        panel.AddLine(self.text.text1, valueCtrl, self.text.text2)     
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())



