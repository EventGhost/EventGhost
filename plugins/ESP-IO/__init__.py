# -*- coding: utf-8 -*-
version = "0.0.5"

# plugins/ESP-IO/__init__.py
#
# Copyright (C) 2017  Pako <lubos.ruckl@gmail.com>
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
# 0.0.5 by Pako 2018-02-10 13:09 GMT+1
#     - added "user variables" actions and "time" actions
# 0.0.4 by Pako 2017-12-21 13:20 GMT+1
#     - http://www.eventghost.net/forum/viewtopic.php?f=9&t=9817&p=49500#p49499
# 0.0.3 by Pako 2017-09-23 19:15 GMT+1
#     - bugfixes
# 0.0.2 by Pako 2017-09-17 07:37 GMT+1
#     - changes to increase reliability
# 0.0.1 by Pako 2017-09-11 13:21 GMT+1
#     - first public version
# ===============================================================================

eg.RegisterPlugin(
    name="ESP-IO",
    author="Pako",
    version=version,
    kind="external",
    guid="{A933B08D-F2F9-4DAC-B901-865EA1C8B527}",
    createMacrosOnAdd=True,
    canMultiLoad=True,
    icon=(
        "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"
    ),
    description=ur'''<rst>
Plugin for control ESP-12F_ (a mini wifi board with 4MB flash based on 
ESP-8266EX).

The project assumes the use of `NodeMcu 1.0`_ or `WeMos D1 mini`_ boards with
FW "ESP-IO".

.. image:: NodeMcu700x525.png
.. image:: WeMos403x345.png

Changing to one of the GPIO will trigger an event in EventGhost.

Plugin uses libraries websocket-client_ .

Plugin version: %s

.. _ESP-12F:           https://en.wikipedia.org/wiki/ESP8266
.. _`NodeMcu 1.0`:     https://en.wikipedia.org/wiki/NodeMCU
.. _`WeMos D1 mini`:   https://wiki.wemos.cc/products:d1:d1_mini
.. _websocket-client:  https://pypi.python.org/pypi/websocket-client
''' % version,
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=9817",
)

from time import time as ttime
from datetime import datetime as dtdt
from threading import Thread
from base64 import b64encode
from copy import deepcopy as cpy
from json import loads, dumps
from random import randrange
from eg.WinApi.Dynamic import CreateEvent, SetEvent
from os.path import split, abspath

mod_pth = abspath(split(__file__)[0])
from sys import path as syspath

syspath.append(mod_pth + "\\lib")
from websocket_0440 import WebSocketApp

# from locale import setlocale, strcoll, LC_ALL
# import logging
# logging.basicConfig()
# setlocale(LC_ALL, "")

ACV = wx.ALIGN_CENTER_VERTICAL
DEFAULT_WAIT = 35.0
PINSTATES = ("LOW", "HIGH")


# ===============================================================================

