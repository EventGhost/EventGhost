# -*- coding: utf-8 -*-
version = "3.13.3"
#
# This file is part of EventGhost.
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
# 3.13.3 by Sem;colon 2016-12-03 11:00 UTC+1
#     - some fixes and cleanup
# 3.13.2 by david-mark 2016-11-18 20:00 UTC+1
#     - bugfix (Fixed incorrect "latin1" decoding)
# 3.13.1 by Sem;colon 2016-11-06 01:00 UTC+1
#     - bugfix (Added "self.protocol_version = 'HTTP/1.1'" for ws connections)
# 3.13 by Sem;colon 2016-10-29 01:00 UTC+1
#     - bugfix (Send event to another webserver was never doing GET but always POST)
#     - Changes to support EG v0.5
# 3.12.1 by Pako 2016-05-08 18:19 UTC+1
#     - many changes - particularly regarding the WebSocket
# 3.12 by by Pako 2016-02-15 17:15 UTC+1
#     - bugfix (Send all values)
# 3.11 by by Pako 2016-02-06 08:44 UTC+1
#     - bugfix (Send or Broadcast Value, when value is persistent)
# 3.10 by by Pako 2016-01-12 11:01 UTC+1
#     - bugfix (handle_one_request & self.rfile.read(1) == "")
# 3.9 by Sem;colon 2015-12-28 01:10 UTC+1
#     - The Method TriggerEnduringEvent now supports "prefix" as keyword argument on POST requests
# 3.8 by Filandre 2015-03-29
#     - add support for Hixie-76 protocol (for browsers 2010-2011)
#     - fix connection for IE
# 3.7 by krambriw & Pako 2015-03-04 07:00 UTC+1
#     - treatment of some unexpected communication status WebSocket client
# 3.6 by Pako 2015-03-02 09:41 UTC+1
#     - message can now include the word Ping
# 3.5 by krambriw 2014-02-26
#     - Added support for client initiated high level ping/pong
#     - Detecting 'WebSocket Protocol Error' and 'Masked frame from server' errors in handle_one_request function
#       to improve session keep alive
# 3.4 by Pako 2014-12-28 11:30 UTC+1
#     - WebSocket client actions added
# 3.3 by Pako 2014-11-30 06:57 UTC+1
#     - bugfix ("Send event to another EventGhost" feature failed since 3.0)
# 3.2 by Sem;colon 2014-11-22 10:00 UTC+1
#     - ExecuteScript now raises exceptions in EventGhost Log
# 3.1 by Pako 2014-11-20 06:25 UTC+1
#     - added support of temporary and persistent variables when rendering page
#     - bugfixes
# 3.0 by Pako 2014-11-16 15:46 UTC+1
#     - added WebSocket support and actions (Tornado webserver compatible)
# 2.1 by Pako 2014-02-14 11:14 UTC+1
#     - added option to serve with secured protocol (https://)
# 2.0 by Sem;colon 2014-01-04 22:15 UTC+1
#     - fixed bug (eventghost crashes if submitting the Set (persistent) value configuration window)
#     - removed decoding of the return value for the SendEventExt action (could cause problems sometimes)
#       the code must now be decoded in a script manually (if decoding is needed)
# 1.9 by Pako 2013-12-04 14:36 UTC+1
#     - added option to disable parsing of strings (Sem;colon's solutions)
# 1.8 by Sem;colon 2013-11-06 20:10 UTC+1
#     - added menue entries (plugin configuration) to customize the join strings in the do_POST Enhancement by Sem;colon
#     - improved handling of some returned datatypes in the do_POST Enhancement by Sem;colon
#     - fixed bug in end_request
# 1.7 by Pako 2013-09-15 08:58 UTC+1
#     - added Autosave option (when a persistent value changed)
#     - added do_POST (Ajax/JSON) method "GetGlobalValue"
#     - fixed do_POST (Ajax/JSON) methods "Set(Persistent)Value"
# 1.6 by Sem;colon 2013-09-07 22:00 UTC+1
#     - edited the POST enhancement by Sem;colon:
#       -changed the function "request=" to GetGlobalValue
#       -added loop for GetValue requests to be able to request multible values at once
#       -fixed bug: GetValue didn't return a value
#     - changed "author" line, so that it showes up correctly under "Special Thanks"
# 1.5 by Sem;colon 2013-08-31 09:32 UTC+1
#     - extended the POST enhancement by Sem;colon
#       to match the functionality of the AJAX JSON POST
# 1.4 by Pako 2013-08-09 11:02 UTC+1
#     - bugfixes
# 1.3 by Pako 2013-08-05 20:30 UTC+1
#     - bugfixes
#     - class text added to SendEventExt action
# 1.2 by Pako 2013-08-02 14:57 UTC+1
#     - added url support link to forum
#     - added support of variables (temporary and persistent)
#     - added actions Get/Set (Persistent) Value and Set Clients Flags
#     - do_POST method "TriggerEvent" can now use another prefixes too
#     - new methods for do_POST: Get/Set (Persistent) Value, Get All Values, ...
#     - ... Get Changed Values, Execute Script (return a result !)
#     - do_POST is no longer limited to JSON Request (author: Sem;colon)
#     - new action SendEventExt (author: Sem;colon)

import eg

eg.RegisterPlugin(
    name = "Webserver",
    author = (
        "Bitmonster",
        "Pako",
        "Sem;colon",
        "krambriw",
    ),
    version = version,
    guid = "{E4305D8E-A3D3-4672-B06E-4EA1F0F6C673}",
    description = ur'''<rst>
Implements a small webserver, that you can use to generate events
through HTML-pages and WebSocket.

Implementation of WebSocket support was made possible through the article_,
published on the SevenWatt_ web..

Plugin version: %s

.. _article:     http://www.sevenwatt.com/main/websocket-html-webserver-python/
.. _SevenWatt:   http://www.sevenwatt.com/main/
''' % version,
    createMacrosOnAdd = True,
    canMultiLoad = True,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeT"
        "AAAACXBIWXMAAA3XAAAN1wFCKJt4AAAAB3RJTUUH1gEECzsZ7j1DbAAAAu1JREFUOMul"
        "kztsW3UUxn////Xb1684NXbzsOskA6UiklWCCOmCCiKwsCDBjBShThVCDICYgCIxMHgC"
        "BhYYkbJAhaIoIBCKKvUBhArHGLexaar4/bj2ffjey0CboagTZ/l0jo5+Ovp0PvifJR4c"
        "5F64NOMX7kcoyrppOwmBwOcRHTGZXBk7YuPW5bfrDwWcWv/gdSFlcWEp55mZyxCJhBGA"
        "ruvcqd+lXKpOsMxLpW/ffe8/gNz6h6/FYuFP184VlNO5E8yfTJEKu2QSQbojk51rt7nx"
        "Z4Pr124Sks7HP3918S0ACfDJlz+ueBRZfPaZJ5R3Xinw3HKKx7MRCgtTzCaDRAMKwjJo"
        "N1qcWX6Uu93xm/nn358/Bmzt7r+RX8wG4kGFdm+MGo3h93lojaCnO5RrbZpjQXYmSSrq"
        "Y2EpJ7zC/QLAA1Ctt5568lxeDHULTYaYQtLUwCOh3dX47Osr9EcG0qOgjUzyi1lq1drK"
        "MWBs2ul4LMLiXJxkSHLQNvB5PWiWzfZuid5wjGnZGMMxXr+faFTFmNihY4DANXyK9L28"
        "NkejM6J5NET4VSa2jaqGkIrEtWxsx0EfaAC47r/my3vN3mg4sAcjk0wyTLvR4vL31zls"
        "9FG8Pp5eXWZm9hEmtoMQgn5/iILbPr4AIbaq1b+Xd/ZmQ/WDO5QPWmSmIzQ6A8aWjTY2"
        "SSdVMoVTBFSVq7/XXOHY3wEoAPGl8+VWq3fBDai+W0ea2K8c0hxa5OdPoOAQUCRnl6bZ"
        "eKnASLf49ZdSM51OvvrH7mZXAeiWtweR3FrvqNF7Mb8wh5QSfzjEYVujdtRnYtuczk4x"
        "HQ3gdQwrEZxs39j6fKdSqbSU+5/Y++uHsieateuHg9VYPCpTqSSp6QSJmIqhm+z9VnJu"
        "V6o9Jv2beq++WywWf3IcZ/hgmNKh9JnVk4+d31CCyRXDljEAx9T6zrC+dzYrribCcn9z"
        "c/ObTqdzALjiIQmNArF76gcMYAB0gT7g3l/+ByWIP9hU8ktfAAAAAElFTkSuQmCC"
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=1663",
)

import wx
import socket
from os import curdir, pardir
from sys import path
from ssl import wrap_socket, CERT_NONE
from posixpath import splitext, normpath
from time import sleep, strftime
from datetime import datetime as dt
from urllib import unquote, unquote_plus
from urllib2 import urlopen, Request as urlRequest
from httplib import HTTPResponse
from jinja2 import BaseLoader, TemplateNotFound, Environment
from json import dumps, loads
from re import IGNORECASE, compile as re_compile
from struct import pack, unpack
from base64 import b64encode, encodestring as b64_encStr
from hashlib import sha1, md5
from threading import Thread, Event
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ThreadingMixIn
from os.path import getmtime, isfile, isdir, join, exists, splitdrive, split
from wx.lib.mixins.listctrl import TextEditMixin
try:
    from websocket import WebSocketApp
except ImportError:
    from websocket import WebSocket as WebSocketApp
SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
ACV = wx.ALIGN_CENTER_VERTICAL

CLOSE_CODE = {
    "\x03\xe8":"NORMAL_CLOSURE",
    "\x03\xe9":"GOING_AWAY",
    "\x03\xea":"PROTOCOL_ERROR",
    "\x03\xee":"ABNORMAL_CLOSURE",
    "\x03\xf3":"SERVER_ERROR",
    "\x03\x00":"UNKNOWN_ERROR",
}


true = True
false = False
METHODS = (
    "SetValue",
    "SetPersistentValue",
    "ExecuteScript",
    "TriggerEvent",

    "GetGlobalValue",
    "GetValue",
    "GetPersistentValue",
    "GetAllValues",

    "GetChangedValues",
    "TriggerEnduringEvent",
    "RepeatEnduringEvent",
    "EndLastEvent",
    "Ping"
)
#===============================================================================

def replInstVal(strng):
    return strng.replace("eg.event","eg_event").replace("eg.result","eg_result")
    

def ClientChoice(evt, text, panel, id3, id4, cl_ip, cl_port, size2, rBMC):
    middleSizer = panel.sizer.GetItem(0).GetSizer()
    dynamicSizer = middleSizer.GetItem(2).GetSizer()
    dynamicSizer.Clear(True)
    middleSizer.Detach(dynamicSizer)
    dynamicSizer.Destroy()
    dynamicSizer = wx.GridBagSizer(2, 10)
    dynamicSizer.SetMinSize(size2)
    middleSizer.Add(dynamicSizer,1, wx.EXPAND)
    mode = rBMC.GetSelection()
    portCtrl = None
    if mode == 1:
        if evt:
            evt.Skip()
        return
    txtLabel = wx.StaticText(panel,-1,text.host)
    txtCtrl = wx.TextCtrl(panel, id3, cl_ip)
    dynamicSizer.Add(txtLabel,(0,0),(1,1))
    dynamicSizer.Add(txtCtrl,(1,0),(1,1),flag = wx.EXPAND)
    portLabel = wx.StaticText(panel,-1,text.port)
    portCtrl = wx.TextCtrl(panel, id4, cl_port)
    dynamicSizer.Add(portLabel,(2,0),(1,1),flag = wx.TOP, border = 10)
    dynamicSizer.Add(portCtrl,(3,0),(1,1))
    panel.sizer.Layout()
    if evt:
        evt.Skip()
#===============================================================================

class WebSocketClient(WebSocketApp):
    def __init__(self, title, url, login, password, noCert, plugin):
        kwargs = {
            'on_open' : plugin.on_open,
            'on_message' : plugin.on_message,
            'on_error' : self.on_error,
            'on_close' : self.on_close,
        }
        if login is not None:
            password = password if password is not None else ""
            kwargs['header']=["Authorization:Basic " + b64encode(login+":"+password)]
        WebSocketApp.__init__(self, url, **kwargs)
        self.url = url
        self.conTime = None
        self.title = title
        self.noCert = noCert
        self.plugin = plugin


    def on_error(self, _, error):
        eg.PrintError(self.plugin.text.wsConError % self.title)
        eg.PrintError(u"[Error %i] %s" % (
            error.args[0],
            error.args[1].decode(eg.systemEncoding)
        ))

        try:
            self.close()
        except:
            pass


    def on_close(self, _):
        try:
            del self.plugin.wsServers[self.title]
        except:
            pass
        self.plugin.TriggerEvent(
            "%s.%s" % (self.plugin.text.wsServerDisconn, self.title),
            payload = self.title
        )


    def start(self):
        if self.noCert:
            self.run_forever(sslopt={"cert_reqs": CERT_NONE})
        else:
            self.run_forever()
#===============================================================================

class Table(wx.ListCtrl):

    def __init__(self, parent, header, minRows):
        wx.ListCtrl.__init__(
            self,
            parent,
            -1,
            style=wx.LC_REPORT|wx.VSCROLL|wx.HSCROLL|wx.LC_HRULES|wx.LC_VRULES,
        )
        for i, colLabel in enumerate(header):
            self.InsertColumn(
                i,
                colLabel,
                format = wx.LIST_FORMAT_LEFT
            )
        self.InsertStringItem(0, "dummy")
        rect = self.GetItemRect(0, wx.LIST_RECT_BOUNDS)
        self.minHeight = 4 + rect[1] + minRows * rect[3]
        self.DeleteAllItems()
#===============================================================================

class VarTable(wx.ListCtrl, TextEditMixin):

    def __init__(self, parent, txt, edit):
        wx.ListCtrl.__init__(
            self,
            parent,
            -1,
            style = wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|wx.LC_EDIT_LABELS,
        )
        self.edit = edit
        self.edCell = None
        self.Show(False)
        TextEditMixin.__init__(self)
        self.editor.SetBackgroundColour(wx.Colour(135, 206, 255))

        self.InsertColumn(0, txt.vrbl)
        self.InsertColumn(1, txt.defVal, wx.LIST_FORMAT_LEFT)
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        self.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
        self.InsertStringItem(0, "dummy")
        rect = self.GetItemRect(0, wx.LIST_RECT_BOUNDS)
        hh = rect[1] #header height
        hi = rect[3] #item height
        self.DeleteAllItems()
        self.w0 = self.GetColumnWidth(0)
        self.w1 = self.GetColumnWidth(1)
        self.wk = SYS_VSCROLL_X+self.GetWindowBorderSize()[0]+self.w0 + self.w1
        width = self.wk
        rows = 10
        self.SetMinSize((max(width, 200), 2 + hh + rows * hi))
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Show(True)


    def SetWidth(self):
        w = (self.GetSize().width - self.wk)
        w0_ = w/2 + self.w0
        w1_ = w/2 + self.w1
        self.SetColumnWidth(0, w0_)
        self.SetColumnWidth(1, w1_)


    def OnSize(self, event):
        wx.CallAfter(self.SetWidth)
        event.Skip()


    def FillData(self, data):
        self.DeleteAllItems()
        cnt = len(data)
        i = 0
        for key, value in data.iteritems():
            self.InsertStringItem(i, key)
            self.SetStringItem(i, 1, value)
            i += 1
        self.Enable(i > 0)


    def OpenEditor(self, col, row): #Hack of default method
        if self.edit:
            self.edCell = (row, col, self.GetItem(row, col).GetText()) #Remember pos and value!!!
            TextEditMixin.OpenEditor(self, col, row)


    def CloseEditor(self, event = None): #Hack of default method
        TextEditMixin.CloseEditor(self, event)
        if not event:
            self.SetStringItem(*self.edCell) #WORKAROUND !!!
        elif isinstance(event, wx.CommandEvent):
            row, col, oldVal = self.edCell
            newVal = self.GetItem(row, col).GetText()
            evt = eg.ValueChangedEvent(self.GetId(), value = (row, col, newVal))
            wx.PostEvent(self, evt)


    def DeleteSelectedItems(self):
        item = self.GetFirstSelected()
        selits = []
        while item != -1:
            selits.append(item)
            item = self.GetNextSelected(item)
        selits.reverse()
        for item in selits:
            self.DeleteItem(item)


    def GetData(self):
        data = {}
        for row in range(self.GetItemCount()):
            data[self.GetItemText(row)] = self.GetItem(row, 1).GetText()
        return data
#===============================================================================

class KeysAsAttrs:
    def __init__(self, pairSet):
        self._pairSet = pairSet

    def __getattr__(self, key):
        try:
            return self._pairSet[key]
        except KeyError,err:
            raise AttributeError(key)
#===============================================================================

