# -*- coding: utf-8 -*-
version = "0.0"

# Plugins/Digispark-RC5/__init__.py
#
# Copyright (C)  2017 Pako  (lubos.ruckl@quick.cz)
#
# This file is a plugin for EventGhost.
# Copyright � 2005-2017 EventGhost Project <http://www.eventghost.net/>
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
# 0.0 by Pako 2017-02-19 11:03 UTC+1
#       - initial version

import eg

eg.RegisterPlugin(
    name="Digispark-RC5",
    author="Pako",
    guid="{95D82769-7940-483F-977A-B923C1FF4D4D}",
    version=version,
    kind="remote",
    canMultiLoad=False,
    description="Digispark used as RC-5 receiver.",
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAADAFBMVEX////b29va2trX"
        "19cAAACsrKyoqKh8fHx4eHhNTU0rKytycnJJSUkeHh6Pj4/Nzc0oKCjLy8vIyMhgYGAF"
        "BQUBAQG2trbf399CQkITExMGBgYqKioiIiIPDw8UFBTT09MgICAMDAzZ2dm+vr4CAgKU"
        "lJRwcHBGRkYDAwPAwMCYmJhtbW0tLS0kJCSjo6Ozs7M4ODjd3d2urq5vb28vLy9PT09W"
        "VlampqbV1dW4uLgRERHJycmSkpKnp6cjIyNOTk57e3s1NTVhYWESEhJsbGw9PT2cnJzG"
        "xsZkZGTDw8O6uroODg67u7sfHx80NDQEBASampouLi5ubm5qamqWlpadnZ07OzvOzs4N"
        "DQ0dHR2Hh4c6OjpmZmZcXFwHBwdra2szMzMXFxdFRUVHR0eAgIDY2Nje3t5ISEiEhITK"
        "ysp2dnYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAEyGgAAgcAAQAAAwAAAQAHMWQAAAAEzAwAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAA0AAAAAAAAAAAAAAAAAAAAAAAAAAABdYeQE"
        "yGhdYbQEyGgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAA/wAAAAoAAAAAAAAAAAAAABIAAAD///8AAAAIMAQISugIUPQAAAAAAAAAAAYA"
        "AQAIThwITtQAAABSUOMAAQD///////8AAAAAAAAAAAAAAABSAAAAAAAEy7wEy7wAAIxG"
        "3/QEyGj9FpgAAAAAAAgAAGAAAAAIULwjGnwAAGQAAAAAAAAAAAAAAABG7tAEyGi+HHC+"
        "HHAAAEBBfoEAAABIewQEyGgAAAAAAAAAAQFCUcYIQSwAABAAABAAAAAABCwyf6NmAAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAUpJREFUeNqtk3dTwkAQxdd4"
        "FlDEFqNI1GBFFLGjYEHsIlYERcXevv8HkEt2uR0nZsYZ948k773fXW53EoC/VZ2maV55"
        "vahWgwfQKIEmD6BZAj63xN9i31olELAf2wJBlrcL4e+Azq5uCei+HjB6hegL8lyIUL8u"
        "qMKmvA4MEjAkXMuKEDA84gqMqjOMueXjvIsJFyDK8smaq6uTxhgwhd50HGAmgcKkdHZu"
        "Hq0Fx1hEubScrKqVVbV9CpdYqtM0rKlTrdOeG8rb5ECGgK1fgCwBCQ5Etndqp9h18j0a"
        "rJXZP7CdQ2z+KCdV8hjztJpDHq2TKOshywZ1ymdzhuKcASn0LqS4RFFgwBVOqmirkqOu"
        "VX6Da8qOvEV5R7lxj07c0UVsSs8RUZHyIf9Iuhx+ks6zekdFhF4AXkm+ARRM8c6/qI/P"
        "n3+K8QX/VN+GOiM6hM3BhAAAAABJRU5ErkJggg=="
    )
)

import os
from codecs import lookup
from copy import deepcopy as cpy
from datetime import datetime as dt
from threading import Timer
from time import sleep, time as ttime
from winsound import PlaySound, SND_ASYNC
from xml.dom import minidom as miniDom

import wx

from arduino import usbdevice


SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)

# ===============================================================================

class Text:
    timeout = 'Timeout for start of auto-repeat [ms]'
    timeout2 = "(0 = no autorepeat)"
    buttons = (
        'Delete remote',
        'Add remote',
        'Import remote',
        'Export remote'
    )
    buttons2 = (
        'Delete item',
        'Clear all',
        'Add item',
        'Duplicate'
    )
    buttons3 = (
        'Delete',
        'Add new'
    )
    label = 'Remote control name:'
    menuPreview = 'List of remotes:'
    prefix = "Event prefix:"
    suffixes = "Common event suffixes ..."
    header = (
        "Native event suffix",
        "Button label",
        "Common event suffix"
    )
    xmlComment1 = "Remote control definition file."
    xmlComment2 = 'Saved at %s by EventGhost plugin "Digispark-RC5".'
    choose = 'Choose a XML file to be import'
    save = 'Save configuration of remote "%s" as XML file ...'
    wildcard = "XML file (*.xml)|*.xml"
    suffTitle = "Common suffixes manager"
    suffsList = "Common suffixes list:"
    suffLabel = "Common suffix editation:"
    cancel = 'Cancel'
    ok = 'OK'
    auto = "Auto close after %i s"
    messBoxTit0 = "EventGhost - Digispark-RC5"
    messBoxTit1 = "Attention !"
    messBoxTit2 = "Attention conflict !"
    messBoxTit3 = "Attention duplicity !"
    message1 = 'Common suffix "%s" can not be deleted,\n\
because it is used in your remote "%s" !'
    message2 = 'The suffix "%s" is not possible map to the common suffix "%s" !\n\
The same suffix has been already mapped\n\
to common suffix "%s" in remote "%s"'
    message3 = 'It is not possible to import remote "%s", because there is a conflict.\n\
In the imported file, the suffix "%s"\n\
is mapped to the common suffix "%s",\n\
while in remote "%s", the same suffix\n\
is mapped to the common suffix "%s".'
    message4 = 'It is not possible to perform import, because the remote named "%s" already exists.'
    message5 = 'It is not possible to import selected file, because there is a problem.\n\
The file "%s" does not have the expected structure.'
    message6 = 'It is not possible to insert the suffix %s,\n\
because the same prefix is already in the table.'
    suffToolTip = """Native event suffix will be automatically inserted into this box, 
when you press a button on the remote control."""


