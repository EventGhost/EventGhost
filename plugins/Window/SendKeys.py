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

"""<rst>
This action emulates keystrokes to control other programs. Just type the text 
you want into the edit-box. 

To emulate special-keys, you have to enclose a keyword in curly braces. 
For example if you want to have a cursor-up-key you write **{Up}**. You
can combine multiple keywords with the plus sign to get key-combinations like 
**{Shift+Ctrl+F1}** or **{Ctrl+V}**. The keywords are not case-sensitive, so 
you can write {SHIFT+ctrl+F1} as well if you like. 

Some keys differentiate between the left or the right side of the keyboard 
and can then be prefixed with an "L" or "R", like the Windows-Key:

**{Win}** or **{LWin}** or **{RWin}**

And here is the list of the remaining keywords EventGhost understands:

    | **{Ctrl}** or **{Control}**
    | **{Shift}**
    | **{Alt}**
    | **{Return}** or **{Enter}**
    | **{Back}** or **{Backspace}**
    | **{Tab}** or **{Tabulator}**
    | **{Esc}** or **{Escape}**
    | **{Spc}** or **{Space}**
    | **{Up}**
    | **{Down}**
    | **{Left}**
    | **{Right}**
    | **{PgUp}** or **{PageUp}**
    | **{PgDown}** or **{PageDown}**
    | **{Home}**
    | **{End}**
    | **{Ins}** or **{Insert}**
    | **{Del}** or **{Delete}**
    | **{Pause}**
    | **{Capslock}**
    | **{Numlock}**
    | **{Scrolllock}**
    | **{F1}, {F2}, ... , {F24}**
    | **{Apps}** (This is the context-menu-key)
    |
    | These will emulate keys from the numpad:
    | **{Divide}**
    | **{Multiply}**
    | **{Subtract}**
    | **{Add}**
    | **{Decimal}**
    | **{Numpad0}, {Numpad1}, ... , {Numpad9}**
"""

