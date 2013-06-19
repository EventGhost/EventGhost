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


import win32gui
import win32api
import win32con
import os
import string

from eg.WinAPI.Utils import GetTopLevelWindowOf
from eg.WinAPI.Utils import BringHwndToFront
from eg.WinAPI.cTypes import SendNotifyMessage
from eg.WinAPI.cTypes import PostMessage as Win32_PostMessage
from eg.WinAPI.cTypes import SendMessage as Win32_SendMessage

# imports local to plugin
from FindWindow import FindWindow
from SendKeys import SendKeys


def GetTargetWindows():
    hwnds = eg.lastFoundWindows
    if not hwnds:
        return [win32gui.GetForegroundWindow()]
    return hwnds


def GetTopLevelOfTargetWindows():
    hwnds = eg.lastFoundWindows
    if not hwnds:
        return [win32gui.GetForegroundWindow()]
    return list(set([GetTopLevelWindowOf(hwnd) for hwnd in hwnds]))


#=============================================================================
# Plugin: Window
#=============================================================================
class Window(eg.PluginClass):

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



class BringToFront(eg.ActionClass):
    name = "Bring to front"
    description = "Bring the specified window to front."
    iconFile = "icons/BringToFront"
    
    def __call__(self):
        for hwnd in GetTargetWindows():
            BringHwndToFront(hwnd)



class MoveTo(eg.ActionClass):
    name = "Move Absolute"
    class text:
        label = "Move window to %s"
        text1 = "Set horizontal position X to"
        text2 = "pixels"
        text3 = "Set vertical position Y to"
        text4 = "pixels"

    
    def __call__(self, x, y):
        for hwnd in GetTopLevelOfTargetWindows():
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            if x is None:
                x = left
            if y is None:
                y = top
            win32gui.MoveWindow(hwnd, x, y, right - left, bottom - top, 1)
            
            
    def GetLabel(self, x, y):
        return self.text.label % ('X:' + str(x) + ', Y:' + str(y))
         
        
    def Configure(self, x=0, y=0):
        text = self.text
        panel = eg.ConfigPanel(self)
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



class Resize(MoveTo):
    name = "Resize"
    description = "Resizes a window to the specified dimension."
    class text:
        label = "Resize window to %s, %s"
        text1 = "Set width to"
        text2 = "pixels"
        text3 = "Set height to"
        text4 = "pixels"

    
    def __call__(self, width=None, height=None):
        for hwnd in GetTopLevelOfTargetWindows():
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            if width is None:
                width = right - left - 1
            if height is None:
                height = bottom - top - 1
            win32gui.MoveWindow(hwnd, left, top, width+1, height+1, 1)
        
        
    def GetLabel(self, x, y):
        return self.text.label % (str(x), str(y))
            


class Maximize(eg.ActionClass):
    name = "Maximize"
    
    def __call__(self):
        for hwnd in GetTopLevelOfTargetWindows():
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)



class Minimize(eg.ActionClass):
    name = "Minimize"
    
    def __call__(self):
        for hwnd in GetTopLevelOfTargetWindows():
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)



class Restore(eg.ActionClass):
    name = "Restore"
    
    def __call__(self):
        for hwnd in GetTopLevelOfTargetWindows():
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)



class Close(eg.ActionClass):
    name = "Close"
    description = "Closes application windows"
    
    def __call__(self):
        for hwnd in GetTopLevelOfTargetWindows():
            SendNotifyMessage(
                hwnd, 
                win32con.WM_SYSCOMMAND, 
                win32con.SC_CLOSE, 
                0
            )



class SendMessage(eg.ActionClass):
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
                result = Win32_SendMessage(hwnd, mesg, wParam, lParam)
            else:
                result = Win32_PostMessage(hwnd, mesg, wParam, lParam)
        return result
    
            
    def GetLabel(self, mesg, wParam=0, lParam=0, kind=0):
        return self.text.name + " %s, %d, %d" % (
            self.msgToNameDict.get(mesg, str(mesg)), 
            wParam, 
            lParam
        )
            
            
    def Configure(self, mesg=win32con.WM_COMMAND, wParam=0, lParam=0, kind=0):
        choices = [x[1] for x in self.msgConstants]
        choicesValues = [x[0] for x in self.msgConstants]
        try:
            i = choicesValues.index(mesg)
            choice = choices[i]
        except:
            choice = str(mesg)

        panel = eg.ConfigPanel(self)
        
        mesgCtrl = wx.ComboBox(
            panel, 
            choices=choices, 
            style=wx.CB_DROPDOWN,
            validator=eg.DigitOnlyValidator(choices)
        )
        mesgCtrl.SetValue(choice)
        
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
                i = choices.index(choice)
                mesg = choicesValues[i]
            except:
                mesg = int(choice)
            panel.SetResult(
                mesg, 
                wParamCtrl.GetValue(),
                lParamCtrl.GetValue(), 
                1 if kindCB.GetValue() else 0
            )
        


class SetAlwaysOnTop(eg.ActionClass):
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
            if not win32gui.IsWindow(hwnd):
                self.PrintError("Not a window")
                continue
            isAlwaysOnTop = win32api.GetWindowLong(
                hwnd,
                win32con.GWL_EXSTYLE
            ) & win32con.WS_EX_TOPMOST != 0
            if action == 1 or (action == 2 and not isAlwaysOnTop):
                flag = win32con.HWND_TOPMOST
            else:
                flag = win32con.HWND_NOTOPMOST
                
            win32gui.SetWindowPos(
                hwnd, flag, 0, 0, 0, 0, win32con.SWP_NOMOVE|win32con.SWP_NOSIZE
            )


    def GetLabel(self, action):
        return self.text.actions[action]
    
    
    def Configure(self, action=2):
        panel = eg.ConfigPanel(self)
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
        
        