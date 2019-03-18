# -*- coding: utf-8 -*-
#
# plugins/Netio/__init__.py
#
# Copyright (C) 2014 Pako
#
# This file is a plugin for EventGhost.
# Copyright (C) 2005-2012 Lars-Peter Voss <bitmonster@eventghost.org>
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

# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.0 by Pako 2014-04-13 11:28 UTC+1
#     - initial version
#===============================================================================

eg.RegisterPlugin(
    name = "Netio",
    author = "Pako",
    version = "0.0",
    kind = "external",
    guid = "{C5A40E2D-7336-414C-9E91-75CD30A17E4C}",
    canMultiLoad = False,
    createMacrosOnAdd = True,
    description = ur"""<rst>
Adds actions to control smart sockets `KOUKAAM Netio`__.

__ http://www.koukaam.se/kkm/products.php?cat_id=19
""",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAC/VBMVEXmYXDtj5riQVPa"
        "ESnYAhvfMUbmYHHwn6jvn6n3z9Trf4vfMUX3z9PmYHD30NThQlTwoKnyr7fdIjjwn6nj"
        "UWLzr7frgIziQVTwoKr40NT////1wMbsgY3nYXHaEinpcX/97/HcITfzsLj0v8XmYXHy"
        "sLfZESn63+PukJv1zdPeMEXunqj8/P3qf4zocH7zvcTrjZn1zdLcITblYHDpf4zwrbbp"
        "f4vhQVPgQVPunab0zNHpfYvjT2HgQFPnb33unafyvMPpfovjUGHvrbXgQFLxu8LkX2/u"
        "qrTsm6bnfIruq7PhTmDwyM7ZECjqmqXx19vjXW3uucDtuL/meojfP1LdL0Tme4jsqLIA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkMeg4AAAAAXRS"
        "TlMAQObYZgAAANdJREFUOMtjYKAfYGJmYWFhY8clywIHXNjkWVAAH4Y8L6oCZk68+kEA"
        "VV4QU4EQLgdiNYKRhYACbAawiOJyoriElLQMkJbFoUBSCgwkWPhxKJCCAhQFihgGSEnJ"
        "iyEp4IDLs8LkpaSxB6Q4DgUMqFZIAxmqOBTIgxTIYMQFgyZchQJQgQIrixZGfKvBzQDa"
        "osSgz2KApsAQOTCMGUxYWBQxDIEFhyXMUca4k68BVK2aAQ4FTnDbnLErQHaQG8E07kEw"
        "E2BR4B+AJB+I1RVBASFgWe9wIvIsAKCsFHTth32AAAAAAElFTkSuQmCC"
    ),
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=6109"
)
#===============================================================================

import eg
import wx
from telnetlib import Telnet as tlTt
from socket import socket as s_socket
from socket import error as sock_error
from socket import AF_INET, SOCK_STREAM
from wx.lib.mixins.listctrl import CheckListCtrlMixin
from copy import deepcopy as cpy
from time import time as ttime
from threading import Thread

ACV = wx.ALIGN_CENTER_VERTICAL
SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
#===============================================================================

class myPassword(eg.Password):
    pass
#===============================================================================

def iI_tlTt(tc):
    return isinstance(tc, tlTt)


def quitTc(tc):
    try:
        tc.write("quit\r\n")
    except:
        pass
#===============================================================================

class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin):

    def __init__(self, parent, header, rows, plugin):
        wx.ListCtrl.__init__(
            self,
            parent,
            -1,
            style = wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|wx.LC_SINGLE_SEL
        )
        self.rows = rows
        self.plugin = plugin
        self.psswds = []
        self.guids = []
        self.selRow = -1
        self.back = self.GetBackgroundColour()
        self.fore = self.GetForegroundColour()
        self.selBack = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.selFore = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        self.wk = SYS_VSCROLL_X+self.GetWindowBorderSize()[0]
        self.collens = []
        hc = len(header)
        for i in range(hc):
            self.InsertColumn(i, header[i])
        for i in range(hc):
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            w = self.GetColumnWidth(i)
            self.collens.append(w)
            self.wk += w
        self.InsertItem(0, "dummy")
        rect = self.GetItemRect(0, wx.LIST_RECT_BOUNDS)
        hh = rect[1] #header height
        hi = rect[3] #item height
        self.DeleteAllItems()
        self.SetMinSize((self.wk, 5 + hh + rows * hi))
        self.SetSize((self.wk, 5 + hh + rows * hi))
        self.Layout()
        CheckListCtrlMixin.__init__(self)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_SIZE, self.OnSize)


    def SetWidth(self):
        newW = self.GetSize().width
        p = newW/float(self.wk)
        col = self.GetColumnCount()
        w = SYS_VSCROLL_X + self.GetWindowBorderSize()[0]+self.GetColumnWidth(0)
        for c in range(1, col-1):
            self.SetColumnWidth(c, p*self.collens[c])
            w += self.GetColumnWidth(c)
        self.SetColumnWidth(col-1, newW-w)


    def OnSize(self, event):
        wx.CallAfter(self.SetWidth)
        event.Skip()


    def OnItemSelected(self, evt):
        self.SelRow(evt.GetSelection())
        evt.Skip()


    # this is called by the base class when an item is checked/unchecked !!!!!!!
    def OnCheckItem(self, index, flag):
        evt = eg.ValueChangedEvent(self.GetId(), value = (index, flag))
        wx.PostEvent(self, evt)


    def SelRow(self, row):
        if row != self.selRow:
            if self.selRow in range(self.GetItemCount()):
                item = self.GetItem(self.selRow)
                item.SetTextColour(self.fore)
                item.SetBackgroundColour(self.back)
                self.SetItem(item)
            self.selRow = row
        if self.GetItemBackgroundColour(row) != self.selBack:
            item = self.GetItem(row)
            item.SetTextColour(self.selFore)
            item.SetBackgroundColour(self.selBack)
            self.SetItem(item)
            self.SetItemState(row, 0, wx.LIST_STATE_SELECTED)


    def DeleteRow(self):
        row = self.selRow
        if row > -1:
            self.psswds.pop(row)
            self.guids.pop(row)
            self.DeleteItem(row)
            row = row if row < self.GetItemCount() else self.GetItemCount() - 1
            if row > -1:
                self.SelRow(row)
            else:
                self.selRow = -1
                evt = eg.ValueChangedEvent(self.GetId(), value="Empty")
                wx.PostEvent(self, evt)


    def AppendRow(self):
        ix = self.GetItemCount()
        self.InsertItem(ix, "")
        self.CheckItem(ix)
        self.EnsureVisible(ix)
        self.SelRow(ix)
        self.psswds.append("")
        self.guids.append("")
        if ix == 0:
            evt = eg.ValueChangedEvent(self.GetId(), value="One")
            wx.PostEvent(self, evt)


    def SetRow(self, rowData, passw):
        row = self.selRow
        if rowData[0]:
            self.CheckItem(row)
        elif self.IsChecked(row):
            self.ToggleItem(row)
        for i in range(1, 6):
            if i != 5:
                self.SetItem(row, i, rowData[i])
            else:
                self.psswds[row]=passw
                self.guids[row]=rowData[i]
                self.SetItem(row, i, 7 * u"\u2022")


    def GetSelectedItemIx(self):
        return self.selRow


    def GetRow(self, row = None):
        row = self.selRow if row is None else row
        rowData=[]
        rowData.append(self.IsChecked(row))
        for i in range(1, self.GetColumnCount()):
            if i != 5:
                rowData.append(self.GetItem(row, i).GetText())
            else:
                rowData.append(self.guids[row])
        return (rowData, self.psswds[row])


    def GetData(self):
        data = []
        psswds = []
        for row in range(self.GetItemCount()):
            rowData, psswd = self.GetRow(row)
            data.append(rowData)
            psswds.append(psswd)
        return (data, psswds)


    def SetData(self, data, psswds):
        if data:
            self.psswds = psswds
            for row in range(len(data)):
                self.AppendRow()
                self.SetRow(data[row], psswds[row])
            self.SelRow(0)
            self.EnsureVisible(0)
