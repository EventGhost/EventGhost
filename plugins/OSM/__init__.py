# -*- coding: utf-8 -*-
#
# plugins/OSM/__init__.py
#
# Copyright (C)  2009-2011 Pako  (lubos.ruckl@quick.cz)
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
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.2.11 by Pako 2015-02-01 18:41 UTC+1
#     - The Back part is divided only by the first found dot
# 0.2.10 by Pako 2014-12-23 15:59 UTC+1
#     - bugfix - Test button on dialog "Show menu"
# 0.2.9 by Pako 2012-01-18 11:13 UTC+1
#     - fixed bug - inversion of option "Show a menu without stealing focus (prevents keyboard control)"
# 0.2.8 by Pako 2012-01-18 10:23 UTC+1
#     - added option "Show a menu without stealing focus (prevents keyboard control)"
# 0.2.7 by Pako 2011-07-03 19:16 UTC+1
#     - added option "Trigger an event if the user has moved the selection in the menu"
# 0.2.6 by Pako 2011-06-27 12:40 UTC+1
#     - bugfix: problem when any menu action is called too soon after its opening
# 0.2.5 by Pako 2011-06-24 14:22 UTC+1
#     - bugfix: If an OSM menu stays open and in the background some other event
#       is triggered that emulates keystrokes forcing a change of active window
#       (for example SendKeys {Win}), EG may become unstable and possibly freeze
# 0.2.4 by Pako 2011-06-05 17:03 UTC+1
#     - Used eg.EVT_VALUE_CHANGED instead of EVT_BUTTON_AFTER
# 0.2.3 by Pako 2011-04-11 13:41 UTC+1
#     - Added some missing strings
# 0.2.2 by Pako 2010-03-10 18:46 GMT+1
#===============================================================================

eg.RegisterPlugin(
    name = "OS Menu",
    author = "Pako",
    version = "0.2.11",
    kind = "other",
    guid = "{FCF3C7A7-FBC1-444D-B768-9477521946DC}",
    description = u"""<rst>
Allows you to create custom On Screen Menu.

Plugin OSM has built-in a function **"Stop processing this event"**,
if the menu is shown on the screen. This facilitates
the use of OSM in your configuration. You can use to control
the menu the same events (the same remote buttons)
as elsewhere in the configuration, without having
to explicitly use the **"Stop processing this event"**,
**"Disable an item"** or **"Exclusive enable a folder / macro"**.
Only it is necessary to place the folder with the OSM as high
as possible in the configuration tree.""",
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=1051",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABoAAAAaCAMAAACelLz8AAADAFBMVEX/////9/f/goL/"
        "z8//x8f//v7/2dn/Kir/gID/c3P/5ub/vb3/TU3/QED/ysr/oqL/7Oz/3t7/rq7/hob/"
        "t7f/qKj/k5P/a2v/hYX/d3f/T0//WVn/NDT/7u7/MTH/vLz/MzP/+fn/0ND/ZGT/tbX/"
        "nJz/LS3/UlL/l5f/wsL/mZn/Skr/8PD/Vlb/qqr/pqb/fn7/wMD/ior/YmL/4uL/kZH/"
        "enr/0dH/b2//Rkb/4OD/aGj/6ur/6Oj/MDD/Pz//Pj7/Ly//Nzf/5OT/cXH/QkL/yMj/"
        "srL/W1v/1dX/rKz/iYn/29v/dnb/ubn/PDz/j4//np7/dHT/e3v/qan/09P/o6P/r6//"
        "ZWX/19f/ODj/Q0P/8fEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABoAABoAAFAY"
        "AAEaAAAAACgAABoAABoYAAEAAAAACCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAPAAASf/////9/fP/4LHx////v4q/9mAgP//c3O9/+ZNTf//QECi/8rs7P//3t6G"
        "/663t///qKhr/5OFhf//d3dZ/080NP//7u68/zEzM///+flk/9C1tf//nJxS/y2Xl///"
        "wsJK/5nw8P//Vlam/6p+fv//wMBi/4ri4v//kZHR/3pvb///RkZo/+Dq6v//6Og//zA+"
        "Pv//Ly/k/zdxcf//QkKy/8hbW///1dWJ/6zb2///dnY8/7mPj///np57/3Spqf//09Ov"
        "/6NlZf//19dD/zjx8f8AAAAABWgAABfHxtwAEQTHyQAAAGjHzBjHzBgAAFxuZVJpcmUu"
        "LmcAABwAAENCblQAAABBmj0AAAAAAAAAAAAAAAAAAAABAAFCadPG/kwAAADabVLsAAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAThJREFUeNp9kudWAjEQRkcQ"
        "BxSkWSgKVlAXBFQUVBTF3ju2938O55sJ7i/NOZvcL3fPTrIJ0b9tKIAWtDCsIeTUCKOF"
        "LUQ0jDo1pilqIaZh3Km4Jk6Ak8Ypp9IWJ8CTxlNOTVvM+KU461TOYs4vxXmnZizy7G8p"
        "jplJgAvyFK3UHPK8qgXgojxpKwXkpKol4HKJuaylCivIq6rWgEWPuVRBqeo6ck1VHRjM"
        "StfAbEZ/zoaqTeAWZpvb2PkOcktVW1e0K91eVLr9DnIZJnQgdEjUZe4eMXs2cQzVw0tV"
        "ohPbbJ3oFGNF1Jn7dM3UOdEFxktRV4BrohtTHaJbjHeimoC4wD2gLfAAeBR4GrzTAjwL"
        "vAACAnnAq8AboC/QALyTLtoO/wPQG1wjT26aHonu/ZP5C+O3P/VH+wFJCR8UaaZiYgAA"
        "AABJRU5ErkJggg=="
    ),
)

import wx.grid
from threading import Timer
from eg.WinApi.Utils import GetMonitorDimensions
from eg.WinApi.Dynamic import CreateEvent, SetEvent

SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
#===============================================================================

