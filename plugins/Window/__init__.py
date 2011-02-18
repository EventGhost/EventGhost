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

import eg

eg.RegisterPlugin(
    name = "Window",
    author = "Bitmonster",
    version = "1.0." + "$LastChangedRevision$".split()[1],
    description = (
        "Actions that are related to the control of windows on the desktop, "
        "like finding specific windows, move, resize and send keypresses to "
        "them."
    ),
    kind = "core",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAV0lEQVR42u2TsRGAAAjE"
        "YDJ+NNgMJ0OwUTo5GgvTfJUcDUxLWFVjHQAwFt2d0r0DwOwQ1eNdIALEzLnRtuQWqJOm"
        "tICIjGQz+wPfCozMB1cgd/dMG7k4AXr8XoPosfNpAAAAAElFTkSuQmCC"
    ),
)


import wx
from win32api import EnumDisplayMonitors
from eg.WinApi.Utils import BringHwndToFront, CloseHwnd, GetMonitorDimensions
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



class BringToFront(eg.ActionBase):
    name = "Bring to front"
    description = "Bring the specified window to front."
    iconFile = "icons/BringToFront"
    
    def __call__(self):
        for hwnd in GetTargetWindows():
            BringHwndToFront(hwnd)



class MoveTo(eg.ActionBase):
    name = "Move Absolute"
    class text:
        label   = "Move window to: Monitor: %i, X: %s, Y: %s"
        text1   = "Set horizontal position X to"
        text2   = "pixels"
        text3   = "Set vertical position Y to"
        text4   = "pixels"
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
        panelAdd = panel.AddLine
        panelAdd(xCheckBox, xCtrl, text.text2)
        panelAdd(yCheckBox, yCtrl, text.text4)
        panelAdd((-1,0),(-1,-1),(-1,-1))
        panelAdd(displayLabel,displayChoice,(-1,-1))

        
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
        text4 = "pixels"

    
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
        panel.AddLine(yCheckBox, yCtrl, text.text4)

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
    name = "Set always on top property"
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
            style = GetWindowLong(hwnd, GWL_EXSTYLE) 
            isAlwaysOnTop = (style & WS_EX_TOPMOST) != 0
            if action == 1 or (action == 2 and not isAlwaysOnTop):
                flag = HWND_TOPMOST
            else:
                flag = HWND_NOTOPMOST
                
            SetWindowPos(hwnd, flag, 0, 0, 0, 0, SWP_NOMOVE|SWP_NOSIZE)


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
        
        