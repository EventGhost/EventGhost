# -*- coding: utf-8 -*-
#
version = "0.2"
# This file is a plugin for EventGhost.
# Copyright (C) 2005-2017 www.eventghost.net
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
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.2 by Pako 2017-07-17 08:34 UTC+1
#     - bugfix
# 0.1 by Pako 2017-07-03 14:21 UTC+1
#     - added support for module RF125-PS
# 0.0 by Pako 2017-05-28 09:02 UTC+1
#     - initial version
#===============================================================================


eg.RegisterPlugin(
    name = "RDM6300",
    author = "Pako",
    version = version,
    kind = "external",
    guid = "{5CB8D6DC-AE57-4254-8457-46A0FC770B64}",
    canMultiLoad = False,
    description =  '''<rst>
Hardware plugin for the 125kHz RFID module RDM6300 or RF125-PS.

.. image:: picture.jpg
.. image:: picture2.jpg

Plugin version: %s
''' % version,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=9688",
    icon = (
        "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"
    ),
)

import wx
from time import clock
from winsound import Beep
from winsound import PlaySound, SND_ASYNC
from eg.WinApi.Dynamic import GetCommState, byref
ACV = wx.ALIGN_CENTER_VERTICAL
SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
DEFAULT_WAIT = 15.0
#===============================================================================

def Move(lst, index, direction):
    tmpList = lst[:]
    max = len(lst)-1
    #Last to first position, other down
    if index == max and direction == 1:
        tmpList[1:] = lst[:-1]
        tmpList[0] = lst[max]
        index2 = 0
    #First to last position, other up
    elif index == 0 and direction == -1:
        tmpList[:-1] = lst[1:]
        tmpList[max] = lst[0]
        index2 = max
    else:
        index2 = index + direction
        tmpList[index] = lst[index2]
        tmpList[index2] = lst[index]
    return index2, tmpList
#===============================================================================

def getID(data):
    if ord(data[0]) != 2 or ord(data[-1]) != 3:
        return "ERROR 1"
    if len(data) == 14:
        chsum = int(data[-3:-1], 16)
    elif len(data) == 13:
        chsum = ord(data[-2])
    else:
        return "ERROR 2"
    lng = 10
    tmp = 0
    for ix in range(1, lng + 1, 2):
        tmp = tmp ^ int(data[ix:ix + 2], 16)
    if tmp != chsum:
        return "ERROR 3"
    res = int(data[1:lng + 1], 16)
    return str(res).zfill(13)
#===============================================================================

class Text:
    timeout = "Timeout [ms]:  "
    header1 = (
        "Serial port",
        "Event prefix"
    )
    header2 = (
        "ID/Native event suffix",
        "Human readable suffix"
    )
    suffToolTip = """Native event suffix will be automatically inserted into 
this box, when you put a RFID tag on the sensor."""
    buttons = (
        'Delete item',
        'Clear all',
        'Add item',
    )
    message1 = 'It is not possible to insert the serial port "%s",\n\
because the same port is already in the table.'
    message2 = 'It is not possible to insert the suffix (tag) "%s",\n\
because the same suffix is already in the table.'
    ok = 'OK'
    auto = "Auto close after %i s"
    messBoxTit0 = "EventGhost - RDM6300"
    messBoxTit1 = "Attention - duplicity !"
    started = 'SerialThreadStarted'
    stopped = 'SerialThreadStopped'
#===============================================================================

class ListCtrl(wx.ListCtrl):

    def GetRow(self, row):
        rowData=[]
        for i in range(self.GetColumnCount()):
            rowData.append(self.GetItem(row, i).GetText())
        return rowData


    def GetData(self):
        data = []
        for row in range(self.GetItemCount()):
            rowData = self.GetRow(row)
            data.append(rowData)
        return data
#===============================================================================