#===============================================================================

class extDialog(wx.Frame):
    def __init__(
        self,
        parent,
        plugin,
        labels,
        data,
        grid,
        add=False,
    ):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style = wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL|wx.RESIZE_BORDER,
            name="NetioExtDialog"
        )
        self.panel = parent
        self.plugin = plugin
        self.text = plugin.text
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.labels = labels
        self.passw = data[1]
        self.data = data[0]
        self.grid = grid
        self.add = add
        self.passRow = 5


    def ShowExtDialog(self, title):
        self.panel.Enable(False)
        self.panel.dialog.buttonRow.cancelButton.Enable(False)
        self.panel.EnableButtons(False)
        self.SetTitle(title)
        text = self.plugin.text
        panel = wx.Panel(self)

        def wxst(label):
            return wx.StaticText(panel, -1, label)

        labels = self.labels
        data = self.data
        rows = len(labels)
        sizer = wx.FlexGridSizer(rows-1, 2, 5, 5)
        sizer.AddGrowableCol(1)
        for row in range(1, rows):
            sizer.Add(wxst(labels[row]), 0, ACV)
            if row != self.passRow:
                txtCtrl = wx.TextCtrl(panel, -1, data[row])
            else:
                txtCtrl = wx.TextCtrl(
                    panel,
                    -1,
                    self.passw,
                    style = wx.TE_PASSWORD
                )
            sizer.Add(txtCtrl,0,wx.EXPAND)

        line = wx.StaticLine(
            panel,
            -1,
            style = wx.LI_HORIZONTAL
        )
        btn1 = wx.Button(panel, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn2 = wx.Button(panel, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sizer,1,wx.ALL|wx.EXPAND,5)
        mainSizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
        mainSizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        mainSizer.Add((1,6))
        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)


        def onClose(evt):
            self.MakeModal(False)
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)


        def onOk(evt):
            if self.add:
                self.grid.AppendRow()
            data=[self.data[0]]
            children = sizer.GetChildren()
            for child in range(1,len(children),2):
                ctrl=children[child].GetWindow()
                val = ctrl.GetValue()
                if child != 2 * self.passRow - 1:
                    data.append(val)
                else:
                    data.append(self.data[5])
                    passw = val
            self.grid.SetRow(data, passw)
            self.Close()
        btn1.Bind(wx.EVT_BUTTON, onOk)


        def onCancel(evt):
            self.Close()
        btn2.Bind(wx.EVT_BUTTON, onCancel)

        mainSizer.Layout()
        w, h = self.GetSize()
        self.SetSize((max(w, 400), h))
        self.SetMinSize((max(w, 400), h))
        self.Raise()
        self.MakeModal(True)
        self.Show()

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler

#===============================================================================

class infDialog(wx.Frame):
    def __init__(
        self,
        plugin,
        parent,
        ix,
        grid
    ):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style = wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL|wx.RESIZE_BORDER,
            name="NetioPlugin_InfoDialog",
        )
        self.SetBackgroundColour(wx.BLACK)
        self.parent = parent
        self.plugin = plugin
        self.text = plugin.text
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.ix = ix
        self.SetTitle(self.text.title4 % grid.GetRow(ix)[0][1])

        demoData = len(self.text.labels) * ["",]
        demoData[3] = "0 years 364 days 23 hours 59 min 59 sec"
        self.ShowInfo(demoData)
        mainSizer = self.panel.GetSizer()
        mainSizer.Fit(self)
        size = self.GetSize()
        self.SetMinSize(size)
        self.SetSize(size)
        self.onRefresh()


    def ShowInfo(self, data):
        text = self.text
        if hasattr(self, "panel"):
            mainSizer = self.panel.GetSizer()
            mainSizer.Clear(True)
            panel = self.panel
            panel.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
            flag = True
        else:
            panel = wx.Panel(self)
            self.panel = panel
            panel.SetBackgroundColour(wx.BLACK)
            panel.SetForegroundColour(wx.Colour(255,255,0))
            mainSizer = wx.BoxSizer(wx.VERTICAL)
            panel.SetSizer(mainSizer)
            flag =False


        def StaticText(txt, bold = False):
            st = wx.StaticText(panel, -1, txt, pos = ((0,-50)))
            if flag:
                st.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
            font = st.GetFont()
            if bold:
                font.SetWeight(wx.FONTWEIGHT_BOLD )
            st.SetFont(font)
            return st

        intSizer = wx.GridBagSizer(8, 20)
        mainSizer.Add(intSizer,1,wx.ALL|wx.EXPAND,5)
        labels = text.labels
        for i in range(len(labels)):
            intSizer.Add(StaticText(labels[i]+":", True),(i,0))
            intSizer.Add(StaticText(data[i]),(i,1))
        mainSizer.Layout()


    def onOK(self, evt):
        self.Close()
        evt.Skip()


    def onRefresh(self, evt = None):
        self.panel.GetSizer().Clear(True)
        self.waitForData(evt is None)
        eg.scheduler.AddTask(0.01, self.plugin.GetInfo, self.ix)
        if evt:
            evt.Skip()


    def onCopy(self, evt):
        eg.scheduler.AddTask(0.01, self.plugin.onCopy)
        evt.Skip()


    def OnRightClick(self, event):
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewIdRef()
            self.popupID2 = wx.NewIdRef()
            self.popupID3 = wx.NewIdRef()
            self.Bind(wx.EVT_MENU, self.onOK, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.onRefresh, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.onCopy, id=self.popupID3)
        menu = wx.Menu()
        menu.Append(self.popupID1, self.text.popup[0])
        menu.Append(self.popupID2, self.text.popup[1])
        menu.Append(self.popupID3, self.text.popup[2])
        self.PopupMenu(menu)
        menu.Destroy()


    def waitForData(self, flag):
        self.parent.Enable(False)
        self.parent.dialog.buttonRow.cancelButton.Enable(False)
        self.parent.EnableButtons(False)
        panel = self.panel
        mainSizer = self.panel.GetSizer()
        waitLabel=wx.StaticText(panel, -1, self.text.collect)
        mainSizer.Add(waitLabel,0,wx.LEFT|wx.TOP,5)
        mainSizer.Layout()
        if flag:
            self.Raise()
            self.MakeModal(True)
            self.Show()


        def onClose(evt):
            self.MakeModal(False)
            self.parent.Enable(True)
            self.parent.dialog.buttonRow.cancelButton.Enable(True)
            self.parent.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler

