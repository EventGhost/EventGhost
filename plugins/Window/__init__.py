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


import win32gui
import win32api
import win32con
import os
import string
import wx

from eg.WinAPI.Utils import GetTopLevelWindowOf
from eg.WinAPI.Utils import BringHwndToFront
from eg.WinAPI.win32types import SendNotifyMessage
from eg.WinAPI.win32types import PostMessage as Win32_PostMessage
from eg.WinAPI.win32types import SendMessage as Win32_SendMessage



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
    pass


#-----------------------------------------------------------------------------
# Action: Window.FindWindow
#-----------------------------------------------------------------------------
from FindWindow import FindWindow



#-----------------------------------------------------------------------------
# Action: Window.BringToFront
#-----------------------------------------------------------------------------
class BringToFront(eg.ActionClass):
    name = "Bring to front"
    description = "Bring the specified window to front."
    iconFile = "icons/BringToFront"
    
    def __call__(self):
        for hwnd in GetTargetWindows():
            BringHwndToFront(hwnd)



#-----------------------------------------------------------------------------
# Action: Window.SendKeys
#-----------------------------------------------------------------------------
from SendKeys import SendKeys


#-----------------------------------------------------------------------------
# Action: Window.MoveTo
#-----------------------------------------------------------------------------
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
        dialog = eg.ConfigurationDialog(self)
        text = self.text

        xCB = wx.CheckBox(dialog, -1, text.text1)
        xCB.SetValue(x is not None)
        def HandleXCheckBox(event):
            xCtrl.Enable(event.IsChecked())
        xCB.Bind(wx.EVT_CHECKBOX, HandleXCheckBox)    

        xCtrl = eg.SpinIntCtrl(dialog, min=-32768, max=32767)
        if x is None:
            x = 0
            xCtrl.Enable(False)
        xCtrl.SetValue(x)
        

        yCB = wx.CheckBox(dialog, -1, text.text3)
        yCB.SetValue(y is not None)
        def HandleYCheckBox(event):
            yCtrl.Enable(event.IsChecked())
        yCB.Bind(wx.EVT_CHECKBOX, HandleYCheckBox)    

        yCtrl = eg.SpinIntCtrl(dialog, min=-32768, max=32767)
        if y is None:
            y = 0
            yCtrl.Enable(False)
        yCtrl.SetValue(y)
        
        dialog.AddGrid(
            (
                (xCB, xCtrl, text.text2),
                (yCB, yCtrl, text.text4),
            )
        )

        if dialog.AffirmedShowModal():
            if xCtrl.IsEnabled():
                x = xCtrl.GetValue()
            else:
                x = None
                
            if yCtrl.IsEnabled():
                y = yCtrl.GetValue()
            else:
                y = None
            return (x, y)



#-----------------------------------------------------------------------------
# Action: Window.Resize
#-----------------------------------------------------------------------------
class Resize(eg.ActionClass):
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
            
            
    def Configure(self, x=0, y=0):
        dialog = eg.ConfigurationDialog(self)
        text = self.text
        xCB = wx.CheckBox(dialog, -1, text.text1)
        xCB.SetValue(x is not None)
        
        xCtrl = eg.SpinIntCtrl(dialog, min=-32768, max=32767)
        if x is None:
            x = 0
            xCtrl.Enable(False)
        xCtrl.SetValue(x)
        
        def HandleXCheckBox(event):
            xCtrl.Enable(event.IsChecked())
        xCB.Bind(wx.EVT_CHECKBOX, HandleXCheckBox)    

        yCB = wx.CheckBox(dialog, -1, text.text3)
        yCB.SetValue(y is not None)
        yCtrl = eg.SpinIntCtrl(dialog, min=-32768, max=32767)
        if y is None:
            y = 0
            yCtrl.Enable(False)
        yCtrl.SetValue(y)
        
        def HandleYCheckBox(event):
            yCtrl.Enable(event.IsChecked())
        yCB.Bind(wx.EVT_CHECKBOX, HandleYCheckBox)    

        dialog.AddGrid(
            (
                (xCB, xCtrl, text.text2),
                (yCB, yCtrl, text.text4),
            )
        )

        if dialog.AffirmedShowModal():
            if xCtrl.IsEnabled():
                x = xCtrl.GetValue()
            else:
                x = None
                
            if yCtrl.IsEnabled():
                y = yCtrl.GetValue()
            else:
                y = None
            return (x, y)



#-----------------------------------------------------------------------------
# Action: Window.Maximize
#-----------------------------------------------------------------------------
class Maximize(eg.ActionClass):
    name = "Maximize"
    
    def __call__(self):
        for hwnd in GetTopLevelOfTargetWindows():
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)



#-----------------------------------------------------------------------------
# Action: Window.Minimize
#-----------------------------------------------------------------------------
class Minimize(eg.ActionClass):
    name = "Minimize"
    
    def __call__(self):
        for hwnd in GetTopLevelOfTargetWindows():
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)



#-----------------------------------------------------------------------------
# Action: Window.Restore
#-----------------------------------------------------------------------------
class Restore(eg.ActionClass):
    name = "Restore"
    
    def __call__(self):
        for hwnd in GetTopLevelOfTargetWindows():
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)



#-----------------------------------------------------------------------------
# Action: Window.Close
#-----------------------------------------------------------------------------
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



#-----------------------------------------------------------------------------
# Action: Window.SendMessage
#-----------------------------------------------------------------------------
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
        
        if panel.Affirmed():
            choice = mesgCtrl.GetValue()
            try:
                i = choices.index(choice)
                mesg = choicesValues[i]
            except:
                mesg = int(choice)
            if kindCB.GetValue():
                kind = 1
            else:
                kind = 0
            return (
                mesg, 
                wParamCtrl.GetValue(),
                lParamCtrl.GetValue(), 
                kind
            )
        

#-----------------------------------------------------------------------------
# Action: Window.SetAlwaysOnTop
#-----------------------------------------------------------------------------
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
        dialog = eg.ConfigurationDialog(self)
        radioBox = wx.RadioBox(
            dialog, 
            -1,
            self.text.radioBox,
            choices=self.text.actions, 
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(action)
        dialog.sizer.Add(radioBox, 0, wx.EXPAND)

        if dialog.AffirmedShowModal():
            return (radioBox.GetSelection(), )
        
        