class Text:
    picker = "Colour Picker"
    triggEvt = "Trigger an event if the user has moved the selection in the menu"
    focus = "Show a menu without stealing focus (prevents keyboard control)"
    selMoved = "SelectionMoved"
    showMenu = u'''<rst>The selected monitor shows the menu, created by user.

*Basic rules for the compilation of event string:*

1) Join **Front of event string** and **Back part(s) of event string**
2) If the string contains more than three parts, truncated to three parts.
3) Truncating is performed by slicing the front parts
4) The third part is applied either as a suffix or as a payload
5) The Back part is divided only by the first found dot !

Some examples of event string compilation in mode **"suffix"**:

+-----------------------+--------------+------------------------+
| Front of event string | Back part(s) | Resulting event string |
+=======================+==============+========================+
|         OSM           | test         | **OSM.test**           |
+-----------------------+--------------+------------------------+
|         OSM.Main      | test         | **OSM.Main.test**      |
+-----------------------+--------------+------------------------+
|         OSM           | Second.Third | **OSM.Second.Third**   |
+-----------------------+--------------+------------------------+
|         OSM.Main      | OnInit.dummy | **Main.OnInit.dummy**  |
+-----------------------+--------------+------------------------+

Some examples of event string compilation in mode **"payload"**:

+-----------------------+--------------+--------------------------+
| Front of event string | Back part(s) | Resulting event string   |
+=======================+==============+==========================+
|         OSM           | test         | **OSM.test**             |
+-----------------------+--------------+--------------------------+
|         OSM.Main      | test         | **OSM.Main u"test"**     |
+-----------------------+--------------+--------------------------+
|         OSM           | Second.Third | **OSM.Second u"Third"**  |
+-----------------------+--------------+--------------------------+
|         OSM.Main      | OnInit.dummy | **Main.OnInit u"dummy"** |
+-----------------------+--------------+--------------------------+

'''

    showMenuExpr = u'''<rst>The selected monitor shows the menu, created from python expression.

This action is almost identical with the action **"Show menu"**. Different is just
a way of creating menu. Here is a menu defined by using python expression. This
expression you enter in the edit box **"List of menu items:"**. He may contain also
variables (eg **eg.result** or **eg.event.payload**).

There are two options for the tuple (list) format choice:

1) It may be simple, such as **( "Item1", "Item2", "Item3")**. In this case, each
list item also used as a label in the menu and as part of the resulting event
(along with a contents of text box **"Front of event string:"**)

2) Tuple (list) can contain nested tuples (lists). Therefore looks eg like this:
**(( "Item1", "event1"), ( "Item2", "event2"), ( "Item3", "event3"))**.
In this case, the first items of nested lists apply as a label in the menu and
the seconds items are applied as **"Back part(s) of event string"** (see the edit box
**"Back part(s) of event string:"** in configuration dialog of action **"Show menu"**).

3) Both the previous form can be freely combined. Tuple (list) can look as follows:
**(("Item1","event1"), ("Item2"), ("Item3","event3"))**

Please see the description of the action **"Show menu"**. There are examples,
which naturally also applies to this action.'''
#===============================================================================

class MenuGrid(wx.grid.Grid):

    def __init__(self, parent, lngth):
        wx.grid.Grid.__init__(self, parent)
        self.SetRowLabelSize(0)
        self.SetColLabelSize(0)
        self.SetDefaultRowSize(16)
        self.SetScrollLineX(1)
        self.SetScrollLineY(1)
        self.EnableEditing(False)
        self.EnableDragColSize(False)
        self.EnableDragRowSize(False)
        self.EnableDragGridSize(False)
        self.EnableGridLines(False)
        attr = wx.grid.GridCellAttr()
        attr.SetAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
        self.SetColAttr(0,attr)
        self.CreateGrid(lngth, 1)
        self.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.SelectRow(0)
        self.Bind(wx.grid.EVT_GRID_CMD_SELECT_CELL, self.onGridSelectCell, self)


    def SetBackgroundColour(self, colour):
        self.SetDefaultCellBackgroundColour(colour)


    def SetForegroundColour(self, colour):
        self.SetDefaultCellTextColour(colour)


    def SetFont(self, font):
        self.SetDefaultCellFont(font)


    def GetSelection(self):
        return self.GetSelectedRows()[0]


    def SetSelection(self, row):
        self.SetGridCursor(row, 0)
        self.SelectRow(row)


    def Set(self, choices):
        oldLen = self.GetNumberRows()
        newLen = len(choices)
        h = self.GetDefaultRowSize()
        if oldLen > newLen:
            self.DeleteRows(0, oldLen-newLen, False)
        elif oldLen < newLen:
            self.AppendRows(newLen-oldLen, False)
        for i in range(len(choices)):
            self.SetCellValue(i,0,choices[i])
            self.SetRowSize(i,h)


    def onGridSelectCell(self, event):
        row = event.GetRow()
        self.SelectRow(row)
        if not self.IsVisible(row,0):
            self.MakeCellVisible(row,0)
        event.Skip()


    def MoveCursor(self, step):
        max = self.GetNumberRows()
        sel = self.GetSelectedRows()[0]
        new = sel + step
        if new < 0:
            new += max
        elif new > max-1:
            new -= max
        self.SetSelection(new)
#===============================================================================
#cls types for ACTIONS list :
#===============================================================================