class VariableDialog(wx.Frame):

    def __init__(self, parent, plugin, pers = False):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style = wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL|wx.RESIZE_BORDER,
            name="Variable manager/viewer"
        )
        self.panel = parent
        self.plugin = plugin
        self.text = plugin.text
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.pers = pers


    def ShowVariableDialog(self, title):
        self.panel.Enable(False)
        self.panel.dialog.buttonRow.cancelButton.Enable(False)
        self.panel.EnableButtons(False)
        self.SetTitle(title)


        text = self.plugin.text
        panel = wx.Panel(self)
        varTable = VarTable(panel, self.text, self.pers)
        if self.pers: # Persistent variable manager
            varTable.FillData(self.plugin.pubPerVars)
        else:  # Temporary variable viewer
            varTable.FillData(self.plugin.pubVars)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        intSizer = wx.BoxSizer(wx.VERTICAL)
        intSizer.Add(varTable,1,wx.EXPAND|wx.BOTTOM, 5)
        sizer.Add(intSizer,1,wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT,10)
        btn3 = wx.Button(panel, -1, self.text.delete)
        btn3.Enable(False)
        btn4 = wx.Button(panel, -1, self.text.clear)
        delSizer = wx.BoxSizer(wx.HORIZONTAL)
        delSizer.Add(btn3)
        delSizer.Add(btn4,0,wx.LEFT,10)
        intSizer.Add(delSizer)

        def onDelete(evt):
            varTable.DeleteSelectedItems()
            btn3.Enable(False)
            evt.Skip()
        btn3.Bind(wx.EVT_BUTTON, onDelete)

        def onClear(evt):
            varTable.DeleteAllItems()
            evt.Skip()
        btn4.Bind(wx.EVT_BUTTON, onClear)

        def OnItemSelected(event):
            selCnt = varTable.GetSelectedItemCount()
            btn3.Enable(selCnt>0)
            varTable.GetSelectedItemCount()
            event.Skip()
        varTable.Bind(wx.EVT_LIST_ITEM_SELECTED, OnItemSelected)
        varTable.Bind(wx.EVT_LIST_ITEM_DESELECTED, OnItemSelected)
        btn1 = wx.Button(panel, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn1.SetDefault()

        def onOK(evt):
            flag = False
            data = varTable.GetData()
            if self.pers:
                pubPerVars = self.plugin.pubPerVars
                old = list(pubPerVars.iterkeys())
                new = list(data.iterkeys())
                deleted = list(set(old) - set(new))
                #renamed = list(set(new)-set(old))
                for key in deleted:
                    self.plugin.DelPersistentValue(key)
                for key, value in data.iteritems():
                    if key not in pubPerVars or value != pubPerVars[key]:
                        pubPerVars[key] = value
                        flag = True
                if flag or len(deleted):
                    wx.CallAfter(self.plugin.SetDocIsDirty)
            else:
                pubVars = self.plugin.pubVars
                old = list(pubVars.iterkeys())
                new = list(data.iterkeys())
                deleted = list(set(old) - set(new))
                #renamed = list(set(new)-set(old))
                for key in deleted:
                    self.plugin.DelValue(key)
                for key, value in data.iteritems():
                    if key not in pubVars or value != pubVars[key]:
                        pubVars[key] = value
            self.Close()
        btn1.Bind(wx.EVT_BUTTON,onOK)

        line = wx.StaticLine(
            panel,
            -1,
            size = (20,-1),
            style = wx.LI_HORIZONTAL
        )
        sizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
        btn2 = wx.Button(panel, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        sizer.Add((1,6))
        sizer.Fit(self)

        def onClose(evt):
            self.MakeModal(False)
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)
   
        def onCancel(evt):
            self.Close()
        btn2.Bind(wx.EVT_BUTTON, onCancel)
        
        self.SetSize((500, -1))
        self.SetMinSize((500, -1))
        sizer.Layout()
        self.Raise()
        self.MakeModal(True)
        self.Show()
#===============================================================================

class ClientsDialog(wx.Frame):

    def __init__(self, parent, plugin):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style = wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL|wx.RESIZE_BORDER,
            name="WebSocket clients"
        )
        self.panel = parent
        self.plugin = plugin
        self.text = plugin.text
        self.SetIcon(self.plugin.info.icon.GetWxIcon())


    def ShowClientsDialog(self):
        text = self.plugin.text
        self.SetTitle(text.wsServers)
        self.panel.Enable(False)
        self.panel.dialog.buttonRow.cancelButton.Enable(False)
        self.panel.EnableButtons(False)

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)

        cliSizer = wx.GridBagSizer(5, 5)
        clientListCtrl = Table(
            panel,
            text.colLabelsCli,
            3
        )
        #setting cols width
        clientListCtrl.InsertStringItem(0, " 255.255.255.255")
        clientListCtrl.SetStringItem(0, 1, "HHHHHHH")
        clientListCtrl.SetStringItem(0, 2, "0000-00-00 00:00:00")
        width_c = SYS_VSCROLL_X + clientListCtrl.GetWindowBorderSize()[0]
        for i in range(3):
            clientListCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            width_c += clientListCtrl.GetColumnWidth(i)
        clientListCtrl.SetMinSize((width_c, clientListCtrl.minHeight))
        #buttons
        abCli_Id = wx.NewId()
        abAllCli_Id = wx.NewId()
        self.buttonIds = (abCli_Id, abAllCli_Id)
        abortButtonCli = wx.Button(panel, abCli_Id, text.abort)
        abortAllButtonCli = wx.Button(panel, abAllCli_Id, text.abortAll)
        refreshButtonCli = wx.Button(panel, -1, text.refresh)
        cliSizer.Add(clientListCtrl, (0, 0), (1, 4), flag = wx.EXPAND)
        cliSizer.Add(abortButtonCli, (1, 0), flag = wx.LEFT, border = 10)
        cliSizer.Add(abortAllButtonCli, (1, 1))
        cliSizer.Add(refreshButtonCli, (1, 2))
        cliSizer.AddGrowableRow(0)
        cliSizer.AddGrowableCol(2)
        sizer.Add(cliSizer, 1, wx.EXPAND)

        def onDelete(evt):
            item = clientListCtrl.GetFirstSelected()
            while item != -1:
                ip = clientListCtrl.GetItem(item, 0).GetText()
                port = clientListCtrl.GetItem(item, 1).GetText()
                self.plugin.wsClients[(str(ip), int(port))].on_ws_closed()
                item = clientListCtrl.GetNextSelected(item)
            self.RefreshTable()
            abortButtonCli.Enable(False)
            evt.Skip()
        abortButtonCli.Bind(wx.EVT_BUTTON, onDelete)

        def onClear(evt):
            clnts = list(self.plugin.wsClients.iterkeys())
            for clnt in clnts:
                self.plugin.wsClients[clnt].on_ws_closed()
            self.RefreshTable()
            evt.Skip()
        abortAllButtonCli.Bind(wx.EVT_BUTTON, onClear)

        def onRefresh(evt):
            self.RefreshTable()
            evt.Skip()
        refreshButtonCli.Bind(wx.EVT_BUTTON, onRefresh)

        def OnItemSelected(event):
            selCnt = clientListCtrl.GetSelectedItemCount()
            abortButtonCli.Enable(selCnt>0)
            clientListCtrl.GetSelectedItemCount()
            event.Skip()
        clientListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, OnItemSelected)
        clientListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, OnItemSelected)
        btn1 = wx.Button(panel, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn1.SetDefault()

        def onOK(evt):
            self.Close()
        btn1.Bind(wx.EVT_BUTTON, onOK)

        line = wx.StaticLine(
            panel,
            -1,
            size = (20,-1),
            style = wx.LI_HORIZONTAL
        )
        sizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
        btn2 = wx.Button(panel, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        sizer.Add((1,6))
        sizer.Fit(self)
        self.table = clientListCtrl
        self.RefreshTable()
        abortButtonCli.Enable(False)

        def onClose(evt):
            self.MakeModal(False)
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)
   
        def onCancel(evt):
            self.Close()
        btn2.Bind(wx.EVT_BUTTON, onCancel)
        
        self.SetMinSize(self.GetSize())
        sizer.Layout()
        self.Raise()
        self.MakeModal(True)
        self.Show()

    def RefreshTable(self):
        table = self.table
        table.DeleteAllItems()
        for i, clnt in enumerate(list(self.plugin.wsClients.iterkeys())):
            table.InsertStringItem(i, clnt[0])
            table.SetStringItem(i, 1, str(clnt[1]))
            table.SetStringItem(i, 2, dt.fromtimestamp(
                    self.plugin.wsClientsTime[clnt]
                ).strftime('%Y-%m-%d %H:%M:%S'))
        cnt = table.GetItemCount()
        abortAllButtonCli = wx.FindWindowById(self.buttonIds[1])
        abortAllButtonCli.Enable(cnt > 0)
#===============================================================================

class ServersDialog(wx.Frame):

    def __init__(self, parent, plugin):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style = wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL|wx.RESIZE_BORDER,
            name="WebSocket servers"
        )
        self.panel = parent
        self.plugin = plugin
        self.text = plugin.text
        self.SetIcon(self.plugin.info.icon.GetWxIcon())


    def ShowServersDialog(self):
        text = self.plugin.text
        self.SetTitle(text.wsServers)
        self.panel.Enable(False)
        self.panel.dialog.buttonRow.cancelButton.Enable(False)
        self.panel.EnableButtons(False)

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)

        srvSizer = wx.GridBagSizer(5, 5)
        serverListCtrl = Table(
            panel,
            text.colLabelsSrvr,
            3
        )
        #setting cols width
        serverListCtrl.InsertStringItem(0, 16*"H")
        serverListCtrl.SetStringItem(0, 1, 24*"H")
        serverListCtrl.SetStringItem(0, 2, "0000-00-00 00:00:00")
        width_c = SYS_VSCROLL_X + serverListCtrl.GetWindowBorderSize()[0]
        for i in range(3):
            serverListCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            width_c += serverListCtrl.GetColumnWidth(i)
        serverListCtrl.SetMinSize((width_c, serverListCtrl.minHeight))
        #buttons
        abSrv_Id = wx.NewId()
        abAllSrv_Id = wx.NewId()
        self.buttonIds = (abSrv_Id, abAllSrv_Id)
        abortButtonSrv = wx.Button(panel, abSrv_Id, text.abort)
        abortAllButtonSrv = wx.Button(panel, abAllSrv_Id, text.abortAll)
        refreshButtonSrv = wx.Button(panel, -1, text.refresh)
        srvSizer.Add(serverListCtrl, (0, 0), (1, 4), flag = wx.EXPAND)
        srvSizer.Add(abortButtonSrv, (1, 0), flag = wx.LEFT, border = 10)
        srvSizer.Add(abortAllButtonSrv, (1, 1))
        srvSizer.Add(refreshButtonSrv, (1, 2))
        srvSizer.AddGrowableRow(0)
        srvSizer.AddGrowableCol(2)
        sizer.Add(srvSizer, 1, wx.EXPAND)

        def onDelete(evt):
            item = serverListCtrl.GetFirstSelected()
            while item != -1:
                title = serverListCtrl.GetItem(item, 0).GetText()
                #url = serverListCtrl.GetItem(item, 1).GetText()
                self.plugin.wsServers[title].close()
                item = serverListCtrl.GetNextSelected(item)
            self.RefreshTable()
            abortButtonSrv.Enable(False)
            evt.Skip()
        abortButtonSrv.Bind(wx.EVT_BUTTON, onDelete)

        def onClear(evt):
            srvrs = list(self.plugin.wsServers.iterkeys())
            for srvr in srvrs:
                self.plugin.wsServers[srvr].close()
            self.RefreshTable()
            evt.Skip()
        abortAllButtonSrv.Bind(wx.EVT_BUTTON, onClear)

        def onRefresh(evt):
            self.RefreshTable()
            evt.Skip()
        refreshButtonSrv.Bind(wx.EVT_BUTTON, onRefresh)

        def OnItemSelected(event):
            selCnt = serverListCtrl.GetSelectedItemCount()
            abortButtonSrv.Enable(selCnt>0)
            serverListCtrl.GetSelectedItemCount()
            event.Skip()
        serverListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, OnItemSelected)
        serverListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, OnItemSelected)
        btn1 = wx.Button(panel, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn1.SetDefault()

        def onOK(evt):
            self.Close()
        btn1.Bind(wx.EVT_BUTTON, onOK)

        line = wx.StaticLine(
            panel,
            -1,
            size = (20,-1),
            style = wx.LI_HORIZONTAL
        )
        sizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
        btn2 = wx.Button(panel, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        sizer.Add((1,6))
        sizer.Fit(self)
        self.table = serverListCtrl
        self.RefreshTable()
        abortButtonSrv.Enable(False)

        def onClose(evt):
            self.MakeModal(False)
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)
   
        def onCancel(evt):
            self.Close()
        btn2.Bind(wx.EVT_BUTTON, onCancel)
        
        self.SetMinSize(self.GetSize())
        sizer.Layout()
        self.Raise()
        self.MakeModal(True)
        self.Show()

    def RefreshTable(self):
        table = self.table
        table.DeleteAllItems()
        for i, srvr in enumerate(list(self.plugin.wsServers.iterkeys())):
            server = self.plugin.wsServers[srvr]
            table.InsertStringItem(i, server.title)
            table.SetStringItem(i, 1, str(server.url))
            ts = dt.fromtimestamp(
                server.conTime
            ).strftime('%Y-%m-%d %H:%M:%S') if server.conTime else ""
            table.SetStringItem(i, 2, ts)
        cnt = table.GetItemCount()
        abortAllButtonSrv = wx.FindWindowById(self.buttonIds[1])
        abortAllButtonSrv.Enable(cnt > 0)
#===============================================================================

class FileLoader(BaseLoader):
    """Loads templates from the file system."""

    def get_source(self, environment, filename):
        try:
            sourceFile = open(filename, "rb")
        except IOError:
            raise TemplateNotFound(filename)
        try:
            contents = sourceFile.read().decode("utf-8")
        finally:
            sourceFile.close()

        mtime = getmtime(filename)
        def uptodate():
            try:
                return getmtime(filename) == mtime
            except OSError:
                return False
        return contents, filename, uptodate


class MyServer(ThreadingMixIn, HTTPServer):
    address_family = getattr(socket, 'AF_INET6', None)

    def __init__(self, requestHandler, port, certfile, keyfile):
        self.httpdThread = None
        self.abort = False
        for res in socket.getaddrinfo(None, port, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            self.address_family = res[0]
            self.socket_type = res[1]
            address = res[4]
            break

        HTTPServer.__init__(self, address, requestHandler)
        if isfile(certfile) and isfile(keyfile):
            self.socket = wrap_socket(
                self.socket,
                certfile = certfile,
                keyfile = keyfile,
                server_side = True
            )


    def server_bind(self):
        """Called by constructor to bind the socket."""
        if socket.has_ipv6 and eg.WindowsVersion >= 'Vista':
            # make it a dual-stack socket if OS is Vista/Win7
            IPPROTO_IPV6 = 41
            self.socket.setsockopt(IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        HTTPServer.server_bind(self)


    def Start(self):
        """Starts the HTTP server thread"""
        self.httpdThread = Thread(name="WebserverThread", target = self.Run)
        self.httpdThread.start()


    def Run(self):
        try:
            # Handle one request at a time until stopped
            while not self.abort:
                self.handle_request()
        finally:
            self.httpdThread = None


    def Stop(self):
        """Stops the HTTP server thread"""
        if self.httpdThread:
            self.abort = True
            # closing the socket will awake the underlying select.select() call
            # so the handle_request() loop will notice the abort flag
            # immediately
            self.socket.close()
            self.RequestHandlerClass.repeatTimer.Stop()
#===============================================================================

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    extensions_map = SimpleHTTPRequestHandler.extensions_map.copy()
    extensions_map['.ico'] = 'image/x-icon'
    extensions_map['.svg'] = 'image/svg+xml'
    extensions_map['.manifest'] = 'text/cache-manifest'
    handshake_done = False
    clAddr = None
    magic = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    # these class attributes will be set by the plugin:
    authString = None
    authRealm = None
    basepath = None
    repeatTimer = None
    environment = None
    plugin = None
    
    def getClientAddress(self):
        ip = self.client_address
        return (ip[0].replace('::ffff:', ''), ip[1])


    def on_ws_message(self, message):
        try:
            message = message.decode("utf-8")
        except:
            pass
        try:
            data = loads(message)
        except:
            if message.find('WebSocket Protocol Error') > -1:
                eg.PrintNotice('message: '+message)
                self.on_ws_closed()
            elif message.find('Masked frame from server') > -1:
                eg.PrintNotice('message: '+message)
                self.on_ws_closed()
            else:
                self.plugin.TriggerEvent(
                    u"ClientMessage.%s" % message,
                    payload = (self.clAddr, message)
                )
            return
        # JSON request
        if not isinstance(data, dict) or "method" not in data.iterkeys():
            self.plugin.TriggerEvent(
                "ClientMessage",
                payload = (self.clAddr, data)
            )
        else:
            methodName = data["method"]
            if methodName in METHODS:
                if methodName == "Ping":
                    id = data["id"] if "id" in data else -1
                    content = dumps({
                        "method":"Pong",
                        "id":id,
                        "client_address":self.clAddr
                    })
                    self.plugin.ServerSendMessage(self.clAddr, content)
                    return
                try:
                    args = data.get("args", [])
                    kwargs = data.get("kwargs", {})
                    result = self.plugin.ProcessTheArguments(
                        self,
                        methodName,
                        args,
                        kwargs
                    )
                    content = dumps(result)
                    self.plugin.ServerSendMessage(self.clAddr, content)
                except:
                    pass
            else:
                self.plugin.TriggerEvent(
                    methodName,
                    payload = (self.clAddr, data)
                )

    def on_ws_closed(self):
        self.handshake_done = False
        if self.clAddr in self.plugin.wsClients and self.close_connection == 0:
            self.send_close()
            self.close_connection = 1
            self.plugin.TriggerEvent(
                self.plugin.text.wsClientDisconn,
                payload = [self.clAddr]
            )
            del self.plugin.wsClients[self.clAddr]
            del self.plugin.wsClientsTime[self.clAddr]


    def send_close(self):
        msg = bytearray()
        msg.append(0x88)
        msg.append(0x00)
        try:
            self.request.send(msg)
        except:
            pass


    def handle_one_request(self):
        if not self.handshake_done:
            try:
                SimpleHTTPRequestHandler.handle_one_request(self)
            except Exception, exc:
                eg.PrintError(
                    "Webserver: Exception on handle_one_request:",
                    unicode(exc)
                )
            #SimpleHTTPRequestHandler.handle_one_request(self)
        else: # WebSocket read next message
            try:
                opcode = self.rfile.read(1)
#F              if not opcode:
#F                  return # ??????????
            except Exception, exc:
                if exc.args[0] in (10053, 10054, 10060):
                    return self.on_ws_closed()
                else:
                    eg.PrintTraceback() # debugging ...
### Filandre
            if self.protocol == 1:
                decoded = ""
                next = True
                while next:
                    try:
                        char = self.rfile.read(1)
                    except:
                        return self.on_ws_closed()
                    next = char != chr(255)
                    if next:
                        decoded += char
            else:
###
                length = self.rfile.read(1)
                if length:
                    length = ord(length) & 127
                    if length == 126:
                        length = unpack(">H", self.rfile.read(2))[0]
                    elif length == 127:
                        length = unpack(">Q", self.rfile.read(8))[0]
                    masks = [ord(byte) for byte in self.rfile.read(4)]
                    decoded = ""
                    for char in self.rfile.read(length):
                        decoded += chr(ord(char) ^ masks[len(decoded) % 4])
                else:
                    opcode = "\x08"
                    decoded = "\x03\xe9"

            _stream = 0x0
            _text = 0x1
            _binary = 0x2
            _close = 0x8
            _ping = 0x9
            _pong = 0xa

            opcode = ord(opcode) & 0x0F

### krambriw
            # close
            if opcode == _close:
               decoded = decoded if decoded in CLOSE_CODE else "\x03\x00"
               eg.PrintNotice('Websocket closing: ' + CLOSE_CODE[decoded])
               self.on_ws_closed()
            # ping
            elif opcode == _ping:
                #print 'ping'
                resp = ['Pong', self.client_address]
                self.write_message(repr(resp))
            # pong
            elif opcode == _pong:
                pass
            # data
            elif opcode == _stream or opcode == _text or opcode == _binary:
                self.on_ws_message(decoded)
###
    
    
    def write_message(self, message):
        try:
### Filandre
          if self.protocol == 1:
            self.request.send(chr(0))
            self.request.send(message)
            self.request.send(chr(255))
          else:
###
            self.request.send(chr(129))
            length = len(message)
            if length <= 125:
                self.request.send(chr(length))
            elif length >= 126 and length <= 65535:
                self.request.send(chr(126))
                self.request.send(pack(">H", length))
            else:
                self.request.send(chr(127))
                self.request.send(pack(">Q", length))
            self.request.send(message)
        except:
            pass


    def handshake(self):
        headers = self.headers
        if str(headers.get("Upgrade", None)).lower() != "websocket":
            return
### Filandre
        key = ''
        try: # RFC 6455
            key = headers['Sec-WebSocket-Key']
        except: # Hixie-76
            key1 = headers['Sec-WebSocket-Key1']
            key2 = headers['Sec-WebSocket-Key2']
            key3 = self.rfile.read(8)
        if key == '':
            spaces1 = key1.count(" ")
            spaces2 = key2.count(" ")
            num1 = int("".join([c for c in key1 if c.isdigit()])) / spaces1
            num2 = int("".join([c for c in key2 if c.isdigit()])) / spaces2
            digest = md5(pack('>II8s', num1, num2, key3)).digest()
            self.send_response(101, 'WebSocket Protocol Handshake')
            self.send_header('Upgrade', 'WebSocket')
            self.send_header('Connection', 'Upgrade')
            self.send_header('Sec-WebSocket-Origin', headers['Origin'])
            self.send_header('Sec-WebSocket-Location', headers['Origin'].replace('http', 'ws') + '/')
            self.end_headers()
            self.wfile.write(digest)
            self.wfile.flush()
            self.protocol = 1
        else:
###
            try:
                digest = b64encode(sha1(key + self.magic).hexdigest().decode('hex'))
            except:
                eg.PrintTraceback()
            self.protocol_version = 'HTTP/1.1'
            self.send_response(101, 'Switching Protocols')
            self.send_header('Upgrade', 'websocket')
            self.send_header('Connection', 'Upgrade')
            self.send_header('Sec-WebSocket-Accept', str(digest))
            self.end_headers()
            self.protocol = 0
        self.handshake_done = True
        self.close_connection = 0
#  ws_connected
        self.plugin.wsClients[self.clAddr] = self
        self.plugin.wsClientsTime[self.clAddr] = eg.Utils.time.time()
        self.plugin.TriggerEvent(
            self.plugin.text.wsClientConn,
            payload = [self.clAddr]
        )


    def version_string(self):
        """Return the server software version string."""
        return "EventGhost/" + eg.Version.string


    def Authenticate(self):
        # only authenticate, if set
        if self.authString is None:
            return True

        # do Basic HTTP-Authentication
        authHeader = self.headers.get('authorization')
        if authHeader is not None:
            authType, authString = authHeader.split(' ', 2)
            if authType.lower() == 'basic' and authString == self.authString:
                return True

        self.send_response(401)
        self.send_header('WWW-Authenticate','Basic realm="%s"' % self.authRealm)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        return False


    def SendContent(self, path):
        fsPath = self.translate_path(path)
        if isdir(fsPath):
            if not path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", path + "/")
                self.end_headers()
                return None
            for index in ("index.html", "index.htm"):
                index = join(fsPath, index)
                if exists(index):
                    fsPath = index
                    break
            else:
                return self.list_directory(path)
        extension = splitext(fsPath)[1].lower()
        if extension not in (".htm", ".html"):
            f = self.send_head()
            if f:
                self.wfile.write(f.read())
                f.close()
            return
        try:
            template = self.environment.get_template(fsPath)
        except TemplateNotFound:
            self.send_error(404, "File not found")
            return
        kwargs = {}
        kwargs.update(self.plugin.pubVars)
        kwargs.update(self.plugin.pubPerVars)
        content = template.render(**kwargs)
        self.end_request(content)


    def end_request(self, content, case = 'text/html'):
        content=content.encode("UTF-8")
        self.send_response(200)
        self.send_header("Content-type", case)
        self.send_header("Content-Length", len(content))
        self.end_headers()
        self.wfile.write(content)
        self.wfile.close()


    def do_POST(self):
        """Serve a POST request."""
        # First do Basic HTTP-Authentication, if set
        if not self.Authenticate():
            return
        self.clAddr = self.getClientAddress()
        contentLength = int(self.headers.get('content-length'))
        content = self.rfile.read(contentLength)
        plugin = self.plugin
        try:
            data = loads(content)
        except:

# Enhancement by Sem;colon - START
            data=content.split("&")
            if data[0]=="request":
                self.SendContent(self.path)
                if len(data)>1:
                    self.plugin.TriggerEvent(data[1], data[2:])
            else:
                content = "True"
                i=1
                if data[0]=="GetGlobalValue":
                    content = ""
                    while i<len(data):
                        try:
                            content += unicode(self.environment.globals[data[i]])
                        except:
                            content += "None"
                        i+=1
                        if i<len(data):
                            content+=self.plugin.valueSplitter
                elif data[0]=="ExecuteScript":
                    content = ""
                    while i < len(data):
                        try:
                            output = eval(data[i])
                            if isinstance(output, str) or isinstance(output, unicode) or isinstance(output, int) or isinstance(output, float) or isinstance(output, long):
                                content += unicode(output)
                            elif isinstance(output, list):
                                content += self.plugin.listSplitter.join(unicode(x) for x in output)
                            else:
                                content += "True"
                        except:
                            print "Webserver: ExecuteScript Error: data[i] = ", data[i]
                            content += "False"
                            raise
                        i += 1
                        if i < len(data):
                            content += self.plugin.valueSplitter
                elif data[0] == "GetValue":
                    content = ""
                    while i < len(data):
                        try:
                            content += self.plugin.GetValue(data[i], self.clAddr[0])
                        except:
                            content += "None"
                        i+=1
                        if i<len(data):
                            content+=self.plugin.valueSplitter
                elif data[0]=="GetPersistentValue":
                    content = ""
                    while i<len(data):
                        try:
                            content += self.plugin.GetPersistentValue(data[i], self.clAddr[0])
                        except:
                            content += "None"
                        i+=1
                        if i<len(data):
                            content+=self.plugin.valueSplitter
                elif data[0]=="SetValue":
                    try:
                        self.plugin.SetValue(data[1], data[2])
                    except:
                        content = "False"
                elif data[0]=="SetPersistentValue":
                    try:
                        self.plugin.SetPersistentValue(data[1], data[2])
                    except:
                        content = "False"
                elif data[0]=="GetAllValues":
                    try:
                        content = dumps(self.plugin.GetAllValues(self.clAddr[0]))
                    except:
                        content = "False"
                elif data[0]=="GetChangedValues":
                    try:
                        content = dumps(self.plugin.GetChangedValues(self.clAddr[0]))
                    except:
                        content = "False"
                elif data[0] == "TriggerEnduringEvent":
                    self.plugin.EndLastEnduringEvent()
                    if data[1][0:7]=="prefix=" and len(data)>2:
                        data[2]=data[2].replace("suffix=","")
                        if len(data)>3:
                            data[3]=data[3].replace("payload=","")
                        self.plugin.lastEnduringEvent=eg.TriggerEnduringEvent(prefix=data[1][7:], suffix=data[2], payload=data[3:])
                    else:
                        self.plugin.lastEnduringEvent=self.plugin.TriggerEnduringEvent(data[1], data[2:])
                    self.repeatTimer.Reset(2000)
                elif data[0] == "RepeatEnduringEvent":
                    self.repeatTimer.Reset(2000)
                elif data[0] == "EndLastEvent":
                    self.repeatTimer.Reset(None)
                    #self.plugin.EndLastEvent()
                    self.plugin.EndLastEnduringEvent()
                elif data[0]=="TriggerEvent":
                    if data[1][0:7]=="prefix=" and len(data)>2:
                        data[2]=data[2].replace("suffix=","")
                        if len(data)>3:
                            data[3]=data[3].replace("payload=","")
                        eg.TriggerEvent(prefix=data[1][7:], suffix=data[2], payload=data[3:])
                    else:
                        self.plugin.TriggerEvent(data[1], data[2:])
                else:
                    self.plugin.TriggerEvent(data[0], data[1:])
                self.end_request(content)
# Enhancement by Sem;colon - END

        else: # JSON request
            methodName = data["method"]
            args = data.get("args", [])
            kwargs = data.get("kwargs", {})
            result = self.plugin.ProcessTheArguments(
                self,
                methodName,
                args,
                kwargs
            )
            content = dumps(result)
            self.end_request(content, 'application/json; charset=UTF-8')


    def do_GET(self):
        """Serve a GET request."""
        self.clAddr = self.getClientAddress()
        if self.plugin.noAutWs:
            # First test, if WebSocket connection
            if str(self.headers.get("Upgrade", None)).lower() == "websocket":
                return self.handshake() #switch to WebSocket !
            if not self.Authenticate():
                return
        else:
            # First do Basic HTTP-Authentication, if set
            if not self.Authenticate():
                return
            if str(self.headers.get("Upgrade", None)).lower() == "websocket":
                return self.handshake() #switch to WebSocket !

        path, dummy, remaining = self.path.partition("?")
        if remaining:
            queries = remaining.split("#", 1)[0].split("&")
            queries = [unquote_plus(part).decode("utf-8") for part in queries]
            if len(queries) > 0:
                event = queries.pop(0).strip()
                if "withoutRelease" in queries:
                    queries.remove("withoutRelease")
                    event = self.plugin.TriggerEnduringEvent(event, queries)
                    while not event.isEnded:
                        sleep(0.05)
                elif event == "ButtonReleased":
                    self.plugin.EndLastEvent()
                else:
                    event = self.plugin.TriggerEvent(event, queries)
                    while not event.isEnded:
                        sleep(0.05)
        try:
            self.SendContent(path)
        except Exception, exc:
            self.plugin.EndLastEvent()
            eg.PrintError("Webserver error", self.path)
            eg.PrintError("Exception", unicode(exc))
            if exc.args[0] == 10053: # Software caused connection abort
                pass
            elif exc.args[0] == 10054: # Connection reset by peer
                pass
            else:
                raise


    def log_message(self, format, *args):
        pass


    def copyfile(self, src, dst):
        dst.write(src.read())


    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # stolen from SimpleHTTPServer.SimpleHTTPRequestHandler
        # but changed to handle files from a defined basepath instead
        # of os.getcwd()
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        path = normpath(unquote(path))
        words = [word for word in path.split('/') if word]
        path = self.basepath
        for word in words:
            drive, word = splitdrive(word)
            head, word = split(word)
            if word in (curdir, pardir):
                continue
            path = join(path, word)
        return path
#===============================================================================

class WsBroadcastMessage(eg.ActionBase):
    eg_event = None
    eg_result = None

    class text:
        mess = "Message for broadcast:"
        err = 'Error in action "Websocket broadcast message(%s)"'
        onlyChange = "Data send only if it has been changed"
        period = "Sending period [s]:"

    def Task(self, _, cond, message):
        if self.plugin.info.isStarted:
            self.task = eg.scheduler.AddTask(
                    self.period,
                    self.Task,
                    None,
                    cond,
                    message
                )

        if not self.pars:
            message = self.plugin.EvalString2(message, self)
        cond = self.plugin.EvalString(cond, self) if cond != "" else True

        if cond:
            if message != self.message or not self.onlyChange:
                self.plugin.BroadcastMessage(message)
        self.message = message


    def __call__(
        self,
        message = "",
        pars = False,
        onlyChange = True,
        cond = "",
        period = 5.0
    ):
        self.message = None
        self.onlyChange = onlyChange
        self.period = period
        self.pars = pars

        self.eg_event = eg.event
        self.eg_result = eg.result
        message = replInstVal(message)
        cond = replInstVal(cond)

        if self.value:
            self.Task(None, cond, message)
        else:
            if not pars:
                message = self.plugin.EvalString2(message, self)
            cond = self.plugin.EvalString(cond, self) if cond != "" else True
            if cond:
                self.plugin.BroadcastMessage(message)


    def Configure(
        self,
        message = "",
        pars = False,
        onlyChange = True,
        cond = "",
        period = 5.0
    ):
        text = self.text
        panel = eg.ConfigPanel()
        messCtrl = wx.TextCtrl(panel, -1, message)
        parsCtrl = wx.CheckBox(panel, -1, self.plugin.text.parsing)
        parsCtrl.SetValue(pars)
        condLabel = wx.StaticText(panel, -1, self.plugin.text.cond)
        condCtrl = wx.TextCtrl(panel, -1, cond)
        messSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.mess),
            wx.VERTICAL
        )
        messSizer.Add(messCtrl, 0, wx.EXPAND)
        messSizer.Add(parsCtrl, 0, wx.EXPAND|wx.TOP, 3)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(messSizer, 0, wx.EXPAND|wx.TOP, 15)
        mainSizer.Add(condLabel,0,wx.TOP,10)
        mainSizer.Add(condCtrl,0,wx.EXPAND|wx.TOP,2)
        panel.sizer.Add(mainSizer, 0, wx.EXPAND|wx.TOP, 15)


        if self.value:
            periodLabel = wx.StaticText(panel, -1, text.period)
            periodCtrl = eg.SpinNumCtrl(
                panel,
                -1,
                period,
                integerWidth = 5,
                fractionWidth = 1,
                allowNegative = False,
                min = 0.1,
                increment = 0.1,
            )
            changeCtrl = wx.CheckBox(panel, -1, text.onlyChange)
            changeCtrl.SetValue(onlyChange)
            perSizer = wx.BoxSizer(wx.HORIZONTAL)
            perSizer.Add(periodLabel,0,ACV)
            perSizer.Add(periodCtrl,0,wx.LEFT,1)
            perSizer.Add((-1,-1),1,wx.EXPAND)
            perSizer.Add(changeCtrl,0,wx.TOP,4)
            mainSizer.Add(perSizer,0,wx.EXPAND|wx.TOP,10)
        panel.sizer.Layout()


        while panel.Affirmed():
            change = changeCtrl.GetValue() if self.value else None
            period = periodCtrl.GetValue() if self.value else None
            panel.SetResult(
                messCtrl.GetValue(),
                parsCtrl.GetValue(),
                change,
                condCtrl.GetValue(),
                period,
            )
#===============================================================================

class WsBroadcastValue(eg.ActionBase):
    eg_event = None
    eg_result = None

    class text:
        varnames = "Variable name or list of variables (separated by commas):"
        err = 'Error in action "Websocket send values(%s)"'
        onlyChange = "Data send only if it has been changed"
        period = "Sending period [s]:"

    def Task(self, _, cond, varnames):
        if self.plugin.info.isStarted:
            self.task = eg.scheduler.AddTask(
                    self.period,
                    self.Task,
                    None,
                    cond,
                    varnames
                )
        varnames = self.plugin.EvalString(varnames, self)
        cond = self.plugin.EvalString(cond, self) if cond != "" else True
        if cond:
            try:
                keys = varnames.replace(" ", "")
                keys = keys.split(",")
            except:
                eg.PrintError(self.text.err % str(varnames))
                return
            try:
                vals = {}
                for key in keys:
                    k = self.plugin.EvalString(key, self)
                    vals[k] = self.plugin.GetUniValue(k)
            except:
                eg.PrintError(self.text.err % str(varnames))




            if vals != self.vals or not self.onlyChange:

                self.plugin.BroadcastMessage(
                    dumps({'method' :'Values', 'kwargs':vals}),
                )
        self.vals = vals


    def __call__(
        self,
        varnames = "",
        onlyChange = True,
        cond = "",
        period = 5.0
    ):
        self.varnames = varnames
        self.onlyChange = onlyChange
        self.period = period
        self.vals = None

        self.eg_event = eg.event
        self.eg_result = eg.result
        cond = replInstVal(cond)

        if self.value:
            self.Task(None, cond, varnames)
        else:
            try:
                keys = varnames.replace(" ", "")
                keys = keys.split(",")
            except:
                eg.PrintError(self.text.err % str(varnames))
                return
            try:
                vals = {}
                for key in keys:
                    k = self.plugin.EvalString(key, self)
                    vals[k] = self.plugin.GetUniValue(k)
            except:
                eg.PrintError(self.text.err % str(varnames))

            cond = self.plugin.EvalString(cond, self) if cond != "" else True
            if cond:
                self.plugin.BroadcastMessage(
                    dumps({'method' :'Values', 'kwargs':vals}),
                )


    def GetLabel(
        self,
        varnames,
        onlyChange,
        cond,
        period
    ):
        return "%s: %s" % (self.name, varnames)


    def Configure(
        self,
        varnames = "",
        onlyChange = True,
        cond = "",
        period = 5.0
    ):
        text = self.text
        panel = eg.ConfigPanel()
        sendLabel = wx.StaticText(panel, -1, text.varnames)
        condLabel = wx.StaticText(panel, -1, self.plugin.text.cond)
        sendCtrl = wx.TextCtrl(panel, -1, varnames)
        condCtrl = wx.TextCtrl(panel, -1, cond)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sendLabel,0,wx.TOP,10)
        mainSizer.Add(sendCtrl,0,wx.EXPAND|wx.TOP,2)
        mainSizer.Add(condLabel,0,wx.TOP,10)
        mainSizer.Add(condCtrl,0,wx.EXPAND|wx.TOP,2)
        panel.sizer.Add(mainSizer,0,wx.ALL|wx.EXPAND,10)
        if self.value:
            periodLabel = wx.StaticText(panel, -1, text.period)
            periodCtrl = eg.SpinNumCtrl(
                panel,
                -1,
                period,
                integerWidth = 5,
                fractionWidth = 1,
                allowNegative = False,
                min = 0.1,
                increment = 0.1,
            )
            changeCtrl = wx.CheckBox(panel, -1, text.onlyChange)
            changeCtrl.SetValue(onlyChange)
            perSizer = wx.BoxSizer(wx.HORIZONTAL)
            perSizer.Add(periodLabel, 0, ACV)
            perSizer.Add(periodCtrl,0,wx.LEFT,1)
            perSizer.Add((-1,-1),1,wx.EXPAND)
            perSizer.Add(changeCtrl,0,wx.TOP,4)
            mainSizer.Add(perSizer,0,wx.EXPAND|wx.TOP,10)
        panel.sizer.Layout()


        while panel.Affirmed():
            change = changeCtrl.GetValue() if self.value else None
            period = periodCtrl.GetValue() if self.value else None
            panel.SetResult(
                sendCtrl.GetValue(),
                change,
                condCtrl.GetValue(),
                period,
            )