class WebSocketClient(WebSocketApp):
    def __init__(self, url, plugin):
        WebSocketApp.__init__(
            self,
            url,
            on_open=plugin.on_open,
            on_message=plugin.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.plugin = plugin

    def on_error(self, _, error):
        eg.PrintError(self.plugin.text.wsError % (self.plugin.info.eventPrefix, error))
        self.plugin.stopWatchdog()
        self.watchdog = eg.scheduler.AddTask(5.0, self.plugin.watcher)

    def on_close(self, _):
        if self.plugin.connFlag:
            self.plugin.TriggerEvent(self.plugin.text.wsClosedEvt)
            self.plugin.connFlag = False

    def start(self):
        auth = None
        if self.plugin.proxy[0] != "":
            host = str(self.plugin.proxy[0])
            port = self.plugin.proxy[1]
            if self.plugin.proxy[2] != "":
                auth = (
                    str(self.plugin.proxy[2]),
                    str(self.plugin.proxy[3].Get())
                )
        else:
            host = None
            port = None
        self.run_forever(
            http_proxy_host=host,
            http_proxy_port=port,
            http_proxy_auth=auth
        )
    # ===============================================================================


class Text:
    debug = "Logging level:"
    debug2 = "(the higher the number, the more message writes ...)"
    prefix = "Event prefix:"
    host = "Host address:"
    port = "TCP/IP port:"
    password = "Password:"
    server = "ESP-IO general settings"
    cancel = "Cancel"
    ok = "OK"
    headers = (
        "Host:",
        "Port:",
        "Username:",
        "Password:",
    )
    proxyInfo = """If the proxy server does not require authentication, 
leave the Username and Password entries blank."""
    proxyTitle = "Proxy settings"
    reconnect = "Haven't seen a nop lately, reconnecting"
    config = "ConfigLoaded"
    wsOpenedEvt = "WebSocketOpened"
    wsClosedEvt = "WebSocketClosed"
    wsError = u"%s: WebSocket error: %s"
    wsMssg = "WebSocket message: %s"
    input = '%s: Pin "%s" is input !'
    unknmsg = '%s: Unknown message: %s'


# ===============================================================================

class ESP_IO(eg.PluginClass):
    wsC = None
    text = Text
    prefix = None
    connFlag = False
    msgWait = 0
    lastMessage = 0
    watchdog = None
    debug = 5
    proxy = ("",)
    gpios = {}
    queryData = {}
    tz = 0.0

    def __init__(self):
        self.AddActionsFromList(ACTIONS)

    def GetToken(self):
        flag = True
        while flag:
            token = format(randrange(16777216), '06x')
            flag = token in self.queryData
        event = CreateEvent(None, 0, 0, None)
        self.queryData[token] = event
        return token

    def SendPinCommand(self, cmd, pin, value):
        gpio = None
        for key, val in self.gpios.items():
            if val[0] == pin:
                gpio = key
                break
        if gpio is None:
            return
        token = self.GetToken()
        evt = self.queryData[token]
        msg = {"command": cmd, "id": gpio, "token": token}
        if value is not None:
            msg["value"] = value
        msg = dumps(msg)
        if cmd == "getpinstate" or self.gpios[gpio][1]:  # get value or pin is output ?
            try:
                self.wsC.send(msg)
                eg.actionThread.WaitOnEvent(evt)
                data = self.queryData[token]
                del self.queryData[token]
            except:
                del self.queryData[token]
                data = {}
            return data
        else:
            eg.PrintError(self.text.input % (self.info.eventPrefix, pin))

    def SendVarCommand(self, cmd, ix, value):
        token = self.GetToken()
        evt = self.queryData[token]
        msg = {"command": cmd, "index": ix, "token": token}
        if value is not None:
            msg["value"] = value
        msg = dumps(msg)
        # if cmd == "getuservar":
        try:
            self.wsC.send(msg)
            eg.actionThread.WaitOnEvent(evt)
            data = self.queryData[token]
            del self.queryData[token]
        except:
            del self.queryData[token]
            data = {}
        return data
        # else:
        #    eg.PrintError(self.text.input % (self.info.eventPrefix, pin))

    def SendTimeCommand(self, cmd):
        token = self.GetToken()
        evt = self.queryData[token]
        msg = {"command": cmd, "token": token}
        if cmd == "settime":
            msg["epoch"] = int(0.5 + ttime() + self.tz * 3600)
        msg = dumps(msg)
        try:
            self.wsC.send(msg)
            eg.actionThread.WaitOnEvent(evt)
            data = self.queryData[token]
            del self.queryData[token]
        except:
            del self.queryData[token]
            data = {}
        return data

    def normalizeURL(self, url, port):
        if not url.startswith("ws://"):
            if url.startswith("http://"):
                url = url.replace("http://", "ws://")
            else:
                url = "ws://" + url
        if not url.endswith("/ws") and not url.endswith("/ws/"):
            if url.endswith("/"):
                url += "ws"
            else:
                url += "/ws"
        elif url.endswith("/ws/"):
            url = url[:-1]
        return url.replace("/ws", ":%i/ws" % port)

    def __start__(
        self,
        prefix=None,
        debug=3,
        host="ws://",
        port=80,
        password="",
        dummy="",
        proxy=["", 0, "", ""]
    ):
        prefix = self.name if prefix is None else prefix
        self.info.eventPrefix = prefix
        self.prefix = prefix
        self.debug = debug
        self.proxy = proxy
        self.connFlag = False
        self.msgWait = DEFAULT_WAIT
        self.lastMessage = ttime()
        self.queryData = {}
        self.debug = debug
        _ = eg.scheduler.AddTask(1.0, self.establishSubscriber)
        self.url = self.normalizeURL(host, port)
        self.port = port
        if not isinstance(password, eg.Password):
            passw = eg.Password(None)
            passw.Set(password)
        else:
            passw = password
        self.password = b64encode(passw.Get())

    def stopWatchdog(self):
        if self.watchdog:
            try:
                eg.scheduler.CancelTask(self.watchdog)
            except:
                pass

    def OnComputerResume(self, dummy):
        self.watchdog = eg.scheduler.AddTask(15.0, self.watcher)

    def OnComputerSuspend(self, dummy):
        self.stopWatchdog()
        if self.wsC:
            self.wsC.close()
        self.wsC = None
        self.ct = None

    def __stop__(self):
        self.stopWatchdog()
        if self.wsC:
            self.wsC.close()
        self.wsC = None
        self.ct = None

    def Log(self, message, level):
        if self.debug >= level:
            print "%s: %s" % (self.info.eventPrefix, message)

    def watcher(self):
        if not self.info.isStarted:
            return
        if (ttime() - self.lastMessage) > self.msgWait:
            self.Log(self.text.reconnect, 2)
            self.msgWait = min(600000, self.msgWait * 2)
            self.refreshWebSocket()
        self.stopWatchdog()
        self.watchdog = eg.scheduler.AddTask(5.0, self.watcher)

    def on_open(self, _):
        self.connFlag = True
        self.TriggerEvent(self.text.wsOpenedEvt)

    def establishSubscriber(self):
        if self.wsC:
            return
        self.wsC = WebSocketClient(self.url, self)
        self.ct = Thread(target=self.wsC.start)
        self.ct.start()
        self.lastMessage = ttime()
        self.stopWatchdog()
        self.watchdog = eg.scheduler.AddTask(0.01, self.watcher)

    def refreshWebSocket(self):
        self.msgWait = DEFAULT_WAIT
        if self.wsC:
            self.wsC.close()
        self.wsC = None
        self.establishSubscriber()

    def on_message(self, _, m):
        if not self.info.isStarted:
            if self.wsC:
                self.wsC.close()
        if m is None:
            return
        try:
            m = loads(m)
            if 'command' in m and m['command'] == 'configfile':
                del m['apwd']
                del m['pswd']
            self.Log(self.text.wsMssg % repr(m), 5)
            self.lastMessage = ttime()
            self.msgWait = DEFAULT_WAIT
        except:
            eg.PrintTraceback()
            self.refreshWebSocket()
            return
        if "token" in m:
            token = m['token']
            event = self.queryData[token]
            del m["token"]
            self.queryData[token] = m
            SetEvent(event)
            return
        if 'command' in m:
            cmd = m['command']
            if cmd == 'nop':
                pass
            elif cmd == 'password':
                self.wsC.send("{'command':'password','password':'%s'}" % self.password)
            elif cmd == 'authorized':
                self.wsC.send("{'command':'getconf'}")
                self.TriggerEvent(self.text.config)
            elif cmd == 'configfile':
                self.tz = float(m['tz'])
                self.gpios = {}
                for item in m['gpios']:
                    if item[1] and item[0] != m['wled']:
                        self.gpios[item[0]] = (item[2], item[3])  # title, out
                self.wsC.send("{'command':'pinlist'}")
            elif cmd == 'pinlist':
                pass
            elif cmd == 'change':
                suffix = m['title']
                if m['id'] != 'A0':
                    suffix += ".%s" % PINSTATES[m['value']]
                self.TriggerEvent(suffix, payload=m['value'])
        else:
            eg.PrintNotice(unknmsg % (self.info.eventPrefix, repr(m)))

    def Configure(
        self,
        prefix=None,
        debug=3,
        host="ws://",
        port=80,
        password="",
        dummy="",
        proxy=["", 0, "", ""]
    ):
        prefix = self.name if prefix is None else prefix
        if not isinstance(proxy[3], eg.Password):
            p = eg.Password(None)
            p.Set("")
            proxy[3] = p
        text = self.text
        panel = eg.ConfigPanel(self)
        panel.proxy = cpy(proxy)

        if not isinstance(password, eg.Password):
            passw = eg.Password(None)
            passw.Set(password)
        else:
            passw = password
        debugLabel2 = wx.StaticText(panel, -1, text.debug2)
        debugCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            debug,
            min=1,
            max=5
        )
        debugSizer = wx.BoxSizer(wx.HORIZONTAL)
        debugSizer.Add(debugCtrl, 0, wx.RIGHT, 5)
        debugSizer.Add(debugLabel2, 0, flag=ACV)
        prefixCtrl = panel.TextCtrl(prefix)
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, min=1, max=65535)
        passwordCtrl = wx.TextCtrl(panel, -1, passw.Get(), style=wx.TE_PASSWORD)
        labels = (
            panel.StaticText(text.prefix),
            panel.StaticText(text.host),
            panel.StaticText(text.port),
            panel.StaticText(text.password),
            panel.StaticText(text.debug)
        )
        eg.EqualizeWidths(labels)
        topSizer = wx.FlexGridSizer(2, 2, 5, 5)
        topSizer.Add(labels[0], 0, ACV | wx.LEFT, 10)
        topSizer.Add(prefixCtrl, 0, wx.EXPAND | wx.LEFT, 5)
        topSizer.Add(labels[4], 0, ACV | wx.LEFT, 10)
        topSizer.Add(debugSizer, 0, wx.EXPAND | wx.LEFT, 5)
        sizer = wx.FlexGridSizer(3, 2, 5, 5)
        sizer.AddGrowableCol(1)
        sizer.Add(labels[1], 0, ACV)
        sizer.Add(hostCtrl, 0)
        sizer.Add(labels[2], 0, ACV)
        sizer.Add(portCtrl)
        sizer.Add(labels[3], 0, ACV)
        sizer.Add(passwordCtrl)
        staticBox = wx.StaticBox(panel, label=text.server)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 5)
        panel.sizer.Add(topSizer, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)
        proxyBtn = wx.Button(panel.dialog, -1, text.proxyTitle)

        def onProxyBtn(evt):
            dlg = ProxyDialog(
                parent=panel,
                plugin=self,
                labels=text.headers,
                data=panel.proxy,
            )
            wx.CallAfter(
                dlg.ShowProxyDlg, text.proxyTitle
            )
            evt.Skip()

        proxyBtn.Bind(wx.EVT_BUTTON, onProxyBtn)
        panel.dialog.buttonRow.Add(proxyBtn)

        while panel.Affirmed():
            oldPassw = passw.Get()
            newPassw = passwordCtrl.GetValue()
            if oldPassw != newPassw:
                passw.Set(newPassw)
                dummy = str(ttime())
            if proxy[3].Get() != panel.proxy[3].Get():
                dummy = str(ttime())
            panel.SetResult(
                prefixCtrl.GetValue(),
                debugCtrl.GetValue(),
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                passw,
                dummy,
                panel.proxy
            )