class ShowMenu(eg.ActionBase):
    panel = None

    class text:
        label = 'Label:'
        evtString = 'Back part(s) of event string:'
        osmLabel = 'OSM show on:'
        menuPreview = 'On screen menu preview:'
        delete = 'Delete'
        insert = 'Insert new'
        menuFont = 'Menu font:'
        txtColour = 'Text colour'
        background = 'Background colour'
        txtColourSel = 'Selected text colour'
        backgroundSel = 'Selected background colour'
        prefixLabel = 'Front of event string:'
        modeLabel = "The third part applied as:"
        mode = ("event suffix", "event payload")


    def Move(self,index,direction):
        tmpList=self.choices[:]
        max = len(self.choices)-1
        #Last to first position, other down
        if index == max and direction == 1:
            tmpList[1:] = self.choices[:-1]
            tmpList[0] = self.choices[max]
            index2 = 0
        #First to last position, other up
        elif index == 0 and direction == -1:
            tmpList[:-1] = self.choices[1:]
            tmpList[max] = self.choices[0]
            index2 = max
        else:
            index2 = index+direction
            tmpList[index] = self.choices[index2]
            tmpList[index2] = self.choices[index]
        self.choices=tmpList
        return index2


    def __call__(
        self,
        choices,
        fore,
        back,
        fontInfo,
        prefix,
        monitor = 0,
        mode = 0,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75),
        triggEvt = False,
        focus = True,
    ):
        if not self.plugin.menuDlg:
            event = CreateEvent(None, 0, 0, None)
            wx.CallAfter(
                Menu,
                choices,
                fore,
                back,
                foreSel,
                backSel,
                fontInfo,
                False,
                self.plugin,
                eg.ParseString(prefix),
                monitor,
                mode,
                event,
                triggEvt,
                focus,
            )
            eg.actionThread.WaitOnEvent(event)


    def GetLabel(
        self,
        choices,
        fore,
        back,
        fontInfo,
        prefix,
        monitor,
        mode,
        foreSel,
        backSel,
        triggEvt,
        focus,
    ):
        res = self.name+': '
        for n in range(0,min(3,len(choices))):
            res=res+choices[n][0]+', '
        res = res[:-2]
        if len(choices) > 3:
            res += ', ...'
        return res


    def Configure(
        self,
        choices=[],
        fore = (75, 75, 75),
        back = (180, 180, 180),
        fontInfo = None,
        prefix = 'OSM',
        monitor = 0,
        mode = 0,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75),
        triggEvt = False,
        focus = True,
    ):
        self.choices = choices[:]
        self.fore = fore
        self.foreSel = foreSel
        self.back = back
        self.backSel = backSel
        self.oldSel=0
        global panel
        panel = eg.ConfigPanel(self)
        mainSizer = panel.sizer
        topSizer=wx.BoxSizer(wx.HORIZONTAL)
        topMiddleSizer=wx.BoxSizer(wx.VERTICAL)
        topRightSizer=wx.FlexGridSizer(5, 2, 8, 10)
        previewLbl=wx.StaticText(panel, -1, self.text.menuPreview)
        mainSizer.Add(previewLbl)
        mainSizer.Add(topSizer,0,wx.TOP,5)
        bottomSizer=wx.GridBagSizer(3, 0)
        mainSizer.Add(bottomSizer,0,wx.TOP,6)
        #Button UP
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
        btnUP = wx.BitmapButton(panel, -1, bmp)
        btnUP.Enable(False)
        #Button DOWN
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16, 16))
        btnDOWN = wx.BitmapButton(panel, -1, bmp)
        btnDOWN.Enable(False)
        ch = len(choices) if len(choices) > 0 else 1
        listBoxCtrl = MenuGrid(panel, ch)
        listBoxCtrl.SetMinSize(wx.Size(178,148))
        listBoxCtrl.SetBackgroundColour(self.back)
        listBoxCtrl.SetForegroundColour(self.fore)
        listBoxCtrl.SetSelectionBackground(self.backSel)
        listBoxCtrl.SetSelectionForeground(self.foreSel)
        if fontInfo is None:
            font = listBoxCtrl.GetFont()
            font.SetPointSize(36)
            fontInfo = font.GetNativeFontInfoDesc()
        else:
            font = wx.FontFromNativeInfoString(fontInfo)
        for n in range(10,20):
            font.SetPointSize(n)
            btnUP.SetFont(font)
            hght = btnUP.GetTextExtent('X')[1]
            if hght > 20:
                break
        listBoxCtrl.SetDefaultCellFont(font)
        listBoxCtrl.SetDefaultRowSize(hght+4, True)
        for i in range(len(choices)):
            listBoxCtrl.SetCellFont(i,0,font)
        wdth = 178
        if (hght+4)*len(choices) > 148:
            wdth -=  SYS_VSCROLL_X
        listBoxCtrl.SetColSize(0, wdth)
        topSizer.Add(listBoxCtrl)
        topSizer.Add((20,1))
        topSizer.Add(topMiddleSizer)
        topSizer.Add((30,1))
        topSizer.Add(topRightSizer)
        labelLbl=wx.StaticText(panel, -1, self.text.label)
        labelCtrl=wx.TextCtrl(panel,-1,'',size=wx.Size(180,-1))
        eventLbl=wx.StaticText(panel, -1, self.text.evtString)
        eventCtrl = wx.TextCtrl(panel,-1,'',size=wx.Size(180,-1))
        prefixLbl=wx.StaticText(panel, -1, self.text.prefixLabel)
        prefixCtrl = wx.TextCtrl(panel,-1,prefix,size=wx.Size(96,-1))
        osmLbl = wx.StaticText(panel, -1, self.text.osmLabel)
        displayChoice = eg.DisplayChoice(panel, monitor)
        triggEvtCtrl = wx.CheckBox(panel, -1, self.plugin.text.triggEvt)
        triggEvtCtrl.SetValue(triggEvt)
        focusCtrl = wx.CheckBox(panel, -1, self.plugin.text.focus)
        focusCtrl.SetValue(focus)
        mainSizer.Add(triggEvtCtrl,0,wx.TOP,10)
        mainSizer.Add(focusCtrl,0,wx.TOP,10)
        bottomSizer.Add((20,-1),(2, 2))
        bottomSizer.Add((20,-1),(2, 5))
        bottomSizer.Add(labelLbl,(0, 0),(1,1),flag = wx.TOP,border = 8)
        bottomSizer.Add(labelCtrl,(1, 0),(1,2),wx.EXPAND)
        bottomSizer.Add(prefixLbl,(0, 3),(1,1),flag = wx.TOP, border = 8)
        bottomSizer.Add(prefixCtrl,(1, 3),(1,2),flag = wx.EXPAND)
        bottomSizer.Add(eventLbl,(2, 0),(1,1),flag = wx.TOP,border = 8)
        bottomSizer.Add(eventCtrl,(3, 0),(1,2),flag = wx.EXPAND)
        bottomSizer.Add(osmLbl,(2, 6),(1,1),flag = wx.TOP, border = 8)
        bottomSizer.Add(displayChoice,(3, 6),(1,2),flag = wx.EXPAND)
        topMiddleSizer.Add(btnUP)
        topMiddleSizer.Add(btnDOWN,0,wx.TOP,5)
        #Buttons 'Delete' and 'Insert new'
        w1 = panel.GetTextExtent(self.text.delete)[0]
        w2 = panel.GetTextExtent(self.text.insert)[0]
        if w1 > w2:
            btnDEL=wx.Button(panel,-1,self.text.delete)
            btnApp=wx.Button(panel,-1,self.text.insert,size=btnDEL.GetSize())
        else:
            btnApp=wx.Button(panel,-1,self.text.insert)
            btnDEL=wx.Button(panel,-1,self.text.delete,size=btnApp.GetSize())
        btnDEL.Enable(False)
        topMiddleSizer.Add(btnDEL,0,wx.TOP,12)
        topMiddleSizer.Add(btnApp,0,wx.TOP,9)
        #Font button
        fontLbl=wx.StaticText(panel, -1, self.text.menuFont)
        fontButton = eg.FontSelectButton(panel, value = fontInfo)
        #Button Text Colour
        foreLbl=wx.StaticText(panel, -1, self.text.txtColour+':')
        foreColourButton = eg.ColourSelectButton(panel,self.fore, title = self.text.txtColour)
        #Button Background Colour
        backLbl=wx.StaticText(panel, -1, self.text.background+':')
        backColourButton = eg.ColourSelectButton(panel,self.back, title = self.text.background)
        #Button Selected Text Colour
        foreSelLbl=wx.StaticText(panel, -1, self.text.txtColourSel+':')
        foreSelColourButton = eg.ColourSelectButton(panel,self.foreSel, title = self.text.txtColourSel)
        #Button Selected Background Colour
        backSelLbl=wx.StaticText(panel, -1, self.text.backgroundSel+':')
        backSelColourButton = eg.ColourSelectButton(panel,self.backSel, title = self.text.backgroundSel)
        topRightSizer.Add(fontLbl,0,wx.TOP,4)
        topRightSizer.Add(fontButton,0,wx.TOP,0)
        topRightSizer.Add(foreLbl,0,wx.TOP,4)
        topRightSizer.Add(foreColourButton,0,wx.TOP,0)
        topRightSizer.Add(backLbl,0,wx.TOP,4)
        topRightSizer.Add(backColourButton,0,wx.TOP,0)
        topRightSizer.Add(foreSelLbl,0,wx.TOP,4)
        topRightSizer.Add(foreSelColourButton,0,wx.TOP,0)
        topRightSizer.Add(backSelLbl,0,wx.TOP,4)
        topRightSizer.Add(backSelColourButton,0,wx.TOP,0)
        modeLbl = wx.StaticText(panel, -1, self.text.modeLabel)
        modeCtrl = wx.Choice(
            panel,
            -1,
            choices = self.text.mode
        )
        bottomSizer.Add(modeLbl,(2, 3),(1, 1),flag = wx.TOP,border = 8)
        bottomSizer.Add(modeCtrl,(3, 3),(1, 2),flag = wx.EXPAND)
        modeCtrl.SetSelection(mode)
        if len(self.choices) > 0:
            listBoxCtrl.Set([item[0] for item in self.choices])
            listBoxCtrl.SetSelection(0)
            labelCtrl.SetValue(self.choices[0][0])
            eventCtrl.SetValue(self.choices[0][1])
            self.oldSel=0
            btnUP.Enable(True)
            btnDOWN.Enable(True)
            btnDEL.Enable(True)
        else:
            labelCtrl.Enable(False)
            labelLbl.Enable(False)
            eventCtrl.Enable(False)
            eventLbl.Enable(False)
            panel.EnableButtons(False)
        listBoxCtrl.SetFocus()
        panel.sizer.Layout()


        def OnFontBtn(evt):
            value = evt.GetValue()
            font = wx.FontFromNativeInfoString(value)
            for n in range(10,20):
                font.SetPointSize(n)
                btnUP.SetFont(font)
                hght = btnUP.GetTextExtent('X')[1]
                if hght > 20:
                    break
            listBoxCtrl.SetDefaultCellFont(font)
            listBoxCtrl.SetDefaultRowSize(hght+4, True)
            for i in range(len(choices)):
                listBoxCtrl.SetCellFont(i,0,font)
            listBoxCtrl.SetFocus()
            evt.Skip()
        fontButton.Bind(eg.EVT_VALUE_CHANGED, OnFontBtn)


        def OnColourBtn(evt):
            id = evt.GetId()
            value = evt.GetValue()
            if id == foreColourButton.GetId():
                listBoxCtrl.SetForegroundColour(value)
            elif id == backColourButton.GetId():
                listBoxCtrl.SetBackgroundColour(value)
            elif id == backSelColourButton.GetId():
                listBoxCtrl.SetSelectionBackground(value)
            elif id == foreSelColourButton.GetId():
                listBoxCtrl.SetSelectionForeground(value)
            listBoxCtrl.Refresh()
            listBoxCtrl.SetFocus()
            evt.Skip()
        foreColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)
        backColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)
        foreSelColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)
        backSelColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)


        def OnClick(evt):
            #sel = listBoxCtrl.GetSelection()
            sel = evt.GetRow()
            label = labelCtrl.GetValue()
            event = eventCtrl.GetValue()
            if label.strip()<>"":
                if [item[0] for item in self.choices].count(label)==1:
                    self.oldSel=sel
                    item = self.choices[sel]
                    labelCtrl.SetValue(item[0])
                    eventCtrl.SetValue(item[1])
            listBoxCtrl.SetSelection(self.oldSel)
            listBoxCtrl.SetFocus()
            evt.Skip()
        #listBoxCtrl.Bind(wx.EVT_LISTBOX, OnClick)
        listBoxCtrl.Bind(wx.grid.EVT_GRID_CMD_CELL_LEFT_CLICK, OnClick)


        def OnButtonUp(evt):
            newSel=self.Move(listBoxCtrl.GetSelection(),-1)
            listBoxCtrl.Set([item[0] for item in self.choices])
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnUP.Bind(wx.EVT_BUTTON, OnButtonUp)


        def OnButtonDown(evt):
            newSel=self.Move(listBoxCtrl.GetSelection(),1)
            listBoxCtrl.Set([item[0] for item in self.choices])
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnDOWN.Bind(wx.EVT_BUTTON, OnButtonDown)


        def OnButtonDelete(evt):
            lngth=len(self.choices)
            if lngth==2:
                btnUP.Enable(False)
                btnDOWN.Enable(False)
            sel = listBoxCtrl.GetSelection()
            if lngth == 1:
                self.choices=[]
                listBoxCtrl.Set([])
                labelCtrl.SetValue('')
                eventCtrl.SetValue('')
                labelCtrl.Enable(False)
                labelLbl.Enable(False)
                eventCtrl.Enable(False)
                eventLbl.Enable(False)
                panel.EnableButtons(False)
                btnDEL.Enable(False)
                btnApp.Enable(True)
                evt.Skip()
                return
            elif sel == lngth - 1:
                sel = 0
            self.oldSel = sel
            tmp = self.choices.pop(listBoxCtrl.GetSelection())
            listBoxCtrl.Set([item[0] for item in self.choices])
            listBoxCtrl.SetSelection(sel)
            item = self.choices[sel]
            labelCtrl.SetValue(item[0])
            eventCtrl.SetValue(item[1])
            wdth = 178
            if listBoxCtrl.GetDefaultRowSize()*len(self.choices) > 148:
                wdth -=  SYS_VSCROLL_X
            listBoxCtrl.SetColSize(0, wdth)
            evt.Skip()
        btnDEL.Bind(wx.EVT_BUTTON, OnButtonDelete)


        def OnTextChange(evt):
            if self.choices<>[]:
                flag = False
                sel = self.oldSel
                label = labelCtrl.GetValue()
                event = eventCtrl.GetValue()
                self.choices[sel]=(label,event)
                listBoxCtrl.Set([item[0] for item in self.choices])
                listBoxCtrl.SetSelection(sel)
                if label.strip()<>"":
                    if event.strip()<>"":
                        if [item[0] for item in self.choices].count(label)==1:
                            flag = True
                panel.EnableButtons(flag)
                btnApp.Enable(flag)
            evt.Skip()
        labelCtrl.Bind(wx.EVT_TEXT, OnTextChange)
        eventCtrl.Bind(wx.EVT_TEXT, OnTextChange)


        def OnButtonAppend(evt):
            if len(self.choices)==1:
                btnUP.Enable(True)
                btnDOWN.Enable(True)
            labelCtrl.Enable(True)
            labelLbl.Enable(True)
            eventCtrl.Enable(True)
            eventLbl.Enable(True)
            if len(self.choices) > 0:
                sel = listBoxCtrl.GetSelection() + 1
                self.oldSel=sel
                self.choices.insert(sel,('',''))
            else:
                self.choices.append(('',''))
                sel = 0
            wdth = 178
            if listBoxCtrl.GetDefaultRowSize()*len(self.choices) > 148:
                wdth -=  SYS_VSCROLL_X
            listBoxCtrl.SetColSize(0, wdth)
            listBoxCtrl.Set([item[0] for item in self.choices])
            listBoxCtrl.SetSelection(sel)
            labelCtrl.SetValue('')
            labelCtrl.SetFocus()
            eventCtrl.SetValue('')
            btnApp.Enable(False)
            btnDEL.Enable(True)
            evt.Skip()
        btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)


        # re-assign the test button
        def OnButton(event):
            if not self.plugin.menuDlg:
                wx.CallAfter(
                    Menu,
                    self.choices,
                    foreColourButton.GetValue(),
                    backColourButton.GetValue(),
                    foreSelColourButton.GetValue(),
                    backSelColourButton.GetValue(),
                    fontButton.GetValue(),
                    True,
                    self.plugin,
                    prefixCtrl.GetValue(),
                    displayChoice.GetSelection(),
                    modeCtrl.GetSelection(),
                    CreateEvent(None, 0, 0, None),
                    triggEvtCtrl.GetValue(),
                    focusCtrl.GetValue(),
                )

        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnButton)

        while panel.Affirmed():
            panel.SetResult(
            self.choices,
            foreColourButton.GetValue(),
            backColourButton.GetValue(),
            fontButton.GetValue(),
            prefixCtrl.GetValue(),
            displayChoice.GetSelection(),
            modeCtrl.GetSelection(),
            foreSelColourButton.GetValue(),
            backSelColourButton.GetValue(),
            triggEvtCtrl.GetValue(),
            focusCtrl.GetValue(),
        )