#===============================================================================

class Text:
    label1="List of Netio devices:"
    header1 = (
        "Enabled",
        "Name/Event",
        "IP address        ",
        "Port",
        "Username",
        "Password",
    )
    buttons1 = (
        "Add new",
        "Duplicate",
        "Edit",
        "Delete",
        "Show info",
    )
    title1 = "Netio detail"
    title4 = 'Netio "%s" detail'
    cancel = "Cancel"
    ok = "OK"
    period = "Polling period [s]:"
    prefix = "Event prefix:"
    notAcc = 'Netio "%s" is not accessible !'
    warn = "Warning"
    collect = "Data collection in progress. Please wait ..."
    labels = (
        "Alias",
        "Version",
        "MAC address",
        "Uptime",
        "System time",
        "Timezone",
        "Swdelay",
        "States of sockets",
    )
    popup = (
        "Close",
        "Refresh",
        "Copy to clipboard"
    )
    states = ("OFF","ON")
    chooseLbl = "Select Netio device by:"
    chooses = ("Name", "IP address")
    nioLbl = "Netio:"
    unknown = 'Unknown Netio: "%s"'
    sock = "Socket:"
    state = "Turn (0=OFF, 1=ON):"
    parsErr = 'Parsing error for "%s"'
    tryConn = 'Trying to connect with Netio "%s"'
    unexp = 'Unexpected result: %s'
    noConn = 'No connection with "%s"'
#===============================================================================

def isAlive(host, port):
    try:
        sock = s_socket(AF_INET, SOCK_STREAM)
        sock.settimeout(0.2)
        sock.connect((host,port))
        sock.close()
        return True
    except:
        return False
#===============================================================================