import eg
import wx

    
class SendKeys(eg.ActionBase):
    name = "Emulate Keystrokes"
    description = __doc__ 
    iconFile = "icons/SendKeys"
    class text:
        useAlternativeMethod = "Use alternate method to emulate keypresses"
        insertButton = "&Insert"
        specialKeyTool = "Special key tool"
        textToType = "Text to type:"
        class Keys:
            returnKey = "Return"
            enter = "Enter"
            tabulator = "Tabulator"
            backspace = "Backspace"
            escape = "Escape"
            space = "Space"
            up = "Up"
            down = "Down"
            left = "Left"
            right = "Right"
            insert = "Insert"
            delete = "Delete"
            home = "Home"
            end = "End"
            pageUp = "Page Up"
            pageDown = "Page Down"   
            win = "Windows key"
            context = "Context menu key"
            numDivide = "Numpad Divide"
            numMultiply = "Numpad Multiply"
            numSubtract = "Numpad Subtract"
            numAdd = "Numpad Add"
            numDecimal = "Numpad Decimal"
            num0 = "Numpad 0"
            num1 = "Numpad 1"
            num2 = "Numpad 2"
            num3 = "Numpad 3"
            num4 = "Numpad 4"
            num5 = "Numpad 5"
            num6 = "Numpad 6"
            num7 = "Numpad 7"
            num8 = "Numpad 8"
            num9 = "Numpad 9"
            
        
    def __call__(self, data, useAlternateMethod=False):
        hwnds = eg.lastFoundWindows
        if not hwnds:
            hwnd = None
        else:
            hwnd = hwnds[0]
        eg.SendKeys(hwnd, data, useAlternateMethod)
        
        
    def Configure(self, data="", useAlternateMethod=False):
        panel = eg.ConfigPanel(self)
        text = self.text
        key = text.Keys
        keyChoices = [
            (key.returnKey, "Return"), 
            (key.enter, "Enter"),
            (key.tabulator, "Tabulator"), 
            (key.backspace, "Backspace"),
            (key.escape, "Escape"),
            (key.space, "Space"),
            (key.up, "Up"),
            (key.down, "Down"),
            (key.left, "Left"),
            (key.right, "Right"),
            (key.insert, "Insert"),
            (key.delete, "Delete"),
            (key.home, "Home"),
            (key.end, "End"),
            (key.pageUp, "PageUp"),
            (key.pageDown, "PageDown"),
            (key.win, "Win"),
            (key.context, "Apps"),
            (key.numDivide, "Divide"),
            (key.numMultiply, "Multiply"),
            (key.numSubtract, "Subtract"),
            (key.numAdd, "Add"),
            (key.numDecimal, "Decimal"),
            (key.num0, "Numpad0"),
            (key.num1, "Numpad1"),
            (key.num2, "Numpad2"),
            (key.num3, "Numpad3"),
            (key.num4, "Numpad4"),
            (key.num5, "Numpad5"),
            (key.num6, "Numpad6"),
            (key.num7, "Numpad7"),
            (key.num8, "Numpad8"),
            (key.num9, "Numpad9"),
        ]
        fKeys = (
            "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10",
            "F11", "F12", "F13", "F14", "F15", "F16", "F17", "F18", "F19", 
            "F20", "F21", "F22", "F23", "F24"
        )
        keyLabels, keyWords = zip(*keyChoices)
        keyLabels += fKeys
        keyWords += fKeys
        textCtrl = panel.TextCtrl(data, style=wx.TE_NOHIDESEL)
        alternateMethodCB = panel.CheckBox(
            useAlternateMethod, 
            text.useAlternativeMethod
        )
        
        shiftCB = wx.CheckBox(panel, -1, "Shift")
        ctrlCB = wx.CheckBox(panel, -1, "Ctrl")
        altCB = wx.CheckBox(panel, -1, "Alt")
        keyChoice = wx.Choice(panel, -1, choices=keyLabels)
        keyChoice.SetSelection(0)
        insertButton = wx.Button(panel, -1, text.insertButton)
        def DummyHandler(dummyEvent):
            pass # used to prevent propagating of the event to the panel
        shiftCB.Bind(wx.EVT_CHECKBOX, DummyHandler)
        ctrlCB.Bind(wx.EVT_CHECKBOX, DummyHandler)
        altCB.Bind(wx.EVT_CHECKBOX, DummyHandler)
        keyChoice.Bind(wx.EVT_CHOICE, DummyHandler)
        
        def OnInsert(dummyEvent):
            res = []
            if shiftCB.GetValue():
                res.append("Shift")
            if ctrlCB.GetValue():
                res.append("Ctrl")
            if altCB.GetValue():
                res.append("Alt")
            res.append(keyWords[keyChoice.GetSelection()])
            textCtrl.WriteText("{%s}" % "+".join(res))
        insertButton.Bind(wx.EVT_BUTTON, OnInsert)
        
        cbSizer = eg.VBoxSizer(
            (shiftCB, 0, wx.EXPAND|wx.BOTTOM, 5),
            (ctrlCB, 0, wx.EXPAND|wx.BOTTOM, 5),
            (altCB, 0, wx.EXPAND, 0),
        )
        rightSizer = eg.VBoxSizer(
            (keyChoice),
            (insertButton, 0, wx.TOP|wx.ALIGN_CENTER_HORIZONTAL, 15),
        )
        staticBox = wx.StaticBox(panel, -1, text.specialKeyTool)
        specialKeySizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        specialKeySizer.Add(cbSizer)
        specialKeySizer.Add((15, 15))
        specialKeySizer.Add(rightSizer)
        
        panel.sizer.AddMany(
            (
                (panel.StaticText(text.textToType)),
                (textCtrl, 0, wx.EXPAND),
                ((10, 10)),
                (specialKeySizer, 0, wx.ALIGN_RIGHT),
                ((10, 10), 1),
                (alternateMethodCB),
            )
        )
        
        while panel.Affirmed():
            panel.SetResult(textCtrl.GetValue(), alternateMethodCB.GetValue())