# ===============================================================================

class ProxyDialog(wx.Frame):
    def __init__(
        self,
        parent,
        plugin,
        labels,
        data,
    ):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL | wx.RESIZE_BORDER,
            name="ProxyDialog"
        )
        self.panel = parent
        self.plugin = plugin
        self.text = plugin.text
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.labels = labels
        self.data = data

    def ShowProxyDlg(self, title):
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
        sizer = wx.GridBagSizer(5, 5)
        for row in range(rows):
            sizer.Add(wxst(labels[row]), (row, 0), flag=ACV)
            if row not in (1, 3):
                txtCtrl = wx.TextCtrl(panel, -1, data[row])
            elif row == 1:
                txtCtrl = eg.SpinIntCtrl(
                    panel,
                    -1,
                    data[row],
                    min=0,
                    max=65535
                )
            elif row == 3:
                self.password = eg.Password(data[row])
                txtCtrl = wx.TextCtrl(
                    panel,
                    -1,
                    self.password.Get(),
                    style=wx.TE_PASSWORD
                )
            sizer.Add(txtCtrl, (row, 1), flag=wx.EXPAND)
        info = wxst(text.proxyInfo)
        info.Enable(False)
        sizer.Add(info, (rows, 0), (1, 2), flag=ACV)
        sizer.AddGrowableCol(1)

        line = wx.StaticLine(
            panel,
            -1,
            style=wx.LI_HORIZONTAL
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
        mainSizer.Add(sizer, 1, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(line, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 5)
        mainSizer.Add(btnsizer, 0, wx.EXPAND | wx.RIGHT, 10)
        mainSizer.Add((1, 6))
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
            data = []
            children = sizer.GetChildren()
            for child in range(1, len(children), 2):
                ctrl = children[child].GetWindow()
                if child != 7:
                    data.append(ctrl.GetValue())
                else:
                    self.password.Set(ctrl.GetValue())
                    data.append(self.password)
            self.GetParent().proxy = data
            self.Close()

        btn1.Bind(wx.EVT_BUTTON, onOk)

        def onCancel(evt):
            self.Close()

        btn2.Bind(wx.EVT_BUTTON, onCancel)

        mainSizer.Layout()
        w, h = self.GetSize()
        self.SetSize((max(w, 300), h))
        self.SetMinSize((max(w, 300), h))
        self.Raise()
        self.MakeModal(True)
        self.Centre()
        self.Show()

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler


# ===============================================================================

class pinCommand(eg.ActionBase):
    class text:
        pin = "Pin:"
        val = "State:"

    def __call__(self, pin="", val=0):
        pin = eg.ParseString(pin)
        data = self.plugin.SendPinCommand(
            self.value,
            pin,
            val if self.value == "setpinstate" else None
        )
        if data is not None:
            if "A0" not in self.plugin.gpios or pin != self.plugin.gpios["A0"][0]:
                return PINSTATES[data['value']]
            else:
                return data['value']

    def GetLabel(self, pin="", val=0):
        if self.value == "setpinstate":
            return "%s: %s %s" % (self.name, pin, PINSTATES[val])
        else:
            return "%s: %s" % (self.name, pin)

    def Configure(self, pin="", val=0):
        text = self.text
        panel = eg.ConfigPanel()
        pinLabel = wx.StaticText(panel, -1, text.pin)
        if len(self.plugin.gpios.values()):
            if self.value == "getpinstate":
                choices = [item[0] for item in self.plugin.gpios.values()]
            else:
                choices = [item[0] for item in self.plugin.gpios.values() if item[1]]
            choices.sort()
        else:
            choices = ()  # TEST AND DISABLE ?
        pinCombo = wx.ComboBox(
            panel,
            -1,
            choices=choices,
        )
        pinCombo.SetStringSelection(pin)

        if self.value == "setpinstate":
            valLabel = wx.StaticText(panel, -1, text.val)
            valCtrl = wx.Choice(panel, -1, choices=PINSTATES)
            valCtrl.SetSelection(val)

        sizer = wx.FlexGridSizer(2 if self.value == "setpinstate" else 1, 2, 10, 10)
        sizer.Add(pinLabel, 0, ACV)
        sizer.Add(pinCombo)

        if self.value == "setpinstate":
            sizer.Add(valLabel, 0, ACV)
            sizer.Add(valCtrl)
        panel.sizer.Add(sizer, 0, wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(
                pinCombo.GetValue(),
                valCtrl.GetSelection() if self.value == "setpinstate" else None,
            )


# ===============================================================================

class varCommand(eg.ActionBase):
    class text:
        index = "Index:"
        val = "Value:"

    def __call__(self, index=0, val=""):
        data = self.plugin.SendVarCommand(
            self.value,
            index,
            eg.ParseString(val) if self.value == "setuservar" else None
        )
        if data is not None and 'value' in data:
            return data['value']

    def GetLabel(self, index=0, val=""):
        if self.value == "setuservar":
            return "%s: %s: %s" % (self.name, index, val)
        else:
            return "%s: %s" % (self.name, index)

    def Configure(self, index=0, val=""):
        text = self.text
        panel = eg.ConfigPanel()
        ixLabel = wx.StaticText(panel, -1, text.index)
        ixCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            index,
            min=0,
            max=7
        )

        if self.value == "setuservar":
            valLabel = wx.StaticText(panel, -1, text.val)
            valCtrl = wx.TextCtrl(panel, -1, val)

        sizer = wx.FlexGridSizer(2 if self.value == "setuservar" else 1, 2, 10, 10)
        sizer.AddGrowableCol(1)
        sizer.Add(ixLabel, 0, ACV)
        sizer.Add(ixCtrl)

        if self.value == "setuservar":
            sizer.Add(valLabel, 0, ACV)
            sizer.Add(valCtrl, 0, wx.EXPAND)
        panel.sizer.Add(sizer, 0, wx.ALL | wx.EXPAND, 10)

        while panel.Affirmed():
            panel.SetResult(
                ixCtrl.GetValue(),
                valCtrl.GetValue() if self.value == "setuservar" else "",
            )


# ===============================================================================

class timeCommand(eg.ActionBase):

    def __call__(self):
        cmd = self.value if self.value != "timediff" else "gettime"
        res = self.plugin.SendTimeCommand(cmd)['epoch'] \
              - int(3600 * self.plugin.tz)
        if self.value != "timediff":
            try:
                dvtm = dtdt.fromtimestamp(res).strftime('%Y-%m-%d %H:%M:%S')
                return dvtm
            except ValueError:
                return "Undefined"
        else:
            return int(0.5 + ttime()) - res


# ===============================================================================

ACTIONS = (
    (pinCommand,
     "GetPinState",
     "Get pin state",
     "Get pin state.",
     "getpinstate"
     ),
    (pinCommand,
     "TogglePinState",
     "Toggle pin state",
     "Toggles pin state.",
     "toggle"
     ),
    (pinCommand,
     "SetPinState",
     "Set pin state",
     "Set pin state",
     "setpinstate"
     ),
    (varCommand,
     "GetUserVar",
     "Get user variable",
     "Get user variable.",
     "getuservar"
     ),
    (timeCommand,
     "GetDeviceTime",
     "Get device time",
     "Get device time.",
     "gettime"
     ),
    (timeCommand,
     "GetTimeDiff",
     "Get time difference",
     "Get time difference.",
     "timediff"
     ),
    (timeCommand,
     "SetDeviceTime",
     "Set device time",
     "Set device time.",
     "settime"
     ),
)
# ===============================================================================