#===============================================================================

class CreateMenuFromList(eg.ActionBase):
    panel = None

    class text:
        label = 'List of menu items:'
        osmLabel = 'OSM show on:'
        menuPreview = 'On screen menu preview:'
        menuFont = 'Menu font:'
        txtColour = 'Text colour'
        background = 'Background colour'
        txtColourSel = 'Selected text colour'
        backgroundSel = 'Selected background colour'
        prefixLabel = 'Front of event string:'
        modeLabel = "The third part applied as:"
        mode = ("event suffix", "event payload")


    def __call__(
        self,
        choices,
        fore,
        back,
        fontInfo,
        prefix,
        monitor=0,
        mode = 0,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75),
        triggEvt = False,
        focus = True,
    ):
        if not self.plugin.menuDlg:
            try:
                lst = eg.ParseString(choices)
                lst =  eval(lst)
            except:
                return
            chcs = []
            for item in lst:
                if type(item) is unicode or type(item) is str:
                    chcs.append((item, item))
                elif type(item) is tuple or type(item) is list:
                    if len(item) == 1:
                        chcs.append((item[0], item[0]))
                    else:
                        chcs.append(item)
            event = CreateEvent(None, 0, 0, None)
            wx.CallAfter(
                Menu,
                chcs,
                fore,
                back,
                foreSel,
                backSel,
                fontInfo,
                False,
                self.plugin,
                eg.ParseString(prefix),
                monitor,
                mode,
                event,
                triggEvt,
                focus,
            )
            eg.actionThread.WaitOnEvent(event)


    def Configure(
        self,
        choices="",
        fore = (75, 75, 75),
        back = (180, 180, 180),
        fontInfo = None,
        prefix = 'OSM',
        monitor = 0,
        mode = 0,
        foreSel = (180, 180, 180),
        backSel = (75, 75, 75),
        triggEvt = False,
        focus = True,
    ):
        self.fore = fore
        self.back = back
        self.foreSel = foreSel
        self.backSel = backSel
        self.oldSel=0
        global panel
        panel = eg.ConfigPanel(self)
        mainSizer = panel.sizer
        topSizer=wx.BoxSizer(wx.HORIZONTAL)
        topRightSizer=wx.FlexGridSizer(5,2,8,30)
        previewLbl=wx.StaticText(panel, -1, self.text.menuPreview)
        mainSizer.Add(previewLbl)
        mainSizer.Add(topSizer,0,wx.TOP,5)
        bottomSizer=wx.GridBagSizer(2, 0)
        mainSizer.Add(bottomSizer,0,wx.TOP,6)
        #Font button
        fontLbl=wx.StaticText(panel, -1, self.text.menuFont)
        fontButton = eg.FontSelectButton(panel, value = fontInfo)
        #Button Text Colour
        foreLbl=wx.StaticText(panel, -1, self.text.txtColour+':')
        foreColourButton = eg.ColourSelectButton(panel,self.fore, title = self.text.txtColour)
        #Button Background Colour
        backLbl=wx.StaticText(panel, -1, self.text.background+':')
        backColourButton = eg.ColourSelectButton(panel,self.back, title = self.text.background)
        #Button Selected Text Colour
        foreSelLbl=wx.StaticText(panel, -1, self.text.txtColourSel+':')
        foreSelColourButton = eg.ColourSelectButton(panel,self.foreSel, title = self.text.txtColourSel)
        #Button Selected Background Colour
        backSelLbl=wx.StaticText(panel, -1, self.text.backgroundSel+':')
        backSelColourButton = eg.ColourSelectButton(panel,self.backSel, title = self.text.backgroundSel)
        try:
            lst = eg.ParseString(choices)
            lst =  eval(lst)
        except:
            lst = None
        chcs = []
        if lst and len(lst) > 0:
            for item in lst:
                if type(item) is unicode or type(item) is str:
                    chcs.append((item, item))
                elif type(item) is tuple or type(item) is list:
                    if len(item) == 1:
                        chcs.append((item[0], item[0]))
                    else:
                        chcs.append(item)
        ch = len(chcs) if len(chcs) > 0 else 1
        listBoxCtrl = MenuGrid(panel, ch)
        listBoxCtrl.SetMinSize(wx.Size(240, 148))
        listBoxCtrl.SetBackgroundColour(self.back)
        listBoxCtrl.SetForegroundColour(self.fore)
        listBoxCtrl.SetSelectionBackground(self.backSel)
        listBoxCtrl.SetSelectionForeground(self.foreSel)
        if fontInfo is None:
            font = listBoxCtrl.GetFont()
            font.SetPointSize(36)
            fontInfo = font.GetNativeFontInfoDesc()
        else:
            font = wx.FontFromNativeInfoString(fontInfo)
        for n in range(10,20):
            font.SetPointSize(n)
            fontButton.SetFont(font)
            hght = fontButton.GetTextExtent('X')[1]
            if hght > 20:
                break
        listBoxCtrl.SetDefaultCellFont(font)
        listBoxCtrl.SetDefaultRowSize(hght+4, True)
        for i in range(len(chcs)):
            listBoxCtrl.SetCellFont(i,0,font)
        wdth = 240
        if (hght+4)*len(chcs) > 148:
            wdth -=  SYS_VSCROLL_X
        listBoxCtrl.SetColSize(0, wdth)
        topSizer.Add(listBoxCtrl)
        topSizer.Add((40,1))
        topSizer.Add(topRightSizer)
        listLbl = wx.StaticText(panel, -1, self.text.label)
        listCtrl = wx.TextCtrl(panel,-1,choices)
        prefixLbl = wx.StaticText(panel, -1, self.text.prefixLabel)
        prefixCtrl = wx.TextCtrl(panel,-1,prefix,size=wx.Size(96,-1))
        osmLbl = wx.StaticText(panel, -1, self.text.osmLabel)
        displayChoice = eg.DisplayChoice(panel, monitor)
        triggEvtCtrl = wx.CheckBox(panel, -1, self.plugin.text.triggEvt)
        triggEvtCtrl.SetValue(triggEvt)
        focusCtrl = wx.CheckBox(panel, -1, self.plugin.text.focus)
        focusCtrl.SetValue(focus)
        mainSizer.Add(triggEvtCtrl,0,wx.TOP,10)
        mainSizer.Add(focusCtrl,0,wx.TOP,10)
        bottomSizer.Add((30,-1),(2, 2))
        bottomSizer.Add((30,-1),(2, 5))
        bottomSizer.Add(listLbl,(0, 0), (1, 1),flag = wx.TOP,border = 8)
        bottomSizer.Add(listCtrl,(1, 0), (1, 8),flag = wx.EXPAND)
        bottomSizer.Add(prefixLbl,(2, 0), (1, 1),flag = wx.TOP, border = 8)
        bottomSizer.Add(prefixCtrl,(3, 0), (1, 2),flag = wx.EXPAND)
        bottomSizer.Add(osmLbl,(2, 6), (1, 1),flag = wx.TOP, border = 8)
        bottomSizer.Add(displayChoice, (3, 6),(1, 2),flag = wx.EXPAND)
        topRightSizer.Add(fontLbl,0,wx.TOP,4)
        topRightSizer.Add(fontButton,0,wx.TOP,0)
        topRightSizer.Add(foreLbl,0,wx.TOP,4)
        topRightSizer.Add(foreColourButton,0,wx.TOP,0)
        topRightSizer.Add(backLbl,0,wx.TOP,4)
        topRightSizer.Add(backColourButton,0,wx.TOP,0)
        topRightSizer.Add(foreSelLbl,0,wx.TOP,4)
        topRightSizer.Add(foreSelColourButton,0,wx.TOP,0)
        topRightSizer.Add(backSelLbl,0,wx.TOP,4)
        topRightSizer.Add(backSelColourButton,0,wx.TOP,0)
        #mode choice
        modeLbl = wx.StaticText(panel, -1, self.text.modeLabel)
        modeCtrl = wx.Choice(
            panel,
            -1,
            choices = self.text.mode
        )
        bottomSizer.Add(modeLbl,(2, 3),(1, 1),flag = wx.TOP,border = 8)
        bottomSizer.Add(modeCtrl,(3, 3),(1, 2),flag = wx.EXPAND)
        modeCtrl.SetSelection(mode)
        listBoxCtrl.SetFocus()
        mainSizer.Layout()


        def OnFontBtn(evt):
            value = evt.GetValue()
            font = wx.FontFromNativeInfoString(value)
            for n in range(10,20):
                font.SetPointSize(n)
                fontButton.SetFont(font)
                hght = fontButton.GetTextExtent('X')[1]
                if hght > 20:
                    break
            listBoxCtrl.SetDefaultCellFont(font)
            listBoxCtrl.SetDefaultRowSize(hght+4, True)
            for i in range(len(chcs)):
                listBoxCtrl.SetCellFont(i,0,font)
            listBoxCtrl.SetFocus()
            evt.Skip()
        fontButton.Bind(eg.EVT_VALUE_CHANGED, OnFontBtn)


        def OnColourBtn(evt):
            id = evt.GetId()
            value = evt.GetValue()
            if id == foreColourButton.GetId():
                listBoxCtrl.SetForegroundColour(value)
            elif id == backColourButton.GetId():
                listBoxCtrl.SetBackgroundColour(value)
            elif id == backSelColourButton.GetId():
                listBoxCtrl.SetSelectionBackground(value)
            elif id == foreSelColourButton.GetId():
                listBoxCtrl.SetSelectionForeground(value)
            listBoxCtrl.Refresh()
            listBoxCtrl.SetFocus()
            evt.Skip()
        foreColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)
        backColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)
        foreSelColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)
        backSelColourButton.Bind(eg.EVT_VALUE_CHANGED, OnColourBtn)


        def OnTextChange(evt=None):
            try:
                lst = eg.ParseString(listCtrl.GetValue())
                lst =  eval(lst)
                if lst and len(lst) > 0:
                    chcs = []
                    for item in lst:
                        if type(item) is unicode or type(item) is str:
                            chcs.append((item, item))
                        elif type(item) is tuple or type(item) is list:
                            if len(item) == 1:
                                chcs.append((item[0], item[0]))
                            else:
                                chcs.append(item)
                    listBoxCtrl.Set([item[0] for item in chcs])
                    wdth = 240
                    if listBoxCtrl.GetDefaultRowSize()*len(chcs) > 148:
                        wdth -=  SYS_VSCROLL_X
                    listBoxCtrl.SetColSize(0, wdth)
            except:
                listBoxCtrl.Set([])
                lst = None
            if evt:
                evt.Skip()
        listCtrl.Bind(wx.EVT_TEXT, OnTextChange)
        OnTextChange()


        # re-assign the test button
        def OnButton(event):
            if not self.plugin.menuDlg:
                try:
                    lst = eg.ParseString(listCtrl.GetValue())
                    lst =  eval(lst)
                except:
                    return
                chcs = []
                if lst and len(lst)>0:
                    for item in lst:
                        if type(item) is unicode or type(item) is str:
                            chcs.append((item, item))
                        elif type(item) is tuple or type(item) is list:
                            if len(item) == 1:
                                chcs.append((item[0], item[0]))
                            else:
                                chcs.append(item)
                        wx.CallAfter(
                            Menu,
                            chcs,
                            foreColourButton.GetValue(),
                            backColourButton.GetValue(),
                            foreSelColourButton.GetValue(),
                            backSelColourButton.GetValue(),
                            fontButton.GetValue(),
                            True,
                            self.plugin,
                            prefixCtrl.GetValue(),
                            displayChoice.GetSelection(),
                            modeCtrl.GetSelection(),
                            CreateEvent(None, 0, 0, None),
                            triggEvtCtrl.GetValue(),
                            focusCtrl.GetValue(),
                        )
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnButton)

        while panel.Affirmed():
            panel.SetResult(
            listCtrl.GetValue(),
            foreColourButton.GetValue(),
            backColourButton.GetValue(),
            fontButton.GetValue(),
            prefixCtrl.GetValue(),
            displayChoice.GetSelection(),
            modeCtrl.GetSelection(),
            foreSelColourButton.GetValue(),
            backSelColourButton.GetValue(),
            triggEvtCtrl.GetValue(),
            focusCtrl.GetValue(),
        )
