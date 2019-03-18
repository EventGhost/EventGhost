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
# 0.6 by Pako 2015-03-02 19:19 UTC+1
#     - message can now include the word "Ping"
# 0.5 by krambriw 2015-02-20
#     - introduced retries in BroadcastMessage function
#     - added, where missing, a short sleep in all while loops to free CPU
#     - added support for handling an incoming 'Ping' event responding with a
#      'Pong' response 
# 0.4 by Pako 2014-07-25 08:39 UTC+1
#     - first version for release r1669 and later (no need to install libraries)
#     - Common handler: get method fixed
#     - mimetype >>> '.json': 'application/json' <<< added
# 0.3 by Pako 2014-04-19 12:35 UTC+1
#     - "Default document:" optional parameter added
# 0.2 by Pako 2014-03-29 08:12 UTC+1
#     - added support of webp image format
# 0.1 by Pako 2014-02-12 18:43 UTC+1
#     - added option to work with a secure protocol (https://)
# 0.0 by Pako 2014-01-13 13:35 UTC+1
#     - initial version
# ===============================================================================

version = "0.6"

eg.RegisterPlugin(
    name="Tornado",
    author="Pako",
    version=version,
    guid="{377321D5-CE2D-4A66-97D6-48EC23467318}",
    description='''Webserver with support for WebSocket protocol.

<br>A significant part of the code is taken from the <b>Webserver plugin</b>. 
<br><b>Tornado plugin</b> has (almost) all of the features of that
 plugin and is backward compatible with it.
<br><br> 
This means, that implements a small webserver, that you can use to generate 
events through HTML-pages, including the ability to create interactive 
web-based GUI to control different programs.
<br><br>
Tornado plugin also has an extra (compared <b>Webserver plugin</b>) 
built-in support of <b>WebSocket protocol</b>, so you can use 
the "push technology" (introduced by the new HTML5 standard).
<br><br>
In all Python expressions (used in a action of the group "WebSocket action") 
in this plugin, you can use the following convention:
<br>The values of temporary variables are available as an attribute 
of object "tv", <br>while the values of persistent variables are available 
as an attribute of an object "pv".
<font color=#FF0000><br><b>Example:</b> we have a temporary variable, whose name
 is <b><i>artist</i></b>.
<br>Then we can get its value as <b><i>tv.artist</i></b></font>.
<br><br>
<b>Tornado plugin</b> is based on the
 <a href = "http://www.tornadoweb.org/en/stable/">Tornado library.</a>''',
    createMacrosOnAdd=True,
    canMultiLoad=True,
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAABsAAAAgCAYAAADjaQM7AAAHjUlEQVRIx6WXS4wcRxmA"
        "v6qu7p6emZ2dndmXs3H8jOMHSYwJTqQoSg7BJOIQiSMgIeCUKIpAiEOEEBckDiCuHDgG"
        "CRGBeCRCXAgRQcoLKSIPLMfx2+vd7OyuZ3pm+l31c5j1xiax5ISSfnVXddX/Vf9/1f9X"
        "KT5lEZEAmAXuAu4BDgIe8ArwvFIqv9lY8ykgHeA4cKJy7v60qu4al7aVOespUPO12lci"
        "3+TA858ZJiJN4IRz7mvjyj60keWzvaxQg6JUmbVYEbRSHOuqhSXffE5EfqeUcp8KJiIK"
        "eMA5961RVT2xkmRzK0mm4rJEBCLj0Ql9ap6HrzWRZxSwF4iA8S3DRCQEvl5a+/TyOL33"
        "4jjVm3mBUYr5WshMGBBoRVJZ4qJiUJQg6IZv7g6NNw+cuyVYr9ebKq19JrXumfPD8fyl"
        "cYIVYTEK6YQBCtjMC5LKEmpNy/e5vREx5fvWN96bwOYt+WxdpNWoqu8PivK7Z+JR60qa"
        "0zQeS/UIoxW9NCe3lpkwoFsPsE6I84pQaxbrtfcc/FZDJSL6k/ymrjOdPy7L7w2L8ofn"
        "RklrNc3phj5zYcC4tPTzkplawJTvkRSWD5Oc0joavmGpWWOpVR8rpf6tRJbR+l0l8urI"
        "mNfmlBp+DBZn2VczK784MxztWkky5moh3TCgl+Q4ERbrNbLKcmWUIcBsLaBuPConjAtL"
        "ah0aaPoe0zW/6tSDjWZgXgR+1QiC17dhK2m6O1Tqlxfj5Mtnh2M15RuW6jVWxzlGK2Zr"
        "Ab2kYDMtmG+E1DyPOK/YSAqUgrrvEWhN6YQ4KxnllnbNZ2+n7na36//QuB+16vV/GhHR"
        "G3n+RD8rHrk8SpVysFAL2UxLrBPmo4BLcUphHTtbEVnpON0fMy4tnZrh0NwU3XqIpxUi"
        "wqioOLeZcKo3ZiMpdGndw/vnmk8OBoOTenU0mq2sfXxllIXDvGI2CtDAZlIwFwWsjnLy"
        "yrFQD9lMSt7fGBPnFZUVeuOSi/0MhyAAStEMfQ7NT7GrHTHOLafWxipOqy+VQXBMK7g3"
        "Kdx9G0mhDIpuLWA9Kan7Hs7B+rhgoTEBnb+aUlSCtRMprbASZySFxYlsi9aKTj3AKM0g"
        "qRikxQyOu7RV6gvDopge5pa68Qg8TZyVNANDPysJPA3A5TincoJ1gnVMnlbwlALkBpgV"
        "YZRVNH0PoxVZ5VQltmWsk8OjvPKKylH3PTyl6EQBU4EhziqshVFmyUuHE0GELREA5psB"
        "vtHYrboCBmnJcj+jEXiMcotWiCg1NBbaaemUdYKvNVorlto1tFK0csPl/sRM1gnOTSAi"
        "E6W7Zmrs6kQIYEVQQFJY3lkeEhhFFGicCKHvja3IOV1Z0ZWdKAJwE0/jBGabITvbEZUV"
        "ZAukULRqhkOLTY4sTVELvBvMlxSWKPDYN1dnfVTSjnwiX58Va08ZEcmVUlJWotItR2/v"
        "eAW7uxHdhk+cllQOar5mOvKpBx5asdV/OzbQqhsORk3OrI5Ziwu+uGfaGV+9lK6uXjQW"
        "+SAwyokT72pSUliH0eqj8QqmIsNUzWzXFWrLdNeaPpqgAKv9jPeWR4RGMzcdfGjhjwcO"
        "HMi1UvrVRuCNQ0+zPixZHxVYJiaxwkcCuC0zW5Ftcde9WxGWNzPeOj9kkFaUlVBU4kSp"
        "PoCWynsjCrzXu81ARrnlbC8hTiuccMNyvplcg+Sl49SVMa9/0EcQds7UJn2cmDKzNQB9"
        "aK5xRRn1m4V2cLXb8Fm+mvOf5RG9OKey7gbFpRPitGJtMIkq19rXhwWvnu7z1vmYTtPn"
        "87tbBL5GKwWK2Ekx2M5ngbW/bwbm8J656OmiktrFjYzNYUm36dOqGwKjqZzQH5esxyXj"
        "3HJ09xS756NJxkgrispx9x1N7piLSHLL8mbOQjsQYzhZ+H5vG3ZgdjZ+e3X15+2G0QeX"
        "6t+Jenp65WrOmbV02/FuK3L4nmKuFWztocm3HZ2QuelgMikrvHdxRGUdO2fDkUK/cHRm"
        "pn9Dpr5ncfHDVy5c+MlUvXHh4O3Nb9zWCQ4PxjbaGJb60nqG1oo9cxOlvlEkhWOUVdRD"
        "DxQYo3AIg6TkytWc/TsimW0FfxWb/fljyfNa+bGIfqzX2+eJekCE40Ulj51dSfafW0tx"
        "DoynKCvBeIqje5oszIRopdAakszyr9Mxg6TiwcPtUbdpnjo2P/trpZR8Iuy6I5b6+8t4"
        "jYPrj5fC0+uD4uHTV5Lw8npOp2lYaE9i4iitmGn67F+qc2kt4833Y47dOWX3LUbPaVv8"
        "4L6lpfWb/tknlTdW+3tLKb85TKonz1xJZlc2cxWnFmuF+XbA3oWIHd2AN07FOIEHj7RP"
        "GiXffmjn4mvX69G3Aju+2D5bZKOfNures0d21//2wKHp/p23RWI8RXfKpzvt8/a5MRtx"
        "yd4dNRsE6sVhGr9109PVLZ731ctrawvKcqIq5al3z42On15OVBR6iAiHdzXcvh21F6jk"
        "2Uf23HbyM18sJoFZCbCKyHMvLa80F7vB0bV+EU43jOxaDLP5TvinCvuzR/csnfy/bjH/"
        "Q5XywvIHnWn/6v1Hpqso0O/4hr9Ya/7w6B2Lyzcb9l8ezHt24/qirQAAAABJRU5ErkJg"
        "gg=="
    ),
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=5972",
)

import base64
import json
import logging
import mimetypes
import os
import posixpath
import socket
import time
import urllib2
from copy import deepcopy as cpy
from httplib import HTTPResponse
from os.path import getmtime, isfile, join, split, splitdrive
from re import compile, IGNORECASE
from threading import Event, Thread
from urllib import unquote, unquote_plus

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import wx
from jinja2 import BaseLoader, Environment, TemplateNotFound
from tornado import httputil
from tornado.escape import _unicode
from tornado.util import basestring_type
from wx.lib.mixins.listctrl import TextEditMixin

import eg

SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)


# ===============================================================================

def clear(self):
    """Resets all headers and content for this response."""
    self._headers = httputil.HTTPHeaders({
        "Server": "TornadoServer/%s/EventGhost/%s/TornadoPlugin/%s" %
                  (tornado.version, eg.Version.string, version),
        "Content-Type": "text/html; charset=UTF-8",
        "Date": httputil.format_timestamp(time.time()),
    })
    self.set_default_headers()
    if (not self.request.supports_http_1_1() and
        getattr(self.request, 'connection', None) and
        not self.request.connection.no_keep_alive):
        conn_header = self.request.headers.get("Connection")
        if conn_header and (conn_header.lower() == "keep-alive"):
            self.set_header("Connection", "Keep-Alive")
    self._write_buffer = []
    self._status_code = 200
    self._reason = httputil.responses[200]


tornado.web.RequestHandler.clear = clear


# ===============================================================================

class LogFormatter(logging.Formatter):
    def __init__(self, limit, *args, **kwargs):
        logging.Formatter.__init__(self, *args, **kwargs)
        self.limit = limit

    def format(self, record):
        try:
            record.message = record.getMessage()
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)
        assert isinstance(record.message, basestring_type)  # guaranteed by logging
        record.asctime = time.strftime(
            "%Y-%m-%d %H:%M:%S", self.converter(record.created))
        prefix = '[%(asctime)s %(levelname)1.1s %(module)s:%(lineno)d]' % \
                 record.__dict__

        def safe_unicode(s):
            try:
                return _unicode(s)
            except UnicodeDecodeError:
                return repr(s)

        limit = self.limit
        formatted = prefix + " " + safe_unicode(record.message)
        if limit:
            formatted = formatted[:limit]
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            lines = [formatted.rstrip()]
            lines.extend(safe_unicode(ln) for ln in record.exc_text.split('\n'))
            # Traceback without limit !!!
            # lines = [line[:limit] for line in lines] if limit else lines
            formatted = '\n'.join(lines)
        return formatted.replace("\n", "\n    ")


# ===============================================================================

class NullHandler(logging.Handler):

    def handle(self, record):
        pass

    def emit(self, record):
        pass

    def createLock(self):
        self.lock = None


# ===============================================================================