class Netio(eg.PluginBase):

    text = Text
    result = None
    dialog = None
    poll = None
    telnets = None


    def parseArgument(self, arg):
        if isinstance(arg, int):
            return arg
        try:
            tmp = eg.ParseString(arg)
        except:
            pass
        try:
            tmp = eval(tmp)
            tmp = int(tmp)
        except:
            pass
        if not isinstance(tmp, int):
            eg.PrintError(self.text.parsErr % str(arg))
            return None
        return tmp


    def __init__(self):
        self.AddActionsFromList(ACTIONS)
        

    def closeTc(self, tc, ix):
        self.telnets[ix] = None
        if iI_tlTt(tc):
            quitTc(tc)
            try:
                tc.close()
            except:
                pass
        return None


    def createPollConn(self, nio, ix):
        if not self.info.isStarted:
            return

        if not isAlive(nio[2], int(nio[3])):
            tc = self.telnets[ix]
            self.telnets[ix] = None
            if iI_tlTt(tc):
                try:
                    tc.close()
                except:
                    pass
            return            
        print self.text.tryConn % nio[1]   
        
        tc = tlTt()
        try:
            tc.open(nio[2], int(nio[3]), 1)
        except:           
            self.telnets[ix] = None
            try:
                tc.close()
            except:
                pass
            return
        resp = tc.read_until('100 HELLO ',1)
        if not '100 HELLO ' in resp:
            self.telnets[ix] = None
            return self.closeTc(tc, ix)
        resp = tc.read_very_eager()
        if not ' - KSHELL V' in resp:
            return self.closeTc(tc, ix)
        tc.write(str("login %s %s\r\n" % (nio[4], myPassword(nio[5]).Get())))
        resp = tc.read_until('250 ',1)
        if not '250 ' in resp:
            return self.closeTc(tc, ix)
        resp = tc.read_very_eager()
        if not resp == 'OK\r\n':
            return self.closeTc(tc, ix)
        eg.TriggerEvent(
            "Ready",
            prefix = "%s-%s" % (
                self.info.eventPrefix,
                self.nios[ix][1].replace(" ","_")),
            payload = self.nios[ix][1]
            )
        self.telnets[ix] = tc


    def createConn(self, nio, ix):
        if not self.info.isStarted:
            return None

        if not isAlive(nio[2], int(nio[3])):
            tc = self.telnets[ix]
            return self.closeTc(tc, ix)        
        tc = tlTt()
        try:
            tc.open(nio[2], int(nio[3]), 2)
        except:
            return self.closeTc(tc, ix)
        resp = tc.read_until('100 HELLO ',1)
        if not '100 HELLO ' in resp:
            return self.closeTc(tc, ix)
        resp = tc.read_very_eager()
        if not ' - KSHELL V' in resp:
            return self.closeTc(tc, ix)
        tc.write(str("login %s %s\r\n" % (nio[4], myPassword(nio[5]).Get())))
        resp = tc.read_until('250 ',1)
        if not '250 ' in resp:
            return self.closeTc(tc, ix)
        resp = tc.read_very_eager()
        if not resp == 'OK\r\n':
            return self.closeTc(tc, ix)
        return tc


    def GetPasswords(self, content, nios):
        myPassword.SetDatabaseContent(content)
        passwds = []
        for ix, nio in enumerate(nios):
            passwds.append(myPassword(nio[5]).Get())
        return passwds
        

    def __start__(
        self,
        nios=[],
        prefix="Netio",
        period = 5,
        content = ""
    ):
        myPassword.SetDatabaseContent(content)    
        self.nios = nios
        self.states = len(self.nios)*[[]]
        self.telnets = len(self.nios)*[None]
        self.info.eventPrefix = prefix
        self.period = period
        t = int(ttime())
        ct = 10-t%10
        t = t + ct
        self.poll = eg.scheduler.AddTask(0.01, self.polling, t)


    def __stop__(self):
        if self.poll:
            try:
                eg.scheduler.CancelTask(self.poll)
            except:
                pass
        for tc in self.telnets:
            if iI_tlTt(tc):
                quitTc(tc)
                tc.close()
        self.telnets = None


    def polling(self, oldT):
        if not self.info.isStarted:
            return
        per = self.period
        newT = oldT + per if ttime() - oldT < per / 2 else oldT + 2 * per
        self.poll = eg.scheduler.AddTaskAbsolute(newT, self.polling, newT)
        for ix, tc in enumerate(self.telnets):
            if not self.nios[ix][0]: # not enabled
                continue
            if tc is None:
                self.telnets[ix] = "Start"
                if self.info.isStarted:
                    connThread = Thread(
                        target = self.createPollConn,
                        args = (self.nios[ix],ix)
                    )
                    connThread.start()                
                    continue
                else:
                    return
            if not iI_tlTt(tc):
                continue
            try:
                tc.write("port list\r\n")
                resp = tc.read_until('250 ',1)
                if not '250 ' in resp:
                    self.closeTc(tc, ix)
                    self.unreachableEvent(ix)
                    continue
                resp = tc.read_very_eager()
                if len(resp) == 6 and resp.endswith('\r\n'):
                    states = resp[:4]
                    if self.states[ix] == []:
                        self.states[ix] = states
                    elif states != self.states[ix]:
                        for s in range(4):
                            if states[s] != self.states[ix][s]:
                                iS = int(states[s])
                                eg.TriggerEvent("SocketStateChanged.%s-%s" % (
                                    str(s+1),
                                    self.text.states[iS]
                                ), prefix = "%s-%s" % (
                                    self.info.eventPrefix,
                                    self.nios[ix][1].replace(" ","_")
                                ), payload = (s+1,iS))
                        self.states[ix] = states
                else:
                    eg.PrintError(self.text.unexp % repr(resp))
            except sock_error as se:
                if iI_tlTt(tc) and se.errno == 10054:
                    self.telnets[ix] = None
                    self.unreachableEvent(ix)
            except Exception,  exc:
                if iI_tlTt(tc):
                    self.telnets[ix] = None
                    eg.TriggerEvent(
                        "UnknownException",
                        prefix = "%s-%s" % (
                            self.info.eventPrefix,
                            self.nios[ix][1].replace(" ","_")),
                        payload = (
                            self.nios[ix][1],
                            exc[1].decode(eg.systemEncoding))
                        )             


    def unreachableEvent(self, ix):
        eg.TriggerEvent(
            "Unreachable",
            prefix = "%s-%s" % (
                self.info.eventPrefix,
                self.nios[ix][1].replace(" ","_")),
            payload = self.nios[ix][1]
        )    


    def enableNio(self, ix, enable):
        self.nios[ix][0] = enable
        if not enable:
            tc = self.telnets[ix]
            if iI_tlTt(tc):
                quitTc(tc)
                tc.close()
            self.telnets[ix] = None
        return bool(self.nios[ix][0])


    def GetValues(self, ix):
        data = len(self.text.labels) * ["???"]
        nio = self.nio_grid.GetData()[0][ix]
        tc = self.createConn(nio,ix)
        if not iI_tlTt(tc):
            eg.PrintNotice(self.text.notAcc % nio[1])
            return data
        tc.write("alias\r\n")
        resp = tc.read_until("250 ",1)
        if not '250 ' in resp:
            return data
        resp = tc.read_very_eager()
        data[0] = resp[1:11]
        tc.write("version\r\n")
        resp = tc.read_until("250 ",1)
        if not '250 ' in resp:
            return data
        resp = tc.read_very_eager()
        data[1] = resp[:-2]
        tc.write("system mac\r\n")
        resp = tc.read_until("250 ",1)
        if not '250 ' in resp:
            return data
        resp = tc.read_very_eager()
        data[2] = resp[:-2]
        tc.write("uptime\r\n")
        resp = tc.read_until("250 ",1)
        if not '250 ' in resp:
            return data
        resp = tc.read_very_eager()
        data[3] = resp[:-2]
        tc.write("system time\r\n")
        resp = tc.read_until("250 ",1)
        if not '250 ' in resp:
            return data
        resp = tc.read_very_eager()
        data[4] = "%s %s" % (resp[:11], resp[11:-2])
        tc.write("system timezone\r\n")
        resp = tc.read_until("250 ",1)
        if not '250 ' in resp:
            return data
        resp = tc.read_very_eager()
        data[5] = resp[:-2]
        tc.write("system swdelay\r\n")
        resp = tc.read_until("250 ",1)
        if not '250 ' in resp:
            return data
        resp = tc.read_very_eager()
        data[6] = "%i ms" % (100 * int(resp[:-2]))
        tc.write("port list\r\n")
        resp = tc.read_until("250 ",1)
        if not '250 ' in resp:
            return data
        resp = tc.read_very_eager()
        data[7] = resp[:-2]
        tc.write("quit\r\n")
        tc.close()
        return data


    def GetInfo(self, ix):
        data = self.GetValues(ix)
        self.data = data
        eg.scheduler.AddTask(0.01, self.dataReady, data)


    def dataReady(self, data):
        wx.CallAfter(self.dialog.ShowInfo, data)
        return True


    def onCopy(self):
        clipData = ""
        for i in range(len(self.text.labels)):
            clipData+="%s\t%s\n" %(self.text.labels[i]+":", self.data[i])
        eg.plugins.System.SetClipboard(clipData)


    def Configure(
        self,
        nios=[],
        prefix="Netio",
        period = 5,
        content = ""
        ):
        passwds = self.GetPasswords(content, nios)
        if nios != []:
            pass #DODELAT   
        panel = eg.ConfigPanel()
        panel.GetParent().GetParent().SetIcon(self.info.icon.GetWxIcon())
        label1 = wx.StaticText(panel, -1, self.text.label1)
        nio_grid = CheckListCtrl(panel, self.text.header1, 3, self)
        self.nio_grid = nio_grid
        nio_grid.SetData(nios, passwds)


        def enableButtons1(enable):
            for b in range(1, len(self.text.buttons1)):
                wx.FindWindowById(bttns[b]).Enable(enable)


        def OnGridChange1(evt):
            value = evt.GetValue()
            if value == "Empty":
                enableButtons1(False)
            elif value == "One":
                enableButtons1(True)
            evt.Skip()
        nio_grid.Bind(eg.EVT_VALUE_CHANGED, OnGridChange1)


        def edit1():
            dlg = extDialog(
                parent = panel,
                plugin = self,
                labels = self.text.header1,
                data=nio_grid.GetRow(),
                grid=nio_grid,
            )
            dlg.Centre()
            wx.CallAfter(
                dlg.ShowExtDialog,
                self.text.title1,
            )


        def OnActivated1(evt):
            edit1()
            evt.Skip()
        nio_grid.Bind(wx.EVT_LIST_ITEM_ACTIVATED, OnActivated1)


        def onButton(evt):
            id = evt.GetId()
            if id == bttns[0]: #Add
                dlg = extDialog(
                    parent = panel,
                    plugin = self,
                    labels = self.text.header1,
                    data=([True,"","","1234","admin",myPassword(None).guid],""),
                    grid=nio_grid,
                    add=True,
                )
                dlg.Centre()
                wx.CallAfter(
                    dlg.ShowExtDialog,
                    self.text.title1,
                )
            elif id == bttns[1]: #Duplicate
                data = list(nio_grid.GetRow())
                data[0][5] = myPassword(None).guid
                dlg = extDialog(
                    parent = panel,
                    plugin = self,
                    labels = self.text.header1,
                    data = data,
                    grid = nio_grid,
                    add = True
                )
                dlg.Centre()
                wx.CallAfter(
                    dlg.ShowExtDialog,
                    self.text.title1,
                )
            elif id == bttns[2]: # Edit
                edit1()
            elif id == bttns[3]: # Delete
                nio_grid.DeleteRow()
            elif id == bttns[4]: # Show info
                nio = nio_grid.GetRow()[0]
                ix = nio_grid.GetSelectedItemIx()
                if isAlive(nio[2], int(nio[3])):
                    self.dialog = infDialog(
                        self,
                        parent = panel,
                        ix = ix,
                        grid = nio_grid
                    )
                    self.dialog.Centre()
                else:
                    messDial = eg.MessageDialog(
                        panel,
                        self.text.notAcc % nio[1],
                        self.text.warn,
                        wx.OK|wx.ICON_EXCLAMATION|wx.STAY_ON_TOP
                    )
                    messDial.ShowModal()
                    messDial.Destroy()
            evt.Skip()

        panel.sizer.Add(label1, 0, wx.TOP|wx.LEFT, 5)
        panel.sizer.Add(nio_grid, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)
        bttnSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        bttnSizer1.Add((5, -1))
        i = 0
        bttns = []
        for bttn in self.text.buttons1:
            id = wx.NewIdRef()
            bttns.append(id)
            b = wx.Button(panel, id, bttn)
            bttnSizer1.Add(b,1)
            if not len(nios) and i not in (0,):
                b.Enable(False)
            if i == 0:
                b.SetDefault()
            b.Bind(wx.EVT_BUTTON, onButton, id = id)
            bttnSizer1.Add((5, -1))
            i += 1
        panel.sizer.Add(bttnSizer1,0,wx.EXPAND)
        bottomSizer = wx.GridBagSizer(5, 5)
        panel.sizer.Add(bottomSizer,0,wx.ALL,5)
        prefLbl = wx.StaticText(panel, -1, self.text.prefix)
        prefCtrl = wx.TextCtrl(panel, -1, prefix)
        periLbl = wx.StaticText(panel, -1, self.text.period)
        periCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            period,
            min=5,
            max=30,
        )
        periCtrl.increment = 5

        def onPeriod(evt):
            val = evt.GetString()
            try:
                val = int(val)
            except:
                val = 0
                periCtrl.SetValue(0)
            evt.Skip()
        periCtrl.Bind(wx.EVT_TEXT, onPeriod)
        
        bottomSizer.Add(prefLbl,(0,0),flag=wx.ALIGN_CENTER_VERTICAL)
        bottomSizer.Add(prefCtrl,(0,1),flag=wx.EXPAND)
        bottomSizer.Add(periLbl,(1,0),flag=wx.ALIGN_CENTER_VERTICAL)
        bottomSizer.Add(periCtrl,(1,1),flag=wx.EXPAND)
        
        while panel.Affirmed():
            try:
                nios, passwds = nio_grid.GetData()
            except:
                nios = []
                passwds = []
            content = ""
            myPassword.SetDatabaseContent(content)
            if nios:
                for ix, nio in enumerate(nios):
                    passw = myPassword(nio[5])
                    passw.Set(passwds[ix])
                content = myPassword.GetDatabaseContent()
            panel.SetResult(
                nios,
                prefCtrl.GetValue(),
                periCtrl.GetValue(),
                content
            )
