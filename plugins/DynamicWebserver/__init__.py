# -*- coding: utf-8 -*-
# plugins/DynamicWebserver/__init__.py
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

eg.RegisterPlugin(
    name = "Dynamic Webserver",
    author = (
        "Bitmonster",
        "Kingtd",
    ),
    version = "1.0.503",
    guid = "{2FC713FF-0093-4271-A520-F0F6BB05A0E8}",
    description = u'''<rst>Implements a small webserver,
that you can use to generate events through HTML-pages.

========================
This plugin is obsolete!
========================
Use the Webserver plugin instead.
---------------------------------''',
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=1610",
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


import BaseHTTPServer
import SimpleHTTPServer
import os
import posixpath
import urllib
import threading
import httplib
import mimetypes
import base64
import re



class MyServer(BaseHTTPServer.HTTPServer):
    pass
    #def handle_error(self, request, client_address):
    #    eg.PrintError("HTTP Error")



class MyHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):


    def webvars(self, match ):
        try:
            value=getattr(eg.globals,match.group()[13:-2])
            return value
        except:
            return ""

    def do_GET(self):
        """Serve a GET request."""

        # First do Basic HTTP-Authentication, if set
        if self.server.authString != None:
            authenticated = False
            authHeader = self.headers.get('authorization')
            if authHeader is not None:
                (authType, authData) = authHeader.split(' ', 2)
                if authType.lower() == 'basic':
                    if base64.decodestring(authData) == self.server.authString:
                        authenticated= True
            if not authenticated:
                self.send_response(401)
                self.send_header(
                    'WWW-Authenticate',
                    'Basic realm="%s"' % self.server.authRealm
                )
                self.end_headers()
                return

        # Main Handler
        f = None
        try:
            p = self.path.split('?', 1)
            self.path = p[0]
            f = self.send_head()
            if not f:
                return
            tempwpage=f.read()
            tempwpage=re.sub('{{eg.globals..*?}}', self.webvars, tempwpage)
            self.wfile.write(tempwpage)
            # self.copyfile(f, self.wfile)
            f.close()
            f = None
            if len(p) < 2:
                return
            a = p[1].split('&')
            event = urllib.unquote_plus(a[0]).decode("latin1")
            withoutRelease = False
            payload = None
            if len(a) > 1:
                startPos = 1
                if a[1] == "withoutRelease":
                    withoutRelease = True
                    startPos = 2
                if len(a) > startPos:
                    payload = []
                    for i in range(startPos, len(a)):
                        payload.append(
                            urllib.unquote_plus(a[i]).decode("latin1")
                        )
            if event.strip() == "ButtonReleased":
                self.EndLastEvent()
            elif withoutRelease:
                self.TriggerEnduringEvent(event, payload)
            else:
                self.TriggerEvent(event, payload)
        except Exception, ex:
            eg.PrintError("Webserver socket error", self.path)
            eg.PrintError(Exception, ex)
            if f is not None:
                f.close()
            if ex.args[0] == 10053: # Software caused connection abort
                pass
            elif ex.args[0] == 10054: # Connection reset by peer
                pass
            else:
                raise

    def log_message(self, format, *args):
        # suppress all messages
        pass


    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        if ctype.startswith('text/'):
            mode = 'r'
        else:
            mode = 'rb'
        try:
            f = open(path, mode)
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        self.end_headers()
        return f




    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # stolen from SimpleHTTPServer.SimpleHTTPRequestHandler
        # but changed to handle files from a defined basepath instead
        # of os.getcwd()
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = self.server.basepath
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path

    extensions_map = mimetypes.types_map.copy()
    extensions_map.update(
        {
            '': 'application/octet-stream', # Default
            '.py': 'text/plain',
            '.c': 'text/plain',
            '.h': 'text/plain',
            '.ico': 'image/x-icon',
        }
    )



class DynamicWebserver(eg.PluginClass):
    canMultiLoad = True

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
        self.httpd_thread = threading.Thread(target=self.ThreadLoop)
        self.httpd_thread.start()
        self.running = True


    def __stop__(self):
        if self.running:
            self.abort = True
            conn = httplib.HTTPConnection("localhost:%d" % self.port)
            conn.request("QUIT", "/")
            conn.getresponse()
            self.httpd_thread = None
            self.running = False


    def ThreadLoop(self):
        class mySubHandler(MyHTTPRequestHandler):
            TriggerEvent = self.TriggerEvent
            TriggerEnduringEvent = self.TriggerEnduringEvent
            EndLastEvent = self.EndLastEvent

        server = MyServer(('', self.port), mySubHandler)
        server.basepath = self.basepath

        server.authRealm = self.authRealm
        if self.authUsername != '' or self.authPassword != '':
            server.authString = self.authUsername + ':' + self.authPassword
        else:
            server.authString = None

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
        panel = eg.ConfigPanel(self)

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

        ACV = wx.ALIGN_CENTER_VERTICAL
        sizer = wx.FlexGridSizer(3, 2, 5, 5)
        sizer.Add(labels[0], 0, ACV)
        sizer.Add(portCtrl)
        sizer.Add(labels[1], 0, ACV)
        sizer.Add(filepathCtrl)
        sizer.Add(labels[2], 0, ACV)
        sizer.Add(editCtrl)
        staticBox = wx.StaticBox(panel, label=text.generalBox)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
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