#===============================================================================

class WsBroadcastAllValues(eg.ActionBase):
    eg_event = None
    eg_result = None

    class text:
        onlyChange = "Data send only if it has been changed"
        period = "Sending period [s]:"

    def Task(self, _, cond):
        if self.plugin.info.isStarted:
            self.task = eg.scheduler.AddTask(
                    self.period,
                    self.Task,
                    None,
                    cond
                )
        cond = self.plugin.EvalString(cond, self) if cond != "" else True
        if cond:
            vals = self.plugin.GetAllValues()
            if vals != self.vals or not self.onlyChange:
                self.plugin.BroadcastMessage(
                    dumps(vals),
                )
        self.vals = vals


    def __call__(
        self,
        onlyChange = True,
        cond = "",
        period = 5.0
    ):
        self.onlyChange = onlyChange
        self.period = period
        self.vals = None

        self.eg_event = eg.event
        self.eg_result = eg.result
        cond = replInstVal(cond)

        if self.value:
            self.Task(None, cond)
        else:
            cond = self.plugin.EvalString(cond, self) if cond != "" else True
            if cond:
                vals = self.plugin.GetAllValues()
                self.plugin.BroadcastMessage(
                    dumps(vals),
                )


    def Configure(
        self,
        onlyChange = True,
        cond = "",
        period = 5.0
    ):
        text = self.text
        panel = eg.ConfigPanel()
        condLabel = wx.StaticText(panel, -1, self.plugin.text.cond)
        condCtrl = wx.TextCtrl(panel, -1, cond)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(condLabel,0,wx.TOP,10)
        mainSizer.Add(condCtrl,0,wx.EXPAND|wx.TOP,2)
        panel.sizer.Add(mainSizer,0,wx.ALL|wx.EXPAND,10)
        if self.value:
            periodLabel = wx.StaticText(panel, -1, text.period)
            periodCtrl = eg.SpinNumCtrl(
                panel,
                -1,
                period,
                integerWidth = 5,
                fractionWidth = 1,
                allowNegative = False,
                min = 0.1,
                increment = 0.1,
            )
            changeCtrl = wx.CheckBox(panel, -1, text.onlyChange)
            changeCtrl.SetValue(onlyChange)
            perSizer = wx.BoxSizer(wx.HORIZONTAL)
            perSizer.Add(periodLabel, 0, ACV)
            perSizer.Add(periodCtrl,0,wx.LEFT,1)
            perSizer.Add((-1,-1),1,wx.EXPAND)
            perSizer.Add(changeCtrl,0,wx.TOP,4)
            mainSizer.Add(perSizer,0,wx.EXPAND|wx.TOP,10)
        panel.sizer.Layout()


        while panel.Affirmed():
            change = changeCtrl.GetValue() if self.value else None
            period = periodCtrl.GetValue() if self.value else None
            panel.SetResult(
                change,
                condCtrl.GetValue(),
                period,
            )
#===============================================================================

class WsBroadcastData(eg.ActionBase):
    eg_event = None
    eg_result = None

    class text:
        dataName = "Data name:"
        data2send = "Data for broadcast (python expression):"
        onlyChange = "Data send only if it has been changed"
        cond = "Condition for data sending (python expression):"
        period = "Sending period [s]:"
 

    def Task(self, _, cond, dataName, data2send):
        if self.plugin.info.isStarted:
            self.task = eg.scheduler.AddTask(
                self.period,
                self.Task,
                None,
                cond,
                dataName,
                data2send
            )

        dataName = self.plugin.EvalString(dataName, self)
        data = self.plugin.EvalString(data2send, self)
        cond = self.plugin.EvalString(cond, self) if cond != "" else True
        if cond:
            if data != self.data or not self.onlyChange:
                self.plugin.BroadcastMessage(
                    dumps(
                        {'method' :'Data', 'dataName':dataName, 'data':data}
                    )
                )
        self.data = data
        

    def __call__(
        self,
        dataName = "",
        data2send = "",
        cond = "",
        onlyChange = True,
        period = 5.0
    ):
        self.onlyChange = onlyChange
        self.period = period
        self.data = None

        self.eg_event = eg.event
        self.eg_result = eg.result
        dataName = replInstVal(dataName)
        data2send = replInstVal(data2send)
        cond = replInstVal(cond)

        if self.value:
            self.Task(None, cond, dataName, data2send)
        else:
            dataName = self.plugin.EvalString(dataName, self)
            data = self.plugin.EvalString(data2send, self)
            cond = self.plugin.EvalString(cond, self) if cond != "" else True
            if cond:
                self.plugin.BroadcastMessage(
                    dumps(
                        {'method' :'Data', 'dataName':dataName, 'data':data}
                    )
                )


    def Configure(
        self,
        dataName = "",
        data2send = "",
        cond = "",
        onlyChange = True,
        period = 5.0
    ):
        panel = eg.ConfigPanel(self)
        text = self.text
        nameLabel = wx.StaticText(panel, -1, text.dataName)
        sendLabel = wx.StaticText(panel, -1, text.data2send)
        condLabel = wx.StaticText(panel, -1, text.cond)
        nameCtrl = wx.TextCtrl(panel, -1, dataName)
        sendCtrl = wx.TextCtrl(panel, -1, data2send)
        condCtrl = wx.TextCtrl(panel, -1, cond)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(nameLabel)
        mainSizer.Add(nameCtrl,0,wx.EXPAND|wx.TOP,2)
        mainSizer.Add(sendLabel,0,wx.TOP,10)
        mainSizer.Add(sendCtrl,0,wx.EXPAND|wx.TOP,2)
        mainSizer.Add(condLabel,0,wx.TOP,10)
        mainSizer.Add(condCtrl,0,wx.EXPAND|wx.TOP,2)
        panel.sizer.Add(mainSizer,0,wx.ALL|wx.EXPAND,10)
        if self.value:
            periodLabel = wx.StaticText(panel, -1, text.period)
            changeCtrl = wx.CheckBox(panel, -1, text.onlyChange)
            changeCtrl.SetValue(onlyChange)
            periodCtrl = eg.SpinNumCtrl(
                panel,
                -1,
                period,
                integerWidth = 5,
                fractionWidth = 1,
                allowNegative = False,
                min = 0.1,
                increment = 0.1,
            )
            perSizer = wx.BoxSizer(wx.HORIZONTAL)
            perSizer.Add(periodLabel, 0, ACV)
            perSizer.Add(periodCtrl,0,wx.LEFT,1)
            perSizer.Add((-1,-1),1,wx.EXPAND)
            perSizer.Add(changeCtrl,0,wx.TOP,4)
            mainSizer.Add(perSizer,0,wx.EXPAND|wx.TOP,10)
       
        while panel.Affirmed():
            change = changeCtrl.GetValue() if self.value else None
            period = periodCtrl.GetValue() if self.value else None
            panel.SetResult(
                nameCtrl.GetValue(),
                sendCtrl.GetValue(),
                condCtrl.GetValue(),
                change,
                period
            )
#===============================================================================

class WsBroadcastCommand(eg.ActionBase):
    eg_event = None
    eg_result = None

    class text:
        cond = "Condition:"
        cmdName = "Command name:"
        arg1 = "Argument 1:"
        arg2 = "Argument 2:"
        arg3 = "Argument 3:"
        othArgs = "Arguments:"
        kwArgs = "Keyw. arguments:"
        onlyChange = "Data send only if it has been changed"
        period = "Sending period [s]:"
        

    def Task(self, _, cond, cmdName, arg1, arg2, arg3, othArgs, kwArgs):
        if self.plugin.info.isStarted:
            self.task = eg.scheduler.AddTask(
                self.period,
                self.Task,
                None,
                cond,
                cmdName,
                arg1,
                arg2,
                arg3,
                othArgs,
                kwArgs
            )

        cmdName = self.plugin.EvalString(cmdName)
        args = [self.plugin.EvalString(arg1, self)] if self.arg1 != "" else []
        if self.arg2 != "":
            args.append(self.plugin.EvalString(arg2, self))
        if self.arg3 != "":
            args.append(self.plugin.EvalString(arg3, self))
        if self.othArgs != "":
            try:
                othArgs = list(self.plugin.EvalString(othArgs, self))
                args.extend(othArgs)
            except:
                pass
        kwargs = {}
        if self.kwArgs != "":
            try:
                kwargs = dict(self.plugin.EvalString2(kwArgs, self))
            except:
                pass
        cond = self.plugin.EvalString(cond, self) if cond != "" else True
        if cond:
            if args != self.args or kwargs != self.kwargs or not self.onlyChange:
                self.plugin.BroadcastMessage(
                    dumps(
                        {
                            'method' :'Command',
                            'cmdName':cmdName,
                            'args':args,
                            'kwargs':kwargs
                        }
                    )
                )
        self.args = args
        self.kwargs = kwargs


    def __call__(
        self,
        cmdName = "",
        cond = "",
        arg1 = "",
        arg2 = "",
        arg3 = "",
        othArgs = "",
        kwArgs = "",
        onlyChange = True,
        period = 5.0
    ):


        self.eg_event = eg.event
        self.eg_result = eg.result
        cmdName = replInstVal(cmdName)
        arg1 = replInstVal(arg1)
        arg2 = replInstVal(arg2)
        arg3 = replInstVal(arg3)
        othArgs = replInstVal(othArgs)
        kwArgs = replInstVal(kwArgs)
        cond = replInstVal(cond)
        if self.value:
            self.onlyChange = onlyChange
            self.period = period
            self.args = None
            self.kwargs = None
            self.Task(
                None,
                cond,
                cmdName,
                arg1,
                arg2,
                arg3,
                othArgs,
                kwArgs
            )
        else:
            cmdName = self.plugin.EvalString(cmdName)
            args = [self.plugin.EvalString(arg1, self)] if arg1 != "" else []
            if arg2 != "":
                args.append(self.plugin.EvalString(arg2, self))
            if arg3 != "":
                args.append(self.plugin.EvalString(arg3, self))
            if othArgs != "":
                try:
                    othArgs = list(self.plugin.EvalString(othArgs, self))
                    args.extend(othArgs)
                except:
                    pass
            kwargs = {}
            if kwArgs != "":
                try:
                    kwargs = dict(self.plugin.EvalString2(kwArgs, self))
                except:
                    pass
            cond = self.plugin.EvalString(cond, self) if cond != "" else True
            if cond:
                self.plugin.BroadcastMessage(
                    dumps(
                        {
                            'method' :'Command',
                            'cmdName':cmdName,
                            'args':args,
                            'kwargs':kwargs
                        }
                    )
                )


    def Configure(
        self,
        cmdName = "",
        cond = "",
        arg1 = "",
        arg2 = "",
        arg3 = "",
        othArgs = "",
        kwArgs = "",
        onlyChange = True,
        period = 5.0
    ):
        panel = eg.ConfigPanel(self)
        text = self.text
        nameLabel = wx.StaticText(panel, -1, text.cmdName)
        condLabel = wx.StaticText(panel, -1, text.cond)
        arg1Label = wx.StaticText(panel, -1, text.arg1)
        arg2Label = wx.StaticText(panel, -1, text.arg2)
        arg3Label = wx.StaticText(panel, -1, text.arg3)
        othLabel = wx.StaticText(panel, -1, text.othArgs)
        kwLabel = wx.StaticText(panel, -1, text.kwArgs)
        nameCtrl = wx.TextCtrl(panel, -1, cmdName)
        condCtrl = wx.TextCtrl(panel, -1, cond)
        arg1Ctrl = wx.TextCtrl(panel, -1, arg1)
        arg2Ctrl = wx.TextCtrl(panel, -1, arg2)
        arg3Ctrl = wx.TextCtrl(panel, -1, arg3)
        othCtrl = wx.TextCtrl(panel, -1, othArgs)
        kwCtrl = wx.TextCtrl(panel, -1, kwArgs)
        mainSizer = wx.FlexGridSizer(7, 2, 2, 10)
        mainSizer.AddGrowableCol(1)
        mainSizer.Add(nameLabel, 0, ACV)
        mainSizer.Add(nameCtrl,0,wx.EXPAND)
        mainSizer.Add(arg1Label, 0, ACV)
        mainSizer.Add(arg1Ctrl,0,wx.EXPAND)
        mainSizer.Add(arg2Label, 0, ACV)
        mainSizer.Add(arg2Ctrl,0,wx.EXPAND)
        mainSizer.Add(arg3Label, 0, ACV)
        mainSizer.Add(arg3Ctrl,0,wx.EXPAND)
        mainSizer.Add(othLabel, 0, ACV)
        mainSizer.Add(othCtrl,0,wx.EXPAND)
        mainSizer.Add(kwLabel, 0, ACV)
        mainSizer.Add(kwCtrl,0,wx.EXPAND)
        mainSizer.Add(condLabel, 0, ACV)
        mainSizer.Add(condCtrl,0,wx.EXPAND)
        panel.sizer.Add(mainSizer,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
        if self.value:
            periodLabel = wx.StaticText(panel, -1, text.period)
            periodCtrl = eg.SpinNumCtrl(
                panel,
                -1,
                period,
                integerWidth = 5,
                fractionWidth = 1,
                allowNegative = False,
                min = 0.1,
                increment = 0.1,
            )
            changeCtrl = wx.CheckBox(panel, -1, text.onlyChange)
            changeCtrl.SetValue(onlyChange)
            perSizer = wx.BoxSizer(wx.HORIZONTAL)
            perSizer.Add(periodCtrl,0,wx.LEFT,1)
            perSizer.Add((-1,-1),1,wx.EXPAND)
            perSizer.Add(changeCtrl,0,wx.TOP,4)
            mainSizer.Add(periodLabel, 0, ACV)
            mainSizer.Add(perSizer,0,wx.EXPAND)

        while panel.Affirmed():
            change = changeCtrl.GetValue() if self.value else None
            period = periodCtrl.GetValue() if self.value else None
            panel.SetResult(
                nameCtrl.GetValue(),
                condCtrl.GetValue(),
                arg1Ctrl.GetValue(),
                arg2Ctrl.GetValue(),
                arg3Ctrl.GetValue(),
                othCtrl.GetValue(),
                kwCtrl.GetValue(),
                change,
                period
            )
#===============================================================================

class WsBroadcastUniversal(eg.ActionBase):
    eg_event = None
    eg_result = None

    class text:
        cond = "Condition:"
        method = "Method:"
        othArgs = "Arguments:"
        kwArgs = "Keyw. arguments:"
        onlyChange = "Data send only if it has been changed"
        period = "Sending period [s]:"
        

    def Task(self, _, cond, method, othArgs, kwArgs):
        if self.plugin.info.isStarted:
            self.task = eg.scheduler.AddTask(
                self.period,
                self.Task,
                None,
                cond,
                method,
                othArgs,
                kwArgs
            )
        args = []
        if othArgs != "":
            try:
                args = list(self.plugin.EvalString(othArgs, self))
            except:
                pass
        kwargs = {}
        if kwArgs != "":
            try:
                kwargs = dict(self.plugin.EvalString2(kwArgs, self))
            except:
                pass
        cond = self.plugin.EvalString(cond, self) if cond != "" else True
        if cond:
            if args != self.args or kwargs != self.kwargs or not self.onlyChange:
                self.plugin.BroadcastMessage(
                    dumps(
                        {
                            'method' :method,
                            'args':args,
                            'kwargs':kwargs
                        }
                    )
                )
        self.args = args
        self.kwargs = kwargs


    def __call__(
        self,
        method = "",
        cond = "",
        othArgs = "",
        kwArgs = "",
        onlyChange = True,
        period = 5.0
    ):
        self.eg_event = eg.event
        self.eg_result = eg.result
        othArgs = replInstVal(othArgs)
        kwArgs = replInstVal(kwArgs)
        cond = replInstVal(cond)
        if self.value:
            self.period = period
            self.args = None
            self.kwargs = None
            self.Task(
                None,
                cond,
                method,
                othArgs,
                kwArgs
                )
        else:
            args = []
            if othArgs != "":
                try:
                    args = list(self.plugin.EvalString(othArgs, self))
                except:
                    pass
            kwargs = {}
            if kwArgs != "":
                try:
                    kwargs = dict(self.plugin.EvalString2(kwArgs, self))
                except:
                    pass
            cond = self.plugin.EvalString(cond, self) if cond != "" else True
            if cond:
                self.plugin.BroadcastMessage(
                    dumps(
                        {
                            'method' :method,
                            'args':args,
                            'kwargs':kwargs
                        }
                    ),
                )


    def GetLabel(
        self,
        method,
        cond,
        othArgs,
        kwArgs,
        onlyChange,
        period
    ):
        return "%s: %s" % (self.name, method)


    def Configure(
        self,
        method = "",
        cond = "",
        othArgs = "",
        kwArgs = "",
        onlyChange = True,
        period = 5.0
    ):
        panel = eg.ConfigPanel(self)
        text = self.text
        staticBox = wx.StaticBox(panel, -1, "")
        methodLabel = wx.StaticText(panel, -1, text.method)
        condLabel = wx.StaticText(panel, -1, text.cond)
        othLabel = wx.StaticText(panel, -1, text.othArgs)
        kwLabel = wx.StaticText(panel, -1, text.kwArgs)
        methodCtrl = wx.ComboBox(
            panel,
            -1,
            choices = METHODS[:8],
            style = wx.CB_DROPDOWN
        )
        methodCtrl.SetValue(method)
        condCtrl = wx.TextCtrl(panel, -1, cond)
        othCtrl = wx.TextCtrl(panel, -1, othArgs)
        kwCtrl = wx.TextCtrl(panel, -1, kwArgs)
        mainSizer = wx.FlexGridSizer(5, 2, 8, 10)
        mainSizer.AddGrowableCol(1)
        mainSizer.Add(methodLabel, 0, ACV)
        mainSizer.Add(methodCtrl,0,wx.EXPAND)
        mainSizer.Add(othLabel, 0, ACV)
        mainSizer.Add(othCtrl,0,wx.EXPAND)
        mainSizer.Add(kwLabel, 0, ACV)
        mainSizer.Add(kwCtrl,0,wx.EXPAND)
        mainSizer.Add(condLabel, 0, ACV)
        mainSizer.Add(condCtrl,0,wx.EXPAND)
        if self.value:
            periodLabel = wx.StaticText(panel, -1, text.period)
            periodCtrl = eg.SpinNumCtrl(
                panel,
                -1,
                period,
                integerWidth = 5,
                fractionWidth = 1,
                allowNegative = False,
                min = 0.1,
                increment = 0.1,
            )
            changeCtrl = wx.CheckBox(panel, -1, text.onlyChange)
            changeCtrl.SetValue(onlyChange)
            perSizer = wx.BoxSizer(wx.HORIZONTAL)
            mainSizer.Add(periodLabel, 0, ACV)
            perSizer.Add(periodCtrl,0,wx.LEFT,1)
            perSizer.Add((-1,-1),1,wx.EXPAND)
            perSizer.Add(changeCtrl,0,wx.TOP,4)
            mainSizer.Add(perSizer,0,wx.EXPAND)
        panel.sizer.Add(mainSizer,0,wx.ALL|wx.EXPAND,8)
       
        while panel.Affirmed():
            change = changeCtrl.GetValue() if self.value else None
            period = periodCtrl.GetValue() if self.value else None
            panel.SetResult(
                methodCtrl.GetValue(),
                condCtrl.GetValue(),
                othCtrl.GetValue(),
                kwCtrl.GetValue(),
                change,
                period
            )
#===============================================================================

class WsSendMessage(eg.ActionBase):
    eg_event = None
    eg_result = None

    class text:
        mess = "Message to send:"
        cond = "Condition for data sending (python expression):"
        onlyChange = "Data send only if it has been changed"
        period = "Sending period [s]:"
        err = 'Error in action "Websocket send values(%s)"'
        cond = "Condition for data sending (python expression):"
        onlyChange = "Data send only if it has been changed"
        period = "Sending period [s]:"

    def Task(self, client, cond, message):
        if self.plugin.info.isStarted:
            self.task = eg.scheduler.AddTask(
                    self.period,
                    self.Task,
                    client,
                    cond,
                    message
                )

        if not self.pars:
            message = self.plugin.EvalString2(message, self)
        cond = self.plugin.EvalString(cond, self) if cond != "" else True
        if cond:
            if message != self.message or not self.onlyChange:
                self.plugin.ServerSendMessage(
                    client,
                    message,
                )
        self.message = message

    def __call__(
        self,
        cl_ip = "127.0.0.1",
        cl_port = "1234",
        modeClient = 1,
        message = "",
        pars = False,
        onlyChange = True,
        cond = "",
        period = 5.0
    ):
        self.message = None
        self.onlyChange = onlyChange
        self.period = period
        self.pars = pars

        self.eg_event = eg.event
        self.eg_result = eg.result
        message = replInstVal(message)
        cond = replInstVal(cond)
        client = eg.event.payload[0] if modeClient else (
            eg.ParseString(cl_ip),
            int(eg.ParseString(cl_port))
        )
        if self.value:
            self.Task(client, cond, message)
        else:
            if not pars:
                message = self.plugin.EvalString2(message, self)
            cond = self.plugin.EvalString(cond, self) if cond != "" else True
            if cond:
                self.plugin.ServerSendMessage(
                    client,
                    message,
                )


    def GetLabel(
        self,
        cl_ip,
        cl_port,
        modeClient,
        message,
        pars,
        onlyChange,
        cond,
        period
    ):
        if modeClient:
            client = "{eg.event.payload[0]}"
            return "%s: %s: %s" % (self.name, client, message)
        else:
            return "%s: %s:%s: %s" % (self.name, cl_ip, cl_port, message)


    def Configure(
        self,
        cl_ip = "127.0.0.1",
        cl_port = "1234",
        modeClient = 1,
        message = "",
        pars = False,
        onlyChange = True,
        cond = "",
        period = 5.0
    ):
        text = self.text
        panel = eg.ConfigPanel()
        id2 = wx.NewId()
        id3 = wx.NewId()
        id4 = wx.NewId()
        radioBoxModeClient = wx.RadioBox(
            panel,
            -1,
            self.plugin.text.modeClientChoiceLabel,
            choices = self.plugin.text.modeClientChoice,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxModeClient.SetSelection(modeClient)
        staticBox = wx.StaticBox(panel, -1, "")
        tmpSizer = wx.GridBagSizer(2, 10)
        txtLabel = wx.StaticText(panel,-1,self.plugin.text.host)
        txtCtrl = wx.TextCtrl(panel,id3,"")
        portLabel = wx.StaticText(panel,-1,self.plugin.text.port)
        portCtrl = wx.TextCtrl(panel,id2,"")
        tmpSizer.Add(txtLabel,(0,0),(1,1))
        tmpSizer.Add(txtCtrl,(1,0),(1,1),flag = wx.EXPAND)
        tmpSizer.Add(portLabel,(2,0),(1,1),flag = wx.TOP, border = 10)
        tmpSizer.Add(portCtrl,(3,0),(1,1))
        middleSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        middleSizer.Add(radioBoxModeClient,0,wx.LEFT|wx.EXPAND)
        middleSizer.Add((20,-1),0,wx.LEFT|wx.EXPAND)
        middleSizer.Add(tmpSizer,0,wx.LEFT|wx.EXPAND)
        panel.sizer.Add(middleSizer, 0, wx.TOP|wx.EXPAND, 8)
        condLabel = wx.StaticText(panel, -1, text.cond)
        messCtrl = wx.TextCtrl(panel, -1, message)
        parsCtrl = wx.CheckBox(panel, -1, self.plugin.text.parsing)
        parsCtrl.SetValue(pars)
        if self.value:
            parsCtrl.Show(False)
        condCtrl = wx.TextCtrl(panel, -1, cond)
        messSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.mess),
            wx.VERTICAL
        )
        messSizer.Add(messCtrl, 0, wx.EXPAND)
        messSizer.Add(parsCtrl, 0, wx.EXPAND|wx.TOP, 3)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(messSizer, 0, wx.EXPAND|wx.TOP, 15)
        mainSizer.Add(condLabel,0,wx.TOP,10)
        mainSizer.Add(condCtrl,0,wx.EXPAND|wx.TOP,2)
        panel.sizer.Add(mainSizer,0,wx.ALL|wx.EXPAND,10)
        if self.value:
            periodLabel = wx.StaticText(panel, -1, text.period)
            periodCtrl = eg.SpinNumCtrl(
                panel,
                -1,
                period,
                integerWidth = 5,
                fractionWidth = 1,
                allowNegative = False,
                min = 0.1,
                increment = 0.1,
            )
            changeCtrl = wx.CheckBox(panel, -1, text.onlyChange)
            changeCtrl.SetValue(onlyChange)
            perSizer = wx.BoxSizer(wx.HORIZONTAL)
            perSizer.Add(periodLabel, 0, ACV)
            perSizer.Add(periodCtrl,0,wx.LEFT,1)
            perSizer.Add((-1,-1),1,wx.EXPAND)
            perSizer.Add(changeCtrl,0,wx.TOP,4)
            mainSizer.Add(perSizer,0,wx.EXPAND|wx.TOP,10)
        panel.sizer.Layout()
        size2 = (-1, tmpSizer.GetMinSize()[1])

        def OnClientChoice(evt = None):
            ClientChoice(
                evt,
                self.plugin.text,
                panel,
                id3,
                id4,
                cl_ip,
                cl_port,
                size2,
                radioBoxModeClient
        )
        radioBoxModeClient.Bind(wx.EVT_RADIOBOX, OnClientChoice)
        OnClientChoice()

        while panel.Affirmed():
            modeClient = radioBoxModeClient.GetSelection()
            if not modeClient:
                cl_ip = wx.FindWindowById(id3).GetValue()
                cl_port = wx.FindWindowById(id4).GetValue()
            change = changeCtrl.GetValue() if self.value else None
            period = periodCtrl.GetValue() if self.value else None
            panel.SetResult(
                cl_ip,
                cl_port,
                modeClient,
                messCtrl.GetValue(),
                parsCtrl.GetValue(),
                change,
                condCtrl.GetValue(),
                period,
            )