#===============================================================================

class TurnAllSocket(eg.ActionBase):

    def __call__(self, choose=0,nio="",state=1):
        nio = eg.ParseString(nio)
        state = self.plugin.parseArgument(state)
        if state is None:
            return
        tmp = [ni[choose+1] for ni in self.plugin.nios]
        if nio in tmp:
            ix = tmp.index(nio)
            tc = self.plugin.createConn(self.plugin.nios[ix],ix)
            if iI_tlTt(tc):
                state = 4*str(state)
                tc.write("port list %s\r\n" % state)
                resp = tc.read_until('250 ',1)
                if not '250 ' in resp:
                    return self.plugin.closeTc(tc, ix)
                resp = tc.read_very_eager() # 'OK\r\n'
                tc.write("quit\r\n")
                tc.close()
                return resp
            else:
                eg.PrintNotice(self.plugin.text.noConn % nio)
        else:
            eg.PrintNotice(self.plugin.text.unknown % nio)


    def GetLabel(self, choose,nio,state):
        if isinstance(state, int):
            state = self.plugin.text.states[state]
        return "%s: %s: %s" % (self.name, nio, state)


    def Configure(self, choose=0,nio="",state=1):
        panel = eg.ConfigPanel(self)
        chooseSizer = wx.BoxSizer(wx.HORIZONTAL)
        chooseLbl=wx.StaticText(panel,-1,self.plugin.text.chooseLbl)
        nioLbl=wx.StaticText(panel,-1,self.plugin.text.nioLbl)
        stateLbl=wx.StaticText(panel,-1,self.plugin.text.state)
        rb0=panel.RadioButton(choose==0,self.plugin.text.chooses[0], style=wx.RB_GROUP)
        rb1 = panel.RadioButton(choose==1, self.plugin.text.chooses[1])        
        choices = [rp[choose+1] for rp in self.plugin.nios]
        nioCtrl = wx.ComboBox(panel, -1, choices = choices,style=wx.CB_DROPDOWN)
        nioCtrl.SetValue(nio)
        stateCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            state,
            min = 0,
            max = 1
        )
        chooseSizer.Add(rb0)
        chooseSizer.Add(rb1, 0, wx.LEFT, 10)
        topSizer = wx.FlexGridSizer(3, 2, 10, 20)
        topSizer.AddGrowableCol(1)
        topSizer.Add(chooseLbl,0,ACV)
        topSizer.Add(chooseSizer)
        topSizer.Add(nioLbl,0,ACV)
        topSizer.Add(nioCtrl, 0, wx.EXPAND)
        topSizer.Add(stateLbl,0,ACV)
        topSizer.Add(stateCtrl,0,wx.EXPAND)
        panel.sizer.Add(topSizer,1,wx.ALL|wx.EXPAND,10)

        def onRadioBox(evt):
            ix = 1 + rb1.GetValue()
            oldIx = 1 + int(not rb1.GetValue())
            lst = [ni[ix] for ni in self.plugin.nios]
            oldLst = [ni[oldIx] for ni in self.plugin.nios]
            tmp = nioCtrl.GetValue()
            nioCtrl.Clear()
            nioCtrl.AppendItems(lst)
            if tmp in oldLst:
                tmp = lst[oldLst.index(tmp)]
                nioCtrl.SetValue(tmp)
            evt.Skip()
        rb0.Bind(wx.EVT_RADIOBUTTON, onRadioBox)
        rb1.Bind(wx.EVT_RADIOBUTTON, onRadioBox)

        while panel.Affirmed():
            panel.SetResult(
                int(rb1.GetValue()),
                nioCtrl.GetValue(),
                #sockCtrl.GetValue(),
                stateCtrl.GetValue(),
            )