class KeysAsAttrs:
    def __init__(self, pairSet):
        self._pairSet = pairSet

    def __getattr__(self, key):
        try:
            return self._pairSet[key]
        except KeyError, err:
            raise AttributeError(key)


# ===============================================================================

class VarTable(wx.ListCtrl, TextEditMixin):

    def __init__(self, parent, txt, edit):
        wx.ListCtrl.__init__(
            self,
            parent,
            -1,
            style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.LC_EDIT_LABELS,
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
        self.InsertItem(0, "dummy")
        rect = self.GetItemRect(0, wx.LIST_RECT_BOUNDS)
        hh = rect[1]  # header height
        hi = rect[3]  # item height
        self.DeleteAllItems()
        self.w0 = self.GetColumnWidth(0)
        self.w1 = self.GetColumnWidth(1)
        self.wk = SYS_VSCROLL_X + self.GetWindowBorderSize()[0] + self.w0 + self.w1
        width = self.wk
        rows = 10
        self.SetMinSize((max(width, 200), 2 + hh + rows * hi))
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Show(True)

    def SetWidth(self):
        w = (self.GetSize().width - self.wk)
        w0_ = w / 2 + self.w0
        w1_ = w / 2 + self.w1
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
            self.InsertItem(i, key)
            self.SetItem(i, 1, value)
            i += 1
        self.Enable(i > 0)

    def OpenEditor(self, col, row):  # Hack of default method
        if self.edit:
            self.edCell = (row, col, self.GetItem(row, col).GetText())  # Remember pos and value!!!
            TextEditMixin.OpenEditor(self, col, row)

    def CloseEditor(self, event=None):  # Hack of default method
        TextEditMixin.CloseEditor(self, event)
        if not event:
            self.SetItem(*self.edCell)  # WORKAROUND !!!
        elif isinstance(event, wx.CommandEvent):
            row, col, oldVal = self.edCell
            newVal = self.GetItem(row, col).GetText()
            evt = eg.ValueChangedEvent(self.GetId(), value=(row, col, newVal))
            wx.PostEvent(self, evt)

    def DeleteSelectedItems(self):
        item = self.GetFirstSelected()
        selits = []
        while item != -1:
            selits.append(item)
            item = self.GetNextSelected(item)
            time.sleep(0.05)
        selits.reverse()
        for item in selits:
            self.DeleteItem(item)

    def GetData(self):
        data = {}
        for row in range(self.GetItemCount()):
            data[self.GetItemText(row)] = self.GetItem(row, 1).GetText()
        return data


# ===============================================================================

class VariableDialog(wx.Frame):

    def __init__(self, parent, plugin, pers=False):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL | wx.RESIZE_BORDER,
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
        intSizer.Add(varTable, 1, wx.EXPAND | wx.BOTTOM, 5)
        sizer.Add(intSizer, 1, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 10)
        if self.pers:  # Persistent variable manager
            varTable.FillData(self.plugin.pubPerVars)
            btn3 = wx.Button(panel, -1, self.text.delete)
            btn3.Enable(False)
            btn4 = wx.Button(panel, -1, self.text.clear)
            delSizer = wx.BoxSizer(wx.HORIZONTAL)
            delSizer.Add(btn3)
            delSizer.Add(btn4, 0, wx.LEFT, 10)
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
                btn3.Enable(selCnt > 0)
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
                deleted = list(set(old) - set(new))
                # renamed = list(set(new)-set(old))
                for key in deleted:
                    self.plugin.DelPersistentValue(key)
                for key, value in data.iteritems():
                    if key not in pubPerVars or value != pubPerVars[key]:
                        pubPerVars[key] = value
                        flag = True
                if flag or len(deleted):
                    wx.CallAfter(self.plugin.SetDocIsDirty)
                self.Close()

            btn1.Bind(wx.EVT_BUTTON, onOK)

            line = wx.StaticLine(
                panel,
                -1,
                size=(20, -1),
                style=wx.LI_HORIZONTAL
            )
            sizer.Add(line, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 5)
        else:  # Temporary variable viewer
            varTable.FillData(self.plugin.pubVars)

        btn2 = wx.Button(panel, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        if self.pers:
            btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.EXPAND | wx.RIGHT, 10)
        sizer.Add((1, 6))
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

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler


# ===============================================================================

def Authenticate(handler):
    # only authenticate, if set
    if handler.plugin.authString is None:
        return True
    # do Basic HTTP-Authentication
    authHeader = handler.request.headers.get('authorization')
    if authHeader is not None:
        authType, authString = authHeader.split(' ', 2)
        if authType.lower() == 'basic' \
            and authString == handler.plugin.authString:
            return True
    handler.set_status(401)
    handler.set_header(
        'WWW-Authenticate',
        'Basic realm="%s"' % handler.plugin.authRealm
    )
    handler.finish()
    return False


def translate_path(handler, path):
    """Translate a /-separated PATH to the local filename syntax.

    Components that mean special things to the local file system
    (e.g. drive or directory names) are ignored.  (XXX They should
    probably be diagnosed.)

    """
    path = path.split('?', 1)[0]
    path = path.split('#', 1)[0]
    path = posixpath.normpath(unquote(path))
    words = [word for word in path.split('/') if word]
    path = handler.settings["template_path"]
    for word in words:
        drive, word = splitdrive(word)
        head, word = split(word)
        if word in (os.curdir, os.pardir):
            continue
        path = join(path, word)
    return path


def SendContent(handler, path):
    fsPath = translate_path(handler, path)
    try:
        template = handler.environment.get_template(fsPath)
    except TemplateNotFound:
        handler.send_error(404, "File not found")
        return
    kwargs = cpy(handler.plugin.pubVars)
    kwargs.update(handler.plugin.pubPerVars)
    content = template.render(**kwargs)
    handler.write(content)


def ClientChoice(evt, text, panel, id3, id4, cl_ip, cl_port, size2, rBMC):
    middleSizer = panel.sizer.GetItem(0).GetSizer()
    dynamicSizer = middleSizer.GetItem(2).GetSizer()
    dynamicSizer.Clear(True)
    middleSizer.Detach(dynamicSizer)
    dynamicSizer.Destroy()
    dynamicSizer = wx.GridBagSizer(2, 10)
    dynamicSizer.SetMinSize(size2)
    middleSizer.Add(dynamicSizer, 1, wx.EXPAND)
    mode = rBMC.GetSelection()
    portCtrl = None
    if mode == 1:
        if evt:
            evt.Skip()
        return
    txtLabel = wx.StaticText(panel, -1, text.host)
    txtCtrl = wx.TextCtrl(panel, id3, cl_ip)
    dynamicSizer.Add(txtLabel, (0, 0), (1, 1))
    dynamicSizer.Add(txtCtrl, (1, 0), (1, 1), flag=wx.EXPAND)
    portLabel = wx.StaticText(panel, -1, text.port)
    portCtrl = wx.TextCtrl(panel, id4, cl_port)
    dynamicSizer.Add(portLabel, (2, 0), (1, 1), flag=wx.TOP, border=10)
    dynamicSizer.Add(portCtrl, (3, 0), (1, 1))
    panel.sizer.Layout()
    if evt:
        evt.Skip()


# ===============================================================================

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


# ===============================================================================

class RootHandler(tornado.web.RequestHandler):
    def initialize(self, plugin):
        self.plugin = plugin
        self.logger = plugin.logger

    def post(self):  # Another EventGhost "Send event" receiver !!!
        # First do Basic HTTP-Authentication, if set
        if not Authenticate(self):
            return
        content = self.request.body
        try:
            data = json.loads(content)
        except:
            self.application.logger.error("non json error:", exc_info=True)
        else:  # JSON request
            methodName = data["method"]
            args = data.get("args", [])
            kwargs = data.get("kwargs", {})
            result = self.plugin.ProcessTheArguments(
                self,
                methodName,
                args,
                kwargs
            )
            content = json.dumps(result)
            content = content.encode("UTF-8")
            self.write(content)
            self.set_header("Content-Type", 'application/json; charset=UTF-8')

    def get(self):  # "It works ..." handler
        # First do Basic HTTP-Authentication, if set
        if not Authenticate(self):
            return

        if self.plugin.defDoc == "":
            content = '''<html lang="en-US">
<head>
<meta http-equiv="refresh" content="1">
<title>It works!</title>
</head>
<body>
<h1>It works !</h1>
<span style="font-size: x-large">TornadoServer/%s<br>
EventGhost/%s<br>
TornadoPlugin/%s<br>
Server time: %s</span>
</body>
</html>''' % (
                tornado.version,
                eg.Version.string,
                version,
                httputil.format_timestamp(time.time())
            )
        else:
            content = '''<html lang="en-US">
<head>
<meta HTTP-EQUIV="REFRESH" content="0; url=http://%s/%s">
</head>
</html>''' % (self.request.host, self.plugin.defDoc)
        try:
            self.write(content)
            self.finish()
        except:
            self.application.logger.error(
                "write(content) error:",
                exc_info=True
            )


# ===============================================================================

class CommonHandler(tornado.web.StaticFileHandler):
    def initialize(self, path, plugin):
        self.plugin = plugin
        self.logger = plugin.logger
        self.environment = Environment(loader=FileLoader())
        self.environment.globals = eg.globals.__dict__
        self.client_address = self.request.connection.address
        tornado.web.StaticFileHandler.initialize(self, path)

    def log_exception(self, typ, value, tb):
        if isinstance(value, tornado.web.HTTPError):
            if value.log_message:
                format = "%d %s: " + value.log_message
                args = ([value.status_code, self._request_summary()] +
                        list(value.args))
                self.logger.warning(format, *args)
        else:
            self.logger.error(
                "Uncaught exception %s\n%r",
                self._request_summary(),
                self.request,
                exc_info=(typ, value, tb)
            )

    def set_extra_headers(self, path):
        # Disable caching ...
        self.set_header(
            'Cache-Control',
            'no-store, no-cache, must-revalidate, max-age=0'
        )

    def get_content_type(self):
        """Returns the ``Content-Type`` header to be used for this request.
        """
        ext = posixpath.splitext(self.absolute_path)[1].lower()
        if ext in self.plugin.extensions_map:
            return self.plugin.extensions_map[ext]
        else:
            return self.plugin.extensions_map['']

    def end_request(self, content, case='text/html; charset=UTF-8'):
        content = content.encode("UTF-8")
        self.write(content)
        self.set_header("Content-Type", case)

    def get(self, path, include_body=True):
        # First do Basic HTTP-Authentication, if set
        if not Authenticate(self):
            return

        _, _, remaining = self.request.uri.partition("?")
        if remaining:
            queries = remaining.split("#", 1)[0].split("&")
            queries = [unquote_plus(part).decode("latin1") for part in queries]
            if len(queries) > 0:
                event = queries.pop(0).strip()
                if "withoutRelease" in queries:
                    queries.remove("withoutRelease")
                    event = self.plugin.TriggerEnduringEvent(event, queries)
                    while not event.isEnded:
                        time.sleep(0.1)
                elif event == "ButtonReleased":
                    self.plugin.EndLastEvent()
                else:
                    event = self.plugin.TriggerEvent(event, queries)
                    while not event.isEnded:
                        time.sleep(0.1)

        if path.endswith('/'):
            path = path[:-1]

        # self.absolute_path = os.path.join(root, path)
        p = self.parse_url_path(path)
        absolute_path = self.get_absolute_path(self.root, p)
        self.absolute_path = self.validate_absolute_path(
            self.root, absolute_path)
        extension = posixpath.splitext(path)[1].lower()
        if extension in (".htm", ".html"):
            try:
                SendContent(self, path)
            except:
                self.application.logger.error(
                    "SendContent error:",
                    exc_info=True
                )
        else:
            tornado.web.StaticFileHandler.get(self, path, include_body)

    #    def post(self, *args, **kwargs):
    def post(self, path):
        # First do Basic HTTP-Authentication, if set
        if not Authenticate(self):
            return

        content = self.request.body
        plugin = self.plugin
        try:
            data = json.loads(content)
        except:
            # Enhancement by Sem;colon - START
            data = content.split("&")
            if data[0] == "request":
                SendContent(self, path)
                if len(data) > 1:
                    plugin.TriggerEvent(data[1], data[2:])
            else:
                content = ""
                i = 1
                if data[0] == "GetGlobalValue":
                    while i < len(data):
                        try:
                            content += unicode(
                                self.environment.globals[data[i]]
                            )
                        except:
                            content += "None"
                        i += 1
                        if i < len(data):
                            content += self.plugin.valueSplitter
                        time.sleep(0.05)
                elif data[0] == "ExecuteScript":
                    while i < len(data):
                        try:
                            output = eval(data[i])
                            if isinstance(output, str) \
                                or isinstance(output, unicode) \
                                or isinstance(output, int) \
                                or isinstance(output, float) \
                                or isinstance(output, long):
                                content += unicode(output)
                            elif isinstance(output, list):
                                content += self.plugin.listSplitter.join(
                                    unicode(x) for x in output
                                )
                            else:
                                content += "True"
                        except:
                            content += "False"
                        i += 1
                        if i < len(data):
                            content += self.plugin.valueSplitter
                        time.sleep(0.05)
                elif data[0] == "GetValue":
                    while i < len(data):
                        try:
                            content += plugin.GetValue(
                                data[i],
                                self.client_address[0]
                            )
                        except:
                            content += "None"
                        i += 1
                        if i < len(data):
                            content += self.plugin.valueSplitter
                        time.sleep(0.05)
                elif data[0] == "GetPersistentValue":
                    while i < len(data):
                        try:
                            content += plugin.GetPersistentValue(
                                data[i],
                                self.client_address[0]
                            )
                        except:
                            content += "None"
                        i += 1
                        if i < len(data):
                            content += self.plugin.valueSplitter
                        time.sleep(0.05)
                elif data[0] == "SetValue":
                    try:
                        plugin.SetValue(data[1], data[2])
                        content = "True"
                    except:
                        content = "False"
                elif data[0] == "SetPersistentValue":
                    try:
                        plugin.SetPersistentValue(data[1], data[2])
                        content = "True"
                    except:
                        content = "False"
                elif data[0] == "GetAllValues":
                    try:
                        content = json.dumps(
                            plugin.GetAllValues(self.client_address[0])
                        )
                    except:
                        content = "False"
                elif data[0] == "GetChangedValues":
                    try:
                        content = json.dumps(
                            plugin.GetChangedValues(self.client_address[0])
                        )
                    except:
                        content = "False"
                elif data[0] == "TriggerEnduringEvent":
                    try:
                        plugin.TriggerEnduringEvent(data[1], data[2:])
                        self.application.repeatTimer.Reset(2000)
                        content = "True"
                    except:
                        content = "False"
                elif data[0] == "RepeatEnduringEvent":
                    try:
                        self.application.repeatTimer.Reset(2000)
                        content = "True"
                    except:
                        content = "False"
                elif data[0] == "EndLastEvent":
                    try:
                        self.application.repeatTimer.Reset(None)
                        plugin.EndLastEvent()
                        content = "True"
                    except:
                        content = "False"
                elif data[0] == "TriggerEvent":
                    if data[1][0:7] == "prefix=" and len(data) > 2:
                        data[2] = data[2].replace("suffix=", "")
                        if len(data) > 3:
                            data[3] = data[3].replace("payload=", "")
                        eg.TriggerEvent(
                            prefix=data[1][7:],
                            suffix=data[2],
                            payload=data[3:]
                        )
                    else:
                        plugin.TriggerEvent(data[1], data[2:])
                else:
                    plugin.TriggerEvent(data[0], data[1:])
                self.end_request(content)
        # Enhancement by Sem;colon - END

        else:  # JSON request
            methodName = data["method"]
            args = data.get("args", [])
            kwargs = data.get("kwargs", {})
            result = plugin.ProcessTheArguments(self, methodName, args, kwargs)
            content = json.dumps(result)
            self.end_request(content, 'application/json; charset=UTF-8')


# ===============================================================================

class wsHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, plugin):
        self.plugin = plugin
        self.client_address = self.request.connection.address

    def write_message(self, message, binary=False):
        if isinstance(message, dict):
            message = tornado.escape.json_encode(message)
        self.ws_connection.write_message(message, binary=binary)
        self.application.logger.info(
            "WS_MESSAGE --> %s: %s",
            repr(self.client_address),
            message
        )

    def open(self):
        self.plugin.TriggerEvent(
            self.plugin.text.wsClientConn,
            payload=[self.client_address]
        )
        self.plugin.wsClients[self.client_address] = self
        self.application.logger.info(
            "WebSocket  *** %s: %s",
            repr(self.client_address),
            self.plugin.text.cli_con
        )

    def on_message(self, message):
        try:
            data = json.loads(message)
        except:
            # if message.find('WebSocket Protocol Error') > -1:
            #    eg.PrintNotice('message: '+message)
            #    self.on_close()
            # elif message.find('Masked frame from server') > -1:
            #    eg.PrintNotice('message: '+message)
            #    self.on_close()
            # else:
            self.plugin.TriggerEvent(message, payload=[self.client_address])
            return
        if not isinstance(data, dict) or "method" not in data.iterkeys():
            self.plugin.TriggerEvent(
                "ClientMessage",
                payload=(self.client_address, data)
            )

        else:  # JSON request
            methodName = data["method"]
            ### krambriw
            if methodName == "Ping":
                id = data["id"] if "id" in data else -1
                content = json.dumps({
                    "method": "Pong",
                    "id": id,
                    "client_address": self.client_address
                })
                self.write_message(content)
                return
            ###
            try:
                args = data.get("args", [])
                kwargs = data.get("kwargs", {})
                self.plugin.ProcessTheArguments(self, methodName, args, kwargs)
            except:
                self.application.logger.error(
                    "on_message error:",
                    exc_info=True
                )
            #    result = self.plugin.ProcessTheArguments(self, methodName, args, kwargs)
        #    content = json.dumps(result)
        #    self.write_message(content) # Need further processed, according to methodName ???

        self.application.logger.info(
            "WS_MESSAGE <-- %s: %s",
            repr(self.client_address),
            message
        )

    def on_close(self):
        self.plugin.TriggerEvent(
            self.plugin.text.wsClientDisconn,
            payload=[self.client_address]
        )
        if self.client_address in self.plugin.wsClients:
            del self.plugin.wsClients[self.client_address]
        self.application.logger.info(
            "WebSocket  *** %s: %s",
            repr(self.client_address),
            self.plugin.text.cli_discon
        )