# ===============================================================================

class DigisparkThreadWorker(eg.ThreadWorker):
    run = True
    plugin = None
    usbdev = None
    message = ""
    lastMessage = ""
    starttime = 0

    def Setup(self, plugin, timeout, suffs):
        self.plugin = plugin
        self.timeout = timeout
        self.suffs = suffs
        tmr = Timer(0.1, self.Run)
        tmr.start()

    def Finish(self):
        self.run = False

    def flush(self):
        while True:
            try:
                ch = self.usbdev.read()
            except:
                break

    def Init(self):
        while self.run and self.usbdev is None:
            try:
                self.usbdev = usbdevice.ArduinoUsbDevice(idVendor=0x16c0, idProduct=0x05df)
                self.flush()
            except:
                sleep(5.0)

    def Run(self):
        while self.run:
            if self.usbdev is not None:
                try:
                    ch = self.usbdev.read()
                    if ch == 10:
                        if self.message != self.lastMessage:
                            if self.timeout:
                                self.starttime = ttime()
                            if self.plugin.suffText:
                                self.plugin.SetSuffText(self.message[2:-1])
                            else:
                                suff = self.message[2:-1]
                                suff = self.suffs[suff] if suff in self.suffs else suff
                                self.plugin.TriggerEvent(suff)
                            self.lastMessage = self.message
                        else:
                            if self.timeout:
                                if 1000 * (ttime() - self.starttime) > self.timeout:
                                    if self.plugin.suffText:
                                        self.plugin.SetSuffText(self.message[2:-1])
                                    else:
                                        suff = self.message[2:-1]
                                        suff = self.suffs[suff] if suff in self.suffs else suff
                                        self.plugin.TriggerEvent(suff)
                        self.message = ""
                    else:
                        self.message += chr(ch)
                except Exception as e:
                    if str(e) == 'No Data':
                        sleep(0.2)
                    else:
                        self.usbdev = None
                        self.Init()
            else:
                self.Init()


# ===============================================================================

