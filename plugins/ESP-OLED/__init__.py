# -*- coding: utf-8 -*-
version = "0.0.1"

# plugins/ESP-OLED/__init__.py
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
# 0.0.1 by Pako 2017-11-09 12:28 GMT+1
#     - added forum url
# 0.0.0 by Pako 2017-11-08 12:34 GMT+1
#     - first public version
#===============================================================================

eg.RegisterPlugin(
    name = "ESP-OLED",
    author = "Pako",
    version = version,
    kind = "external",
    guid = "{DF92D654-CA37-4E46-812A-AD8A518D6403}",
    createMacrosOnAdd = True,
    canMultiLoad = True,
    icon = (
        "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"
        "5V8AAAAASUVORK5CYII="
    ),
    description = ur'''<rst>
Remote OLED display, controlled by ESP-12F_ (a mini wifi board with 4MB flash based on 
ESP-8266EX).

The project assumes the use of `NodeMcu 1.0`_ or `WeMos D1 mini`_ boards with
FW "ESP-OLED".

The device may be in a completely different network than EventGhost. 
Only Internet connectivity at both ends is a condition. 
No public IP or VPN or port redirection is needed. 
This is possible thanks to the Beebotte_ service.

.. image:: NodeMcu700x525.png
.. image:: WeMos403x345.png
.. image:: Display700x700.png

Press any of the three buttons will trigger an event in EventGhost.

Plugin uses libraries bbt_python_ and paho.mqtt.python_.

Plugin version: %s

.. _ESP-12F:           https://en.wikipedia.org/wiki/ESP8266
.. _`NodeMcu 1.0`:     https://en.wikipedia.org/wiki/NodeMCU
.. _`WeMos D1 mini`:   https://wiki.wemos.cc/products:d1:d1_mini
.. _Beebotte:          https://beebotte.com
.. _bbt_python:        https://github.com/beebotte/bbt_python
.. _paho.mqtt.python:  https://github.com/eclipse/paho.mqtt.python
''' % version,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=9928",
)

import paho.mqtt.client as mqtt
from time import time as ttime
from threading import Thread
from base64 import b64encode
from copy import deepcopy as cpy
from json import loads
from random import randrange
from eg.WinApi.Dynamic import CreateEvent, SetEvent
from os.path import split, abspath
mod_pth = abspath(split(__file__)[0])
from sys import path as syspath
syspath.append(mod_pth + "\\lib")
from beebotte import *
import time
import paho.mqtt.client as mqtt

from locale import setlocale, strcoll, LC_ALL
#import logging
#logging.basicConfig()
#setlocale(LC_ALL, "")

ACV           = wx.ALIGN_CENTER_VERTICAL
WATCHDOG_TIME  = 35.0
PINSTATES     = ("LOW", "HIGH")
MQTT_HOST     = "mqtt.beebotte.com"
MQTT_PORT     = 1883
SLEEP_TIME    = 60
#===============================================================================

class Text:
    debug = "Logging level:"
    debug2 = "(the higher the number, the more message writes ...)"
    prefix = "Event prefix:"
    password = "Password:"
    label = "Beebotte settings"
    channel = "Channel"
    cmdrsrc = "Command resource"
    msgrsrc = "Message resource"
    apikey = "API key"
    secretkey = "Secret key"
    token = "Channel token"
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
    connlost = 'ConnectionLost'
    config = "Connected"
    addLstnr = 'Adding MQTT messaging listener'
    unknmsg = '%s: Unknown message: "%s"'
    input = '%s: Pin "%s" is input !'
#===============================================================================