#===============================================================================

class MoveCursor(eg.ActionBase):

    class text:
        step = "Step (1 - 25):"

    def __call__(self, step = 1):
        if self.plugin.menuDlg:
            self.plugin.menuDlg.MoveCursor(step * self.value)
            eg.event.skipEvent = True


    def Configure(self, step = 1):
        panel = eg.ConfigPanel(self)
        stepCtrl = panel.SpinIntCtrl(step, min=1, max=25)
        panel.AddLine(self.text.step, stepCtrl)
        while panel.Affirmed():
            panel.SetResult(
                stepCtrl.GetValue(),
                )
#===============================================================================

class PageUpDown(eg.ActionBase):

    def __call__(self):
        if self.plugin.menuDlg:
            self.plugin.menuDlg.PageUpDown(self.value)
            eg.event.skipEvent = True
#===============================================================================

class OK_Btn(eg.ActionBase):

    def __call__(self):
        if self.plugin.menuDlg:
            self.plugin.menuDlg.SendEvent()
            eg.event.skipEvent = True
#===============================================================================

class Num_Btn(eg.ActionBase):

    def __call__(self):
        if self.plugin.menuDlg:
            self.plugin.menuDlg.SendEventNum(self.value if self.value > 0 else 10)
            eg.event.skipEvent = True