#===============================================================================

class WsSendValue(eg.ActionBase):
    eg_event = None
    eg_result = None

    class text:
        varnames = "Variable name or list of variables (separated by commas):"
        err = 'Error in action "Websocket send values(%s)"'
        cond = "Condition for data sending (python expression):"
        onlyChange = "Data send only if it has been changed"
        period = "Sending period [s]:"

    def Task(self, client, cond, varnames):
        if self.plugin.info.isStarted:
            self.task = eg.scheduler.AddTask(
                    self.period,
                    self.Task,
                    client,
                    cond,
                    varnames
                )
        varnames = self.plugin.EvalString(varnames, self)
        cond = self.plugin.EvalString(cond, self) if cond != "" else True
        if cond:
            try:
                keys = varnames.replace(" ", "")
                keys = keys.split(",")
            except:
                eg.PrintError(self.text.err % str(varnames))
                return
            try:
                vals = {}
                for key in keys:
                    k = self.plugin.EvalString(key, self)
                    vals[k] = self.plugin.GetUniValue(k)
            except:
                eg.PrintError(self.text.err % str(varnames))

            if vals != self.vals or not self.onlyChange:

                self.plugin.ServerSendMessage(
                    client,
                    dumps({'method' :'Values', 'kwargs':vals}),
                )
        self.vals = vals


    def __call__(
        self,
        cl_ip = "127.0.0.1",
        cl_port = "1234",
        modeClient = 1,
        varnames = "",
        onlyChange = True,
        cond = "",
        period = 5.0
    ):
        self.varnames = varnames
        self.onlyChange = onlyChange
        self.period = period
        self.vals = None
        self.eg_event = eg.event
        self.eg_result = eg.result
        cond = replInstVal(cond)
        client = eg.event.payload[0] if modeClient else (
            eg.ParseString(cl_ip),
            int(eg.ParseString(cl_port))
        )
        if self.value:
            self.Task(client, cond, varnames)
        else:
            try:
                keys = varnames.replace(" ", "")
                keys = keys.split(",")
            except:
                eg.PrintError(self.text.err % str(varnames))
                return
            try:
                vals = {}
                for key in keys:
                    k = self.plugin.EvalString(key, self)
                    vals[k] = self.plugin.GetUniValue(k)
            except:
                eg.PrintError(self.text.err % str(varnames))
            cond = self.plugin.EvalString(cond, self) if cond != "" else True
            if cond:
                self.plugin.ServerSendMessage(
                    client,
                    dumps({'method' :'Values', 'kwargs':vals}),
                )


    def GetLabel(
        self,
        cl_ip,
        cl_port,
        modeClient,
        varnames,
        onlyChange,
        cond,
        period
    ):
        if modeClient:
            client = "{eg.event.payload[0]}"
            return "%s: %s: %s" % (self.name, client, varnames)
        else:
            return "%s: %s:%s: %s" % (self.name, cl_ip, cl_port, varnames)


    def Configure(
        self,
        cl_ip = "127.0.0.1",
        cl_port = "1234",
        modeClient = 1,
        varnames = "",
        onlyChange = True,
        cond = "",
        period = 5.0
    ):
        text = self.text
        panel = eg.ConfigPanel()
        id2 = wx.NewId()
        id3 = wx.NewId()
        id4 = wx.NewId()
        radioBoxModeClient = wx.RadioBox(
            panel,
            -1,
            self.plugin.text.modeClientChoiceLabel,
            choices = self.plugin.text.modeClientChoice,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxModeClient.SetSelection(modeClient)
        staticBox = wx.StaticBox(panel, -1, "")
        tmpSizer = wx.GridBagSizer(2, 10)
        txtLabel = wx.StaticText(panel,-1,self.plugin.text.host)
        txtCtrl = wx.TextCtrl(panel,id3,"")
        portLabel = wx.StaticText(panel,-1,self.plugin.text.port)
        portCtrl = wx.TextCtrl(panel,id2,"")
        tmpSizer.Add(txtLabel,(0,0),(1,1))
        tmpSizer.Add(txtCtrl,(1,0),(1,1),flag = wx.EXPAND)
        tmpSizer.Add(portLabel,(2,0),(1,1),flag = wx.TOP, border = 10)
        tmpSizer.Add(portCtrl,(3,0),(1,1))
        middleSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        middleSizer.Add(radioBoxModeClient,0,wx.LEFT|wx.EXPAND)
        middleSizer.Add((20,-1),0,wx.LEFT|wx.EXPAND)
        middleSizer.Add(tmpSizer,0,wx.LEFT|wx.EXPAND)
        panel.sizer.Add(middleSizer, 0, wx.TOP|wx.EXPAND, 8)
        sendLabel = wx.StaticText(panel, -1, text.varnames)
        condLabel = wx.StaticText(panel, -1, text.cond)
        sendCtrl = wx.TextCtrl(panel, -1, varnames)
        condCtrl = wx.TextCtrl(panel, -1, cond)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sendLabel,0,wx.TOP,10)
        mainSizer.Add(sendCtrl,0,wx.EXPAND|wx.TOP,2)
        mainSizer.Add(condLabel,0,wx.TOP,10)
        mainSizer.Add(condCtrl,0,wx.EXPAND|wx.TOP,2)
        panel.sizer.Add(mainSizer,0,wx.ALL|wx.EXPAND,10)
        if self.value:
            periodLabel = wx.StaticText(panel, -1, text.period)
            periodCtrl = eg.SpinNumCtrl(
                panel,
                -1,
                period,
                integerWidth = 5,
                fractionWidth = 1,
                allowNegative = False,
                min = 0.1,
                increment = 0.1,
            )
            changeCtrl = wx.CheckBox(panel, -1, text.onlyChange)
            changeCtrl.SetValue(onlyChange)
            perSizer = wx.BoxSizer(wx.HORIZONTAL)
            perSizer.Add(periodLabel, 0, ACV)
            perSizer.Add(periodCtrl,0,wx.LEFT,1)
            perSizer.Add((-1,-1),1,wx.EXPAND)
            perSizer.Add(changeCtrl,0,wx.TOP,4)
            mainSizer.Add(perSizer,0,wx.EXPAND|wx.TOP,10)
        panel.sizer.Layout()
        size2 = (-1, tmpSizer.GetMinSize()[1])

        def OnClientChoice(evt = None):
            ClientChoice(
                evt,
                self.plugin.text,
                panel,
                id3,
                id4,
                cl_ip,
                cl_port,
                size2,
                radioBoxModeClient
        )
        radioBoxModeClient.Bind(wx.EVT_RADIOBOX, OnClientChoice)
        OnClientChoice()

        while panel.Affirmed():
            modeClient = radioBoxModeClient.GetSelection()
            if not modeClient:
                cl_ip = wx.FindWindowById(id3).GetValue()
                cl_port = wx.FindWindowById(id4).GetValue()
            change = changeCtrl.GetValue() if self.value else None
            period = periodCtrl.GetValue() if self.value else None
            panel.SetResult(
                cl_ip,
                cl_port,
                modeClient,
                sendCtrl.GetValue(),
                change,
                condCtrl.GetValue(),
                period,
            )
#===============================================================================

class WsSendAllValues(eg.ActionBase):
    eg_event = None
    eg_result = None

    class text:
        cond = "Condition for data sending (python expression):"
        onlyChange = "Data send only if it has been changed"
        period = "Sending period [s]:"


    def Task(self, client, cond):
        if self.plugin.info.isStarted:
            self.task = eg.scheduler.AddTask(
                    self.period,
                    self.Task,
                    client,
                    cond
                )
        cond = self.plugin.EvalString(cond, self) if cond != "" else True
        if cond:
            vals = self.plugin.GetAllValues()
            if vals != self.vals or not self.onlyChange:
                self.plugin.ClientSendMessage(
                    client,
                    dumps(vals)
                )
        self.vals = vals


    def __call__(
        self,
        cl_ip = "127.0.0.1",
        cl_port = "1234",
        modeClient = 1,
        onlyChange = True,
        cond = "",
        period = 5.0
    ):
        self.onlyChange = onlyChange
        self.period=period
        self.vals = None
        self.eg_event = eg.event
        self.eg_result = eg.result
        cond = replInstVal(cond)

        client = eg.event.payload[0] if modeClient else (
            eg.ParseString(cl_ip),
            int(eg.ParseString(cl_port))
        )
        if self.value:
            self.Task(client, cond)
        else:
            cond = self.plugin.EvalString(cond, self) if cond != "" else True
            if cond:
                vals = self.plugin.GetAllValues()
                return self.plugin.ServerSendMessage(
                    client,
                    dumps(vals)
                )


    def GetLabel(
        self,
        cl_ip,
        cl_port,
        modeClient,
        onlyChange,
        cond,
        period
    ):
        if modeClient:
            client = "{eg.event.payload[0]}"
            return "%s: %s: %s" % (self.name, client)
        else:
            return "%s: %s:%s: %s" % (self.name, cl_ip, cl_port)


    def Configure(
        self,
        cl_ip = "127.0.0.1",
        cl_port = "1234",
        modeClient = 1,
        onlyChange = True,
        cond = "",
        period = 5.0
    ):
        text = self.text
        panel = eg.ConfigPanel()
        id2 = wx.NewId()
        id3 = wx.NewId()
        id4 = wx.NewId()
        radioBoxModeClient = wx.RadioBox(
            panel,
            -1,
            self.plugin.text.modeClientChoiceLabel,
            choices = self.plugin.text.modeClientChoice,
            style = wx.RA_SPECIFY_ROWS
        )
        radioBoxModeClient.SetSelection(modeClient)
        staticBox = wx.StaticBox(panel, -1, "")
        tmpSizer = wx.GridBagSizer(2, 10)
        txtLabel = wx.StaticText(panel,-1,self.plugin.text.host)
        txtCtrl = wx.TextCtrl(panel,id3,"")
        portLabel = wx.StaticText(panel,-1,self.plugin.text.port)
        portCtrl = wx.TextCtrl(panel,id2,"")
        tmpSizer.Add(txtLabel,(0,0),(1,1))
        tmpSizer.Add(txtCtrl,(1,0),(1,1),flag = wx.EXPAND)
        tmpSizer.Add(portLabel,(2,0),(1,1),flag = wx.TOP, border = 10)
        tmpSizer.Add(portCtrl,(3,0),(1,1))
        middleSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        middleSizer.Add(radioBoxModeClient,0,wx.LEFT|wx.EXPAND)
        middleSizer.Add((20,-1),0,wx.LEFT|wx.EXPAND)
        middleSizer.Add(tmpSizer,0,wx.LEFT|wx.EXPAND)
        panel.sizer.Add(middleSizer, 0, wx.TOP|wx.EXPAND, 8)
        condLabel = wx.StaticText(panel, -1, text.cond)
        condCtrl = wx.TextCtrl(panel, -1, cond)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(condLabel,0,wx.TOP,10)
        mainSizer.Add(condCtrl,0,wx.EXPAND|wx.TOP,2)
        panel.sizer.Add(mainSizer,0,wx.ALL|wx.EXPAND,10)
        if self.value:
            periodLabel = wx.StaticText(panel, -1, text.period)
            periodCtrl = eg.SpinNumCtrl(
                panel,
                -1,
                period,
                integerWidth = 5,
                fractionWidth = 1,
                allowNegative = False,
                min = 0.1,
                increment = 0.1,
            )
            changeCtrl = wx.CheckBox(panel, -1, text.onlyChange)
            changeCtrl.SetValue(onlyChange)
            perSizer = wx.BoxSizer(wx.HORIZONTAL)
            perSizer.Add(periodLabel, 0, ACV)
            perSizer.Add(periodCtrl,0,wx.LEFT,1)
            perSizer.Add((-1,-1),1,wx.EXPAND)
            perSizer.Add(changeCtrl,0,wx.TOP,4)
            mainSizer.Add(perSizer,0,wx.EXPAND|wx.TOP,10)
        panel.sizer.Layout()
        size2 = (-1, tmpSizer.GetMinSize()[1])

        def OnClientChoice(evt = None):
            ClientChoice(
                evt,
                self.plugin.text,
                panel,
                id3,
                id4,
                cl_ip,
                cl_port,
                size2,
                radioBoxModeClient
        )
        radioBoxModeClient.Bind(wx.EVT_RADIOBOX, OnClientChoice)
        OnClientChoice()

        while panel.Affirmed():
            modeClient = radioBoxModeClient.GetSelection()
            if not modeClient:
                cl_ip = wx.FindWindowById(id3).GetValue()
                cl_port = wx.FindWindowById(id4).GetValue()
            change = changeCtrl.GetValue() if self.value else None
            period = periodCtrl.GetValue() if self.value else None
            panel.SetResult(
                cl_ip,
                cl_port,
                modeClient,
                change,
                condCtrl.GetValue(),
                period,
            )
#===============================================================================