#===============================================================================

class TurnSocket(eg.ActionBase):

    def __call__(self, choose=0,nio="",sock=1,state=1):
        nio = eg.ParseString(nio)
        sock = self.plugin.parseArgument(sock)
        if sock is None:
            return
        state = self.plugin.parseArgument(state)
        if state is None:
            return
        tmp = [ni[choose+1] for ni in self.plugin.nios]
        if nio in tmp:
            ix = tmp.index(nio)
            tc = self.plugin.createConn(self.plugin.nios[ix],ix)
            if iI_tlTt(tc):
                tc.write("port %i %i\r\n" % (sock, state))
                resp = tc.read_until('250 ',1)
                if not '250 ' in resp:
                    return self.plugin.closeTc(tc, ix)
                resp = tc.read_until('\r\n',1)
                if not '\r\n' in resp:
                    return self.plugin.closeTc(tc, ix)
                tc.write("quit\r\n")
                tc.close()
                return resp
            else:
                eg.PrintNotice(self.plugin.text.noConn % nio)
        else:
            eg.PrintNotice(self.plugin.text.unknown % nio)


    def GetLabel(self, choose,nio,sock,state):
        if isinstance(state, int):
            state = self.plugin.text.states[state]
        if isinstance(sock, int):
            sock = str(sock)
        return "%s: %s: %s: %s" % (self.name, nio, sock, state)


    def Configure(self, choose=0,nio="",sock=1,state=1):
        panel = eg.ConfigPanel(self)
        chooseSizer = wx.BoxSizer(wx.HORIZONTAL)
        chooseLbl=wx.StaticText(panel,-1,self.plugin.text.chooseLbl)
        nioLbl=wx.StaticText(panel,-1,self.plugin.text.nioLbl)
        sockLbl=wx.StaticText(panel,-1,self.plugin.text.sock)
        stateLbl=wx.StaticText(panel,-1,self.plugin.text.state)
        rb0=panel.RadioButton(choose==0,self.plugin.text.chooses[0], style=wx.RB_GROUP)
        rb1 = panel.RadioButton(choose==1, self.plugin.text.chooses[1])  
        choices = [rp[choose+1] for rp in self.plugin.nios]
        nioCtrl = wx.ComboBox(panel, -1, choices = choices,style=wx.CB_DROPDOWN)
        nioCtrl.SetValue(nio)
        sockCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            sock,
            min = 1,
            max = 4
        )
        stateCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            state,
            min = 0,
            max = 1
        )
        
        chooseSizer.Add(rb0)
        chooseSizer.Add(rb1, 0, wx.LEFT, 10)
        topSizer = wx.FlexGridSizer(4, 2, 10, 20)
        topSizer.AddGrowableCol(1)
        topSizer.Add(chooseLbl,0,ACV)
        topSizer.Add(chooseSizer)
        topSizer.Add(nioLbl,0,ACV)
        topSizer.Add(nioCtrl, 0, wx.EXPAND)
        topSizer.Add(sockLbl,0,ACV)
        topSizer.Add(sockCtrl,0,wx.EXPAND)
        topSizer.Add(stateLbl,0,ACV)
        topSizer.Add(stateCtrl,0,wx.EXPAND)
        panel.sizer.Add(topSizer,1,wx.ALL|wx.EXPAND,10)

        def onRadioBox(evt):
            ix = 1 + rb1.GetValue()
            oldIx = 1 + int(not rb1.GetValue())
            lst = [ni[ix] for ni in self.plugin.nios]
            oldLst = [ni[oldIx] for ni in self.plugin.nios]
            tmp = nioCtrl.GetValue()
            nioCtrl.Clear()
            nioCtrl.AppendItems(lst)
            if tmp in oldLst:
                tmp = lst[oldLst.index(tmp)]
                nioCtrl.SetValue(tmp)
            evt.Skip()
        rb0.Bind(wx.EVT_RADIOBUTTON, onRadioBox)
        rb1.Bind(wx.EVT_RADIOBUTTON, onRadioBox)

        while panel.Affirmed():
            panel.SetResult(
                int(rb1.GetValue()),
                nioCtrl.GetValue(),
                sockCtrl.GetValue(),
                stateCtrl.GetValue(),
            )
#===============================================================================

class ResetSocket(eg.ActionBase):

    def __call__(self, choose=0,nio="",sock=1):
        nio = eg.ParseString(nio)
        sock = self.plugin.parseArgument(sock)
        if sock is None:
            return
        tmp = [ni[choose+1] for ni in self.plugin.nios]
        if nio in tmp:
            ix = tmp.index(nio)
            tc = self.plugin.createConn(self.plugin.nios[ix],ix)
            if iI_tlTt(tc):
                tc.write("port %i int\r\n" % sock)
                resp = tc.read_until('250 ',1)
                if not '250 ' in resp:
                    return self.plugin.closeTc(tc, ix)
                resp = tc.read_until('\r\n',1)
                tc.write("quit\r\n")
                tc.close()
                return resp
            else:
                eg.PrintNotice(self.plugin.text.noConn % nio)
        else:
            eg.PrintNotice(self.plugin.text.unknown % nio)


    def GetLabel(self, choose,nio,sock):
        if isinstance(sock, int):
            sock = str(sock)
        return "%s: %s: %s" % (self.name, nio, sock)


    def Configure(self, choose=0,nio="",sock=1):
        panel = eg.ConfigPanel(self)
        chooseSizer = wx.BoxSizer(wx.HORIZONTAL)
        chooseLbl=wx.StaticText(panel,-1,self.plugin.text.chooseLbl)
        nioLbl=wx.StaticText(panel,-1,self.plugin.text.nioLbl)
        sockLbl=wx.StaticText(panel,-1,self.plugin.text.sock)
        rb0=panel.RadioButton(choose==0,self.plugin.text.chooses[0], style=wx.RB_GROUP)
        rb1 = panel.RadioButton(choose==1, self.plugin.text.chooses[1]) 
        choices = [rp[choose+1] for rp in self.plugin.nios]
        nioCtrl = wx.ComboBox(panel, -1, choices = choices,style=wx.CB_DROPDOWN)
        nioCtrl.SetValue(nio)
        sockCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            sock,
            min = 1,
            max = 4
        )
        chooseSizer.Add(rb0)
        chooseSizer.Add(rb1, 0, wx.LEFT, 10)
        topSizer = wx.FlexGridSizer(4, 2, 10, 20)
        topSizer.AddGrowableCol(1)
        topSizer.Add(chooseLbl,0,ACV)
        topSizer.Add(chooseSizer)
        topSizer.Add(nioLbl,0,ACV)
        topSizer.Add(nioCtrl, 0, wx.EXPAND)
        topSizer.Add(sockLbl,0,ACV)
        topSizer.Add(sockCtrl,0,wx.EXPAND)
        panel.sizer.Add(topSizer,1,wx.ALL|wx.EXPAND,10)

        def onRadioBox(evt):
            ix = 1 + rb1.GetValue()
            oldIx = 1 + int(not rb1.GetValue())
            lst = [ni[ix] for ni in self.plugin.nios]
            oldLst = [ni[oldIx] for ni in self.plugin.nios]
            tmp = nioCtrl.GetValue()
            nioCtrl.Clear()
            nioCtrl.AppendItems(lst)
            if tmp in oldLst:
                tmp = lst[oldLst.index(tmp)]
                nioCtrl.SetValue(tmp)
            evt.Skip()
        rb0.Bind(wx.EVT_RADIOBUTTON, onRadioBox)
        rb1.Bind(wx.EVT_RADIOBUTTON, onRadioBox)

        while panel.Affirmed():
            panel.SetResult(
                int(rb1.GetValue()),
                nioCtrl.GetValue(),
                sockCtrl.GetValue()
            )