class ESP_OLED(eg.PluginClass):
    client = None
    text = Text
    prefix = None
    lastMessage = 0
    watchdog = None
    debug = 3
    proxy = ("",)
    gpios = {}
    queryData = {}
    cfgFlag = False
    connFlag = False
    messages = ["", ""]

    def __init__(self):
        self.AddActionsFromList(ACTIONS)


    def SendMessage(self, message):
        msg = {"command":"msg","msg":message}
        try:
            self.resource.publish(msg)
            if message != self.messages[1]:
                self.messages[0] = self.messages[1]
            self.messages[1] = message
        except:
            eg.PrintTraceback()       


    def startClient(self):
        if self.client is not None:
            try:
                self.client.unsubscribe(str("%s/%s" % (self.channel, self.msgrsrc)))
            except:
                pass
            try:
                self.client.disconnect()
            except:
                pass
        self.client = None
        del self.client

        #Will be called upon reception of CONNACK response from the server.
        def on_connect(client, data, rc):
            client.subscribe(str("%s/%s" % (self.channel, self.msgrsrc)), 1)
            self.cfgFlag = True

        def on_message(client, data, msg):
            pld = loads(msg.payload)
            if isinstance(pld, dict) and "data" in pld:
                if isinstance(pld["data"], dict) and 'message' in pld["data"]:
                    m = pld["data"]
                    mssg = m['message']
                    self.Log('message: %s' % m['message'], 5)
                    self.lastMessage = ttime()
                    if mssg == 'nop':
                        if self.cfgFlag:
                            self.resource.publish({'command':'getconf'})
                    elif mssg == 'config':
                            self.cfgFlag = False
                            self.connFlag = True
                            self.TriggerEvent(self.text.config)
                    elif mssg == 'button': #{u'message': u'button', u'button': 0}
                        self.TriggerEvent("Button.%i" % (1 + int(m['button'])))
                    else:
                        eg.PrintNotice(self.text.unknmsg % (self.info.eventPrefix, repr(m)))
                else:
                    eg.PrintNotice(self.text.unknmsg % (self.info.eventPrefix, repr(pld["data"])))
            else:
                eg.PrintNotice(self.text.unknmsg % (self.info.eventPrefix, repr(pld)))

        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message         
        self.client.username_pw_set("token:%s" % self.TOKEN)
        try:
            self.client.connect(MQTT_HOST, MQTT_PORT, SLEEP_TIME)
        except  Exception, exc:
            eg.PrintError("%s: %s" % (self.info.eventPrefix, exc.args[1]))
        self.client.loop_start()


    def __start__(
        self,
        prefix = None,
        debug = 3,
        channel = "",
        cmdrsrc = "",
        msgrsrc = "",
        bbt_tkn = "",
        bbt_api = "",
        bbt_secret = "",
        dummy = "",
        proxy = ["", 0, "", ""]
    ):
        prefix = self.name if prefix is None else prefix
        self.info.eventPrefix = prefix
        self.debug = debug
        self.proxy = proxy
        self.cfgFlag = False
        self.lastMessage = ttime()
        self.queryData = {}
        self.channel = channel
        self.msgrsrc = msgrsrc
        if not isinstance(bbt_tkn, eg.Password):
            tkn = eg.Password(None)
            tkn.Set(bbt_tkn)
        else:
            tkn = bbt_tkn
        self.TOKEN = tkn.Get()

        if not isinstance(bbt_api, eg.Password):
            api = eg.Password(None)
            api.Set(bbt_api)
        else:
            api = bbt_api
        API_KEY = api.Get()

        if not isinstance(bbt_secret, eg.Password):
            secret = eg.Password(None)
            secret.Set(bbt_secret)
        else:
            secret = bbt_secret
        SECRET_KEY = secret.Get()
        bbt = BBT(API_KEY, SECRET_KEY)
        self.resource = Resource(bbt, self.channel, cmdrsrc)
        self.watchdog = eg.scheduler.AddTask(WATCHDOG_TIME, self.watcher)
        self.startClient()


    def stopWatchdog(self):
        if self.watchdog:
            try:
                eg.scheduler.CancelTask(self.watchdog)
            except:
                pass


    def OnComputerResume(self, dummy):
        self.cfgFlag = False
        self.connFlag = False
        self.gpios = {}
        self.watchdog = eg.scheduler.AddTask(5.0, self.watcher)


    def OnComputerSuspend(self, dummy):
        self.stopWatchdog()
  

    def __stop__(self):
        self.stopWatchdog()
        try:
            self.client.unsubscribe(str("%s/%s" % (self.channel, self.msgrsrc)))
        except:
            pass
        try:
            self.client.disconnect()
        except:
            pass
        self.client = None


    def Log(self, message, level):
        if self.debug >= level:
            print "%s: %s" % (self.info.eventPrefix, message)


    def watcher(self):
        if not self.info.isStarted:
            return
        self.stopWatchdog()
        if (ttime() - self.lastMessage) > WATCHDOG_TIME:
            if self.connFlag:
                self.TriggerEvent(self.text.connlost)
                self.gpios = {}
                self.connFlag = False
            self.startClient()
        self.watchdog = eg.scheduler.AddTask(WATCHDOG_TIME, self.watcher)


    def Configure(
        self,
        prefix = None,
        debug = 3,
        channel = "",
        cmdrsrc = "",
        msgrsrc = "",
        bbt_tkn = "",
        bbt_api = "",
        bbt_secret = "",
        dummy = "",
        proxy = ["", 0, "", ""]
    ):
        prefix = self.name if prefix is None else prefix
        if not isinstance(proxy[3], eg.Password):
            p = eg.Password(None)
            p.Set("")
            proxy[3] = p
        if not isinstance(bbt_tkn, eg.Password):
            tkn = eg.Password(None)
            tkn.Set("")
            bbt_tkn = tkn
        tkn = bbt_tkn
        if not isinstance(bbt_api, eg.Password):
            api = eg.Password(None)
            api.Set("")
            bbt_api = api
        api = bbt_api
        if not isinstance(bbt_secret, eg.Password):
            secret = eg.Password(None)
            secret.Set("")
            bbt_secret = secret
        secret = bbt_secret
        text = self.text
        panel = eg.ConfigPanel(self)
        panel.proxy = cpy(proxy)

        debugLabel2 = wx.StaticText(panel, -1, text.debug2)
        debugCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            debug,
            min = 1,
            max = 5
        )
        debugSizer = wx.BoxSizer(wx.HORIZONTAL)
        debugSizer.Add(debugCtrl, 0, wx.RIGHT, 5)
        debugSizer.Add( debugLabel2, 0, flag = ACV)
        prefixCtrl = panel.TextCtrl(prefix)
        labels = (
            panel.StaticText(text.prefix),
            panel.StaticText(text.debug),
            panel.StaticText(text.channel),
            panel.StaticText(text.cmdrsrc),
            panel.StaticText(text.msgrsrc),
            panel.StaticText(text.apikey),
            panel.StaticText(text.secretkey),
            panel.StaticText(text.token)
        )
        channelCtrl = wx.TextCtrl(panel, -1, channel)
        cmdrsrcCtrl = wx.TextCtrl(panel, -1, cmdrsrc)
        msgrsrcCtrl = wx.TextCtrl(panel, -1, msgrsrc)
        apiCtrl = wx.TextCtrl(panel, -1, bbt_api.Get(), style = wx.TE_PASSWORD)
        secretCtrl = wx.TextCtrl(panel, -1, bbt_secret.Get(), style = wx.TE_PASSWORD)
        tokenCtrl = wx.TextCtrl(panel, -1, bbt_tkn.Get(), style = wx.TE_PASSWORD)
        eg.EqualizeWidths(labels) 
        topSizer = wx.FlexGridSizer(6, 2, 5, 5)
        topSizer.Add(labels[0], 0, ACV|wx.LEFT,10)
        topSizer.Add(prefixCtrl,0,wx.EXPAND|wx.LEFT,5)
        topSizer.Add(labels[1], 0, ACV|wx.LEFT,10)
        topSizer.Add(debugSizer,0,wx.EXPAND|wx.LEFT,5)
        sizer = wx.FlexGridSizer(6, 2, 5, 5)
        sizer.AddGrowableCol(1)        
        sizer.Add(labels[2], 0, ACV)
        sizer.Add(channelCtrl,0,wx.EXPAND)
        sizer.Add(labels[3], 0, ACV)
        sizer.Add(cmdrsrcCtrl,0,wx.EXPAND)
        sizer.Add(labels[4], 0, ACV)
        sizer.Add(msgrsrcCtrl,0,wx.EXPAND)
        sizer.Add(labels[5], 0, ACV)
        sizer.Add(apiCtrl,0,wx.EXPAND)
        sizer.Add(labels[6], 0, ACV)
        sizer.Add(secretCtrl,0,wx.EXPAND)
        sizer.Add(labels[7], 0, ACV)
        sizer.Add(tokenCtrl,0,wx.EXPAND)
        staticBox = wx.StaticBox(panel, label=text.label)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)
        panel.sizer.Add(topSizer, 0, wx.EXPAND|wx.TOP|wx.BOTTOM,5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 10)
        proxyBtn = wx.Button(panel.dialog, -1, text.proxyTitle)

        def onProxyBtn(evt):
            dlg = ProxyDialog(
                parent = panel,
                plugin = self,
                labels = text.headers,
                data = panel.proxy,
            )
            wx.CallAfter(
                dlg.ShowProxyDlg, text.proxyTitle
            )
            evt.Skip()
        proxyBtn.Bind(wx.EVT_BUTTON, onProxyBtn)
        panel.dialog.buttonRow.Add(proxyBtn)
        while panel.Affirmed():
            oldTkn = tkn.Get()
            newTkn = tokenCtrl.GetValue()
            if oldTkn != newTkn:
                tkn.Set(newTkn)
                dummy = str(ttime())
            oldApi = api.Get()
            newApi = apiCtrl.GetValue()
            if oldApi != newApi:
                api.Set(newApi)
                dummy = str(ttime())
            oldSecret = secret.Get()
            newSecret = secretCtrl.GetValue()
            if oldSecret != newSecret:
                secret.Set(newSecret)
                dummy = str(ttime())
            if proxy[3].Get() != panel.proxy[3].Get():
                dummy = str(ttime())
            panel.SetResult(
                prefixCtrl.GetValue(),
                debugCtrl.GetValue(),
                channelCtrl.GetValue(),
                cmdrsrcCtrl.GetValue(),
                msgrsrcCtrl.GetValue(),
                tkn,
                api,
                secret,
                dummy,
                panel.proxy
           )