class WsSendData(eg.ActionBase):
    eg_event = None
    eg_result = None

    class text:
        dataName = "Data name:"
        data2send = "Data for broadcast (python expression):"
        cond = "Condition for data sending (python expression):"
        onlyChange = "Data send only if it has been changed"
        period = "Sending period [s]:"


    def Task(self, client, cond, dataName, data2send):
        if self.plugin.info.isStarted:
            self.task = eg.scheduler.AddTask(
                self.period,
                self.Task,
                client,
                cond,
                dataName,
                data2send
            )
        dataName = self.plugin.EvalString(dataName, self)
        data = self.plugin.EvalString(data2send, self)
        cond = self.plugin.EvalString(cond, self) if cond != "" else True
        if cond:
            if data != self.data or not self.onlyChange:
                self.plugin.ServerSendMessage(
                    client,
                    dumps({
                        'method':'Data',
                        'dataName':dataName,
                        'data':data
                    }),
                )
        self.data = data


    def __call__(
        self,
        cl_ip = "127.0.0.1",
        cl_port = "1234",
        modeClient = 1,
        dataName = "",
        data2send = "",
        onlyChange = True,
        cond = "",
        period = 5.0
    ):
        self.onlyChange = onlyChange
        self.period = period
        self.data = None
        self.eg_event = eg.event
        self.eg_result = eg.result
        dataName = replInstVal(dataName)
        data2send = replInstVal(data2send)
        cond = replInstVal(cond)

        client = eg.event.payload[0] if modeClient else (
            eg.ParseString(cl_ip),
            int(eg.ParseString(cl_port))
        )
        if self.value:
            self.Task(client, cond, dataName, data2send)
        else:
            dataName = self.plugin.EvalString(dataName, self)
            data = self.plugin.EvalString(data2send, self)
            cond = self.plugin.EvalString(cond, self) if cond != "" else True
            if cond:
                self.plugin.ServerSendMessage(
                    client,
                    dumps({
                        'method':'Data',
                        'dataName':dataName,
                        'data':data
                    }),
                )


    def GetLabel(
        self,
        cl_ip,
        cl_port,
        modeClient,
        dataName,
        data2send,
        onlyChange,
        cond,
        period
    ):
        if modeClient:
            client = "{eg.event.payload[0]}"
            return "%s: %s: %s" % (self.name, client, dataName)
        else:
            return "%s: %s:%s: %s" % (self.name, cl_ip, cl_port, dataName)


    def Configure(
        self,
        cl_ip = "127.0.0.1",
        cl_port = "1234",
        modeClient = 1,
        dataName = "",
        data2send = "",
        onlyChange = True,
        cond = "",
        period = 5.0
    ):
        text = self.text
        panel = eg.ConfigPanel()
        id2 = wx.NewId()
        id3 = wx.NewId()
        id4 = wx.NewId()
        radioBoxModeClient = wx.RadioBox(
            panel,
            -1,
            self.plugin.text.modeClientChoiceLabel,
            choices = self.plugin.text.modeClientChoice,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxModeClient.SetSelection(modeClient)
        staticBox = wx.StaticBox(panel, -1, "")
        tmpSizer = wx.GridBagSizer(2, 10)
        txtLabel = wx.StaticText(panel,-1,self.plugin.text.host)
        txtCtrl = wx.TextCtrl(panel,id3,"")
        portLabel = wx.StaticText(panel,-1,self.plugin.text.port)
        portCtrl = wx.TextCtrl(panel,id2,"")
        tmpSizer.Add(txtLabel,(0,0),(1,1))
        tmpSizer.Add(txtCtrl,(1,0),(1,1),flag = wx.EXPAND)
        tmpSizer.Add(portLabel,(2,0),(1,1),flag = wx.TOP, border = 10)
        tmpSizer.Add(portCtrl,(3,0),(1,1))
        middleSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        middleSizer.Add(radioBoxModeClient,0,wx.LEFT|wx.EXPAND)
        middleSizer.Add((20,-1),0,wx.LEFT|wx.EXPAND)
        middleSizer.Add(tmpSizer,0,wx.LEFT|wx.EXPAND)
        panel.sizer.Add(middleSizer, 0, wx.TOP|wx.EXPAND, 8)
        nameLabel = wx.StaticText(panel, -1, text.dataName)
        sendLabel = wx.StaticText(panel, -1, text.data2send)
        condLabel = wx.StaticText(panel, -1, text.cond)
        nameCtrl = wx.TextCtrl(panel, -1, dataName)
        sendCtrl = wx.TextCtrl(panel, -1, data2send)
        condCtrl = wx.TextCtrl(panel, -1, cond)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(nameLabel)
        mainSizer.Add(nameCtrl,0,wx.EXPAND|wx.TOP,2)
        mainSizer.Add(sendLabel,0,wx.TOP,10)
        mainSizer.Add(sendCtrl,0,wx.EXPAND|wx.TOP,2)
        mainSizer.Add(condLabel,0,wx.TOP,10)
        mainSizer.Add(condCtrl,0,wx.EXPAND|wx.TOP,2)
        panel.sizer.Add(mainSizer,0,wx.ALL|wx.EXPAND,10)
        if self.value:
            periodLabel = wx.StaticText(panel, -1, text.period)
            periodCtrl = eg.SpinNumCtrl(
                panel,
                -1,
                period,
                integerWidth = 5,
                fractionWidth = 1,
                allowNegative = False,
                min = 0.1,
                increment = 0.1,
            )
            changeCtrl = wx.CheckBox(panel, -1, text.onlyChange)
            changeCtrl.SetValue(onlyChange)
            perSizer = wx.BoxSizer(wx.HORIZONTAL)
            perSizer.Add(periodLabel, 0, ACV)
            perSizer.Add(periodCtrl,0,wx.LEFT,1)
            perSizer.Add((-1,-1),1,wx.EXPAND)
            perSizer.Add(changeCtrl,0,wx.TOP,4)
            mainSizer.Add(perSizer,0,wx.EXPAND|wx.TOP,10)
        panel.sizer.Layout()
        size2 = (-1, tmpSizer.GetMinSize()[1])

        def OnClientChoice(evt = None):
            ClientChoice(
                evt,
                self.plugin.text,
                panel,
                id3,
                id4,
                cl_ip,
                cl_port,
                size2,
                radioBoxModeClient
        )
        radioBoxModeClient.Bind(wx.EVT_RADIOBOX, OnClientChoice)
        OnClientChoice()

        while panel.Affirmed():
            modeClient = radioBoxModeClient.GetSelection()
            if not modeClient:
                cl_ip = wx.FindWindowById(id3).GetValue()
                cl_port = wx.FindWindowById(id4).GetValue()
            change = changeCtrl.GetValue() if self.value else None
            period = periodCtrl.GetValue() if self.value else None
            panel.SetResult(
                cl_ip,
                cl_port,
                modeClient,
                nameCtrl.GetValue(),
                sendCtrl.GetValue(),
                change,
                condCtrl.GetValue(),
                period,
            )
#===============================================================================

class WsSendCommand(eg.ActionBase):
    eg_event = None
    eg_result = None

    class text:
        cond = "Condition:"
        cmdName = "Command name:"
        arg1 = "Argument 1:"
        arg2 = "Argument 2:"
        arg3 = "Argument 3:"
        othArgs = "Arguments:"
        kwArgs = "Keyw. arguments:"
        onlyChange = "Data send only if it has been changed"
        period = "Sending period [s]:"

    def Task(self, client, cond, cmdName, arg1, arg2, arg3, othArgs, kwArgs):
        if self.plugin.info.isStarted:
            self.task = eg.scheduler.AddTask(
                self.period,
                self.Task,
                client,
                cond,
                cmdName,
                arg1,
                arg2,
                arg3,
                othArgs,
                kwArgs
            )

        cmdName = self.plugin.EvalString(cmdName)
        args = [self.plugin.EvalString(arg1, self)] if self.arg1 != "" else []
        if self.arg2 != "":
            args.append(self.plugin.EvalString(arg2, self))
        if self.arg3 != "":
            args.append(self.plugin.EvalString(arg3, self))
        if self.othArgs != "":
            try:
                othArgs = list(self.plugin.EvalString(othArgs, self))
                args.extend(othArgs)
            except:
                pass
        kwargs = {}
        if self.kwArgs != "":
            try:
                kwargs = dict(self.plugin.EvalString2(kwArgs, self))
            except:
                pass
        cond = self.plugin.EvalString(cond, self) if cond != "" else True
        if cond:
            if args != self.args or kwargs != self.kwargs or not self.onlyChange:
                self.plugin.ServerSendMessage(
                    client,
                    dumps(
                        {
                            'method' :'Command',
                            'cmdName':cmdName,
                            'args':args,
                            'kwargs':kwargs
                        }
                    ),
                )
        self.args = args
        self.kwargs = kwargs


    def __call__(
        self,
        cl_ip = "127.0.0.1",
        cl_port = "1234",
        modeClient = 1,
        cmdName = "",
        cond = "",
        arg1 = "",
        arg2 = "",
        arg3 = "",
        othArgs = "",
        kwArgs = "",
        onlyChange = True,
        period = 5.0
    ):
        self.eg_event = eg.event
        self.eg_result = eg.result
        cmdName = replInstVal(cmdName)
        arg1 = replInstVal(arg1)
        arg2 = replInstVal(arg2)
        arg3 = replInstVal(arg3)
        othArgs = replInstVal(othArgs)
        kwArgs = replInstVal(kwArgs)
        cond = replInstVal(cond)

        client = eg.event.payload[0] if modeClient else (
            eg.ParseString(cl_ip),
            int(eg.ParseString(cl_port))
        )
        if self.value:
            self.onlyChange = onlyChange
            self.period = period
            self.args = None
            self.kwargs = None
            self.Task(
                client,
                cond,
                cmdName,
                arg1,
                arg2,
                arg3,
                othArgs,
                kwArgs
            )
        else:
            cmdName = self.plugin.EvalString(cmdName)
            args = [self.plugin.EvalString(arg1, self)] if arg1 != "" else []
            if arg2 != "":
                args.append(self.plugin.EvalString(arg2, self))
            if arg3 != "":
                args.append(self.plugin.EvalString(arg3, self))
            if othArgs != "":
                try:
                    othArgs = list(self.plugin.EvalString(othArgs, self))
                    args.extend(othArgs)
                except:
                    pass
            kwargs = {}
            if kwArgs != "":
                try:
                    kwargs = dict(self.plugin.EvalString2(kwArgs, self))
                except:
                    pass
            cond = self.plugin.EvalString(cond, self) if cond != "" else True
            if cond:
                self.plugin.ServerSendMessage(
                    client,
                    dumps(
                        {
                            'method' :'Command',
                            'cmdName':cmdName,
                            'args':args,
                            'kwargs':kwargs
                        }
                    ),
                )


    def GetLabel(
        self,
        cl_ip,
        cl_port,
        modeClient,
        cmdName,
        cond,
        arg1,
        arg2,
        arg3,
        othArgs,
        kwArgs,
        onlyChange,
        period
    ):
        if modeClient:
            client = "{eg.event.payload[0]}"
            return "%s: %s: %s: (%s, %s)" % (
                self.name,
                client,
                cmdName,
                arg1,
                arg2
            )
        else:
            return "%s: %s:%s: %s: (%s, %s)" % (
                self.name,
                cl_ip,
                cl_port,
                cmdName,
                arg1,
                arg2
            )


    def Configure(
        self,
        cl_ip = "127.0.0.1",
        cl_port = "1234",
        modeClient = 1,
        cmdName = "",
        cond = "",
        arg1 = "",
        arg2 = "",
        arg3 = "",
        othArgs = "",
        kwArgs = "",
        onlyChange = True,
        period = 5.0
    ):
        panel = eg.ConfigPanel(self)
        text = self.text
        id2 = wx.NewId()
        id3 = wx.NewId()
        id4 = wx.NewId()
        radioBoxModeClient = wx.RadioBox(
            panel,
            -1,
            self.plugin.text.modeClientChoiceLabel,
            choices = self.plugin.text.modeClientChoice,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxModeClient.SetSelection(modeClient)
        staticBox = wx.StaticBox(panel, -1, "")
        tmpSizer = wx.GridBagSizer(2, 10)
        txtLabel = wx.StaticText(panel,-1,self.plugin.text.host)
        txtCtrl = wx.TextCtrl(panel,id3,"")
        portLabel = wx.StaticText(panel,-1,self.plugin.text.port)
        portCtrl = wx.TextCtrl(panel,id2,"")
        tmpSizer.Add(txtLabel,(0,0),(1,1))
        tmpSizer.Add(txtCtrl,(1,0),(1,1),flag = wx.EXPAND)
        tmpSizer.Add(portLabel,(2,0),(1,1),flag = wx.TOP, border = 10)
        tmpSizer.Add(portCtrl,(3,0),(1,1))
        middleSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        middleSizer.Add(radioBoxModeClient,0,wx.LEFT|wx.EXPAND)
        middleSizer.Add((20,-1),0,wx.LEFT|wx.EXPAND)
        middleSizer.Add(tmpSizer,0,wx.LEFT|wx.EXPAND)
        panel.sizer.Add(middleSizer, 0, wx.TOP|wx.LEFT|wx.RIGHT|wx.EXPAND, 8)
        panel.sizer.Layout()
        size2 = (-1, tmpSizer.GetMinSize()[1])

        def OnClientChoice(evt = None):
            ClientChoice(
                evt,
                self.plugin.text,
                panel,
                id3,
                id4,
                cl_ip,
                cl_port,
                size2,
                radioBoxModeClient
        )
        radioBoxModeClient.Bind(wx.EVT_RADIOBOX, OnClientChoice)
        OnClientChoice()

        nameLabel = wx.StaticText(panel, -1, text.cmdName)
        condLabel = wx.StaticText(panel, -1, text.cond)
        arg1Label = wx.StaticText(panel, -1, text.arg1)
        arg2Label = wx.StaticText(panel, -1, text.arg2)
        arg3Label = wx.StaticText(panel, -1, text.arg3)
        othLabel = wx.StaticText(panel, -1, text.othArgs)
        kwLabel = wx.StaticText(panel, -1, text.kwArgs)
        nameCtrl = wx.TextCtrl(panel, -1, cmdName)
        condCtrl = wx.TextCtrl(panel, -1, cond)
        arg1Ctrl = wx.TextCtrl(panel, -1, arg1)
        arg2Ctrl = wx.TextCtrl(panel, -1, arg2)
        arg3Ctrl = wx.TextCtrl(panel, -1, arg3)
        othCtrl = wx.TextCtrl(panel, -1, othArgs)
        kwCtrl = wx.TextCtrl(panel, -1, kwArgs)
        mainSizer = wx.FlexGridSizer(7, 2, 2, 10)
        mainSizer.AddGrowableCol(1)
        mainSizer.Add(nameLabel, 0, ACV)
        mainSizer.Add(nameCtrl,0,wx.EXPAND)
        mainSizer.Add(arg1Label, 0, ACV)
        mainSizer.Add(arg1Ctrl,0,wx.EXPAND)
        mainSizer.Add(arg2Label, 0, ACV)
        mainSizer.Add(arg2Ctrl,0,wx.EXPAND)
        mainSizer.Add(arg3Label, 0, ACV)
        mainSizer.Add(arg3Ctrl,0,wx.EXPAND)
        mainSizer.Add(othLabel, 0, ACV)
        mainSizer.Add(othCtrl,0,wx.EXPAND)
        mainSizer.Add(kwLabel, 0, ACV)
        mainSizer.Add(kwCtrl,0,wx.EXPAND)
        mainSizer.Add(condLabel, 0, ACV)
        mainSizer.Add(condCtrl,0,wx.EXPAND)
        if self.value:
            periodLabel = wx.StaticText(panel, -1, text.period)
            periodCtrl = eg.SpinNumCtrl(
                panel,
                -1,
                period,
                integerWidth = 5,
                fractionWidth = 1,
                allowNegative = False,
                min = 0.1,
                increment = 0.1,
            )
            changeCtrl = wx.CheckBox(panel, -1, text.onlyChange)
            changeCtrl.SetValue(onlyChange)
            perSizer = wx.BoxSizer(wx.HORIZONTAL)
            mainSizer.Add(periodLabel, 0, ACV)
            perSizer.Add(periodCtrl,0,wx.LEFT,1)
            perSizer.Add((-1,-1),1,wx.EXPAND)
            perSizer.Add(changeCtrl,0,wx.TOP,4)
            mainSizer.Add(perSizer,0,wx.EXPAND)
        panel.sizer.Add(mainSizer,0,wx.ALL|wx.EXPAND,8)
       
        while panel.Affirmed():
            modeClient = radioBoxModeClient.GetSelection()
            if not modeClient:
                cl_ip = wx.FindWindowById(id3).GetValue()
                cl_port = wx.FindWindowById(id4).GetValue()
            change = changeCtrl.GetValue() if self.value else None
            period = periodCtrl.GetValue() if self.value else None
            panel.SetResult(
                cl_ip,
                cl_port,
                modeClient,
                nameCtrl.GetValue(),
                condCtrl.GetValue(),
                arg1Ctrl.GetValue(),
                arg2Ctrl.GetValue(),
                arg3Ctrl.GetValue(),
                othCtrl.GetValue(),
                kwCtrl.GetValue(),
                change,
                period
            )
#===============================================================================

class WsSendUniversal(eg.ActionBase):
    eg_event = None
    eg_result = None

    class text:
        cond = "Condition:"
        method = "Method:"
        othArgs = "Arguments:"
        kwArgs = "Keyw. arguments:"
        onlyChange = "Data send only if it has been changed"
        period = "Sending period [s]:"


    def Task(self, client, cond, method, othArgs, kwArgs):
        if self.plugin.info.isStarted:
            self.task = eg.scheduler.AddTask(
                self.period,
                self.Task,
                client,
                cond,
                method,
                othArgs,
                kwArgs
            )
        args = []
        if othArgs != "":
            try:
                args = list(self.plugin.EvalString(othArgs, self))
            except:
                pass
        kwargs = {}
        if kwArgs != "":
            try:
                kwargs = dict(self.plugin.EvalString2(kwArgs, self))
            except:
                pass
        cond = self.plugin.EvalString(cond, self) if cond != "" else True
        if cond:
            if args != self.args or kwargs != self.kwargs or not self.onlyChange:
                self.plugin.ServerSendMessage(
                    client,
                    dumps(
                        {
                            'method' :method,
                            'args':args,
                            'kwargs':kwargs
                        }
                    )
                )
        self.args = args
        self.kwargs = kwargs


    def __call__(
        self,
        cl_ip = "127.0.0.1",
        cl_port = "1234",
        modeClient = 1,
        method = "",
        cond = "",
        othArgs = "",
        kwArgs = "",
        onlyChange = True,
        period = 5.0
    ):
        client = eg.event.payload[0] if modeClient else (
            eg.ParseString(cl_ip),
            int(eg.ParseString(cl_port))
        )

        self.eg_event = eg.event
        self.eg_result = eg.result
        othArgs = replInstVal(othArgs)
        kwArgs = replInstVal(kwArgs)
        cond = replInstVal(cond)


        if self.value:
            self.period = period
            self.args = None
            self.kwargs = None
            self.Task(
                client,
                cond,
                method,
                othArgs,
                kwArgs
                )
        else:
            args = []
            if othArgs != "":
                try:
                    args = list(self.plugin.EvalString(othArgs, self))
                except:
                    pass
            kwargs = {}
            if kwArgs != "":
                try:
                    kwargs = dict(self.plugin.EvalString2(kwArgs, self))
                except:
                    pass
            cond = self.plugin.EvalString(cond, self) if cond != "" else True
            if cond:
                self.plugin.ServerSendMessage(
                    client,
                    dumps(
                        {
                            'method' :method,
                            'args':args,
                            'kwargs':kwargs
                        }
                    ),
                )


    def GetLabel(
        self,
        cl_ip,
        cl_port,
        modeClient,
        method,
        cond,
        othArgs,
        kwArgs,
        onlyChange,
        period
    ):
        if modeClient:
            client = "{eg.event.payload[0]}"
            return "%s: %s: %s" % (
                self.name,
                client,
                method,
            )
        else:
            return "%s: %s:%s: %s" % (
                self.name,
                cl_ip,
                cl_port,
                method
            )


    def Configure(
        self,
        cl_ip = "127.0.0.1",
        cl_port = "1234",
        modeClient = 1,
        method = "",
        cond = "",
        othArgs = "",
        kwArgs = "",
        onlyChange = True,
        period = 5.0
    ):
        panel = eg.ConfigPanel(self)
        text = self.text
        id2 = wx.NewId()
        id3 = wx.NewId()
        id4 = wx.NewId()
        radioBoxModeClient = wx.RadioBox(
            panel,
            -1,
            self.plugin.text.modeClientChoiceLabel,
            choices = self.plugin.text.modeClientChoice,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxModeClient.SetSelection(modeClient)
        staticBox = wx.StaticBox(panel, -1, "")
        tmpSizer = wx.GridBagSizer(2, 10)
        txtLabel = wx.StaticText(panel,-1,self.plugin.text.host)
        txtCtrl = wx.TextCtrl(panel,id3,"")
        portLabel = wx.StaticText(panel,-1,self.plugin.text.port)
        portCtrl = wx.TextCtrl(panel,id2,"")
        tmpSizer.Add(txtLabel,(0,0),(1,1))
        tmpSizer.Add(txtCtrl,(1,0),(1,1),flag = wx.EXPAND)
        tmpSizer.Add(portLabel,(2,0),(1,1),flag = wx.TOP, border = 10)
        tmpSizer.Add(portCtrl,(3,0),(1,1))
        middleSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        middleSizer.Add(radioBoxModeClient,0,wx.LEFT|wx.EXPAND)
        middleSizer.Add((20,-1),0,wx.LEFT|wx.EXPAND)
        middleSizer.Add(tmpSizer,0,wx.LEFT|wx.EXPAND)
        panel.sizer.Add(middleSizer, 0, wx.TOP|wx.LEFT|wx.RIGHT|wx.EXPAND, 8)

        panel.sizer.Layout()
        size2 = (-1, tmpSizer.GetMinSize()[1])

        def OnClientChoice(evt = None):
            ClientChoice(
                evt,
                self.plugin.text,
                panel,
                id3,
                id4,
                cl_ip,
                cl_port,
                size2,
                radioBoxModeClient
        )
        radioBoxModeClient.Bind(wx.EVT_RADIOBOX, OnClientChoice)
        OnClientChoice()

        methodLabel = wx.StaticText(panel, -1, text.method)
        condLabel = wx.StaticText(panel, -1, text.cond)
        othLabel = wx.StaticText(panel, -1, text.othArgs)
        kwLabel = wx.StaticText(panel, -1, text.kwArgs)
        methodCtrl = wx.ComboBox(
            panel,
            -1,
            choices = METHODS[:8],
            style = wx.CB_DROPDOWN
        )
        methodCtrl.SetValue(method)
        condCtrl = wx.TextCtrl(panel, -1, cond)
        othCtrl = wx.TextCtrl(panel, -1, othArgs)
        kwCtrl = wx.TextCtrl(panel, -1, kwArgs)
        mainSizer = wx.FlexGridSizer(7, 2, 2, 10)
        mainSizer.AddGrowableCol(1)
        mainSizer.Add(methodLabel, 0, ACV)
        mainSizer.Add(methodCtrl,0,wx.EXPAND)
        mainSizer.Add(othLabel, 0, ACV)
        mainSizer.Add(othCtrl,0,wx.EXPAND)
        mainSizer.Add(kwLabel, 0, ACV)
        mainSizer.Add(kwCtrl,0,wx.EXPAND)
        mainSizer.Add(condLabel, 0, ACV)
        mainSizer.Add(condCtrl,0,wx.EXPAND)
        if self.value:
            periodLabel = wx.StaticText(panel, -1, text.period)
            periodCtrl = eg.SpinNumCtrl(
                panel,
                -1,
                period,
                integerWidth = 5,
                fractionWidth = 1,
                allowNegative = False,
                min = 0.1,
                increment = 0.1,
            )
            changeCtrl = wx.CheckBox(panel, -1, text.onlyChange)
            changeCtrl.SetValue(onlyChange)
            perSizer = wx.BoxSizer(wx.HORIZONTAL)
            mainSizer.Add(periodLabel, 0, ACV)
            perSizer.Add(periodCtrl,0,wx.LEFT,1)
            perSizer.Add((-1,-1),1,wx.EXPAND)
            perSizer.Add(changeCtrl,0,wx.TOP,4)
            mainSizer.Add(perSizer,0,wx.EXPAND)
        panel.sizer.Add(mainSizer,0,wx.ALL|wx.EXPAND,8)
       
        while panel.Affirmed():
            modeClient = radioBoxModeClient.GetSelection()
            if not modeClient:
                cl_ip = wx.FindWindowById(id3).GetValue()
                cl_port = wx.FindWindowById(id4).GetValue()
            change = changeCtrl.GetValue() if self.value else None
            period = periodCtrl.GetValue() if self.value else None
            panel.SetResult(
                cl_ip,
                cl_port,
                modeClient,
                methodCtrl.GetValue(),
                condCtrl.GetValue(),
                othCtrl.GetValue(),
                kwCtrl.GetValue(),
                change,
                period
            )
#===============================================================================

class WsStopClientPeriodicTasks(eg.ActionBase):

    class text:
        label = "Data or command name (empty = all  client's  tasks):"

    def __call__(
        self,
        cl_ip="127.0.0.1",
        cl_port = "1234",
        modeClient = 1,
        taskName = ""
    ):
        client = eg.event.payload[0] if modeClient else (
            eg.ParseString(cl_ip),
            int(eg.ParseString(cl_port))
        )
        self.plugin.StopClientPeriodicTasks(client, taskName)


    def GetLabel(self, cl_ip, cl_port, modeClient, taskName):
        if modeClient:
            client = "{eg.event.payload[0]}"
            return "%s: %s: %s" % (self.name, client, taskName)
        else:
            return "%s: %s:%s: %s" % (self.name, cl_ip, cl_port, taskName)

    def Configure(
        self,
        cl_ip="127.0.0.1",
        cl_port = "1234",
        modeClient = 1,
        taskName = ""
    ):
        text = self.text
        panel = eg.ConfigPanel()
        label = wx.StaticText(panel,-1,self.text.label)
        taskCtrl = wx.TextCtrl(panel,-1,taskName)
        id2 = wx.NewId()
        id3 = wx.NewId()
        id4 = wx.NewId()
        radioBoxModeClient = wx.RadioBox(
            panel,
            -1,
            self.plugin.text.modeClientChoiceLabel,
            choices = self.plugin.text.modeClientChoice,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxModeClient.SetSelection(modeClient)
        staticBox = wx.StaticBox(panel, -1, "")
        tmpSizer = wx.GridBagSizer(2, 10)
        txtLabel = wx.StaticText(panel,-1,self.plugin.text.host)
        txtCtrl = wx.TextCtrl(panel,id3,"")
        portLabel = wx.StaticText(panel,-1,self.plugin.text.port)
        portCtrl = wx.TextCtrl(panel,id2,"")
        tmpSizer.Add(txtLabel,(0,0),(1,1))
        tmpSizer.Add(txtCtrl,(1,0),(1,1),flag = wx.EXPAND)
        tmpSizer.Add(portLabel,(2,0),(1,1),flag = wx.TOP, border = 10)
        tmpSizer.Add(portCtrl,(3,0),(1,1))
        middleSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        middleSizer.Add(radioBoxModeClient,0,wx.LEFT|wx.EXPAND)
        middleSizer.Add((20,-1),0,wx.LEFT|wx.EXPAND)
        middleSizer.Add(tmpSizer,0,wx.LEFT|wx.EXPAND)
        panel.sizer.Add(middleSizer, 0, wx.TOP|wx.EXPAND, 8)
        panel.sizer.Layout()
        size2 = (-1, tmpSizer.GetMinSize()[1])

        def OnClientChoice(evt = None):
            ClientChoice(
                evt,
                self.plugin.text,
                panel,
                id3,
                id4,
                cl_ip,
                cl_port,
                size2,
                radioBoxModeClient
        )
        radioBoxModeClient.Bind(wx.EVT_RADIOBOX, OnClientChoice)
        OnClientChoice()
        panel.sizer.Add(label, 0, wx.TOP,8)
        panel.sizer.Add(taskCtrl, 0, wx.EXPAND|wx.TOP,2)

        while panel.Affirmed():
            modeClient = radioBoxModeClient.GetSelection()
            if not modeClient:
                cl_ip = wx.FindWindowById(id3).GetValue()
                cl_port = wx.FindWindowById(id4).GetValue()
            panel.SetResult(
                cl_ip,
                cl_port,
                modeClient,
                taskCtrl.GetValue()
            )
#===============================================================================

class WsStopPeriodicTasks(eg.ActionBase):

    class text:
        labels = (
            "Data or command name (empty = all tasks):",
            "Data or command name (empty = all broadcast tasks):"
        )


    def __call__(self, taskName = ""):
        self.plugin.StopPeriodicTasks(self.value[0], taskName)


    def Configure(self, taskName = ""):
        panel = eg.ConfigPanel()
        taskCtrl = wx.TextCtrl(panel,-1,taskName)
        if self.value[1] is None:
            taskCtrl.Show(False)
            panel.dialog.buttonRow.applyButton.Enable(False)
            panel.dialog.buttonRow.testButton.Show(False)
            label = panel.StaticText(
                eg.text.General.noOptionsAction,
                style=wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE
            )
            panel.sizer.Add((0, 0), 1, wx.EXPAND)
            panel.sizer.Add(label, 0, wx.ALIGN_CENTRE)
            panel.sizer.Add((0, 0), 1, wx.EXPAND)
        else:
            label = wx.StaticText(panel,-1,self.text.labels[self.value[1]])
            mainSizer = wx.BoxSizer(wx.VERTICAL)
            mainSizer.Add(label)
            mainSizer.Add(taskCtrl,0,wx.EXPAND)
            panel.sizer.Add(mainSizer,1,wx.EXPAND|wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(taskCtrl.GetValue(),)
#===============================================================================

class SetClientsFlags(eg.ActionBase):

    class text:
        varname = "Dummy variable name:"
        err = 'Error in action "Set clients flags(%s)"'

    def __call__(self, varname = "", pars = False):
        try:
            key = eg.ParseString(varname) if not pars else varname
            self.plugin.SetClientsFlags(key)
        except:
            eg.PrintError(self.text.err % str(varname))

    def Configure(self, varname = "", pars = False):
        panel = eg.ConfigPanel(self)
        varnameCtrl = panel.TextCtrl(varname)
        parsCtrl = wx.CheckBox(panel, -1, self.plugin.text.parsing)
        parsCtrl.SetValue(pars)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        varnameLbl = panel.StaticText(self.text.varname)
        mainSizer.Add(varnameLbl)
        mainSizer.Add(varnameCtrl, 0, wx.EXPAND|wx.TOP, 1)
        mainSizer.Add(parsCtrl, 0, wx.TOP, 4)
        panel.sizer.Add(mainSizer, 0, wx.EXPAND|wx.ALL, 10)
        while panel.Affirmed():
            panel.SetResult(
                varnameCtrl.GetValue(),
                parsCtrl.GetValue()
            )
#===============================================================================

class GetValue(eg.ActionBase):

    class text:
        varname = "Variable name:"
        err = 'Error in action "Get temporary value(%s)"'
        err2 = 'Error in action "Delete temporary value(%s)"'

    def __call__(self, varname = "", pars = False):
        try:
            key = eg.ParseString(varname) if not pars else varname
            if self.value:
                self.plugin.DelValue(key)
            else:
                return self.plugin.GetValue(key)
        except:
            if self.value:
                eg.PrintError(self.text.err2 % str(varname))
            else:
                eg.PrintError(self.text.err % str(varname))
       
    def Configure(self, varname = "", pars = False):
        panel = eg.ConfigPanel(self)
        varnameCtrl = panel.TextCtrl(varname)
        parsCtrl = wx.CheckBox(panel, -1, self.plugin.text.parsing)
        parsCtrl.SetValue(pars)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        varnameLbl = panel.StaticText(self.text.varname)
        mainSizer.Add(varnameLbl)
        mainSizer.Add(varnameCtrl, 0, wx.EXPAND|wx.TOP, 1)
        mainSizer.Add(parsCtrl, 0, wx.TOP, 4)
        panel.sizer.Add(mainSizer, 0, wx.EXPAND|wx.ALL, 10)
       
        while panel.Affirmed():
            panel.SetResult(
                varnameCtrl.GetValue(),
                parsCtrl.GetValue()
            )
#===============================================================================

class GetPersistentValue(GetValue):

    class text:
        varname = "Persistent variable name:"
        err = 'Error in action "Get persistent value(%s)"'
        err2 = 'Error in action "Delete persistent value(%s)"'

    def __call__(self, varname = "", pars = False):
        try:
            key = eg.ParseString(varname) if not pars else varname
            if self.value:
                self.plugin.DelPersistentValue(key)
            else:
                return self.plugin.GetPersistentValue(key)
        except:
            if self.value:
                eg.PrintError(self.text.err2 % str(varname))
            else:
                eg.PrintError(self.text.err % str(varname))
#===============================================================================

class SetValue(eg.ActionBase):

    class text:
        varname = "Variable name:"
        value = "Value:"
        err = 'Error in action "Set temporary value(%s, %s)"'

    def __call__(
        self,
        varname = "",
        value = "{eg.event.payload}",
        pars1 = False,
        pars2 = False,
        mode = 1
    ):
        try:
            key = eg.ParseString(varname) if not pars1 else varname
            if mode or key not in self.plugin.pubVars:
                val = eg.ParseString(value) if not pars2 else value
                self.plugin.SetValue(key, val)
        except:
            eg.PrintTraceback()
            eg.PrintError(self.text.err % (str(varname), str(value)))

    def GetLabel(self, varname, value, pars1, pars2, mode):
        return "%s: %s: %s" % (self.name, varname, value)
       
    def Configure(
        self,
        varname = "",
        value = "{eg.event.payload}",
        pars1 = False,
        pars2 = False,
        mode = 1
    ):
        panel = eg.ConfigPanel(self)
        varnameCtrl = panel.TextCtrl(varname)
        pars1Ctrl = wx.CheckBox(panel, -1, self.plugin.text.parsing)
        pars1Ctrl.SetValue(pars1)
        valueCtrl = panel.TextCtrl(value)
        pars2Ctrl = wx.CheckBox(panel, -1, self.plugin.text.parsing)
        pars2Ctrl.SetValue(pars2)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        varnameLbl = panel.StaticText(self.text.varname)
        valueLbl = panel.StaticText(self.text.value)
        radioBox = wx.RadioBox(
            panel,
            -1,
            "",
            choices = self.plugin.text.setVar,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(mode)
        mainSizer.Add(varnameLbl)
        mainSizer.Add(varnameCtrl, 0, wx.EXPAND|wx.TOP, 1)
        mainSizer.Add(pars1Ctrl, 0, wx.EXPAND|wx.TOP, 4)
        mainSizer.Add(valueLbl, 0, wx.EXPAND|wx.TOP, 15)
        mainSizer.Add(valueCtrl, 0, wx.EXPAND|wx.TOP, 1)
        mainSizer.Add(pars2Ctrl, 0, wx.EXPAND|wx.TOP, 4)
        mainSizer.Add(radioBox,0,wx.EXPAND|wx.TOP, 10)
        panel.sizer.Add(mainSizer, 0, wx.EXPAND|wx.ALL, 10)
        while panel.Affirmed():
            panel.SetResult(
                varnameCtrl.GetValue(),
                valueCtrl.GetValue(),
                pars1Ctrl.GetValue(),
                pars2Ctrl.GetValue(),
                radioBox.GetSelection()
            )
#===============================================================================

class SetPersistentValue(SetValue):

    class text:
        varname = "Persistent variable name:"
        value = "Value:"
        err = 'Error in action "Set persistent value(%s, %s)"'

    def __call__(
        self,
        varname = "",
        value = "{eg.event.payload}",
        pars1 = False,
        pars2 = False,
        mode = 1
    ):
        try:
            key = eg.ParseString(varname) if not pars1 else varname
            if mode or key not in self.plugin.pubPerVars:
                val = eg.ParseString(value) if not pars2 else value
                self.plugin.SetPersistentValue(key, val)
        except:
            eg.PrintError(self.text.err % (str(varname), str(value)))
#===============================================================================

class SendEvent(eg.ActionBase):

    class text:
        event = "Event:"
        host = "Host:"
        port ="Port:"
        username = "Username:"
        password = "Password:"
        errmsg = "Target server returned status %s"

    def __call__(
        self,
        event="",
        host="",
        port=80,
        user="",
        password="",
        pars = False
    ):
        text = self.text
        def Request(methodName, *args, **kwargs):
            data = {"method": methodName}
            if len(args):
                data["args"] = args
            if len(kwargs):
                data["kwargs"] = kwargs
            content = dumps(data)
            authString = b64_encStr(user + ':' + password).strip()
            sock = None
            for af, socktype, proto, canonname, sa in socket.getaddrinfo(
                host, port, socket.AF_UNSPEC, socket.SOCK_STREAM
            ):
                try:
                    sock = socket.socket(af, socktype, proto)
                except socket.error:
                    sock = None
                    continue
                sock.settimeout(2)
                try:
                    sock.connect(sa)
                except socket.error:
                    sock.close()
                    sock = None
                    continue
                break
            data = [
                "POST %s HTTP/1.0" % "/",
                "Host: %sock:%d" % (host, port),
                "User-Agent: EventGhost/%s" % eg.Version.string,
                "Authorization: Basic %s" % authString,
                "Content-Length: %d" % len(content),
                "Content-Type: application/json; charset=UTF-8",
                "",
                content
            ]
            sock.send("\r\n".join(data))

            response = HTTPResponse(sock)
            response.begin()
            content = response.read()
            response.close()
            sock.close()
            if response.status != 200:
                raise Exception(
                    text.errmsg % response.status
                )
            return loads(content)

        event = eg.ParseString(event) if not pars else event
        Request("TriggerEnduringEvent", event)
        stopEvent = Event()
        eg.event.AddUpFunc(stopEvent.set)
        def RepeatLoop():
            while True:
                stopEvent.wait(1.0)
                if stopEvent.isSet():
                    break
                Request("RepeatEnduringEvent", event)
            Request("EndLastEvent")
        Thread(target=RepeatLoop).start()


    def Configure(
        self,
        event="",
        host="",
        port=80,
        user="",
        password="",
        pars = False
    ):
        text = self.text
        panel = eg.ConfigPanel(self)
        eventCtrl = panel.TextCtrl(event)
        parsCtrl = wx.CheckBox(panel, -1, self.plugin.text.parsing)
        parsCtrl.SetValue(pars)
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, min=1, max=65535)
        userCtrl = panel.TextCtrl(user)
        passwordCtrl = panel.TextCtrl(password)
        fl = wx.EXPAND|wx.TOP
        box=wx.GridBagSizer(2, 5)
        box.Add(panel.StaticText(text.event), (0, 0), flag = wx.TOP, border=12)
        box.Add(eventCtrl, (0, 1), flag = fl, border=9)
        box.Add(parsCtrl, (1, 0), (1, 2))
        box.Add(panel.StaticText(text.host), (2, 0), flag = wx.TOP, border=12)
        box.Add(hostCtrl, (2, 1), flag = fl, border=9)
        box.Add(panel.StaticText(text.port), (3, 0), flag = wx.TOP, border=12)
        box.Add(portCtrl, (3, 1), flag = wx.TOP, border=9)
        box.Add(panel.StaticText(text.username), (4, 0), flag=wx.TOP, border=12)
        box.Add(userCtrl, (4, 1), flag = fl, border=9)
        box.Add(panel.StaticText(text.password), (5, 0), flag=wx.TOP, border=12)
        box.Add(passwordCtrl, (5, 1), flag = fl, border=9)
        box.AddGrowableCol(1)
        panel.sizer.Add(box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)

        while panel.Affirmed():
            panel.SetResult(
                eventCtrl.GetValue(),
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                userCtrl.GetValue(),
                passwordCtrl.GetValue(),
                parsCtrl.GetValue()
            )
#===============================================================================


class SendEventExt(eg.ActionBase):

    class text:
        url = "URL:"
        event = "Event:"
        username = "Username:"
        password = "Password:"
        msg1 = "This page isn't protected by basic authentication."
        msg2 = 'But we failed for another reason.'
        msg3 = 'A 401 error without an authentication response header - very weird.'
        msg4 = 'The authentication line is badly formed.'
        msg5 = 'SendEventExt only works with BASIC authentication.'
        msg6 = "url, username or password is wrong."

    def __call__(self, event="", host="", user="", password=""):
        text = self.text
        if event!="":
            req = urlRequest(host, event)
        else:
            req = urlRequest(host)
        try:
            handle = urlopen(req)
        except IOError, e:
            # If we fail then the page could be protected
            if not hasattr(e, 'code') or e.code != 401:
                # we got an error - but not a 401 error
                #print text.msg1
                #print text.msg2
                eg.PrintError("Webserver: Error " + str(e.code if hasattr(e, "code") else e))
                return None
            authline = e.headers.get('www-authenticate', '')
            # this gets the www-authenticat line from the headers - which has the authentication scheme and realm in it
            if not authline:
                eg.PrintError("Webserver: " + text.msg3)
                return None
            authobj = re_compile(r'''(?:\s*www-authenticate\s*:)?\s*(\w*)\s+realm=['"](\w+)['"]''', IGNORECASE)
            # this regular expression is used to extract scheme and realm
            matchobj = authobj.match(authline)
            if not matchobj:
                # if the authline isn't matched by the regular expression then something is wrong
                eg.PrintError("Webserver: " + text.msg4)
                #authheader=b'Basic ' + b64encode(user + b':' + password)
                return None
            scheme = matchobj.group(1)
            realm = matchobj.group(2)
            if scheme.lower() != 'basic':
                eg.PrintError("Webserver: " + text.msg5)
                return None
            base64string = b64_encStr('%s:%s' % (user, password))[:-1]
            authheader =  "Basic %s" % base64string
            req.add_header("Authorization", authheader)
            try:
                handle = urlopen(req)
            except IOError, e:
                eg.PrintError("Webserver: Error " + str(e.code if hasattr(e, "code") else e) + ": " + text.msg6)
                return None
        thepage = unquote(handle.read()) # handle.read()
        return thepage


    def Configure(self, event="", host="http://127.0.0.1:80", user="", password=""):
        text = self.text
        panel = eg.ConfigPanel(self)
        eventCtrl = panel.TextCtrl(event)
        hostCtrl = panel.TextCtrl(host)
        userCtrl = panel.TextCtrl(user)
        passwordCtrl = panel.TextCtrl(password)
        fl = wx.EXPAND|wx.TOP
        box=wx.GridBagSizer(2, 5)
        box.Add(panel.StaticText(text.event), (0, 0), flag = wx.TOP, border=12)
        box.Add(eventCtrl, (0, 1), flag = fl, border=9)
        box.Add(panel.StaticText(text.url), (2, 0), flag = wx.TOP, border=12)
        box.Add(hostCtrl, (2, 1), flag = fl, border=9)
        box.Add(panel.StaticText(text.username), (4, 0), flag=wx.TOP, border=12)
        box.Add(userCtrl, (4, 1), flag = fl, border=9)
        box.Add(panel.StaticText(text.password), (5, 0), flag=wx.TOP, border=12)
        box.Add(passwordCtrl, (5, 1), flag = fl, border=9)
        box.AddGrowableCol(1)
        panel.sizer.Add(box, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        while panel.Affirmed():
            panel.SetResult(
                eventCtrl.GetValue(),
                hostCtrl.GetValue(),
                userCtrl.GetValue(),
                passwordCtrl.GetValue(),
            )

#===============================================================================

class Webserver(eg.PluginBase):

    server = None
    wsClients = {}
    wsClientsTime = {}
    knowlClients = {}
    pubPerClients = {}
    pubVars = {}
    pubPerVars = {}
    wsServers = {}
    lastEnduringEvent = None

    class text:
        generalBox = "General Settings"
        port = "TCP/IP port:"
        documentRoot = "HTML documents root:"
        eventPrefix = "Event prefix:"
        authBox = "Basic Authentication"
        serverTitle = "Server title"
        authRealm = "Realm:"
        authUsername = "Username:"
        authPassword = "Password:"
        dialogPers = "Persistent variables"
        dialogTemp = "Temporary variables"
        ok = "OK"
        cancel = "Cancel"
        vrbl = "Variable name"
        defVal = "Variable value"
        delete = "Delete selected variables"
        clear = "Clear all variables"
        autosave = "Automatically save the document when the value of a persistent variable is changed"
        nonAjaxBox = "Additional settings for non-AJAX POST requests"
        listSplitter = "String between list items:"
        valueSplitter = "String between returned values:"
        parsing = "disable parsing of string"
        certfile = "SSL certificate"
        keyfile = "SSL private key"
        sslTool = "Select the appropriate file if you want to use a secure "\
"protocol (https).\n If this field remains blank, the server will use an "\
"unsecure protocol (http). "
        cMask = (
            "crt files (*.crt)|*.crt"
            "|pem files (*.pem)|*.pem"
            "|All files (*.*)|*.*"
        )
        kMask = (
            "key files (*.key)|*.key"
            "|pem files (*.pem)|*.pem"
            "|All files (*.*)|*.*"
        )
        modeClientChoiceLabel = 'Client address to specify as'
        modeClientChoice = (
            'Explicitly (or Python expression)',
            'From eg.event.payload[0]',
        )
        host = "TCP/IP address:"
        wsClientDisconn = "WsClientDisconnected"
        wsClientConn = "WsClientConnected"
        wsServerDisconn = "WsServerDisconnected"
        wsServerConn = "WsServerConnected"
        suff_started = "Started"
        suff_stopped = "Stopped"
        started = "Webserver started as %s on port %i"
        secur = (
            "secured (https://)",
            "unsecured (http://)",
        )
        stopped = "Webserver on port %i stopped"
        forcDel = "WebSocket client %s force deleted"
        keyErr = "KeyError (non existent client): %s"
        noAutWs = "Basic Authentication is not required when WebSocket connections from clients"
        sendFail = 'Send a message to the server "%s" failed'
        noConn = 'Connection to the server "%s" is not created or has been interrupted.'
        srvrExists = 'Server named "%s" is already connected'
        wsConError = 'Error on the WebSocket connection to the server "%s"'
        wsClients = "Websocket clients"
        wsServers = "Websocket servers"
        colLabelsCli = (
            "Client IP address",
            "Client TCP/IP port",
            "Connected since ...",
        )
        colLabelsSrvr = (
            "Server title",
            "Server URL",
            "Connected since ...",
        )
        abort = "Disconnect"
        abortAll = "Disconnect all"
        refresh = "Refresh"
        cond = "Condition for data sending (python expression):"
        setVar = (
            "Action to perform only if the variable does not exist yet",
            "Action to perform always"
        )

    def __init__(self):
        self.AddEvents()
        self.AddActionsFromList(ACTIONS)


    def OnComputerSuspend(self, dummy):
        self.__stop__()


    def OnComputerResume(self, dummy):
        trItem = self.info.treeItem
        args = list(trItem.GetArguments())
        self.__start__(*args)


    def __start__(
        self,
        prefix=None,
        port = 80,
        basepath = None,
        authRealm = "Eventghost",
        authUsername = "",
        authPassword = "",
        pubPerVars = {},
        autosave = False,
        listSplitter = ",",
        valueSplitter = ";;",
        certfile = "",
        keyfile = "",
        noAutWs = False
    ):

        self.port = port
        self.info.eventPrefix = prefix
        if authUsername or authPassword:
            authString = b64encode(authUsername + ':' + authPassword)
        else:
            authString = None
        self.knowlClients = {}
        self.pubPerClients = {}
        self.pubVars = {}

        self.wsClients = {}
        self.wsClientsTime = {}

        self.tv = KeysAsAttrs(self.pubVars)
        self.pubPerVars = pubPerVars
        self.pv = KeysAsAttrs(self.pubPerVars)
        self.wsServers = {}

        self.autosave = autosave
        self.listSplitter = unicode(listSplitter)
        self.valueSplitter = unicode(valueSplitter)
        self.noAutWs = noAutWs
        for key in self.pubPerVars.iterkeys():
            self.pubPerClients[key] = []
        class RequestHandler(MyHTTPRequestHandler):
            plugin = self
            environment = Environment(loader=FileLoader())
            environment.globals = eg.globals.__dict__
            repeatTimer = eg.ResettableTimer(self.EndLastEnduringEvent)
        RequestHandler.basepath = basepath
        RequestHandler.authRealm = authRealm
        RequestHandler.authString = authString
        self.server = MyServer(RequestHandler, port, certfile, keyfile)
        self.server.Start()
        sr = int(not (isfile(certfile) and isfile(keyfile)))
        self.TriggerEvent(
            self.text.suff_started,
            self.text.started % (self.text.secur[sr], port)
        )
        eg.PrintNotice("Persistent values: " + repr(self.pubPerVars))
        

    def __stop__(self):
        clnts = list(self.wsClients.iterkeys())
        for clnt in clnts:
            self.wsClients[clnt].on_ws_closed()
        self.StopAllClients()
        self.server.Stop()
        self.server = None
        self.TriggerEvent(
            self.text.suff_stopped,
            payload = self.text.stopped % self.port
        )


    def EndLastEnduringEvent(self):
        if self.lastEnduringEvent:
            self.lastEnduringEvent.SetShouldEnd()
        
        
    def GetValue(self, key, client = None):
        if key in self.pubVars:
            if client:
                tmp = self.knowlClients[key]
                if not client in tmp:
                    tmp.append(client)
                return self.pubVars[key]
            else:
                return self.pubVars[key]


    def GetUniValue(self, key, client = None):
        if key in self.pubVars:
            return self.GetValue(key, client)
        elif key in self.pubPerVars:
            return self.GetPersistentValue(key, client)


    def DelValue(self, key):
        if key in self.pubVars:
            del self.pubVars[key]
        if key in self.knowlClients:
            del self.knowlClients[key]


    def ClearValues(self):
        tmpLst = list(self.pubVars.iterkeys())
        for key in tmpLst:
            del self.pubVars[key]
        self.knowlClients = {}


    def DelPersistentValue(self, key):
        if key in self.pubPerVars:
            del self.pubPerVars[key]
            wx.CallAfter(self.SetDocIsDirty)
        if key in self.pubPerClients:
            del self.pubPerClients[key]


    def ClearPersistentValues(self):
        tmpLst = list(self.pubPerVars.iterkeys())
        for key in tmpLst:
            del self.pubPerVars[key]
        self.pubPerClients = {}
        wx.CallAfter(self.SetDocIsDirty)


    def GetPersistentValue(self, key, client = None):
        if key in self.pubPerVars:
            if client:
                tmp = self.pubPerClients[key]
                if not client in tmp:
                    tmp.append(client)
                return self.pubPerVars[key]
            else:
                return self.pubPerVars[key]


    def SetValue(self, key, value):
        if key not in self.pubPerVars:
            if key not in self.pubVars or value != self.pubVars[key]:
                self.pubVars[key] = unicode(value)
                self.knowlClients[key] = []
           

    def SetPersistentValue(self, key, value):
        if key not in self.pubVars:
            if key not in self.pubPerVars or value != self.pubPerVars[key]:
                self.pubPerVars[key] = unicode(value)
                self.pubPerClients[key] = []
                wx.CallAfter(self.SetDocIsDirty)
           

    def SetClientsFlags(self, key):
        if key not in self.pubVars:
            self.pubVars[key] = "dummy"
        self.knowlClients[key] = []
        

    def GetChangedValues(self, client):
        tmpDict = {}
        for key, value in self.pubVars.iteritems():
            if not client in self.knowlClients[key]:
                tmpDict[key] = value
                self.knowlClients[key].append(client)
        for key, value in self.pubPerVars.iteritems():
            if not client in self.pubPerClients[key]:
                tmpDict[key] = value
                self.pubPerClients[key].append(client)
        return {"method":"Values","kwargs":tmpDict}


    def GetAllValues(self, client = None):
        try:
            tmpDict = {}
            for key, value in self.pubVars.iteritems():
                if client:
                    if not client in self.knowlClients[key]:
                        self.knowlClients[key].append(client)
                tmpDict[key] = value
            for key, value in self.pubPerVars.iteritems():
                if client:
                    if not client in self.pubPerClients[key]:
                        self.pubPerClients[key].append(client)
                tmpDict[key] = value
            return {"method":"Values","kwargs":tmpDict}
        except:
            eg.PrintTraceback()


    def BroadcastMessage(self, message):
        tmp = list(self.wsClients.iteritems())
        for key, client in tmp:
            try:
                client.write_message(message)
            except Exception, exc:
                if exc.args[0] in (10053, 10054, 10060):
                    if client in self.wsClients:
                        del self.wsClients[client]
                    if client in self.wsClientsTime:
                        del self.wsClientsTime[client]
                    eg.PrintNotice(self.text.forcDel % repr(client))
                    self.TriggerEvent(
                        self.text.wsClientDisconn,
                        payload = [client]
                    )
                else:
                    #eg.PrintTraceback() # debugging ...
                    return


    def StopPeriodicTasks(self, kind, taskName = ""):
        heap = list(eg.scheduler.__dict__['heap'])
        for t in heap:
            if hasattr(t, "__len__") and hasattr(t[2], "__len__") and len(t[2]) > 2 and hasattr(t[2][-1], "__self__"):
                try:
                    if t[2][-1].__self__.plugin == self:
                        if  kind: # all or all named
                            if taskName == "" or taskName == t[2][2]:
                                eg.scheduler.CancelTask(t)
                        elif t[2][0] is None: # only broadcast type
                            if taskName == "" or taskName == t[2][2]:
                                eg.scheduler.CancelTask(t)
                except:
                    pass


    def StopClientPeriodicTasks(self, client, taskName = ""):
        heap = list(eg.scheduler.__dict__['heap'])
        for t in heap:
            if hasattr(t, "__len__") and hasattr(t[2], "__len__") and len(t[2]) > 2 and hasattr(t[2][-1], "__self__") and t[2][0] is not None:
                try:
                    if t[2][-1].__self__.plugin == self and t[2][0] == client:
                        if taskName == "" or taskName ==  t[2][2]:
                            eg.scheduler.CancelTask(t)
                except:
                    pass


    def ProcessTheArguments(
        self,
        handler,
        methodName,
        args,
        kwargs,
    ):
        sender = handler.clAddr[0]
        result = None
        if methodName == "GetGlobalValue":
            if len(args):
                try:
                    result = unicode(handler.environment.globals[args[0]])
                except:
                    pass
        elif methodName == "GetValue":
            if len(args):
                try:
                    result = self.GetValue(args[0], sender)
                except:
                    pass
        elif methodName == "GetPersistentValue":
            if len(args):
                try:
                    result = self.GetPersistentValue(
                        args[0],
                        sender
                    )
                except:
                    result = None
        elif methodName == "SetValue":
            if len(args):
                try:
                    self.SetValue(args[0], args[1])
                    result = True
                except:
                    result = False
        elif methodName == "SetPersistentValue":
            if len(args):
                try:
                    self.SetPersistentValue(args[0], args[1])
                    result = True
                except:
                    result = False
        elif methodName == "GetAllValues":
            result = self.GetAllValues(sender)
        elif methodName == "GetChangedValues":
            result = self.GetChangedValues(sender)
        elif methodName == "ExecuteScript":
            try:
                result = eval(args[0])
            except:
                print "Webserver: ExecuteScript Error: args[0] = ", args[0]
                result = None
                raise
        elif methodName == "TriggerEvent":
            if 'payload' in kwargs:
                if isinstance(kwargs['payload'], (str, unicode)):
                    if kwargs['payload'] == 'client_address':
                        kwargs['payload'] = [handler.clAddr]
                elif isinstance(kwargs['payload'], (list, tuple)):
                    tmp = list(kwargs['payload'])
                    for i, item in enumerate(tmp):
                        if item == 'client_address':
                            tmp[i] = handler.clAddr
                    kwargs['payload'] = tmp
            if 'prefix' in kwargs:
                eg.TriggerEvent(*args, **kwargs)
            else:
                self.TriggerEvent(*args, **kwargs)
        elif methodName == "TriggerEnduringEvent":
            self.EndLastEnduringEvent()
            if 'prefix' in kwargs:
                self.lastEnduringEvent=eg.TriggerEnduringEvent(*args, **kwargs)
            else:
                self.lastEnduringEvent=self.TriggerEnduringEvent(*args, **kwargs)
            handler.repeatTimer.Reset(2000)
        elif methodName == "RepeatEnduringEvent":
            handler.repeatTimer.Reset(2000)
        elif methodName == "EndLastEvent":
            handler.repeatTimer.Reset(None)
            #self.EndLastEvent()
            self.EndLastEnduringEvent()
        return result



    def ProcessTheArguments_S_C(
        self,
        title,
        methodName,
        args,
        kwargs,
    ):
        result = None
        if methodName == "GetGlobalValue":
            if len(args):
                try:
                    result = unicode(eg.globals.__dict__[args[0]])
                except:
                    pass
        elif methodName == "GetValue":
            if len(args):
                try:
                    result = self.GetValue(args[0])
                except:
                    pass
        elif methodName == "GetPersistentValue":
            if len(args):
                try:
                    result = self.GetPersistentValue(args[0])
                except:
                    result = None
        elif methodName == "SetValue":
            if len(args):
                try:
                    self.SetValue(args[0], args[1])
                    result = True
                except:
                    result = False
        elif methodName == "SetPersistentValue":
            if len(args):
                try:
                    self.SetPersistentValue(args[0], args[1])
                    result = True
                except:
                    result = False
        elif methodName == "GetAllValues":
            result = self.GetAllValues()
        #elif methodName == "GetChangedValues":
        #    result = self.GetChangedValues(sender)
        elif methodName == "ExecuteScript":
            try:
                result = eval(args[0])
            except:
                print "Webserver: ExecuteScript Error: args[0] = ", args[0]
                result = None
                raise
        elif methodName == "TriggerEvent":
            if 'payload' in kwargs and kwargs['payload'] == 'server_title':
                kwargs['payload'] = [title]
            if 'prefix' in kwargs:
                eg.TriggerEvent(*args, **kwargs)
            else:
                self.TriggerEvent(*args, **kwargs)
        return result


    def SetDocIsDirty(self):
        eg.document.SetIsDirty()
        if self.autosave:
            eg.document.Save()


    def EvalString2(self, strng, action):
        dct = {}
        dct.update(action.__dict__)
        dct.update(self.__dict__)


        def filterFunction(word):
            return eval(word, {}, dct)

        try:
            res = eval(strng, {}, dct)
        except Exception as e:
            try:
                res = eg.ParseString(strng, filterFunction)
            except:
                res = strng
        return res


    def EvalString(self, strng, action = None):
        dct = {}
        if action is not None:
            dct.update(action.__dict__)
        dct.update(self.__dict__)


        def filterFunction(word):
            return eval(word, {}, dct)

        try:
            res = eg.ParseString(strng, filterFunction)
        except:
            if strng.startswith("{") and strng.endswith("}"):
                res = strng[1:-1]
            else:
                res = strng
        try:
            res = eval(res, {}, dct)
        except:
            pass
        return res


    def ServerSendMessage(self, client, message):
        if client in self.wsClients:
            try:
                self.wsClients[client].write_message(message)
            except Exception, exc:
                if exc.args[0] in (10053, 10054, 10060):
                    del self.wsClients[client]
                    del self.wsClientsTime[client]
                    eg.PrintNotice(self.text.forcDel % repr(client))
                    self.TriggerEvent(
                        self.text.wsClientDisconn,
                        payload = [client]
                    )
                else:
                    #eg.PrintTraceback() # debugging ...
                    pass
        else:
            eg.PrintNotice(self.text.keyErr % repr(client))
       

    def StartClient(
        self,
        title,
        url,
        login,
        password,
        noCert
    ):
        wsC = WebSocketClient(title, url, login, password, noCert, self)
        if not title in self.wsServers.iterkeys():
            self.wsServers[title] = wsC
            ct = Thread(target = wsC.start)
            ct.start()
        else:
            eg.PrintError(self.text.srvrExists % title)


    def StopClient(self, title):
        if title in self.wsServers:
            try:
                self.wsServers[title].close()
            except:
                pass
            try:
                del self.wsServers[title]
            except:
                pass


    def StopAllClients(self):
        clients = list(self.wsServers.iteritems())
        for title, client in clients:
            client.close()
            del self.wsServers[title]


    def on_open(self, server):
        server.conTime = eg.Utils.time.time()
        self.TriggerEvent(
            "%s.%s" % (self.text.wsServerConn, server.title),
            payload = server.title
        )


    def on_message(self, server, message):
        try:
            message = message.decode('utf-8')
        except Exception as e:
            pass
        try:
            data = loads(message)
        except:
            self.TriggerEvent(
                u"ServerMessage.%s" % message,
                payload=(server.title, message)
            )
            return
        # JSON request
        try:
            methodName = data["method"]
        except:
            self.TriggerEvent("ServerMessage", payload = (server.title, data))
        else:
            if methodName in METHODS[:8]:
                try:
                    args = data.get("args", [])
                    kwargs = data.get("kwargs", {})
                    result = self.ProcessTheArguments_S_C(
                        server.title,
                        methodName,
                        args,
                        kwargs
                    )
                    content = dumps(result)
                    try:
                        self.ClientSendMessage(server.title, content)
                    except:
                        eg.PrintTraceback()
                except:
                    eg.PrintTraceback()
            else:
                self.TriggerEvent(
                    methodName,
                    payload = (server.title, data)
                )


    def ClientSendMessage(self, title, message):
        if title in self.wsServers:
            try:
                self.wsServers[title].send(message.encode("utf-8"))
            except:
                eg.PrintError(self.text.sendFail % title)
        else:
            eg.PrintError(self.text.noConn % title)


    def GetActions(self, id, action = None):
        def Traverse(item):
            if item.__class__ == eg.document.ActionItem:
                if hasattr(item.executable, 'actionId'):
                    #if item.executable.name == actName and\
                    if item.executable.actionId == id and\
                    item.executable.plugin.name == self.name and\
                    item.executable != action and item.args:
                        actions.append(item)
            elif item and item.childs:
                    for child in item.childs:
                        Traverse(child)
        actions = []
        Traverse(eg.document.__dict__['root'])
        return actions

    def Configure(
        self,
        prefix="HTTP",
        port = 80,
        basepath="",
        authRealm="EventGhost",
        authUsername="",
        authPassword="",
        pubPerVars = {},
        autosave = False,
        listSplitter =",",
        valueSplitter =";;",
        certfile = "",
        keyfile = "",
        noAutWs = False
    ):
        text = self.text
        panel = eg.ConfigPanel()
        portCtrl = panel.SpinIntCtrl(port, min=1, max=65535)
        filepathCtrl = panel.DirBrowseButton(basepath)
        certfileCtrl = eg.FileBrowseButton(
            panel,
            -1,
            toolTip = text.sslTool,
            dialogTitle = text.certfile,
            buttonText = eg.text.General.browse,
            startDirectory = "",
            initialValue = certfile,
            fileMask = text.cMask,
        )
        keyfileCtrl = eg.FileBrowseButton(
            panel,
            -1,
            toolTip = text.sslTool,
            dialogTitle = text.keyfile,
            buttonText = eg.text.General.browse,
            startDirectory = "",
            initialValue = keyfile,
            fileMask = text.kMask,
        )
        editCtrl = panel.TextCtrl(prefix)
        authRealmCtrl = panel.TextCtrl(authRealm)
        authUsernameCtrl = panel.TextCtrl(authUsername)
        authPasswordCtrl = panel.TextCtrl(authPassword)
        listSplitterCtrl = panel.TextCtrl(listSplitter)
        valueSplitterCtrl = panel.TextCtrl(valueSplitter)

        labels = (
            panel.StaticText(text.port),
            panel.StaticText(text.documentRoot),
            panel.StaticText(text.eventPrefix),
            panel.StaticText(text.authRealm),
            panel.StaticText(text.authUsername),
            panel.StaticText(text.authPassword),
            panel.StaticText(text.listSplitter),
            panel.StaticText(text.valueSplitter),
            panel.StaticText(text.certfile + ":"),
            panel.StaticText(text.keyfile + ":")
        )
        eg.EqualizeWidths(labels)
        labels[8].SetToolTipString(text.sslTool)
        labels[9].SetToolTipString(text.sslTool)
        noAutWsCtrl = wx.CheckBox(panel, -1, self.text.noAutWs)
        noAutWsCtrl.SetValue(noAutWs)

        sizer = wx.FlexGridSizer(5, 2, 5, 5)
        sizer.AddGrowableCol(1)
        sizer.Add(labels[0], 0, ACV)
        sizer.Add(portCtrl)
        sizer.Add(labels[1], 0, ACV)
        sizer.Add(filepathCtrl, 0, wx.EXPAND)
        sizer.Add(labels[8], 0, ACV)
        sizer.Add(certfileCtrl, 0, wx.EXPAND)
        sizer.Add(labels[9], 0, ACV)
        sizer.Add(keyfileCtrl, 0, wx.EXPAND)
        sizer.Add(labels[2], 0, ACV)
        sizer.Add(editCtrl)
        staticBox = wx.StaticBox(panel, label=text.generalBox)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        sizer = wx.FlexGridSizer(3, 2, 5, 5)
        sizer.Add(labels[3], 0, ACV)
        sizer.Add(authRealmCtrl)
        sizer.Add(labels[4], 0, ACV)
        sizer.Add(authUsernameCtrl)
        sizer.Add(labels[5], 0, ACV)
        sizer.Add(authPasswordCtrl)
        staticBox = wx.StaticBox(panel, label=text.authBox)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer, 0, wx.LEFT|wx.RIGHT, 5)
        staticBoxSizer.Add(noAutWsCtrl,0,wx.LEFT|wx.TOP|wx.BOTTOM,5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND|wx.TOP, 10)

        sizer = wx.FlexGridSizer(3, 2, 5, 5)
        sizer.Add(labels[6], 0, ACV)
        sizer.Add(listSplitterCtrl)
        sizer.Add(labels[7], 0, ACV)
        sizer.Add(valueSplitterCtrl)
        staticBox = wx.StaticBox(panel, label=text.nonAjaxBox)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND|wx.TOP, 10)
        
#        def ConfigureTargets(event):
#            dialog = ConfigureTargetsDialog(panel, [])
#            dialog.ShowModal()
#            dialog.Destroy()
#        configureTargetsButton = panel.Button("Configure Targets")
#        configureTargetsButton.Bind(wx.EVT_BUTTON, ConfigureTargets)
#        panel.sizer.Add(configureTargetsButton)
        aSaveCtrl = wx.CheckBox(panel, -1, self.text.autosave)
        aSaveCtrl.SetValue(autosave)
        dialogButton = wx.Button(panel,-1,self.text.dialogPers)
        dialogButton2 = wx.Button(panel,-1,self.text.dialogTemp)
        dialogButton3 = wx.Button(panel,-1,self.text.wsClients)
        dialogButton4 = wx.Button(panel,-1,self.text.wsServers)
        dialogSizer = wx.BoxSizer(wx.HORIZONTAL)
        dialogSizer.Add(dialogButton)
        dialogSizer.Add(dialogButton2,0,wx.LEFT,15)
        dialogSizer.Add(dialogButton3,0,wx.LEFT,15)
        dialogSizer.Add(dialogButton4,0,wx.LEFT,15)
        panel.sizer.Add(aSaveCtrl,0,wx.TOP,5)
        panel.sizer.Add(dialogSizer,0,wx.TOP,5)

        def OnDialogBtn(evt):
            dlg = VariableDialog(
                parent = panel,
                plugin = self,
                pers = True
            )
            dlg.Centre()
            wx.CallAfter(
                dlg.ShowVariableDialog,
                self.text.dialogPers,
            )
            evt.Skip()
        dialogButton.Bind(wx.EVT_BUTTON, OnDialogBtn)


        def OnDialog2Btn(evt):
            dlg = VariableDialog(
                parent = panel,
                plugin = self,
            )
            dlg.Centre()
            wx.CallAfter(
                dlg.ShowVariableDialog,
                self.text.dialogTemp,
            )
            evt.Skip()
        dialogButton2.Bind(wx.EVT_BUTTON, OnDialog2Btn)


        def OnDialog3Btn(evt):
            dlg = ClientsDialog(
                parent = panel,
                plugin = self,
            )
            dlg.Centre()
            wx.CallAfter(dlg.ShowClientsDialog)
            evt.Skip()
        dialogButton3.Bind(wx.EVT_BUTTON, OnDialog3Btn)


        def OnDialog4Btn(evt):
            dlg = ServersDialog(
                parent = panel,
                plugin = self,
            )
            dlg.Centre()
            wx.CallAfter(dlg.ShowServersDialog)
            evt.Skip()
        dialogButton4.Bind(wx.EVT_BUTTON, OnDialog4Btn)


        while panel.Affirmed():
            panel.SetResult(
                editCtrl.GetValue(),
                portCtrl.GetValue(),
                filepathCtrl.GetValue(),
                authRealmCtrl.GetValue(),
                authUsernameCtrl.GetValue(),
                authPasswordCtrl.GetValue(),
                self.pubPerVars,
                aSaveCtrl.GetValue(),
                listSplitterCtrl.GetValue(),
                valueSplitterCtrl.GetValue(),
                certfileCtrl.GetValue(),
                keyfileCtrl.GetValue(),
                noAutWsCtrl.GetValue()
            )
#===============================================================================

class ConfigureTargetsDialog(eg.Dialog):

    def __init__(self, parent, targets):
        self.selectedItem = None
        eg.Dialog.__init__(
            self,
            parent,
            -1,
            "Configure Targets",
            style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER
        )
        self.listCtrl = wx.ListCtrl(self, style=wx.LC_REPORT, size=(200, 200))
        self.listCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelectItem)
        self.listCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnDeselectItem)
        self.listCtrl.InsertColumn(0, "Target")
        for i in range(10):
            self.listCtrl.InsertStringItem(i, "Test %d" % i)

        addButton = self.Button("Add")
        editButton = self.Button("Edit")
        deleteButton = self.Button("Remove")
        deleteButton.Bind(wx.EVT_BUTTON, self.OnDelete)
        okButton = self.Button("OK")
        cancelButton = self.Button("Cancel")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.listCtrl, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(addButton)
        sizer.Add(editButton)
        sizer.Add(deleteButton)
        sizer.Add(okButton)
        sizer.Add(cancelButton)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.SetMinSize(self.GetSize())


    def OnSelectItem(self, event):
        self.selectedItem = event.GetItem().GetId()


    def OnDeselectItem(self, event):
        self.selectedItem = None


    def OnDelete(self, event):
        if self.selectedItem is not None:
            self.listCtrl.DeleteItem(self.selectedItem)
#===============================================================================

class StartClient(eg.ActionBase):
    actionId = "StartClient"

    class text:
        noCert = "Do not require the server certificate when secured connection"
        serverUrl = "Server URL"
        uniq = "The title must be unique !"

    def __call__(
        self,
        title = "Server",
        url = "ws://echo.websocket.org",
        login = "",
        password = "",
        noCert = False
    ):
        title = eg.ParseString(title)
        url = eg.ParseString(url)
        login = eg.ParseString(login)
        password = eg.ParseString(password)
        self.plugin.StartClient(title, url, login, password, noCert)


    def Configure(
        self,
        title = "Server",
        url = "ws://echo.websocket.org",
        login = "",
        password = "",
        noCert = False
    ):
        text = self.text
        pext = self.plugin.text
        panel = eg.ConfigPanel()


        titleCtrl = wx.TextCtrl(panel,-1,title)
        titleCtrl.SetToolTipString(text.uniq)
        titleSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, pext.serverTitle),
            wx.HORIZONTAL
        )
        titleSizer.Add(titleCtrl, 1, wx.EXPAND)

        urlCtrl = wx.TextCtrl(panel,-1,url)
        urlSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.serverUrl),
            wx.HORIZONTAL
        )
        urlSizer.Add(urlCtrl, 1, wx.EXPAND)
        loginLabel = wx.StaticText(panel,-1,pext.authUsername)
        passwordLabel = wx.StaticText(panel,-1,pext.authPassword)
        loginCtrl = wx.TextCtrl(panel,-1,login)
        passwordCtrl = wx.TextCtrl(panel,-1,password)
        noCertCtrl = wx.CheckBox(panel, -1, text.noCert)
        noCertCtrl.SetValue(noCert)
        credSizer = wx.GridBagSizer(10, 8)
        topSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, pext.authBox),
            wx.HORIZONTAL
        )

        credSizer.Add(loginLabel,(1,0),(1,1), flag = ACV)
        credSizer.Add(loginCtrl,(1,1),(1,1), flag = wx.EXPAND)
        credSizer.Add(passwordLabel,(0,0),(1,1), flag = ACV)
        credSizer.Add(passwordCtrl,(0,1),(1,1), flag = wx.EXPAND)
        credSizer.AddGrowableCol(1)

        topSizer.Add(credSizer, 1, wx.EXPAND)
        panel.sizer.Add(titleSizer, 0, wx.EXPAND)
        panel.sizer.Add(urlSizer, 0, wx.EXPAND|wx.TOP,8)
        panel.sizer.Add(topSizer, 0, wx.EXPAND|wx.TOP,8)
        panel.sizer.Add(noCertCtrl, 0, wx.TOP,8)
        
        def onTitleCtrl(evt):
            title = evt.GetString()
            actions = self.plugin.GetActions(StartClient.actionId, self)
            ts = [actn.args[0] for actn in actions]
            panel.EnableButtons(title != "" and title not in ts)
            evt.Skip()
        titleCtrl.Bind(wx.EVT_TEXT, onTitleCtrl)

        while panel.Affirmed():
            panel.SetResult(
                titleCtrl.GetValue(),
                urlCtrl.GetValue(),
                loginCtrl.GetValue(),
                passwordCtrl.GetValue(),
                noCertCtrl.GetValue()
            )