class Digispark_RC5(eg.PluginBase):
    text = Text
    suffText = None

    def __start__(
        self,
        prefix="RC5",
        timeout=800,
        remotes=[],
        suffixes=None
    ):
        self.info.eventPrefix = prefix
        suffs = {}
        for rem in remotes:
            for suff in rem[1]:
                suffs[suff[0]] = suff[2]
        self.workerThread = DigisparkThreadWorker(self, timeout, suffs)
        try:
            self.workerThread.Start(10)
        except:
            eg.PrintTraceback()

    def __stop__(self):
        self.workerThread.Stop(10)

    def SetSuffText(self, val):
        self.suffText.SetValue(val)

    def Configure(
        self,
        prefix="RC5",
        timeout=800,
        remotes=[],
        suffixes=None
    ):
        panel = eg.ConfigPanel(self, resizable=True)
        panel.GetParent().GetParent().SetIcon(self.info.icon.GetWxIcon())
        text = self.text
        self.remotes = cpy(remotes)
        del remotes
        if not suffixes:
            from eg.Classes.IrDecoder.Rc6 import MCE_REMOTE as MCE
            suffixes = list(MCE.itervalues())
        panel.suffixes = suffixes

        def TestUse(val):
            rem = None
            for item in self.remotes:
                for button in item[1]:
                    if button[2] == val:
                        rem = item[0]
                        break
                if rem:
                    break
            return rem

        panel.testUse = TestUse

        box0 = wx.StaticBox(panel, -1, text.timeout)
        timeoutSizer = wx.StaticBoxSizer(box0, wx.HORIZONTAL)
        timeoutCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            timeout,
            min=0,
            max=5000,
        )
        timeoutCtrl.increment = 100
        timeoutLabel = wx.StaticText(panel, -1, text.timeout2)
        timeoutSizer.Add(timeoutCtrl, 0, wx.EXPAND | wx.TOP, 4)
        timeoutSizer.Add(timeoutLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)

        leftSizer = wx.BoxSizer(wx.VERTICAL)
        box1 = wx.StaticBox(panel, -1, "")
        eventSizer = wx.StaticBoxSizer(box1, wx.VERTICAL)
        prefLabel = wx.StaticText(panel, -1, text.prefix)
        prefText = wx.TextCtrl(panel, -1, prefix)
        buttonsListCtrl = wx.ListCtrl(panel, -1,
                                      style=wx.LC_REPORT | wx.VSCROLL | wx.LC_VRULES | wx.LC_HRULES | wx.LC_SINGLE_SEL)
        self.back = buttonsListCtrl.GetBackgroundColour()
        self.fore = buttonsListCtrl.GetForegroundColour()
        self.selBack = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.selFore = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        suffText = wx.TextCtrl(panel, -1, "", style=wx.TE_READONLY)
        suffText.SetToolTip(text.suffToolTip)
        labelText = wx.TextCtrl(panel, -1, "")
        suffChoice = wx.Choice(panel, -1, choices=panel.suffixes)

        def UpdateChoices():
            suffChoice.Clear()
            suffChoice.AppendItems(panel.suffixes)

        panel.updateChoices = UpdateChoices

        evtPrefSizer = wx.BoxSizer(wx.HORIZONTAL)
        evtPrefSizer.Add(prefLabel, 0, wx.TOP, 3)
        evtPrefSizer.Add(prefText, 1, wx.EXPAND | wx.LEFT, 5)
        eventSizer.Add(evtPrefSizer, 0, wx.EXPAND | wx.TOP, 4)
        suffButton = wx.Button(panel, -1, text.suffixes)
        eventSizer.Add(suffButton, 0, wx.EXPAND | wx.TOP, 8)
        remListSizer = wx.GridBagSizer(1, 10)
        box2 = wx.StaticBox(panel, -1, "")
        rightStatSizer = wx.StaticBoxSizer(box2, wx.VERTICAL)
        rightSizer = wx.GridBagSizer(8, 1)
        rightStatSizer.Add(rightSizer, 1, wx.EXPAND)
        remListLabel = wx.StaticText(panel, -1, text.menuPreview)
        listBoxCtrl = wx.ListBox(
            panel, -1,
            style=wx.LB_SINGLE | wx.LB_NEEDED_SB
        )
        labelLbl = wx.StaticText(panel, -1, text.label)
        labelCtrl = wx.TextCtrl(panel, -1, '')
        # Buttons 'Delete', 'Import', 'Export' and 'Insert new'
        lenLst = [panel.GetTextExtent(item)[0] for item in text.buttons]
        btn = wx.Button(panel, -1, text.buttons[lenLst.index(max(lenLst))])
        sz = btn.GetSize()
        btn.Destroy()
        btnDEL = wx.Button(panel, -1, text.buttons[0], size=sz)
        btnExp = wx.Button(panel, -1, text.buttons[3], size=sz)
        btnImp = wx.Button(panel, -1, text.buttons[2], size=sz)
        btnApp = wx.Button(panel, -1, text.buttons[1], size=sz)

        def EnableBtns(enable):
            btnDEL.Enable(enable)
            btnExp.Enable(enable)

        def EnableLabel(enable):
            labelCtrl.Enable(enable)
            labelLbl.Enable(enable)

        EnableBtns(False)
        EnableLabel(False)
        lenLst = [panel.GetTextExtent(item)[0] for item in text.buttons2]
        btn = wx.Button(panel, -1, text.buttons2[lenLst.index(max(lenLst))])
        sz = btn.GetSize()
        btn.Destroy()
        delEvent = wx.Button(panel, -1, text.buttons2[0], size=sz)
        clearEvents = wx.Button(panel, -1, text.buttons2[1], size=sz)
        addEvent = wx.Button(panel, -1, text.buttons2[2], size=sz)
        duplEvent = wx.Button(panel, -1, text.buttons2[3], size=sz)

        # Button UP
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
        btnUP = wx.BitmapButton(panel, -1, bmp)
        btnUP.Enable(False)
        # Button DOWN
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16, 16))
        btnDOWN = wx.BitmapButton(panel, -1, bmp)
        btnDOWN.Enable(False)

        leftSizer.Add(timeoutSizer, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        leftSizer.Add(eventSizer, 0, wx.EXPAND)
        leftSizer.Add(remListSizer, 1, wx.EXPAND | wx.TOP, 5)
        leftSizer.Add((1, 4))
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(leftSizer, 0, wx.EXPAND)
        mainSizer.Add(rightStatSizer, 1, wx.LEFT | wx.EXPAND, 24)
        panel.sizer.Add(mainSizer, 1, wx.EXPAND)

        def EnableCtrls(enable):
            suffText.Enable(enable)
            labelText.Enable(enable)
            suffChoice.Enable(enable)
            if enable:
                self.suffText = suffText
            else:
                self.suffText = None

        def ResetCtrls():
            suffText.ChangeValue("")
            labelText.ChangeValue("")
            suffChoice.SetSelection(-1)

        def FillButtonsList(item):
            buttonsListCtrl.DeleteAllItems()
            for row in range(len(item[1])):
                buttonsListCtrl.InsertItem(row, item[1][row][0])
                buttonsListCtrl.SetItem(row, 1, item[1][row][1])
                buttonsListCtrl.SetItem(row, 2, item[1][row][2])

        def FillRemoteForm(item):
            self.oldSel = -1
            addEvent.Enable(True if self.remotes else False)
            ResetCtrls()
            FillButtonsList(item)
            clearEvents.Enable(len(item[1]) > 0)
            EnableButtonsRight(False)
            duplEvent.Enable(False)
            EnableCtrls(False)

        evtPrefSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        evtPrefSizer2.Add((-1, 1), 1, wx.EXPAND)
        w = 0
        for i, colLabel in enumerate(text.header):
            buttonsListCtrl.InsertColumn(i, colLabel)
            buttonsListCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            w += buttonsListCtrl.GetColumnWidth(i)
        buttonsListCtrl.SetSize((w + SYS_VSCROLL_X + buttonsListCtrl.GetWindowBorderSize()[0], -1))
        w0 = buttonsListCtrl.GetColumnWidth(0)
        w1 = buttonsListCtrl.GetColumnWidth(1)
        w2 = buttonsListCtrl.GetColumnWidth(2)
        suffText.SetMinSize((w0 - 1, -1))
        labelText.SetMinSize((w1 - 1, -1))
        suffChoice.SetMinSize((w2 - 1, -1))
        rightSizer.AddGrowableRow(5)
        rightSizer.Add(evtPrefSizer2, (0, 0), (1, 4), flag=wx.EXPAND | wx.TOP, border=4)
        rightSizer.Add(buttonsListCtrl, (1, 0), (5, 4), flag=wx.EXPAND)
        rightSizer.Add(delEvent, (1, 4), flag=wx.TOP | wx.ALIGN_RIGHT, border=24)
        rightSizer.Add(clearEvents, (2, 4), flag=wx.ALIGN_RIGHT)
        brdr = 8 + SYS_VSCROLL_X + buttonsListCtrl.GetWindowBorderSize()[0]
        rightSizer.Add(btnUP, (3, 4), flag=wx.LEFT, border=brdr)
        rightSizer.Add(btnDOWN, (4, 4), flag=wx.LEFT, border=brdr)
        rightSizer.Add(duplEvent, (5, 4), flag=wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT)
        rightSizer.Add(suffText, (6, 0), flag=wx.EXPAND | wx.LEFT, border=1)
        rightSizer.Add(labelText, (6, 1), flag=wx.EXPAND | wx.LEFT, border=1)
        rightSizer.Add(suffChoice, (6, 2), flag=wx.EXPAND | wx.LEFT, border=1)
        rightSizer.Add(addEvent, (6, 4), flag=wx.LEFT, border=brdr)
        rightSizer.AddGrowableCol(0, w0)
        rightSizer.AddGrowableCol(1, w1)
        rightSizer.AddGrowableCol(2, w2)
        remListSizer.AddGrowableRow(4)
        remListSizer.Add(remListLabel, (0, 0))
        remListSizer.Add(listBoxCtrl, (1, 0), (4, 1), flag=wx.EXPAND)
        remListSizer.Add(labelLbl, (5, 0), flag=wx.TOP, border=12)
        remListSizer.Add(labelCtrl, (6, 0), flag=wx.EXPAND)
        remListSizer.Add(btnDEL, (1, 1))
        remListSizer.Add(btnExp, (2, 1), flag=wx.TOP, border=5)
        remListSizer.Add(btnImp, (5, 1))
        remListSizer.Add(btnApp, (6, 1))
        panel.sizer.Layout()

        def EnableLeftSide(enable):
            EnableBtns(enable)
            EnableLabel(enable)
            btnApp.Enable(enable)
            btnImp.Enable(enable)
            remListLabel.Enable(enable)
            listBoxCtrl.Enable(enable)
            labelLbl.Enable(enable)
            labelCtrl.Enable(enable)

        def SetWidth():
            w0 = suffText.GetSize()[0] + 1
            w1 = labelText.GetSize()[0] + 1
            w2 = suffChoice.GetSize()[0] + 1
            buttonsListCtrl.SetSize((w0 + w1 + w2 + SYS_VSCROLL_X + buttonsListCtrl.GetWindowBorderSize()[0], -1))
            buttonsListCtrl.SetColumnWidth(0, w0)
            buttonsListCtrl.SetColumnWidth(1, w1)
            buttonsListCtrl.SetColumnWidth(2, w2)

        def OnSize(event):
            wx.CallAfter(SetWidth)
            panel.Update()
            event.Skip()

        panel.Bind(wx.EVT_SIZE, OnSize)

        def OnDelEvent(evt):
            rem = listBoxCtrl.GetSelection()
            self.remotes[rem][1].pop(self.oldSel)
            buttonsListCtrl.DeleteItem(self.oldSel)
            lngth = len(self.remotes[rem][1])
            if lngth == 0:
                self.oldSel = -1
                RightSide()
                ResetCtrls()
                evt.Skip()
                return
            elif self.oldSel == lngth:
                row = lngth - 1
            else:
                row = self.oldSel
            self.oldSel = -1
            SelRow(row)
            suffText.ChangeValue(buttonsListCtrl.GetItemText(row))
            labelText.ChangeValue(buttonsListCtrl.GetItem(row, 1).GetText())
            suffChoice.SetStringSelection(buttonsListCtrl.GetItem(row, 2).GetText())
            RightSide()
            Validation()
            evt.Skip()

        delEvent.Bind(wx.EVT_BUTTON, OnDelEvent)

        def OnClearEvents(evt):
            rem = listBoxCtrl.GetSelection()
            print "rem:", rem
            print self.remotes
            self.remotes[rem][1] = []
            buttonsListCtrl.DeleteAllItems()
            self.oldSel = -1
            EnableLeftSide(True)
            RightSide()
            ResetCtrls()
            evt.Skip()

        clearEvents.Bind(wx.EVT_BUTTON, OnClearEvents)

        def onButtonDelete(evt):
            sel = listBoxCtrl.GetSelection()
            listBoxCtrl.Delete(sel)
            self.remotes.pop(sel)
            lngth = len(self.remotes)
            if lngth > 0:
                if sel == lngth:
                    sel = lngth - 1
                listBoxCtrl.SetSelection(sel)
                onClick()
            else:
                labelCtrl.ChangeValue("")
                EnableBtns(False)
                EnableLabel(False)
                item = ["", []]
                FillRemoteForm(item)
            evt.Skip()

        btnDEL.Bind(wx.EVT_BUTTON, onButtonDelete)

        def OnLabelChange(evt):
            flag = False
            sel = listBoxCtrl.GetSelection()
            label = labelCtrl.GetValue()
            self.remotes[sel][0] = label
            listBoxCtrl.SetString(sel, label)
            enable = label != ""
            if enable:
                if [n[0] for n in self.remotes].count(label) == 1:
                    flag = True
            EnableBtns(enable)
            btnApp.Enable(flag)
            btnImp.Enable(flag)
            item = self.remotes[sel]
            RightSide(flag)
            evt.Skip()

        labelCtrl.Bind(wx.EVT_TEXT, OnLabelChange)

        def OnButtonAppend(evt):
            EnableLabel(True)
            item = ["", []]
            self.remotes.append(item)
            listBoxCtrl.Append("")
            listBoxCtrl.SetSelection(listBoxCtrl.GetCount() - 1)
            labelCtrl.SetValue("")
            FillRemoteForm(item)
            labelCtrl.SetFocus()
            addEvent.Enable(False)
            evt.Skip()

        btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)

        def EnableButtonsRight(enable):
            delEvent.Enable(enable)
            if enable:
                rem = listBoxCtrl.GetSelection()
                if len(self.remotes[rem][1]) < 2:
                    enable = False
            btnUP.Enable(enable)
            btnDOWN.Enable(enable)

        def RightSide(flag=True):
            rem = listBoxCtrl.GetSelection()
            label = labelCtrl.GetValue()
            if flag and rem > -1 and label != "":
                EnableLeftSide(True)
                panel.dialog.buttonRow.okButton.Enable(True)
                buttonsListCtrl.Enable(True)
                if len(self.remotes[rem][1]) == 0:
                    addEvent.Enable(True)
                    duplEvent.Enable(False)
                    EnableButtonsRight(False)
                    clearEvents.Enable(False)
                    EnableCtrls(False)
                elif len(self.remotes[rem][1]) > 0:
                    clearEvents.Enable(True)
                    if self.oldSel != -1:
                        EnableButtonsRight(True)
                        duplEvent.Enable(True)
                        EnableCtrls(True)
                    else:
                        EnableButtonsRight(False)
                        duplEvent.Enable(False)
                        EnableCtrls(False)
            else:
                panel.dialog.buttonRow.okButton.Enable(False)
                addEvent.Enable(False)
                duplEvent.Enable(False)
                EnableButtonsRight(False)
                clearEvents.Enable(False)
                EnableCtrls(False)

        def Validation():
            flag = True
            strng = suffText.GetValue()
            rem = listBoxCtrl.GetSelection()
            newSuff = suffChoice.GetStringSelection()
            name = None
            sfx = None
            for i in range(len(self.remotes)):
                item = self.remotes[i]
                if i == rem:
                    continue
                for suff in item[1]:
                    if suff[0] == strng and suff[2] != newSuff:
                        name = item[0]
                        sfx = suff[2]
                        break
                if name:
                    break
            if name:
                if newSuff == "":
                    suffChoice.SetStringSelection(suff[2])
                    self.remotes[rem][1][self.oldSel][2] = suff[2]
                    buttonsListCtrl.SetItem(self.oldSel, 2, suff[2])
                    if labelText.GetValue() == "":
                        labelText.ChangeValue(suff[1])
                        self.remotes[rem][1][self.oldSel][1] = suff[1]
                        buttonsListCtrl.SetItem(self.oldSel, 1, suff[1])
                    addEvent.Enable(True)
                    duplEvent.Enable(True)
                    EnableLeftSide(True)
                    panel.dialog.buttonRow.okButton.Enable(True)
                else:
                    MessageBox(
                        panel,
                        text.message2 % (strng, newSuff, sfx, name),
                        text.messBoxTit2,
                        wx.ICON_EXCLAMATION,
                        plugin=self,
                    )
                    flag = False
            if [item[0] for item in self.remotes[rem][1]].count(strng) > 1:
                suffText.SetValue("")
                MessageBox(
                    panel,
                    text.message6 % (strng),
                    text.messBoxTit3,
                    wx.ICON_EXCLAMATION,
                    plugin=self,
                    time=7
                )
            if strng == "":
                flag = False
            if labelText.GetValue().strip() == "":
                flag = False
            if suffChoice.GetSelection() == -1:
                flag = False
            addEvent.Enable(flag)
            duplEvent.Enable(flag)
            EnableLeftSide(flag)
            panel.dialog.buttonRow.okButton.Enable(flag)

        def SetSuffix(eventPrefix, eventSuffix):
            if prefix == eventPrefix:
                suffText.SetValue(eventSuffix)

        def OnButtonAddEvent(evt):
            if self.oldSel == -1:
                self.oldSel = buttonsListCtrl.GetItemCount() - 1
            row = self.oldSel + 1
            self.remotes[listBoxCtrl.GetSelection()][1].insert(row, ["", "", ""])
            buttonsListCtrl.InsertItem(row, "")
            buttonsListCtrl.SetItem(row, 1, "")
            buttonsListCtrl.SetItem(row, 2, "")
            buttonsListCtrl.EnsureVisible(row)
            SelRow(row)
            EnableCtrls(True)
            addEvent.Enable(False)
            duplEvent.Enable(False)
            clearEvents.Enable(True)
            EnableLeftSide(False)
            panel.dialog.buttonRow.okButton.Enable(False)
            ResetCtrls()
            EnableButtonsRight(True)
            evt.Skip()

        addEvent.Bind(wx.EVT_BUTTON, OnButtonAddEvent)
        addEvent.Enable(False)

        def OnButtonDuplEvent(evt):
            addEvent.Enable(False)
            duplEvent.Enable(False)
            panel.dialog.buttonRow.okButton.Enable(False)
            suffText.ChangeValue("")
            strng1 = labelText.GetValue()
            strng2 = suffChoice.GetStringSelection()
            row = self.oldSel + 1
            self.remotes[listBoxCtrl.GetSelection()][1].insert(row, ["", strng1, strng2])
            buttonsListCtrl.InsertItem(row, "")
            buttonsListCtrl.SetItem(row, 1, strng1)
            buttonsListCtrl.SetItem(row, 2, strng2)
            SelRow(row)
            buttonsListCtrl.EnsureVisible(row)
            evt.Skip()

        duplEvent.Bind(wx.EVT_BUTTON, OnButtonDuplEvent)

        def OnSuffText(evt):
            strng = evt.GetString()
            self.remotes[listBoxCtrl.GetSelection()][1][self.oldSel][0] = strng
            buttonsListCtrl.SetItem(self.oldSel, 0, strng)
            Validation()
            evt.Skip()

        suffText.Bind(wx.EVT_TEXT, OnSuffText)

        def OnLabelText(evt):
            strng = labelText.GetValue()
            self.remotes[listBoxCtrl.GetSelection()][1][self.oldSel][1] = strng
            buttonsListCtrl.SetItem(self.oldSel, 1, strng)
            Validation()
            evt.Skip()

        labelText.Bind(wx.EVT_TEXT, OnLabelText)

        def OnSuffChoice(evt):
            strng = suffChoice.GetStringSelection()
            self.remotes[listBoxCtrl.GetSelection()][1][self.oldSel][2] = strng
            buttonsListCtrl.SetItem(self.oldSel, 2, strng)
            if labelText.GetValue() == "":
                labelText.ChangeValue(strng)
                self.remotes[listBoxCtrl.GetSelection()][1][self.oldSel][1] = strng
                buttonsListCtrl.SetItem(self.oldSel, 1, strng)
            duplEvent.Enable(True)
            Validation()
            evt.Skip()

        suffChoice.Bind(wx.EVT_CHOICE, OnSuffChoice)

        def SelRow(row):
            if row != self.oldSel:
                if self.oldSel in range(buttonsListCtrl.GetItemCount()):
                    item = buttonsListCtrl.GetItem(self.oldSel)
                    item.SetTextColour(self.fore)
                    item.SetBackgroundColour(self.back)
                    buttonsListCtrl.SetItem(item)
                self.oldSel = row
            if buttonsListCtrl.GetItemBackgroundColour(row) != self.selBack:
                item = buttonsListCtrl.GetItem(row)
                item.SetTextColour(self.selFore)
                item.SetBackgroundColour(self.selBack)
                buttonsListCtrl.SetItem(item)

        def OnSuffixSelect(evt):
            row = evt.GetIndex()
            buttonsListCtrl.SetItemState(row, 0, wx.LIST_STATE_SELECTED)
            if row == self.oldSel:
                evt.Skip()
                return
            if not addEvent.IsEnabled() and self.oldSel > -1:
                old = self.oldSel
                self.oldSel = row
                SelRow(old)
                PlaySound('SystemExclamation', SND_ASYNC)
                evt.Skip()
                return
            EnableCtrls(True)
            SelRow(row)
            duplEvent.Enable(True)
            EnableButtonsRight(True)
            suffText.ChangeValue(buttonsListCtrl.GetItemText(row))
            labelText.ChangeValue(buttonsListCtrl.GetItem(row, 1).GetText())
            suffChoice.SetStringSelection(buttonsListCtrl.GetItem(row, 2).GetText())
            evt.Skip()

        buttonsListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, OnSuffixSelect)

        def OnBtnExp(evt):
            ix = listBoxCtrl.GetSelection()
            name = self.remotes[ix][0]
            dlg = wx.FileDialog(
                panel,
                message=text.save % name,
                defaultDir=eg.configDir,
                defaultFile=name,
                wildcard=text.wildcard,
                style=wx.FD_SAVE
            )
            if dlg.ShowModal() == wx.ID_OK:
                self.dataToXml(self.remotes[ix], dlg.GetPath())
            dlg.Destroy()
            evt.Skip()

        btnExp.Bind(wx.EVT_BUTTON, OnBtnExp)

        def OnBtnImp(evt):
            dlg = wx.FileDialog(
                panel,
                message=text.choose,
                defaultDir=eg.configDir,
                defaultFile="",
                wildcard=text.wildcard,
                style=wx.FD_OPEN | wx.FD_CHANGE_DIR
            )
            if dlg.ShowModal() == wx.ID_OK:
                filePath = dlg.GetPath()
                newitem = self.xmlToData(filePath)
                dlg.Destroy()
            else:
                dlg.Destroy()
                evt.Skip()
                return
            if not newitem:
                MessageBox(
                    panel,
                    text.message5 % os.path.split(filePath)[1],
                    text.messBoxTit1,
                    wx.ICON_EXCLAMATION,
                    plugin=self,
                )
                evt.Skip()
                return
            s = None
            for i in range(len(self.remotes)):
                rem = self.remotes[i]
                if newitem[0] == rem[0]:
                    MessageBox(
                        panel,
                        text.message4 % newitem[0],
                        text.messBoxTit2,
                        wx.ICON_EXCLAMATION,
                        plugin=self,
                    )
                    evt.Skip()
                    return
            for i in range(len(self.remotes)):
                rem = self.remotes[i]
                for suff in newitem[1]:
                    for sf in rem[1]:
                        if suff[0] == sf[0] and suff[2] != sf[2]:
                            s = suff[0]
                            n = rem[0]
                            n0 = suff[2]
                            n1 = sf[2]
                            break
                    if s:
                        break
                if s:
                    break
            if s:
                MessageBox(
                    panel,
                    text.message3 % (newitem[0], s, n0, n, n1),
                    text.messBoxTit2,
                    wx.ICON_EXCLAMATION,
                    plugin=self,
                )
                evt.Skip()
                return
            else:
                for suff in newitem[1]:
                    if suff[2] not in panel.suffixes:
                        panel.suffixes.append(suff[2])
                self.remotes.append(newitem)
                listBoxCtrl.Append(newitem[0])
                listBoxCtrl.SetSelection(listBoxCtrl.GetCount() - 1)
                labelCtrl.SetValue(newitem[0])
                FillRemoteForm(newitem)
            evt.Skip()

        btnImp.Bind(wx.EVT_BUTTON, OnBtnImp)

        def OnSuffButton(evt):
            dlg = SuffixesFrame(
                parent=panel,
                plugin=self,
            )
            dlg.Centre()
            wx.CallAfter(dlg.ShowSuffixesFrame)
            evt.Skip()

        suffButton.Bind(wx.EVT_BUTTON, OnSuffButton)

        def onButtonUp(evt):
            rem = listBoxCtrl.GetSelection()
            newSel, suffixes = Move(self.remotes[rem][1], self.oldSel, -1)
            self.remotes[rem][1] = suffixes
            FillButtonsList(self.remotes[rem])
            SelRow(newSel)
            buttonsListCtrl.EnsureVisible(self.oldSel)
            evt.Skip()

        btnUP.Bind(wx.EVT_BUTTON, onButtonUp)

        def onButtonDown(evt):
            rem = listBoxCtrl.GetSelection()
            newSel, suffixes = Move(self.remotes[rem][1], self.oldSel, 1)
            self.remotes[rem][1] = suffixes
            FillButtonsList(self.remotes[rem])
            SelRow(newSel)
            buttonsListCtrl.EnsureVisible(self.oldSel)
            evt.Skip()

        btnDOWN.Bind(wx.EVT_BUTTON, onButtonDown)

        def OnApplyBtn(evt):
            panel.dialog.buttonRow.applyButton.Enable(False)
            # evt.Skip() => applyButton work is only fictive !!!

        panel.dialog.buttonRow.applyButton.Bind(wx.EVT_BUTTON, OnApplyBtn)

        def OnCloseBox(evt):
            self.suffText = None
            evt.Skip()

        panel.dialog.Bind(wx.EVT_CLOSE, OnCloseBox)
        panel.dialog.buttonRow.cancelButton.Bind(wx.EVT_BUTTON, OnCloseBox)

        def onClick(evt=None, init=False):
            if init:
                listBoxCtrl.Set([n[0] for n in self.remotes])
                if listBoxCtrl.GetCount():
                    listBoxCtrl.SetSelection(0)
            if listBoxCtrl.GetCount():
                rem = listBoxCtrl.GetSelection()
                item = self.remotes[rem]
                FillRemoteForm(self.remotes[rem])
                EnableBtns(True)
                EnableLabel(True)
            else:
                item = ["", "", []]
            labelCtrl.ChangeValue(item[0])
            FillRemoteForm(item)
            listBoxCtrl.SetFocus()
            if evt:
                evt.Skip()

        listBoxCtrl.Bind(wx.EVT_LISTBOX, onClick)
        onClick(init=True)

        while panel.Affirmed():
            panel.SetResult(
                prefText.GetValue(),
                timeoutCtrl.GetValue(),
                self.remotes,
                panel.suffixes
            )

    # ===============================================================================

    def dataToXml(self, data, xmlpath):
        impl = miniDom.getDOMImplementation()
        dom = impl.createDocument(None, u'Remote', None)
        root = dom.documentElement
        commentNode1 = dom.createComment(self.text.xmlComment1)
        dom.insertBefore(commentNode1, root)
        commentNode2 = dom.createComment(self.text.xmlComment2 % str(dt.now())[:19])
        dom.insertBefore(commentNode2, root)
        root.setAttribute(u'Name', unicode(data[0]))
        suffixesNode = dom.createElement(u'Suffixes')
        for item in data[1]:
            suffixNode = dom.createElement(u'Suffix')
            natSuffNode = dom.createElement(u'Native_event_suffix')
            natSuffText = dom.createTextNode(unicode(item[0]))
            natSuffNode.appendChild(natSuffText)
            suffixNode.appendChild(natSuffNode)
            labelNode = dom.createElement(u'Button_label')
            labelText = dom.createTextNode(unicode(item[1]))
            labelNode.appendChild(labelText)
            suffixNode.appendChild(labelNode)
            newSuffNode = dom.createElement(u'New_event_suffix')
            newSuffixText = dom.createTextNode(unicode(item[2]))
            newSuffNode.appendChild(newSuffixText)
            suffixNode.appendChild(newSuffNode)
            suffixesNode.appendChild(suffixNode)
        root.appendChild(suffixesNode)
        f = file(xmlpath, 'wb')
        writer = lookup('utf-8')[3](f)
        dom.writexml(writer, encoding='utf-8')
        f.close()

    # ===============================================================================

    def xmlToData(self, xmlfile):
        data = []
        xmldoc = miniDom.parse(xmlfile)
        document = xmldoc.getElementsByTagName('Remote')
        if len(document) == 0:
            return None
        remote = document[0]
        name = remote.attributes["Name"].value
        data.append(name)
        suffixes = remote.getElementsByTagName('Suffixes')
        if len(suffixes) == 0:
            return None
        suffs = suffixes[0].getElementsByTagName('Suffix')
        if len(suffs) == 0:
            return None
        data2 = []
        for suffix in suffs:
            dataItem = []
            natSuff = suffix.getElementsByTagName('Native_event_suffix')
            if len(natSuff) == 0:
                return None
            dataItem.append(natSuff[0].firstChild.data)
            buttLabel = suffix.getElementsByTagName('Button_label')
            if len(buttLabel) == 0:
                return None
            dataItem.append(buttLabel[0].firstChild.data)
            newSuff = suffix.getElementsByTagName('New_event_suffix')
            if len(newSuff) == 0:
                return None
            dataItem.append(newSuff[0].firstChild.data)
            data2.append(dataItem)
        data.append(data2)
        return data


