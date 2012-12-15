# -*- coding: utf-8 -*-
#
# plugins/NTP/__init__.py
#
# This file is a plugin for EventGhost.
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
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.0.3  by Pako 2012-12-15 11:04 UTC+1
#      - bugfix
# 0.0.2  by Pako 2012-12-15 10:50 UTC+1
#      - url for support is set
# 0.0.1  by Pako 2012-12-14 19:11 UTC+1
#      - initial version 
#===============================================================================

import eg
import wx
import ntplib
import time
from datetime import datetime as dt
from win32api import SetSystemTime

SERVERS = [
"north-america.pool.ntp.org",
"europe.pool.ntp.org",
"pool.ntp.org",
"time.nist.gov",
"time.windows.com",
]

eg.RegisterPlugin(
    name="NTP",
    description=ur'''<rst>
Works as a simple NTP client.

| 
| **ATTENTION:**
| To use this plugin on Windows Vista and later, 
| it is necessary to EventGhost was started with "Run as Administrator" !!!
|
| This plugin uses the library **ntplib.py** by **Charles-Francois Natali**.
''',
    kind="other",
    author="Pako",
    guid = "{DCD090E9-D561-4FBA-9BAB-31A7DE66455F}",
    version="0.0.2",
    createMacrosOnAdd=True,
    canMultiLoad = False,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=5088",
    icon = (
        "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"
    ),
)
#===============================================================================

class Text:
    listLabel = "List of NTP servers:"
    periodic = "Periodic synchronization"
    rateLbl = "Interval (min):"
    autoLbl = "Start automatically"
    delete = 'Delete'
    insert = 'Add new'
    stop = "NTP stopped" 
    start = "NTP started" 
    status = (
        "NTP is stopped",
        "NTP is running"
    )
    synchro = "Time synchronized"
    failed = "Synchronization failed"
    testLbl = "Test"
    syncLbl = "Synchronize now"
    testStart = 'Test of server "%s" started'
    syncStart = 'Instant synchronization with server "%s" started'
    testPassed = 'Test passed. TIME: %s  OFFSET: %s'
    testFailed = 'Test failed. ERROR: %s'
    noResponse = "No server responds."
#===============================================================================

def Move(lst,index,direction):
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
        index2 = index+direction
        tmpList[index] = lst[index2]
        tmpList[index2] = lst[index]
    return index2,tmpList
#===============================================================================

class LogCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        kwargs["style"] = 0 if not kwargs.has_key("style") else kwargs["style"]
        kwargs["style"] |= wx.TE_MULTILINE|wx.TE_READONLY|wx.SUNKEN_BORDER
        wx.TextCtrl.__init__(self, *args, **kwargs)
        self.SetForegroundColour("GREY")
        self.write("Logging started...", "")
        self.Bind(wx.EVT_SIZE, self.OnSize)


    def MakeVisibleEnd(self):
        self.ShowPosition(self.GetLastPosition())        


    def write( self, msg, lf="\n"):
        self.AppendText("%s%s   %s" % (
            lf,
            str(dt.fromtimestamp(time.time()))[11:19],
            msg)
        )
        self.MakeVisibleEnd()       


    def OnSize(self, event):
        wx.CallAfter(self.MakeVisibleEnd)
        event.Skip()
#===============================================================================
 