#===============================================================================

class StopClient(eg.ActionBase):

    def __call__(self, title):
        title = eg.ParseString(title)
        self.plugin.StopClient(title)


    def Configure(self, title = ""):
        text = self.plugin.text
        panel = eg.ConfigPanel()
        actions = self.plugin.GetActions(StartClient.actionId)
        ts = [actn.args[0] for actn in actions]
        titleCtrl = wx.ComboBox(panel, -1, choices = ts, style = wx.CB_DROPDOWN)
        if title:
            titleCtrl.SetValue(title)
        elif len(ts):
            titleCtrl.SetSelection(0)
        staticBox = wx.StaticBox(panel, -1, text.serverTitle)
        topSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        topSizer.Add(titleCtrl,1,wx.LEFT|wx.EXPAND)
        panel.sizer.Add(topSizer, 0, wx.LEFT|wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                titleCtrl.GetValue(),
            )
#===============================================================================

class StopAllClients(eg.ActionBase):

    def __call__(self):
        self.plugin.StopAllClients()
#===============================================================================

class ClSendMessage(eg.ActionBase):
    eg_event = None
    eg_result = None

    class text:
        mess = "Message to be sent"


    def __call__(
        self,
        title = "",
        message = "",
        pars = False,
        cond = ""

    ):
        self.eg_event = eg.event
        self.eg_result = eg.result
        self.pars = pars
        message = replInstVal(message)
        title = replInstVal(title)
        cond = replInstVal(cond)

        cond = self.plugin.EvalString(cond, self) if cond != "" else True
        if cond:
            if not pars:
                message = self.plugin.EvalString2(message, self)
            self.plugin.ClientSendMessage(
                self.plugin.EvalString(title, self),
                message,
            )


    def GetLabel(self, title, message, pars, cond):
        return "%s: %s: %s" % (self.name, title, message[:24])


    def Configure(
        self,
        title ="",
        message = "",
        pars = False,
        cond = ""
    ):
        pext = self.plugin.text
        panel = eg.ConfigPanel()
        actions = self.plugin.GetActions(StartClient.actionId)
        ts = [actn.args[0] for actn in actions]
        titleCtrl = wx.ComboBox(panel, -1, choices = ts, style = wx.CB_DROPDOWN)
        if title:
            titleCtrl.SetValue(title)
        elif len(ts):
            titleCtrl.SetSelection(0)
        staticBox = wx.StaticBox(panel, -1, pext.serverTitle)
        topSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        topSizer.Add(titleCtrl,1,wx.LEFT|wx.EXPAND)
        messCtrl = wx.TextCtrl(panel, -1, message)
        messSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, self.text.mess),
            wx.VERTICAL
        )
        parsCtrl = wx.CheckBox(panel, -1, pext.parsing)
        parsCtrl.SetValue(pars)
        condLabel = wx.StaticText(panel, -1, pext.cond)
        condCtrl = wx.TextCtrl(panel, -1, cond)
        messSizer.Add(messCtrl, 0, wx.EXPAND)
        messSizer.Add(parsCtrl, 0, wx.EXPAND|wx.TOP, 3)

        panel.sizer.Add(topSizer, 0, wx.LEFT|wx.EXPAND)
        panel.sizer.Add(messSizer, 0, wx.EXPAND|wx.TOP, 8)
        panel.sizer.Add(condLabel,0,wx.TOP,10)
        panel.sizer.Add(condCtrl,0,wx.EXPAND|wx.TOP,2)

        while panel.Affirmed():
            panel.SetResult(
                titleCtrl.GetValue(),
                messCtrl.GetValue(),
                parsCtrl.GetValue(),
                condCtrl.GetValue()
            )
