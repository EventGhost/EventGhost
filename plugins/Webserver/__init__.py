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
    version = "1.0",
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
import posixpath
import threading
import httplib
import base64
import time
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ThreadingMixIn
from urllib import unquote, unquote_plus
import json
import jinja2


class FileLoader(jinja2.BaseLoader):
    """Loads templates from the file system."""

    def get_source(self, environment, filename):
        try:
            f = open(filename, "rb")
        except IOError:
            raise jinja2.TemplateNotFound(filename)
        try:
            contents = f.read().decode("utf-8")
        finally:
            f.close()

        mtime = os.path.getmtime(filename)
        def uptodate():
            try:
                return os.path.getmtime(filename) == mtime
            except OSError:
                return False
        return contents, filename, uptodate



class MyServer(ThreadingMixIn, HTTPServer):

    def __init__(self, address, handler, basepath, authRealm, authString):
        HTTPServer.__init__(self, address, handler)
        self.basepath = basepath
        self.authRealm = authRealm
        self.authString = authString
        self.env = jinja2.Environment(loader=FileLoader())
        self.env.globals = eg.globals.__dict__

    #def handle_error(self, request, client_address):
    #    eg.PrintError("HTTP Error")



class MyHTTPRequestHandler(SimpleHTTPRequestHandler):

    def Authenticate(self):
        # only authenticate, if set
        if self.server.authString is None:
            return True

        # do Basic HTTP-Authentication
        authHeader = self.headers.get('authorization')
        if authHeader is not None:
            (authType, authData) = authHeader.split(' ', 2)
            if authType.lower() == 'basic':
                if base64.decodestring(authData) == self.server.authString:
                    return True

        self.send_response(401)
        self.send_header(
            'WWW-Authenticate', 
            'Basic realm="%s"' % self.server.authRealm
        )
        self.end_headers()
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
            for index in "index.html", "index.htm":
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
            template = self.server.env.get_template(fsPath)
        except jinja2.TemplateNotFound:
            self.send_error(404, "File not found")
            return
        content = template.render()
        self.send_response(200)
        self.send_header("Content-type", 'text/html')
        self.send_header("Content-Length", len(content))
        #self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        self.wfile.write(content)


    def do_POST(self):
        """Serve a POST request."""
        # First do Basic HTTP-Authentication, if set
        if not self.Authenticate():
            return
        #print self.headers
        contentLength = int(self.headers.get('content-length'))
        data = self.rfile.read(contentLength)
        print data
        try:
            data = json.loads(data)
        except:
            eg.PrintTraceback()
            
        action = data[0]
        result = None
        if action == "TriggerEvent":
            event = data[1][0]
            self.TriggerEvent(event)
        elif action == "TriggerEnduringEvent":
            event = data[1][0]
            self.TriggerEnduringEvent(event)
            self.currentTimer.Reset(2000)
        elif action == "RepeatEnduringEvent":
            self.currentTimer.Reset(2000)
        elif action == "EndLastEvent":
            self.currentTimer.Reset(None)
            self.EndLastEvent()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(result))
        

    def do_GET(self):
        """Serve a GET request."""
        # First do Basic HTTP-Authentication, if set
        if not self.Authenticate():
            return

        # Main Handler
        infile = None
        try:
            pathParts = self.path.split('?', 1)
            self.path = pathParts[0]

            infile = self.send_head()
            if not infile:
                return
            self.copyfile(infile, self.wfile)
            infile.close()
            infile = None

            if len(pathParts) < 2:
                return
            queryParts = [
                unquote_plus(part).decode("latin1")
                    for part in pathParts[1].split('&')
            ]
            event = queryParts[0]
            withoutRelease = False
            payload = None
            if len(queryParts) > 1:
                startPos = 1
                if queryParts[1] == "withoutRelease":
                    withoutRelease = True
                    startPos = 2
                if len(queryParts) > startPos:
                    payload = queryParts[startPos:]
            if event.strip() == "ButtonReleased":
                self.EndLastEvent()
            elif withoutRelease:
                self.TriggerEnduringEvent(event, payload)
            else:
                self.TriggerEvent(event, payload)
        except Exception, exc:
            self.EndLastEvent()
            eg.PrintError("Webserver socket error", self.path)
            eg.PrintError(Exception, exc)
            if infile is not None:
                infile.close()
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
        path = posixpath.normpath(unquote(path))
        words = [word for word in path.split('/') if word]
        path = self.server.basepath
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path

    extensions_map = SimpleHTTPRequestHandler.extensions_map.copy()
    extensions_map['.ico'] = 'image/x-icon'
    extensions_map['.manifest'] = 'text/cache-manifest'