class SerialThread(eg.SerialThread):
    hFile = None
    prefix = None
    buff = ""
    lastEvt = 0

    def setPrefix(self, prefix):
        self.prefix = prefix


    def getBuffer(self):
        return self.buff


    def setBuffer(self, txt):
        self.buff = txt


    def Open(self, port = 0, baudrate = 9600, mode = "8N1"):
        eg.SerialThread.Open(self, port, baudrate, mode)
        if self.hFile == 0xFFFFFFFF:
            self.hFile = None
        return self.hFile


    def gcs(self):
        try:
            return GetCommState(self.hFile, byref(self.dcb))
        except:
            return 0
#===============================================================================

class RDM6300(eg.PluginBase):

    text = Text
    suffText = None

    def __start__(
        self,
        timeout = 300,
        devices = [],
        suffixes = []
        ):
        self.timeout = timeout/1000.0
        self.devices = devices
        self.suffs = dict(suffixes)
        self.threads = {}
        self.flags = {}
        self.buffers = {}
        for item in devices:
            self.flags[item[0]] = False
        self.watchdog = eg.scheduler.AddTask(0.1, self.watcher)


    def OnComputerResume(self, dummy):
        self.stopWatchdog()
        trItem = self.info.treeItem
        args = list(trItem.GetArguments())
        self.__start__(*args)


    def OnComputerSuspend(self, dummy):
        self.stopWatchdog()
        self.StopThreads()


    def watcher(self):
        if not self.info.isStarted:
            return
        self.watchdog = eg.scheduler.AddTask(DEFAULT_WAIT, self.watcher)
        for item in self.devices:
            flag = self.flags[item[0]]
            if len(self.threads) > 0 and item[0] in self.threads:
                thrd = self.threads[item[0]]
                state = thrd.gcs()
            else:
                state = False
            if not state:
                if flag:
                    eg.TriggerEvent(self.text.stopped, prefix = item[1])
                    self.flags[item[0]] = False
                thrd = self.startSerialThread(item)
                if thrd:
                    state = thrd.gcs()
                    if state:
                        eg.TriggerEvent(self.text.started, prefix = item[1])
                        self.flags[item[0]] = True


    def stopWatchdog(self):
        if self.watchdog:
            try:
                eg.scheduler.CancelTask(self.watchdog)
            except:
                pass


    def startSerialThread(self, dev):
        if dev[0] in self.threads:
            thrd = self.threads[dev[0]]
            if thrd in self.buffers:
                del self.buffers[thrd]
            self.threads[dev[0]] = None
            del self.threads[dev[0]]
        thrd = SerialThread()
        self.threads[dev[0]] = thrd
        thrd.setPrefix(dev[1])
        try:
            hFile = thrd.Open(int(dev[0].split("COM")[-1]) - 1, 9600)
            if hFile:
                self.buffers[thrd] = ""
                thrd.Start()
                thrd.SetReadEventCallback(self.OnReceive)
        except:
            pass
        return thrd


    def StopThreads(self):
        for item in self.devices:
            if item[0] in self.threads:
                if self.threads[item[0]].gcs():
                    self.threads[item[0]].SuspendReadEvents()
                    self.threads[item[0]].Close()
                    eg.TriggerEvent(self.text.stopped, prefix = item[1])
        self.threads = {}
        del self.threads
        del self.devices
        del self.suffs
        del self.flags
        del self.buffers

    @eg.LogIt
    def __stop__(self):
        self.StopThreads()


    def OnReceive(self, serialThread):
        self.buffers[serialThread] += serialThread.Read(1024)
        while True:
            terminatorPos = self.buffers[serialThread].find("\x03")
            if terminatorPos < 0:
                break
            data = self.buffers[serialThread] [0:terminatorPos + 1]
            self.buffers[serialThread] = \
                self.buffers[serialThread][terminatorPos + 1:]
            if len(data) < 2:
                continue
            suff = getID(data)
            if not suff.startswith("ERROR"):
                now = clock()
                if now - serialThread.lastEvt > self.timeout:
                    if self.suffText:
                        self.SetSuffText(suff)
                    else:
                        Beep(1000, 250)
                        if suff in self.suffs:
                            eg.TriggerEvent(
                                "Known.%s" % self.suffs[suff],
                                prefix = serialThread.prefix,
                                payload = suff
                            )
                        else:
                            eg.TriggerEvent(
                                "Unknown",
                                prefix = serialThread.prefix,
                                payload = suff
                            )
                serialThread.lastEvt = now


    def SetSuffText(self, val):
        self.suffText.SetValue(val)


    def Configure(
        self,
        timeout = 300,
        devices = [],
        suffixes = [] 
        ):
        panel = eg.ConfigPanel()
        text = self.text
        self.oldDevSel = -1
        self.oldSel = -1
        panel.GetParent().GetParent().SetIcon(self.info.icon.GetWxIcon())
        timeoutLabel = wx.StaticText(panel.dialog, -1, text.timeout)
        timeoutCtrl = eg.SpinIntCtrl(
            panel.dialog,
            -1,
            timeout,
            min = 10,
            max = 5000
        )
        timeoutCtrl.increment = 10
        leftSizer = wx.GridBagSizer(8, 1)
        devListCtrl = ListCtrl(
            panel,
            -1,
            style = wx.LC_REPORT | 
                wx.VSCROLL |
                wx.LC_VRULES |
                wx.LC_HRULES |
                wx.LC_SINGLE_SEL
        )
        self.back = devListCtrl.GetBackgroundColour()
        self.fore = devListCtrl.GetForegroundColour()
        self.selBack = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.selFore = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        lenLst = [panel.GetTextExtent(item)[0] for item in text.buttons]
        btn = wx.Button(panel,-1,text.buttons[lenLst.index(max(lenLst))])
        sz = btn.GetSize()
        btn.Destroy()

        delDev = wx.Button(panel, -1, text.buttons[0], size = sz)
        clearDevs = wx.Button(panel, -1, text.buttons[1], size = sz)
        addDev = wx.Button(panel, -1, text.buttons[2], size = sz)

        #Button UP
        bmpUp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
        btnDevUP = wx.BitmapButton(panel, -1, bmpUp)
        btnDevUP.Enable(False)
        #Button DOWN
        bmpDown = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16,16))
        btnDevDOWN = wx.BitmapButton(panel, -1, bmpDown)
        btnDevDOWN.Enable(False)
        portCtrl = eg.SerialPortChoice(panel, -1)
        portCtrl.SetSelection(-1)
        prefixCtrl = wx.TextCtrl(panel, -1, "")

        def FillDevList(lst):
            devListCtrl.DeleteAllItems()
            for row in range(len(lst)):
                devListCtrl.InsertItem(row, lst[row][0])
                devListCtrl.SetItem(row, 1, lst[row][1])

        w = 0
        for i, colLabel in enumerate(text.header1):
            devListCtrl.InsertColumn(i, colLabel)
            devListCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            w += devListCtrl.GetColumnWidth(i)
        devListCtrl.SetSize((
            w + SYS_VSCROLL_X + devListCtrl.GetWindowBorderSize()[0],
            -1
        ))
        w0 = panel.GetTextExtent(text.header1[0])[0]
        w1 = devListCtrl.GetColumnWidth(1)
        portCtrl.SetMinSize((w0 - 1, -1))
        prefixCtrl.SetMinSize((max(w1 - 1, 100), -1))        
        box1 = wx.StaticBox(panel, -1, "")
        leftStatSizer = wx.StaticBoxSizer(box1, wx.VERTICAL)
        leftSizer = wx.GridBagSizer(3, 1)
        leftStatSizer.Add(leftSizer, 1, wx.EXPAND|wx.TOP, 3)
        leftSizer.Add(devListCtrl, (0, 0), (5, 3), flag = wx.EXPAND)
        leftSizer.Add(delDev, (0, 3), flag = wx.TOP|wx.ALIGN_RIGHT, border = 24)
        leftSizer.Add(clearDevs, (1, 3), flag = wx.ALIGN_RIGHT)
        brdr = 2 + SYS_VSCROLL_X + devListCtrl.GetWindowBorderSize()[0]
        leftSizer.Add(btnDevUP, (2, 3), flag = wx.LEFT, border = brdr)
        leftSizer.Add(btnDevDOWN, (3, 3), flag = wx.LEFT, border = brdr)
        leftSizer.Add(portCtrl, (5, 0), flag = wx.EXPAND|wx.LEFT, border = 1)
        leftSizer.Add(prefixCtrl, (5, 1), flag = wx.EXPAND|wx.LEFT, border = 1)
        leftSizer.Add(addDev, (5, 3), flag = wx.LEFT, border = brdr)
        leftSizer.AddGrowableRow(4)
        leftSizer.AddGrowableCol(0, w0 - 1)
        leftSizer.AddGrowableCol(1, w1)
        suffixListCtrl = ListCtrl(
            panel,
            -1,
            style = wx.LC_REPORT |
                wx.VSCROLL |
                wx.LC_VRULES |
                wx.LC_HRULES |
                wx.LC_SINGLE_SEL
        )
        suffText = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY)
        suffText.SetToolTip(text.suffToolTip)
        humanText = wx.TextCtrl(panel, -1, "")
        delEvent = wx.Button(panel, -1, text.buttons[0], size = sz)
        clearEvents = wx.Button(panel, -1, text.buttons[1], size = sz)
        addEvent = wx.Button(panel, -1, text.buttons[2], size = sz)

        #Button UP
        btnUP = wx.BitmapButton(panel, -1, bmpUp)
        btnUP.Enable(False)
        #Button DOWN
        btnDOWN = wx.BitmapButton(panel, -1, bmpDown)
        btnDOWN.Enable(False)

        def FillSuffixList(lst):
            suffixListCtrl.DeleteAllItems()
            for row in range(len(lst)):
                suffixListCtrl.InsertItem(row, lst[row][0])
                suffixListCtrl.SetItem(row, 1, lst[row][1])
        w = 0
        for i, colLabel in enumerate(text.header2):
            suffixListCtrl.InsertColumn(i, colLabel)
            suffixListCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            w += suffixListCtrl.GetColumnWidth(i)
        suffixListCtrl.SetSize((
            w + SYS_VSCROLL_X + suffixListCtrl.GetWindowBorderSize()[0],
            -1
        ))
        w0 = suffixListCtrl.GetColumnWidth(0)
        w1 = suffixListCtrl.GetColumnWidth(1)
        suffText.SetMinSize((w0-1, -1))
        humanText.SetMinSize((w1-1, -1))        
        box2 = wx.StaticBox(panel, -1, "")
        rightStatSizer = wx.StaticBoxSizer(box2, wx.VERTICAL)
        rightSizer = wx.GridBagSizer(3, 1)
        rightStatSizer.Add(rightSizer, 1, wx.EXPAND|wx.TOP, 3)
        rightSizer.Add(suffixListCtrl, (0, 0), (5, 3), flag = wx.EXPAND)
        rightSizer.Add(delEvent, (0, 3), flag=wx.TOP|wx.ALIGN_RIGHT, border = 24)
        rightSizer.Add(clearEvents, (1, 3), flag = wx.ALIGN_RIGHT)
        rightSizer.Add(btnUP, (2, 3), flag = wx.LEFT, border = brdr)
        rightSizer.Add(btnDOWN, (3, 3), flag = wx.LEFT, border = brdr)
        rightSizer.Add(suffText, (5, 0), flag = wx.EXPAND|wx.LEFT, border = 1)
        rightSizer.Add(humanText, (5, 1), flag = wx.EXPAND|wx.LEFT, border = 1)
        rightSizer.Add(addEvent, (5, 3), flag = wx.LEFT, border = brdr)        
        rightSizer.AddGrowableRow(4)
        rightSizer.AddGrowableCol(0, w0)
        rightSizer.AddGrowableCol(1, w1)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(leftStatSizer, 4, wx.EXPAND)
        mainSizer.Add(rightStatSizer, 5, wx.EXPAND|wx.LEFT, 10)
        panel.sizer.Add(mainSizer, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)
        panel.dialog.buttonRow.Add(timeoutLabel, 0, ACV)
        panel.dialog.buttonRow.Add(timeoutCtrl)
        panel.sizer.Layout()

        def EnableDevCtrls(enable):
            portCtrl.Enable(enable)
            prefixCtrl.Enable(enable) 


        def EnableCtrls(enable):
            suffText.Enable(enable)
            humanText.Enable(enable) 
            if enable:
                self.suffText = suffText
            else:
                self.suffText = None


        def ResetDevCtrls():
            portCtrl.SetSelection(-1)
            prefixCtrl.ChangeValue("")


        def ResetCtrls():
            suffText.ChangeValue("")
            humanText.ChangeValue("")


        def SetWidth():
            w0 = suffText.GetSize()[0]+1
            w1 = humanText.GetSize()[0]+1
            w2 = portCtrl.GetSize()[0]+1
            w3 = prefixCtrl.GetSize()[0]+1
            suffixListCtrl.SetSize((
                w0+w1+SYS_VSCROLL_X + suffixListCtrl.GetWindowBorderSize()[0],
                -1
            ))
            suffixListCtrl.SetColumnWidth(0, w0)
            suffixListCtrl.SetColumnWidth(1, w1)
            devListCtrl.SetSize((
                w2+w3+SYS_VSCROLL_X + devListCtrl.GetWindowBorderSize()[0],
                -1
            ))
            devListCtrl.SetColumnWidth(0, w2)
            devListCtrl.SetColumnWidth(1, w3)


        def OnSize(event):
            wx.CallAfter(SetWidth)
            panel.Update()
            event.Skip()
        panel.Bind(wx.EVT_SIZE, OnSize)


        def OnDelDev(evt):
            devListCtrl.DeleteItem(self.oldDevSel)
            lngth = devListCtrl.GetItemCount()
            if lngth == 0:
                self.oldDevSel = -1
                LeftSide()
                ResetDevCtrls()
                evt.Skip()
                return
            elif self.oldDevSel == lngth:
                row = lngth - 1
            else:
                row = self.oldDevSel
            self.oldDevSel = -1
            SelDevRow(row)
            portCtrl.SetStringSelection(devListCtrl.GetItemText(row))
            prefixCtrl.ChangeValue(devListCtrl.GetItem(row, 1).GetText())
            LeftSide()
            Validation()
            evt.Skip()
        delDev.Bind(wx.EVT_BUTTON, OnDelDev)


        def OnDelEvent(evt):
            suffixListCtrl.DeleteItem(self.oldSel)
            lngth = suffixListCtrl.GetItemCount()
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
            suffText.ChangeValue(suffixListCtrl.GetItemText(row))
            humanText.ChangeValue(suffixListCtrl.GetItem(row, 1).GetText())
            RightSide()
            Validation()
            evt.Skip()
        delEvent.Bind(wx.EVT_BUTTON, OnDelEvent)


        def OnClearDevs(evt):
            devListCtrl.DeleteAllItems()
            self.oldDevSel = -1
            LeftSide()
            ResetDevCtrls()
            evt.Skip()
        clearDevs.Bind(wx.EVT_BUTTON, OnClearDevs)


        def OnClearEvents(evt):
            suffixListCtrl.DeleteAllItems()
            self.oldSel = -1
            RightSide()
            ResetCtrls()
            evt.Skip()
        clearEvents.Bind(wx.EVT_BUTTON, OnClearEvents)


        def EnableButtonsLeft(enable):
            delDev.Enable(enable)
            btnDevUP.Enable(enable)
            btnDevDOWN.Enable(enable)        


        def EnableButtonsRight(enable):
            delEvent.Enable(enable)
            btnUP.Enable(enable)
            btnDOWN.Enable(enable)        


        def LeftSide():           
            devListCtrl.Enable(True)
            lngth = devListCtrl.GetItemCount()
            if lngth == 0:
                addDev.Enable(True)
                EnableButtonsLeft(False)
                clearDevs.Enable(False)
                EnableDevCtrls(False)
            elif lngth > 0:
                clearDevs.Enable(True)
                if self.oldDevSel != -1:
                    EnableButtonsLeft(True)
                    EnableDevCtrls(True)
                else:
                    EnableButtonsLeft(False)
                    EnableDevCtrls(False)


        def RightSide():   
            suffixListCtrl.Enable(True)
            lngth = suffixListCtrl.GetItemCount()
            if lngth == 0:
                addEvent.Enable(True)
                EnableButtonsRight(False)
                clearEvents.Enable(False)
                EnableCtrls(False)
            elif lngth > 0:
                clearEvents.Enable(True)
                if self.oldSel != -1:
                    EnableButtonsRight(True)
                    EnableCtrls(True)
                else:
                    EnableButtonsRight(False)
                    EnableCtrls(False)


        def Validation():
            flag = True
            strng = suffText.GetValue()
            newSuff = humanText.GetValue()
            data = suffixListCtrl.GetData()
            if suffText.IsEnabled() and strng == "":
                flag = False
            if humanText.IsEnabled() and newSuff == "":
                flag = False
            for item in data:
                if item[0] == strng and item[1] != newSuff:
                    flag = False
                    break
            tmp = [i[0] for i in data]
            cnt = tmp.count(strng)
            if cnt > 1:
                suffixListCtrl.SetItem(self.oldSel, 0, "")
                suffText.ChangeValue("")
                flag = False
                MessageBox(
                    panel,
                    text.message2 % (strng),
                    text.messBoxTit1,
                    wx.ICON_EXCLAMATION,
                    plugin = self,
                    time = 15
                    )
            addEvent.Enable(flag)
            flag2 = True
            strng = portCtrl.GetStringSelection()
            newPref = prefixCtrl.GetValue()
            data = devListCtrl.GetData()
            if portCtrl.IsEnabled() and strng == "":
                flag2 = False
            if prefixCtrl.IsEnabled() and newPref == "":
                flag2 = False
            for item in data:
                if item[0] == strng and item[1] != newPref:
                    flag2 = False
                    break
            tmp = [i[0] for i in data]
            cnt = tmp.count(strng)
            if cnt > 1:
                devListCtrl.SetItem(self.oldDevSel, 0, "")
                portCtrl.SetSelection(-1)
                flag2 = False
                MessageBox(
                    panel,
                    text.message1 % (strng),
                    text.messBoxTit1,
                    wx.ICON_EXCLAMATION,
                    plugin = self,
                    time = 15
                    )
            addDev.Enable(flag2)
            panel.dialog.buttonRow.okButton.Enable(flag and flag2)
            

        def OnButtonAddDev(evt):
            if self.oldDevSel == -1:
                self.oldDevSel = devListCtrl.GetItemCount() - 1
            row = self.oldDevSel + 1
            devListCtrl.InsertItem(row, "")
            devListCtrl.SetItem(row, 1, "")
            devListCtrl.EnsureVisible(row)
            SelDevRow(row)
            EnableDevCtrls(True)
            addDev.Enable(False)
            clearDevs.Enable(True)
            panel.dialog.buttonRow.okButton.Enable(False)
            ResetDevCtrls()
            EnableButtonsLeft(True)
            evt.Skip()
        addDev.Bind(wx.EVT_BUTTON, OnButtonAddDev)
        

        def OnButtonAddEvent(evt):
            if self.oldSel == -1:
                self.oldSel = suffixListCtrl.GetItemCount() - 1
            row = self.oldSel + 1
            suffixListCtrl.InsertItem(row, "")
            suffixListCtrl.SetItem(row, 1, "")
            suffixListCtrl.EnsureVisible(row)
            SelRow(row)
            EnableCtrls(True)
            addEvent.Enable(False)
            clearEvents.Enable(True)
            panel.dialog.buttonRow.okButton.Enable(False)
            ResetCtrls()
            EnableButtonsRight(True)
            evt.Skip()
        addEvent.Bind(wx.EVT_BUTTON, OnButtonAddEvent)
        

        def OnPortCtrl(evt):
            strng = evt.GetString()
            devListCtrl.SetItem(self.oldDevSel, 0, strng)
            Validation()
            evt.Skip()
        portCtrl.Bind(wx.EVT_CHOICE, OnPortCtrl)


        def OnSuffText(evt):
            strng = evt.GetString()
            suffixListCtrl.SetItem(self.oldSel, 0, strng)
            Validation()
            evt.Skip()
        suffText.Bind(wx.EVT_TEXT, OnSuffText)


        def OnHumanText(evt):
            strng = humanText.GetValue()
            suffixListCtrl.SetItem(self.oldSel, 1, strng)
            Validation()
            evt.Skip()
        humanText.Bind(wx.EVT_TEXT, OnHumanText)


        def OnPrefixCtrl(evt):
            strng = prefixCtrl.GetValue()
            devListCtrl.SetItem(self.oldDevSel, 1, strng)
            Validation()
            evt.Skip()
        prefixCtrl.Bind(wx.EVT_TEXT, OnPrefixCtrl)


        def SelDevRow(row):
            if row != self.oldDevSel:
                if self.oldDevSel in range(devListCtrl.GetItemCount()):
                    item = devListCtrl.GetItem(self.oldDevSel)
                    item.SetTextColour(self.fore)
                    item.SetBackgroundColour(self.back)
                    devListCtrl.SetItem(item)
                self.oldDevSel = row
            if devListCtrl.GetItemBackgroundColour(row) != self.selBack:
                item = devListCtrl.GetItem(row)
                item.SetTextColour(self.selFore)
                item.SetBackgroundColour(self.selBack)
                devListCtrl.SetItem(item)


        def SelRow(row):
            if row != self.oldSel:
                if self.oldSel in range(suffixListCtrl.GetItemCount()):
                    item = suffixListCtrl.GetItem(self.oldSel)
                    item.SetTextColour(self.fore)
                    item.SetBackgroundColour(self.back)
                    suffixListCtrl.SetItem(item)
                self.oldSel = row
            if suffixListCtrl.GetItemBackgroundColour(row) != self.selBack:
                item = suffixListCtrl.GetItem(row)
                item.SetTextColour(self.selFore)
                item.SetBackgroundColour(self.selBack)
                suffixListCtrl.SetItem(item)


        def OnDevSelect(evt):
            row = evt.GetIndex()
            devListCtrl.SetItemState(row, 0, wx.LIST_STATE_SELECTED)
            if row == self.oldDevSel:
                evt.Skip()            
                return                
            if not addDev.IsEnabled() and self.oldDevSel > -1:
                old = self.oldDevSel
                self.oldDevSel = row
                SelDevRow(old)
                PlaySound('SystemExclamation', SND_ASYNC)
                evt.Skip()            
                return
            EnableDevCtrls(True)
            SelDevRow(row)
            EnableButtonsLeft(True)
            portCtrl.SetStringSelection(devListCtrl.GetItemText(row))
            prefixCtrl.ChangeValue(devListCtrl.GetItem(row, 1).GetText())
            evt.Skip()            
        devListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, OnDevSelect)


        def OnSuffixSelect(evt):
            row = evt.GetIndex()
            suffixListCtrl.SetItemState(row, 0, wx.LIST_STATE_SELECTED)
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
            EnableButtonsRight(True)
            suffText.ChangeValue(suffixListCtrl.GetItemText(row))
            humanText.ChangeValue(suffixListCtrl.GetItem(row, 1).GetText())
            evt.Skip()            
        suffixListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, OnSuffixSelect)


        def onButtonDevUp(evt):
            newSel, devs = Move(devListCtrl.GetData(), self.oldDevSel, -1)
            FillDevList(devs)
            SelDevRow(newSel)
            devListCtrl.EnsureVisible(self.oldDevSel)
            evt.Skip()
        btnDevUP.Bind(wx.EVT_BUTTON, onButtonDevUp)


        def onButtonDevDown(evt):
            newSel, devs = Move(devListCtrl.GetData(), self.oldDevSel, 1)
            FillDevList(devs)
            SelDevRow(newSel)
            devListCtrl.EnsureVisible(self.oldDevSel)
            evt.Skip()
        btnDevDOWN.Bind(wx.EVT_BUTTON, onButtonDevDown)


        def onButtonUp(evt):
            newSel, suffixes = Move(suffixListCtrl.GetData(), self.oldSel, -1)
            FillSuffixList(suffixes)
            SelRow(newSel)
            suffixListCtrl.EnsureVisible(self.oldSel)
            evt.Skip()
        btnUP.Bind(wx.EVT_BUTTON, onButtonUp)


        def onButtonDown(evt):
            newSel, suffixes = Move(suffixListCtrl.GetData(), self.oldSel, 1)
            FillSuffixList(suffixes)
            SelRow(newSel)
            suffixListCtrl.EnsureVisible(self.oldSel)
            evt.Skip()
        btnDOWN.Bind(wx.EVT_BUTTON, onButtonDown)

        FillDevList(devices)
        LeftSide()
        ResetDevCtrls()
        FillSuffixList(suffixes)
        RightSide()
        ResetCtrls()

        def OnCloseBox(evt):
            self.suffText = None
            evt.Skip()
        panel.dialog.Bind(wx.EVT_CLOSE, OnCloseBox)
        panel.dialog.buttonRow.cancelButton.Bind(wx.EVT_BUTTON, OnCloseBox)

        while panel.Affirmed():
            panel.SetResult(
            timeoutCtrl.GetValue(),
            devListCtrl.GetData(),
            suffixListCtrl.GetData()
            )