#===============================================================================

class ClSendValue(eg.ActionBase):
    eg_event = None
    eg_result = None

    class text:
        varnames = "Variable name or list of variables (separated by commas):"

    def __call__(
        self,
        title="",
        varnames = "",
        cond = "",
    ):
        self.eg_event = eg.event
        self.eg_result = eg.result
        #self.pars = pars
        varnames = replInstVal(varnames)
        title = replInstVal(title)
        cond = replInstVal(cond)

        cond = self.plugin.EvalString(cond, self) if cond != "" else True
        if cond:
            try:
                keys = varnames.replace(" ", "")
                keys = keys.split(",")
            except:
                eg.PrintError(self.text.err % str(varnames))
                return
            try:
                vals = {}
                for key in keys:
                    k = self.plugin.EvalString(key, self)
                    vals[k] = self.plugin.GetUniValue(k)
            except:
                eg.PrintError(self.text.err % str(varnames))
            return self.plugin.ClientSendMessage(
                self.plugin.EvalString(title, self),
                dumps({'method':'Values', 'kwargs':vals}),
            )


    def GetLabel(self, title, varnames, cond):
        return "%s: %s: %s" % (self.name, title, varnames)


    def Configure(
        self,
        title="",
        varnames = "",
        cond = "",
    ):
        pext = self.plugin.text
        panel = eg.ConfigPanel()
        actions = self.plugin.GetActions(StartClient.actionId)
        ts = [actn.args[0] for actn in actions]
        titleCtrl = wx.ComboBox(panel, -1, choices = ts, style = wx.CB_DROPDOWN)
        if title:
            titleCtrl.SetValue(title)
        elif len(ts):
            titleCtrl.SetSelection(0)
        staticBox = wx.StaticBox(panel, -1, pext.serverTitle)
        topSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        topSizer.Add(titleCtrl,1,wx.LEFT|wx.EXPAND)
        varnamesCtrl = panel.TextCtrl(varnames)
        condLabel = wx.StaticText(panel, -1, pext.cond)
        condCtrl = wx.TextCtrl(panel, -1, cond)
        messSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, self.text.varnames),
            wx.VERTICAL
        )
        messSizer.Add(varnamesCtrl, 0, wx.EXPAND)
        panel.sizer.Add(topSizer, 0, wx.LEFT|wx.EXPAND)
        panel.sizer.Add(messSizer, 0, wx.EXPAND|wx.TOP, 8)
        panel.sizer.Add(condLabel,0,wx.TOP,10)
        panel.sizer.Add(condCtrl,0,wx.EXPAND|wx.TOP,2)

        while panel.Affirmed():
            panel.SetResult(
                titleCtrl.GetValue(),
                varnamesCtrl.GetValue(),
                condCtrl.GetValue()
            )
#===============================================================================

class ClSendAllValues(eg.ActionBase):
    eg_event = None
    eg_result = None

    def __call__(
        self,
        title = "",
        cond = ""
    ):
        self.eg_event = eg.event
        self.eg_result = eg.result
        title = replInstVal(title)
        cond = replInstVal(cond)

        cond = self.plugin.EvalString(cond, self) if cond != "" else True
        if cond:
            values = self.plugin.GetAllValues()
            self.plugin.ClientSendMessage(
                self.plugin.EvalString(title, self),
                dumps(values)
            )


    def Configure(
        self,
        title = "",
        cond = ""
    ):
        pext = self.plugin.text
        panel = eg.ConfigPanel()
        actions = self.plugin.GetActions(StartClient.actionId)
        ts = [actn.args[0] for actn in actions]
        titleCtrl = wx.ComboBox(panel, -1, choices = ts, style = wx.CB_DROPDOWN)
        condLabel = wx.StaticText(panel, -1, pext.cond)
        condCtrl = wx.TextCtrl(panel, -1, cond)
        if title:
            titleCtrl.SetValue(title)
        elif len(ts):
            titleCtrl.SetSelection(0)
        staticBox = wx.StaticBox(panel, -1, pext.serverTitle)
        topSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        topSizer.Add(titleCtrl,1,wx.LEFT|wx.EXPAND)
        panel.sizer.Add(topSizer, 0, wx.LEFT|wx.EXPAND)
        panel.sizer.Add(condLabel,0,wx.TOP,10)
        panel.sizer.Add(condCtrl,0,wx.EXPAND|wx.TOP,2)

        while panel.Affirmed():
            panel.SetResult(
                titleCtrl.GetValue(),
                condCtrl.GetValue()
            )
#===============================================================================

class ClSendData(eg.ActionBase):
    eg_event = None
    eg_result = None

    class text:
        dataName = "Data name:"
        data2send = "Data for broadcast (python expression):"


    def __call__(
        self,
        title = "",
        dataName = "",
        data2send = "",
        cond = "",
    ):
        self.eg_event = eg.event
        self.eg_result = eg.result
        title = replInstVal(title)
        dataName = replInstVal(dataName)
        data2send = replInstVal(data2send)
        cond = replInstVal(cond)
 
        dataName = self.plugin.EvalString(dataName, self)
        data = self.plugin.EvalString(data2send, self)
        cond = self.plugin.EvalString(cond, self) if cond != "" else True
        if cond:
            self.plugin.ClientSendMessage(
                self.plugin.EvalString(title, self),
                dumps({
                    'method':'Data',
                    'dataName':dataName,
                    'data':data
                })
            )


    def GetLabel(self, title, dataName, data2send, cond):
        return "%s: %s: %s" % (self.name, title, dataName)


    def Configure(
        self,
        title = "",
        dataName = "",
        data2send = "",
        cond = "",
    ):
        pext = self.plugin.text
        text = self.text
        panel = eg.ConfigPanel()

        actions = self.plugin.GetActions(StartClient.actionId)
        ts = [actn.args[0] for actn in actions]
        titleCtrl = wx.ComboBox(panel, -1, choices = ts, style = wx.CB_DROPDOWN)
        if title:
            titleCtrl.SetValue(title)
        elif len(ts):
            titleCtrl.SetSelection(0)
        staticBox = wx.StaticBox(panel, -1, pext.serverTitle)
        topSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        topSizer.Add(titleCtrl,1,wx.LEFT|wx.EXPAND)
        panel.sizer.Add(topSizer, 0, wx.LEFT|wx.EXPAND)

        nameLabel = wx.StaticText(panel, -1, text.dataName)
        sendLabel = wx.StaticText(panel, -1, text.data2send)
        condLabel = wx.StaticText(panel, -1, pext.cond)
        nameCtrl = wx.TextCtrl(panel, -1, dataName)
        sendCtrl = wx.TextCtrl(panel, -1, data2send)
        condCtrl = wx.TextCtrl(panel, -1, cond)
        mainSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, ""),
            wx.VERTICAL
        )
        mainSizer.Add(nameLabel)
        mainSizer.Add(nameCtrl,0,wx.EXPAND|wx.TOP,2)
        mainSizer.Add(sendLabel,0,wx.TOP,10)
        mainSizer.Add(sendCtrl,0,wx.EXPAND|wx.TOP,2)
        panel.sizer.Add(mainSizer,0,wx.TOP|wx.BOTTOM|wx.EXPAND,5)
        panel.sizer.Add(condLabel, 0, wx.TOP, 5)
        panel.sizer.Add(condCtrl, 0, wx.EXPAND|wx.TOP, 2)

        while panel.Affirmed():
            panel.SetResult(
                titleCtrl.GetValue(),
                nameCtrl.GetValue(),
                sendCtrl.GetValue(),
                condCtrl.GetValue(),
            )
#===============================================================================

class ClSendCommand(eg.ActionBase):
    eg_event = None
    eg_result = None

    class text:
        cond = "Condition:"
        cmdName = "Command name:"
        arg1 = "Argument 1:"
        arg2 = "Argument 2:"
        arg3 = "Argument 3:"
        othArgs = "Arguments:"
        kwArgs = "Keyw. arguments:"
        onlyChange = "Data send only if it has been changed"
        period = "Sending period [s]:"
        

    def __call__(
        self,
        title = "",
        cmdName = "",
        cond = "",
        arg1 = "",
        arg2 = "",
        arg3 = "",
        othArgs = "",
        kwArgs = "",
    ):
        self.eg_event = eg.event
        self.eg_result = eg.result
        title = replInstVal(title)
        cmdName = replInstVal(cmdName)
        cond = replInstVal(cond)
        arg1 = replInstVal(arg1)
        arg2 = replInstVal(arg2)
        arg3 = replInstVal(arg3)
        othArgs = replInstVal(othArgs)
        kwArgs = replInstVal(kwArgs)

        cmdName = self.plugin.EvalString(cmdName, self)
        args = [self.plugin.EvalString(arg1)] if arg1 != "" else []
        if arg2 != "":
            args.append(self.plugin.EvalString(arg2, self))
        if arg3 != "":
            args.append(self.plugin.EvalString(arg3, self))
        if othArgs != "":
            try:
                othArgs = list(self.plugin.EvalString(othArgs, self))
                args.extend(othArgs)
            except:
                pass
        kwargs = {}
        if kwArgs != "":
            try:
                kwargs = dict(self.plugin.EvalString2(kwArgs, self))
            except:
                pass
        cond = self.plugin.EvalString(cond, self) if cond != "" else True
        if cond:
            self.plugin.ClientSendMessage(
                self.plugin.EvalString(title, self),
                dumps(
                    {
                        'method' :'Command',
                        'cmdName':cmdName,
                        'args':args,
                        'kwargs':kwargs
                    }
                )
            )


    def GetLabel(
        self,
        title,
        cmdName,
        cond,
        arg1,
        arg2,
        arg3,
        othArgs,
        kwArgs
    ):
        return "%s: %s: %s" % (
            self.name,
            title,
            cmdName
        )


    def Configure(
        self,
        title="",
        cmdName="",
        cond="",
        arg1="",
        arg2="",
        arg3="",
        othArgs="",
        kwArgs ="",
    ):
        panel = eg.ConfigPanel(self)
        pext = self.plugin.text
        text = self.text
        actions = self.plugin.GetActions(StartClient.actionId)
        ts = [actn.args[0] for actn in actions]
        titleCtrl = wx.ComboBox(panel, -1, choices = ts, style = wx.CB_DROPDOWN)
        if title:
            titleCtrl.SetValue(title)
        elif len(ts):
            titleCtrl.SetSelection(0)
        staticBox = wx.StaticBox(panel, -1, pext.serverTitle)
        topSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        topSizer.Add(titleCtrl,1,wx.LEFT|wx.EXPAND)
        panel.sizer.Add(topSizer, 0, wx.LEFT|wx.EXPAND)

        nameLabel = wx.StaticText(panel, -1, text.cmdName)
        condLabel = wx.StaticText(panel, -1, text.cond)
        arg1Label = wx.StaticText(panel, -1, text.arg1)
        arg2Label = wx.StaticText(panel, -1, text.arg2)
        arg3Label = wx.StaticText(panel, -1, text.arg3)
        othLabel = wx.StaticText(panel, -1, text.othArgs)
        kwLabel = wx.StaticText(panel, -1, text.kwArgs)
        nameCtrl = wx.TextCtrl(panel, -1, cmdName)
        condCtrl = wx.TextCtrl(panel, -1, cond)
        arg1Ctrl = wx.TextCtrl(panel, -1, arg1)
        arg2Ctrl = wx.TextCtrl(panel, -1, arg2)
        arg3Ctrl = wx.TextCtrl(panel, -1, arg3)
        othCtrl = wx.TextCtrl(panel, -1, othArgs)
        kwCtrl = wx.TextCtrl(panel, -1, kwArgs)
        mainSizer = wx.FlexGridSizer(7, 2, 2, 10)
        mainSizer.AddGrowableCol(1)
        mainSizer.Add(nameLabel, 0, ACV)
        mainSizer.Add(nameCtrl,0,wx.EXPAND)
        mainSizer.Add(arg1Label, 0, ACV)
        mainSizer.Add(arg1Ctrl,0,wx.EXPAND)
        mainSizer.Add(arg2Label, 0, ACV)
        mainSizer.Add(arg2Ctrl,0,wx.EXPAND)
        mainSizer.Add(arg3Label, 0, ACV)
        mainSizer.Add(arg3Ctrl,0,wx.EXPAND)
        mainSizer.Add(othLabel, 0, ACV)
        mainSizer.Add(othCtrl,0,wx.EXPAND)
        mainSizer.Add(kwLabel, 0, ACV)
        mainSizer.Add(kwCtrl,0,wx.EXPAND)
        mainSizer.Add(condLabel, 0, ACV)
        mainSizer.Add(condCtrl,0,wx.EXPAND)

        messSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, ""),
            wx.VERTICAL
        )
        messSizer.Add(mainSizer,0,wx.EXPAND)
        panel.sizer.Add(messSizer,0,wx.TOP|wx.BOTTOM|wx.EXPAND,5)
       
        while panel.Affirmed():
            panel.SetResult(
                titleCtrl.GetValue(),
                nameCtrl.GetValue(),
                condCtrl.GetValue(),
                arg1Ctrl.GetValue(),
                arg2Ctrl.GetValue(),
                arg3Ctrl.GetValue(),
                othCtrl.GetValue(),
                kwCtrl.GetValue()
            )
