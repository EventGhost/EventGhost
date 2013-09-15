# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
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
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 1.8 by Sem;colon 2013-09-15 12:47 UTC+1
#     - ExecuteScript method (Sem;colon part) can now handle list outputs
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
    author = "Bitmonster & Pako & Sem;colon",
    version = "1.8",
    guid = "{E4305D8E-A3D3-4672-B06E-4EA1F0F6C673}",
    description = (
        "Implements a small webserver, that you can use to generate events "
        "through HTML-pages."
    ),
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
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=1663",
)

import wx
import os
import sys
import posixpath
import base64
import time
import urllib2
import socket
import httplib
import json
import jinja2
import cStringIO
import re
from threading import Thread, Event
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ThreadingMixIn
from urllib import unquote, unquote_plus
from os.path import getmtime
from wx.lib.mixins.listctrl import TextEditMixin
SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)

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

class VariableDialog(wx.Frame):

    def __init__(self, parent, plugin, pers=False):
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
        varTable.FillData(self.plugin.pubPerVars)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        intSizer = wx.BoxSizer(wx.VERTICAL)
        intSizer.Add(varTable,1,wx.EXPAND|wx.BOTTOM, 5)
        sizer.Add(intSizer,1,wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT,10)
        if self.pers: # Persistent variable manager
            varTable.FillData(self.plugin.pubPerVars)
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
                pubPerVars = self.plugin.pubPerVars
                old = list(pubPerVars.iterkeys())
                new = list(data.iterkeys())
                deleted = list(set(old)-set(new))
                #renamed = list(set(new)-set(old))
                for key in deleted:
                    self.plugin.DelPersistentValue(key)
                for key, value in data.iteritems():
                    if key not in pubPerVars or value != pubPerVars[key]:
                        pubPerVars[key] = value
                        flag = True
                if flag or len(deleted):
                    wx.CallAfter(self.plugin.SetDocIsDirty)
                self.Close()
            btn1.Bind(wx.EVT_BUTTON,onOK)

            line = wx.StaticLine(
                panel,
                -1,
                size = (20,-1),
                style = wx.LI_HORIZONTAL
            )
            sizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
        else:  # Temporary variable viewer
            varTable.FillData(self.plugin.pubVars)

        btn2 = wx.Button(panel, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        if self.pers:
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

class FileLoader(jinja2.BaseLoader):
    """Loads templates from the file system."""

    def get_source(self, environment, filename):
        try:
            sourceFile = open(filename, "rb")
        except IOError:
            raise jinja2.TemplateNotFound(filename)
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

    def __init__(self, requestHandler, port):
        self.httpdThread = None
        self.abort = False
        for res in socket.getaddrinfo(None, port, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            self.address_family = res[0]
            self.socket_type = res[1]
            address = res[4]
            break

        HTTPServer.__init__(self, address, requestHandler)


    def server_bind(self):
        """Called by constructor to bind the socket."""
        if socket.has_ipv6 and sys.getwindowsversion()[0] > 5:
            # make it a dual-stack socket if OS is Vista/Win7
            IPPROTO_IPV6 = 41
            self.socket.setsockopt(IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        HTTPServer.server_bind(self)


    def Start(self):
        """Starts the HTTP server thread"""
        self.httpdThread = Thread(name="WebserverThread", target=self.Run)
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


class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    extensions_map = SimpleHTTPRequestHandler.extensions_map.copy()
    extensions_map['.ico'] = 'image/x-icon'
    extensions_map['.svg'] = 'image/svg+xml'
    extensions_map['.manifest'] = 'text/cache-manifest'
    # these class attributes will be set by the plugin
    authString = None
    authRealm = None
    basepath = None
    repeatTimer = None
    environment = None
    plugin = None


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
        self.send_header('WWW-Authenticate', 'Basic realm="%s"' % self.authRealm)
        return False


    def SendContent(self, path):
        fsPath = self.translate_path(path)
        if os.path.isdir(fsPath):
            if not path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", path + "/")
                self.end_headers()
                return None
            for index in ("index.html", "index.htm"):
                index = os.path.join(fsPath, index)
                if os.path.exists(index):
                    fsPath = index
                    break
            else:
                return self.list_directory(path)
        extension = posixpath.splitext(fsPath)[1].lower()
        if extension not in (".htm", ".html"):
            f = self.send_head()
            if f:
                self.wfile.write(f.read())
                f.close()
            return
        try:
            template = self.environment.get_template(fsPath)
        except jinja2.TemplateNotFound:
            self.send_error(404, "File not found")
            return
        content = template.render()
        self.end_request(content)


    def end_request(self, content, case = 'text/html'):
        self.send_response(200)
        self.send_header("Content-type", case)
        self.send_header("Content-Length", len(content))
        self.end_headers()
        self.wfile.write(content.encode("UTF-8"))
        self.wfile.close()

       
    def do_POST(self):
        """Serve a POST request."""
        # First do Basic HTTP-Authentication, if set
        if not self.Authenticate():
            return
        contentLength = int(self.headers.get('content-length'))
        content = self.rfile.read(contentLength)
        plugin = self.plugin
        try:
            data = json.loads(content)
        except:

# Enhancement by Sem;colon - START
            data=content.split("&")
            if data[0]=="request":
                self.SendContent(self.path)
                if len(data)>1:
                    plugin.TriggerEvent(data[1], data[2:])
            else:
                content = ""
                i=1
                if data[0]=="GetGlobalValue":
                    while i<len(data):
                        try:
                            content += self.environment.globals[data[i]]
                        except:
                            content += "None"
                        i+=1
                        if i<len(data):
                            content+=";;"
                elif data[0]=="ExecuteScript":
                    while i<len(data):
                        try:
                            output = eval(data[i])
                            if isinstance(output, str) or isinstance(output, unicode) or isinstance(output, int):
                                content += unicode(output)
                            elif isinstance(output, list):
                                content += u", ".join(output)
                            else:
                                content += "True"
                        except:
                            content += "False"
                        i+=1
                        if i<len(data):
                            content+=";;"
                elif data[0]=="GetValue":
                    while i<len(data):
                        try:
                            content += plugin.GetValue(data[i], self.client_address[0])
                        except:
                            content += "None"
                        i+=1
                        if i<len(data):
                            content+=";;"
                elif data[0]=="GetPersistentValue":
                    while i<len(data):
                        try:
                            content += plugin.GetPersistentValue(data[i], self.client_address[0])
                        except:
                            content += "None"
                        i+=1
                        if i<len(data):
                            content+=";;"
                elif data[0]=="SetValue":
                    try:
                        plugin.SetValue(data[1], data[2])
                        content = "True"
                    except:
                        content = "False"
                elif data[0]=="SetPersistentValue":
                    try:
                        plugin.SetPersistentValue(data[1], data[2])
                        content = "True"
                    except:
                        content = "False"
                elif data[0]=="GetAllValues":
                    try:
                        content = json.dumps(plugin.GetAllValues(self.client_address[0]))
                    except:
                        content = "False"
                elif data[0]=="GetChangedValues":
                    try:
                        content = json.dumps(plugin.GetChangedValues(self.client_address[0]))
                    except:
                        content = "False"
                elif data[0] == "TriggerEnduringEvent":
                    try:
                        plugin.TriggerEnduringEvent(data[1], data[2:])
                        self.repeatTimer.Reset(2000)
                        content = "True"
                    except:
                        content = "False"
                elif data[0] == "RepeatEnduringEvent":
                    try:
                        self.repeatTimer.Reset(2000)
                        content = "True"
                    except:
                        content = "False"
                elif data[0] == "EndLastEvent":
                    try:
                        self.repeatTimer.Reset(None)
                        plugin.EndLastEvent()
                        content = "True"
                    except:
                        content = "False"
                elif data[0]=="TriggerEvent":
                    if data[1][0:7]=="prefix=" and len(data)>2:
                        data[2]=data[2].replace("suffix=","")
                        if len(data)>3:
                          data[3]=data[3].replace("payload=","")
                        eg.TriggerEvent(prefix=data[1][7:], suffix=data[2], payload=data[3:])
                    else:
                        plugin.TriggerEvent(data[1], data[2:])
                else:
                    plugin.TriggerEvent(data[0], data[1:])
                self.end_request(content)
# Enhancement by Sem;colon - END

        else: # JSON request
            result = None
            methodName = data["method"]
            args = data.get("args", [])
            kwargs = data.get("kwargs", {})
            if methodName == "GetGlobalValue":   
                if len(args):
                    try:
                        result = self.environment.globals[args[0]]
                    except:
                        result = None
            if methodName == "GetValue":   
                if len(args):
                    try:
                        result = plugin.GetValue(args[0], self.client_address[0])
                    except:
                        result = None
            elif methodName == "GetPersistentValue":   
                if len(args):
                    try:
                        result = plugin.GetPersistentValue(args[0], self.client_address[0])
                    except:
                        result = None
            elif methodName == "SetValue":
                if len(args):
                    try:
                        plugin.SetValue(args[0], args[1])
                        result = True
                    except:
                        result = False     
            elif methodName == "SetPersistentValue":
                if len(args):
                    try:
                        plugin.SetPersistentValue(args[0], args[1])
                        result = True
                    except:
                        result = False     
            elif methodName == "GetAllValues":
                result = plugin.GetAllValues(self.client_address[0])
            elif methodName == "GetChangedValues":
                result = plugin.GetChangedValues(self.client_address[0])
            elif methodName == "ExecuteScript":
                try:
                    result = eval(args[0])
                except:
                    result = None
            elif methodName == "TriggerEvent":
                if 'prefix' in kwargs:
                    eg.TriggerEvent(*args, **kwargs)
                else:
                    plugin.TriggerEvent(*args, **kwargs)
            elif methodName == "TriggerEnduringEvent":
                plugin.TriggerEnduringEvent(*args, **kwargs)
                self.repeatTimer.Reset(2000)
            elif methodName == "RepeatEnduringEvent":
                self.repeatTimer.Reset(2000)
            elif methodName == "EndLastEvent":
                self.repeatTimer.Reset(None)
                plugin.EndLastEvent()
            content = json.dumps(result)
            self.end_request(content, 'application/json; charset=UTF-8')


    def do_GET(self):
        """Serve a GET request."""
        # First do Basic HTTP-Authentication, if set
        if not self.Authenticate():
            return

        path, dummy, remaining = self.path.partition("?")
        if remaining:
            queries = remaining.split("#", 1)[0].split("&")
            #print "queries =",queries
            queries = [unquote_plus(part).decode("latin1") for part in queries]
            if len(queries) > 0:
                event = queries.pop(0).strip()
                if "withoutRelease" in queries:
                    queries.remove("withoutRelease")
                    event = self.plugin.TriggerEnduringEvent(event, queries)
                    while not event.isEnded:
                        time.sleep(0.05)
                elif event == "ButtonReleased":
                    self.plugin.EndLastEvent()
                else:
                    event = self.plugin.TriggerEvent(event, queries)
                    while not event.isEnded:
                        time.sleep(0.05)
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
        path = posixpath.normpath(unquote(path))
        words = [word for word in path.split('/') if word]
        path = self.basepath
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path
     
       
class SetClientsFlags(eg.ActionBase):

    class text:
        varname = "Dummy variable name:"

    def __call__(self, varname = ""):
        key = eg.ParseString(varname)
        self.plugin.SetClientsFlags(key)
       

    def Configure(self, varname = ""):
        panel = eg.ConfigPanel(self)
        varnameCtrl = panel.TextCtrl(varname)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        varnameLbl = panel.StaticText(self.text.varname)
        mainSizer.Add(varnameLbl)
        mainSizer.Add(varnameCtrl, 0, wx.EXPAND|wx.TOP, 1)
        panel.sizer.Add(mainSizer, 0, wx.EXPAND|wx.ALL, 10)
        while panel.Affirmed():
            panel.SetResult(
                varnameCtrl.GetValue(),
            )       

   
class GetValue(eg.ActionBase):

    class text:
        varname = "Variable name:"
        err = 'Error in action "GetValue(%s)"'

    def __call__(self, varname = ""):
        try:
            key = eg.ParseString(varname)
            return self.plugin.GetValue(key)
        except:
            eg.PrintError(self.text.err % str(varname))
       
    def Configure(self, varname = ""):
        panel = eg.ConfigPanel(self)
        varnameCtrl = panel.TextCtrl(varname)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        varnameLbl = panel.StaticText(self.text.varname)
        mainSizer.Add(varnameLbl)
        mainSizer.Add(varnameCtrl, 0, wx.EXPAND|wx.TOP, 1)
        panel.sizer.Add(mainSizer, 0, wx.EXPAND|wx.ALL, 10)
       
        while panel.Affirmed():
            panel.SetResult(
                varnameCtrl.GetValue(),
            )       


class GetPersistentValue(eg.ActionBase):

    class text:
        varname = "Persistent variable name:"
        err = 'Error in action "GetPersistentValue(%s)"'

    def __call__(self, varname = ""):
        try:
            key = eg.ParseString(varname)
            return self.plugin.GetPersistentValue(key)
        except:
            eg.PrintError(self.text.err % str(varname))
       
    def Configure(self, varname = ""):
        panel = eg.ConfigPanel(self)
        varnameCtrl = panel.TextCtrl(varname)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        varnameLbl = panel.StaticText(self.text.varname)
        mainSizer.Add(varnameLbl)
        mainSizer.Add(varnameCtrl, 0, wx.EXPAND|wx.TOP, 1)
        panel.sizer.Add(mainSizer, 0, wx.EXPAND|wx.ALL, 10)
        while panel.Affirmed():
            panel.SetResult(
                varnameCtrl.GetValue(),
            )       


class SetValue(eg.ActionBase):

    class text:
        varname = "Variable name:"
        value = "Value:"
        err = 'Error in action "SetValue(%s, %s)"'

    def __call__(self, varname = "", value = "{eg.event.payload}"):
        try:
            key = eg.ParseString(varname)
            value = eg.ParseString(value)
            self.plugin.SetValue(key, value)
        except:
            eg.PrintError(self.text.err % (str(varname), str(value)))

    def GetLabel(self, varname, value):
        return "%s: %s: %s" % (self.name, varname, value)
       
    def Configure(self, varname = "", value = "{eg.event.payload}"):
        panel = eg.ConfigPanel(self)
        varnameCtrl = panel.TextCtrl(varname)
        valueCtrl = panel.TextCtrl(value)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        varnameLbl = panel.StaticText(self.text.varname)
        valueLbl = panel.StaticText(self.text.value)
        mainSizer.Add(varnameLbl)
        mainSizer.Add(varnameCtrl, 0, wx.EXPAND|wx.TOP, 1)
        mainSizer.Add(valueLbl, 0, wx.EXPAND|wx.TOP, 20)
        mainSizer.Add(valueCtrl, 0, wx.EXPAND|wx.TOP, 1)
        panel.sizer.Add(mainSizer, 0, wx.EXPAND|wx.ALL, 10)
        while panel.Affirmed():
            panel.SetResult(
                varnameCtrl.GetValue(),
                valueCtrl.GetValue(),
            )       


class SetPersistentValue(eg.ActionBase):

    class text:
        varname = "Persistent variable name:"
        value = "Value:"
        err = 'Error in action "SetValue(%s, %s)"'

    def __call__(self, varname = "", value = "{eg.event.payload}"):
        try:
            key = eg.ParseString(varname)
            value = eg.ParseString(value)
            self.plugin.SetPersistentValue(key, value)
        except:
            eg.PrintError(self.text.err % (str(varname), str(value)))

    def GetLabel(self, varname, value):
        return "%s: %s: %s" % (self.name, varname, value)
       
    def Configure(self, varname = "", value = "{eg.event.payload}"):
        panel = eg.ConfigPanel(self)
        varnameCtrl = panel.TextCtrl(varname)
        valueCtrl = panel.TextCtrl(value)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        varnameLbl = panel.StaticText(self.text.varname)
        valueLbl = panel.StaticText(self.text.value)
        mainSizer.Add(varnameLbl)
        mainSizer.Add(varnameCtrl, 0, wx.EXPAND|wx.TOP, 1)
        mainSizer.Add(valueLbl, 0, wx.EXPAND|wx.TOP, 20)
        mainSizer.Add(valueCtrl, 0, wx.EXPAND|wx.TOP, 1)
        panel.sizer.Add(mainSizer, 0, wx.EXPAND|wx.ALL, 10)
        while panel.Affirmed():
            panel.SetResult(
                varnameCtrl.GetValue(),
                valueCtrl.GetValue(),
            )       


class SendEvent(eg.ActionBase):

    class text:
        event = "Event:"
        host = "Host:"
        port ="Port:"
        username = "Username:"
        passsword = "Password:"
        errmsg = "Target server returned status %s"       

    def __call__(self, event="", host="", port=80, user="", password=""):
        text = self.text
        def Request(methodName, *args, **kwargs):
            data = {"method": methodName}
            if len(args):
                data["args"] = args
            if len(kwargs):
                data["kwargs"] = kwargs
            content = json.dumps(data)
            authString = base64.encodestring(user + ':' + password).strip()
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

            response = httplib.HTTPResponse(sock)
            response.begin()
            content = response.read()
            response.close()
            sock.close()
            if response.status != 200:
                raise Exception(
                    text.errmsg % response.status
                )
            return json.loads(content)

        event = eg.ParseString(event)
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


    def Configure(self, event="", host="", port=80, user="", password=""):
        text = self.text
        panel = eg.ConfigPanel(self)
        eventCtrl = panel.TextCtrl(event)
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, min=1, max=65535)
        userCtrl = panel.TextCtrl(user)
        passwordCtrl = panel.TextCtrl(password)
        panel.sizer.AddMany([
            panel.StaticText(text.event),
            eventCtrl,
            panel.StaticText(text.host),
            hostCtrl,
            panel.StaticText(text.port),
            portCtrl,
            panel.StaticText(text.username),
            userCtrl,
            panel.StaticText(text.password),
            passwordCtrl,
        ])
        while panel.Affirmed():
            panel.SetResult(
                eventCtrl.GetValue(),
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                userCtrl.GetValue(),
                passwordCtrl.GetValue(),
            )


# Enhancement by Sem;colon - START
class SendEventExt(eg.ActionBase):

    class text:
        url = "Url: (like you would put it into a webbrowser)"
        event = "Event:"
        username = "Username:"
        passsword = "Password:"
        msg1 = "This page isn't protected by authentication."
        msg2 = 'But we failed for another reason.'
        msg3 = 'A 401 error without an authentication response header - very weird.'
        msg4 = 'The authentication line is badly formed.'
        msg5 = 'This example only works with BASIC authentication.'
        msg6 = "url, username or password is wrong."

    def __call__(self, event="", host="", user="", password=""):
        text = self.text
        req = urllib2.Request(host,event)
        try:
            handle = urllib2.urlopen(req)
        except IOError, e:
            # If we fail then the page could be protected
            if not hasattr(e, 'code') or e.code != 401:                 
                # we got an error - but not a 401 error
                print text.msg1
                print text.msg2
           
            authline = e.headers.get('www-authenticate', '')               
            # this gets the www-authenticat line from the headers - which has the authentication scheme and realm in it
            if not authline:
                print text.msg3
               
            authobj = re.compile(r'''(?:\s*www-authenticate\s*:)?\s*(\w*)\s+realm=['"](\w+)['"]''', re.IGNORECASE)         
            # this regular expression is used to extract scheme and realm
            matchobj = authobj.match(authline)
            if not matchobj:                                       
                # if the authline isn't matched by the regular expression then something is wrong
                print text.msg4
            scheme = matchobj.group(1)
            realm = matchobj.group(2)
            if scheme.lower() != 'basic':
                print text.msg5
           
            base64string = base64.encodestring('%s:%s' % (user, password))[:-1]
            authheader =  "Basic %s" % base64string
            req.add_header("Authorization", authheader)
            try:
                handle = urllib2.urlopen(req)
            except IOError, e:
                print text.msg6
        #else:
            # If we don't fail then the page isn't protected
            #print "This page isn't protected by authentication."
        thepage = urllib2.unquote(handle.read()).decode(eg.systemEncoding,'replace') # handle.read()
        return thepage


    def Configure(self, event="", host="http://127.0.0.1:80", user="", password=""):
        text = self.text
        panel = eg.ConfigPanel(self)
        eventCtrl = panel.TextCtrl(event)
        hostCtrl = panel.TextCtrl(host)
        userCtrl = panel.TextCtrl(user)
        passwordCtrl = panel.TextCtrl(password)
        panel.sizer.AddMany([
            panel.StaticText(text.event),
            eventCtrl,
            panel.StaticText(text.url),
            hostCtrl,
            panel.StaticText(text.username),
            userCtrl,
            panel.StaticText(text.password),
            passwordCtrl,
        ])
        while panel.Affirmed():
            panel.SetResult(
                eventCtrl.GetValue(),
                hostCtrl.GetValue(),
                userCtrl.GetValue(),
                passwordCtrl.GetValue(),
            )
# Enhancement by Sem;colon - END


class Webserver(eg.PluginBase):

    knowlClients = {}
    pubPerClients = {}
    pubVars = {}
    pubPerVars = {}

    class text:
        generalBox = "General Settings"
        port = "TCP/IP port:"
        documentRoot = "HTML documents root:"
        eventPrefix = "Event prefix:"
        authBox = "Basic Authentication"
        authRealm = "Realm:"
        authUsername = "Username:"
        authPassword = "Password:"
        dialogPers = "Persistent variable manager"
        dialogTemp = "Temporary variable viewer"
        ok = "OK"
        cancel = "Cancel"
        vrbl = "Variable name"
        defVal = "Variable value"
        delete = "Delete selected variables"
        clear = "Clear all variables"
        autosave = "Automatically save the document when the value of a persistent variable is changed"

    def __init__(self):
        self.AddEvents()
        self.AddActionsFromList(ACTIONS)
        self.running = False

    def __start__(
        self,
        prefix=None,
        port=80,
        basepath=None,
        authRealm="Eventghost",
        authUsername="",
        authPassword="",
        pubPerVars = {},
        autosave = False
    ):
        self.info.eventPrefix = prefix
        if authUsername or authPassword:
            authString = base64.b64encode(authUsername + ':' + authPassword)
        else:
            authString = None
        self.knowlClients = {}
        self.pubPerClients = {}
        self.pubVars = {}
        self.pubPerVars = pubPerVars
        self.autosave = autosave
        for key in self.pubPerVars.iterkeys():
            self.pubPerClients[key] = []
        eg.PrintNotice("Persistent values: " + repr(self.pubPerVars))
        class RequestHandler(MyHTTPRequestHandler):
            plugin = self
            environment = jinja2.Environment(loader=FileLoader())
            environment.globals = eg.globals.__dict__
            repeatTimer = eg.ResettableTimer(self.EndLastEvent)
        RequestHandler.basepath = basepath
        RequestHandler.authRealm = authRealm
        RequestHandler.authString = authString
        self.server = MyServer(RequestHandler, port)
        self.server.Start()


    def __stop__(self):
        self.server.Stop()


    def GetValue(self, key, client = None):
        if key in self.pubVars:
            if client:
                tmp = self.knowlClients[key]
                if not client in tmp:
                    tmp.append(client)
                return self.pubVars[key]
            else:
                return self.pubVars[key]


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
        return tmpDict


    def GetAllValues(self, client):
        tmpDict = {}
        for key, value in self.pubVars.iteritems():
            if not client in self.knowlClients[key]:
                self.knowlClients[key].append(client)
            tmpDict[key] = value
        for key, value in self.pubPerVars.iteritems():
            if not client in self.pubPerClients[key]:
                self.pubPerClients[key].append(client)
            tmpDict[key] = value
        return tmpDict


    def SetDocIsDirty(self):     
        eg.document.SetIsDirty()
        if self.autosave:
            eg.document.Save()
       

    def Configure(
        self,
        prefix="HTTP",
        port = 80,
        basepath="",
        authRealm="EventGhost",
        authUsername="",
        authPassword="",
        pubPerVars = {},
        autosave = False
    ):
        text = self.text
        panel = eg.ConfigPanel()
        portCtrl = panel.SpinIntCtrl(port, min=1, max=65535)
        filepathCtrl = panel.DirBrowseButton(basepath)
        editCtrl = panel.TextCtrl(prefix)
        authRealmCtrl = panel.TextCtrl(authRealm)
        authUsernameCtrl = panel.TextCtrl(authUsername)
        authPasswordCtrl = panel.TextCtrl(authPassword)

        labels = (
            panel.StaticText(text.port),
            panel.StaticText(text.documentRoot),
            panel.StaticText(text.eventPrefix),
            panel.StaticText(text.authRealm),
            panel.StaticText(text.authUsername),
            panel.StaticText(text.authPassword),
        )
        eg.EqualizeWidths(labels)

        acv = wx.ALIGN_CENTER_VERTICAL
        sizer = wx.FlexGridSizer(3, 2, 5, 5)
        sizer.Add(labels[0], 0, acv)
        sizer.Add(portCtrl)
        sizer.Add(labels[1], 0, acv)
        sizer.Add(filepathCtrl)
        sizer.Add(labels[2], 0, acv)
        sizer.Add(editCtrl)
        staticBox = wx.StaticBox(panel, label=text.generalBox)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        sizer = wx.FlexGridSizer(3, 2, 5, 5)
        sizer.Add(labels[3], 0, acv)
        sizer.Add(authRealmCtrl)
        sizer.Add(labels[4], 0, acv)
        sizer.Add(authUsernameCtrl)
        sizer.Add(labels[5], 0, acv)
        sizer.Add(authPasswordCtrl)
        staticBox = wx.StaticBox(panel, label=text.authBox)
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
        dialogButton = wx.Button(panel,-1,self.text.dialogPers + " ...")
        dialogButton2 = wx.Button(panel,-1,self.text.dialogTemp + " ...")
        dialogSizer = wx.BoxSizer(wx.HORIZONTAL)
        dialogSizer.Add(dialogButton)
        dialogSizer.Add(dialogButton2,0,wx.LEFT,15)
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



        while panel.Affirmed():
            panel.SetResult(
                editCtrl.GetValue(),
                portCtrl.GetValue(),
                filepathCtrl.GetValue(),
                authRealmCtrl.GetValue(),
                authUsernameCtrl.GetValue(),
                authPasswordCtrl.GetValue(),
                self.pubPerVars,
                aSaveCtrl.GetValue()
            )


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

ACTIONS = (
    (
        SendEvent,
        "SendEvent",
        "Send event to another EventGhost",
        "Sends event to another EventGhost webserver.",
        None
    ),
    (
        SendEventExt,
        "SendEventExt",
        "Send event to another webserver",
        "Sends event to another webserver.",
       None
    ),
    (
        GetValue,
        "GetValue",
        "Get temporary value",
        "Gets value of temporary variable.",
        None
    ),
    (
        GetPersistentValue,
        "GetPersistentValue",
        "Get persistent value",
        "Gets value of persistent variable.",
        None
    ),
    (
        SetValue,
        "SetValue",
        "Set temporary value",
        "Sets value of temporary variable.",
        None
    ),
    (
        SetPersistentValue,
        "SetPersistentValue",
        "Set persistent value",
        "Sets value of persistent variable.",
        None
    ),
    (
        SetClientsFlags,
        "SetClientsFlags",
        "Set clients flags",
        "Sets clients flags of dummy variable.",
        None
    ),
)