# ===============================================================================

class ServerThread(Thread):
    def __init__(self, plugin, port, wsFolder, ssl_options):
        Thread.__init__(self)
        self.plugin = plugin
        self.port = port
        self.wsFolder = wsFolder
        self.ssl_options = ssl_options

    def run(self):
        http_server = TornadoApplication(
            self.plugin,
            self.port,
            self.wsFolder,
            self.ssl_options
        )
        http_server.Start()

    # ===============================================================================


class TornadoApplication(tornado.web.Application):

    def __init__(self, plugin, port, wsFolder, ssl_options):
        self.ssl_options = ssl_options
        self.logger = plugin.logger
        self.port = port
        self.plugin = plugin
        self.repeatTimer = eg.ResettableTimer(self.plugin.EndLastEvent)
        root = plugin.basepath
        handlers = [
            (r'/', RootHandler, {"plugin": plugin}),
            (r'/%s' % wsFolder, wsHandler, {"plugin": plugin}),
            (r"/(.*)", CommonHandler, {"path": root, "plugin": plugin}),
        ]
        settings = dict(
            template_path=root,
            static_path=root,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        plugin.server = self

    def Start(self):
        self.http_server = tornado.httpserver.HTTPServer(
            self,
            ssl_options=self.ssl_options)
        self.http_server.listen(self.port)
        # self.http_server.bind(self.port)
        # self.http_server.start(0)
        self.instance = tornado.ioloop.IOLoop.instance()
        sr = int(self.ssl_options is None)
        print self.plugin.text.started % (self.plugin.text.secur[sr], self.port)
        self.instance.start()  # loop started ...

    def Stop(self):
        self.repeatTimer.Stop()
        if self.instance:
            self.instance.stop()
        if self.http_server:
            self.http_server.stop()
        print self.plugin.text.stopped % self.port

    def log_request(self, handler):
        request_time = 1000.0 * handler.request.request_time()
        if handler.get_status() < 400:
            log_method = self.logger.info
        elif handler.get_status() < 500:
            log_method = self.logger.warning
        else:
            log_method = self.logger.error
            log_method("%d %s %.2fms", handler.get_status(),
                       handler._request_summary(), request_time, exc_info=True)
            return
        log_method("%d %s %.2fms", handler.get_status(),
                   handler._request_summary(), request_time)


# ===============================================================================

class SetClientsFlags(eg.ActionBase):
    class text:
        varname = "Dummy variable name:"
        err = 'Error in action "Set clients flags(%s)"'

    def __call__(self, varname="", pars=False):
        try:
            key = eg.ParseString(varname) if not pars else varname
            self.plugin.SetClientsFlags(key)
        except:
            eg.PrintError(self.text.err % str(varname))

    def Configure(self, varname="", pars=False):
        panel = eg.ConfigPanel(self)
        varnameCtrl = panel.TextCtrl(varname)
        parsCtrl = wx.CheckBox(panel, -1, self.plugin.text.parsing)
        parsCtrl.SetValue(pars)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        varnameLbl = panel.StaticText(self.text.varname)
        mainSizer.Add(varnameLbl)
        mainSizer.Add(varnameCtrl, 0, wx.EXPAND | wx.TOP, 1)
        mainSizer.Add(parsCtrl, 0, wx.TOP, 4)
        panel.sizer.Add(mainSizer, 0, wx.EXPAND | wx.ALL, 10)
        while panel.Affirmed():
            panel.SetResult(
                varnameCtrl.GetValue(),
                parsCtrl.GetValue()
            )
        # ===============================================================================


class GetValue(eg.ActionBase):
    class text:
        varname = "Variable name:"
        err = 'Error in action "Get temporary value(%s)"'

    def __call__(self, varname="", pars=False):
        try:
            key = eg.ParseString(varname) if not pars else varname
            return self.plugin.GetValue(key)
        except:
            eg.PrintError(self.text.err % str(varname))

    def Configure(self, varname="", pars=False):
        panel = eg.ConfigPanel(self)
        varnameCtrl = panel.TextCtrl(varname)
        parsCtrl = wx.CheckBox(panel, -1, self.plugin.text.parsing)
        parsCtrl.SetValue(pars)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        varnameLbl = panel.StaticText(self.text.varname)
        mainSizer.Add(varnameLbl)
        mainSizer.Add(varnameCtrl, 0, wx.EXPAND | wx.TOP, 1)
        mainSizer.Add(parsCtrl, 0, wx.TOP, 4)
        panel.sizer.Add(mainSizer, 0, wx.EXPAND | wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(
                varnameCtrl.GetValue(),
                parsCtrl.GetValue()
            )
        # ===============================================================================


class GetPersistentValue(GetValue):
    class text:
        varname = "Persistent variable name:"
        err = 'Error in action "Get persistent value(%s)"'

    def __call__(self, varname="", pars=False):
        try:
            key = eg.ParseString(varname) if not pars else varname
            return self.plugin.GetPersistentValue(key)
        except:
            eg.PrintError(self.text.err % str(varname))
        # ===============================================================================


class SetValue(eg.ActionBase):
    class text:
        varname = "Variable name:"
        value = "Value:"
        err = 'Error in action "Set temporary value(%s, %s)"'

    def __call__(
        self,
        varname="",
        value="{eg.event.payload}",
        pars1=False,
        pars2=False
    ):
        try:
            key = eg.ParseString(varname) if not pars1 else varname
            val = eg.ParseString(value) if not pars2 else value
            self.plugin.SetValue(key, val)
        except:
            eg.PrintError(self.text.err % (str(varname), str(value)))

    def GetLabel(self, varname, value, pars1, pars2):
        return "%s: %s: %s" % (self.name, varname, value)

    def Configure(
        self,
        varname="",
        value="{eg.event.payload}",
        pars1=False,
        pars2=False
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
        mainSizer.Add(varnameLbl)
        mainSizer.Add(varnameCtrl, 0, wx.EXPAND | wx.TOP, 1)
        mainSizer.Add(pars1Ctrl, 0, wx.EXPAND | wx.TOP, 4)
        mainSizer.Add(valueLbl, 0, wx.EXPAND | wx.TOP, 20)
        mainSizer.Add(valueCtrl, 0, wx.EXPAND | wx.TOP, 1)
        mainSizer.Add(pars2Ctrl, 0, wx.EXPAND | wx.TOP, 4)
        panel.sizer.Add(mainSizer, 0, wx.EXPAND | wx.ALL, 10)
        while panel.Affirmed():
            panel.SetResult(
                varnameCtrl.GetValue(),
                valueCtrl.GetValue(),
                pars1Ctrl.GetValue(),
                pars2Ctrl.GetValue(),
            )
        # ===============================================================================


class SetPersistentValue(SetValue):
    class text:
        varname = "Persistent variable name:"
        value = "Value:"
        err = 'Error in action "Set persistent value(%s, %s)"'

    def __call__(
        self,
        varname="",
        value="{eg.event.payload}",
        pars1=False,
        pars2=False
    ):
        try:
            key = eg.ParseString(varname) if not pars1 else varname
            val = eg.ParseString(value) if not pars2 else value
            self.plugin.SetPersistentValue(key, val)
        except:
            eg.PrintError(self.text.err % (str(varname), str(value)))
        # ===============================================================================


class WsSendMessage(eg.ActionBase):
    class text:
        mess = "Message to be sent:"

    def __call__(
        self,
        message="",
        cl_ip="127.0.0.1",
        cl_port="1234",
        modeClient=1,
        pars=False
    ):
        if not pars:
            message = self.plugin.EvalString(message)
        return self.plugin.ServerSendMessage(
            message,
            cl_ip,
            cl_port,
            modeClient
        )

    def GetLabel(self, message, cl_ip, cl_port, modeClient, pars):
        if modeClient:
            client = "{eg.event.payload[0]}"
            return "%s: %s: %s" % (self.name, client, message)
        else:
            return "%s: %s:%s: %s" % (self.name, cl_ip, cl_port, message)

    def Configure(
        self,
        message="",
        cl_ip="127.0.0.1",
        cl_port="1234",
        modeClient=1,
        pars=False
    ):
        text = self.text
        panel = eg.ConfigPanel()
        id2 = wx.NewIdRef()
        id3 = wx.NewIdRef()
        id4 = wx.NewIdRef()
        radioBoxModeClient = wx.RadioBox(
            panel,
            -1,
            self.plugin.text.modeClientChoiceLabel,
            choices=self.plugin.text.modeClientChoice,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxModeClient.SetSelection(modeClient)
        staticBox = wx.StaticBox(panel, -1, "")
        tmpSizer = wx.GridBagSizer(2, 10)
        txtLabel = wx.StaticText(panel, -1, self.plugin.text.host)
        txtCtrl = wx.TextCtrl(panel, id3, "")
        portLabel = wx.StaticText(panel, -1, self.plugin.text.port)
        portCtrl = wx.TextCtrl(panel, id2, "")
        tmpSizer.Add(txtLabel, (0, 0), (1, 1))
        tmpSizer.Add(txtCtrl, (1, 0), (1, 1), flag=wx.EXPAND)
        tmpSizer.Add(portLabel, (2, 0), (1, 1), flag=wx.TOP, border=10)
        tmpSizer.Add(portCtrl, (3, 0), (1, 1))
        middleSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        middleSizer.Add(radioBoxModeClient, 0, wx.LEFT | wx.EXPAND)
        middleSizer.Add((20, -1), 0, wx.LEFT | wx.EXPAND)
        middleSizer.Add(tmpSizer, 0, wx.LEFT | wx.EXPAND)
        panel.sizer.Add(middleSizer, 0, wx.TOP | wx.EXPAND, 8)
        panel.sizer.Layout()
        size2 = (-1, tmpSizer.GetMinSize()[1])

        def OnClientChoice(evt=None):
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

        messCtrl = wx.TextCtrl(panel, -1, message)
        messSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.mess),
            wx.VERTICAL
        )
        parsCtrl = wx.CheckBox(panel, -1, self.plugin.text.parsing)
        parsCtrl.SetValue(pars)
        panel.sizer.Add(messSizer, 0, wx.EXPAND | wx.TOP, 8)
        messSizer.Add(messCtrl, 0, wx.EXPAND)
        messSizer.Add(parsCtrl, 0, wx.EXPAND | wx.TOP, 3)

        while panel.Affirmed():
            modeClient = radioBoxModeClient.GetSelection()
            if not modeClient:
                cl_ip = wx.FindWindowById(id3).GetValue()
                cl_port = wx.FindWindowById(id4).GetValue()
            panel.SetResult(
                messCtrl.GetValue(),
                cl_ip,
                cl_port,
                modeClient,
                parsCtrl.GetValue()
            )


# ===============================================================================

class WsBroadcastMessage(eg.ActionBase):
    class text:
        mess = "Message for broadcast:"

    def __call__(self, message="", pars=False):
        if not pars:
            message = self.plugin.EvalString(message)
        return self.plugin.BroadcastMessage(message)

    def Configure(self, message="", pars=False):
        text = self.text
        panel = eg.ConfigPanel()
        messCtrl = wx.TextCtrl(panel, -1, message)
        parsCtrl = wx.CheckBox(panel, -1, self.plugin.text.parsing)
        parsCtrl.SetValue(pars)
        messSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.mess),
            wx.VERTICAL
        )
        panel.sizer.Add(messSizer, 0, wx.EXPAND | wx.TOP, 15)
        messSizer.Add(messCtrl, 0, wx.EXPAND)
        messSizer.Add(parsCtrl, 0, wx.EXPAND | wx.TOP, 3)

        while panel.Affirmed():
            panel.SetResult(
                messCtrl.GetValue(),
                parsCtrl.GetValue()
            )