class NTP(eg.PluginBase):

    text = Text
    task = None
    log = None
    flag = True

    def __init__(self):
        self.AddActionsFromList(ACTIONS)
    
    
    def __start__(self, servers = SERVERS, rate = 60, auto = True):
        self.servers = servers
        self.rate = rate
        if auto:
            self.StartNTP()


    def __stop__(self):
        self.StopNTP()


    def Configure(self, servers = SERVERS, rate = 60, auto = True):

        def boxEnable(enable):
            self.serverCtrl.Enable(enable)
            btnTest.Enable(enable)

        text = self.text
        panel = eg.ConfigPanel(self)
        self.servers = servers
        leftSizer = wx.FlexGridSizer(4, 2, 2, 8)
        topMiddleSizer=wx.BoxSizer(wx.VERTICAL)
        listLabel=wx.StaticText(panel, -1, text.listLabel)
        listBoxCtrl=wx.ListBox(
            panel,-1,
            size=wx.Size(200, 110),
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        self.statusLbl=wx.StaticText(panel, -1, "")
        self.statusLbl.SetForegroundColour(wx.RED)
        self.serverCtrl=wx.TextCtrl(panel,-1,'')
        rateLbl=wx.StaticText(panel, -1, text.rateLbl)
        rateCtrl = eg.SpinIntCtrl(panel, -1, rate, min=1, max=1440)
        autoCtrl = wx.CheckBox(panel, -1, text.autoLbl)
        autoCtrl.SetValue(auto)
        sz = panel.dialog.GetClientSize()
        console = LogCtrl(panel, -1, "", wx.DefaultPosition, wx.Size(sz[0], 60))                      
        console.SetMinSize(wx.Size(sz[0], 60))            
        self.log = console

        #Button UP
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
        btnUP = wx.BitmapButton(panel, -1, bmp)
        btnUP.Enable(False)
        topMiddleSizer.Add(btnUP)
        #Button DOWN
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16, 16))
        btnDOWN = wx.BitmapButton(panel, -1, bmp)
        btnDOWN.Enable(False)
        topMiddleSizer.Add(btnDOWN,0,wx.TOP,3)
        #Buttons 'Delete' and 'Insert new'
        btnApp=wx.Button(panel,-1,text.insert)
        btnDEL=wx.Button(panel,-1,text.delete)
        #Buttons 'Test'
        btnTest=wx.Button(panel,-1,text.testLbl)
        eg.EqualizeWidths((btnDEL, btnApp, btnTest))
        #Buttons 'Sync'
        btnSync=wx.Button(panel,-1,text.syncLbl)
        btnDEL.Enable(False)
        
        leftSizer.Add(listLabel,0,wx.TOP,5)
        leftSizer.Add((1,1))
        leftSizer.Add(listBoxCtrl,0,wx.TOP,2)
        leftSizer.Add(topMiddleSizer,0,wx.TOP,5)
        leftSizer.Add(self.serverCtrl,0,wx.EXPAND|wx.TOP,4)
        leftSizer.Add(btnTest,0,wx.TOP,3)
        rightStatBox = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.periodic),
            wx.VERTICAL
        ) 
        rightStatBox.Add(rateLbl,0,wx.TOP,5)
        rightStatBox.Add(rateCtrl,0,wx.EXPAND|wx.TOP,2)
        rightStatBox.Add(autoCtrl,0,wx.TOP,14)
        rightStatBox.Add(self.statusLbl,0,wx.TOP,14)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer.Add(rightStatBox,1,wx.EXPAND)        
        rightSizer.Add(btnSync,0,wx.TOP,12)        
        
        topMiddleSizer.Add(btnDEL,0,wx.TOP,5)
        topMiddleSizer.Add(btnApp,0,wx.TOP,5)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(leftSizer,0,wx.RIGHT,15)
        mainSizer.Add(rightSizer, 1, wx.EXPAND|wx.TOP,7)
        panel.sizer.Add(mainSizer,0,wx.EXPAND)
        panel.sizer.Add(console,1,wx.EXPAND|wx.TOP,5)
        if len(self.servers) > 0:
            listBoxCtrl.Set(self.servers)
            listBoxCtrl.SetSelection(0)
            self.serverCtrl.SetValue(self.servers[0])
            self.oldSel=0
            btnUP.Enable(True)
            btnDOWN.Enable(True)
            btnDEL.Enable(True)
        else:
            boxEnable(False)
            panel.dialog.buttonRow.applyButton.Enable(False)
            panel.dialog.buttonRow.okButton.Enable(False)
        panel.sizer.Layout()


        def onClick(evt):
            self.flag = False
            sel = listBoxCtrl.GetSelection()
            label = self.serverCtrl.GetValue()
            if label.strip() != "":
                if self.servers.count(label) == 1:
                    self.oldSel=sel
                    self.serverCtrl.SetValue(self.servers[sel])
            listBoxCtrl.SetSelection(self.oldSel)
            listBoxCtrl.SetFocus()
            evt.Skip()
            self.flag = True
        listBoxCtrl.Bind(wx.EVT_LISTBOX, onClick)


        def onButtonSync(evt):
            self.InstantSynchro()
            #server = self.serverCtrl.GetValue()
            #self.Log(self.text.syncStart % server)
            #self.Synchro((server,))  
        btnSync.Bind(wx.EVT_BUTTON, onButtonSync)


        def onButtonTest(evt):
            server = self.serverCtrl.GetValue()
            self.Log(self.text.testStart % server)
            resp = self.NtpRequest(server)
            if isinstance(resp, list):
                self.Log(self.text.testPassed % (
                    str(dt.fromtimestamp(resp[0]))[:19],
                    str(resp[1]))
                )
            else:
                self.Log(self.text.testFailed % resp)
        btnTest.Bind(wx.EVT_BUTTON, onButtonTest)


        def onButtonUp(evt):
            newSel,self.servers=Move(self.servers,listBoxCtrl.GetSelection(),-1)
            listBoxCtrl.Set(self.servers)
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            #evt.Skip()
        btnUP.Bind(wx.EVT_BUTTON, onButtonUp)


        def onButtonDown(evt):
            newSel,self.servers=Move(self.servers,listBoxCtrl.GetSelection(),1)
            listBoxCtrl.Set(self.servers)
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            #evt.Skip()
        btnDOWN.Bind(wx.EVT_BUTTON, onButtonDown)


        def onButtonDelete(evt):
            self.flag = False
            lngth=len(self.servers)
            if lngth==2:
                btnUP.Enable(False)
                btnDOWN.Enable(False)
            sel = listBoxCtrl.GetSelection()
            if lngth == 1:
                self.servers=[]
                listBoxCtrl.Set([])
                self.serverCtrl.SetValue("")
                boxEnable(False)
                panel.dialog.buttonRow.applyButton.Enable(False)
                panel.dialog.buttonRow.okButton.Enable(False)
                btnDEL.Enable(False)
                btnApp.Enable(True)
                evt.Skip()
                return
            elif sel == lngth - 1:
                sel = 0
            self.oldSel = sel
            self.servers.pop(listBoxCtrl.GetSelection())
            listBoxCtrl.Set(self.servers)
            listBoxCtrl.SetSelection(sel)
            self.serverCtrl.SetValue(self.servers[sel])
            evt.Skip()
            self.flag = True
        btnDEL.Bind(wx.EVT_BUTTON, onButtonDelete)


        def OnTxtChange(evt):
            if self.servers != [] and self.flag:
                flag = False
                sel = self.oldSel
                label = self.serverCtrl.GetValue()
                self.servers[sel]=label
                listBoxCtrl.Set(self.servers)
                listBoxCtrl.SetSelection(sel)
                if label != "":
                    flag = self.servers.count(label) == 1
                panel.dialog.buttonRow.applyButton.Enable(flag)
                panel.dialog.buttonRow.okButton.Enable(flag)
                btnApp.Enable(flag)
            evt.Skip()
        self.serverCtrl.Bind(wx.EVT_TEXT, OnTxtChange)


        def OnButtonAppend(evt):
            self.flag = False
            if len(self.servers)==1:
                btnUP.Enable(True)
                btnDOWN.Enable(True)
            boxEnable(True)
            sel = listBoxCtrl.GetSelection() + 1
            self.oldSel=sel
            self.servers.insert(sel,"")
            listBoxCtrl.Set(self.servers)
            listBoxCtrl.SetSelection(sel)
            self.serverCtrl.SetValue("")
            self.serverCtrl.SetFocus()
            btnApp.Enable(False)
            btnDEL.Enable(True)
            evt.Skip()
            self.flag = True
        btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)


        # the apply button wrapper
        onApply = panel.dialog.OnApply
        def OnButton(event):
            console = self.log
            onApply(event)
            wx.CallAfter(self.SetStatusLabel)
            self.log = console
        panel.dialog.buttonRow.applyButton.Bind(wx.EVT_BUTTON, OnButton)

        # the cancel button wrapper
        onCancel = panel.dialog.OnCancel
        def OnCancel(event):
            onCancel(event)
            self.log = None
        panel.dialog.buttonRow.cancelButton.Bind(wx.EVT_BUTTON, OnCancel)

        onClose = panel.dialog.OnClose
        def OnClose(event):
            onClose(event)
            self.log = None
        panel.dialog.Bind(wx.EVT_CLOSE, OnClose)

        self.SetStatusLabel()


        while panel.Affirmed():
            self.log = None
            panel.SetResult(
                listBoxCtrl.GetStrings(),
                rateCtrl.GetValue(),
                autoCtrl.GetValue(),
            )


    def InstantSynchro(self):
        if self.log:
            server = self.serverCtrl.GetValue()
            self.Log(self.text.syncStart % server)
            self.Synchro((server,))
        else:
            self.Synchro()


    def SetStatusLabel(self):
        if self.log:
            label = self.text.status[self.task is not None]
            self.statusLbl.SetLabel(label)
            self.Log(label)


    def Set_SystemTime(self, tmstmp):
        str_tm = time.localtime(tmstmp)
        try:
            result = SetSystemTime(
                str_tm.tm_year,
                str_tm.tm_mon,
                str_tm.tm_wday,
                str_tm.tm_mday,
                str_tm.tm_hour,
                str_tm.tm_min,
                str_tm.tm_sec,
                int((tmstmp+0.0005)%1*1000)
            )
            return result
        except Exception, e:
            s = e.args[2].decode(eg.systemEncoding)
            return s


    def NtpRequest(self, server, c=ntplib.NTPClient()):
        try:
            resp = c.request(server)
            result = [resp.tx_time, round(resp.offset, 6)]
            return result
        except ntplib.NTPException, e:
            s = e.args[0].decode(eg.systemEncoding)
            eg.PrintError("NTP: " + s)
            return s
        except Exception, e:
            s = e.args[1].decode(eg.systemEncoding)
            eg.PrintError("NTP: " + s + ": "+server)
            return s


    def GetNTPtime(self, servers = None):
        c = ntplib.NTPClient()
        if servers is None:
            servers = self.servers
            flag = False
        else:
            flag = True
        for server in servers:
            resp = self.NtpRequest(server, c)
            if isinstance(resp, list):
                resp.append(server)
                break
        return resp if isinstance(resp, list) or flag else self.text.noResponse


    def Log(self, mess):
        if self.log:
            self.log.write(mess)


    def Synchro(self, servers = None):
        ntp = self.GetNTPtime(servers)
        res = self.Set_SystemTime(ntp[0]+time.timezone) if isinstance(ntp, list) else ntp
        if isinstance(res, int) and res:
            eg.PrintNotice("NTP: %s. SERVER: %s  OFFSET: %s s" % (
                self.text.synchro,
                str(ntp[2]),
                str(ntp[1]))
            )
            self.Log("%s. SERVER: %s  OFFSET: %s s" % (
                self.text.synchro,
                str(ntp[2]),
                str(ntp[1]))
            )
        else:
            eg.PrintError("NTP: %s. ERROR: %s" % (self.text.failed, res))
            self.Log("%s. ERROR: %s" % (self.text.failed, res))
        return res


    def Polling(self):
        self.task = eg.scheduler.AddTask(60 * self.rate, self.Polling)
        self.Synchro()


    def StopNTP(self):
        if self.task:
            eg.scheduler.CancelTask(self.task)
            eg.PrintNotice(self.text.stop)
            self.task = None
            self.SetStatusLabel()        


    def StartNTP(self):
        self.StopNTP()
        self.task = eg.scheduler.AddTask(60 * self.rate, self.Polling)
        self.Synchro()
        eg.PrintNotice(self.text.start)
        self.SetStatusLabel()        