#===============================================================================

class GetSocketState(eg.ActionBase):

    class text:
        res = "Result to return as:"
        kinds = ('"OFF"/"ON"','"0"/"1"','0/1','False/True')


    def __call__(self, choose=0,nio="",sock=1,res=0):
        nio = eg.ParseString(nio)
        sock = self.plugin.parseArgument(sock)
        if sock is None:
            return
        tmp = [ni[choose+1] for ni in self.plugin.nios]
        if nio in tmp:
            ix = tmp.index(nio)
            tc = self.plugin.createConn(self.plugin.nios[ix],ix)
            if iI_tlTt(tc):
                tc.write("port %i\r\n" % sock)
                resp = tc.read_until('250 ',1)
                if not '250 ' in resp:
                    return self.plugin.closeTc(tc, ix)
                resp = tc.read_very_eager()
                tc.write("quit\r\n")
                tc.close()
                if resp == "0\r\n" or resp == "1\r\n":
                    resp = resp[0]
                    i = int(resp)
                    return [self.plugin.text.states[i], resp, i, bool(i)][res]
                else:
                    eg.PrintError(self.plugin.text.unexp % repr(resp))
            else:
                eg.PrintNotice(self.plugin.text.noConn % nio)
        else:
            eg.PrintNotice(self.plugin.text.unknown % nio)


    def GetLabel(self, choose,nio,sock,res):
        if isinstance(sock, int):
            sock = str(sock)
        return "%s: %s: %s" % (self.name, nio, sock)


    def Configure(self, choose=0,nio="",sock=1,res=0):
        panel = eg.ConfigPanel(self)
        text = self.text
        chooseSizer = wx.BoxSizer(wx.HORIZONTAL)
        resSizer = wx.BoxSizer(wx.HORIZONTAL)
        chooseLbl=wx.StaticText(panel,-1,self.plugin.text.chooseLbl)
        nioLbl=wx.StaticText(panel,-1,self.plugin.text.nioLbl)
        sockLbl=wx.StaticText(panel,-1,self.plugin.text.sock)
        resLbl=wx.StaticText(panel,-1,text.res)
        rb0=panel.RadioButton(choose==0,self.plugin.text.chooses[0], style=wx.RB_GROUP)
        rb1 = panel.RadioButton(choose==1, self.plugin.text.chooses[1])        
        choices = [rp[choose+1] for rp in self.plugin.nios]
        nioCtrl = wx.ComboBox(panel, -1, choices = choices,style=wx.CB_DROPDOWN)
        nioCtrl.SetValue(nio)
        sockCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            sock,
            min = 1,
            max = 4
        )

        rb2=panel.RadioButton(res==0, text.kinds[0], style=wx.RB_GROUP)
        rb3 = panel.RadioButton(res==1, text.kinds[1])
        rb4 = panel.RadioButton(res==2, text.kinds[2])
        rb5 = panel.RadioButton(res==3, text.kinds[3])
        chooseSizer.Add(rb0)
        chooseSizer.Add(rb1, 0, wx.LEFT, 10)
        resSizer.Add(rb2)
        resSizer.Add(rb3, 0, wx.LEFT, 10)
        resSizer.Add(rb4, 0, wx.LEFT, 10)
        resSizer.Add(rb5, 0, wx.LEFT, 10)
        topSizer = wx.FlexGridSizer(4, 2, 10, 20)
        topSizer.AddGrowableCol(1)
        topSizer.Add(chooseLbl,0,ACV)
        topSizer.Add(chooseSizer)
        topSizer.Add(nioLbl,0,ACV)
        topSizer.Add(nioCtrl, 0, wx.EXPAND)
        topSizer.Add(sockLbl,0,ACV)
        topSizer.Add(sockCtrl,0,wx.EXPAND)
        topSizer.Add(resLbl,0,ACV)
        topSizer.Add(resSizer)
        panel.sizer.Add(topSizer,1,wx.ALL|wx.EXPAND,10)

        def onRadioBox(evt):
            ix = 1 + rb1.GetValue()
            oldIx = 1 + int(not rb1.GetValue())
            lst = [ni[ix] for ni in self.plugin.nios]
            oldLst = [ni[oldIx] for ni in self.plugin.nios]
            tmp = nioCtrl.GetValue()
            nioCtrl.Clear()
            nioCtrl.AppendItems(lst)
            if tmp in oldLst:
                tmp = lst[oldLst.index(tmp)]
                nioCtrl.SetValue(tmp)
            evt.Skip()
        rb0.Bind(wx.EVT_RADIOBUTTON, onRadioBox)
        rb1.Bind(wx.EVT_RADIOBUTTON, onRadioBox)

        while panel.Affirmed():
            panel.SetResult(
                int(rb1.GetValue()),
                nioCtrl.GetValue(),
                sockCtrl.GetValue(),
                int(rb3.GetValue())+2*int(rb4.GetValue())+3*int(rb5.GetValue()),
            )
#===============================================================================