#===============================================================================

class MessageBox(wx.Dialog):

    def __init__(
        self,
        parent,
        message,
        caption = '',
        flags = 0,
        time = 0,
        plugin = None
    ):
        PlaySound('SystemExclamation', SND_ASYNC)
        wx.Dialog.__init__(self, parent, style = wx.DEFAULT_DIALOG_STYLE )
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
                bmp = wx.ArtProvider.GetBitmap(art, wx.ART_MESSAGE_BOX, (32,32))
                icon = wx.StaticBitmap(self, -1, bmp)
                icon2 = wx.StaticBitmap(self, -1, bmp)
            else:
                icon = (32, 32)
                icon2 = (32, 32)
        if caption:
            caption = wx.StaticText(self, -1, caption)
            caption.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD))
        message = wx.StaticText(self, -1, message)
        line = wx.StaticLine(self, -1, size = (1, -1), style = wx.LI_HORIZONTAL)
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
        bottomSizer.Add((1,1),1,wx.EXPAND) 
        bottomSizer.Add(button, 0, wx.RIGHT, 10)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(icon,0,wx.LEFT|wx.RIGHT,10)
        topSizer.Add((1,1),1,wx.EXPAND)
        topSizer.Add(caption,0,wx.TOP,5)
        topSizer.Add((1,1),1,wx.EXPAND)
        topSizer.Add(icon2,0,wx.LEFT|wx.RIGHT,10)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 0, wx.EXPAND|wx.TOP|wx.BOTTOM,10)
        mainSizer.Add(message, 0, wx.EXPAND|wx.LEFT|wx.RIGHT,10)
        mainSizer.Add(line, 0, wx.EXPAND|wx.ALL,5)
        mainSizer.Add(bottomSizer, 0, wx.EXPAND|wx.BOTTOM,5)
        
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
#===============================================================================