#===============================================================================

class synchronize(eg.ActionBase):

    def __call__(self):
        return self.plugin.InstantSynchro()
#===============================================================================

class start_ntp(eg.ActionBase):

    def __call__(self):
        return self.plugin.StartNTP()
#===============================================================================

class stop_ntp(eg.ActionBase):

    def __call__(self):
        return self.plugin.StopNTP()
#===============================================================================

class get_ntp_time(eg.ActionBase):

    class text:
        formLabel = "Date/time format:"

    def GetDTstring(self, ts, form):
        return (
            str(dt.fromtimestamp(ts))[:19],
            time.ctime(ts),
            tuple(time.localtime(ts)),
            ts
        )[form]


    def __call__(self, format = 0):
        ts = self.plugin.GetNTPtime() if self.value else (time.time(), 0)
        return (self.GetDTstring(ts[0], format), str(round(ts[1], 6)))


    def Configure(self, format = 0):
        panel = eg.ConfigPanel()
        formLabel = wx.StaticText(panel,-1,self.text.formLabel)
        choices = []
        ts = time.time()
        for frm in range(4):
            choices.append(str(self.GetDTstring(ts, frm)))
        formCtrl = wx.Choice(panel, -1, choices = choices)
        formCtrl.SetSelection(format)
        sizer = wx.FlexGridSizer(1, 2, 5, 10)
        sizer.Add(formLabel,0,wx.TOP,3)
        sizer.Add(formCtrl)
        panel.sizer.Add(sizer,0,wx.ALL|wx.EXPAND,20)

        while panel.Affirmed():
            panel.SetResult(
                formCtrl.GetSelection(),
            )
#===============================================================================

ACTIONS = (
    (get_ntp_time, "get_ntp_time", "Get NTP time", "Gets NTP time.", 1),
    (get_ntp_time, "get_local_time", "Get local time", "Gets local time.", 0),
    (stop_ntp, "stop_ntp", "Stop NTP", "Stops NTP.", None),
    (start_ntp, "start_ntp", "Start NTP", "Starts NTP.", None),
    (synchronize, "synchronize", "Synchronize now", "Performs an instant synchronization.", None),
)