import urllib2

class SendEvent(eg.ActionBase):
    
    def __call__(self, host, event, user, password):
        # Create an OpenerDirector with support for Basic HTTP Authentication...
        auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password(realm='EventGhost',
                                  uri="http://" + host + "/",
                                  user=user,
                                  passwd=password)
        opener = urllib2.build_opener(auth_handler)
        # ...and install it globally so it can be used with urlopen.
        urllib2.install_opener(opener)
        data = '["TriggerEnduringEvent",["%s"]]' % event
        urllib2.urlopen("http://" + host + "/", data, 2)
        def EndLastEvent():
            urllib2.urlopen("http://" + host + "/", '["EndLastEvent"]', 2)
        eg.event.AddUpFunc(EndLastEvent)        
    
    
    def Configure(self, host="", event="", user="", password=""):
        panel = eg.ConfigPanel(self)
        hostCtrl = panel.TextCtrl(host)
        eventCtrl = panel.TextCtrl(event)
        userCtrl = panel.TextCtrl(user)
        passwordCtrl = panel.TextCtrl(password)
        panel.sizer.AddMany([
            panel.StaticText("Host:"),
            hostCtrl,
            panel.StaticText("Event:"),
            eventCtrl,
            panel.StaticText("Username:"),
            userCtrl,
            panel.StaticText("Password:"),
            passwordCtrl,
        ])
        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                eventCtrl.GetValue(),
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
        authPassword=""
    ):
        self.info.eventPrefix = prefix
        self.port = port
        self.basepath = basepath
        self.authRealm = authRealm
        self.authUsername = authUsername
        self.authPassword = authPassword
        self.abort = False
        self.httpdThread = threading.Thread(
            name="WebserverThread",
            target=self.ThreadLoop
        )
        self.httpdThread.start()
        self.running = True


    def __stop__(self):
        if self.running:
            self.abort = True
            conn = httplib.HTTPConnection("127.0.0.1:%d" % self.port)
            conn.request("QUIT", "/")
            conn.getresponse()
            self.httpdThread = None
            self.running = False


    def OnTimeout(self):
        print "OnTimeout"
        self.EndLastEvent()
        
        
    def ThreadLoop(self):
        class MySubHandler(MyHTTPRequestHandler):
            TriggerEvent = self.TriggerEvent
            TriggerEnduringEvent = self.TriggerEnduringEvent
            EndLastEvent = self.EndLastEvent
            currentTimer = eg.ResettableTimer(self.OnTimeout)
            
        if self.authUsername or self.authPassword:
            authString = self.authUsername + ':' + self.authPassword
        else:
            authString = None
        server = MyServer(
            ('', self.port),
            MySubHandler,
            self.basepath,
            self.authRealm,
            authString
        )
        # Handle one request at a time until stopped
        while not self.abort:
            server.handle_request()


    def Configure(
        self,
        prefix="HTTP",
        port=80,
        basepath="",
        authRealm="EventGhost",
        authUsername="",
        authPassword=""
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

        while panel.Affirmed():
            panel.SetResult(
                editCtrl.GetValue(),
                portCtrl.GetValue(),
                filepathCtrl.GetValue(),
                authRealmCtrl.GetValue(),
                authUsernameCtrl.GetValue(),
                authPasswordCtrl.GetValue()
            )