class SendCommand(eg.ActionBase):

    class text:
        command = "Command:"

    def __call__(self, choose=0,nio="",cmd=""):
        cmd = eg.ParseString(cmd)
        nio = eg.ParseString(nio)
        tmp = [ni[choose+1] for ni in self.plugin.nios]
        if nio in tmp:
            ix = tmp.index(nio)
            tc = self.plugin.createConn(self.plugin.nios[ix],ix)
            if iI_tlTt(tc):
                print "tc =",tc
                tc.write("%s\r\n" % str(cmd.strip()))
                resp = tc.read_until("250 ",1)
                print "resp =",resp
                if not '250 ' in resp:
                    return self.plugin.closeTc(tc, ix)
                resp = tc.read_very_eager()
                tc.write("quit\r\n")
                tc.close()
                return resp
            else:
                eg.PrintNotice(self.plugin.text.noConn % nio)
        else:
            eg.PrintNotice(self.plugin.text.unknown % nio)


    def GetLabel(self, choose, nio, cmd):
        return "%s: %s: %s" % (self.name, nio, cmd)


    def Configure(self, choose=0,nio="",cmd=""):
        panel = eg.ConfigPanel(self)
        chooseSizer = wx.BoxSizer(wx.HORIZONTAL)
        chooseLbl=wx.StaticText(panel,-1,self.plugin.text.chooseLbl)
        nioLbl=wx.StaticText(panel,-1,self.plugin.text.nioLbl)
        sockLbl=wx.StaticText(panel,-1,self.text.command)
        rb0=panel.RadioButton(choose==0,self.plugin.text.chooses[0], style=wx.RB_GROUP)
        rb1 = panel.RadioButton(choose==1, self.plugin.text.chooses[1])
        choices = [rp[choose+1] for rp in self.plugin.nios]
        nioCtrl = wx.ComboBox(panel, -1, choices = choices,style=wx.CB_DROPDOWN)
        nioCtrl.SetValue(nio)
        cmdCtrl = wx.TextCtrl(panel, -1, cmd, style=wx.TE_MULTILINE)
        chooseSizer.Add(rb0)
        chooseSizer.Add(rb1, 0, wx.LEFT, 10)
        topSizer = wx.FlexGridSizer(3, 2, 10, 20)
        topSizer.AddGrowableRow(2)
        topSizer.AddGrowableCol(1)
        topSizer.Add(chooseLbl)
        topSizer.Add(chooseSizer)
        topSizer.Add(nioLbl,0,wx.TOP,4)
        topSizer.Add(nioCtrl, 0, wx.EXPAND)
        topSizer.Add(sockLbl)
        topSizer.Add(cmdCtrl, 1, wx.EXPAND)
        mainSizer= wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 1, wx.EXPAND)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,10)

        def onRadioBox(evt):
            ix = 1 + rb1.GetValue()
            oldIx = 1 + int(not rb1.GetValue())
            lst = [ni[ix] for ni in self.plugin.nios]
            oldLst = [ni[oldIx] for ni in self.plugin.nios]
            tmp = nioCtrl.GetValue()
            nioCtrl.Clear()
            nioCtrl.AppendItems(lst)
            if tmp in oldLst:
                tmp = lst[oldLst.index(tmp)]
                nioCtrl.SetValue(tmp)
            evt.Skip()
        rb0.Bind(wx.EVT_RADIOBUTTON, onRadioBox)
        rb1.Bind(wx.EVT_RADIOBUTTON, onRadioBox)

        while panel.Affirmed():
            panel.SetResult(
                int(rb1.GetValue()),
                nioCtrl.GetValue(),
                cmdCtrl.GetValue(),
            )
#===============================================================================

class enableNio(eg.ActionBase):

    def __call__(self, choose=0,nio=""):
        nio = eg.ParseString(nio)
        tmp = [rp[choose+1] for rp in self.plugin.nios]
        if nio in tmp:
            ix = tmp.index(nio)
            return self.plugin.enableNio(ix, self.value)
        else:
            eg.PrintNotice(self.plugin.text.unknown % nio)


    def GetLabel(self, choose=0,nio=""):
        return "%s: %s" % (self.name, nio)


    def Configure(self, choose=0,nio=""):
        panel = eg.ConfigPanel(self)
        chooseSizer = wx.BoxSizer(wx.HORIZONTAL)
        chooseLbl=wx.StaticText(panel,-1,self.plugin.text.chooseLbl)
        nioLbl=wx.StaticText(panel,-1,self.plugin.text.nioLbl)
        rb0=panel.RadioButton(choose==0,self.plugin.text.chooses[0], style=wx.RB_GROUP)
        rb1 = panel.RadioButton(choose==1, self.plugin.text.chooses[1])
        choices = [rp[choose+1] for rp in self.plugin.nios]
        nioCtrl = wx.ComboBox(panel, -1, choices = choices,style=wx.CB_DROPDOWN)
        nioCtrl.SetValue(nio)
        chooseSizer.Add(rb0)
        chooseSizer.Add(rb1, 0, wx.LEFT, 10)
        topSizer = wx.FlexGridSizer(3, 2, 10, 20)
        topSizer.AddGrowableCol(1)
        topSizer.Add(chooseLbl)
        topSizer.Add(chooseSizer)
        topSizer.Add(nioLbl,0,wx.TOP,4)
        topSizer.Add(nioCtrl, 0, wx.EXPAND)
        mainSizer= wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 0, wx.EXPAND)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,10)

        def onRadioBox(evt):
            ix = 1 + rb1.GetValue()
            oldIx = 1 + int(not rb1.GetValue())
            lst = [ni[ix] for ni in self.plugin.nios]
            oldLst = [ni[oldIx] for ni in self.plugin.nios]
            tmp = nioCtrl.GetValue()
            nioCtrl.Clear()
            nioCtrl.AppendItems(lst)
            if tmp in oldLst:
                tmp = lst[oldLst.index(tmp)]
                nioCtrl.SetValue(tmp)
            evt.Skip()
        rb0.Bind(wx.EVT_RADIOBUTTON, onRadioBox)
        rb1.Bind(wx.EVT_RADIOBUTTON, onRadioBox)

        while panel.Affirmed():
            panel.SetResult(
                int(rb1.GetValue()),
                nioCtrl.GetValue(),
            )
#===============================================================================
ACTIONS = (
    (TurnAllSocket, "TurnAllSocket", "Turn all socket ON/OFF", "Turns all socket ON or OFF.", None),
    (TurnSocket, "TurnSocket", "Turn socket ON/OFF", "Turns socket ON or OFF.", None),
    (ResetSocket, "ResetSocket", "Reset socket", "Resets socket.", None),
    (GetSocketState, "GetSocketState", "Get socket state", "Returns state of socket (ON or OFF).", None),
    (SendCommand, "SendCommand", "Send command", "Sends command to selected Netio.", None),
    (enableNio, "EnableNio", "Enable Netio", "Enables selected Netio.", True),
    (enableNio, "DisableNio", "Disable Netio", "Disables selected Netio.", False),
)