#===============================================================================

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
            style = wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL|wx.RESIZE_BORDER,
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
            sizer.Add(wxst(labels[row]), (row, 0), flag = ACV)
            if row not in (1, 3):
                txtCtrl = wx.TextCtrl(panel, -1, data[row])
            elif row == 1:
                txtCtrl = eg.SpinIntCtrl(
                    panel,
                    -1,
                    data[row],
                    min = 0,
                    max = 65535
                )
            elif row == 3:
                self.password = eg.Password(data[row])
                txtCtrl = wx.TextCtrl(
                    panel,
                    -1,
                    self.password.Get(),
                    style = wx.TE_PASSWORD
                )
            sizer.Add(txtCtrl, (row, 1), flag = wx.EXPAND)
        sizer.AddGrowableCol(1)
        info = wxst(text.proxyInfo)
        info.Enable(False)
        sizer.Add(info, (rows, 0), (1, 2), flag = ACV) 

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

#===============================================================================

class SendMessage(eg.ActionBase):

    class text:
        label = "Message:"
        

    def __call__(self, message = ""):
        message = eg.ParseString(message)
        if len(message)>305:
            eg.PrintNotice("Message too long. Shortened to 300 characters.")
        self.plugin.SendMessage(message[:305])


    def Configure(
        self,
        message = ""
    ):
        panel = eg.ConfigPanel()
        panel.GetParent().GetParent().SetIcon(self.plugin.info.icon.GetWxIcon())
        label = wx.StaticText(panel, -1, self.text.label)
        ctrl = wx.TextCtrl(panel, -1, message, style = wx.TE_MULTILINE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, 0, wx.BOTTOM, 8)
        sizer.Add(ctrl, 1, wx.EXPAND)
        panel.sizer.Add(sizer, 1, wx.EXPAND|wx.ALL, 10)
  
        while panel.Affirmed():
            panel.SetResult(
                ctrl.GetValue(),
            )
#===============================================================================

class ResendMessage(eg.ActionBase):

    def __call__(self):
        msg = self.plugin.messages[self.value]
        if msg!="":
            self.plugin.SendMessage(msg)
#===============================================================================

ACTIONS = (    
    (SendMessage,
        "SendMessage",
        "Send message",
        "Sends message.",
        None
    ),
    (ResendMessage,
        "ResendMessage0",
        "Resend the last but one message",
        "Resends the last but one message.",
        0
    ),
    (ResendMessage,
        "ResendMessage1",
        "Resend the last message",
        "Resends the last message.",
        1
    ),
)
#===============================================================================