# ===============================================================================

def Move(lst, index, direction):
    tmpList = lst[:]
    max = len(lst) - 1
    # Last to first position, other down
    if index == max and direction == 1:
        tmpList[1:] = lst[:-1]
        tmpList[0] = lst[max]
        index2 = 0
    # First to last position, other up
    elif index == 0 and direction == -1:
        tmpList[:-1] = lst[1:]
        tmpList[max] = lst[0]
        index2 = max
    else:
        index2 = index + direction
        tmpList[index] = lst[index2]
        tmpList[index2] = lst[index]
    return index2, tmpList


# ===============================================================================

class SuffixesFrame(wx.Dialog):
    oldSel = 0

    def __init__(self, parent, plugin):
        self.plugin = plugin
        wx.Dialog.__init__(
            self,
            parent,
            -1,
            style=wx.RESIZE_BORDER | wx.DEFAULT_DIALOG_STYLE | wx.CLOSE_BOX | wx.TAB_TRAVERSAL,
            name=plugin.text.suffTitle
        )
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.panel = parent
        self.suffixes = cpy(self.panel.suffixes)

    def ShowSuffixesFrame(self):
        text = self.plugin.text
        self.SetTitle(text.suffTitle)
        sizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer = wx.GridBagSizer(1, 8)
        previewLbl = wx.StaticText(self, -1, text.suffsList)
        listBoxCtrl = wx.ListBox(
            self, -1,
            size=wx.Size(120, -1),
            style=wx.LB_SINGLE | wx.LB_NEEDED_SB
        )
        # Button UP
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
        btnUP = wx.BitmapButton(self, -1, bmp)
        btnUP.Enable(False)
        # Button DOWN
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16, 16))
        btnDOWN = wx.BitmapButton(self, -1, bmp)
        btnDOWN.Enable(False)
        # Buttons 'Delete' and 'Insert new'
        lenLst = [self.panel.GetTextExtent(item)[0] for item in text.buttons3]
        dummBttn = wx.Button(self, -1, text.buttons3[(lenLst).index(max(lenLst))])
        sz = dummBttn.GetSize()
        dummBttn.Destroy()
        btnDEL = wx.Button(self, -1, text.buttons3[0], size=sz)
        btnApp = wx.Button(self, -1, text.buttons3[1], size=sz)
        btnDEL.Enable(False)
        labelLbl = wx.StaticText(self, -1, text.suffLabel)
        suffLabelCtrl = wx.TextCtrl(self, -1, '')
        mainSizer.Add(previewLbl, (0, 0), flag=wx.TOP, border=5)
        mainSizer.Add(listBoxCtrl, (1, 0), (4, 1), flag=wx.TOP | wx.EXPAND)
        mainSizer.Add(btnUP, (1, 1))
        mainSizer.Add(btnDOWN, (2, 1), flag=wx.TOP, border=5)
        mainSizer.Add(btnDEL, (3, 1), flag=wx.TOP, border=5)
        mainSizer.AddGrowableRow(4, 1)
        mainSizer.Add((1, -1), (4, 1), flag=wx.EXPAND | wx.TOP, border=155)
        mainSizer.Add(labelLbl, (5, 0), flag=wx.TOP, border=6)
        mainSizer.Add(suffLabelCtrl, (6, 0), flag=wx.EXPAND)
        mainSizer.Add(btnApp, (6, 1))
        sizer.Add(mainSizer, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        line = wx.StaticLine(self, -1, size=(20, -1), pos=(200, 0), style=wx.LI_HORIZONTAL)
        btn1 = wx.Button(self, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn1.Enable(False)
        btn1.SetDefault()
        btn2 = wx.Button(self, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add((1, 5))
        sizer.Add(line, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 5)
        sizer.Add(btnsizer, 0, wx.EXPAND | wx.RIGHT, 10)
        sizer.Add((1, 5))
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.CenterOnParent()
        self.SetMinSize(self.GetSize())

        def boxEnable(enable):
            suffLabelCtrl.Enable(enable)
            labelLbl.Enable(enable)

        if len(self.suffixes) > 0:
            listBoxCtrl.Set(self.suffixes)
            listBoxCtrl.SetSelection(0)
            suffLabelCtrl.ChangeValue(self.suffixes[0])
            self.oldSel = 0
            btnUP.Enable(True)
            btnDOWN.Enable(True)
            btnDEL.Enable(True)
        else:
            boxEnable(False)
            btn1.Enable(False)

        def onClose(evt):
            self.MakeModal(False)
            self.GetParent().GetParent().Raise()
            self.Destroy()

        self.Bind(wx.EVT_CLOSE, onClose)

        def onCancel(evt):
            self.Close()

        btn2.Bind(wx.EVT_BUTTON, onCancel)

        def onOK(evt):
            self.panel.suffixes = self.suffixes
            self.panel.updateChoices()
            self.Close()

        btn1.Bind(wx.EVT_BUTTON, onOK)

        def validation():
            flag = True
            label = suffLabelCtrl.GetValue()
            if label == "":
                flag = False
            else:
                if self.suffixes.count(label) != 1:
                    flag = False
            btn1.Enable(flag)
            btnApp.Enable(flag)

        def OnTxtChange(evt):
            if self.suffixes <> []:
                sel = self.oldSel
                label = suffLabelCtrl.GetValue()
                self.suffixes[sel] = label
                listBoxCtrl.Set(self.suffixes)
                listBoxCtrl.SetSelection(sel)
                validation()
            evt.Skip()

        suffLabelCtrl.Bind(wx.EVT_TEXT, OnTxtChange)

        def onClick(evt):
            sel = listBoxCtrl.GetSelection()
            label = suffLabelCtrl.GetValue()
            if label.strip() <> "":
                if self.suffixes.count(label) == 1:
                    self.oldSel = sel
                    suffLabelCtrl.ChangeValue(self.suffixes[sel])
            listBoxCtrl.SetSelection(self.oldSel)
            listBoxCtrl.SetFocus()
            evt.Skip()

        listBoxCtrl.Bind(wx.EVT_LISTBOX, onClick)

        def onButtonUp(evt):
            newSel, self.suffixes = Move(self.suffixes, listBoxCtrl.GetSelection(), -1)
            listBoxCtrl.Set(self.suffixes)
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            validation()
            evt.Skip()

        btnUP.Bind(wx.EVT_BUTTON, onButtonUp)

        def onButtonDown(evt):
            newSel, self.suffixes = Move(self.suffixes, listBoxCtrl.GetSelection(), 1)
            listBoxCtrl.Set(self.suffixes)
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            validation()
            evt.Skip()

        btnDOWN.Bind(wx.EVT_BUTTON, onButtonDown)

        def onButtonDelete(evt):
            suff = suffLabelCtrl.GetValue()
            rem = self.panel.testUse(suff)
            if rem:
                MessageBox(
                    self,
                    text.message1 % (suff, rem),
                    text.messBoxTit1,
                    wx.ICON_EXCLAMATION,
                    plugin=self.plugin,
                    time=20
                )
                return
            lngth = len(self.suffixes)
            if lngth == 2:
                btnUP.Enable(False)
                btnDOWN.Enable(False)
            sel = listBoxCtrl.GetSelection()
            if lngth == 1:
                self.suffixes = []
                listBoxCtrl.Set([])
                suffLabelCtrl.ChangeValue("")
                boxEnable(False)
                btn1.Enable(False)
                btnDEL.Enable(False)
                btnApp.Enable(True)
                btnImp.Enable(True)
                evt.Skip()
                return
            elif sel == lngth - 1:
                sel = 0
            self.oldSel = sel
            tmp = self.suffixes.pop(listBoxCtrl.GetSelection())
            listBoxCtrl.Set(self.suffixes)
            listBoxCtrl.SetSelection(sel)
            suffLabelCtrl.ChangeValue(self.suffixes[sel])
            validation()
            evt.Skip()

        btnDEL.Bind(wx.EVT_BUTTON, onButtonDelete)

        def OnButtonAppend(evt):
            if len(self.suffixes) == 1:
                btnUP.Enable(True)
                btnDOWN.Enable(True)
            boxEnable(True)
            sel = listBoxCtrl.GetSelection() + 1
            self.oldSel = sel
            self.suffixes.insert(sel, "")
            listBoxCtrl.Set(self.suffixes)
            listBoxCtrl.SetSelection(sel)
            suffLabelCtrl.ChangeValue("")
            suffLabelCtrl.SetFocus()
            btnApp.Enable(False)
            btnDEL.Enable(True)
            evt.Skip()

        btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)

        sizer.Layout()
        self.MakeModal(True)
        self.SetFocus()
        self.Show()

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler


# ===============================================================================

class MessageBox(wx.Dialog):

    def __init__(self, parent, message, caption='', flags=0, time=0, plugin=None):
        PlaySound('SystemExclamation', SND_ASYNC)
        wx.Dialog.__init__(self, parent, style=wx.DEFAULT_DIALOG_STYLE)
        self.SetTitle(plugin.text.messBoxTit0)
        self.SetIcon(plugin.info.icon.GetWxIcon())
        if flags:
            art = None
            if flags & wx.ICON_EXCLAMATION:
                art = wx.ART_WARNING
            elif flags & wx.ICON_ERROR:
                art = wx.ART_ERROR
            elif flags & wx.ICON_QUESTION:
                art = wx.ART_QUESTION
            elif flags & wx.ICON_INFORMATION:
                art = wx.ART_INFORMATION
            if art is not None:
                bmp = wx.ArtProvider.GetBitmap(art, wx.ART_MESSAGE_BOX, (32, 32))
                icon = wx.StaticBitmap(self, -1, bmp)
                icon2 = wx.StaticBitmap(self, -1, bmp)
            else:
                icon = (32, 32)
                icon2 = (32, 32)
        if caption:
            caption = wx.StaticText(self, -1, caption)
            caption.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD))
        message = wx.StaticText(self, -1, message)
        line = wx.StaticLine(self, -1, size=(1, -1), style=wx.LI_HORIZONTAL)
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer.Add((10, 1))

        if time:
            self.cnt = time
            txt = plugin.text.auto % self.cnt
            info = wx.StaticText(self, -1, txt)
            info.Enable(False)
            bottomSizer.Add(info, 0, wx.TOP, 3)

            def UpdateInfoLabel(evt):
                self.cnt -= 1
                txt = plugin.text.auto % self.cnt
                info.SetLabel(txt)
                if not self.cnt:
                    self.Close()

            self.Bind(wx.EVT_TIMER, UpdateInfoLabel)
            self.timer = wx.Timer(self)
            self.timer.Start(1000)
        else:
            self.timer = None

        button = wx.Button(self, -1, plugin.text.ok)
        button.SetDefault()
        bottomSizer.Add((1, 1), 1, wx.EXPAND)
        bottomSizer.Add(button, 0, wx.RIGHT, 10)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(icon, 0, wx.LEFT | wx.RIGHT, 10)
        topSizer.Add((1, 1), 1, wx.EXPAND)
        topSizer.Add(caption, 0, wx.TOP, 5)
        topSizer.Add((1, 1), 1, wx.EXPAND)
        topSizer.Add(icon2, 0, wx.LEFT | wx.RIGHT, 10)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)
        mainSizer.Add(message, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        mainSizer.Add(line, 0, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(bottomSizer, 0, wx.EXPAND | wx.BOTTOM, 5)

        def OnButton(evt):
            self.Close()
            evt.Skip()

        button.Bind(wx.EVT_BUTTON, OnButton)

        def onClose(evt):
            if self.timer:
                self.timer.Stop()
                del self.timer
            self.MakeModal(False)
            self.GetParent().Raise()
            self.Destroy()

        self.Bind(wx.EVT_CLOSE, onClose)
        self.SetSizer(mainSizer)
        self.Fit()
        self.MakeModal(True)
        self.Show()

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler

# ===============================================================================