# ===============================================================================

class WsBroadcastValue(eg.ActionBase):
    class text:
        varnames = "Variable name or list of variables (separated by commas):"
        err = 'Error in action "Websocket broadcast values(%s)"'

    def __call__(self, varnames=""):
        try:
            keys = varnames.replace(" ", "")
            keys = keys.split(",")
        except:
            eg.PrintError(self.text.err % str(varnames))
            return
        try:
            vals = {}
            for key in keys:
                k = self.plugin.EvalString(key)
                vals[k] = self.plugin.GetValue(k)
        except:
            eg.PrintError(self.text.err % str(varnames))
        return self.plugin.BroadcastMessage(
            json.dumps({'method': 'Values', 'kwargs': vals})
        )

    def Configure(self, varnames=""):
        panel = eg.ConfigPanel(self)
        varnamesCtrl = panel.TextCtrl(varnames)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        varnamesLbl = panel.StaticText(self.text.varnames)
        mainSizer.Add(varnamesLbl)
        mainSizer.Add(varnamesCtrl, 0, wx.EXPAND | wx.TOP, 1)
        panel.sizer.Add(mainSizer, 0, wx.EXPAND | wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(
                varnamesCtrl.GetValue(),
            )
        # ===============================================================================


class WsSendValue(eg.ActionBase):
    class text:
        varnames = "Variable name or list of variables (separated by commas):"

    def __call__(
        self,
        cl_ip="127.0.0.1",
        cl_port="1234",
        modeClient=1,
        varnames="",
    ):
        try:
            keys = varnames.replace(" ", "")
            keys = keys.split(",")
        except:
            eg.PrintError(self.text.err % str(varnames))
            return
        try:
            vals = {}
            for key in keys:
                k = self.plugin.EvalString(key)
                vals[k] = self.plugin.GetValue(k)
        except:
            eg.PrintError(self.text.err % str(varnames))
        return self.plugin.ServerSendMessage(
            json.dumps({'method': 'Values', 'kwargs': vals}),
            cl_ip,
            cl_port,
            modeClient,
        )

    def GetLabel(self, cl_ip, cl_port, modeClient, varnames):
        if modeClient:
            client = "{eg.event.payload[0]}"
            return "%s: %s: %s" % (self.name, client, varnames)
        else:
            return "%s: %s:%s: %s" % (self.name, cl_ip, cl_port, varnames)

    def Configure(
        self,
        cl_ip="127.0.0.1",
        cl_port="1234",
        modeClient=1,
        varnames="",
    ):
        text = self.text
        panel = eg.ConfigPanel()
        id2 = wx.NewIdRef()
        id3 = wx.NewIdRef()
        id4 = wx.NewIdRef()
        radioBoxModeClient = wx.RadioBox(
            panel,
            -1,
            self.plugin.text.modeClientChoiceLabel,
            choices=self.plugin.text.modeClientChoice,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxModeClient.SetSelection(modeClient)
        staticBox = wx.StaticBox(panel, -1, "")
        tmpSizer = wx.GridBagSizer(2, 10)
        txtLabel = wx.StaticText(panel, -1, self.plugin.text.host)
        txtCtrl = wx.TextCtrl(panel, id3, "")
        portLabel = wx.StaticText(panel, -1, self.plugin.text.port)
        portCtrl = wx.TextCtrl(panel, id2, "")
        tmpSizer.Add(txtLabel, (0, 0), (1, 1))
        tmpSizer.Add(txtCtrl, (1, 0), (1, 1), flag=wx.EXPAND)
        tmpSizer.Add(portLabel, (2, 0), (1, 1), flag=wx.TOP, border=10)
        tmpSizer.Add(portCtrl, (3, 0), (1, 1))
        middleSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        middleSizer.Add(radioBoxModeClient, 0, wx.LEFT | wx.EXPAND)
        middleSizer.Add((20, -1), 0, wx.LEFT | wx.EXPAND)
        middleSizer.Add(tmpSizer, 0, wx.LEFT | wx.EXPAND)
        panel.sizer.Add(middleSizer, 0, wx.TOP | wx.EXPAND, 8)
        panel.sizer.Layout()
        size2 = (-1, tmpSizer.GetMinSize()[1])

        def OnClientChoice(evt=None):
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

        varnamesCtrl = panel.TextCtrl(varnames)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        varnamesLbl = panel.StaticText(self.text.varnames)
        mainSizer.Add(varnamesLbl)
        mainSizer.Add(varnamesCtrl, 0, wx.EXPAND | wx.TOP, 1)
        panel.sizer.Add(mainSizer, 0, wx.EXPAND | wx.ALL, 10)

        while panel.Affirmed():
            modeClient = radioBoxModeClient.GetSelection()
            if not modeClient:
                cl_ip = wx.FindWindowById(id3).GetValue()
                cl_port = wx.FindWindowById(id4).GetValue()
            panel.SetResult(
                cl_ip,
                cl_port,
                modeClient,
                varnamesCtrl.GetValue(),
            )


# ===============================================================================

class WsBroadcastAllValues(eg.ActionBase):

    def __call__(self):
        values = self.plugin.GetAllValues()
        return self.plugin.BroadcastMessage(
            json.dumps({'method': 'Values', 'kwargs': values})
        )


# ===============================================================================

class WsSendAllValues(eg.ActionBase):

    def __call__(
        self,
        cl_ip="127.0.0.1",
        cl_port="1234",
        modeClient=1
    ):
        values = self.plugin.GetAllValues()
        return self.plugin.ServerSendMessage(
            json.dumps({'method': 'Values', 'kwargs': values}),
            cl_ip,
            cl_port,
            modeClient,
        )

    def GetLabel(self, cl_ip, cl_port, modeClient):
        if modeClient:
            client = "{eg.event.payload[0]}"
            return "%s: %s" % (self.name, client)
        else:
            return "%s: %s:%s" % (self.name, cl_ip, cl_port)

    def Configure(
        self,
        cl_ip="127.0.0.1",
        cl_port="1234",
        modeClient=1
    ):
        panel = eg.ConfigPanel()
        id2 = wx.NewIdRef()
        id3 = wx.NewIdRef()
        id4 = wx.NewIdRef()
        radioBoxModeClient = wx.RadioBox(
            panel,
            -1,
            self.plugin.text.modeClientChoiceLabel,
            choices=self.plugin.text.modeClientChoice,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxModeClient.SetSelection(modeClient)
        staticBox = wx.StaticBox(panel, -1, "")
        tmpSizer = wx.GridBagSizer(2, 10)
        txtLabel = wx.StaticText(panel, -1, self.plugin.text.host)
        txtCtrl = wx.TextCtrl(panel, id3, "")
        portLabel = wx.StaticText(panel, -1, self.plugin.text.port)
        portCtrl = wx.TextCtrl(panel, id2, "")
        tmpSizer.Add(txtLabel, (0, 0), (1, 1))
        tmpSizer.Add(txtCtrl, (1, 0), (1, 1), flag=wx.EXPAND)
        tmpSizer.Add(portLabel, (2, 0), (1, 1), flag=wx.TOP, border=10)
        tmpSizer.Add(portCtrl, (3, 0), (1, 1))
        middleSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        middleSizer.Add(radioBoxModeClient, 0, wx.LEFT | wx.EXPAND)
        middleSizer.Add((20, -1), 0, wx.LEFT | wx.EXPAND)
        middleSizer.Add(tmpSizer, 0, wx.LEFT | wx.EXPAND)
        panel.sizer.Add(middleSizer, 0, wx.TOP | wx.EXPAND, 8)
        panel.sizer.Layout()
        size2 = (-1, tmpSizer.GetMinSize()[1])

        def OnClientChoice(evt=None):
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
            panel.SetResult(
                cl_ip,
                cl_port,
                modeClient,
            )


# ===============================================================================

class WsBroadcastData(eg.ActionBase):
    class text:
        dataName = "Data name:"
        data2send = "Data for broadcast (python expression):"
        onlyChange = "Data send only if it has been changed"
        cond = "Condition for data sending (python expression):"
        period = "Sending period [s]:"

    def Task(self, plugin, dataName):
        if self.plugin.info.isStarted:
            self.task = eg.scheduler.AddTask(
                self.period,
                self.Task,
                self.plugin,
                dataName
            )

        data = self.plugin.EvalString(self.data2send)
        cond = self.plugin.EvalString(self.cond) if self.cond != "" else True
        if cond:
            if data != self.data or not self.onlyChange:
                self.plugin.BroadcastMessage(
                    json.dumps(
                        {'method': 'Data', 'dataName': dataName, 'data': data}
                    )
                )
        self.data = data

    def __call__(
        self,
        dataName="",
        data2send="",
        cond="",
        onlyChange=True,
        period=5.0
    ):
        self.data2send = data2send
        self.onlyChange = onlyChange
        self.cond = cond
        self.period = period
        self.data = None
        if self.value:
            self.Task(self.plugin, dataName)
        else:
            data = self.plugin.EvalString(data2send)
            cond = self.plugin.EvalString(cond) if cond != "" else True
            if cond:
                self.plugin.BroadcastMessage(
                    json.dumps(
                        {'method': 'Data', 'dataName': dataName, 'data': data}
                    )
                )

    def Configure(
        self,
        dataName="",
        data2send="",
        cond="",
        onlyChange=True,
        period=5.0
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
        mainSizer.Add(nameCtrl, 0, wx.EXPAND | wx.TOP, 2)
        mainSizer.Add(sendLabel, 0, wx.TOP, 10)
        mainSizer.Add(sendCtrl, 0, wx.EXPAND | wx.TOP, 2)
        mainSizer.Add(condLabel, 0, wx.TOP, 10)
        mainSizer.Add(condCtrl, 0, wx.EXPAND | wx.TOP, 2)
        panel.sizer.Add(mainSizer, 0, wx.ALL | wx.EXPAND, 10)
        if self.value:
            periodLabel = wx.StaticText(panel, -1, text.period)
            changeCtrl = wx.CheckBox(panel, -1, text.onlyChange)
            changeCtrl.SetValue(onlyChange)
            periodCtrl = eg.SpinNumCtrl(
                panel,
                -1,
                period,
                integerWidth=5,
                fractionWidth=1,
                allowNegative=False,
                min=0.1,
                increment=0.1,
            )
            perSizer = wx.BoxSizer(wx.HORIZONTAL)
            perSizer.Add(periodLabel, 0, wx.TOP, 3)
            perSizer.Add(periodCtrl, 0, wx.LEFT, 1)
            perSizer.Add((-1, -1), 1, wx.EXPAND)
            perSizer.Add(changeCtrl, 0, wx.TOP, 4)
            mainSizer.Add(perSizer, 0, wx.EXPAND | wx.TOP, 10)

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
        # ===============================================================================


class WsPeriodicallySendData(eg.ActionBase):
    class text:
        dataName = "Data name:"
        data2send = "Data for broadcast (python expression):"
        cond = "Condition for data sending (python expression):"
        onlyChange = "Data send only if it has been changed"
        period = "Sending period [s]:"

    def Task(self, plugin, client, dataName):
        if self.plugin.info.isStarted:
            self.task = eg.scheduler.AddTask(
                self.period,
                self.Task,
                self.plugin,
                client,
                dataName
            )
        data = self.plugin.EvalString(self.data2send)
        cond = self.plugin.EvalString(self.cond) if self.cond != "" else True
        if cond:
            if data != self.data or not self.onlyChange:
                self.plugin.ServerSendMessage(
                    json.dumps({
                        'method': 'Data',
                        'dataName': dataName,
                        'data': data
                    }),
                    self.cl_ip,
                    self.cl_port,
                    self.modeClient,
                )
        self.data = data

    def __call__(
        self,
        cl_ip="127.0.0.1",
        cl_port="1234",
        modeClient=1,
        dataName="",
        data2send="",
        onlyChange=True,
        cond="",
        period=5.0
    ):
        self.cl_ip = cl_ip
        self.cl_port = cl_port
        self.modeClient = modeClient
        self.data2send = data2send
        self.onlyChange = onlyChange
        self.cond = cond
        self.period = period
        self.data = None

        client = eg.event.payload[0] if modeClient else (
            eg.ParseString(cl_ip),
            int(eg.ParseString(cl_port))
        )
        if self.value:
            self.Task(self.plugin, client, dataName)
        else:
            data = self.plugin.EvalString(data2send)
            cond = self.plugin.EvalString(cond) if cond != "" else True
            if cond:
                self.plugin.ServerSendMessage(
                    json.dumps({
                        'method': 'Data',
                        'dataName': dataName,
                        'data': data
                    }),
                    cl_ip,
                    cl_port,
                    modeClient,
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
        cl_ip="127.0.0.1",
        cl_port="1234",
        modeClient=1,
        dataName="",
        data2send="",
        onlyChange=True,
        cond="",
        period=5.0
    ):
        text = self.text
        panel = eg.ConfigPanel()
        id2 = wx.NewIdRef()
        id3 = wx.NewIdRef()
        id4 = wx.NewIdRef()
        radioBoxModeClient = wx.RadioBox(
            panel,
            -1,
            self.plugin.text.modeClientChoiceLabel,
            choices=self.plugin.text.modeClientChoice,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxModeClient.SetSelection(modeClient)
        staticBox = wx.StaticBox(panel, -1, "")
        tmpSizer = wx.GridBagSizer(2, 10)
        txtLabel = wx.StaticText(panel, -1, self.plugin.text.host)
        txtCtrl = wx.TextCtrl(panel, id3, "")
        portLabel = wx.StaticText(panel, -1, self.plugin.text.port)
        portCtrl = wx.TextCtrl(panel, id2, "")
        tmpSizer.Add(txtLabel, (0, 0), (1, 1))
        tmpSizer.Add(txtCtrl, (1, 0), (1, 1), flag=wx.EXPAND)
        tmpSizer.Add(portLabel, (2, 0), (1, 1), flag=wx.TOP, border=10)
        tmpSizer.Add(portCtrl, (3, 0), (1, 1))
        middleSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        middleSizer.Add(radioBoxModeClient, 0, wx.LEFT | wx.EXPAND)
        middleSizer.Add((20, -1), 0, wx.LEFT | wx.EXPAND)
        middleSizer.Add(tmpSizer, 0, wx.LEFT | wx.EXPAND)
        panel.sizer.Add(middleSizer, 0, wx.TOP | wx.EXPAND, 8)
        nameLabel = wx.StaticText(panel, -1, text.dataName)
        sendLabel = wx.StaticText(panel, -1, text.data2send)
        condLabel = wx.StaticText(panel, -1, text.cond)
        nameCtrl = wx.TextCtrl(panel, -1, dataName)
        sendCtrl = wx.TextCtrl(panel, -1, data2send)
        condCtrl = wx.TextCtrl(panel, -1, cond)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(nameLabel)
        mainSizer.Add(nameCtrl, 0, wx.EXPAND | wx.TOP, 2)
        mainSizer.Add(sendLabel, 0, wx.TOP, 10)
        mainSizer.Add(sendCtrl, 0, wx.EXPAND | wx.TOP, 2)
        mainSizer.Add(condLabel, 0, wx.TOP, 10)
        mainSizer.Add(condCtrl, 0, wx.EXPAND | wx.TOP, 2)
        panel.sizer.Add(mainSizer, 0, wx.ALL | wx.EXPAND, 10)
        if self.value:
            periodLabel = wx.StaticText(panel, -1, text.period)
            periodCtrl = eg.SpinNumCtrl(
                panel,
                -1,
                period,
                integerWidth=5,
                fractionWidth=1,
                allowNegative=False,
                min=0.1,
                increment=0.1,
            )
            changeCtrl = wx.CheckBox(panel, -1, text.onlyChange)
            changeCtrl.SetValue(onlyChange)
            perSizer = wx.BoxSizer(wx.HORIZONTAL)
            perSizer.Add(periodLabel, 0, wx.TOP, 3)
            perSizer.Add(periodCtrl, 0, wx.LEFT, 1)
            perSizer.Add((-1, -1), 1, wx.EXPAND)
            perSizer.Add(changeCtrl, 0, wx.TOP, 4)
            mainSizer.Add(perSizer, 0, wx.EXPAND | wx.TOP, 10)
        panel.sizer.Layout()
        size2 = (-1, tmpSizer.GetMinSize()[1])

        def OnClientChoice(evt=None):
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


# ===============================================================================

class WsSendCommand(eg.ActionBase):
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

    def Task(self, plugin, client, cmdName):
        if self.plugin.info.isStarted:
            self.task = eg.scheduler.AddTask(
                self.period,
                self.Task,
                self.plugin,
                client,
                cmdName
            )
        args = [self.plugin.EvalString(self.arg1)] if self.arg1 != "" else []
        if self.arg2 != "":
            args.append(self.plugin.EvalString(self.arg2))
        if self.arg3 != "":
            args.append(self.plugin.EvalString(self.arg3))
        if self.othArgs != "":
            try:
                othArgs = list(self.plugin.EvalString(self.othArgs))
                args.extend(othArgs)
            except:
                pass
        kwargs = {}
        if kwArgs != "":
            try:
                kwargs = dict(self.plugin.EvalString(kwArgs, False))
            except:
                pass
        cond = self.plugin.EvalString(self.cond) if self.cond != "" else True
        if cond:
            if args != self.args or kwargs != self.kwargs or not self.onlyChange:
                self.plugin.BroadcastMessage(
                    json.dumps(
                        {
                            'method': 'Command',
                            'cmdName': cmdName,
                            'args': args,
                            'kwargs': kwargs
                        }
                    )
                )
        self.args = args
        self.kwargs = kwargs

    def __call__(
        self,
        cl_ip="127.0.0.1",
        cl_port="1234",
        modeClient=1,
        cmdName="",
        cond="",
        arg1="",
        arg2="",
        arg3="",
        othArgs="",
        kwArgs="",
        onlyChange=True,
        period=5.0
    ):
        cmdName = self.plugin.EvalString(cmdName)
        client = eg.event.payload[0] if modeClient else (
            eg.ParseString(cl_ip),
            int(eg.ParseString(cl_port))
        )
        if self.value:
            self.cond = cond
            self.arg1 = arg1
            self.arg2 = arg2
            self.arg3 = arg3
            self.othArgs = othArgs
            self.kwArgs = kwArgs
            self.onlyChange = onlyChange
            self.period = period
            self.Task(self.plugin, client, cmdName)
        else:
            args = [self.plugin.EvalString(arg1)] if arg1 != "" else []
            if arg2 != "":
                args.append(self.plugin.EvalString(arg2))
            if arg3 != "":
                args.append(self.plugin.EvalString(arg3))
            if othArgs != "":
                try:
                    othArgs = list(self.plugin.EvalString(othArgs))
                    args.extend(othArgs)
                except:
                    pass
            kwargs = {}
            if kwArgs != "":
                try:
                    kwargs = dict(self.plugin.EvalString(kwArgs, False))
                except:
                    pass
            cond = self.plugin.EvalString(cond) if cond != "" else True
            if cond:
                self.plugin.BroadcastMessage(
                    json.dumps(
                        {
                            'method': 'Command',
                            'cmdName': cmdName,
                            'args': args,
                            'kwargs': kwargs
                        }
                    )
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
        cl_ip="127.0.0.1",
        cl_port="1234",
        modeClient=1,
        cmdName="",
        cond="",
        arg1="",
        arg2="",
        arg3="",
        othArgs="",
        kwArgs="",
        onlyChange=True,
        period=5.0
    ):
        panel = eg.ConfigPanel(self)
        text = self.text
        id2 = wx.NewIdRef()
        id3 = wx.NewIdRef()
        id4 = wx.NewIdRef()
        radioBoxModeClient = wx.RadioBox(
            panel,
            -1,
            self.plugin.text.modeClientChoiceLabel,
            choices=self.plugin.text.modeClientChoice,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxModeClient.SetSelection(modeClient)
        staticBox = wx.StaticBox(panel, -1, "")
        tmpSizer = wx.GridBagSizer(2, 10)
        txtLabel = wx.StaticText(panel, -1, self.plugin.text.host)
        txtCtrl = wx.TextCtrl(panel, id3, "")
        portLabel = wx.StaticText(panel, -1, self.plugin.text.port)
        portCtrl = wx.TextCtrl(panel, id2, "")
        tmpSizer.Add(txtLabel, (0, 0), (1, 1))
        tmpSizer.Add(txtCtrl, (1, 0), (1, 1), flag=wx.EXPAND)
        tmpSizer.Add(portLabel, (2, 0), (1, 1), flag=wx.TOP, border=10)
        tmpSizer.Add(portCtrl, (3, 0), (1, 1))
        middleSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        middleSizer.Add(radioBoxModeClient, 0, wx.LEFT | wx.EXPAND)
        middleSizer.Add((20, -1), 0, wx.LEFT | wx.EXPAND)
        middleSizer.Add(tmpSizer, 0, wx.LEFT | wx.EXPAND)
        panel.sizer.Add(middleSizer, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 8)

        panel.sizer.Layout()
        size2 = (-1, tmpSizer.GetMinSize()[1])

        def OnClientChoice(evt=None):
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
        mainSizer = wx.FlexGridSizer(8, 2, 2, 10)
        mainSizer.AddGrowableCol(1)
        mainSizer.Add(nameLabel, 0, wx.TOP, 3)
        mainSizer.Add(nameCtrl, 0, wx.EXPAND)
        mainSizer.Add(arg1Label, 0, wx.TOP, 3)
        mainSizer.Add(arg1Ctrl, 0, wx.EXPAND)
        mainSizer.Add(arg2Label, 0, wx.TOP, 3)
        mainSizer.Add(arg2Ctrl, 0, wx.EXPAND)
        mainSizer.Add(arg3Label, 0, wx.TOP, 3)
        mainSizer.Add(arg3Ctrl, 0, wx.EXPAND)
        mainSizer.Add(othLabel, 0, wx.TOP, 3)
        mainSizer.Add(othCtrl, 0, wx.EXPAND)
        mainSizer.Add(kwLabel, 0, wx.TOP, 3)
        mainSizer.Add(kwCtrl, 0, wx.EXPAND)
        mainSizer.Add(condLabel, 0, wx.TOP, 3)
        mainSizer.Add(condCtrl, 0, wx.EXPAND)
        if self.value:
            periodLabel = wx.StaticText(panel, -1, text.period)
            periodCtrl = eg.SpinNumCtrl(
                panel,
                -1,
                period,
                integerWidth=5,
                fractionWidth=1,
                allowNegative=False,
                min=0.1,
                increment=0.1,
            )
            changeCtrl = wx.CheckBox(panel, -1, text.onlyChange)
            changeCtrl.SetValue(onlyChange)
            perSizer = wx.BoxSizer(wx.HORIZONTAL)
            mainSizer.Add(periodLabel, 0, wx.TOP, 3)
            perSizer.Add(periodCtrl, 0, wx.LEFT, 1)
            perSizer.Add((-1, -1), 1, wx.EXPAND)
            perSizer.Add(changeCtrl, 0, wx.TOP, 4)
            mainSizer.Add(perSizer, 0, wx.EXPAND)
        panel.sizer.Add(mainSizer, 0, wx.ALL | wx.EXPAND, 8)

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
        # ===============================================================================


class WsBroadcastCommand(eg.ActionBase):
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

    def Task(self, plugin, cmdName):
        if self.plugin.info.isStarted:
            self.task = eg.scheduler.AddTask(
                self.period,
                self.Task,
                plugin,
                cmdName
            )
        args = [self.plugin.EvalString(self.arg1)] if self.arg1 != "" else []
        if self.arg2 != "":
            args.append(self.plugin.EvalString(self.arg2))
        if self.arg3 != "":
            args.append(self.plugin.EvalString(self.arg3))
        if self.othArgs != "":
            try:
                othArgs = list(self.plugin.EvalString(self.othArgs))
                args.extend(othArgs)
            except:
                pass
        kwargs = {}
        if self.kwArgs != "":
            try:
                kwargs = dict(self.plugin.EvalString(self.kwArgs, False))
            except:
                pass
        cond = self.plugin.EvalString(self.cond) if self.cond != "" else True
        if cond:
            if args != self.args or kwargs != self.kwargs or not self.onlyChange:
                self.plugin.BroadcastMessage(
                    json.dumps(
                        {
                            'method': 'Command',
                            'cmdName': cmdName,
                            'args': args,
                            'kwargs': kwargs
                        }
                    )
                )
        self.args = args
        self.kwargs = kwargs

    def __call__(
        self,
        cmdName="",
        cond="",
        arg1="",
        arg2="",
        arg3="",
        othArgs="",
        kwArgs="",
        onlyChange=True,
        period=5.0
    ):
        cmdName = self.plugin.EvalString(cmdName)
        if self.value:
            self.arg1 = arg1
            self.arg2 = arg2
            self.arg3 = arg3
            self.othArgs = othArgs
            self.kwArgs = kwArgs
            self.onlyChange = onlyChange
            self.period = period
            self.cond = cond
            self.args = None
            self.kwargs = None
            self.Task(self.plugin, cmdName)
        else:
            args = [self.plugin.EvalString(arg1)] if arg1 != "" else []
            if arg2 != "":
                args.append(self.plugin.EvalString(arg2))
            if arg3 != "":
                args.append(self.plugin.EvalString(arg3))
            if othArgs != "":
                try:
                    othArgs = list(self.plugin.EvalString(othArgs))
                    args.extend(othArgs)
                except:
                    pass
            kwargs = {}
            if kwArgs != "":
                try:
                    kwargs = dict(self.plugin.EvalString(kwArgs, False))
                except:
                    pass
            cond = self.plugin.EvalString(cond) if cond != "" else True
            if cond:
                self.plugin.BroadcastMessage(
                    json.dumps(
                        {
                            'method': 'Command',
                            'cmdName': cmdName,
                            'args': args,
                            'kwargs': kwargs
                        }
                    )
                )

    def Configure(
        self,
        cmdName="",
        cond="",
        arg1="",
        arg2="",
        arg3="",
        othArgs="",
        kwArgs="",
        onlyChange=True,
        period=5.0
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
        mainSizer = wx.FlexGridSizer(8, 2, 2, 10)
        mainSizer.AddGrowableCol(1)
        mainSizer.Add(nameLabel, 0, wx.TOP, 3)
        mainSizer.Add(nameCtrl, 0, wx.EXPAND)
        mainSizer.Add(arg1Label, 0, wx.TOP, 3)
        mainSizer.Add(arg1Ctrl, 0, wx.EXPAND)
        mainSizer.Add(arg2Label, 0, wx.TOP, 3)
        mainSizer.Add(arg2Ctrl, 0, wx.EXPAND)
        mainSizer.Add(arg3Label, 0, wx.TOP, 3)
        mainSizer.Add(arg3Ctrl, 0, wx.EXPAND)
        mainSizer.Add(othLabel, 0, wx.TOP, 3)
        mainSizer.Add(othCtrl, 0, wx.EXPAND)
        mainSizer.Add(kwLabel, 0, wx.TOP, 3)
        mainSizer.Add(kwCtrl, 0, wx.EXPAND)
        mainSizer.Add(condLabel, 0, wx.TOP, 3)
        mainSizer.Add(condCtrl, 0, wx.EXPAND)
        panel.sizer.Add(mainSizer, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        if self.value:
            periodLabel = wx.StaticText(panel, -1, text.period)
            periodCtrl = eg.SpinNumCtrl(
                panel,
                -1,
                period,
                integerWidth=5,
                fractionWidth=1,
                allowNegative=False,
                min=0.1,
                increment=0.1,
            )
            changeCtrl = wx.CheckBox(panel, -1, text.onlyChange)
            changeCtrl.SetValue(onlyChange)
            perSizer = wx.BoxSizer(wx.HORIZONTAL)
            perSizer.Add(periodCtrl, 0, wx.LEFT, 1)
            perSizer.Add((-1, -1), 1, wx.EXPAND)
            perSizer.Add(changeCtrl, 0, wx.TOP, 4)
            mainSizer.Add(periodLabel, 0, wx.TOP, 3)
            mainSizer.Add(perSizer, 0, wx.EXPAND)

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
        # ===============================================================================


class WsStopPeriodicTasks(eg.ActionBase):
    class text:
        label = "Data or command name (empty = all broadcast tasks):"

    def __call__(self, taskName=""):
        self.plugin.StopPeriodicTasks(self.value, taskName)

    def Configure(self, taskName=""):
        panel = eg.ConfigPanel()
        taskCtrl = wx.TextCtrl(panel, -1, taskName)
        if self.value:
            taskCtrl.Show(False)
            panel.dialog.buttonRow.applyButton.Enable(False)
            panel.dialog.buttonRow.testButton.Show(False)
            label = panel.StaticText(
                eg.text.General.noOptionsAction,
                style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE
            )
            panel.sizer.Add((0, 0), 1, wx.EXPAND)
            panel.sizer.Add(label, 0, wx.ALIGN_CENTRE)
            panel.sizer.Add((0, 0), 1, wx.EXPAND)
        else:
            label = wx.StaticText(panel, -1, self.text.label)
            mainSizer = wx.BoxSizer(wx.VERTICAL)
            mainSizer.Add(label)
            mainSizer.Add(taskCtrl, 0, wx.EXPAND)
            panel.sizer.Add(mainSizer, 1, wx.EXPAND | wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(taskCtrl.GetValue(), )


# ===============================================================================

class WsStopClientPeriodicTasks(eg.ActionBase):
    class text:
        label = "Data or command name (empty = all  client's  tasks):"

    def __call__(
        self,
        cl_ip="127.0.0.1",
        cl_port="1234",
        modeClient=1,
        taskName=""
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
        cl_port="1234",
        modeClient=1,
        taskName=""
    ):
        text = self.text
        panel = eg.ConfigPanel()
        label = wx.StaticText(panel, -1, self.text.label)
        taskCtrl = wx.TextCtrl(panel, -1, taskName)
        id2 = wx.NewIdRef()
        id3 = wx.NewIdRef()
        id4 = wx.NewIdRef()
        radioBoxModeClient = wx.RadioBox(
            panel,
            -1,
            self.plugin.text.modeClientChoiceLabel,
            choices=self.plugin.text.modeClientChoice,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxModeClient.SetSelection(modeClient)
        staticBox = wx.StaticBox(panel, -1, "")
        tmpSizer = wx.GridBagSizer(2, 10)
        txtLabel = wx.StaticText(panel, -1, self.plugin.text.host)
        txtCtrl = wx.TextCtrl(panel, id3, "")
        portLabel = wx.StaticText(panel, -1, self.plugin.text.port)
        portCtrl = wx.TextCtrl(panel, id2, "")
        tmpSizer.Add(txtLabel, (0, 0), (1, 1))
        tmpSizer.Add(txtCtrl, (1, 0), (1, 1), flag=wx.EXPAND)
        tmpSizer.Add(portLabel, (2, 0), (1, 1), flag=wx.TOP, border=10)
        tmpSizer.Add(portCtrl, (3, 0), (1, 1))
        middleSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        middleSizer.Add(radioBoxModeClient, 0, wx.LEFT | wx.EXPAND)
        middleSizer.Add((20, -1), 0, wx.LEFT | wx.EXPAND)
        middleSizer.Add(tmpSizer, 0, wx.LEFT | wx.EXPAND)
        panel.sizer.Add(middleSizer, 0, wx.TOP | wx.EXPAND, 8)
        panel.sizer.Layout()
        size2 = (-1, tmpSizer.GetMinSize()[1])

        def OnClientChoice(evt=None):
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
        panel.sizer.Add(label, 0, wx.TOP, 8)
        panel.sizer.Add(taskCtrl, 0, wx.EXPAND | wx.TOP, 2)

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


# ===============================================================================

class SendEvent(eg.ActionBase):
    class text:
        event = "Event:"
        host = "Host:"
        port = "Port:"
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
        pars=False
    ):
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

            response = HTTPResponse(sock)
            response.begin()
            content = response.read()
            response.close()
            sock.close()
            if response.status != 200:
                raise Exception(
                    text.errmsg % response.status
                )
            return json.loads(content)

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
        pars=False
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
        fl = wx.EXPAND | wx.TOP
        box = wx.GridBagSizer(2, 5)
        box.Add(panel.StaticText(text.event), (0, 0), flag=wx.TOP, border=12)
        box.Add(eventCtrl, (0, 1), flag=fl, border=9)
        box.Add(parsCtrl, (1, 0), (1, 2))
        box.Add(panel.StaticText(text.host), (2, 0), flag=wx.TOP, border=12)
        box.Add(hostCtrl, (2, 1), flag=fl, border=9)
        box.Add(panel.StaticText(text.port), (3, 0), flag=wx.TOP, border=12)
        box.Add(portCtrl, (3, 1), flag=wx.TOP, border=9)
        box.Add(panel.StaticText(text.username), (4, 0), flag=wx.TOP, border=12)
        box.Add(userCtrl, (4, 1), flag=fl, border=9)
        box.Add(panel.StaticText(text.password), (5, 0), flag=wx.TOP, border=12)
        box.Add(passwordCtrl, (5, 1), flag=fl, border=9)
        box.AddGrowableCol(1)
        panel.sizer.Add(box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        while panel.Affirmed():
            panel.SetResult(
                eventCtrl.GetValue(),
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                userCtrl.GetValue(),
                passwordCtrl.GetValue(),
                parsCtrl.GetValue()
            )


# ===============================================================================

# Enhancement by Sem;colon - START
class SendEventExt(eg.ActionBase):
    class text:
        url = "Url:"
        urlTT = "Like you would put it into a webbrowser"
        event = "Event:"
        username = "Username:"
        password = "Password:"
        msg1 = "This page isn't protected by authentication."
        msg2 = 'But we failed for another reason.'
        msg3 = 'A 401 error without an authentication response header - very weird.'
        msg4 = 'The authentication line is badly formed.'
        msg5 = 'This example only works with BASIC authentication.'
        msg6 = "url, username or password is wrong."

    def __call__(self, event="", host="", user="", password=""):
        text = self.text
        req = urllib2.Request(host, event)
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

            authobj = compile(r'''(?:\s*www-authenticate\s*:)?\s*(\w*)\s+realm=['"](\w+)['"]''', IGNORECASE)
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
            authheader = "Basic %s" % base64string
            req.add_header("Authorization", authheader)
            try:
                handle = urllib2.urlopen(req)
            except IOError, e:
                print text.msg6
        # else:
        # If we don't fail then the page isn't protected
        # print "This page isn't protected by authentication."
        thepage = urllib2.unquote(handle.read()).decode(eg.systemEncoding, 'replace')  # handle.read()
        return thepage

    def Configure(self, event="", host="http://127.0.0.1:80", user="", password=""):
        text = self.text
        panel = eg.ConfigPanel(self)
        eventCtrl = panel.TextCtrl(event)
        hostLabel = panel.StaticText(text.url)
        hostCtrl = panel.TextCtrl(host)
        userCtrl = panel.TextCtrl(user)
        passwordCtrl = panel.TextCtrl(password)
        hostLabel.SetToolTip(text.urlTT)
        hostCtrl.SetToolTip(text.urlTT)
        fl = wx.EXPAND | wx.TOP
        box = wx.GridBagSizer(2, 5)
        box.Add(panel.StaticText(text.event), (0, 0), flag=wx.TOP, border=12)
        box.Add(eventCtrl, (0, 1), flag=fl, border=9)
        box.Add(hostLabel, (1, 0), flag=wx.TOP, border=12)
        box.Add(hostCtrl, (1, 1), flag=fl, border=9)
        box.Add(panel.StaticText(text.username), (2, 0), flag=wx.TOP, border=12)
        box.Add(userCtrl, (2, 1), flag=fl, border=9)
        box.Add(panel.StaticText(text.password), (3, 0), flag=wx.TOP, border=12)
        box.Add(passwordCtrl, (3, 1), flag=fl, border=9)
        box.AddGrowableCol(1)
        panel.sizer.Add(box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        while panel.Affirmed():
            panel.SetResult(
                eventCtrl.GetValue(),
                hostCtrl.GetValue(),
                userCtrl.GetValue(),
                passwordCtrl.GetValue(),
            )


# Enhancement by Sem;colon - END
# ===============================================================================

class Tornado(eg.PluginBase):
    knowlClients = {}
    pubPerClients = {}
    pubVars = {}
    pubPerVars = {}
    extensions_map = None
    server = None

    class text:
        generalBox = "General Settings"
        port = "TCP/IP port:"
        documentRoot = "HTML documents root:"
        eventPrefix = "Event prefix:"
        websocketFldr = "Websocket virtual subfolder:"
        logFile = "Log file (blank = no logging):"
        limit1 = "Maximum line length:"
        limit2 = "characters (0 = no limit)"
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
        autosave = "Automatically save the document when the value of a" \
                   " persistent variable is changed"
        nonAjaxBox = "Additional settings for non-AJAX POST requests"
        websocketBox = "Settings for WebSocket"
        logBox = "Settings for (debug) logging"
        listSplitter = "String between list items:"
        valueSplitter = "String between returned values:"
        parsing = "disable parsing and/or evaluating of string"
        wsClientDisconn = "WsClientDisconnected"
        wsClientConn = "WsClientConnected"
        started = "Tornado webserver started as %s on port %i"
        secur = (
            "secured (https://)",
            "unsecured (http://)",
        )
        stopped = "Tornado webserver on port %i stopped"
        cli_discon = "Client disconnected"
        cli_con = "Client connected"
        modeClientChoiceLabel = 'Client address to specify as'
        modeClientChoice = (
            'Explicitly (or Python expression)',
            'From eg.event.payload[0]',
        )
        host = "TCP/IP address:"
        certfile = "SSL certificate"
        keyfile = "SSL private key"
        defDoc = "Default document:"
        defDocTool = 'If it is filled (for example as "index.html"), then just' \
                     ' this one document will be open instead of "It works!" page.'
        sslTool = "Select the appropriate file if you want to use a secure " \
                  "protocol (https).\n If this field remains blank, the server will use an " \
                  "insecure protocol (http). "
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

    def __init__(self):
        self.AddEvents()
        self.AddActionsFromList(ACTIONS)
        self.running = False
        if not mimetypes.inited:
            mimetypes.init()
        self.extensions_map = mimetypes.types_map.copy()
        self.extensions_map.update({
            '.webp': 'image/webp',
            '.ico': 'image/x-icon',
            '.svg': 'image/svg+xml',
            '.manifest': 'text/cache-manifest',
            '.json': 'application/json'
        })

    def __start__(
        self,
        prefix=None,
        port=80,
        basepath=None,
        authRealm="Eventghost",
        authUsername="",
        authPassword="",
        pubPerVars={},
        autosave=False,
        listSplitter=",",
        valueSplitter=";;",
        wsvs="ws",
        log="",
        limit=0,
        certfile="",
        keyfile="",
        defDoc=""
    ):
        self.info.eventPrefix = prefix
        if authUsername or authPassword:
            authString = base64.b64encode(authUsername + ':' + authPassword)
        else:
            authString = None
        self.wsClients = {}
        self.knowlClients = {}
        self.pubPerClients = {}
        self.pubVars = {}
        self.tv = KeysAsAttrs(self.pubVars)
        self.pubPerVars = pubPerVars
        self.pv = KeysAsAttrs(self.pubPerVars)
        self.autosave = autosave
        self.listSplitter = unicode(listSplitter)
        self.valueSplitter = unicode(valueSplitter)
        self.defDoc = defDoc
        for key in self.pubPerVars.iterkeys():
            self.pubPerClients[key] = []
        eg.PrintNotice("Persistent values: " + repr(self.pubPerVars))
        self.basepath = basepath
        self.authRealm = authRealm
        self.authString = authString
        self.logger = logging.getLogger("Tornado_" + str(port))
        # if not eg.debug.level:
        self.logger.propagate = 0  # !!!
        if log:
            self.logger.setLevel(logging.DEBUG)
            hndlr = logging.handlers.TimedRotatingFileHandler(
                log,
                when='midnight',
                interval=1,
                backupCount=10
            )
            hndlr.setFormatter(LogFormatter(limit))
        else:
            hndlr = NullHandler()
        self.logger.addHandler(hndlr)
        if isfile(certfile) and isfile(keyfile):
            ssl_options = dict(
                certfile=certfile,
                keyfile=keyfile,
                cert_reqs=0
            )
        else:
            ssl_options = None
        self.httpd_thread = ServerThread(self, port, wsvs, ssl_options)
        self.httpd_thread.start()
        secur = int(ssl_options is None)
        self.logger.info(self.text.started % (self.text.secur[secur], port))

    def __stop__(self):
        self.logger.info(self.text.stopped % self.server.port)
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)
        self.server.Stop()
        self.StopPeriodicTasks(True)
        self.httpd_thread = None

    def GetValue(self, key, client=None):
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

    def GetPersistentValue(self, key, client=None):
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

    def GetAllValues(self, client=None):
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
        return tmpDict

    def BroadcastMessage(self, message):
        #### krambriw
        try:
            for key, client in self.wsClients.iteritems():
                success = False
                for i in range(5):
                    if not success:
                        try:
                            client.write_message(message)
                            success = True
                        except:
                            time.sleep(0.05)
                            # print 'New attempt:', i, repr(key)
                if not success:
                    del self.wsClients[key]
                    eg.PrintError("WebSocket client %s force deleted" % repr(key))
        except:
            pass

    ####

    def ServerSendMessage(self, message, cl_ip, cl_port, modeClient):
        client = eg.event.payload[0] if modeClient else (
            eg.ParseString(cl_ip),
            int(eg.ParseString(cl_port))
        )
        if client in self.wsClients:
            self.wsClients[client].write_message(message)
        else:
            self.logger.warning(
                "KeyError (non existent client): %s" % repr(client)
            )
            eg.PrintNotice("KeyError (non existent client): %s" % repr(client))

    def SetDocIsDirty(self):
        eg.document.SetIsDirty()
        if self.autosave:
            eg.document.Save()

    def EvalString(self, strng, remBrac=True):
        try:
            strng = eg.ParseString(strng)
        except:
            if remBrac and strng.startswith("{") and strng.endswith("}"):
                strng = strng[1:-1]
        tv = self.tv
        pv = self.pv
        try:
            strng = eval(strng)
        except:
            pass
        return strng

    def StopPeriodicTasks(self, all, taskName=""):
        for t in eg.scheduler.__dict__['heap']:
            try:
                if len(t[2]) > 1 and t[2][0] == self:
                    if all:
                        eg.scheduler.CancelTask(t)
                    elif len(t[2]) == 2:
                        if taskName == "" or taskName == t[2][1]:
                            eg.scheduler.CancelTask(t)
            except:
                pass

    def StopClientPeriodicTasks(self, client, taskName=""):
        for t in eg.scheduler.__dict__['heap']:
            try:
                if len(t[2]) > 2 and t[2][0] == self and t[2][1] == client:
                    if taskName == "" or taskName == t[2][2]:
                        eg.scheduler.CancelTask(t)
            except:
                pass

    def ProcessTheArguments(self, handler, methodName, args, kwargs):
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
                    result = self.GetValue(args[0], handler.client_address[0])
                except:
                    pass
        elif methodName == "GetPersistentValue":
            if len(args):
                try:
                    result = self.GetPersistentValue(
                        args[0],
                        handler.client_address[0]
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
            result = self.GetAllValues(handler.client_address[0])
        elif methodName == "GetChangedValues":
            result = self.GetChangedValues(handler.client_address[0])
        elif methodName == "ExecuteScript":
            try:
                result = eval(args[0])
            except:
                result = None
        elif methodName == "TriggerEvent":
            if 'payload' in kwargs and kwargs['payload'] == 'client_address':
                kwargs['payload'] = [handler.client_address]
            if 'prefix' in kwargs:
                eg.TriggerEvent(*args, **kwargs)
            else:
                self.TriggerEvent(*args, **kwargs)
        elif methodName == "TriggerEnduringEvent":
            self.TriggerEnduringEvent(*args, **kwargs)
            handler.application.repeatTimer.Reset(2000)
        elif methodName == "RepeatEnduringEvent":
            handler.application.repeatTimer.Reset(2000)
        elif methodName == "EndLastEvent":
            handler.application.repeatTimer.Reset(None)
            self.EndLastEvent()
        return result

    def Configure(
        self,
        prefix="HTTP",
        port=80,
        basepath="",
        authRealm="EventGhost",
        authUsername="",
        authPassword="",
        pubPerVars={},
        autosave=False,
        listSplitter=",",
        valueSplitter=";;",
        wsvs="ws",
        log="",
        limit=0,
        certfile="",
        keyfile="",
        defDoc=""
    ):
        text = self.text
        panel = eg.ConfigPanel()
        portCtrl = panel.SpinIntCtrl(port, min=1, max=65535)
        filepathCtrl = panel.DirBrowseButton(basepath)
        certfileCtrl = eg.FileBrowseButton(
            panel,
            -1,
            toolTip=text.sslTool,
            dialogTitle=text.certfile,
            buttonText=eg.text.General.browse,
            startDirectory="",
            initialValue=certfile,  # if certfile is not "" else "",
            fileMask=text.cMask,
        )

        keyfileCtrl = eg.FileBrowseButton(
            panel,
            -1,
            toolTip=text.sslTool,
            dialogTitle=text.keyfile,
            buttonText=eg.text.General.browse,
            startDirectory="",
            initialValue=keyfile,  # if keyfile is not "" else "",
            fileMask=text.kMask,
        )

        defDocCtrl = panel.TextCtrl(defDoc)
        defDocCtrl.SetToolTip(text.defDocTool)
        editCtrl = panel.TextCtrl(prefix)
        wsvsCtrl = panel.TextCtrl(wsvs)
        logCtrl = panel.FileBrowseButton(log)
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
            panel.StaticText(text.websocketFldr),
            panel.StaticText(text.logFile),
            panel.StaticText(text.limit1),
            panel.StaticText(text.certfile + ":"),
            panel.StaticText(text.keyfile + ":"),
            panel.StaticText(text.defDoc)
        )
        eg.EqualizeWidths(labels)
        labels[11].SetToolTip(text.sslTool)
        labels[12].SetToolTip(text.sslTool)
        labels[13].SetToolTip(text.defDocTool)

        acv = wx.ALIGN_CENTER_VERTICAL
        sizer = wx.FlexGridSizer(6, 2, 5, 5)
        sizer.AddGrowableCol(1)
        sizer.Add(labels[0], 0, acv)
        sizer.Add(portCtrl)
        sizer.Add(labels[1], 0, acv)
        sizer.Add(filepathCtrl, 0, wx.EXPAND)
        sizer.Add(labels[13], 0, acv)
        sizer.Add(defDocCtrl, 0, wx.EXPAND)
        sizer.Add(labels[11], 0, acv)
        sizer.Add(certfileCtrl, 0, wx.EXPAND)
        sizer.Add(labels[12], 0, acv)
        sizer.Add(keyfileCtrl, 0, wx.EXPAND)
        sizer.Add(labels[2], 0, acv)
        sizer.Add(editCtrl)
        staticBox = wx.StaticBox(panel, label=text.generalBox)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 5)
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
        staticBoxSizer.Add(sizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND | wx.TOP, 10)

        sizer = wx.FlexGridSizer(3, 2, 5, 5)
        sizer.Add(labels[6], 0, acv)
        sizer.Add(listSplitterCtrl)
        sizer.Add(labels[7], 0, acv)
        sizer.Add(valueSplitterCtrl)
        staticBox = wx.StaticBox(panel, label=text.nonAjaxBox)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND | wx.TOP, 10)

        sizer = wx.FlexGridSizer(2, 2, 5, 5)
        sizer.AddGrowableCol(1)
        sizer.Add(labels[8], 0, acv)
        sizer.Add(wsvsCtrl)
        staticBox = wx.StaticBox(panel, label=text.websocketBox)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND | wx.TOP, 10)

        sizer = wx.FlexGridSizer(2, 2, 5, 5)
        sizer.AddGrowableCol(1)
        sizer.Add(labels[9], 0, acv)
        sizer.Add(logCtrl, 0, wx.EXPAND)
        sizer.Add(labels[10], 0, acv)
        bSizer = wx.BoxSizer(wx.HORIZONTAL)
        limitCtrl = panel.SpinIntCtrl(limit, min=0, max=999)
        bSizer.Add(limitCtrl, 0, wx.RIGHT, 5)
        bSizer.Add(panel.StaticText(text.limit2), 0, acv)
        sizer.Add(bSizer)
        staticBox = wx.StaticBox(panel, label=text.logBox)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND | wx.TOP, 10)

        aSaveCtrl = wx.CheckBox(panel, -1, self.text.autosave)
        aSaveCtrl.SetValue(autosave)
        dialogButton = wx.Button(panel, -1, self.text.dialogPers + " ...")
        dialogButton2 = wx.Button(panel, -1, self.text.dialogTemp + " ...")
        dialogSizer = wx.BoxSizer(wx.HORIZONTAL)
        dialogSizer.Add(dialogButton)
        dialogSizer.Add(dialogButton2, 0, wx.LEFT, 15)
        panel.sizer.Add(aSaveCtrl, 0, wx.TOP, 5)
        panel.sizer.Add(dialogSizer, 0, wx.TOP, 5)

        def OnDialogBtn(evt):
            dlg = VariableDialog(
                parent=panel,
                plugin=self,
                pers=True
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
                parent=panel,
                plugin=self
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
                aSaveCtrl.GetValue(),
                listSplitterCtrl.GetValue(),
                valueSplitterCtrl.GetValue(),
                wsvsCtrl.GetValue(),
                logCtrl.GetValue(),
                limitCtrl.GetValue(),
                certfileCtrl.GetValue(),
                keyfileCtrl.GetValue(),
                defDocCtrl.GetValue()
            )


# ===============================================================================

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
    (eg.ActionGroup,
     'VariableActions',
     'Variable actions',
     'Variable actions', (
         (GetValue,
          "GetValue",
          "Get temporary value",
          "Gets value of temporary variable.",
          None
          ),
         (GetPersistentValue,
          "GetPersistentValue",
          "Get persistent value",
          "Gets value of persistent variable.",
          None
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
     'Websocket actions',
     'Websocket actions', (
         (WsBroadcastMessage,
          'BroadcastMessage',
          'Broadcast message',
          '''Broadcasts a message to all WebSocket clients.

Following (optional) evaluation, message is sent as is (no JSON formatting).''',
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
          None
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
          None
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
         (WsSendMessage,
          'SendMessage',
          'Send message',
          '''Sends a message to one WebSocket client.

Following (optional) evaluation, message is sent as is (no JSON formatting).''',
          None
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
          None
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
          None
          ),
         (WsPeriodicallySendData,
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
         (eg.ActionGroup,
          'PeriodicActions',
          'Periodically repeated actions',
          'Periodically repeated actions', (
              (WsBroadcastData,
               'WsPeriodicallyBroadcastData',
               'Periodically broadcast data',
               '''Periodically broadcasts data to all WebSocket clients.
               
Same as Broadcast data action, but the broadcasting is automatically repeated
periodically after a predetermined time.''',
               True
               ),
              (WsBroadcastCommand,
               'WsPeriodicallyBroadcastCmd',
               'Periodically broadcast command',
               '''Periodically broadcasts command to all WebSocket clients.

Same as Broadcast command action, but the broadcasting is automatically repeated
periodically after a predetermined time.''',
               True
               ),
              (WsPeriodicallySendData,
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

Same as Send command action, but the sending is automatically repeated
periodically after a predetermined time.''',
               True
               ),
              (WsStopPeriodicTasks,
               'WsStopAllPeriodicTasks',
               'Stop all periodic tasks',
               'Stops all periodic tasks.',
               True
               ),
              (WsStopPeriodicTasks,
               'WsStopBroadcastPeriodicTasks',
               'Stop periodic tasks (broadcast)',
               'Stops periodic tasks (broadcast).',
               False
               ),
              (WsStopClientPeriodicTasks,
               'WsStopClientPeriodicTasks',
               'Stop periodic tasks (one client)',
               'Stops periodic tasks (one client).',
               None
               ),
          )),
     )),
)