#===============================================================================

class Cancel_Btn(eg.ActionBase):

    def __call__(self):
        if self.plugin.menuDlg:
            self.plugin.menuDlg.destroyMenu()
            eg.event.skipEvent = True
#===============================================================================

class Get_Btn (eg.ActionBase):

    class text:
        radiobox = 'Choice of menu attribute'
        boxLabel = 'Label'
        boxEvent = 'Event string'
        boxIndex = 'Index'
        boxBoth  = 'All'
        labelGet = 'Get'


    def __call__(self,val = 0):
        if self.plugin.menuDlg:
            eg.event.skipEvent = True
            if val < 3:
                return self.plugin.menuDlg.GetValue()[val]
            else:
                return self.plugin.menuDlg.GetValue()


    def GetLabel(self,val):
        LabelList = (
            self.text.boxLabel,
            self.text.boxEvent,
            self.text.boxIndex,
            self.text.boxBoth
        )
        return self.text.labelGet+' '+LabelList[val]


    def Configure(self, val=0):
        panel = eg.ConfigPanel(self)
        radioBoxItems = wx.RadioBox(
            panel,
            -1,
            self.text.radiobox,
            (0,0),
            (200, 104),
            choices=[
                self.text.boxLabel,
                self.text.boxEvent,
                self.text.boxIndex,
                self.text.boxBoth
            ],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxItems.SetSelection(val)
        panel.AddCtrl(radioBoxItems)

        while panel.Affirmed():
            panel.SetResult(radioBoxItems.GetSelection())
#===============================================================================

ACTIONS = (
    (ShowMenu, 'ShowMenu', 'Show menu', Text.showMenu, None),
    (CreateMenuFromList, 'CreateMenuFromList', 'Show menu, created from expression', Text.showMenuExpr, None),
    (MoveCursor, 'MoveDown', 'Cursor Down', 'Cursor Down.', 1),
    (MoveCursor, 'MoveUp', 'Cursor Up', 'Cursor Up.', -1),
    (PageUpDown, 'PageUp', 'Page Up', 'Page Up.', -1),
    (PageUpDown, 'PageDown', 'Page Down', 'Page Down.', 1),
    (OK_Btn, 'OK_Btn', 'OK', 'OK button pressed.', None),
    (Cancel_Btn, 'Cancel_Btn', 'Cancel', 'Cancel button pressed.', None),
    ( eg.ActionGroup, 'HotKeys', 'Numeric Hot Keys', 'Numeric Hot Keys ',(
        (Num_Btn, 'Num_Btn_1', 'Button 1', 'Button 1 pressed.', 1),
        (Num_Btn, 'Num_Btn_2', 'Button 2', 'Button 2 pressed.', 2),
        (Num_Btn, 'Num_Btn_3', 'Button 3', 'Button 3 pressed.', 3),
        (Num_Btn, 'Num_Btn_4', 'Button 4', 'Button 4 pressed.', 4),
        (Num_Btn, 'Num_Btn_5', 'Button 5', 'Button 5 pressed.', 5),
        (Num_Btn, 'Num_Btn_6', 'Button 6', 'Button 6 pressed.', 6),
        (Num_Btn, 'Num_Btn_7', 'Button 7', 'Button 7 pressed.', 7),
        (Num_Btn, 'Num_Btn_8', 'Button 8', 'Button 8 pressed.', 8),
        (Num_Btn, 'Num_Btn_9', 'Button 9', 'Button 9 pressed.', 9),
        (Num_Btn, 'Num_Btn_0', 'Button 0', 'Button 0 pressed.', 0),
        )),
    (Get_Btn, 'Get_Btn', 'Get value', 'Get value of selected item.', None),
)
#===============================================================================

class OSM(eg.PluginBase):
    menuDlg = None
    text = Text

    def __init__(self):
        self.AddActionsFromList(ACTIONS)
#===============================================================================

class Menu(wx.Frame):

    def __init__(
        self,
        choices,
        fore,
        back,
        foreSel,
        backSel,
        fontInfo,
        flag,
        plugin,
        prefix,
        monitor,
        mode,
        event,
        triggEvt,
        focus,
):
        wx.Frame.__init__(
            self,
            None,
            -1,
            'OS_Menu',
            style = wx.STAY_ON_TOP|wx.SIMPLE_BORDER
        )
        self.plugin  = plugin

        self.choices = choices
        self.fore    = fore
        self.back    = back
        self.foreSel = foreSel
        self.backSel = backSel
        self.flag    = flag
        self.prefix  = prefix
        self.monitor = monitor
        self.mode    = mode
        self.triggEvt = triggEvt
        self.sel = 0

    #def ShowMenu(self):
        self.SetBackgroundColour((0, 0, 0))
        if len(self.choices) == 0:
            return
        monDim = GetMonitorDimensions()
        try:
            x,y,ws,hs = monDim[monitor]
        except IndexError:
            x,y,ws,hs = monDim[0]
        choices = [item[0] for item in self.choices]
        self.eventChoiceCtrl = MenuGrid(self,len(choices))
        self.eventChoiceCtrl.SetForegroundColour(self.fore)
        self.eventChoiceCtrl.SetBackgroundColour(self.back)
        self.eventChoiceCtrl.SetSelectionBackground(self.backSel)
        self.eventChoiceCtrl.SetSelectionForeground(self.foreSel)
        if fontInfo is None:
            font = self.eventChoiceCtrl.GetDefaultCellFont()
            font.SetPointSize(36)
            fontInfo = font.GetNativeFontInfoDesc()
        else:
            font = wx.FontFromNativeInfoString(fontInfo)
        self.eventChoiceCtrl.SetFont(font)
        self.SetFont(font)
        # menu height calculation:
        h=self.GetCharHeight()+4
        for i in range(len(choices)):
            self.eventChoiceCtrl.SetCellValue(i,0,choices[i])
            self.eventChoiceCtrl.SetRowSize(i,h)
        height0 = len(choices)*h
        height1 = h*((hs-20)/h)
        height = min(height0, height1)+6
        # menu width calculation:
        width_lst=[]
        for item in choices:
            width_lst.append(self.GetTextExtent(item+' ')[0])
        width = max(width_lst) + 8
        self.eventChoiceCtrl.SetColSize(0,width)
        if height1 < height0:
            width += SYS_VSCROLL_X
        width = min((width,ws-50))+6
        x_pos = x+(ws-width)/2
        y_pos = y + (hs-height)/2
        self.SetDimensions(x_pos,y_pos,width,height)
        self.eventChoiceCtrl.SetDimensions(2,2,width-6,height-6,wx.SIZE_AUTO)
        mainSizer =wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        mainSizer.Add(self.eventChoiceCtrl, 0, wx.EXPAND)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.grid.EVT_GRID_CMD_CELL_LEFT_DCLICK, self.onDoubleClick, self.eventChoiceCtrl)
        self.Bind(wx.grid.EVT_GRID_CMD_CELL_LEFT_CLICK, self.onClick, self.eventChoiceCtrl)
        self.Bind(wx.EVT_CHAR_HOOK, self.onFrameCharHook)

        if self.flag:
            self.timer=MyTimer(t = 5.0, plugin = self.plugin)

        self.plugin.menuDlg = self
        if focus:
            eg.WinApi.Dynamic.ShowWindow(self.GetHandle(), 4)
        else:
            self.Show(True)
            self.Raise()
        wx.Yield()
        SetEvent(event)



    def testSelChange(self, sel = None):
        if sel is None:
            sel = self.eventChoiceCtrl.GetSelection()
        if sel != self.sel:
            self.sel = sel
            if self.triggEvt:
                eg.TriggerEvent(
                    self.plugin.text.selMoved,
                    prefix = self.prefix,
                    payload = (
                        self.choices[sel][0],
                        self.choices[sel][1],
                        sel
                    )
                )


    def PageUpDown(self, direction):
        max=len(self.choices)
        if max > 0:
            if direction > 0:
                self.eventChoiceCtrl.MovePageDown()
            else:
                self.eventChoiceCtrl.MovePageUp()
        self.testSelChange()


    def MoveCursor(self, step):
        max=len(self.choices)
        if max > 0:
            self.eventChoiceCtrl.MoveCursor(step)
        self.testSelChange()


    def GetValue(self):
        sel = self.eventChoiceCtrl.GetSelection()
        return (
            self.choices[sel][0],
            self.choices[sel][1],
            sel
        )


    def SendEventSel(self, sel):
        self.destroyMenu()
        evtString = self.prefix.split(".")
        sp = self.choices[sel][1]
        ix = sp.find(".")
        if ix > -1:
            evtString.append(sp[:ix])
            evtString.append(sp[ix+1:])
        else:
            evtString.append(sp)
        evtString = evtString[-3:]
        if len(evtString) == 3:
            if self.mode:
                eg.TriggerEvent(evtString[1], prefix = evtString[0], payload = evtString[2])
            else:
                eg.TriggerEvent(".".join(evtString[-2:]), prefix = evtString[0])
        elif len(evtString) == 2:
            eg.TriggerEvent(evtString[1], prefix = evtString[0])


    def SendEventNum(self, num):
        if num <= len(self.choices):
            sel = num-1
            self.SendEventSel(sel)


    def onClose(self, event):
        self.plugin.menuDlg = None
        wx.CallAfter(self.Show, False)
        wx.CallAfter(self.Destroy)


    def onFrameCharHook(self, event):
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_RETURN or keyCode == wx.WXK_NUMPAD_ENTER:
            row = self.eventChoiceCtrl.GetSelection()
            self.SendEventSel(row)
        elif keyCode == wx.WXK_ESCAPE:
            self.Close()
        elif keyCode in (wx.WXK_UP, wx.WXK_NUMPAD_UP):
            self.MoveCursor(-1)
        elif keyCode in (wx.WXK_DOWN, wx.WXK_NUMPAD_DOWN):
            self.MoveCursor(1)
        elif keyCode in (wx.WXK_PAGEUP, wx.WXK_NUMPAD_PAGEUP):
            self.PageUpDown(-1)
        elif keyCode in (wx.WXK_PAGEDOWN, wx.WXK_NUMPAD_PAGEDOWN):
            self.PageUpDown(1)
        else:
            event.Skip()


    def onClick(self, event):
        row = event.GetRow()
        self.testSelChange(row)
        event.Skip()


    def onDoubleClick(self, event):
        row = event.GetRow()
        self.SendEventSel(row)
        event.Skip()


    def SendEvent(self):
        row = self.eventChoiceCtrl.GetSelection()
        self.SendEventSel(row)


    def destroyMenu(self):
        if self.flag:
            self.timer.Cancel()
        self.Close()
#===============================================================================

class MyTimer():

    def __init__(self, t, plugin):
        self.timer = Timer(t, self.Run)
        self.plugin = plugin
        self.timer.start()


    def Run(self):
        try:
            self.plugin.menuDlg.destroyMenu()
        except:
            pass


    def Cancel(self):
        self.timer.cancel()
#===============================================================================
