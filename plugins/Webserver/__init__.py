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

import eg

eg.RegisterPlugin(
    name = "Webserver",
    author = "Bitmonster",
    version = "1.1",
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
from threading import Thread, Event
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ThreadingMixIn
from urllib import unquote, unquote_plus
from os.path import getmtime
import json
import jinja2
import cStringIO

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
            #print res
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

    #def handle_error(self, request, client_address):
    #    eg.PrintError("HTTP Error")



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
        self.send_response(200)
        self.send_header("Content-type", 'text/html')
        self.send_header("Content-Length", len(content))
        self.end_headers()
        self.wfile.write(content.encode("UTF-8"))


    def do_POST(self):
        """Serve a POST request."""
        # First do Basic HTTP-Authentication, if set
        #print "do post"
        #print self.headers
        contentLength = int(self.headers.get('content-length'))
        content = self.rfile.read(contentLength)
        #print content
        if not self.Authenticate():
            return

        try:
            data = json.loads(content)
        except:
            eg.PrintTraceback()
        print data
        methodName = data["method"]
        args = data.get("args", [])
        kwargs = data.get("kwargs", {})
        result = None
        if methodName == "TriggerEvent":
            self.plugin.TriggerEvent(*args, **kwargs)
        elif methodName == "TriggerEnduringEvent":
            self.plugin.TriggerEnduringEvent(*args, **kwargs)
            self.repeatTimer.Reset(2000)
        elif methodName == "RepeatEnduringEvent":
            self.repeatTimer.Reset(2000)
        elif methodName == "EndLastEvent":
            self.repeatTimer.Reset(None)
            self.plugin.EndLastEvent()
        content = json.dumps(result)
        self.send_response(200)
        self.send_header("Content-type", 'application/json; charset=UTF-8')
        self.send_header("Content-Length", len(content))
        self.end_headers()
        self.wfile.write(content.encode("UTF-8"))
        self.wfile.close()


    def do_GET(self):
        """Serve a GET request."""
        # First do Basic HTTP-Authentication, if set
        if not self.Authenticate():
            return

        path, dummy, remaining = self.path.partition("?")
        if remaining:
            queries = remaining.split("#", 1)[0].split("&")
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
        # suppress all messages
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



class SendEvent(eg.ActionBase):

    def __call__(self, event="", host="", port=80, user="", password=""):
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
                    "Target server returned status %s" % response.status
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
        panel = eg.ConfigPanel(self)
        eventCtrl = panel.TextCtrl(event)
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, min=1, max=65535)
        userCtrl = panel.TextCtrl(user)
        passwordCtrl = panel.TextCtrl(password)
        panel.sizer.AddMany([
            panel.StaticText("Event:"),
            eventCtrl,
            panel.StaticText("Host:"),
            hostCtrl,
            panel.StaticText("Port:"),
            portCtrl,
            panel.StaticText("Username:"),
            userCtrl,
            panel.StaticText("Password:"),
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



class Webserver(eg.PluginBase):

    class text:
        generalBox = "General Settings"
        port = "TCP/IP port:"
        documentRoot = "HTML documents root:"
        eventPrefix = "Event prefix:"
        authBox = "Basic Authentication"
        authRealm = "Realm:"
        authUsername = "Username:"
        authPassword = "Password:"


    def __init__(self):
        self.AddEvents()
        self.AddAction(SendEvent)
        self.running = False


    def __start__(
        self,
        prefix=None,
        port=80,
        basepath=None,
        authRealm="Eventghost",
        authUsername="",
        authPassword="",
    ):
        self.info.eventPrefix = prefix
        if authUsername or authPassword:
            authString = base64.b64encode(authUsername + ':' + authPassword)
        else:
            authString = None
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


    def Configure(
        self,
        prefix="HTTP",
        port=80,
        basepath="",
        authRealm="EventGhost",
        authUsername="",
        authPassword="",
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
        while panel.Affirmed():
            panel.SetResult(
                editCtrl.GetValue(),
                portCtrl.GetValue(),
                filepathCtrl.GetValue(),
                authRealmCtrl.GetValue(),
                authUsernameCtrl.GetValue(),
                authPasswordCtrl.GetValue(),
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