#===============================================================================

class ClSendUniversal(eg.ActionBase):
    eg_event = None
    eg_result = None

    class text:
        cond = "Condition:"
        method = "Method:"
        othArgs = "Arguments:"
        kwArgs = "Keyw. arguments:"
        onlyChange = "Data send only if it has been changed"
        period = "Sending period [s]:"
        

    def __call__(
        self,
        title = "",
        method = "",
        cond = "",
        othArgs = "",
        kwArgs = ""
    ):
        self.eg_event = eg.event
        self.eg_result = eg.result
        title = replInstVal(title)
        othArgs = replInstVal(othArgs)
        kwArgs = replInstVal(kwArgs)
        cond = replInstVal(cond)

        args = []
        if othArgs != "":
            try:
                args = list(self.plugin.EvalString(othArgs, self))
            except:
                pass
        kwargs = {}
        if kwArgs != "":
            try:
                kwargs = dict(self.plugin.EvalString2(kwArgs, self))
            except:
                pass

        cond = self.plugin.EvalString(cond, self) if cond != "" else True
        if cond:
            self.plugin.ClientSendMessage(
                self.plugin.EvalString(title, self),
                dumps(
                    {
                        'method' :method,
                        'args':args,
                        'kwargs':kwargs
                    }
                ),
            )


    def GetLabel(
        self,
        title,
        method,
        cond,
        othArgs,
        kwArgs
    ):
        return "%s: %s: %s" % (self.name, title, method)


    def Configure(
        self,
        title = "",
        method = "",
        cond = "",
        othArgs = "",
        kwArgs = ""
    ):
        panel = eg.ConfigPanel(self)
        pext = self.plugin.text
        text = self.text
        actions = self.plugin.GetActions(StartClient.actionId)
        ts = [actn.args[0] for actn in actions]
        titleCtrl = wx.ComboBox(panel, -1, choices = ts, style = wx.CB_DROPDOWN)
        if title:
            titleCtrl.SetValue(title)
        elif len(ts):
            titleCtrl.SetSelection(0)
        staticBox = wx.StaticBox(panel, -1, pext.serverTitle)
        topSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        topSizer.Add(titleCtrl,1,wx.LEFT|wx.EXPAND)
        panel.sizer.Add(topSizer, 0, wx.LEFT|wx.EXPAND)
        staticBox = wx.StaticBox(panel, -1, "")
        methodLabel = wx.StaticText(panel, -1, text.method)
        condLabel = wx.StaticText(panel, -1, text.cond)
        othLabel = wx.StaticText(panel, -1, text.othArgs)
        kwLabel = wx.StaticText(panel, -1, text.kwArgs)
        methodCtrl = wx.ComboBox(
            panel,
            -1,
            choices = METHODS[:8],
            style = wx.CB_DROPDOWN
        )
        methodCtrl.SetValue(method)
        condCtrl = wx.TextCtrl(panel, -1, cond)
        othCtrl = wx.TextCtrl(panel, -1, othArgs)
        kwCtrl = wx.TextCtrl(panel, -1, kwArgs)
        mainSizer = wx.FlexGridSizer(5, 2, 8, 10)
        mainSizer.AddGrowableCol(1)
        mainSizer.Add(methodLabel, 0, ACV)
        mainSizer.Add(methodCtrl,0,wx.EXPAND)
        mainSizer.Add(othLabel, 0, ACV)
        mainSizer.Add(othCtrl,0,wx.EXPAND)
        mainSizer.Add(kwLabel, 0, ACV)
        mainSizer.Add(kwCtrl,0,wx.EXPAND)
        mainSizer.Add(condLabel, 0, ACV)
        mainSizer.Add(condCtrl,0,wx.EXPAND)
        messSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, ""),
            wx.VERTICAL
        )
        messSizer.Add(mainSizer, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
        panel.sizer.Add(messSizer, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
       
        while panel.Affirmed():
            panel.SetResult(
                titleCtrl.GetValue(),
                methodCtrl.GetValue(),
                condCtrl.GetValue(),
                othCtrl.GetValue(),
                kwCtrl.GetValue()
            )
#===============================================================================

class JumpIf(eg.ActionBase):

    class text:
        text1 = "If:"
        text2 = "Jump to:"
        text3 = "and return after execution"
        text4 = "Else jump to:"
        mesg1 = "Select the macro..."
        mesg2 = (
            "Please select the macro that should be executed, if the "
            "condition is fulfilled."
        )
        mesg3 = (
            "Please select the macro that should be executed, if the "
            "condition is not fulfilled."
        )
        tooltip1 = "Enter the name of temporary or persistent variable"
        tooltip2 = "Enter the string to compare"
        choices = (
            'contains',
            "doesn't contain ",
            'is',
            "isn't",
            'starts with',
            'ends with',
        )
        treeLabels = [
            'If %s jump to "%s"',
            ' and return',
            ', else jump to "%s"'
        ]
        err0 = 'Webserver: The variable "%s" does not exist.'
        err1 = "Webserver: Evaluation of expression '%s' failed."

    def __call__(
        self,
        kind = 0,
        link = None,
        gosub = False,
        link2 = None,
        gosub2 = False,
        var = "",
        val = ""
    ):
    
        conds = [
            '%s.find("%s") > -1',
            'not %s.find("%s") > -1',
            '%s == "%s"',
            'not %s == "%s"',
            '%s.startswith("%s")',
            '%s.endswith("%s")'
        ]
        
        if var in self.plugin.pubVars:
            vr = 'self.plugin.pubVars["%s"]' % var
        elif var in self.plugin.pubPerVars:
            vr = 'self.plugin.pubPerVars["%s"]' % var
        else:
            eg.PrintError(self.text.err0 % var)
            return
        expr = conds[kind] % (vr, val)
        try:
            cond = eval(expr)
        except:
            eg.PrintError(self.text.err1 % expr)
            return
        if cond:
            if gosub:
                eg.programReturnStack.append(eg.programCounter)
            nextItem = link.target
            nextIndex = nextItem.parent.GetChildIndex(nextItem)
            eg.indent += 1
            eg.programCounter = (nextItem, nextIndex)
        else:
            if gosub2:
                eg.programReturnStack.append(eg.programCounter)
            nextItem = link2.target
            nextIndex = nextItem.parent.GetChildIndex(nextItem)
            eg.indent += 1
            eg.programCounter = (nextItem, nextIndex)
        return eg.result


    def GetLabel(
        self,
        kind,
        link,
        gosub,
        link2,
        gosub2,
        var,
        val
    ):
        cond = '%s %s "%s"' % (var, self.text.choices[kind], val)
        labels = self.text.treeLabels
        target = link.target if link is not None else None
        target2 = link2.target if link2 is not None else None
        res = labels[0] % (cond, target.name if target is not None else "None")
        if gosub:
            res += labels[1]
        if target2 is not None:
            res += labels[2] % target2.name
            if gosub2:
                res += labels[1]
        return res


    def Configure(
        self,
        kind = 0,
        link = None,
        gosub = False,
        link2 = None,
        gosub2 = False,
        var="",
        val = ""
    ):
        text = self.text
        panel = eg.ConfigPanel()
        lbl1 = wx.StaticText(panel, -1, self.text.text1)
        lbl2 = wx.StaticText(panel, -1, self.text.text2)
        lbl4 = wx.StaticText(panel, -1, self.text.text4)
        ctrl1 = wx.TextCtrl(panel, -1, var)
        ctrl1.SetToolTipString(text.tooltip1)
        ctrl2 = wx.TextCtrl(panel, -1, val)
        ctrl2.SetToolTipString(text.tooltip2)
        kindCtrl = panel.Choice(kind, choices=self.text.choices)
        linkCtrl = panel.MacroSelectButton(
            eg.text.General.choose,
            text.mesg1,
            text.mesg2,
            link
        )
        linkCtrl.textBox.textCtrl.SetToolTipString(text.mesg2)
        linkCtrl.button.SetToolTipString(text.mesg2)
        gosubCtrl = panel.CheckBox(gosub, text.text3)
        linkCtrl2 = panel.MacroSelectButton(
            eg.text.General.choose,
            text.mesg1,
            text.mesg3,
            link2
        )
        linkCtrl2.textBox.textCtrl.SetToolTipString(text.mesg3)
        linkCtrl2.button.SetToolTipString(text.mesg3)
        gosubCtrl2 = panel.CheckBox(gosub2, text.text3)
        eg.EqualizeWidths((lbl1,lbl2,lbl4))
        topSizer = wx.FlexGridSizer(1, 4, 15, 5)
        topSizer.AddGrowableCol(1)
        topSizer.AddGrowableCol(3)
        topSizer.Add(lbl1, 0, wx.ALIGN_CENTER_VERTICAL)
        topSizer.Add(ctrl1, 0, wx.EXPAND)
        topSizer.Add(kindCtrl, 0, wx.EXPAND)
        topSizer.Add(ctrl2, 0, wx.EXPAND)

        sizer = wx.FlexGridSizer(4, 2, 3, 5)
        sizer.AddGrowableCol(1)
        sizer.Add(lbl2, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(linkCtrl, 1, wx.EXPAND)
        sizer.Add((0, 0))
        sizer.Add(gosubCtrl)
        sizer.Add((0, 15))
        sizer.Add((0, 15))
        sizer.Add(lbl4, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(linkCtrl2, 1, wx.EXPAND)
        sizer.Add((0, 0))
        sizer.Add(gosubCtrl2)

        panel.sizer.Add(topSizer, 0, wx.TOP|wx.EXPAND, 10)
        panel.sizer.Add(sizer,0,wx.TOP|wx.EXPAND, 25)
        
        panel.dialog.buttonRow.testButton.Show(False)

        while panel.Affirmed():
            lnk = linkCtrl.GetValue()
            lnk2 = linkCtrl2.GetValue()
            panel.SetResult(
                kindCtrl.GetValue(),
                None if repr(lnk) == "XmlIdLink(-1)" else lnk,
                gosubCtrl.GetValue(),
                None if repr(lnk2) == "XmlIdLink(-1)" else lnk2,
                gosubCtrl2.GetValue(),
                ctrl1.GetValue(),
                ctrl2.GetValue()
            )
#===============================================================================

ACTIONS = (
    (SendEvent,
        "SendEvent",
        "Send event to another EventGhost",
        "Sends event to another EventGhost webserver.",
        None
    ),
    (SendEventExt,
        "SendEventExt",
        "Send event to another webserver",
        "Sends event to another webserver.",
       None
    ),
    (
        JumpIf,
        'JumpIf',
        "Jump according to the value of the variable",
        "Jumps if the value of the variable satisfies the given condition "
        "(with the option to specify the destination "
        "also for the second case).",
        None
    ),
    (eg.ActionGroup,
        'VariableActions',
        'Variable actions',
        'Variable actions', (
        (GetValue,
            "GetValue",
            "Get temporary value",
            "Gets value of temporary variable.",
            False
        ),
        (GetValue,
            "DeleteValue",
            "Delete temporary value",
            "Delets temporary variable.",
            True
        ),
        (GetPersistentValue,
            "GetPersistentValue",
            "Get persistent value",
            "Gets value of persistent variable.",
            False
        ),
        (GetPersistentValue,
            "DeletePersistentValue",
            "Delete persistent value",
            "Delets persistent variable.",
            True
        ),
        (SetValue,
            "SetValue",
            "Set temporary value",
            "Sets value of temporary variable.",
            None
        ),
        (SetPersistentValue,
            "SetPersistentValue",
            "Set persistent value",
            "Sets value of persistent variable.",
            None
        ),
        (SetClientsFlags,
            "SetClientsFlags",
            "Set clients flags",
            "Sets clients flags of dummy variable.",
            None
        ),
    )),
    (eg.ActionGroup,
        'WebsocketActions',
        'Websocket actions server-client',
        'Websocket actions server-client', (
            (WsBroadcastMessage,
            'BroadcastMessage',
            'Broadcast message',
            '''Broadcasts a message to all WebSocket clients.
Message is sent as is (no JSON formatting).''',
            None
            ),
            (WsBroadcastValue,
            'BroadcastValue',
            'Broadcast values',
            '''Broadcasts a value(-s) of a variable(-s)
 (temporary or persistent) to all WebSocket clients.

Specify name of a variable or list of variables (separated by commas,
 without parentheses).
<br>Following the evaluation, a message is formatted as a JSON object.
<br>A client receives a message in the following form:
<br>{'method': 'Values', 'kwargs': {key1: value1, key2: value2, ...}},
<br>where keyX is variable name and valueX is the value of this variable.''',
            False
            ),
            (WsBroadcastAllValues,
            'BroadcastAllValues',
            'Broadcast all values',
            '''Broadcasts the values of all variables (temporary and persistent)
 to all WebSocket clients.

A message is formatted as a JSON object.
A client receives a message in the following form:
{'method': 'Values', 'kwargs': {key1: value1, key2: value2, ...}},
where keyX is variable name and valueX is the value of this variable.''',
            False
            ),
            (WsBroadcastData,
            'WsBroadcastData',
            'Broadcast data',
            '''Broadcasts some data to all WebSocket clients.

Data can be obtained for example by evaluating Python expression.
Sending may be conditional upon the fulfillment (optional) conditions.
The condition may also be a Python expression.
A message is formatted as a JSON object.
A client receives a message in the following form:
{'method': 'Data', 'dataName': dataName, 'data': data}.''',
            False
            ),
            (WsBroadcastCommand,
            'WsBroadcastCmd',
            'Broadcast command',
            '''Broadcasts a command to all WebSocket clients.

This action allows you to specify more complex set of data into a single
 message.<br>Data sending may be conditional upon the fulfillment (optional)
 conditions. The condition can be a Python expression.
<br>A message is formatted as a JSON object.
<br>A client receives a message in the following form:
<br>{'method' :'Command', 'cmdName':cmdName, 'args':args, 'kwargs':kwargs},
<br>where args are the arguments of the lines Argument 1 to 3 and/or argument of
 line Arguments and kwargs is argument from the line Keyw. arguments.
<br>"args" is a Python list, while "kwargs" is a Python dictionary.''',
            False
            ),
            (WsBroadcastUniversal,
            'WsBroadcastUniversal',
            'Broadcast universal packet',
            '''Broadcasts a universal packet to all WebSocket clients.

This action allows you to specify a universal data packet.
<br>Data sending may be conditional upon the fulfillment (optional)
 conditions. The condition can be a Python expression.
<br>A message is formatted as a JSON object.
<br>A client receives a message in the following form:
<br>{'method' :method, 'args':args, 'kwargs':kwargs},
<br>where method is the selected method,
<br>args is argument from the line Arguments
<br>and kwargs is argument from the line Keyw. arguments.
<br>Note: args is a Python list, while kwargs is a Python dictionary.''',
            False
            ),
            (WsSendMessage,
            'SendMessage',
            'Send message',
            '''Sends a message to one WebSocket client.
Message is sent as is (no JSON formatting).''',
            False
            ),
                (WsSendValue,
                'SendValue',
                'Send values',
                '''Sends a value(-s) of a variable(-s) (temporary or persistent)
to one WebSocket client.

Specify name of a variable or list of variables (separated by commas,
 without parentheses).
<br>Following the evaluation, a message is formatted as a JSON object.
<br>A client receives a message in the following form:
<br>{'method': 'Values', 'kwargs': {key1: value1, key2: value2, ...}},
<br>where keyX is variable name and valueX is the value of this variable.''',
                False
                ),
            (WsSendAllValues,
            'SendAllValues',
            'Send all values',
            '''Sends the values of all variables (temporary and persistent)
 to one WebSocket client.

A message is formatted as a JSON object.
A client receives a message in the following form:
{'method': 'Values', 'kwargs': {key1: value1, key2: value2, ...}},
where keyX is variable name and valueX is the value of this variable.''',
            False
            ),
            (WsSendData,
            'WsSendData',
            'Send data',
            '''Sends some data to one WebSocket client.

Data can be obtained for example by evaluating Python expression.
Sending may be conditional upon the fulfillment (optional) conditions.
The condition may also be a Python expression.
A message is formatted as a JSON object.
A client receives a message in the following form:
{'method': 'Data', 'dataName': dataName, 'data': data}.''',
            False
            ),
            (WsSendCommand,
            'WsSendCmd',
            'Send command',
            '''Sends a command to one WebSocket client.

This action allows you to specify more complex set of data into a single
 message.<br>Data sending may be conditional upon the fulfillment (optional)
 conditions. The condition can be a Python expression.
<br>A message is formatted as a JSON object.
<br>A client receives a message in the following form:
<br>{'method' :'Command', 'cmdName':cmdName, 'args':args, 'kwargs':kwargs},
<br>where args are the arguments of the lines Argument 1 to 3 and/or argument of
 line Arguments and kwargs is argument from the line Keyw. arguments.
<br>"args" is a Python list, while "kwargs" is a Python dictionary.''',
            False
            ),
            (WsSendUniversal,
            'WsSendUniversal',
            'Send universal packet',
            '''Sends a universal packet to one WebSocket client.

This action allows you to specify a universal data packet.
<br>Data sending may be conditional upon the fulfillment (optional)
 conditions. The condition can be a Python expression.
<br>A message is formatted as a JSON object.
<br>A client receives a message in the following form:
<br>{'method' :method, 'args':args, 'kwargs':kwargs},
<br>where method is the selected method,
<br>args is argument from the line Arguments
<br>and kwargs is argument from the line Keyw. arguments.
<br>Note: args is a Python list, while kwargs is a Python dictionary.''',
            False
            ),
            (WsStopPeriodicTasks,
            'WsStopAllPeriodicTasks',
            'Stop all periodic tasks',
            'Stops all periodic tasks.',
            (True, None)
            ),
            (WsStopPeriodicTasks,
            'WsStopAllNamedPeriodicTasks',
            'Stop periodic tasks with the given name',
            'Stops periodic tasks with the given name.',
            (True, 0)
            ),
            (WsStopPeriodicTasks,
            'WsStopBroadcastPeriodicTasks',
            'Stop all periodic tasks (broadcast type)',
            'Stops periodic tasks (broadcast type).',
            (False, None)
            ),
            (WsStopPeriodicTasks,
            'WsStopNamedBroadcastPeriodicTasks',
            'Stop all periodic tasks (broadcast type) with the given name',
            'Stops periodic tasks (broadcast type) with the given name.',
            (False, 1)
            ),
            (WsStopClientPeriodicTasks,
            'WsStopClientPeriodicTasks',
            'Stop periodic tasks (one client)',
            'Stops periodic tasks (one client).',
            None
            ),
            (eg.ActionGroup,
            'PeriodicActions',
            'Periodically repeated actions',
            'Periodically repeated actions', (
            (WsBroadcastMessage,
            'WsPeriodicallyBroadcastMessage',
            'Periodically broadcast message',
            '''Periodically broadcasts message to all WebSocket clients.
            
Same as Broadcast message action, but the broadcasting is automatically
 repeated periodically after a predetermined time.''',
            True
            ),
            (WsBroadcastValue,
            'WsPeriodicallyBroadcastValue',
            'Periodically broadcast values',
            '''Periodically broadcasts values to all WebSocket clients.
            
Same as Broadcast values action, but the broadcasting is automatically
 repeated periodically after a predetermined time.''',
            True
            ),
            (WsBroadcastAllValues,
            'WsPeriodicallyBroadcastAllValues',
            'Periodically broadcast all values',
            '''Periodically broadcasts all values to all WebSocket clients.
            
Same as Broadcast all values action, but the broadcasting is automatically
 repeated periodically after a predetermined time.''',
            True
            ),
            (WsBroadcastData,
            'WsPeriodicallyBroadcastData',
            'Periodically broadcast data',
            '''Periodically broadcasts data to all WebSocket clients.
            
Same as "Broadcast data" action, but the broadcasting is automatically repeated
 periodically after a predetermined time.''',
            True
            ),
            (WsBroadcastCommand,
            'WsPeriodicallyBroadcastCmd',
            'Periodically broadcast command',
            '''Periodically broadcasts command to all WebSocket clients.

Same as "Broadcast command" action, but the broadcasting is automatically
 repeated periodically after a predetermined time.''',
            True
            ),
            (WsBroadcastUniversal,
            'WsPeriodicallyBroadcastUniversal',
            'Periodically broadcast universal packet',
            '''Periodically broadcasts universal packet to all WebSocket clients.

Same as "Broadcast universal packet" action, but the broadcasting is
 automatically repeated periodically after a predetermined time.''',
            True
            ),
            (WsSendMessage,
            'WsPeriodicallySendMessage',
            'Periodically send message',
            '''Periodically sends message to one WebSocket client.
            
Same as Send message action, but the sending is automatically repeated
 periodically after a predetermined time.''',
            True
            ),
            (WsSendValue,
            'WsPeriodicallySendValue',
            'Periodically send values',
            '''Periodically sends values to one WebSocket client.
            
Same as Send values action, but the sending is automatically repeated
 periodically after a predetermined time.''',
            True
            ),
            (WsSendAllValues,
            'WsPeriodicallySendAllValues',
            'Periodically sends all values',
            '''Periodically sends the values of all variables
(temporary and persistent) to one WebSocket client.

Same as Send all values action, but the sending is automatically repeated
 periodically after a predetermined time.''',
            True
            ),

            (WsSendData,
            'WsPeriodicallySendData',
            'Periodically send data',
            '''Periodically sends data to one WebSocket client.
            
Same as Send data action, but the sending is automatically repeated
 periodically after a predetermined time.''',
            True
            ),
            (WsSendCommand,
            'WsPeriodicallySendCmd',
            'Periodically send command',
            '''Periodically sends command to one WebSocket client.

Same as "Send command" action, but the sending is automatically repeated
 periodically after a predetermined time.''',
            True
            ),
            (WsSendUniversal,
            'WsPeriodicallySendUniversal',
            'Periodically send universal packet',
            '''Periodically sends a universal packet to one WebSocket client.

Same as "Send universal packet" action, but the sending is automatically
 repeated periodically after a predetermined time.''',
            True
            ),

        )),
    )),
    ( eg.ActionGroup, 'ClientActions', 'Websocket actions client-server', 'Websocket actions client-server',(
        (StartClient, 'StartClient', 'Start client', 'Starts client.', None),
        (StopClient, 'StopClient', 'Stop client', 'Stops client.', None),
        (StopAllClients, 'StopAllClients', 'Stop all clients', 'Stops all clients.', None),
        (ClSendMessage,
            'ClSendMessage',
            'Send message to server',
            '''Sends a message to WebSocket server.
Message is sent as is (no JSON formatting).''',
            None
        ),
        (ClSendValue,
            'ClSendValue',
            'Send values to server',
            '''Sends a value(-s) of a variable(-s) (temporary or persistent)
to WebSocket server.

Specify name of a variable or list of variables (separated by commas,
 without parentheses).
<br>Following the evaluation, a message is formatted as a JSON object.
<br>A server receives a message in the following form:
<br>{'method': 'Values', 'kwargs': {key1: value1, key2: value2, ...}},
<br>where keyX is variable name and valueX is the value of this variable.''',
            None
        ),
        (ClSendAllValues,
            'ClSendAllValues',
            'Send all values to server',
            '''Sends the values of all variables (temporary and persistent)
 to WebSocket server.

A message is formatted as a JSON object.
A server receives a message in the following form:
{'method': 'Values', 'kwargs': {key1: value1, key2: value2, ...}},
where keyX is variable name and valueX is the value of this variable.''',
            None
        ),
        (ClSendData,
            'ClSendData',
            'Send data to server',
            '''Sends some data to WebSocket server.

Data can be obtained for example by evaluating Python expression.
Sending may be conditional upon the fulfillment (optional) conditions.
The condition may also be a Python expression.
A message is formatted as a JSON object.
A server receives a message in the following form:
{'method': 'Data', 'dataName': dataName, 'data': data}.''',
            False
        ),
        (ClSendCommand,
            'ClSendCmd',
            'Send command to server',
            '''Sends a command to WebSocket server.

This action allows you to specify more complex set of data into a single
 message.<br>Data sending may be conditional upon the fulfillment (optional)
 conditions. The condition can be a Python expression.
<br>A message is formatted as a JSON object.
<br>A server receives a message in the following form:
<br>{'method' :'Command', 'cmdName':cmdName, 'args':args, 'kwargs':kwargs},
<br>where args are the arguments of the lines Argument 1 to 3 and/or argument of
 line Arguments and kwargs is argument from the line Keyw. arguments.
<br>"args" is a Python list, while "kwargs" is a Python dictionary.''',
            False
        ),
        (ClSendUniversal,
            'ClSendUniversal',
            'Send universal packet to server',
            '''Sends a universal packet to WebSocket server.

This action allows you to specify a universal data packet.
<br>Data sending may be conditional upon the fulfillment (optional)
 conditions. The condition can be a Python expression.
<br>A message is formatted as a JSON object.
<br>A server receives a message in the following form:
<br>{'method' :method, 'args':args, 'kwargs':kwargs},
<br>where method is the selected method,
<br>args is argument from the line Arguments
<br>and kwargs is argument from the line Keyw. arguments.
<br>Note: args is a Python list, while kwargs is a Python dictionary.''',
            False
        ),
        )),
)
